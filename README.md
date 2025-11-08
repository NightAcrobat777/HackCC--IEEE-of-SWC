# HackCC - Unified Student Support Platform

A comprehensive platform for California community college students with AI-powered assistance for college transfers, internship discovery, and mentorship opportunities.

## Features

🎓 **College Transfer Programs** - Find articulation agreements between community colleges and 4-year universities

💼 **Internship Discovery** - Browse and filter internship opportunities by company, location, and category

👥 **Mentorship Programs** - Discover mentorship opportunities by major, organization, and format

🤖 **AI Chat Interface** - Integrated chatbot for natural language queries across all services

## Project Structure

```
├── apis/
│   ├── api.py                          # Unified Flask REST API (transfers, internships, mentorships)
│   ├── example_api_test.py             # Comprehensive API testing script
│   ├── test_api_and_generate_colleges.py  # Test API and generate colleges.json
│   ├── generate_comprehensive_colleges.py # Generate comprehensive colleges.json
│   ├── TESTING_AND_DATA_GENERATION.md # Testing documentation
│   ├── combined_api/                   # Transfer & internship modules
│   │   ├── api.py                      # Transfer & internship endpoints
│   │   ├── scraper.py                  # assist.org scraper
│   │   ├── fetch_and_clone_internships.py
│   │   ├── internship_scraper.py
│   │   ├── colleges.json
│   │   ├── QUICK_REFERENCE.md          # Quick reference guide
│   │   └── API_DOCUMENTATION.md        # Detailed API documentation
│   ├── mentorship_api/                 # Mentorship module
│   │   └── mentorship_api.py
│   ├── mentorship_scraper.py           # Mentorship data scraper
│   ├── API.md                          # Complete API documentation
│   └── scraper.py                      # Transfer scraper utility
├── llm-chat-app-template/              # Chat interface frontend
│   ├── public/                          # Static frontend assets
│   │   ├── index.html                   # Chat UI
│   │   └── chat.js                      # Chat interface script
│   ├── src/                             # TypeScript source code
│   │   ├── index.ts                     # Worker entry point
│   │   └── types.ts                     # TypeScript type definitions
│   ├── test/                            # Test files
│   ├── package.json                     # Node dependencies
│   ├── tsconfig.json                    # TypeScript configuration
│   ├── wrangler.jsonc                   # Cloudflare Workers config
│   └── README.md                        # Chat app documentation
├── README.md                           # This file
├── 2026_internships.json               # Internship data
├── stem_internships.json               # STEM-specific internships
├── mentorship_opportunities.json       # Mentorship data
├── colleges.json                       # College data
├── venv/                               # Python virtual environment
├── requirements.txt                    # Python dependencies
└── .gitignore                          # Git ignore patterns
```

## Quick Start

### Setup

```bash
cd /home/eli/HackCC---IEEE---SWC
source venv/bin/activate
```

### Start the Unified API Server

```bash
cd apis
python3 api.py
```

Server runs on **`http://localhost:5000`**

API documentation available at: **`http://localhost:5000/`**

**Note**: The API expects data files (`2026_internships.json`, `stem_internships.json`, `mentorship_opportunities.json`, `colleges.json`) to be in the `apis/` directory. Copy them from the root directory if needed.

## Testing & Data Generation

### Generate Comprehensive Colleges List

```bash
cd apis
python3 generate_comprehensive_colleges.py
```

This script generates a complete `colleges.json` with all California transfer institutions (community colleges, CSU, UC, and private universities).

### Test All API Endpoints

```bash
# Terminal 1: Start the API
python3 api.py

# Terminal 2: Run comprehensive tests
python3 test_api_and_generate_colleges.py
```

This tests all endpoints and validates data across transfers, internships, and mentorships modules.

See **[apis/TESTING_AND_DATA_GENERATION.md](apis/TESTING_AND_DATA_GENERATION.md)** for detailed documentation on testing and data generation scripts.

## API Endpoints Overview

### Transfer Programs

- `POST /api/transfer/check` - Check transfer agreement between schools
- `GET /api/transfer/schools` - Search/list all colleges
- `GET /health` - Health check

### Internships

- `GET /api/internships` - Get all internships with filters
- `GET /api/internships/<id>` - Get specific internship
- `GET /api/internships/stats` - Internship statistics
- `GET /api/internships/companies` - List all companies
- `GET /api/internships/locations` - List all locations
- `GET /api/internships/categories` - List all categories
- `GET /api/stem-internships` - STEM-specific internships
- `POST /api/internships/refresh` - Refresh internship data

