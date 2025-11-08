#!/usr/bin/env python3

from scraper import scrape_transfer_articulation, get_institution_id
import json

print("=" * 80)
print("ASSIST.ORG TRANSFER AGREEMENT SCRAPER - EXAMPLES")
print("=" * 80)
print()

schools = [
    ("Berkeley City College", "University of California, Berkeley"),
    ("Diablo Valley College", "University of California, Davis"),
    ("Chabot College", "San Jose State University"),
    ("De Anza College", "University of California, Berkeley"),
    ("Foothill College", "University of California, Santa Cruz"),
    ("Ohlone College", "California State University, East Bay"),
    ("American River College", "University of California, Davis"),
]

print("Fetching transfer agreements for all school pairs...")
print()

all_results = []

for from_school, to_school in schools:
    print(f"[{schools.index((from_school, to_school)) + 1}/{len(schools)}] {from_school} → {to_school}")
    
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
            print(f"     Year IDs: {len(agr.get('sending_year_ids', []))} years supported")
            print(f"     Community College: {agr.get('is_community_college')}")
        else:
            print(f"  ⚠️  No agreements found")
    
    all_results.append(result)
    print()

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
successful = sum(1 for r in all_results if r.get('agreements'))
print(f"Total queries: {len(all_results)}")
print(f"Successful agreements: {successful}")
print()

print("=" * 80)
print("SAMPLE OUTPUT (JSON)")
print("=" * 80)
print(json.dumps(all_results[0], indent=2))
print()

print("=" * 80)
print("HOW TO USE IN YOUR CODE")
print("=" * 80)
print("""
from scraper import scrape_transfer_articulation

# Get transfer agreement between two schools
result = scrape_transfer_articulation(
    "Berkeley City College", 
    "University of California, Berkeley"
)

# Check if successful
if result.get('error'):
    print(f"Error: {result['error']}")
else:
    # Get agreement details
    for agreement in result['agreements']:
        print(f"From: {agreement['institution_name']}")
        print(f"Code: {agreement['institution_code']}")
        print(f"Years: {agreement['sending_year_ids']}")
""")
