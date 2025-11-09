# BetterTransfer - AI-Powered College Transfer Assistant

An intelligent platform built for California community college students to navigate their transfer journey from community college to 4-year universities. Created by Gabe, Eli, Angelo, and Tim for the HackCC hackathon (IEEE HackCC 2025).

## Features

### 🎯 **Interactive Transfer Planning**
- **4-Step Guided Flow**: Intuitive card-based interface with progress tracking
  1. Select your current community college
  2. Choose target universities (multiple selections supported)
  3. Pick your major
  4. Review and confirm your transfer profile
- **Smart Search**: Real-time search with relevance sorting and debouncing for smooth UX
- **Multi-School Selection**: Select and compare multiple target universities simultaneously
- **Profile Persistence**: Your selections are saved and used throughout the chat experience

### 🤖 **AI Transfer Assistant**
- **Context-Aware Chat**: AI assistant with knowledge of your profile (community college, target schools, major)
- **Natural Language Queries**: Ask questions in plain English about your transfer journey
- **Streaming Responses**: Real-time AI responses with markdown formatting support
- **Quick Actions**: One-click access to common queries
  - "What are the transfer requirements?"
  - "Find internships in my field"
  - "Mentorship programs available?"
  - "Free resources and programs"

### 🎓 **College Transfer Programs**
- **Transfer Agreement Lookup**: Check articulation agreements between your CC and target universities
- **assist.org Integration**: Direct access to official California transfer data
- **Multi-School Comparison**: See transfer agreements for all your selected universities at once

### 💼 **Internship Discovery**
- **Major-Specific Search**: Find internships tailored to your field of study
- **STEM Opportunities**: Dedicated STEM internship database with 2026 opportunities
- **Company & Location Filters**: Browse by company, location, season, and category
- **API Integration**: Real-time access to curated internship database

### 👥 **Mentorship Programs**
- **Community College Focus**: Programs specifically designed for CC transfer students
- **Free Resources**: Dedicated filtering for no-cost mentorship opportunities
- **Organization Directory**: Browse programs by major, organization, and format
- **Instant Recommendations**: AI provides personalized mentorship suggestions

### 🎨 **Modern User Experience**
- **Custom Cursor**: Elegant custom cursor with hover effects and click ripples
- **Smooth Animations**: Card-based transitions with Swiper.js
- **Responsive Design**: Mobile-optimized interface that works on all devices
- **Center-Stage Chat**: Full-width chat interface that slides in from the center
- **Back Navigation**: Easy navigation between form and chat with preserved state

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
├── llm-chat-app-template/              # Frontend web application
│   ├── public/                          # Static frontend assets
│   │   ├── index.html                   # Main application UI (BetterTransfer interface)
│   │   ├── colleges.json                # California colleges database
│   │   └── chat.js                      # Chat interface utilities
│   ├── src/                             # TypeScript source code
│   │   ├── index.ts                     # Cloudflare Worker entry point
│   │   └── types.ts                     # TypeScript type definitions
│   ├── test/                            # Test files
│   ├── package.json                     # Node dependencies
│   ├── tsconfig.json                    # TypeScript configuration
│   ├── wrangler.jsonc                   # Cloudflare Workers config
│   └── README.md                        # Frontend documentation
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

### Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend development)
- Virtual environment (recommended)

### Setup

1. **Clone and navigate to the project:**
```bash
cd HackCC---IEEE---SWC
```

2. **Set up Python virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Copy data files to API directory:**
```bash
cp colleges.json apis/
cp 2026_internships.json apis/
cp stem_internships.json apis/
cp mentorship_opportunities.json apis/
```

### Running the Application

#### Start the Backend API Server

```bash
cd apis
python3 api.py
```

Server runs on **`http://localhost:5000`**

API documentation available at: **`http://localhost:5000/`**

#### Start the Frontend (Development)

**Option 1: Simple HTTP Server**
```bash
cd llm-chat-app-template/public
python3 -m http.server 8000
```

