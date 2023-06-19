# Stability AI Streamer

This application is a real-time image processing tool that utilizes the Stability AI engine for creative image transformations. It receives webcam frames from the client, processes them, and then sends them to the Stability AI engine for further transformation. The transformed image is then served back to the client. 

**Please note: This application requires Stability API credentials to work, which may incur costs. Use it responsibly to avoid unexpected charges.**

## Installation

1. Make sure you have Python 3.7 or above installed on your system. You can check this by running `python --version` on your command line.

2. Clone this repository to your local machine using `git clone`.

3. Navigate into the project directory using the command line.

4. Create a Python virtual environment with the command `python -m venv venv`.

5. Activate the virtual environment. On Windows, use `venv\Scripts\activate`, and on Unix or MacOS, use `source venv/bin/activate`.

6. Once the virtual environment is activated, install the necessary packages by running `pip install -r requirements.txt`.

## Usage

Before running the server, make sure you have your Stability API key and have set it as an environment variable. You can do this in the terminal with:

```bash
export STABILITY_API_KEY=your_api_key_here

Next, run the server with the command `python server.py`.

The server will start and listen on `http://127.0.0.1:5002`.

To view the client side of the application, open the file `index.html` in a web browser.

Make sure to allow the webpage to access your webcam. The application will then start capturing frames from the webcam, process them, and update the displayed images accordingly.

Please be aware that this application communicates with the Stability AI engine, and costs may be incurred based on the number of requests made to the engine.

## Disclaimer

Use this application at your own risk. Make sure to understand the pricing model of the Stability AI engine before running this application. Be aware that this application is continually making requests to the Stability AI engine while it's running, which may consume a significant number of credits. If you are unsure, contact Stability AI for more information about their pricing model.

This project is for educational and demonstration purposes. It should be used responsibly and with an understanding of the potential costs associated with the Stability AI service.

## License

This project is open source. However, the Stability AI service it uses is a paid service. Please refer to their terms of service for more details.
