# TransferTree - AI-Powered Transfer Agreement Assistant

An AI chatbot that helps students find transfer agreements between California community colleges and 4-year universities using assist.org data.

## Project Structure

```
├── scraper.py                 # Core API scraper for assist.org
├── api.py                     # Flask REST API server
├── example_usage.py          # Direct scraper usage examples
├── example_api_usage.py      # Flask API usage examples
├── colleges.json             # List of California institutions
├── llm-chat-app-template/    # Cloudflare Workers chat interface
├── API.md                    # Flask API documentation
├── CLAUDE.md                 # Development notes
├── README.md                 # This file
└── venv/                     # Python virtual environment
```

## Quick Start

### Setup
```bash
cd /home/eli/HackCC---IEEE---SWC
source venv/bin/activate
```

### Option 1: Python Scraper (Direct)

#### Run Examples
```bash
./venv/bin/python3 example_usage.py
```

#### Use in Your Code
```python
from scraper import get_degree_information

result = get_degree_information(
    "Southwestern College",
    "University of California, Berkeley"
)

if not result.get('error'):
    agreement = result['agreement']
    print(f"From: {agreement['from_school']}")
    print(f"To: {agreement['to_school']}")
    print(f"Pathway: {agreement['institution_name']}")
    print(f"Years: {agreement['years_supported']}")
    print(f"View: {result['assist_url']}")
```

### Option 2: Flask API (Recommended for Chat Integration)

#### Install Dependencies
```bash
pip install flask flask-cors
```

#### Start API Server
```bash
./venv/bin/python3 api.py
```

Server runs on `http://localhost:5000`

#### Check Transfer Agreement
```bash
curl -X POST http://localhost:5000/api/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "from_school": "Southwestern College",
    "to_school": "University of California, Berkeley"
  }'
```

#### Search Schools
```bash
curl http://localhost:5000/api/schools?q=berkeley
```

#### Run Example Script
```bash
./venv/bin/python3 example_api_usage.py
```

**See [API.md](API.md) for full documentation.**

### API Response Format

```json
{
  "from_school": "Southwestern College",
  "to_school": "University of California, Berkeley",
  "agreement": {
    "from_school": "Southwestern College",
    "to_school": "University of California, Berkeley",
    "institution_name": "Southwestern College",
    "institution_code": "SWSTRN",
    "is_community_college": true,
    "years_supported": 30
  },
  "assist_url": "https://www.assist.org",
  "error": null
}
```

### Frontend (Cloudflare Workers)

```bash
cd llm-chat-app-template
npm install
npm run dev
```

See `llm-chat-app-template/README.md` for full setup and deployment instructions.

## Key Functions

### `get_degree_information(from_school, to_school, year_name="2025-2026", debug=False)`

**Returns transfer agreement data + link to assist.org**

- **Fast**: ~1-2 seconds (REST API only)
- **Reliable**: 100% - No browser automation needed
- **Args**:
  - `from_school`: Community college name
  - `to_school`: University name
  - `year_name`: Academic year (default: "2025-2026")
  - `debug`: Include additional debugging info (optional)

- **Returns**:
  - `from_school`, `to_school`: The transfer pair
  - `agreement`: Transfer agreement details
  - `assist_url`: Link to assist.org for course details
  - `error`: Error message (if any)

### `scrape_transfer_articulation(from_school, to_school, debug=False)`

**Returns raw transfer agreement data from assist.org API**

- Returns institution IDs, agreement metadata, and supported years
- Used internally by `get_degree_information()`

## Development

### Linting
```bash
./venv/bin/python3 -m flake8 scraper.py --max-line-length=100
```

### Testing
```bash
./venv/bin/python3 example_usage.py
```

## Architecture Notes

- **assist.org Integration**: Uses public REST API for agreement data
- **No Playwright**: Avoided browser automation - uses simple REST calls only
- **Fast & Reliable**: Queries typically complete in 1-2 seconds
- **Manual Course Viewing**: Users view detailed course mappings on assist.org directly

## What Works ✅

- Transfer agreement lookup between any CA community college and 4-year university
- Institution ID resolution
- Agreement metadata (code, years covered, institution type)

## Known Limitations

- Course-level detail mapping requires users to visit assist.org directly
- Detailed prerequisites/requirements not scraped (kept simple for reliability)

## Next Steps

1. Connect scraper to Cloudflare Workers API
2. Add school name autocomplete/search
3. Display results in chat interface
4. Add user bookmarking/comparison features
