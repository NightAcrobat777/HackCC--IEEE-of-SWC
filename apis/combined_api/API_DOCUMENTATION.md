# Combined HackCC API Documentation

## Overview

The Combined HackCC API is a unified REST API that provides access to two main services:

1. **Transfer API** - Query college transfer programs and verify transfer compatibility between institutions
2. **Internship API** - Browse and search current internship listings from the 2026-SWE-College-Jobs repository

This single API combines both services into one cohesive interface, eliminating the need to maintain separate API servers.

---

## Quick Start

### Starting the API

```bash
cd /home/eli/HackCC---IEEE---SWC
./venv/bin/python3 combined_api/start.py
```

The server will start on `http://localhost:5000`

### Basic Health Check

```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "ok"
}
```

### View API Documentation

```bash
curl http://localhost:5000/
```

---

## Base URL

```
http://localhost:5000
```

For production deployments, replace `localhost:5000` with your server address.

---

## API Architecture

### Directory Structure

```
combined_api/
├── api.py                    # Main Flask application
├── start.py                  # Server startup script
├── example_usage.py          # Client usage examples
├── __init__.py              # Package initialization
├── scraper.py               # Transfer data scraper (assist.org)
├── colleges.json            # College database
├── fetch_and_clone_internships.py  # Internship data fetcher
└── internship_scraper.py    # Internship scraper
```

### Data Sources

