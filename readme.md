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

4. Code to link with Dart  
    ```dart
    import 'package:http/http.dart' as http;
    import 'dart:convert';

    Future<void> analyzePlant(String plantName, String imagePath) async {
    try {
        var request = http.MultipartRequest(
        'POST',
        Uri.parse('http://localhost:8000/analyze/$plantName'), // Replace with your API URL
        );

        request.fields['name'] = plantName;
        request.files.add(
        await http.MultipartFile.fromPath(
            'image',
            imagePath,
        ),
        );

        var response = await request.send();
        if (response.statusCode == 200) {
        var jsonResponse = json.decode(await response.stream.bytesToString());
        String diseaseType = jsonResponse['disease_type'];
        double accuracy = jsonResponse['accuracy'];
        print("Disease Type: $diseaseType");
        print("Accuracy: $accuracy%");
        } else {
        print("Error: ${response.reasonPhrase}");
        }
    } catch (e) {
        print("Error: $e");
    }
    }

    void main() {
    String plantName = "Tomato";
    String imagePath = "/path/to/your/image.jpg"; // Replace with the actual image path

    analyzePlant(plantName, imagePath);
    }
