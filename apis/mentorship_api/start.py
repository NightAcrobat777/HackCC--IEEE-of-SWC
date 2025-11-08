#!/usr/bin/env python3
"""
Start script for the Mentorship API server
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mentorship_api.mentorship_api import app

if __name__ == '__main__':
    print("\n" + "="*80)
    print("MENTORSHIP PROGRAMS API SERVER")
    print("="*80)
    print("\nStarting server on http://localhost:5002")
    print("Press CTRL+C to stop the server")
    print("\n" + "="*80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5002)
