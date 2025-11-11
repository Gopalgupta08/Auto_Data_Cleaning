from flask import Blueprint, request, jsonify, render_template, current_app, send_file
import pandas as pd
import io
from werkzeug.utils import secure_filename
from ..services.cleaner import clean_dataframe

cleaning_bp = Blueprint('cleaning', __name__)

@cleaning_bp.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@cleaning_bp.route('/api/clean', methods=['POST'])
def api_clean():
    if 'file' not in request.files:
        return jsonify({'error': 'no file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'no selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'file type not allowed'}), 400

    filename = secure_filename(file.filename)

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({'error': 'failed to read csv', 'message': str(e)}), 400

    cleaned = clean_dataframe(df, verbose=False)

    buf = io.StringIO()
    cleaned.to_csv(buf, index=False)
    buf.seek(0)

    return send_file(
        io.BytesIO(buf.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'cleaned_{filename}'
    )
