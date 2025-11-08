#!/usr/bin/env python3

from scraper import scrape_transfer_articulation, get_degree_information
import json

print("=" * 100)
print("ASSIST.ORG TRANSFER AGREEMENT SCRAPER - EXAMPLES")
print("=" * 100)
print()

schools = [
    ("Berkeley City College", "University of California, Berkeley"),
    ("Diablo Valley College", "University of California, Davis"),
    ("Chabot College", "San Jose State University"),
]

print("=" * 100)
print("EXAMPLE 1: TRANSFER AGREEMENTS ONLY (FAST - REST API)")
print("=" * 100)
print()

agreement_results = []

for from_school, to_school in schools:
    idx = schools.index((from_school, to_school)) + 1
    print(f"[{idx}/{len(schools)}] {from_school} → {to_school}")
    
    result = scrape_transfer_articulation(from_school, to_school, debug=False)
    
    if result.get('error'):
        print(f"  ❌ Error: {result['error']}")
    else:
        agreements = result.get('agreements', [])
        if agreements:
            agr = agreements[0]
            print(f"  ✅ Agreement found")
            print(f"     School: {agr.get('institution_name')}")
            print(f"     Code: {agr.get('institution_code')}")
            print(f"     Years supported: {len(agr.get('sending_year_ids', []))}")
            print(f"     Community College: {agr.get('is_community_college')}")
        else:
            print(f"  ⚠️  No agreements found")
    
    agreement_results.append(result)
    print()

print()
print("=" * 100)
print("EXAMPLE 2: COMPLETE DEGREE INFORMATION (REST API)")
print("=" * 100)
print()

from_school = "Berkeley City College"
to_school = "University of California, Berkeley"

print(f"Getting degree info: {from_school} → {to_school}")
print()

degree_info = get_degree_information(from_school, to_school, debug=False)

if degree_info.get('error'):
    print(f"❌ Error: {degree_info['error']}")
else:
    print(f"✅ Transfer Agreement Found")
    print()
    
    agreement = degree_info.get('agreement', {})
    print(f"From: {agreement.get('from_school')}")
    print(f"To: {agreement.get('to_school')}")
    print(f"Pathway: {agreement.get('institution_name')} ({agreement.get('institution_code')})")
    print(f"Years Supported: {agreement.get('years_supported')}")
    print(f"Community College: {agreement.get('is_community_college')}")
    print()
    
    assist_url = degree_info.get('assist_url')
    print(f"View courses on assist.org: {assist_url}")

print()
print()
print("=" * 100)
print("EXAMPLE 3: MULTIPLE SCHOOLS")
print("=" * 100)
print()

test_pairs = [
    ("De Anza College", "University of California, Berkeley"),
    ("Foothill College", "University of California, Davis"),
]

for from_school, to_school in test_pairs:
    print(f"{from_school} → {to_school}")
    
    degree_info = get_degree_information(from_school, to_school, debug=False)
    
    if degree_info.get('error'):
        print(f"  ❌ Error: {degree_info['error']}")
    else:
        agreement = degree_info.get('agreement', {})
        print(f"  ✅ {agreement.get('institution_name')} ({agreement.get('institution_code')})")
        print(f"  Years: {agreement.get('years_supported')}")
        print(f"  View: {degree_info.get('assist_url')}")
    
    print()

print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)
successful = sum(1 for r in agreement_results if r.get('agreements'))
print(f"Transfer agreements found: {successful}/{len(agreement_results)}")
print()

print("=" * 100)
print("RECOMMENDED USAGE")
print("=" * 100)
print("""
from scraper import get_degree_information

# Fast, simple, and reliable (~1-2 seconds)
degree_info = get_degree_information(
    "Berkeley City College",
    "University of California, Berkeley"
)

if not degree_info.get('error'):
    agreement = degree_info['agreement']
    print(f"✅ Transfer Agreement Found")
    print(f"From: {agreement['from_school']}")
    print(f"To: {agreement['to_school']}")
    print(f"Pathway: {agreement['institution_name']} ({agreement['institution_code']})")
    print(f"Years Supported: {agreement['years_supported']}")
    print(f"View courses: {degree_info['assist_url']}")
""")
