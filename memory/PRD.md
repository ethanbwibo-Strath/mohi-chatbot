# Rafiki IT - MOHI Support Interface PRD

## Original Problem Statement
Build "Rafiki IT" - a branded support interface for Missions of Hope International (MOHI) featuring:
- Floating Action Button (FAB) chat widget
- MOHI branding (Deep Blue #1c3c54, Action Blue #4595d1, Green #8bc53f)
- Light/Dark mode with LocalStorage persistence
- IT Quick Links for common FAQs
- Typing indicator animation
- API integration to POST /api/chat

## Architecture
- **Frontend**: React 18 with Tailwind CSS
- **Backend**: FastAPI (Python) with built-in response system
- **User's Existing Backend**: LangChain + OpenAI + ChromaDB (at /app/app/)

## User Personas
1. **MOHI Staff Members** - Need IT support for portal access, leave applications, technical issues
2. **IT Administrators** - Manage the chatbot responses and knowledge base

## Core Requirements (Static)
- [x] Floating widget with MOHI Green FAB button
- [x] Chat container (400px wide) with slide-up animation
- [x] MOHI branded header with logo and "Rafiki IT" title
- [x] Light/Dark theme toggle with LocalStorage persistence
- [x] Quick action buttons for IT Office, Portal Lockout, Leave Application
- [x] Typing indicator with green pulsing animation
- [x] User bubbles in MOHI Green, assistant bubbles in Deep Blue
- [x] Integration with /api/chat endpoint

## What's Been Implemented (Feb 25, 2026)
1. **React Frontend** (`/app/frontend/src/App.js`)
   - Complete floating chat widget with FAB
   - Theme toggle with persistence
   - Quick action buttons
   - Typing indicator
   - Responsive message bubbles

2. **FastAPI Backend** (`/app/backend/server.py`)
   - Health check endpoints
   - /api/chat with built-in intelligent responses
   - Fallback system when AI chatbot unavailable

3. **Styling** (`/app/frontend/src/index.css`, `tailwind.config.js`)
   - Custom MOHI color palette
   - Animations (pulse, slide, fade)
   - Dark mode support

## Prioritized Backlog

### P0 (Critical)
- [ ] Connect to user's existing LangChain chatbot (requires ChromaDB setup and data ingestion)
- [ ] Fix external preview URL accessibility

### P1 (High Priority)
- [ ] Add conversation export functionality
- [ ] Implement typing animation during API response streaming

### P2 (Medium Priority)
- [ ] Add file attachment support
- [ ] Implement chat history persistence across sessions
- [ ] Add more quick action buttons based on FAQ analysis

## Next Tasks
1. User to set up ChromaDB with their knowledge base documents
2. Configure data ingestion pipeline (`/app/app/services/knowledge.py`)
3. Test full AI-powered responses with LangChain

## Technical Notes
- Backend uses built-in responses until ChromaDB is configured
- MOHI logo loaded from: https://mohiit.org/static/images/inventorylogo.png
- Font: Caveat (script) for "Rafiki IT", Inter for body text
