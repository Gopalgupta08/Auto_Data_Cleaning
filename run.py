from app import create_app
from flask import request, jsonify
import pandas as pd

# Create Flask app instance first
app = create_app()

# Define your route after app is created
@app.route('/api/clean', methods=['POST'])
def clean_csv():
    # Check if file part is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Read CSV into pandas
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({'error': f'Failed to read CSV: {e}'}), 400

    # Example cleaning logic (you can replace this)
    df = df.drop_duplicates().fillna('')  # remove duplicates and fill NaNs

    # Return preview of cleaned data (optional)
    preview = df.head(10).to_dict(orient='records')
    return jsonify({
        'message': 'File cleaned successfully!',
        'rows_cleaned': len(df),
        'preview': preview
    })

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
