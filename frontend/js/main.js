// main.js
document.addEventListener('DOMContentLoaded', function() {
    // Navigation
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links and sections
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            // Add active class to clicked link and corresponding section
            this.classList.add('active');
            const sectionId = this.dataset.section;
            document.getElementById(sectionId).classList.add('active');
        });
    });

    // Schema Generator
    const promptInput = document.getElementById('prompt-input');
    const generateBtn = document.getElementById('generate-btn');
    const resultContainer = document.getElementById('result-container');
    const schemaOutput = document.getElementById('schema-output');
    const errorMessage = document.getElementById('error-message');

    generateBtn.addEventListener('click', async function() {
        try {
            const prompt = promptInput.value.trim();
            
            if (!prompt) {
                throw new Error('Please enter a schema description');
            }
            
            errorMessage.style.display = 'none';
            generateBtn.disabled = true;
            generateBtn.textContent = 'Generating...';
            
            const response = await fetch('http://localhost:5000/api/generate-schema', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt })
            });
            
            if (!response.ok) {
                throw new Error('Failed to generate schema');
            }
            
            const data = await response.json();
            
            schemaOutput.textContent = JSON.stringify(data.schema, null, 2);
            resultContainer.style.display = 'block';
            
            // Save to local storage
            saveSchema(prompt, data.schema);
            
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.style.display = 'block';
            
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Schema';
        }
    });

    // File Upload
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const dropzone = uploadArea.querySelector('.dropzone');

    // Handle drag and drop
    dropzone.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.style.borderColor = '#3498db';
    });

    dropzone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.style.borderColor = '#dcdde1';
    });

    dropzone.addEventListener('drop', function(e) {
        e.preventDefault();
        this.style.borderColor = '#dcdde1';
        handleFiles(e.dataTransfer.files);
    });

    // Handle click to upload
    dropzone.addEventListener('click', function() {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    async function handleFiles(files) {
        try {
            errorMessage.style.display = 'none';
            
            const formData = new FormData();
            for (let file of files) {
                if (file.type !== 'text/plain') {
                    throw new Error('Only .txt files are allowed');
                }
                formData.append('files', file);
            }
            
            const response = await fetch('http://localhost:5000/api/bulk-generate', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Failed to process files');
            }
            
            const data = await response.json();
            
            // Save each schema to local storage and display results
            data.results.forEach(result => {
                saveSchema(result.filename, result.schema);
            });
            
            schemaOutput.textContent = JSON.stringify(data.results, null, 2);
            resultContainer.style.display = 'block';
            
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.style.display = 'block';
        }
    }

    // Schema Viewer
    const searchInput = document.getElementById('search-input');
    const schemasList = document.getElementById('schemas-list');
    const schemaDetails = document.getElementById('schema-details');
    const schemaDetailsContent = document.getElementById('schema-details-content');

    // Load and display schemas
    function loadSchemas(searchTerm = '') {
        const schemas = getAllSchemas();
        schemasList.innerHTML = '';
        
        const filteredSchemas = schemas.filter(schema => 
            schema.prompt.toLowerCase().includes(searchTerm.toLowerCase())
        );
        
        filteredSchemas.forEach(schema => {
            const schemaItem = document.createElement('div');
            schemaItem.className = 'schema-item';
            schemaItem.textContent = schema.prompt;
            schemaItem.addEventListener('click', () => displaySchemaDetails(schema));
            schemasList.appendChild(schemaItem);
        });
    }

    // Search functionality
    searchInput.addEventListener('input', function() {
        loadSchemas(this.value);
    });

    // Display schema details
    function displaySchemaDetails(schema) {
        schemaDetailsContent.textContent = JSON.stringify(schema.schema, null, 2);
        schemaDetails.style.display = 'block';
    }

    // Local Storage Functions
    function saveSchema(prompt, schema) {
        const schemas = getAllSchemas();
        schemas.push({
            id: Date.now(),
            timestamp: new Date().toISOString(),
            prompt,
            schema
        });
        localStorage.setItem('schemas', JSON.stringify(schemas));
        loadSchemas(); // Refresh the list
    }

    function getAllSchemas() {
        const schemas = localStorage.getItem('schemas');
        return schemas ? JSON.parse(schemas) : [];
    }

    // Initial load of schemas
    loadSchemas();
});