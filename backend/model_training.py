# model_training.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle
import json

class SchemaGenerator:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = MultiOutputClassifier(
            RandomForestClassifier(n_estimators=100, random_state=42)
        )
        self.field_types = [
            'Text', 'Number', 'Email', 'Phone', 'Checkbox',
            'Currency', 'Date', 'Datetime', 'Picklist',
            'MultiPicklist', 'URL', 'Textarea', 'RichTextarea', 'Lookup'
        ]
        
        # Maximum number of fields to predict
        self.max_fields = 10

    def prepare_training_data(self):
        # Sample training data
        training_data = [
            {
                "prompt": "Create a customer database with name, email, phone and address",
                "fields": [
                    {"name": "name", "type": "Text", "required": True},
                    {"name": "email", "type": "Email", "required": True},
                    {"name": "phone", "type": "Phone", "required": False},
                    {"name": "address", "type": "Textarea", "required": False}
                ]
            },
            {
                "prompt": "Create an employee database with full name, company email, joining date, and salary",
                "fields": [
                    {"name": "full_name", "type": "Text", "required": True},
                    {"name": "company_email", "type": "Email", "required": True},
                    {"name": "joining_date", "type": "Date", "required": True},
                    {"name": "salary", "type": "Currency", "required": True}
                ]
            },
            {
                "prompt": "Make a product catalog with name, price, description, and category",
                "fields": [
                    {"name": "name", "type": "Text", "required": True},
                    {"name": "price", "type": "Currency", "required": True},
                    {"name": "description", "type": "RichTextarea", "required": False},
                    {"name": "category", "type": "Picklist", "required": True}
                ]
            }
            # Add more training examples as needed
        ]

        X = [item["prompt"] for item in training_data]
        
        # Convert fields to numerical format
        y = []
        for item in training_data:
            # Initialize empty field array
            fields_array = np.zeros((self.max_fields, 2))  # [field_type_index, required]
            
            for i, field in enumerate(item["fields"]):
                if i >= self.max_fields:
                    break
                    
                # Convert field type to index
                type_index = self.field_types.index(field["type"])
                required = 1 if field["required"] else 0
                
                fields_array[i] = [type_index, required]
            
            y.append(fields_array)
        
        return np.array(X), np.array(y)

    def train(self):
        X, y = self.prepare_training_data()
        
        # Transform text prompts to numerical features
        X_transformed = self.vectorizer.fit_transform(X)
        
        # Reshape y to work with MultiOutputClassifier
        y_reshaped = y.reshape(y.shape[0], -1)
        
        # Train the model
        self.classifier.fit(X_transformed, y_reshaped)

    def save_model(self, vectorizer_path='vectorizer.pkl', classifier_path='classifier.pkl'):
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        with open(classifier_path, 'wb') as f:
            pickle.dump(self.classifier, f)

    def load_model(self, vectorizer_path='vectorizer.path', classifier_path='classifier.pkl'):
        with open(vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
        
        with open(classifier_path, 'rb') as f:
            self.classifier = pickle.load(f)

    def generate_schema(self, prompt):
        # Transform the prompt
        X_prompt = self.vectorizer.transform([prompt])
        
        # Predict fields
        predictions = self.classifier.predict(X_prompt)
        predictions = predictions.reshape(-1, 2)
        
        # Convert predictions back to schema format
        fields = []
        for i in range(self.max_fields):
            field_type_index = int(predictions[i][0])
            required = bool(predictions[i][1] >= 0.5)
            
            # Skip if it's a zero vector (no field predicted)
            if field_type_index == 0 and not required:
                continue
                
            # Create field
            field = {
                "name": f"field_{i+1}",  # Generic name
                "type": self.field_types[field_type_index],
                "required": required
            }
            fields.append(field)
        
        return {"fields": fields}

if __name__ == "__main__":
    print("Initializing Schema Generator...")
    generator = SchemaGenerator()
    
    print("Training model...")
    generator.train()
    
    print("Saving model...")
    generator.save_model()
    
    print("Testing model...")
    test_prompt = "Create a contact form with name, email, and message"
    result = generator.generate_schema(test_prompt)
    print("Test result:", json.dumps(result, indent=2))
    
    print("Done!")