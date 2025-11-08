#!/usr/bin/env python3

import os
import sys

if __name__ == '__main__' and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from transfer_api.api import app
else:
    from .api import app

def main():
    print("\n" + "="*80)
    print("TRANSFER API - STARTUP")
    print("="*80)

    colleges_file = os.path.join(os.path.dirname(__file__), 'colleges.json')
    
    if not os.path.exists(colleges_file):
        print(f"\n[!] Warning: {colleges_file} not found")
        print("[!] API may not work properly")
    else:
        print(f"[+] Found colleges data file")

    print("\n" + "="*80)
    print("TRANSFER API SERVER - READY")
    print("="*80)
    print("\nAPI Documentation: http://localhost:5000/")
    print("\nAvailable endpoints:")
    print("  - POST http://localhost:5000/api/transfer (check transfer compatibility)")
    print("  - GET  http://localhost:5000/api/schools (list/search colleges)")
    print("  - GET  http://localhost:5000/health (health check)")
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
