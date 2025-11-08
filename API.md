# TransferTree Flask API Documentation

## Setup

### Install Dependencies
```bash
pip install flask flask-cors
```

### Run the API Server
```bash
./venv/bin/python3 api.py
```

Server runs on `http://localhost:5000`

---

## Endpoints

### 1. Check Transfer Agreement
**POST** `/api/transfer`

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
curl -X POST http://localhost:5000/api/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "from_school": "Southwestern College",
    "to_school": "University of California, Berkeley"
  }'
```

#### Python Example
```python
import requests

response = requests.post('http://localhost:5000/api/transfer', json={
    'from_school': 'Southwestern College',
    'to_school': 'University of California, Berkeley'
})

data = response.json()
if not data.get('error'):
    agreement = data['agreement']
    print(f"Transfer: {agreement['from_school']} → {agreement['to_school']}")
    print(f"Pathway: {agreement['institution_name']}")
    print(f"Years: {agreement['years_supported']}")
```

#### JavaScript Example (Fetch)
```javascript
const response = await fetch('http://localhost:5000/api/transfer', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    from_school: 'Southwestern College',
    to_school: 'University of California, Berkeley'
  })
});

const data = await response.json();
if (!data.error) {
  console.log(`Agreement: ${data.agreement.institution_name}`);
  console.log(`View: ${data.assist_url}`);
}
```

---

### 2. Search Schools
**GET** `/api/schools`

Returns a list of schools, optionally filtered by search query.

#### Request
```
GET /api/schools?q=berkeley
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
curl http://localhost:5000/api/schools

# Search for schools
curl http://localhost:5000/api/schools?q=berkeley
```

#### JavaScript Example
```javascript
const query = 'berkeley';
const response = await fetch(`http://localhost:5000/api/schools?q=${encodeURIComponent(query)}`);
const data = await response.json();
console.log(data.schools);
```

---

### 3. Health Check
**GET** `/health`

Simple health check endpoint.

#### Response (200)
```json
{
  "status": "ok"
}
```

#### cURL Example
```bash
curl http://localhost:5000/health
```

---

## Integration with Chat App

### Update Cloudflare Worker

In `llm-chat-app-template/src/index.ts`, add logic to detect transfer queries:

```typescript
const TRANSFER_API = 'http://localhost:5000'; // Update in production

async function handleChatRequest(request: Request, env: Env): Promise<Response> {
  const { messages = [] } = await request.json();
  
  // Check if user is asking about transfers
  const lastMessage = messages[messages.length - 1]?.content || '';
  const transferMatch = lastMessage.match(/transfer.*from\s+(.+?)\s+to\s+(.+?)($|[?.!])/i);
  
  if (transferMatch) {
    const [, fromSchool, toSchool] = transferMatch;
    
    try {
      const transferResponse = await fetch(`${TRANSFER_API}/api/transfer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from_school: fromSchool.trim(),
          to_school: toSchool.trim()
        })
      });
      
      const transferData = await transferResponse.json();
      
      if (!transferData.error && transferData.agreement) {
        const formattedResponse = `
✅ Transfer Agreement Found

From: ${transferData.agreement.from_school}
To: ${transferData.agreement.to_school}
Pathway: ${transferData.agreement.institution_name} (${transferData.agreement.institution_code})
Years Supported: ${transferData.agreement.years_supported}

View detailed course mappings at: ${transferData.assist_url}
        `.trim();
        
        return new Response(formattedResponse, {
          status: 200,
          headers: { 'content-type': 'text/plain' }
        });
      }
    } catch (e) {
      console.error('Transfer API error:', e);
    }
  }
  
  // Fall back to LLM for non-transfer queries
  // ... existing LLM code ...
}
```

---

## Error Handling

### Common Errors

| Status | Error | Reason |
|--------|-------|--------|
| 400 | `Missing required fields` | `from_school` or `to_school` not provided |
| 400 | `Could not find institution IDs` | School name not found in assist.org database |
| 500 | Server error | Unexpected error (check server logs) |

---

## Performance

- Transfer check: ~1-2 seconds (REST API call to assist.org)
- School search: <100ms (local JSON lookup)
- All requests are cached by assist.org, so repeated queries are faster

---

## Testing

### Quick Test with Example Script
```bash
./venv/bin/python3 example_api_usage.py
```

### Manual Testing
```bash
# Test transfer endpoint
./venv/bin/python3 -c "
import requests
import json

response = requests.post('http://localhost:5000/api/transfer', json={
    'from_school': 'Southwestern College',
    'to_school': 'University of California, Berkeley'
})
print(json.dumps(response.json(), indent=2))
"

# Test search endpoint
curl 'http://localhost:5000/api/schools?q=berkeley'
```

---

## Deployment

For production:
1. Use a production WSGI server: `pip install gunicorn`
2. Run: `gunicorn -w 4 -b 0.0.0.0:5000 api.py`
3. Put behind a reverse proxy (Nginx)
4. Update chat app to call the production URL
