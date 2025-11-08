# LLM Chatbot Implementation Plan

## Overview
Integrate the frontend form data (community college, target universities, major) with the LLM chatbot to provide contextual responses and call your Flask API endpoints for relevant results.

---

## Step 1: Enhance Frontend Data Capture
**File**: `llm-chat-app-template/public/index.html` + `chat.js`

### Current State
- Form already collects: Community College (from_university), Target Universities, Major
- User selections stored in `selections` object on landing page

### Changes Needed
1. **Expose selections globally** - Make `selections` object accessible to chat functions
2. **Capture selections when chat starts** - When user clicks "Continue to Course Selection", store the data
3. **Add context to chat initialization** - Update welcome message to acknowledge their selections
4. **Store in sessionStorage** - Persist selections across chat sidebar open/close

### Key Functions to Modify
- `continueToNext()` - Call function to capture and store user data
- `initChatSidebar()` - Load and display user context in welcome message
- `sendMessage()` - Include user context when sending messages to LLM

---

## Step 2: Create API Proxy Endpoints in Cloudflare Worker
**File**: `llm-chat-app-template/src/index.ts`

### New Endpoints to Add
These will proxy requests to your Flask API at `http://localhost:5000`:

1. **GET `/api/data/transfer/check`** - Check transfer agreements
   - Accept: `from_school`, `to_school`
   - Proxy to: `POST http://localhost:5000/api/transfer/check`

2. **GET `/api/data/internships`** - Search internships
   - Accept: `major`, `company`, `location`, `limit`, `offset`
   - Proxy to: `GET http://localhost:5000/api/internships`

3. **GET `/api/data/mentorships`** - Search mentorships
   - Accept: `major`, `organization`, `cost`, `format`, `limit`, `offset`
   - Proxy to: `GET http://localhost:5000/api/mentorships`

4. **GET `/api/data/schools`** - Search schools
   - Accept: `q` (search query)
   - Proxy to: `GET http://localhost:5000/api/transfer/schools`

### Implementation Details
```typescript
// Pattern to follow:
const response = await fetch('http://localhost:5000/api/transfer/check', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(requestBody)
});
return response;
```

---

## Step 3: Update System Prompt with API Instructions
**File**: `llm-chat-app-template/src/index.ts`

### Modify SYSTEM_PROMPT to Include:
1. **User Context** - Dynamically inject from frontend
   - Their community college
   - Target universities
   - Major/field of study

2. **API Reference** - Tell LLM how to fetch data
   ```
   When the user asks about:
   - Transfer agreements → Call GET /api/data/transfer/check with their schools
   - Internships → Call GET /api/data/internships with their major
   - Mentorships → Call GET /api/data/mentorships with their major
   - School information → Call GET /api/data/schools
   ```

3. **Response Format Instructions** - How to format API responses for users

### Example Section
```
When users ask about internships or mentorship, fetch relevant opportunities using:
- For internships: Use their major and interests from context
- For transfer info: Use their from_school and to_school
- Format results clearly with key details (company, position, location, salary, etc.)
```

---

## Step 4: Pass User Context to LLM
**File**: `llm-chat-app-template/public/chat.js` + `index.html`

### Changes
1. **Modify `sendMessage()` function**:
   - Extract user context from form selections
   - Include context in request body sent to `/api/chat`
   - Send as separate field: `{ messages: [...], userContext: {...} }`

2. **Update LLM call in Worker**:
   - Receive `userContext` in request
   - Inject into system prompt dynamically
   - Tailor responses based on user's schools and major

### Data Structure
```javascript
{
  messages: [...],
  userContext: {
    communityCollege: "Southwestern College",
    targetUniversities: ["UC San Diego", "San Diego State"],
    major: "Computer Science"
  }
}
```

---

## Step 5: Frontend UI Enhancements (Optional)
**File**: `llm-chat-app-template/public/index.html`

