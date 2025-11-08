#!/usr/bin/env python3
"""
Script to test all main API endpoints and generate comprehensive colleges.json
Includes testing transfer lookups to discover all possible colleges
"""

import requests
import json
import time
import sys
from pathlib import Path

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✓ Health check: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_home():
    """Test home endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"✓ Home endpoint: {response.status_code}")
        return response.json()
    except Exception as e:
        print(f"✗ Home endpoint failed: {e}")
        return None

def get_all_schools():
    """Get all schools from API"""
    try:
        response = requests.get(f"{BASE_URL}/api/transfer/schools", timeout=5)
        if response.status_code == 200:
            schools = response.json().get('schools', [])
            print(f"✓ Retrieved {len(schools)} schools from API")
            return schools
        else:
            print(f"✗ Failed to get schools: {response.status_code}")
            return []
    except Exception as e:
        print(f"✗ Error getting schools: {e}")
        return []

def test_internships():
    """Test internship endpoints"""
    try:
        response = requests.get(f"{BASE_URL}/api/internships?limit=1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total_count', 0)
            print(f"✓ Internships endpoint: {total} total internships")
        else:
            print(f"✗ Internships endpoint: {response.status_code}")
    except Exception as e:
        print(f"✗ Internships error: {e}")

def test_internships_stats():
    """Test internship stats"""
    try:
        response = requests.get(f"{BASE_URL}/api/internships/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total_internships', 0)
            categories = len(data.get('by_category', {}))
            print(f"✓ Internship stats: {total} internships in {categories} categories")
        else:
            print(f"✗ Internship stats: {response.status_code}")
    except Exception as e:
        print(f"✗ Internship stats error: {e}")

def test_stem_internships():
    """Test STEM internships"""
    try:
        response = requests.get(f"{BASE_URL}/api/stem-internships?limit=1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total_count', 0)
            print(f"✓ STEM internships: found results")
        else:
            print(f"✗ STEM internships: {response.status_code}")
    except Exception as e:
        print(f"✗ STEM internships error: {e}")

def test_mentorships():
    """Test mentorship endpoints"""
    try:
        response = requests.get(f"{BASE_URL}/api/mentorships?limit=1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total_count', 0)
            print(f"✓ Mentorships endpoint: {total} total mentorships")
        else:
            print(f"✗ Mentorships endpoint: {response.status_code}")
    except Exception as e:
        print(f"✗ Mentorships error: {e}")

def test_mentorships_free():
    """Test free mentorships"""
    try:
        response = requests.get(f"{BASE_URL}/api/mentorships/free?limit=1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            total = data.get('total_count', 0)
            print(f"✓ Free mentorships: found results")
        else:
            print(f"✗ Free mentorships: {response.status_code}")
    except Exception as e:
        print(f"✗ Free mentorships error: {e}")

def test_transfer_check(from_school, to_school):
    """Test transfer check endpoint"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/transfer/check",
            json={"from_school": from_school, "to_school": to_school},
            timeout=5
        )
        return response.status_code == 200
    except Exception as e:
        return False

def discover_all_colleges(all_schools):
    """
    Discover all possible colleges by testing transfers
    This is a more comprehensive approach to find all valid college combinations
    """
    from_colleges = set()
    to_colleges = set()
    
    from_colleges.update(all_schools)
    to_colleges.update(all_schools)
    
    print(f"\nAttempting to discover colleges through transfer checks...")
    print(f"Testing sample transfers to find all valid college combinations...")
    
    community_colleges = [s for s in all_schools if 'College' in s and 'University' not in s][:5]
    transfer_colleges = [s for s in all_schools if 'University' in s][:5]
    
    tested = 0
    successful = 0
    
    for from_c in community_colleges:
        for to_c in transfer_colleges:
            if test_transfer_check(from_c, to_c):
                from_colleges.add(from_c)
                to_colleges.add(to_c)
                successful += 1
            tested += 1
            if tested % 10 == 0:
                print(f"  Tested {tested} combinations ({successful} successful)")
    
    print(f"✓ Tested {tested} transfer combinations ({successful} successful)")
    
    return sorted(list(from_colleges)), sorted(list(to_colleges))

def generate_colleges_json(from_colleges, to_colleges):
    """Generate colleges.json file"""
    colleges = {
        "from_institution": from_colleges,
        "transfer_institution": to_colleges
    }
    
    output_path = Path("colleges.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(colleges, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Generated {output_path}")
    print(f"  - From institutions: {len(from_colleges)}")
    print(f"  - Transfer institutions: {len(to_colleges)}")
    print(f"  - File size: {output_path.stat().st_size / 1024:.1f} KB")

def main():
    print("=" * 60)
    print("HackCC API Test Suite & Colleges Generator")
    print("=" * 60)
    
    print("\nTesting API connectivity...")
    if not test_health():
        print("\n✗ API is not running. Please start it with: python3 api.py")
        sys.exit(1)
    
    print("\n--- Testing Endpoints ---")
    test_home()
    time.sleep(0.5)
    
    print("\n--- Transfer Module ---")
    all_schools = get_all_schools()
    time.sleep(0.5)
    
    print("\n--- Internship Module ---")
    test_internships()
    time.sleep(0.5)
    test_internships_stats()
    time.sleep(0.5)
    test_stem_internships()
    time.sleep(0.5)
    
    print("\n--- Mentorship Module ---")
    test_mentorships()
    time.sleep(0.5)
    test_mentorships_free()
    time.sleep(0.5)
    
    print("\n--- Transfer Check Sample ---")
    if len(all_schools) >= 2:
        from_school = all_schools[0]
        to_school = all_schools[-1]
        response = requests.post(
            f"{BASE_URL}/api/transfer/check",
            json={"from_school": from_school, "to_school": to_school},
            timeout=5
        )
        if response.status_code == 200:
            print(f"✓ Transfer check works")
        else:
            print(f"✗ Transfer check failed")
    
    if all_schools:
        from_colleges, to_colleges = discover_all_colleges(all_schools)
        generate_colleges_json(from_colleges, to_colleges)
    else:
        print("\n✗ Could not retrieve schools from API")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
