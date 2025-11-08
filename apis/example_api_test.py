#!/usr/bin/env python3
"""
Example script to test all HackCC Unified API endpoints
Tests transfer, internship, and mentorship endpoints
"""

import requests
import json
from pprint import pprint

API_URL = "http://localhost:5000"

def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def test_health():
    print_section("1. HEALTH CHECK")
    response = requests.get(f"{API_URL}/health")
    print(f"GET /health")
    print(f"Status: {response.status_code}")
    pprint(response.json())

def test_api_documentation():
    print_section("2. API DOCUMENTATION")
    response = requests.get(f"{API_URL}/")
    print(f"GET /")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Message: {data['message']}")
    print(f"Version: {data['version']}")
    print(f"Sections: {list(data['sections'].keys())}")

def test_transfer_schools():
    print_section("3. TRANSFER - SEARCH SCHOOLS")
    
    print("3a. Get all schools")
    response = requests.get(f"{API_URL}/api/transfer/schools")
    print(f"GET /api/transfer/schools")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total schools: {len(data['schools'])}")
    print(f"First 5: {data['schools'][:5]}")
    
    print("\n3b. Search for 'berkeley'")
    response = requests.get(f"{API_URL}/api/transfer/schools?q=berkeley")
    print(f"GET /api/transfer/schools?q=berkeley")
    print(f"Status: {response.status_code}")
    pprint(response.json())

def test_transfer_check():
    print_section("4. TRANSFER - CHECK AGREEMENT")
    
    payload = {
        "from_school": "Southwestern College",
        "to_school": "University of California, Berkeley"
    }
    
    response = requests.post(f"{API_URL}/api/transfer/check", json=payload)
    print(f"POST /api/transfer/check")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"Status: {response.status_code}")
    pprint(response.json())

def test_internships():
    print_section("5. INTERNSHIPS - GET ALL")
    
    print("5a. Get first 3 internships")
    response = requests.get(f"{API_URL}/api/internships?limit=3&offset=0")
    print(f"GET /api/internships?limit=3&offset=0")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total count: {data['total_count']}")
    print(f"Returned: {data['returned_count']}")
    if data['internships']:
        print(f"First internship:")
        pprint(data['internships'][0])
    
    print("\n5b. Get specific internship by index")
    response = requests.get(f"{API_URL}/api/internships/0")
    print(f"GET /api/internships/0")
    print(f"Status: {response.status_code}")
    pprint(response.json())

def test_internship_stats():
    print_section("6. INTERNSHIPS - STATISTICS")
    
    response = requests.get(f"{API_URL}/api/internships/stats")
    print(f"GET /api/internships/stats")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total internships: {data['total_internships']}")
    print(f"Categories: {data['by_category']}")
    print(f"Top 5 companies: {dict(list(data['top_companies'].items())[:5])}")
    print(f"Top 5 locations: {dict(list(data['top_locations'].items())[:5])}")

def test_internship_filters():
    print_section("7. INTERNSHIPS - FILTERS")
    
    print("7a. Get companies")
    response = requests.get(f"{API_URL}/api/internships/companies")
    print(f"GET /api/internships/companies")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total companies: {data['count']}")
    print(f"Sample: {data['companies'][:5]}")
    
    print("\n7b. Get locations")
    response = requests.get(f"{API_URL}/api/internships/locations")
    print(f"GET /api/internships/locations")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total locations: {data['count']}")
    print(f"Sample: {data['locations'][:5]}")
    
    print("\n7c. Get categories")
    response = requests.get(f"{API_URL}/api/internships/categories")
    print(f"GET /api/internships/categories")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total categories: {data['count']}")
    print(f"Categories: {data['categories']}")

def test_stem_internships():
    print_section("8. STEM INTERNSHIPS")
    
    response = requests.get(f"{API_URL}/api/stem-internships?limit=3")
    print(f"GET /api/stem-internships?limit=3")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total STEM internships: {data['total_count']}")
    print(f"Returned: {data['returned_count']}")
    print(f"STEM majors available: {data['stem_majors'][:5]}")
    if data['internships']:
        print(f"First STEM internship:")
        pprint(data['internships'][0])

def test_mentorships():
    print_section("9. MENTORSHIPS - GET ALL")
    
    print("9a. Get first 3 mentorships")
    response = requests.get(f"{API_URL}/api/mentorships?limit=3&offset=0")
    print(f"GET /api/mentorships?limit=3&offset=0")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total count: {data['total_count']}")
    print(f"Returned: {data['returned_count']}")
    if data['mentorships']:
        print(f"First mentorship:")
        pprint(data['mentorships'][0])
    
    print("\n9b. Get specific mentorship by index")
    response = requests.get(f"{API_URL}/api/mentorships/0")
    print(f"GET /api/mentorships/0")
    print(f"Status: {response.status_code}")
    pprint(response.json())

def test_mentorship_stats():
    print_section("10. MENTORSHIPS - STATISTICS")
    
    response = requests.get(f"{API_URL}/api/mentorships/stats")
    print(f"GET /api/mentorships/stats")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total programs: {data['total_programs']}")
    print(f"By format: {data['by_format']}")
    print(f"By cost: {data['by_cost']}")
    print(f"Top organizations: {dict(list(data['by_organization'].items())[:5])}")

def test_mentorship_filters():
    print_section("11. MENTORSHIPS - FILTERS")
    
    print("11a. Get free mentorships")
    response = requests.get(f"{API_URL}/api/mentorships/free?limit=3")
    print(f"GET /api/mentorships/free?limit=3")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total free programs: {data['total_count']}")
    print(f"Sample:\n")
    if data['mentorships']:
        pprint(data['mentorships'][0])
    
    print("\n11b. Get community college friendly programs")
    response = requests.get(f"{API_URL}/api/mentorships/community-college?limit=3")
    print(f"GET /api/mentorships/community-college?limit=3")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total CC-friendly programs: {data['total_count']}")
    
    print("\n11c. Get organizations")
    response = requests.get(f"{API_URL}/api/mentorships/organizations")
    print(f"GET /api/mentorships/organizations")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total organizations: {data['count']}")
    print(f"Sample: {data['organizations'][:5]}")
    
    print("\n11d. Get majors")
    response = requests.get(f"{API_URL}/api/mentorships/majors")
    print(f"GET /api/mentorships/majors")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total majors: {data['count']}")
    print(f"Sample: {data['majors'][:5]}")

def main():
    print("\n" + "="*80)
    print("  HACKCC UNIFIED API - COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    try:
        test_health()
        test_api_documentation()
        test_transfer_schools()
        test_transfer_check()
        test_internships()
        test_internship_stats()
        test_internship_filters()
        test_stem_internships()
        test_mentorships()
        test_mentorship_stats()
        test_mentorship_filters()
        
        print("\n" + "="*80)
        print("  ✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*80 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API at", API_URL)
        print("Make sure the API server is running:")
        print("  cd /apis && ./venv/bin/python3 api.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
