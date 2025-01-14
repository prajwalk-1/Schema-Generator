from flask import Flask, request, jsonify
from flask_cors import CORS
from model_training import SchemaGenerator
import os

app = Flask(__name__)
CORS(app)

print("Loading model...")
generator = SchemaGenerator()
try:
    generator.load_model()
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading model, training new model...")
    generator.train()
    generator.save_model()
    print("New model trained and saved!")

@app.route('/')
def home():
    return jsonify({
        "message": "Schema Generator API",
        "endpoints": {
            "POST /api/generate-schema": "Generate schema from text prompt",
            "POST /api/bulk-generate": "Generate schemas from uploaded files"
        },
        "example": {
            "endpoint": "/api/generate-schema",
            "method": "POST",
            "body": {
                "prompt": "Create a customer database with name, email and phone"
            }
        }
    })

@app.route('/api/generate-schema', methods=['POST'])
def generate_schema():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        schema = generator.generate_schema(prompt)
        return jsonify({"schema": schema})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bulk-generate', methods=['POST'])
def bulk_generate():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files provided"}), 400
        
        results = []
        files = request.files.getlist('files')
        
        for file in files:
            if file.filename == '':
                continue
                
            prompt = file.read().decode('utf-8')
            schema = generator.generate_schema(prompt)
            
            results.append({
                "filename": file.filename,
                "schema": schema
            })
        
        return jsonify({"results": results})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
