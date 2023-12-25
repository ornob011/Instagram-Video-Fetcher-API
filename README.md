# Instagram Video Fetcher API

The Instagram Video Fetche API is a Flask-based web service that provides an efficient way to fetch video information from Instagram posts. It provides an API endpoint that can be used to retrieve video details such as the filename, width, height, and video URLs.

## Features

- Fetch video details from Instagram posts.
- Support for both GraphQL and page scraping methods.
- Robust error handling and logging.

## Getting Started

### Running with Docker

For ease of deployment, the Instagram Video Fetcher API can also be run as a Docker container. This section is intended for end users who wish to run the application without setting up the entire development environment.

#### Prerequisites
- Docker

#### Pulling and Running the Docker Image

1. Pull the Docker Image: 
Download the latest image of the Instagram Video Fetcher API from Docker Hub:

```bash
docker pull ornob011/instagram-fetcher:latest
```

2. Run the Docker Container:
Start the application by running the following command:

```bash
docker run -p 5000:5000 ornob011/instagram-fetcher:latest
```

This command runs the container and maps port 5000 of the container to port 5000 on your host machine, allowing you to access the API via http://localhost:5000.

#### Accessing the Application

Once the container is running, you can access the Instagram Video Fetcher API at `http://localhost:5000`. Use the API endpoint as described in the [below sections](#using-the-api) to fetch video information from Instagram posts.


### Running with Python
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

#### Prerequisites

- Python 3.8 or higher

#### Installation

1. **Clone the Repository**:
   Clone this repository to your local machine using:
   ```bash
   git clone https://github.com/ornob011/Instagram-Video-Fetcher-API
   ```

2. **Install Dependencies**:
    Navigate to the project directory and install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

#### Running the Application

Run the application with the following command:

```bash
python app.py
```

The Flask server will start at http://127.0.0.1:5000/.


#### Using the API
##### Endpoint: Get Video Informations

- URL: /api/video
- Method: GET
- URL Params:
    - Required: url=[string] (The Instragram video URL)

#### Testing the Endpoint
##### Via Web Browser

To test the endpoint via a web browser, simply navigate to the following URL (replace <Instragram_Video_URL> with the actual Instragram video URL):

```bash
http://127.0.0.1:5000/api/video?url=<Instragram_Video_URL>
```

For example:

```bash
http://127.0.0.1:5000/api/video?url=https://www.instagram.com/reel/C09D1y4pEQz/?utm_source=ig_web_copy_link%26igshid=MzRlODBiNWFlZA%3D%3D
```

##### Via cURL

You can also use cURL in your command line:

```bash
curl "http://127.0.0.1:5000/api/video?url=https://www.instagram.com/reel/C09D1y4pEQz/?utm_source=ig_web_copy_link%26igshid=MzRlODBiNWFlZA%3D%3D"
```

##### Via Postman

1. Open Postman: Launch the Postman application on your computer.

2. Create a New Request:
    - Click on the `New` button or `+` tab to start a new request. Set the request method to GET by selecting it from the dropdown menu next to the URL input field.

3. Enter the URL:
    - In the `URL` input field, enter: http://127.0.0.1:5000/api/video

4. Add Query Parameters:
    - Below the `URL` input field, locate the section for entering query parameters.
    - In the `Key` field, enter `url`.
    - In the `Value` field, enter the Instragram video URL. For example: https://www.instagram.com/reel/C09D1y4pEQz/?utm_source=ig_web_copy_link%26igshid=MzRlODBiNWFlZA%3D%3D

5. Send the Request:
    - Click the `Send` button to execute the request.

6. View the Response:
    - The response will be displayed in the lower section of the Postman interface.
    - If successful, you should see a JSON response with the video title and download links.

Here's an illustration of what your Postman setup might look like:

- Method: GET
- URL: http://127.0.0.1:5000/api/video
- Query Params:
    - Key: `url`
    - Value: https://www.instagram.com/reel/C09D1y4pEQz/?utm_source=ig_web_copy_link%26igshid=MzRlODBiNWFlZA%3D%3D

##### Sample Response For Single Video:

The API responds with a JSON object containing the filename, width, height and download link of the video:

```bash
[
    {
        "filename": "ig-video-3259778596195288115.mp4",
        "height": "1333",
        "index": 1,
        "videoUrl": "https://scontent.cdninstagram.com/v/t66.30100-16/10000000_326259600362706_8346032730964966213_n.mp4?_nc_ht=scontent.cdninstagram.com&_nc_cat=106&_nc_ohc=pq2Qvb_VPBwAX9XRgQk&edm=APs17CUBAAAA&ccb=7-5&oh=00_AfDsS1qyk44fFNXyQvEnDK40XyNpEzaGKBlv8ghUXj1sYw&oe=658AC467&_nc_sid=10d13b",
        "width": "750"
    }
]
```

##### Sample Response For Mutiple Videos:

The API responds with a JSON object containing the filename, width, height and download link of the videos:

```bash
[
    {
        "filename": "ig-video-3241488762163645563.mp4",
        "height": "1350",
        "index": 2,
        "videoUrl": "https://scontent.cdninstagram.com/o1/v/t16/f1/m69/GD7i7hIrrKgthFIBAMnHri7fHj1qbpR1AAAF.mp4?efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2Fyb3VzZWxfaXRlbS5jMi4xMDgwLmhpZ2gifQ&_nc_ht=scontent.cdninstagram.com&_nc_cat=101&vs=1523213925184005_3674492696&_nc_vs=HBkcFQIYOnBhc3N0aHJvdWdoX2V2ZXJzdG9yZS9HRDdpN2hJcnJLZ3RoRklCQU1uSHJpN2ZIajFxYnBSMUFBQUYVAALIAQAoABgAGwAVAAAmnMmv7Y229kAVAigCQzMsF0AQIcrAgxJvGBJkYXNoX2hpZ2hfMTA4MHBfdjERAHXuBwA%3D&_nc_rid=d3fe585e6d&ccb=9-4&oh=00_AfBUP6hoo1dXXb0JDlrM9VvlsTBtNyJ2z1jbVbtm0A7LYQ&oe=658AEB9A&_nc_sid=10d13b",
        "width": "1080"
    },
    {
        "filename": "ig-video-3241488767683313106.mp4",
        "height": "1350",
        "index": 3,
        "videoUrl": "https://scontent.cdninstagram.com/o1/v/t16/f1/m69/GGx4BhNMCRdQr9kDAKzfth8qvY9UbpR1AAAF.mp4?efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2Fyb3VzZWxfaXRlbS5jMi4xMDgwLmhpZ2gifQ&_nc_ht=scontent.cdninstagram.com&_nc_cat=104&vs=887184176123330_645947733&_nc_vs=HBkcFQIYOnBhc3N0aHJvdWdoX2V2ZXJzdG9yZS9HR3g0QmhOTUNSZFFyOWtEQUt6ZnRoOHF2WTlVYnBSMUFBQUYVAALIAQAoABgAGwAVAAAmzIKbvemVi0AVAigCQzMsF0AO7ZFocrAhGBJkYXNoX2hpZ2hfMTA4MHBfdjERAHXuBwA%3D&_nc_rid=d3fe593999&ccb=9-4&oh=00_AfDjHeUOnIQRJYf3gxgsaqx6UyXRUartJ1w7N_taniQDiQ&oe=658ABFAF&_nc_sid=10d13b",
        "width": "1080"
    },
    {
        "filename": "ig-video-3241488774847142499.mp4",
        "height": "1350",
        "index": 4,
        "videoUrl": "https://scontent.cdninstagram.com/o1/v/t16/f1/m69/GHydNgdxL0d-2o8YAEzepMBdLR1hbpR1AAAF.mp4?efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2Fyb3VzZWxfaXRlbS5jMi4xMDgwLmhpZ2gifQ&_nc_ht=scontent.cdninstagram.com&_nc_cat=102&vs=1001735390897012_3119641692&_nc_vs=HBkcFQIYOnBhc3N0aHJvdWdoX2V2ZXJzdG9yZS9HSHlkTmdkeEwwZC0ybzhZQUV6ZXBNQmRMUjFoYnBSMUFBQUYVAALIAQAoABgAGwAVAAAm5vr8o%2FD8yz8VAigCQzMsF0AREGJN0vGqGBJkYXNoX2hpZ2hfMTA4MHBfdjERAHXuBwA%3D&_nc_rid=d3fe5a3272&ccb=9-4&oh=00_AfA1-MXzUeqpHxVzVV2EKImfpmlIl616vPr6spBLlDs3aw&oe=658AFC70&_nc_sid=10d13b",
        "width": "1080"
    }
]
```

If an invalid URL is given, the API responds with:

```bash
{
    "error": "Invalid Instagram URL"
}
```

If unable to fetch video information, the API responds with:

```bash
{
    "error": "Unable to fetch video information"
}
```

### Important Notice

#### Warning: This API cannot retrieve download links for private videos on Instragram. It only works with videos that are publicly accessible. If you attempt to fetch links for a private video, the API will not be able to retrieve the necessary data and will return an error message.

Always ensure that the URL provided is for a public Instragram video. This limitation is due to privacy restrictions on Instragram's platform.

### Troubleshooting

- Ensure that the provided URL is a valid Instragram video URL (e.g., https://www.instagram.com/reel/C09D1y4pEQz/?utm_source=ig_web_copy_link%26igshid=MzRlODBiNWFlZA%3D%3D).
- Check if the Flask server is running and accessible.