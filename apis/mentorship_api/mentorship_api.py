#!/usr/bin/env python3
"""
Flask REST API for serving mentorship program data
Provides endpoints to query and filter mentorship opportunities
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import sys
from datetime import datetime

# Add parent directory to path to import mentorship_scraper
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mentorship_scraper import MentorshipScraper

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration - use paths relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENTORSHIP_FILE = os.path.join(BASE_DIR, 'mentorship_opportunities.json')


def load_mentorships():
    """Load mentorships from JSON file"""
    if os.path.exists(MENTORSHIP_FILE):
        try:
            with open(MENTORSHIP_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"Error loading {MENTORSHIP_FILE}: {e}")
            return None
    return None


@app.route('/')
def home():
    """API documentation endpoint"""
    return jsonify({
        'message': 'Mentorship Programs API',
        'version': '1.0',
        'endpoints': {
            'GET /': 'API documentation',
            'GET /api/mentorships': 'Get all mentorship programs with optional filters',
            'GET /api/mentorships/<int:id>': 'Get specific mentorship program by index',
            'GET /api/mentorships/stats': 'Get statistics about mentorship programs',
            'GET /api/mentorships/organizations': 'Get list of all organizations',
            'GET /api/mentorships/majors': 'Get list of all majors',
            'GET /api/mentorships/free': 'Get only free mentorship programs',
            'GET /api/mentorships/community-college': 'Get community college friendly programs',
            'POST /api/mentorships/refresh': 'Refresh mentorship data from scraper'
        },
        'query_parameters': {
            '/api/mentorships': {
                'major': 'Filter by major (case-insensitive partial match)',
                'organization': 'Filter by organization name (case-insensitive partial match)',
                'target_audience': 'Filter by target audience (case-insensitive partial match)',
                'cost': 'Filter by cost (e.g., "free")',
                'format': 'Filter by format (e.g., "virtual", "hybrid", "in-person")',
                'limit': 'Limit number of results',
                'offset': 'Skip first N results'
            }
        }
    })


@app.route('/api/mentorships', methods=['GET'])
def get_mentorships():
    """Get all mentorship programs with optional filtering"""
    data = load_mentorships()

    if not data:
        return jsonify({'error': 'No mentorship data available'}), 404

    mentorships = data.get('mentorships', [])

    # Apply filters
    major = request.args.get('major', '').strip().lower()
    organization = request.args.get('organization', '').strip().lower()
    target_audience = request.args.get('target_audience', '').strip().lower()
    cost = request.args.get('cost', '').strip().lower()
    format_type = request.args.get('format', '').strip().lower()
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int, default=0)

    # Filter by major
    if major:
        mentorships = [m for m in mentorships if
                      major in str(m.get('majors', [])).lower() or
                      'all majors' in str(m.get('majors', [])).lower() or
                      'general' in str(m.get('majors', [])).lower()]

    # Filter by organization (partial match)
    if organization:
        mentorships = [m for m in mentorships if organization in m.get('organization', '').lower()]

    # Filter by target audience (partial match)
    if target_audience:
        mentorships = [m for m in mentorships if target_audience in m.get('target_audience', '').lower()]

    # Filter by cost
    if cost:
        mentorships = [m for m in mentorships if cost in m.get('cost', '').lower()]

    # Filter by format
    if format_type:
        mentorships = [m for m in mentorships if format_type in m.get('format', '').lower()]

    # Apply pagination
    total_count = len(mentorships)
    mentorships = mentorships[offset:]
    if limit:
        mentorships = mentorships[:limit]

    return jsonify({
        'total_count': total_count,
        'returned_count': len(mentorships),
        'offset': offset,
        'mentorships': mentorships,
        'categories': data.get('categories', {}),
        'last_updated': data.get('last_updated', '')
    })


@app.route('/api/mentorships/<int:index>', methods=['GET'])
def get_mentorship_by_index(index):
    """Get a specific mentorship program by index"""
    data = load_mentorships()

    if not data:
        return jsonify({'error': 'No mentorship data available'}), 404

    mentorships = data.get('mentorships', [])

    if 0 <= index < len(mentorships):
        return jsonify(mentorships[index])
    else:
        return jsonify({'error': 'Mentorship program not found'}), 404


@app.route('/api/mentorships/stats', methods=['GET'])
def get_stats():
    """Get statistics about mentorship programs"""
    data = load_mentorships()

    if not data:
        return jsonify({'error': 'No mentorship data available'}), 404

    mentorships = data.get('mentorships', [])

    # Calculate statistics
    organizations = {}
    target_audiences = {}
    formats = {}
    costs = {}

    for mentorship in mentorships:
        # Count by organization
        org = mentorship.get('organization', 'Unknown')
        organizations[org] = organizations.get(org, 0) + 1

        # Count by target audience
        audience = mentorship.get('target_audience', 'Unknown')
        target_audiences[audience] = target_audiences.get(audience, 0) + 1

        # Count by format
        fmt = mentorship.get('format', 'Unknown')
        formats[fmt] = formats.get(fmt, 0) + 1

        # Count by cost
        cost = mentorship.get('cost', 'Unknown')
        costs[cost] = costs.get(cost, 0) + 1

    # Sort by count
    top_organizations = sorted(organizations.items(), key=lambda x: x[1], reverse=True)[:10]

    return jsonify({
        'total_programs': len(mentorships),
        'by_organization': dict(top_organizations),
        'by_format': formats,
        'by_cost': costs,
        'categories': data.get('categories', {}),
        'last_updated': data.get('last_updated', '')
    })


@app.route('/api/mentorships/organizations', methods=['GET'])
def get_organizations():
    """Get list of all unique organizations"""
    data = load_mentorships()

    if not data:
        return jsonify({'error': 'No mentorship data available'}), 404

    mentorships = data.get('mentorships', [])
    organizations = sorted(list(set(m.get('organization', '') for m in mentorships if m.get('organization'))))

    return jsonify({
        'count': len(organizations),
        'organizations': organizations
    })


@app.route('/api/mentorships/majors', methods=['GET'])
def get_majors():
    """Get list of all unique majors"""
    data = load_mentorships()

    if not data:
        return jsonify({'error': 'No mentorship data available'}), 404

    mentorships = data.get('mentorships', [])
    majors_set = set()

    for m in mentorships:
        majors_list = m.get('majors', [])
        if isinstance(majors_list, list):
            majors_set.update(majors_list)

    majors = sorted(list(majors_set))

    return jsonify({
        'count': len(majors),
        'majors': majors
    })


@app.route('/api/mentorships/free', methods=['GET'])
def get_free_mentorships():
    """Get only free mentorship programs"""
    data = load_mentorships()

    if not data:
        return jsonify({'error': 'No mentorship data available'}), 404

    mentorships = data.get('mentorships', [])
    free_mentorships = [m for m in mentorships if m.get('cost', '').lower() == 'free']

    return jsonify({
        'total_count': len(free_mentorships),
        'mentorships': free_mentorships
    })


@app.route('/api/mentorships/community-college', methods=['GET'])
def get_community_college_mentorships():
    """Get community college friendly programs"""
    data = load_mentorships()

    if not data:
        return jsonify({'error': 'No mentorship data available'}), 404

    mentorships = data.get('mentorships', [])
    cc_mentorships = [m for m in mentorships if 'community college' in m.get('target_audience', '').lower()]

    return jsonify({
        'total_count': len(cc_mentorships),
        'mentorships': cc_mentorships
    })


@app.route('/api/mentorships/refresh', methods=['POST'])
def refresh_data():
    """Refresh mentorship data from the scraper"""
    try:
        scraper = MentorshipScraper()

        # Collect all mentorship programs
        scraper.add_tech_mentorship_programs()
        scraper.add_general_mentorship_programs()
        scraper.add_community_college_specific()

        # Save to JSON
        scraper.save_to_json(MENTORSHIP_FILE)

        return jsonify({
            'success': True,
            'message': 'Mentorship data refreshed successfully',
            'total_programs': len(scraper.mentorships),
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
    # Check if data file exists
    if not os.path.exists(MENTORSHIP_FILE):
        print(f"Warning: {MENTORSHIP_FILE} not found.")
        print("Run the refresh endpoint or mentorship_scraper.py to generate data.")

    print("\n" + "="*80)
    print("MENTORSHIP PROGRAMS API SERVER")
    print("="*80)
    print("\nAPI Documentation available at: http://localhost:5002/")
    print("Example endpoints:")
    print("  - GET  http://localhost:5002/api/mentorships")
    print("  - GET  http://localhost:5002/api/mentorships?major=computer%20science")
    print("  - GET  http://localhost:5002/api/mentorships?cost=free")
    print("  - GET  http://localhost:5002/api/mentorships/stats")
    print("  - GET  http://localhost:5002/api/mentorships/free")
    print("  - GET  http://localhost:5002/api/mentorships/community-college")
    print("  - POST http://localhost:5002/api/mentorships/refresh")
    print("\n" + "="*80 + "\n")

    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5002)
