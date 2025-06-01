# Steganography Web Application

This project is a web application for image steganography that allows users to hide text messages within images. It is implemented using FastAPI and can be easily deployed using Docker.

## Features

- Hide text messages within images (encoding)
- Extract hidden text messages from images (decoding)
- Calculate maximum storable bytes based on image dimensions

## Tech Stack

- Backend: FastAPI (Python)
- Image Processing: OpenCV, NumPy
- Container: Docker

## Installation and Setup

### Running with Docker

1. Ensure Docker and Docker Compose are installed on your system.
2. Run the following command from the project root directory:

```bash
docker-compose up --build
```

### Running Locally

1. Python 3.8 or higher is required.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
cd src
python app.py
```

## Usage

1. Access the application at `http://localhost:8000` in your web browser.
2. To hide text in an image:
   - Upload an image file
   - Enter the text you want to hide
   - Click the "Encode" button
3. To extract hidden text:
   - Upload both the original and encoded images
   - Click the "Decode" button

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── src/
    ├── app.py          # FastAPI application
    ├── encoder.py      # Steganography encoding/decoding logic
    └── public/         # Static files (HTML, CSS, JS)
```

## License

This project is licensed under the MIT License. 