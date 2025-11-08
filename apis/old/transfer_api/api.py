#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_cors import CORS
from .scraper import get_degree_information
import json
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLLEGES_FILE = os.path.join(os.path.dirname(__file__), 'colleges.json')

with open(COLLEGES_FILE, 'r') as f:
    colleges_data = json.load(f)

COLLEGES = colleges_data.get('from_institution', []) + colleges_data.get('transfer_institution', [])
COLLEGES = list(set(COLLEGES))
COLLEGES.sort()


@app.route('/api/transfer', methods=['POST'])
def check_transfer():
    try:
        data = request.get_json()
        from_school = data.get('from_school', '').strip()
        to_school = data.get('to_school', '').strip()

        if not from_school or not to_school:
            return jsonify({
                'error': 'Missing required fields: from_school and to_school'
            }), 400

        result = get_degree_information(from_school, to_school)
        return jsonify(result), 200 if not result.get('error') else 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/schools', methods=['GET'])
def search_schools():
    try:
        query = request.args.get('q', '').lower().strip()

        if not query:
            return jsonify({'schools': COLLEGES}), 200

        matches = [c for c in COLLEGES if query in c.lower()]
        matches = matches[:10]

        return jsonify({'schools': matches}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
