#!/usr/bin/env python3

import os
import sys
import json

if __name__ == '__main__' and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from transfer_api.scraper import get_degree_information, scrape_transfer_articulation
else:
    from .scraper import get_degree_information, scrape_transfer_articulation

def main():
    print("\n" + "="*80)
    print("TRANSFER API - USAGE EXAMPLES")
    print("="*80)

    example_transfers = [
        ("Berkeley City College", "University of California, Berkeley"),
        ("Santa Monica College", "University of California, Los Angeles"),
        ("De Anza College", "Stanford University"),
    ]

    for from_school, to_school in example_transfers:
        print(f"\n\n{'─'*80}")
        print(f"Checking transfer: {from_school} → {to_school}")
        print('─'*80)
        
        result = get_degree_information(from_school, to_school)
        
        if result.get('error'):
            print(f"[!] Error: {result['error']}")
        else:
            agreement = result.get('agreement', {})
            print(f"\n[+] Transfer Agreement Found:")
            print(f"    From: {agreement.get('from_school')}")
            print(f"    To: {agreement.get('to_school')}")
            print(f"    Pathway: {agreement.get('institution_name')}")
            print(f"    Code: {agreement.get('institution_code')}")
            print(f"    Community College: {agreement.get('is_community_college')}")
            print(f"    Years Supported: {agreement.get('years_supported')}")
            print(f"    View Details: {result.get('assist_url')}")

    print(f"\n\n{'='*80}")
    print("Examples completed")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
