# Combined HackCC API - Quick Reference

## Start Server
```bash
cd /home/eli/HackCC---IEEE---SWC
./venv/bin/python3 combined_api/start.py
```
Server runs on: `http://localhost:5000`

---

## Transfer API

### Check Transfer Compatibility
```bash
curl -X POST http://localhost:5000/api/transfer/check \
  -H "Content-Type: application/json" \
  -d '{
    "from_school": "Berkeley City College",
    "to_school": "University of California, Berkeley"
  }'
```

### Search Colleges
```bash
# All colleges
curl http://localhost:5000/api/transfer/schools

# Search by name
curl "http://localhost:5000/api/transfer/schools?q=berkeley"
curl "http://localhost:5000/api/transfer/schools?q=university%20of%20california"
```

---

## Internship API

### Get All Internships
```bash
curl http://localhost:5000/api/internships
```

### Filter Internships
```bash
# By category (FAANG+, Quant, Other)
curl "http://localhost:5000/api/internships?category=FAANG%2B"

# By company
curl "http://localhost:5000/api/internships?company=adobe"

# By location
curl "http://localhost:5000/api/internships?location=Remote"

# Combine filters
curl "http://localhost:5000/api/internships?category=FAANG%2B&location=San%20Francisco&limit=5"
```

### Pagination
```bash
# First 20 results
curl "http://localhost:5000/api/internships?limit=20&offset=0"

# Next 20 results
curl "http://localhost:5000/api/internships?limit=20&offset=20"
```

### Get Single Internship
```bash
curl http://localhost:5000/api/internships/0
curl http://localhost:5000/api/internships/42
```

### Statistics
```bash
curl http://localhost:5000/api/internships/stats
```

### Get Lists
```bash
# All companies
curl http://localhost:5000/api/internships/companies

# All locations
curl http://localhost:5000/api/internships/locations

# All categories
curl http://localhost:5000/api/internships/categories
```

### STEM Internships
```bash
# All STEM internships
curl http://localhost:5000/api/stem-internships

# By major
curl "http://localhost:5000/api/stem-internships?major=Computer%20Science"

# By company
curl "http://localhost:5000/api/stem-internships?company=microsoft"
```

### Refresh Data
```bash
curl -X POST http://localhost:5000/api/internships/refresh
```

---

## Utility

### Health Check
```bash
curl http://localhost:5000/health
```

### API Documentation
```bash
curl http://localhost:5000/
```

---

## Query Parameters Reference

### `/api/internships`
| Parameter | Type | Example |
|-----------|------|---------|
| `category` | string | `FAANG+`, `Quant`, `Other` |
| `company` | string | `adobe`, `google` |
| `location` | string | `San Francisco`, `Remote` |
| `limit` | integer | `10`, `50` |
| `offset` | integer | `0`, `20`, `40` |

### `/api/transfer/schools`
| Parameter | Type | Example |
|-----------|------|---------|
| `q` | string | `berkeley`, `davis` |

### `/api/stem-internships`
| Parameter | Type | Example |
|-----------|------|---------|
| `major` | string | `Computer Science` |
| `company` | string | `microsoft` |
| `limit` | integer | `10` |
| `offset` | integer | `0` |

---

## Response Fields

### Internship
- `company` - Company name
- `position` - Job title
- `location` - Work location
- `salary` - Hourly/annual rate
- `category` - FAANG+, Quant, or Other
- `apply_link` - Application URL
- `company_url` - Company website
- `age` - Days since posted
- `date_fetched` - When data was fetched

### Transfer Agreement
- `from_school` - Starting institution
- `to_school` - Transfer destination
- `institution_name` - Pathway school name
- `institution_code` - School code
- `is_community_college` - Boolean
- `years_supported` - Number of years

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error - Internal problem |

---

## Common Filters

### Popular Companies
```bash
curl "http://localhost:5000/api/internships?company=google"
curl "http://localhost:5000/api/internships?company=microsoft"
curl "http://localhost:5000/api/internships?company=amazon"
curl "http://localhost:5000/api/internships?company=meta"
curl "http://localhost:5000/api/internships?company=apple"
```

### Popular Locations
```bash
curl "http://localhost:5000/api/internships?location=San%20Francisco"
curl "http://localhost:5000/api/internships?location=New%20York"
curl "http://localhost:5000/api/internships?location=Seattle"
curl "http://localhost:5000/api/internships?location=Remote"
```

### By Category
```bash
curl "http://localhost:5000/api/internships?category=FAANG%2B"     # Top tier
curl "http://localhost:5000/api/internships?category=Quant"       # Quantitative
curl "http://localhost:5000/api/internships?category=Other"       # All others
```

---

## Python Examples

```python
import requests

# Check transfer
r = requests.post('http://localhost:5000/api/transfer/check', json={
    'from_school': 'Berkeley City College',
    'to_school': 'University of California, Berkeley'
})
print(r.json())

# Get FAANG+ internships
r = requests.get('http://localhost:5000/api/internships', params={
    'category': 'FAANG+',
    'limit': 10
})
for job in r.json()['internships']:
    print(f"{job['company']} - {job['position']} - {job['salary']}")

# Get internship stats
r = requests.get('http://localhost:5000/api/internships/stats')
stats = r.json()
print(f"Total: {stats['total_internships']}")
print(f"Categories: {stats['by_category']}")

# Search colleges
r = requests.get('http://localhost:5000/api/transfer/schools', params={'q': 'berkeley'})
print(r.json()['schools'])
```

---

## JavaScript Examples

```javascript
// Check transfer
const transfer = await fetch('http://localhost:5000/api/transfer/check', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    from_school: 'Berkeley City College',
    to_school: 'University of California, Berkeley'
  })
});
console.log(await transfer.json());

// Get FAANG+ internships
const jobs = await fetch(
  'http://localhost:5000/api/internships?category=FAANG%2B&limit=10'
);
const data = await jobs.json();
data.internships.forEach(job => {
  console.log(`${job.company} - ${job.position} - ${job.salary}`);
});

// Get stats
const stats = await fetch('http://localhost:5000/api/internships/stats');
console.log(await stats.json());

// Search colleges
const schools = await fetch(
  'http://localhost:5000/api/transfer/schools?q=berkeley'
);
console.log(await schools.json());
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Port 5000 already in use | `pkill -f "python3.*combined_api"` |
| No internship data | Run `/api/internships/refresh` or restart |
| Transfer check fails | Verify school names via `/api/transfer/schools` |
| Slow responses | Use pagination and filters |

---

## Full Documentation

See `API_DOCUMENTATION.md` for complete details on all endpoints, parameters, and examples.
