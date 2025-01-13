# Schema Generator

This repository contains a Flask-based backend and a simple frontend for generating database schemas based on user input. The project allows users to interact with the API and web interface to create and visualize database schemas easily.

## API Endpoints

The backend provides the following API endpoints:

1. **`/api/generate-schema`**
   - Method: `POST`
   - Description: Generate a database schema based on a provided prompt.
   - Example Request:
     ```bash
     curl -X POST http://localhost:5000/api/generate-schema \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Create a customer database with name, email and phone"}'
     ```

2. **`/api/bulk-generate`**
   - Method: `POST`
   - Description: Generate multiple database schemas from bulk input.

## Setting Up the Project

### Backend
1. **Run the Flask Server:**
   ```bash
   python backend/app.py
   ```
   The server will run at [http://127.0.0.1:5000](http://127.0.0.1:5000).

2. **Test the API:**
   - Open your browser and visit [http://127.0.0.1:5000](http://127.0.0.1:5000) to view the API documentation.
   - Use tools like `curl` or Postman to test the endpoints.

### Frontend
1. **Serve the Frontend:**
   - Navigate to the frontend directory:
     ```bash
     cd schema-generator/frontend
     ```
   - Start a simple HTTP server:
     ```bash
     python -m http.server 8000
     ```

2. **Access the Frontend:**
   - Open your browser and go to [http://localhost:8000](http://localhost:8000).

### Output
![img](https://github.com/user-attachments/assets/d36e6802-8df3-45d1-9cbc-e594005d7dc8)



## Adding a Root Route for Documentation
To make the API more user-friendly, you can add a root route to display the API documentation:

1. Modify `app.py` to include the following:
   ```python
   from flask import Flask, jsonify

   app = Flask(__name__)

   @app.route('/')
   def home():
       return jsonify({
           "message": "Welcome to the Schema Generator API!",
           "endpoints": [
               {"route": "/api/generate-schema", "method": "POST"},
               {"route": "/api/bulk-generate", "method": "POST"}
           ]
       })
   ```

2. Stop the current server (if running):
   ```bash
   CTRL+C
   ```
3. Save the changes and restart the server:
   ```bash
   python backend/app.py
   ```
