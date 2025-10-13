# Phase 0: MVP Development Environment

## Goal
Prove core functionality works without packaging complexity

## Prerequisites

### Required Software
- Python 3.10+ installed
- Node.js 18+ installed
- Git for version control

### Optional
- VS Code or preferred editor
- Python virtual environment tool
- Git GUI client

## Setup Instructions

### 1. Clone Repository
```bash
git clone <repo-url>
cd calendar-consolidator
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
# Or with virtual environment:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install Node Dependencies
```bash
npm install
```

### 4. Initialize Database
```bash
python python/init_db.py
# Creates ~/.calendar-consolidator/config.db
```

### 5. Run Application
```bash
npm start
# Opens browser to http://localhost:3000
```

## Development Workflow

### Rapid Iteration
- Edit Python code → restart worker
- Edit Node code → restart server (or use nodemon)
- Edit UI → refresh browser
- No build/compile steps

### Testing
- Test with real Microsoft/CalDAV APIs
- Debug easily in local environment
- Use breakpoints and logging

### No Complexity
- No Docker files
- No build configurations
- No deployment scripts

## Target Users
- Developer (you)
- Technical testers who can run Python + Node

## Time Estimate
- < 5 minutes from clone to running
- Assumes Python + Node already installed

## Success Criteria
- Application starts without errors
- Can access UI at localhost:3000
- Database created successfully
- Ready to build features
