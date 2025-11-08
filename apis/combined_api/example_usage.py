#!/usr/bin/env python3

import requests
import json

BASE_URL = "http://localhost:5000"

def print_section(title):
    print(f"\n{'='*80}")
    print(f"{title}")
    print('='*80)

def print_result(title, data):
    print(f"\n{title}")
    print(json.dumps(data, indent=2))

def main():
    print("\n" + "="*80)
    print("COMBINED API - USAGE EXAMPLES")
    print("="*80)

    print_section("1. CHECK TRANSFER COMPATIBILITY")
    try:
        response = requests.post(
            f"{BASE_URL}/api/transfer/check",
            json={
                "from_school": "Berkeley City College",
                "to_school": "University of California, Berkeley"
            }
        )
        print_result("Transfer Check Result:", response.json())
    except Exception as e:
        print(f"[!] Error: {e}")

    print_section("2. SEARCH COLLEGES")
    try:
        response = requests.get(f"{BASE_URL}/api/transfer/schools?q=berkeley")
        print_result("College Search Result:", response.json())
    except Exception as e:
        print(f"[!] Error: {e}")

    print_section("3. GET INTERNSHIP STATISTICS")
    try:
        response = requests.get(f"{BASE_URL}/api/internships/stats")
        stats = response.json()
        print(f"Total Internships: {stats.get('total_internships')}")
        print(f"By Category: {stats.get('by_category')}")
        print(f"Top Companies: {dict(list(stats.get('top_companies', {}).items())[:5])}")
        print(f"Top Locations: {dict(list(stats.get('top_locations', {}).items())[:5])}")
    except Exception as e:
        print(f"[!] Error: {e}")

    print_section("4. GET FAANG+ INTERNSHIPS")
    try:
        response = requests.get(f"{BASE_URL}/api/internships?category=FAANG+&limit=3")
        data = response.json()
        print(f"Found: {data.get('returned_count')} internships (of {data.get('total_count')} total)")
        for i, internship in enumerate(data.get('internships', []), 1):
            print(f"\n[{i}] {internship.get('company')} - {internship.get('position')}")
            print(f"    Location: {internship.get('location')}")
            print(f"    Salary: {internship.get('salary')}")
            print(f"    Apply: {internship.get('apply_link')}")
    except Exception as e:
        print(f"[!] Error: {e}")

    print_section("5. GET STEM INTERNSHIPS")
    try:
        response = requests.get(f"{BASE_URL}/api/stem-internships?limit=2")
        data = response.json()
        print(f"Found: {data.get('returned_count')} STEM internships (of {data.get('total_count')} total)")
        for i, internship in enumerate(data.get('internships', []), 1):
            print(f"\n[{i}] {internship.get('company')} - {internship.get('position')}")
            print(f"    Major: {internship.get('major')}")
    except Exception as e:
        print(f"[!] Error: {e}")

    print_section("6. GET ALL COMPANIES")
    try:
        response = requests.get(f"{BASE_URL}/api/internships/companies")
        data = response.json()
        print(f"Total Companies: {data.get('count')}")
        print(f"Sample: {data.get('companies', [])[:5]}")
    except Exception as e:
        print(f"[!] Error: {e}")

    print_section("7. GET ALL LOCATIONS")
    try:
        response = requests.get(f"{BASE_URL}/api/internships/locations")
        data = response.json()
        print(f"Total Locations: {data.get('count')}")
        print(f"Sample: {data.get('locations', [])[:5]}")
    except Exception as e:
        print(f"[!] Error: {e}")

    print_section("8. HEALTH CHECK")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_result("Health Status:", response.json())
    except Exception as e:
        print(f"[!] Error: {e}")

    print("\n" + "="*80)
    print("Examples completed")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
