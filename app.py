import logging
import requests
import json
import re
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from collections import OrderedDict

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
GRAPHQL_API_URL = "https://www.instagram.com/api/graphql"

# Utility functions
def format_graphql_json(post_json):
    data = post_json.get('data', {}).get('xdt_shortcode_media', {})
    if not data:
        raise ValueError("This post does not exist")

    # Handling multiple videos in a carousel post
    if 'edge_sidecar_to_children' in data:
        videos = []
        for index, edge in enumerate(data['edge_sidecar_to_children']['edges'], start=1):
            node = edge['node']
            if node.get('is_video'):
                videos.append(extract_video_info(node, index))
        return videos

    # Single video post
    if not data.get('is_video'):
        raise ValueError("This post is not a video")
    return [extract_video_info(data, 1)]


def extract_video_info(video_data, index):
    return OrderedDict([
        ('index', index),
        ('filename', f"ig-video-{video_data.get('id')}.mp4"),
        ('height', str(video_data.get('dimensions', {}).get('height', ''))),
        ('width', str(video_data.get('dimensions', {}).get('width', ''))),
        ('videoUrl', video_data.get('video_url', ''))
    ])


def encode_post_request_data(shortcode):
    requestData = {
        "av": "0",
        "__d": "www",
        "__user": "0",
        "__a": "1",
        "__req": "3",
        "__hs": "19624.HYP:instagram_web_pkg.2.1..0.0",
        "dpr": "3",
        "__ccg": "UNKNOWN",
        "__rev": "1008824440",
        "__s": "xf44ne:zhh75g:xr51e7",
        "__hsi": "7282217488877343271",
        "__dyn": "7xeUmwlEnwn8K2WnFw9-2i5U4e0yoW3q32360CEbo1nEhw2nVE4W0om78b87C0yE5ufz81s8hwGwQwoEcE7O2l0Fwqo31w9a9x-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7-0iK2S3qazo7u1xwIw8O321LwTwKG1pg661pwr86C1mwraCg",
        "__csr": "gZ3yFmJkillQvV6ybimnG8AmhqujGbLADgjyEOWz49z9XDlAXBJpC7Wy-vQTSvUGWGh5u8KibG44dBiigrgjDxGjU0150Q0848azk48N09C02IR0go4SaR70r8owyg9pU0V23hwiA0LQczA48S0f-x-27o05NG0fkw",
        "__comet_req": "7",
        "lsd": "AVqbxe3J_YA",
        "jazoest": "2957",
        "__spin_r": "1008824440",
        "__spin_b": "trunk",
        "__spin_t": "1695523385",
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "PolarisPostActionLoadPostQueryQuery",
        "variables": json.dumps({
            "shortcode": shortcode,
            "fetch_comment_count": "null",
            "fetch_related_profile_media_count": "null",
            "parent_comment_count": "null",
            "child_comment_count": "null",
            "fetch_like_count": "null",
            "fetch_tagged_user_count": "null",
            "fetch_preview_comment_count": "null",
            "has_threaded_comments": "false",
            "hoisted_comment_id": "null",
            "hoisted_reply_id": "null",
        }),
        "server_timestamps": "true",
        "doc_id": "10015901848480474",
    }
    return urlencode(requestData)
    

def fetch_from_graphql(post_id, timeout=5):
    API_URL = "https://www.instagram.com/api/graphql"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-FB-Friendly-Name": "PolarisPostActionLoadPostQueryQuery",
        "X-CSRFToken": "RVDUooU5MYsBbS1CNN3CzVAuEP8oHB52",
        "X-IG-App-ID": "1217981644879628",
        "X-FB-LSD": "AVqbxe3J_YA",
        "X-ASBD-ID": "129477",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
    }

    encoded_data = encode_post_request_data(post_id)
    try:
        response = requests.post(GRAPHQL_API_URL, headers=headers, data=encoded_data, timeout=timeout)
        if response.status_code != 200:
            return None
        return format_graphql_json(response.json())
    except requests.RequestException as e:
        logging.error(f"Error fetching from GraphQL: {e}")
        return None


def fetch_from_page(post_id, timeout=5):
    post_url = f"https://www.instagram.com/p/{post_id}/"
    headers = {
        # Add necessary headers here
        "accept": "*/*",
        "host": "www.instagram.com",
        "referer": "https://www.instagram.com/",
        "DNT": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    }

    try:
        response = requests.get(post_url, headers=headers, timeout=timeout)
        if response.status_code != 200:
            return None
        return format_page_json(BeautifulSoup(response.content, 'html.parser'))
    except requests.RequestException as e:
        logging.error(f"Error fetching from page: {e}")
        return None
        

def format_page_json(post_html):
    video_elements = post_html.find_all('video')
    if not video_elements:
        return None

    videos = []
    for index, video in enumerate(video_elements, start=1):
        video_url = video.get('src')
        if video_url:
            video_json = OrderedDict([
                ('index', index),
                ('filename', f"ig-video-{index}.mp4"),
                ('height', video.get('height', '')),
                ('width', video.get('width', '')),
                ('videoUrl', video_url)
            ])
            videos.append(video_json)

    return videos


def get_post_id(post_url):
    post_regex = r"^https://(?:www\.)?instagram\.com/p/([a-zA-Z0-9_-]+)/?"
    reel_regex = r"^https://(?:www\.)?instagram\.com/reels?/([a-zA-Z0-9_-]+)/?"
    post_match = re.search(post_regex, post_url)
    if post_match:
        return post_match.group(1)
    reel_match = re.search(reel_regex, post_url)
    if reel_match:
        return reel_match.group(1)
    raise ValueError("Invalid Instagram URL")


# Flask app setup
app = Flask(__name__)

@app.route('/api/video', methods=['GET'])
def get_video():
    post_url = request.args.get('url')
    if not post_url:
        return jsonify({"error": "URL parameter is missing"}), 400

    try:
        post_id = get_post_id(post_url)
        video_info = fetch_from_page(post_id) or fetch_from_graphql(post_id)
        if not video_info:
            raise ValueError("Unable to fetch video information")
        return jsonify(video_info)
    except Exception as e:
        logging.error(f"Error in get_video: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