### Improvements
1. **Display user context in chat header**
   - Show current major and target school(s)
   - Allow quick edit without re-doing form

2. **Quick action buttons based on major**
   - "Show internships for my major"
   - "Find mentors in CS"
   - "Check transfer requirements"

3. **Better response formatting**
   - Parse API responses into readable tables/lists
   - Add call-to-action buttons (e.g., "Apply now" links)

---

## Step 6: Testing Checklist

### Local Testing
- [ ] Start Flask API: `cd apis && python3 api.py`
- [ ] Start Worker: `cd llm-chat-app-template && npm run dev`
- [ ] Fill form (CC, Universities, Major)
- [ ] Open chat and verify user context appears
- [ ] Test API proxy calls work (check browser console/Network tab)

### Manual Queries to Test
1. "What internships are available for my major?"
2. "How do I transfer from [CC] to [University]?"
3. "Find mentorship programs for my field"
4. "Show me schools offering my major"

### Edge Cases
- [ ] User doesn't fill form (handle gracefully)
- [ ] API returns error (fallback response)
- [ ] Multiple universities selected (parse correctly)
- [ ] Chat works without active user context

---

## Step 7: Production Considerations

### Before Deploying
1. **Use actual API URL** - Replace `http://localhost:5000` with production Flask API URL
2. **CORS handling** - Ensure Flask API allows requests from Cloudflare domain
3. **Error handling** - Graceful fallbacks if Flask API is down
4. **Rate limiting** - Consider adding to avoid API abuse
5. **Authentication** - If needed, add API key to requests

### Configuration
- Store Flask API URL in `wrangler.jsonc` as environment variable
- Test with production URL before full deployment

---

## Implementation Order (Recommended)

1. ✅ **Step 1** - Capture form data in chat context (quickest win)
2. **Step 2** - Create API proxy endpoints (foundation for data access)
3. **Step 3** - Update system prompt with API instructions (teaches LLM to use APIs)
4. **Step 4** - Pass user context to LLM (personalizes responses)
5. **Step 5** - Frontend enhancements (UX improvements)
6. **Step 6** - Testing (validation)
7. **Step 7** - Deploy to production (go live)

---

## Files Modified Summary

| File | Changes | Complexity |
|------|---------|-----------|
| `llm-chat-app-template/public/chat.js` | Add context capture functions | Low |
| `llm-chat-app-template/public/index.html` | Integrate chat context display | Low |
| `llm-chat-app-template/src/index.ts` | Add API proxy endpoints + update system prompt | Medium |
| `llm-chat-app-template/src/types.ts` | Add types for userContext | Low |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│           User Browser                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Frontend (index.html + chat.js)                  │  │
│  │  - Form: CC, Universities, Major                 │  │
│  │  - Chat UI with user context display             │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────────┘
                 │ (messages + userContext)
                 ▼
┌─────────────────────────────────────────────────────────┐
│   Cloudflare Workers (index.ts)                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ /api/chat                                       │   │
│  │  - Receive messages + userContext               │   │
│  │  - Inject context into system prompt            │   │
│  │  - Call Llama 3.3 LLM                          │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │ /api/data/* (new proxy endpoints)              │   │
│  │  - /api/data/transfer/check                    │   │
│  │  - /api/data/internships                       │   │
│  │  - /api/data/mentorships                       │   │
│  │  - /api/data/schools                           │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────┬────────────────────────────────────────┘
                 │ (proxy requests)
                 ▼
┌─────────────────────────────────────────────────────────┐
│   Flask API (apis/api.py) - localhost:5000             │
│  - /api/transfer/check                                  │
│  - /api/internships                                     │
│  - /api/mentorships                                     │
│  - /api/transfer/schools                               │
└─────────────────────────────────────────────────────────┘
```

---

## Notes
- Form data already exists and collects the right fields
- Only need to wire it into the chat system
- API endpoints are already documented and working
- Main work is connecting the pieces together
