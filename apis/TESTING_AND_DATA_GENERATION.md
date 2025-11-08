# Testing and Data Generation

This document describes the testing and data generation scripts available in the apis directory.

## Quick Start

### 1. Generate Colleges JSON (Fastest)

```bash
cd apis
python3 generate_comprehensive_colleges.py
```

This generates a `colleges.json` file with all California colleges and universities.

### 2. Test All API Endpoints

First, start the API server in one terminal:

```bash
cd apis
python3 api.py
```

Then in another terminal, run the comprehensive test suite:

```bash
cd apis
python3 test_api_and_generate_colleges.py
```

## Scripts

### `generate_comprehensive_colleges.py`

**Purpose**: Generate a comprehensive `colleges.json` file with all California transfer institutions.

**Features**:
- ✅ Generates complete list of community colleges
- ✅ Includes all CSU (California State University) campuses
- ✅ Includes all UC (University of California) campuses
- ✅ Includes major private universities
- ✅ No external dependencies required
- ✅ Fast execution (~1 second)

**Usage**:

```bash
python3 generate_comprehensive_colleges.py
```

**Output**:
- Creates/overwrites `colleges.json` in the current directory
- Contains `from_institution` and `transfer_institution` arrays

**Example Output**:
```
============================================================
Generating Comprehensive Colleges JSON
============================================================

✓ Generated comprehensive colleges.json
  - From institutions: 189
  - Transfer institutions: 54
  - File: /home/eli/HackCC---IEEE---SWC/apis/colleges.json
  - Size: 8.5 KB

============================================================
Success!
============================================================
```

### `test_api_and_generate_colleges.py`

**Purpose**: Comprehensive API testing suite that also generates colleges.json

**Features**:
- ✅ Tests all main API endpoints
- ✅ Validates transfers, internships, and mentorships modules
- ✅ Performs transfer lookup checks
- ✅ Discovers colleges through API interactions
- ✅ Generates colleges.json from discovered institutions
- ⚠️ Requires running API server

**Prerequisites**:
- Python 3.7+
- `requests` library (installed via `pip install -r requirements.txt`)
- API server running on `http://localhost:5000`

**Usage**:

```bash
# Terminal 1: Start the API server
python3 api.py

# Terminal 2: Run tests
python3 test_api_and_generate_colleges.py
```

**Tests Performed**:

1. **Health Check** - Verifies API is running
2. **Home Endpoint** - Retrieves API documentation
3. **Transfer Schools** - Gets all available transfer colleges
4. **Internships** - Tests internship retrieval and statistics
5. **STEM Internships** - Tests STEM-specific internships
6. **Mentorships** - Tests mentorship programs and filtering
7. **Free Mentorships** - Tests free mentorship filtering
8. **Transfer Checks** - Tests sample transfer compatibility checks
9. **College Discovery** - Attempts to discover all valid college combinations

**Example Output**:

```
============================================================
HackCC API Test Suite & Colleges Generator
============================================================

Testing API connectivity...
✓ Health check: 200

--- Testing Endpoints ---
✓ Home endpoint: 200

--- Transfer Module ---
✓ Retrieved 189 schools from API

--- Internship Module ---
✓ Internships endpoint: 450 total internships
✓ Internship stats: 450 internships in 3 categories
✓ STEM internships: found results

--- Mentorship Module ---
✓ Mentorships endpoint: 87 total mentorships
✓ Free mentorships: found results

--- Transfer Check Sample ---
✓ Transfer check works

Attempting to discover colleges through transfer checks...
Testing sample transfers to find all valid college combinations...
  Tested 10 combinations (8 successful)
✓ Tested 25 transfer combinations (20 successful)

✓ Generated colleges.json
  - From institutions: 189
  - Transfer institutions: 54
  - File size: 8.5 KB

============================================================
All tests completed!
============================================================
```

## Data Files

After running either script, you'll have:

### `colleges.json`
Location: `apis/colleges.json` (or same directory as script)

Structure:
```json
{
  "from_institution": [
    "College name 1",
    "College name 2",
    ...
  ],
  "transfer_institution": [
    "University name 1",
    "University name 2",
    ...
  ]
}
```

**Usage in API**: 
- `from_institution`: Community colleges students can transfer FROM
- `transfer_institution`: 4-year universities students can transfer TO

## What Gets Tested

### API Endpoints Tested

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Server health check |
| `/` | GET | API documentation |
| `/api/transfer/schools` | GET | List all transfer schools |
| `/api/transfer/check` | POST | Check transfer compatibility |
| `/api/internships` | GET | List all internships |
| `/api/internships/stats` | GET | Internship statistics |
| `/api/stem-internships` | GET | STEM-specific internships |
| `/api/mentorships` | GET | List mentorship programs |
| `/api/mentorships/free` | GET | Free mentorship programs |

### Data Validation

Both scripts validate:
- ✅ College name completeness
- ✅ No duplicate entries
- ✅ Alphabetical sorting
- ✅ JSON file validity
- ✅ File encoding (UTF-8)

## Troubleshooting

### Script: "API is not running"

**Error**: 
```
✗ API is not running. Please start it with: python3 api.py
```

**Solution**: Start the API server in another terminal
```bash
python3 api.py
```

### Script: "Error loading data files"

**Error**: 
```
✗ Error getting schools: Connection refused
```

**Solution**: Ensure API is running and accessible at `http://localhost:5000`

### Missing `requests` library

**Error**: 
```
ModuleNotFoundError: No module named 'requests'
```

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### JSON Generation Issues

If `colleges.json` doesn't exist or is empty:

1. Ensure script has write permissions in the current directory
2. Check disk space
3. Run with `python3 -u` for unbuffered output
4. Verify file isn't locked by another process

## Manual API Testing

Instead of running automated tests, you can manually test endpoints:

```bash
# Get all schools
curl http://localhost:5000/api/transfer/schools

# Search for a specific school
curl 'http://localhost:5000/api/transfer/schools?q=berkeley'

# Check transfer agreement
curl -X POST http://localhost:5000/api/transfer/check \
  -H "Content-Type: application/json" \
  -d '{
    "from_school": "Southwestern College",
    "to_school": "University of California, Berkeley"
  }'

# Get internship statistics
curl http://localhost:5000/api/internships/stats

# Get free mentorships
curl 'http://localhost:5000/api/mentorships/free?limit=5'
```

## Performance Notes

- **`generate_comprehensive_colleges.py`**: ~1 second
- **`test_api_and_generate_colleges.py`**: ~15-30 seconds (depending on transfer checks)

## File Locations

- Scripts: `/apis/`
- Output: `/apis/colleges.json`
- Config: `/apis/api.py`

## Dependencies

See `requirements.txt` for full list. Key dependencies:
- `flask` - Web framework
- `flask-cors` - CORS support
- `requests` - HTTP library for testing

## Next Steps

After generating `colleges.json`:

1. Verify file content: `cat colleges.json | python3 -m json.tool`
2. Copy to root: `cp colleges.json ../`
3. Restart API for changes to take effect
4. Test endpoints with the new data

---

For more API documentation, see `API.md`
