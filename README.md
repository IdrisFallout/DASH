# DASH
Dynamic Adaptive Streaming over HTTP (DASH) is a standard for streaming video over the Internet. DASH is an adaptive bitrate streaming technique that enables high quality streaming of media content over the Internet delivered from conventional HTTP web servers. Similar to Apple's HTTP Live Streaming (HLS) solution, MPEG-DASH works by breaking the content into a sequence of small HTTP-based file segments, each segment containing a short interval of playback time of content that is potentially many hours in duration, such as a movie or the live broadcast of a sports event.
DASH is the secret sauce behind the success of video streaming services like Netflix and YouTube.

## Installation
To set up the project, you need to follow the following steps:
1. Clone the repository
2. Install the requirements(`pip install -r requirements.txt`)
3. Run `uvicorn main:app --host 0.0.0.0 --port 5000` to start the FastAPI server

## Usage
The API has 2 major endpoints:
1.  '/' :- serves the dash player
2. '/dash' :- serves the dash manifest

## Demo
To see the demo, you can visit [this](http://dash-zdvi.onrender.com) link. Alternatively, you can also run the project locally and visit `http://localhost:5000` to see the demo.
You can also see the stream in media players like VLC by using the following link: `http://localhost:5000/dash` as shown below:

![VLC](screenshots/demo.gif?raw=true "DEMO")

## Future Improvements
Build a YouTube like video streaming service using this API.
