# Plant Disease Classifier API

This FastAPI application classifies plant diseases based on input images and plant names.

## Prerequisites

- Python 3.6 or later
- Pip package manager

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/plant-disease-classifier.git
   cd plant-disease-classifier

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

1. Run the FastAPI application:
   ```bash
   uvicorn main:app --reload

2. Access the API at 'http://localhost:8000'
3. Send a POST request to analyze a plant:
   ```bash
   curl -X POST "http://localhost:8000/analyze/Tomato" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "image=@path/to/your/plant_image.jpg"