Open **`http://localhost:8000`** in your browser

**Option 2: Cloudflare Workers (Local Development)**
```bash
cd llm-chat-app-template
npm install
npm run dev
```

#### Full Stack Setup

1. **Terminal 1 - Backend API:**
   ```bash
   cd apis && python3 api.py
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   cd llm-chat-app-template/public
   python3 -m http.server 8000
   ```

3. **Open Browser:**
   Navigate to `http://localhost:8000`

### Using the Application

1. **Landing Page**: Click "Get Started →" to begin
2. **Step 1 - Community College**: Search and select your current CC
3. **Step 2 - Target Universities**: Select one or more target schools
4. **Step 3 - Major**: Choose your intended major
5. **Step 4 - Summary**: Review your selections
6. **Chat Assistant**: Click "Chat with Transfer Assistant →" to start getting personalized help

The AI assistant will use your profile to provide tailored advice on:
- Transfer requirements and articulation agreements
- Relevant internship opportunities in your field
- Mentorship programs for your major
- Free resources available to CC transfer students

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
  - Used by Quick Action: "What are the transfer requirements?"
  - Returns agreement details, years supported, and assist.org URL
- `GET /api/transfer/schools` - Search/list all colleges
- `GET /health` - Health check

### Internships

- `GET /api/internships` - Get all internships with filters
- `GET /api/internships/<id>` - Get specific internship
- `GET /api/internships/stats` - Internship statistics
- `GET /api/internships/companies` - List all companies
- `GET /api/internships/locations` - List all locations
- `GET /api/internships/categories` - List all categories
- `GET /api/stem-internships` - STEM-specific internships (filtered by major)
  - Used by Quick Action: "Find internships in my field"
  - Returns internships matching user's major
- `POST /api/internships/refresh` - Refresh internship data

### Mentorships

- `GET /api/mentorships` - Get all mentorship programs with filters
- `GET /api/mentorships/<id>` - Get specific mentorship program
- `GET /api/mentorships/stats` - Mentorship statistics
- `GET /api/mentorships/organizations` - List all organizations
- `GET /api/mentorships/majors` - List all supported majors
- `GET /api/mentorships/free` - Free mentorship programs
  - Used by Quick Action: "Free resources and programs"
  - Returns no-cost opportunities for students
- `GET /api/mentorships/community-college` - Community college friendly programs
  - Used by Quick Action: "Mentorship programs available?"
  - Returns CC-specific mentorship opportunities
- `POST /api/mentorships/refresh` - Refresh mentorship data

### AI Chat

- `POST /api/chat` - AI-powered chat endpoint
  - Accepts: `{ messages: [...], userProfile: {...} }`
  - Returns: Streaming response with AI-generated answers
  - Context-aware using user's CC, target schools, and major

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

## Frontend Architecture

### Technologies

- **Vanilla JavaScript**: No framework dependencies for maximum performance
- **Swiper.js**: Card-based UI with smooth transitions
- **Marked.js**: Markdown rendering for AI chat responses
- **CSS3**: Modern gradients, animations, and responsive design
- **Cloudflare Workers**: Serverless deployment option for AI chat API

### Key Components

#### 1. Landing Page
- Hero section with "Get Started" CTA
- Smooth slide transition to main app

#### 2. Card Stack Interface
- **Card 1**: Community College selection with live search
- **Card 2**: Target Universities multi-select with tag display
- **Card 3**: Major selection with live search
- **Card 4**: Summary and confirmation
- Progress bar with 4 segments tracking user journey
- Swiper.js cards effect for layered appearance

#### 3. Search System
- **Debounced Input**: 200ms delay for smooth performance
- **Relevance Sorting**: Results starting with search term appear first
- **Live Filtering**: Real-time results as you type
- **Result Limiting**: Max 8 results displayed
- **Selected State**: Visual feedback for chosen items

