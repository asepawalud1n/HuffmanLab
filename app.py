from flask import Flask, render_template, request, send_file, jsonify, url_for
from werkzeug.utils import secure_filename
import os
import json
import csv
from datetime import datetime
from huffman import HuffmanCoding, calculate_dataset_statistics

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['COMPRESSED_FOLDER'] = 'static/compressed'
app.config['DECOMPRESSED_FOLDER'] = 'static/decompressed'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp'}

# Ensure folders exist
for folder in [app.config['UPLOAD_FOLDER'],
               app.config['COMPRESSED_FOLDER'],
               app.config['DECOMPRESSED_FOLDER']]:
    os.makedirs(folder, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/compress', methods=['POST'])
def compress_single():
    """
    Endpoint untuk kompresi single image

    Returns:
        JSON dengan hasil kompresi atau redirect ke result page
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Kompresi
            huffman = HuffmanCoding()
            result = huffman.compress_image(filepath, app.config['COMPRESSED_FOLDER'])

            # Data untuk template
            data = {
                'success': True,
                'filename': result['filename'],
                'base_name': result['base_name'],
                'original_size_bits': result['original_size'],
                'compressed_size_bits': result['compressed_size'],
                'original_size_kb': result['original_size'] / 8 / 1024,
                'compressed_size_kb': result['compressed_size'] / 8 / 1024,
                'compression_ratio': round(result['compression_ratio'], 2),
                'savings_percent': round((1 - result['compressed_size'] / result['original_size']) * 100, 2),
                'image_shape': result['image_shape'],
                'unique_pixels': result['unique_pixels'],
                'original_image': url_for('static', filename=f'uploads/{filename}'),
                'gray_image': url_for('static', filename=f'compressed/{result["base_name"]}_gray.png'),
                'compressed_file': url_for('static', filename=f'compressed/{result["base_name"]}_compressed.bin'),
                'codes_file': url_for('static', filename=f'compressed/{result["base_name"]}_codes.json'),
                'size_file': url_for('static', filename=f'compressed/{result["base_name"]}_size.txt')
            }

            return render_template('result.html', data=data)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/decompress', methods=['POST'])
def decompress():
    """
    Endpoint untuk dekompresi

    Expects:
        - compressed.bin
        - codes.json
        - size.txt

    Returns:
        Decompressed image file
    """
    if 'bin_file' not in request.files or 'codes_file' not in request.files or 'size_file' not in request.files:
        return jsonify({'error': 'Missing required files (bin, codes, size)'}), 400

    bin_file = request.files['bin_file']
    codes_file = request.files['codes_file']
    size_file = request.files['size_file']

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save uploaded files
    bin_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_{timestamp}.bin')
    codes_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_{timestamp}_codes.json')
    size_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_{timestamp}_size.txt')

    bin_file.save(bin_path)
    codes_file.save(codes_path)
    size_file.save(size_path)

    # Output path
    output_path = os.path.join(app.config['DECOMPRESSED_FOLDER'], f'decompressed_{timestamp}.png')

    try:
        huffman = HuffmanCoding()
        result = huffman.decompress_image(bin_path, codes_path, size_path, output_path)

        # Clean up temp files
        os.remove(bin_path)
        os.remove(codes_path)
        os.remove(size_path)

        return send_file(output_path, mimetype='image/png', as_attachment=True,
                        download_name=f'decompressed_{timestamp}.png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/compress_dataset', methods=['POST'])
def compress_dataset():
    """
    Endpoint untuk kompresi multiple images (dataset)

    Returns:
        HTML page dengan tabel, statistik, dan grafik
    """
    if 'images' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    files = request.files.getlist('images')

    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400

    results = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{timestamp}_{filename}"

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                huffman = HuffmanCoding()
                result = huffman.compress_image(filepath, app.config['COMPRESSED_FOLDER'])
                results.append(result)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

    if not results:
        return jsonify({'error': 'No files were successfully processed'}), 400

    # Calculate statistics
    stats = calculate_dataset_statistics(results)

    # Prepare data for template
    table_data = []
    for r in results:
        table_data.append({
            'filename': r['filename'],
            'original_kb': round(r['original_size'] / 8 / 1024, 2),
            'compressed_kb': round(r['compressed_size'] / 8 / 1024, 2),
            'ratio': round(r['compression_ratio'], 2),
            'savings': round((1 - r['compressed_size'] / r['original_size']) * 100, 2)
        })

    # Data for charts
    chart_data = {
        'labels': [r['filename'] for r in results],
        'original_sizes': [r['original_size'] / 8 / 1024 for r in results],  # KB
        'compressed_sizes': [r['compressed_size'] / 8 / 1024 for r in results],  # KB
        'ratios': [r['compression_ratio'] for r in results]
    }

    data = {
        'success': True,
        'total_files': len(results),
        'table_data': table_data,
        'stats': {
            'mean_ratio': round(stats['mean_ratio'], 2),
            'median_ratio': round(stats['median_ratio'], 2),
            'max_ratio': round(stats['max_ratio'], 2),
            'min_ratio': round(stats['min_ratio'], 2),
            'total_original_kb': round(stats['total_original_bits'] / 8 / 1024, 2),
            'total_compressed_kb': round(stats['total_compressed_bits'] / 8 / 1024, 2),
            'total_ratio': round(stats['total_compression_ratio'], 2),
            'savings_percent': round(stats['savings_percentage'], 2)
        },
        'chart_data': chart_data,
        'timestamp': timestamp
    }

    return render_template('dataset_result.html', data=data)


@app.route('/export_csv/<timestamp>')
def export_csv(timestamp):
    """
    Export hasil kompresi dataset ke CSV

    Args:
        timestamp: Timestamp untuk filter file

    Returns:
        CSV file
    """
    # Read all compressed files with matching timestamp
    compressed_files = os.listdir(app.config['COMPRESSED_FOLDER'])
    matching_files = [f for f in compressed_files if timestamp in f and f.endswith('_codes.json')]

    results = []

    for codes_file in matching_files:
        base_name = codes_file.replace('_codes.json', '')

        # Read codes to get compression info
        codes_path = os.path.join(app.config['COMPRESSED_FOLDER'], codes_file)
        bin_path = os.path.join(app.config['COMPRESSED_FOLDER'], f'{base_name}_compressed.bin')
        size_path = os.path.join(app.config['COMPRESSED_FOLDER'], f'{base_name}_size.txt')

        if os.path.exists(bin_path) and os.path.exists(size_path):
            with open(codes_path, 'r') as f:
                codes = json.load(f)

            with open(size_path, 'r') as f:
                height, width = map(int, f.read().strip().split(','))

            original_size = height * width * 8
            compressed_size = os.path.getsize(bin_path) * 8

            results.append({
                'filename': base_name.replace(f'{timestamp}_', ''),
                'original_kb': round(original_size / 8 / 1024, 2),
                'compressed_kb': round(compressed_size / 8 / 1024, 2),
                'ratio': round(original_size / compressed_size, 2),
                'savings': round((1 - compressed_size / original_size) * 100, 2)
            })

    # Create CSV
    csv_path = os.path.join(app.config['COMPRESSED_FOLDER'], f'results_{timestamp}.csv')

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    return send_file(csv_path, mimetype='text/csv', as_attachment=True,
                    download_name=f'compression_results_{timestamp}.csv')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'OK', 'service': 'Huffman Image Compression'})


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Huffman Image Compression Web App")
    print("=" * 60)
    print("📌 Server: http://localhost:5000")
    print("📌 Tekan CTRL+C untuk stop server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)