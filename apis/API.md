# HackCC Unified API Documentation

## Setup

### Install Dependencies
```bash
pip install flask flask-cors
```

### Run the API Server
```bash
cd /apis
./venv/bin/python3 api.py
```

Server runs on `http://localhost:5000`

---

## API Overview

This unified API provides three main sections:

- **Transfer Programs**: Check college transfer agreements
- **Internships**: Browse internship opportunities (including STEM-specific)
- **Mentorship**: Find mentorship programs

---

## Transfer Endpoints

### 1. Check Transfer Agreement
**POST** `/api/transfer/check`

Checks if a transfer agreement exists between two schools and returns agreement details.

#### Request
```json
{
  "from_school": "Southwestern College",
  "to_school": "University of California, Berkeley"
}
```

#### Response (Success - 200)
```json
{
  "from_school": "Southwestern College",
  "to_school": "University of California, Berkeley",
  "year": "2025-2026",
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

#### Response (Error - 400)
```json
{
  "from_school": "Invalid College",
  "to_school": "University of California, Berkeley",
  "year": "2025-2026",
  "agreement": null,
  "assist_url": "https://www.assist.org",
  "error": "Could not find institution IDs. From: None, To: 79"
}
```

#### cURL Example
```bash
curl -X POST http://localhost:5000/api/transfer/check \
  -H "Content-Type: application/json" \
  -d '{
    "from_school": "Southwestern College",
    "to_school": "University of California, Berkeley"
  }'
```

### 2. Search Schools
**GET** `/api/transfer/schools`

Returns a list of schools, optionally filtered by search query.

#### Request
```
GET /api/transfer/schools?q=berkeley
```

#### Response (200)
```json
{
  "schools": [
    "University of California, Berkeley",
    "Berkeley City College"
  ]
}
```

#### Parameters
- `q` (optional): Search query. Returns schools containing this string (case-insensitive)

#### cURL Example
```bash
# Get all schools
curl http://localhost:5000/api/transfer/schools

# Search for schools
curl http://localhost:5000/api/transfer/schools?q=berkeley
```

---

## Internship Endpoints

### 1. Get All Internships
**GET** `/api/internships`

Returns paginated list of internships with optional filters.

#### Query Parameters
- `category` - Filter by category (FAANG+, Quant, Other)
- `company` - Filter by company name
- `location` - Filter by location
- `limit` - Limit results
- `offset` - Pagination offset

#### Example
```bash
curl 'http://localhost:5000/api/internships?category=FAANG%2B&limit=10&offset=0'
```

### 2. Get Internship by Index
**GET** `/api/internships/<id>`

Get a specific internship by its index.

```bash
curl http://localhost:5000/api/internships/0
```

### 3. Internship Statistics
**GET** `/api/internships/stats`

Get statistics about all internships.

```bash
curl http://localhost:5000/api/internships/stats
```

### 4. Get All Companies
**GET** `/api/internships/companies`

List all unique companies with internships.

```bash
curl http://localhost:5000/api/internships/companies
```

### 5. Get All Locations
**GET** `/api/internships/locations`

List all unique locations with internships.

```bash
curl http://localhost:5000/api/internships/locations
```

### 6. Get All Categories
**GET** `/api/internships/categories`

List all internship categories.

```bash
curl http://localhost:5000/api/internships/categories
```

### 7. Get STEM Internships
**GET** `/api/stem-internships`

Get STEM-specific internship opportunities.

#### Query Parameters
- `major` - Filter by major
- `company` - Filter by company name
- `limit` - Limit results
- `offset` - Pagination offset

```bash
curl 'http://localhost:5000/api/stem-internships?major=computer%20science'
```

### 8. Refresh Internship Data
**POST** `/api/internships/refresh`

Refresh internship data from the source repository.

```bash
curl -X POST http://localhost:5000/api/internships/refresh
```

---

## Mentorship Endpoints

### 1. Get All Mentorships
**GET** `/api/mentorships`

Returns paginated list of mentorship programs with optional filters.

#### Query Parameters
- `major` - Filter by major
- `organization` - Filter by organization name
- `target_audience` - Filter by target audience
- `cost` - Filter by cost (e.g., "free")
- `format` - Filter by format (e.g., "virtual", "hybrid", "in-person")
- `limit` - Limit results
- `offset` - Pagination offset

#### Example
```bash
curl 'http://localhost:5000/api/mentorships?cost=free&limit=10'
```

### 2. Get Mentorship by Index
**GET** `/api/mentorships/<id>`

Get a specific mentorship program by its index.

```bash
curl http://localhost:5000/api/mentorships/0
```

### 3. Mentorship Statistics
**GET** `/api/mentorships/stats`

Get statistics about all mentorship programs.

```bash
curl http://localhost:5000/api/mentorships/stats
```

### 4. Get All Organizations
**GET** `/api/mentorships/organizations`

List all unique organizations offering mentorships.

```bash
curl http://localhost:5000/api/mentorships/organizations
```

### 5. Get All Majors
**GET** `/api/mentorships/majors`

List all majors supported by mentorship programs.

```bash
curl http://localhost:5000/api/mentorships/majors
```

### 6. Get Free Mentorships
**GET** `/api/mentorships/free`

Get only free mentorship programs.

```bash
curl http://localhost:5000/api/mentorships/free
```

### 7. Get Community College Friendly Programs
**GET** `/api/mentorships/community-college`

Get mentorship programs friendly to community college students.

```bash
curl http://localhost:5000/api/mentorships/community-college
```

### 8. Refresh Mentorship Data
**POST** `/api/mentorships/refresh`

Refresh mentorship data from the scraper.

```bash
curl -X POST http://localhost:5000/api/mentorships/refresh
```

---

## Health Check

### Health Status
**GET** `/health`

Simple health check endpoint.

#### Response (200)
```json
{
  "status": "ok"
}
```

```bash
curl http://localhost:5000/health
```

---

## API Documentation
**GET** `/`

Get full API documentation with all endpoints and query parameters.

```bash
curl http://localhost:5000/
```

---

## Error Handling

### Common Errors

| Status | Error | Reason |
|--------|-------|--------|
| 400 | `Missing required fields` | Required parameters not provided |
| 404 | `No data available` | Data file not found or empty |
| 404 | `Endpoint not found` | Invalid endpoint |
| 500 | `Internal server error` | Unexpected error (check server logs) |

---

## Performance

- Transfer check: ~1-2 seconds (REST API call to assist.org)
- School search: <100ms (local JSON lookup)
- Internship queries: <100ms (local JSON lookup)
- Mentorship queries: <100ms (local JSON lookup)

---

## Testing

### Manual Testing with cURL

```bash
# Health check
curl http://localhost:5000/health

# List all schools
curl http://localhost:5000/api/transfer/schools

# Check transfer agreement
curl -X POST http://localhost:5000/api/transfer/check \
  -H "Content-Type: application/json" \
  -d '{
    "from_school": "Southwestern College",
    "to_school": "University of California, Berkeley"
  }'

# Get free mentorships
curl http://localhost:5000/api/mentorships/free

# Get STEM internships for Computer Science
curl 'http://localhost:5000/api/stem-internships?major=computer%20science&limit=5'
```

---

## Deployment

For production:
1. Use a production WSGI server: `pip install gunicorn`
2. Run: `gunicorn -w 4 -b 0.0.0.0:5000 api:app`
3. Put behind a reverse proxy (Nginx)
4. Update chat app to call the production URL