#### 4. AI Chat Interface
- **Full-Screen Modal**: Centers on screen with backdrop
- **Streaming Responses**: Real-time AI response display
- **Message History**: Persistent conversation state
- **Quick Actions**: 4 one-click shortcuts for common queries
- **Profile Integration**: Automatically includes user's transfer profile
- **Back Navigation**: Return to form with preserved state

#### 5. User Experience Features
- **Custom Cursor**: Dot and outline with smooth following animation
- **Click Ripples**: Visual feedback on all interactions
- **Hover Effects**: Interactive elements respond to cursor
- **Mobile Optimized**: Touch-friendly with standard cursor on mobile
- **Smooth Transitions**: 350ms cubic-bezier animations
- **Accessibility**: Keyboard navigation and semantic HTML

### Data Flow

```
User Profile Form → localStorage → Chat Assistant → API Calls
                                         ↓
                            Context-Aware Responses
```

1. User completes 4-step form
2. Profile saved to `window.userProfile` and `localStorage`
3. Chat assistant accesses profile for personalized queries
4. Quick actions trigger API calls with user context
5. AI responses stream back in real-time

### File Structure

```
llm-chat-app-template/
├── public/
│   ├── index.html (2,263 lines)
│   │   ├── HTML structure
│   │   ├── Embedded CSS (~1,200 lines)
│   │   └── Embedded JavaScript (~1,000 lines)
│   └── colleges.json
│       └── Combined list of CA community colleges and universities
```

## Backend Architecture

- **Unified REST API**: Single Flask entry point for all services (transfers, internships, mentorships)
- **assist.org Integration**: Uses public REST API for real-time transfer agreement data
- **Local JSON Storage**: Internship and mentorship data cached locally for fast queries
- **Flask Framework**: Lightweight, scalable HTTP server with CORS enabled
- **Cloudflare Workers AI**: Serverless AI chat API with streaming responses

## Development

### Linting

```bash
cd apis
python3 -m flake8 api.py --max-line-length=100
```

### Frontend Development

**Local Testing:**
```bash
cd llm-chat-app-template/public
python3 -m http.server 8000
```

**Cloudflare Workers (with AI chat):**
```bash
cd llm-chat-app-template
npm install
npm run dev
```

See `llm-chat-app-template/README.md` for deployment instructions.

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        BetterTransfer                           │
│                    (Frontend - index.html)                      │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Landing    │→│  Card Stack  │→│  AI Chat     │         │
│  │     Page     │  │  (4 Steps)   │  │  Assistant   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                           ↓                   ↓                 │
│                    User Profile         API Requests            │
│                   (localStorage)              ↓                 │
└─────────────────────────────────────────────────────────────────┘
                                                ↓
                         ┌──────────────────────────────────────┐
                         │    Cloudflare Workers AI             │
                         │      /api/chat (Streaming)           │
                         └──────────────────────────────────────┘
                                                ↓