### Mentorships

- `GET /api/mentorships` - Get all mentorship programs with filters
- `GET /api/mentorships/<id>` - Get specific mentorship program
- `GET /api/mentorships/stats` - Mentorship statistics
- `GET /api/mentorships/organizations` - List all organizations
- `GET /api/mentorships/majors` - List all supported majors
- `GET /api/mentorships/free` - Free mentorship programs
- `GET /api/mentorships/community-college` - Community college friendly programs
- `POST /api/mentorships/refresh` - Refresh mentorship data

**See [apis/API.md](apis/API.md) for complete endpoint documentation.**

## Testing the API

### Run Comprehensive Test Suite

```bash
cd apis
python3 example_api_test.py
```

This tests all endpoints across transfers, internships, and mentorships.

### Manual Testing with cURL

```bash
# Health check
curl http://localhost:5000/health

# Get API documentation
curl http://localhost:5000/

# Search schools
curl 'http://localhost:5000/api/transfer/schools?q=berkeley'

# Check transfer agreement (requires POST)
curl -X POST http://localhost:5000/api/transfer/check \
  -H "Content-Type: application/json" \
  -d '{
    "from_school": "Southwestern College",
    "to_school": "University of California, Berkeley"
  }'

# Get free mentorships
curl 'http://localhost:5000/api/mentorships/free?limit=5'

# Get STEM internships
curl 'http://localhost:5000/api/stem-internships?major=computer%20science&limit=5'

# Get internship statistics
curl http://localhost:5000/api/internships/stats
```

## Python Usage Examples

### Using the Transfer Scraper Directly

```python
from apis.combined_api.scraper import get_degree_information

result = get_degree_information(
    "Southwestern College",
    "University of California, Berkeley"
)

if not result.get('error'):
    agreement = result['agreement']
    print(f"Transfer: {agreement['from_school']} → {agreement['to_school']}")
    print(f"Pathway: {agreement['institution_name']}")
    print(f"Years: {agreement['years_supported']}")
    print(f"View details: {result['assist_url']}")
```

### Using the API with Requests

```python
import requests

# Check transfer agreement
response = requests.post('http://localhost:5000/api/transfer/check', json={
    'from_school': 'Southwestern College',
    'to_school': 'University of California, Berkeley'
})
print(response.json())

# Get free mentorships
response = requests.get('http://localhost:5000/api/mentorships/free')
print(response.json())

# Get STEM internships
response = requests.get('http://localhost:5000/api/stem-internships?major=computer science')
print(response.json())
```

## Chat Interface

```bash
cd llm-chat-app-template
npm install
npm run dev
```

See `llm-chat-app-template/README.md` for full setup and deployment instructions.

## Development

### Linting

```bash
cd apis
python3 -m flake8 api.py --max-line-length=100
```

### Running Tests

```bash
cd apis
python3 example_api_test.py
```

## Architecture

- **Unified REST API**: Single entry point for all services (transfers, internships, mentorships)
- **assist.org Integration**: Uses public REST API for transfer agreement data
- **Local JSON Storage**: Internship and mentorship data cached locally for fast queries
- **Flask Framework**: Lightweight, scalable HTTP server
- **CORS Enabled**: Works with any frontend framework

## Performance

- Transfer check: ~1-2 seconds (REST API call to assist.org)
- School search: <100ms (local JSON lookup)
- Internship queries: <100ms (local JSON lookup)
- Mentorship queries: <100ms (local JSON lookup)

## What Works ✅

- ✅ Transfer agreement lookup between CA community colleges and 4-year universities
- ✅ Internship discovery with multiple filters
- ✅ Mentorship program search and filtering
- ✅ Statistics and analytics for all categories
- ✅ Community college-specific features
- ✅ Free program identification
- ✅ STEM-specific opportunities
- ✅ Pagination and pagination offsets

## Deployment

### Production Setup

```bash
# Install production WSGI server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app

# Or use with reverse proxy (Nginx)
# Configure upstream server to http://localhost:5000
```

## Contributing

1. Follow PEP 8 style guidelines
2. Run linting before commits
3. Add tests for new endpoints
4. Update API.md for endpoint changes

## License

IEEE HackCC 2025