- **Transfer Programs**: Fetched from [assist.org](https://www.assist.org) REST API
- **Internships**: Sourced from [2026-SWE-College-Jobs](https://github.com/speedyapply/2026-SWE-College-Jobs) repository
- **Colleges**: Local JSON database (`colleges.json`)

---

## Authentication

Currently, the API requires no authentication. All endpoints are publicly accessible.

---

## Response Format

All responses are returned in JSON format with the following structure:

### Success Response
```json
{
  "data": "...",
  "error": null,
  "metadata": {}
}
```

### Error Response
```json
{
  "error": "Error message describing what went wrong"
}
```

---

## Transfer API Endpoints

The Transfer API provides endpoints for querying college transfer compatibility.

### 1. Check Transfer Compatibility

**Endpoint:** `POST /api/transfer/check`

**Description:** Check if students can transfer between two institutions and get transfer agreement details.

**Request Body:**
```json
{
  "from_school": "Berkeley City College",
  "to_school": "University of California, Berkeley"
}
```

**Query Parameters:** None

**Required Fields:**
- `from_school` (string): Name of the institution the student is transferring from
- `to_school` (string): Name of the institution the student is transferring to

**Response (Success):**
```json
{
  "from_school": "Berkeley City College",
  "to_school": "University of California, Berkeley",
  "year": "2025-2026",
  "agreement": {
    "from_school": "Berkeley City College",
    "to_school": "University of California, Berkeley",
    "institution_name": "Vista Community College",
    "institution_code": "VISTA",
    "is_community_college": true,
    "years_supported": 30
  },
  "assist_url": "https://www.assist.org",
  "error": null
}
```

**Response (Error):**
```json
{
  "error": "Could not find institution IDs. From: 113, To: None"
}
```

**Status Codes:**
- `200 OK` - Transfer agreement found
- `400 Bad Request` - Missing required fields
- `500 Internal Server Error` - Server error

**Example:**
```bash
curl -X POST http://localhost:5000/api/transfer/check \
  -H "Content-Type: application/json" \
  -d '{
    "from_school": "Berkeley City College",
    "to_school": "University of California, Berkeley"
  }'
```

---

### 2. Search Colleges

**Endpoint:** `GET /api/transfer/schools`

**Description:** Search for available colleges or retrieve a complete list.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | No | Search query (partial match, case-insensitive) |

**Response (All Schools):**
```json
{
  "schools": [
    "Allan Hancock College",
    "American River College",
    "Antelope Valley College",
    "..."
  ]
}
```

**Response (Filtered):**
```json
{
  "schools": [
    "Berkeley City College",
    "University of California, Berkeley"
  ]
}
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Server error

**Examples:**
```bash
# Get all schools
curl http://localhost:5000/api/transfer/schools

# Search for schools containing "berkeley"
curl "http://localhost:5000/api/transfer/schools?q=berkeley"

# Search for UC schools
curl "http://localhost:5000/api/transfer/schools?q=university%20of%20california"
```

---

## Internship API Endpoints

The Internship API provides endpoints for browsing and filtering internship listings.

### 1. Get Internships

**Endpoint:** `GET /api/internships`

**Description:** Retrieve internship listings with optional filtering and pagination.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `category` | string | No | None | Filter by category (FAANG+, Quant, Other) |
| `company` | string | No | None | Filter by company name (partial match) |
| `location` | string | No | None | Filter by location (partial match) |
| `limit` | integer | No | None | Maximum number of results to return |
| `offset` | integer | No | 0 | Number of results to skip |

**Response:**
```json
{
  "total_count": 458,
  "returned_count": 2,
  "offset": 0,
  "internships": [
    {
      "company": "Ramp",
      "position": "Software Engineer Internship - Forward Deployed",
      "location": "New York, NY HQ",
      "salary": "$60/hr",
      "category": "FAANG+",
      "apply_link": "https://jobs.ashbyhq.com/ramp/ccb1aca4-79ac-414b-b7d8-bc908c575ef1",
      "company_url": "https://ramp.com",
      "age": "0d",
      "date_fetched": "2025-11-08 13:48:11"
    },
    {
      "company": "Adobe",
      "position": "2026 AI/ML Intern - Software Engineer Intern",
      "location": "San Jose",
      "salary": "$55/hr",
      "category": "FAANG+",
      "apply_link": "https://adobe.wd5.myworkdayjobs.com/...",
      "company_url": "https://www.adobe.com",
      "age": "1d",
      "date_fetched": "2025-11-08 13:48:11"
    }
  ],
  "metadata": {
    "source": "2026-SWE-College-Jobs Repository",
    "repository_url": "https://github.com/speedyapply/2026-SWE-College-Jobs",
    "date_fetched": "2025-11-08 13:48:11"
  }
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - No internship data available

**Examples:**
```bash
# Get all internships
curl http://localhost:5000/api/internships

# Get FAANG+ internships
curl "http://localhost:5000/api/internships?category=FAANG%2B"

# Get internships in San Francisco
curl "http://localhost:5000/api/internships?location=San%20Francisco"

# Get internships from Adobe
curl "http://localhost:5000/api/internships?company=adobe"

# Paginate results (get 10 at a time)
curl "http://localhost:5000/api/internships?limit=10&offset=0"
curl "http://localhost:5000/api/internships?limit=10&offset=10"

# Combine filters
curl "http://localhost:5000/api/internships?category=FAANG%2B&location=Remote&limit=5"
```

---

### 2. Get Internship by Index

**Endpoint:** `GET /api/internships/<int:index>`

**Description:** Retrieve a specific internship by its index position.

**URL Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `index` | integer | Yes | Zero-based index of the internship |

**Response:**
```json
{
  "company": "Ramp",
  "position": "Software Engineer Internship - Forward Deployed",
  "location": "New York, NY HQ",
  "salary": "$60/hr",
  "category": "FAANG+",
  "apply_link": "https://jobs.ashbyhq.com/ramp/ccb1aca4-79ac-414b-b7d8-bc908c575ef1",
  "company_url": "https://ramp.com",
  "age": "0d",
  "date_fetched": "2025-11-08 13:48:11"
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - Internship index out of range

**Example:**
```bash
curl http://localhost:5000/api/internships/0
curl http://localhost:5000/api/internships/42
```

---

### 3. Get Internship Statistics

**Endpoint:** `GET /api/internships/stats`

**Description:** Get statistics about the internship dataset including breakdown by category, top companies, and top locations.

**Query Parameters:** None

**Response:**
```json
{
  "total_internships": 458,
  "by_category": {
    "FAANG+": 25,
    "Other": 422,
    "Quant": 11
  },
  "top_companies": {
    "CIBC": 8,
    "Marvell": 7,
    "Walt Disney": 6,
    "KLA": 6,
    "Allegion": 5,
    "Bandwidth": 5,
    "General Dynamics Mission Systems": 5,
    "Motorola Solutions": 5,
    "Ramp": 5,
    "Raytheon": 5
  },
  "top_locations": {
    "New York, NY": 15,
    "San Francisco, CA": 18,
    "Boston, MA": 14,
    "Chicago, IL": 13,
    "Raleigh, NC": 7,
    "Santa Clara, CA": 8,
    "New York": 5,
    "Remote": 10,
    "Menlo Park, CA": 5,
    "Milwaukee, WI": 5
  },
  "metadata": {
    "source": "2026-SWE-College-Jobs Repository",
    "repository_url": "https://github.com/speedyapply/2026-SWE-College-Jobs",
    "date_fetched": "2025-11-08 13:48:11"
  }
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - No internship data available

**Example:**
```bash
curl http://localhost:5000/api/internships/stats
```

---

### 4. Get All Companies

**Endpoint:** `GET /api/internships/companies`

**Description:** Retrieve a complete list of all unique companies offering internships.

**Query Parameters:** None

**Response:**
```json
{
  "count": 127,
  "companies": [
    "Adobe",
    "Allegion",
    "Amazon",
    "Apple",
    "Bandwidth",
    "...",
    "Walt Disney"
  ]
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - No internship data available

**Example:**
```bash
curl http://localhost:5000/api/internships/companies
```

---

### 5. Get All Locations

**Endpoint:** `GET /api/internships/locations`

**Description:** Retrieve a complete list of all unique internship locations.

**Query Parameters:** None

**Response:**
```json
{
  "count": 45,
  "locations": [
    "Austin, TX",
    "Boston, MA",
    "Chicago, IL",
    "Los Angeles, CA",
    "Menlo Park, CA",
    "New York, NY",
    "Remote",
    "San Francisco, CA",
    "...",
    "Sunnyvale, CA"
  ]
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - No internship data available

**Example:**
```bash
curl http://localhost:5000/api/internships/locations
```

---

### 6. Get All Categories

**Endpoint:** `GET /api/internships/categories`

**Description:** Retrieve all available internship categories.

**Query Parameters:** None

**Response:**
```json
{
  "count": 3,
  "categories": [
    "FAANG+",
    "Other",
    "Quant"
  ]
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - No internship data available

**Example:**
```bash
curl http://localhost:5000/api/internships/categories
```

---

### 7. Get STEM Internships

**Endpoint:** `GET /api/stem-internships`

**Description:** Retrieve internships specifically tagged for STEM majors, with optional filtering.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `major` | string | No | None | Filter by major field (partial match) |
| `company` | string | No | None | Filter by company name (partial match) |
| `limit` | integer | No | None | Maximum number of results to return |
| `offset` | integer | No | 0 | Number of results to skip |

**Response:**
```json
{
  "total_count": 85,
  "returned_count": 2,
  "offset": 0,
  "internships": [
    {
      "company": "Microsoft",
      "position": "Software Engineer Intern",
      "major": "Computer Science",
      "location": "Seattle, WA",
      "salary": "$50/hr",
      "apply_link": "https://careers.microsoft.com/...",
      "date_fetched": "2025-11-08 13:48:11"
    },
    {
      "company": "Google",
      "position": "Engineering Practicum - Machine Learning",
      "major": "Computer Science",
      "location": "Mountain View, CA",
      "salary": "$55/hr",
      "apply_link": "https://careers.google.com/...",
      "date_fetched": "2025-11-08 13:48:11"
    }
  ],
  "stem_majors": [
    "Computer Science",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Mathematics"
  ],
  "last_updated": "2025-11-08 13:48:11"
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - No STEM internship data available

**Examples:**
```bash
# Get all STEM internships
curl http://localhost:5000/api/stem-internships

# Filter by major
curl "http://localhost:5000/api/stem-internships?major=Computer%20Science"

# Filter by company
curl "http://localhost:5000/api/stem-internships?company=microsoft"

# Paginate STEM internships
curl "http://localhost:5000/api/stem-internships?limit=10&offset=0"
```

---

### 8. Refresh Internship Data

**Endpoint:** `POST /api/internships/refresh`

**Description:** Manually trigger a refresh of internship data from the source repository. This clones/updates the 2026-SWE-College-Jobs repository and re-fetches all internships.

**Request Body:** Empty or null

**Response (Success):**
```json
{
  "success": true,
  "message": "Internship data refreshed successfully",
  "total_internships": 458,
  "timestamp": "2025-11-08 23:05:32"
}
```

**Response (Error):**
```json
{
  "error": "Failed to update repository"
}
```

**Status Codes:**
- `200 OK` - Refresh successful
- `500 Internal Server Error` - Refresh failed

**Notes:**
- This endpoint requires network access to GitHub
- Refresh can take 10-30 seconds depending on internet speed
- Use sparingly in production to avoid rate limiting

**Example:**
```bash
curl -X POST http://localhost:5000/api/internships/refresh
```

---

## Utility Endpoints

### Health Check

**Endpoint:** `GET /health`

**Description:** Simple health check endpoint to verify the API is running.

**Query Parameters:** None

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- `200 OK` - API is healthy

**Example:**
```bash
curl http://localhost:5000/health
```

---

### API Documentation

**Endpoint:** `GET /`

**Description:** Returns the complete API documentation including all available endpoints and query parameters.

**Query Parameters:** None

**Response:**
```json
{
  "message": "Combined HackCC API",
  "version": "1.0",
  "description": "Unified API for college transfer programs and internship listings",
  "sections": {
    "transfer": {
      "base": "/api/transfer",
      "endpoints": {
        "POST /api/transfer/check": "Check transfer compatibility between schools",
        "GET /api/transfer/schools": "Search/list available colleges"
      }
    },
    "internships": {
      "base": "/api/internships",
      "endpoints": {
        "GET /api/internships": "Get all internships with optional filters",
        "GET /api/internships/<id>": "Get specific internship by index",
        "GET /api/internships/stats": "Get internship statistics",
        "GET /api/internships/companies": "Get all companies",
        "GET /api/internships/locations": "Get all locations",
        "GET /api/internships/categories": "Get all categories",
        "GET /api/stem-internships": "Get STEM-specific internships",
        "POST /api/internships/refresh": "Refresh internship data"
      }
    }
  },
  "query_parameters": {
    "/api/internships": {
      "category": "Filter by category (FAANG+, Quant, Other)",
      "company": "Filter by company name",
      "location": "Filter by location",
      "limit": "Limit results",
      "offset": "Pagination offset"
    },
    "/api/transfer/schools": {
      "q": "Search query for college names"
    }
  }
}
```

**Example:**
```bash
curl http://localhost:5000/
```

---

## Error Handling

### Error Response Format

All error responses include an `error` field with a descriptive message:

```json
{
  "error": "Missing required fields: from_school and to_school"
}
```

### Common HTTP Status Codes

| Status | Meaning | Example |
|--------|---------|---------|
| `200 OK` | Request successful | Internship data returned |
| `400 Bad Request` | Invalid request parameters | Missing required fields |
| `404 Not Found` | Resource not found | Internship index out of range |
| `500 Internal Server Error` | Server error | Database connection failed |

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Missing required fields: from_school and to_school` | Transfer check called without required fields | Include both `from_school` and `to_school` in request body |
| `Could not find institution IDs` | School names don't match database | Verify school names using `/api/transfer/schools` endpoint |
| `No internship data available` | Data files missing or not loaded | Run `/api/internships/refresh` or restart server |
| `Internship not found` | Index out of range | Check total count via `/api/internships/stats` first |

---

## Data Models

### Internship Object

```json
{
  "company": "String",
  "position": "String",
  "location": "String",
  "salary": "String (e.g., '$50/hr')",
  "category": "String (FAANG+, Quant, Other)",
  "apply_link": "String (URL)",
  "company_url": "String (URL)",
  "age": "String (e.g., '0d', '3d')",
  "date_fetched": "String (YYYY-MM-DD HH:MM:SS)"
}
```

### Transfer Agreement Object

```json
{
  "from_school": "String",
  "to_school": "String",
  "institution_name": "String (pathway school)",
  "institution_code": "String",
  "is_community_college": "Boolean",
  "years_supported": "Integer"
}
```

### STEM Internship Object

```json
{
  "company": "String",
  "position": "String",
  "major": "String",
  "location": "String",
  "salary": "String",
  "apply_link": "String (URL)",
  "date_fetched": "String (YYYY-MM-DD HH:MM:SS)"
}
```

---

## Usage Examples

### Example 1: Find Transfer Programs

```bash
# Check if students can transfer from Berkeley City College to UC Berkeley
curl -X POST http://localhost:5000/api/transfer/check \
  -H "Content-Type: application/json" \
  -d '{
    "from_school": "Berkeley City College",
    "to_school": "University of California, Berkeley"
  }'
```

### Example 2: Search for FAANG+ Internships in San Francisco

```bash
curl "http://localhost:5000/api/internships?category=FAANG%2B&location=San%20Francisco&limit=10"
```

### Example 3: Get Remote Internship Statistics

```bash
curl "http://localhost:5000/api/internships?location=Remote"
```

### Example 4: Paginate Through All Internships

```bash
# Get first 20
curl "http://localhost:5000/api/internships?limit=20&offset=0"

# Get next 20
curl "http://localhost:5000/api/internships?limit=20&offset=20"

# Get next 20
curl "http://localhost:5000/api/internships?limit=20&offset=40"
```

### Example 5: Search Colleges and Check Transfer

```bash
# Search for colleges
curl "http://localhost:5000/api/transfer/schools?q=davis"

# Check transfer to UC Davis
curl -X POST http://localhost:5000/api/transfer/check \
  -H "Content-Type: application/json" \
  -d '{
    "from_school": "De Anza College",
    "to_school": "University of California, Davis"
  }'
```

### Example 6: Refresh Internship Data

```bash
curl -X POST http://localhost:5000/api/internships/refresh
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. However, for production deployments, consider implementing rate limiting to prevent abuse.

---

## CORS

Cross-Origin Resource Sharing (CORS) is enabled on all endpoints, allowing requests from any origin.

---

## Performance Considerations

### Response Times

- **Transfer API**: ~2-3 seconds (makes external API calls to assist.org)
- **Internship endpoints**: ~10-100ms (local JSON queries)
- **Search endpoints**: ~50-150ms (filtering local data)

### Data Size

- **Total internships**: ~458 records
- **STEM internships**: ~85 records
- **Colleges database**: ~250+ institutions

### Optimization Tips

1. Use pagination with `limit` and `offset` for large result sets
2. Use filters to reduce data size before retrieval
3. Cache responses on the client side when appropriate
4. Avoid calling `/api/internships/refresh` too frequently

---

## Troubleshooting

### API won't start

**Problem:** `Address already in use - Port 5000`

**Solution:** Kill the existing process:
```bash
pkill -f "python3.*combined_api"
```

### No internship data

**Problem:** `No internship data available` error

**Solution:** 
1. Check if data files exist: `ls -la /home/eli/HackCC---IEEE---SWC/*.json`
2. Refresh data: `curl -X POST http://localhost:5000/api/internships/refresh`
3. Restart the server

### Transfer check fails

**Problem:** `Could not find institution IDs`

**Solution:**
1. Verify school name spelling using: `curl "http://localhost:5000/api/transfer/schools?q=berkley"`
2. Use exact names from the colleges list

### Slow responses

**Problem:** API requests taking 10+ seconds

**Solution:**
1. Check network connectivity to assist.org
2. Avoid making many concurrent requests
3. Use pagination and filters to reduce data size

---

## Client Library Examples

### Python

```python
import requests

# Check transfer
response = requests.post('http://localhost:5000/api/transfer/check', json={
    'from_school': 'Berkeley City College',
    'to_school': 'University of California, Berkeley'
})
print(response.json())

# Get internships
response = requests.get('http://localhost:5000/api/internships', params={
    'category': 'FAANG+',
    'limit': 10
})
print(response.json())
```

### JavaScript

```javascript
// Check transfer
const transferResponse = await fetch('http://localhost:5000/api/transfer/check', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    from_school: 'Berkeley City College',
    to_school: 'University of California, Berkeley'
  })
});
const transferData = await transferResponse.json();
console.log(transferData);

// Get internships
const internshipsResponse = await fetch(
  'http://localhost:5000/api/internships?category=FAANG%2B&limit=10'
);
const internshipsData = await internshipsResponse.json();
console.log(internshipsData);
```

### cURL

```bash
# Transfer check
curl -X POST http://localhost:5000/api/transfer/check \
  -H "Content-Type: application/json" \
  -d '{"from_school":"Berkeley City College","to_school":"University of California, Berkeley"}'

# Get internships
curl "http://localhost:5000/api/internships?category=FAANG%2B&limit=10"

# Get stats
curl http://localhost:5000/api/internships/stats
```

---

## Support & Issues

For issues or questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review example requests in the [Usage Examples](#usage-examples) section
3. Verify data files are present and valid
4. Check server logs for detailed error messages

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-08 | Initial release - Combined Transfer and Internship APIs |

---

## License

This API is part of the HackCC project and is available for educational use.

---

**Last Updated:** 2025-11-08