┌─────────────────────────────────────────────────────────────────┐
│               Flask REST API (localhost:5000)                   │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │  Transfer   │  │ Internships │  │ Mentorships │           │
│  │     API     │  │     API     │  │     API     │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│        ↓                 ↓                 ↓                    │
│  assist.org API    JSON Files       JSON Files                │
└─────────────────────────────────────────────────────────────────┘
```

### User Journey

1. **Welcome** → User lands on BetterTransfer homepage
2. **Profile Setup** → 4-step guided form:
   - Current community college
   - Target universities (1+)
   - Intended major
   - Confirmation summary
3. **AI Chat** → Context-aware assistant with Quick Actions:
   - Transfer requirements (fetches from assist.org)
   - Internship opportunities (filtered by major)
   - Mentorship programs (CC-focused)
   - Free resources
4. **Natural Queries** → User can ask follow-up questions in plain English
5. **Streaming Responses** → AI provides detailed, personalized guidance

## Performance

- **Frontend Load**: <1s (single HTML file, minimal dependencies)
- **Card Transitions**: 600ms smooth animations
- **Search Debouncing**: 200ms delay for optimal UX
- **Transfer Agreement Lookup**: ~1-2 seconds (live assist.org API)
- **School/Internship/Mentorship Search**: <100ms (local JSON)
- **AI Chat Response**: Streaming (starts in <1s, completes based on query)

## What Works ✅

### Core Features
- ✅ **4-Step Profile Builder** with live search and multi-select
- ✅ **Transfer Agreement Lookup** between CA community colleges and universities
- ✅ **AI Chat Assistant** with streaming responses and markdown support
- ✅ **Quick Actions** for instant access to common queries
- ✅ **Internship Discovery** with major-based filtering (2026 opportunities)
- ✅ **Mentorship Programs** with CC-specific and free options
- ✅ **Profile Persistence** via localStorage
- ✅ **Back Navigation** between form and chat with state preservation

### UI/UX
- ✅ **Custom Cursor** with smooth animations and click ripples
- ✅ **Card Stack Interface** with Swiper.js
- ✅ **Responsive Design** optimized for mobile and desktop
- ✅ **Real-time Search** with debouncing and relevance sorting
- ✅ **Progress Tracking** with 4-segment progress bar
- ✅ **Smooth Transitions** throughout the application

### API Integration
- ✅ **assist.org Integration** for official CA transfer data
- ✅ **Context-Aware AI** using user profile in queries
- ✅ **Multiple Target Schools** support in single request
- ✅ **STEM Internship Database** with company and location data
- ✅ **Free Resource Identification** across all categories

## Use Cases

1. **Transfer Planning**: "I'm at Southwestern College and want to transfer to UC Berkeley for Computer Science. What courses do I need?"

2. **Internship Search**: "Find me summer 2026 CS internships in San Diego"

3. **Mentorship Discovery**: "Are there any free mentorship programs for community college students in STEM?"

4. **Multi-School Comparison**: "Compare transfer requirements for UCSD, UCLA, and UC Berkeley"

5. **Deadline Tracking**: "When are the transfer application deadlines for UC schools?"

6. **GPA Requirements**: "What GPA do I need to transfer to San Diego State?"

## Deployment

### Backend API (Production)

```bash
# Install production WSGI server
pip install gunicorn

# Run with Gunicorn
cd apis
gunicorn -w 4 -b 0.0.0.0:5000 api:app

# Or use with reverse proxy (Nginx)
# Configure upstream server to http://localhost:5000
```

### Frontend (Cloudflare Workers)

```bash
cd llm-chat-app-template
npm install
wrangler login
wrangler deploy
```

The frontend can be deployed to:
- **Cloudflare Workers**: Serverless with built-in AI chat
- **Static Hosting**: Any CDN (Vercel, Netlify, GitHub Pages)
- **Traditional Server**: Nginx, Apache, etc.

## Team

**Created for IEEE HackCC 2025 Hackathon**

- **Gabe** - Frontend & UX Design
- **Eli** - Backend API & assist.org Integration  
- **Angelo** - Data Collection & Testing
- **Tim** - AI Integration & Documentation

## Contributing

1. Follow PEP 8 style guidelines for Python code
2. Use ESLint for JavaScript (if adding external JS files)
3. Run linting before commits
4. Add tests for new API endpoints
5. Update API.md for endpoint changes
6. Test on both desktop and mobile devices

## Technologies Used

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Swiper.js 11.x (Card UI)
- Marked.js 11.x (Markdown rendering)
- Web APIs (localStorage, Fetch, Streams)

### Backend
- Python 3.8+
- Flask (REST API)
- Requests (HTTP client)
- assist.org REST API

### AI/ML
- Cloudflare Workers AI
- Llama models (text generation)
- Streaming responses

### Deployment
- Cloudflare Workers (Frontend + AI)
- Gunicorn (Backend production)
- Any cloud platform (AWS, GCP, Azure, etc.)

## License

IEEE HackCC 2025

---

**BetterTransfer** - Making college transfer journeys smoother, one student at a time. 🎓✨
