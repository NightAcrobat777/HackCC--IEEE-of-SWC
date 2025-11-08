#!/usr/bin/env python3
"""
Flask REST API for serving internship data
Provides endpoints to query and filter internships from the fetch_and_clone_internships script
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from .fetch_and_clone_internships import InternshipFetcher

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration - use paths relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERNSHIPS_FILE = os.path.join(BASE_DIR, '2026_internships.json')
STEM_INTERNSHIPS_FILE = os.path.join(BASE_DIR, 'stem_internships.json')


def load_internships():
    """Load internships from JSON file"""
    if os.path.exists(INTERNSHIPS_FILE):
        try:
            with open(INTERNSHIPS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"Error loading {INTERNSHIPS_FILE}: {e}")
            return None
    return None


def load_stem_internships():
    """Load STEM internships from JSON file"""
    if os.path.exists(STEM_INTERNSHIPS_FILE):
        try:
            with open(STEM_INTERNSHIPS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {STEM_INTERNSHIPS_FILE}: {e}")
            return None
    return None


@app.route('/')
def home():
    """API documentation endpoint"""
    return jsonify({
        'message': 'Internship API',
        'version': '1.0',
        'endpoints': {
            'GET /': 'API documentation',
            'GET /api/internships': 'Get all internships with optional filters',
            'GET /api/internships/<int:id>': 'Get specific internship by index',
            'GET /api/internships/stats': 'Get statistics about internships',
            'GET /api/internships/companies': 'Get list of all companies',
            'GET /api/internships/locations': 'Get list of all locations',
            'GET /api/internships/categories': 'Get list of all categories',
            'GET /api/stem-internships': 'Get STEM-specific internships',
            'POST /api/refresh': 'Refresh internship data from source repository'
        },
        'query_parameters': {
            '/api/internships': {
                'category': 'Filter by category (FAANG+, Quant, Other)',
                'company': 'Filter by company name (case-insensitive partial match)',
                'location': 'Filter by location (case-insensitive partial match)',
                'limit': 'Limit number of results',
                'offset': 'Skip first N results'
            }
        }
    })


@app.route('/api/internships', methods=['GET'])
def get_internships():
    """Get all internships with optional filtering"""
    data = load_internships()

    if not data:
        return jsonify({'error': 'No internship data available'}), 404

    internships = data.get('internships', [])

    # Apply filters
    category = request.args.get('category', '').strip()
    company = request.args.get('company', '').strip().lower()
    location = request.args.get('location', '').strip().lower()
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int, default=0)

    # Filter by category
    if category:
        internships = [i for i in internships if i.get('category', '').lower() == category.lower()]

    # Filter by company (partial match)
    if company:
        internships = [i for i in internships if company in i.get('company', '').lower()]

    # Filter by location (partial match)
    if location:
        internships = [i for i in internships if location in i.get('location', '').lower()]

    # Apply pagination
    total_count = len(internships)
    internships = internships[offset:]
    if limit:
        internships = internships[:limit]

    return jsonify({
        'total_count': total_count,
        'returned_count': len(internships),
        'offset': offset,
        'internships': internships,
        'metadata': data.get('metadata', {})
    })


@app.route('/api/internships/<int:index>', methods=['GET'])
def get_internship_by_index(index):
    """Get a specific internship by index"""
    data = load_internships()

    if not data:
        return jsonify({'error': 'No internship data available'}), 404

    internships = data.get('internships', [])

    if 0 <= index < len(internships):
        return jsonify(internships[index])
    else:
        return jsonify({'error': 'Internship not found'}), 404


@app.route('/api/internships/stats', methods=['GET'])
def get_stats():
    """Get statistics about internships"""
    data = load_internships()

    if not data:
        return jsonify({'error': 'No internship data available'}), 404

    internships = data.get('internships', [])

    # Calculate statistics
    categories = {}
    companies = {}
    locations = {}

    for internship in internships:
        # Count by category
        cat = internship.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1

        # Count by company
        comp = internship.get('company', 'Unknown')
        companies[comp] = companies.get(comp, 0) + 1

        # Count by location
        loc = internship.get('location', 'Unknown')
        locations[loc] = locations.get(loc, 0) + 1

    # Sort by count
    top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:10]
    top_locations = sorted(locations.items(), key=lambda x: x[1], reverse=True)[:10]

    return jsonify({
        'total_internships': len(internships),
        'by_category': categories,
        'top_companies': dict(top_companies),
        'top_locations': dict(top_locations),
        'metadata': data.get('metadata', {})
    })


@app.route('/api/internships/companies', methods=['GET'])
def get_companies():
    """Get list of all unique companies"""
    data = load_internships()

    if not data:
        return jsonify({'error': 'No internship data available'}), 404

    internships = data.get('internships', [])
    companies = sorted(list(set(i.get('company', '') for i in internships if i.get('company'))))

    return jsonify({
        'count': len(companies),
        'companies': companies
    })


@app.route('/api/internships/locations', methods=['GET'])
def get_locations():
    """Get list of all unique locations"""
    data = load_internships()

    if not data:
        return jsonify({'error': 'No internship data available'}), 404

    internships = data.get('internships', [])
    locations = sorted(list(set(i.get('location', '') for i in internships if i.get('location'))))

    return jsonify({
        'count': len(locations),
        'locations': locations
    })


@app.route('/api/internships/categories', methods=['GET'])
def get_categories():
    """Get list of all categories"""
    data = load_internships()

    if not data:
        return jsonify({'error': 'No internship data available'}), 404

    internships = data.get('internships', [])
    categories = sorted(list(set(i.get('category', '') for i in internships if i.get('category'))))

    return jsonify({
        'count': len(categories),
        'categories': categories
    })


@app.route('/api/stem-internships', methods=['GET'])
def get_stem_internships():
    """Get STEM-specific internships"""
    data = load_stem_internships()

    if not data:
        return jsonify({'error': 'No STEM internship data available'}), 404

    # Apply filters
    major = request.args.get('major', '').strip().lower()
    company = request.args.get('company', '').strip().lower()
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int, default=0)

    internships = data.get('internships', [])

    # Filter by major (partial match)
    if major:
        internships = [i for i in internships if major in i.get('major', '').lower()]

    # Filter by company (partial match)
    if company:
        internships = [i for i in internships if company in i.get('company', '').lower()]

    # Apply pagination
    total_count = len(internships)
    internships = internships[offset:]
    if limit:
        internships = internships[:limit]

    return jsonify({
        'total_count': total_count,
        'returned_count': len(internships),
        'offset': offset,
        'internships': internships,
        'stem_majors': data.get('stem_majors', []),
        'last_updated': data.get('last_updated', '')
    })


@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Refresh internship data from the source repository"""
    try:
        fetcher = InternshipFetcher()

        # Clone or update repository
        if not fetcher.clone_or_update_repo():
            return jsonify({'error': 'Failed to update repository'}), 500

        # Fetch internships
        if not fetcher.fetch_internships():
            return jsonify({'error': 'Failed to fetch internships'}), 500

        # Save to JSON
        if not fetcher.save_to_json():
            return jsonify({'error': 'Failed to save internships'}), 500

        return jsonify({
            'success': True,
            'message': 'Internship data refreshed successfully',
            'total_internships': len(fetcher.internships),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    except Exception as e:
        return jsonify({'error': f'Failed to refresh data: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Check if data files exist
    if not os.path.exists(INTERNSHIPS_FILE):
        print(f"Warning: {INTERNSHIPS_FILE} not found. Run fetch_and_clone_internships.py first.")

    if not os.path.exists(STEM_INTERNSHIPS_FILE):
        print(f"Warning: {STEM_INTERNSHIPS_FILE} not found.")

    print("\n" + "="*80)
    print("INTERNSHIP API SERVER")
    print("="*80)
    print("\nAPI Documentation available at: http://localhost:5001/")
    print("Example endpoints:")
    print("  - GET  http://localhost:5001/api/internships")
    print("  - GET  http://localhost:5001/api/internships?category=FAANG+")
    print("  - GET  http://localhost:5001/api/internships?company=google")
    print("  - GET  http://localhost:5001/api/internships/stats")
    print("  - GET  http://localhost:5001/api/stem-internships")
    print("  - POST http://localhost:5001/api/refresh")
    print("\n" + "="*80 + "\n")

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5001)
