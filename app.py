from flask import Flask, request, render_template, jsonify, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename

from models.detector import is_term_sheet
from models.extractor import extract_data
from models.validator import validate_term_sheet
from models.summarizer import generate_summary
from utils.ocr import perform_ocr
from utils.file_handler import read_file_content, get_file_extension

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory storage for processed results
processed_results = {}

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'txt', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if files were uploaded
    if 'termsheet' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['termsheet']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Supported types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    # Handle the file
    filename = secure_filename(file.filename)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
    file.save(file_path)
    
    # Get reference template if provided
    reference_template = None
    if 'reference' in request.files and request.files['reference'].filename != '':
        ref_file = request.files['reference']
        if allowed_file(ref_file.filename):
            ref_filename = secure_filename(ref_file.filename)
            ref_path = os.path.join(app.config['UPLOAD_FOLDER'], f"ref_{file_id}_{ref_filename}")
            ref_file.save(ref_path)
            reference_template = read_file_content(ref_path)
    
    # Process based on file type and user choice
    file_ext = get_file_extension(file_path)
    use_ocr = request.form.get('use_ocr') == 'true'
    
    # Extract text content
    if use_ocr and file_ext in ['jpg', 'jpeg', 'png', 'pdf']:
        text_content = perform_ocr(file_path)
    else:
        text_content = read_file_content(file_path)
    
    # Validate if it's a term sheet
    if not is_term_sheet(text_content):
        return jsonify({'error': 'The uploaded file does not appear to be a valid term sheet'}), 400
    
    # Process the term sheet
    extracted_data = extract_data(text_content)
    validation_results = validate_term_sheet(extracted_data, reference_template)
    summary = generate_summary(text_content)
    
    # Store results
    result = {
        'file_id': file_id,
        'filename': filename,
        'extracted_data': extracted_data,
        'validation_results': validation_results,
        'summary': summary
    }
    processed_results[file_id] = result
    
    return jsonify({'file_id': file_id, 'redirect': url_for('results', file_id=file_id)})

@app.route('/results/<file_id>')
def results(file_id):
    if file_id not in processed_results:
        return redirect(url_for('index'))
    
    result = processed_results[file_id]
    return render_template('results.html', result=result)

@app.route('/api/results/<file_id>')
def api_results(file_id):
    if file_id not in processed_results:
        return jsonify({'error': 'Results not found'}), 404
    
    return jsonify(processed_results[file_id])

if __name__ == '__main__':
    app.run(debug=True)