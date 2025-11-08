#!/usr/bin/env python3

import os
import sys

if __name__ == '__main__' and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from combined_api.api import app
else:
    from .api import app

def main():
    print("\n" + "="*80)
    print("COMBINED HACKCC API - STARTUP")
    print("="*80)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    colleges_file = os.path.join(os.path.dirname(__file__), 'colleges.json')
    internships_file = os.path.join(base_dir, '2026_internships.json')
    stem_file = os.path.join(base_dir, 'stem_internships.json')

    print("\n[*] Checking data files...")
    if os.path.exists(colleges_file):
        print("[+] Found colleges data file")
    else:
        print("[!] Warning: colleges.json not found")

    if os.path.exists(internships_file):
        print("[+] Found internships data file")
    else:
        print("[!] Warning: 2026_internships.json not found")

    if os.path.exists(stem_file):
        print("[+] Found STEM internships data file")
    else:
        print("[!] Warning: stem_internships.json not found")

    print("\n" + "="*80)
    print("COMBINED API SERVER - READY")
    print("="*80)
    print("\nAPI Documentation: http://localhost:5000/")
    print("\n[TRANSFER API ENDPOINTS]")
    print("  - POST http://localhost:5000/api/transfer/check")
    print("  - GET  http://localhost:5000/api/transfer/schools")
    print("\n[INTERNSHIP API ENDPOINTS]")
    print("  - GET  http://localhost:5000/api/internships")
    print("  - GET  http://localhost:5000/api/internships/stats")
    print("  - GET  http://localhost:5000/api/internships/companies")
    print("  - GET  http://localhost:5000/api/internships/locations")
    print("  - GET  http://localhost:5000/api/internships/categories")
    print("  - GET  http://localhost:5000/api/stem-internships")
    print("  - POST http://localhost:5000/api/internships/refresh")
    print("\n[UTILITY]")
    print("  - GET  http://localhost:5000/health")
    print("\n" + "="*80)
    print("\nPress Ctrl+C to stop the server\n")

    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print("Server stopped")
        print("="*80)
        sys.exit(0)

if __name__ == '__main__':
    main()
