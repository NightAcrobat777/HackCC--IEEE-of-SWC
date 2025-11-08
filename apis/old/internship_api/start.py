#!/usr/bin/env python3
"""
Startup script for Internship API
Fetches/updates internship data and starts the Flask API server
"""

import os
import sys

# Handle both package and standalone execution
if __name__ == '__main__' and __package__ is None:
    # Add parent directory to path for standalone execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from internship_api.fetch_and_clone_internships import InternshipFetcher
    from internship_api.internship_api import app
else:
    # Package execution
    from .fetch_and_clone_internships import InternshipFetcher
    from .internship_api import app

def main():
    print("\n" + "="*80)
    print("INTERNSHIP API - STARTUP")
    print("="*80)

    # Step 1: Fetch/Update internship data
    print("\n[1/2] Fetching internship data...")
    print("-" * 80)

    fetcher = InternshipFetcher()

    # Clone or update repository
    print("\n[*] Cloning/updating repository...")
    if not fetcher.clone_or_update_repo():
        print("[!] Failed to clone/update repository")
        print("[!] Continuing with existing data (if available)...")

    # Fetch internships
    print("\n[*] Fetching internships from README...")
    if fetcher.fetch_internships():
        print(f"[+] Successfully fetched {len(fetcher.internships)} internships")

        # Save to JSON
        if fetcher.save_to_json():
            print("[+] Data saved successfully")
            fetcher.display_summary()
        else:
            print("[!] Failed to save data")
    else:
        print("[!] Failed to fetch internships")
        print("[!] Will use existing data if available...")

    # Step 2: Start the API server
    print("\n" + "="*80)
    print("[2/2] Starting API server...")
    print("-" * 80)

    # Check if data files exist
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    internships_file = os.path.join(base_dir, '2026_internships.json')
    stem_file = os.path.join(base_dir, 'stem_internships.json')

    if not os.path.exists(internships_file):
        print(f"\n[!] Warning: {internships_file} not found")
        print("[!] Some API endpoints may not work properly")
    else:
        print(f"[+] Found internships data file")

    if not os.path.exists(stem_file):
        print(f"[!] Warning: {stem_file} not found")
    else:
        print(f"[+] Found STEM internships data file")

    print("\n" + "="*80)
    print("INTERNSHIP API SERVER - READY")
    print("="*80)
    print("\nAPI Documentation: http://localhost:5001/")
    print("\nAvailable endpoints:")
    print("  - GET  http://localhost:5001/api/internships")
    print("  - GET  http://localhost:5001/api/internships?category=FAANG+")
    print("  - GET  http://localhost:5001/api/internships?company=google")
    print("  - GET  http://localhost:5001/api/internships/stats")
    print("  - GET  http://localhost:5001/api/internships/companies")
    print("  - GET  http://localhost:5001/api/internships/locations")
    print("  - GET  http://localhost:5001/api/stem-internships")
    print("  - POST http://localhost:5001/api/refresh")
    print("\n" + "="*80)
    print("\nPress Ctrl+C to stop the server\n")

    # Run the Flask app
    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print("Server stopped")
        print("="*80)
        sys.exit(0)

if __name__ == '__main__':
    main()
