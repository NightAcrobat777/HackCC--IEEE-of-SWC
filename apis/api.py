#!/usr/bin/env python3
"""
Unified Flask REST API for HackCC - combines transfer, internship, and mentorship data
Provides endpoints to query college transfers, internships, and mentorship opportunities
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from combined_api.scraper import get_degree_information
from combined_api.fetch_and_clone_internships import InternshipFetcher
from mentorship_scraper import MentorshipScraper
from datetime import datetime
import json
import os
import sys

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COLLEGES_FILE = os.path.join(BASE_DIR, 'combined_api', 'colleges.json')
INTERNSHIPS_FILE = os.path.join(BASE_DIR, '2026_internships.json')
STEM_INTERNSHIPS_FILE = os.path.join(BASE_DIR, 'stem_internships.json')
MENTORSHIP_FILE = os.path.join(BASE_DIR, 'mentorship_opportunities.json')

with open(COLLEGES_FILE, 'r') as f:
    colleges_data = json.load(f)

COLLEGES = colleges_data.get('from_institution', []) + colleges_data.get('transfer_institution', [])
COLLEGES = list(set(COLLEGES))
COLLEGES.sort()


def load_internships():
    if os.path.exists(INTERNSHIPS_FILE):
        try:
            with open(INTERNSHIPS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {INTERNSHIPS_FILE}: {e}")
            return None
    return None


def load_stem_internships():
    if os.path.exists(STEM_INTERNSHIPS_FILE):
        try:
            with open(STEM_INTERNSHIPS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {STEM_INTERNSHIPS_FILE}: {e}")
            return None
    return None


def load_mentorships():
    if os.path.exists(MENTORSHIP_FILE):
        try:
            with open(MENTORSHIP_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {MENTORSHIP_FILE}: {e}")
            return None
    return None


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'HackCC Unified API',
        'version': '2.0',
        'description': 'Unified API for college transfer programs, internship listings, and mentorship opportunities',
        'sections': {
            'transfer': {
                'base': '/api/transfer',
                'endpoints': {
                    'POST /api/transfer/check': 'Check transfer compatibility between schools',
                    'GET /api/transfer/schools': 'Search/list available colleges'
                }
            },
            'internships': {
                'base': '/api/internships',
                'endpoints': {
                    'GET /api/internships': 'Get all internships with optional filters',
                    'GET /api/internships/<id>': 'Get specific internship by index',
                    'GET /api/internships/stats': 'Get internship statistics',
                    'GET /api/internships/companies': 'Get all companies',
                    'GET /api/internships/locations': 'Get all locations',
                    'GET /api/internships/categories': 'Get all categories',
                    'GET /api/stem-internships': 'Get STEM-specific internships',
                    'POST /api/internships/refresh': 'Refresh internship data'
                }
            },
            'mentorships': {
                'base': '/api/mentorships',
                'endpoints': {
                    'GET /api/mentorships': 'Get all mentorship programs with optional filters',
                    'GET /api/mentorships/<id>': 'Get specific mentorship program by index',
                    'GET /api/mentorships/stats': 'Get mentorship statistics',
                    'GET /api/mentorships/organizations': 'Get list of all organizations',
                    'GET /api/mentorships/majors': 'Get list of all majors',
                    'GET /api/mentorships/free': 'Get only free mentorship programs',
                    'GET /api/mentorships/community-college': 'Get community college friendly programs',
                    'POST /api/mentorships/refresh': 'Refresh mentorship data'
                }
            }
        },
        'query_parameters': {
            '/api/transfer/check': {
                'from_school': 'Starting school name (required)',
                'to_school': 'Destination school name (required)'
            },
            '/api/transfer/schools': {
                'q': 'Search query for college names'
            },
            '/api/internships': {
                'category': 'Filter by category (FAANG+, Quant, Other)',
                'company': 'Filter by company name',
                'location': 'Filter by location',
                'limit': 'Limit results',
                'offset': 'Pagination offset'
            },
            '/api/stem-internships': {
                'major': 'Filter by major',
                'company': 'Filter by company name',
                'limit': 'Limit results',
                'offset': 'Pagination offset'
            },
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
    }), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/api/transfer/check', methods=['POST'])
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


@app.route('/api/transfer/schools', methods=['GET'])
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


@app.route('/api/internships', methods=['GET'])
def get_internships():
    data = load_internships()

    if not data:
        return jsonify({'error': 'No internship data available'}), 404

    internships = data.get('internships', [])

    category = request.args.get('category', '').strip()
    company = request.args.get('company', '').strip().lower()
    location = request.args.get('location', '').strip().lower()
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int, default=0)

    if category:
        internships = [i for i in internships if i.get('category', '').lower() == category.lower()]

    if company:
        internships = [i for i in internships if company in i.get('company', '').lower()]

    if location:
        internships = [i for i in internships if location in i.get('location', '').lower()]

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
    data = load_internships()

    if not data:
        return jsonify({'error': 'No internship data available'}), 404

    internships = data.get('internships', [])

    if 0 <= index < len(internships):
        return jsonify(internships[index])
    else:
        return jsonify({'error': 'Internship not found'}), 404


@app.route('/api/internships/stats', methods=['GET'])
def get_internship_stats():
    data = load_internships()

    if not data:
        return jsonify({'error': 'No internship data available'}), 404

    internships = data.get('internships', [])

    categories = {}
    companies = {}
    locations = {}

    for internship in internships:
        cat = internship.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1

        comp = internship.get('company', 'Unknown')
        companies[comp] = companies.get(comp, 0) + 1

        loc = internship.get('location', 'Unknown')
        locations[loc] = locations.get(loc, 0) + 1

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
    data = load_stem_internships()

    if not data:
        return jsonify({'error': 'No STEM internship data available'}), 404

    major = request.args.get('major', '').strip().lower()
    company = request.args.get('company', '').strip().lower()
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int, default=0)

    internships = data.get('internships', [])

    if major:
        internships = [i for i in internships if major in i.get('major', '').lower()]

    if company:
        internships = [i for i in internships if company in i.get('company', '').lower()]

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


@app.route('/api/internships/refresh', methods=['POST'])
def refresh_internship_data():
    try:
        fetcher = InternshipFetcher()

        if not fetcher.clone_or_update_repo():
            return jsonify({'error': 'Failed to update repository'}), 500

        if not fetcher.fetch_internships():
            return jsonify({'error': 'Failed to fetch internships'}), 500

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


@app.route('/api/mentorships', methods=['GET'])
def get_mentorships():
    data = load_mentorships()

    if not data:
        return jsonify({'error': 'No mentorship data available'}), 404

    mentorships = data.get('mentorships', [])

    major = request.args.get('major', '').strip().lower()
    organization = request.args.get('organization', '').strip().lower()
    target_audience = request.args.get('target_audience', '').strip().lower()
    cost = request.args.get('cost', '').strip().lower()
    format_type = request.args.get('format', '').strip().lower()
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int, default=0)

    if major:
        mentorships = [m for m in mentorships if
                      major in str(m.get('majors', [])).lower() or
                      'all majors' in str(m.get('majors', [])).lower() or
                      'general' in str(m.get('majors', [])).lower()]

    if organization:
        mentorships = [m for m in mentorships if organization in m.get('organization', '').lower()]

    if target_audience:
        mentorships = [m for m in mentorships if target_audience in m.get('target_audience', '').lower()]

    if cost:
        mentorships = [m for m in mentorships if cost in m.get('cost', '').lower()]

    if format_type:
        mentorships = [m for m in mentorships if format_type in m.get('format', '').lower()]

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
    data = load_mentorships()

    if not data:
        return jsonify({'error': 'No mentorship data available'}), 404

    mentorships = data.get('mentorships', [])

    if 0 <= index < len(mentorships):
        return jsonify(mentorships[index])
    else:
        return jsonify({'error': 'Mentorship program not found'}), 404


@app.route('/api/mentorships/stats', methods=['GET'])
def get_mentorship_stats():
    data = load_mentorships()

    if not data:
        return jsonify({'error': 'No mentorship data available'}), 404

    mentorships = data.get('mentorships', [])

    organizations = {}
    target_audiences = {}
    formats = {}
    costs = {}

    for mentorship in mentorships:
        org = mentorship.get('organization', 'Unknown')
        organizations[org] = organizations.get(org, 0) + 1

        audience = mentorship.get('target_audience', 'Unknown')
        target_audiences[audience] = target_audiences.get(audience, 0) + 1

        fmt = mentorship.get('format', 'Unknown')
        formats[fmt] = formats.get(fmt, 0) + 1

        cost = mentorship.get('cost', 'Unknown')
        costs[cost] = costs.get(cost, 0) + 1

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
def get_mentorship_organizations():
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
def get_mentorship_majors():
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
def refresh_mentorship_data():
    try:
        scraper = MentorshipScraper()

        scraper.add_tech_mentorship_programs()
        scraper.add_general_mentorship_programs()
        scraper.add_community_college_specific()

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
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("\n" + "="*80)
    print("HACKCC UNIFIED API SERVER")
    print("="*80)
    print("\nAPI Documentation available at: http://localhost:5000/")
    print("\nMain sections:")
    print("  - TRANSFERS:      /api/transfer/*")
    print("  - INTERNSHIPS:    /api/internships/* and /api/stem-internships")
    print("  - MENTORSHIPS:    /api/mentorships/*")
    print("\n" + "="*80 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
