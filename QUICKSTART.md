# Quick Start Guide

Get Calendar Consolidator MCP running in under 5 minutes.

## Step 1: Install Prerequisites

Ensure you have:
- **Python 3.10+**: `python3 --version`
- **Node.js 18+**: `node --version`

## Step 2: Setup

Run the automated setup script:

```bash
chmod +x setup.sh
./setup.sh
```

Or manually:

```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Initialize database
python python/init_db.py
```

## Step 3: Start the Application

```bash
npm start
```

Open your browser to: **http://localhost:3000**

## Step 4: Configure Your First Calendar

1. Click **"Sources"** tab
2. Click **"+ Add Source"**
3. Choose **Microsoft Graph**
4. Complete OAuth flow
5. Select calendar to sync

## Step 5: Set Target Calendar

1. Click **"Target"** tab
2. Click **"Set Target"**
3. Choose destination calendar

## Step 6: Sync!

1. Go to **"Sync"** tab
2. Click **"Preview Sync"** to see changes
3. Click **"Sync Now"** to execute

## Troubleshooting

### Database not found
```bash
python python/init_db.py
```

### Python module errors
```bash
pip install -r requirements.txt
```

### Node module errors
```bash
npm install
```

### Port already in use
```bash
PORT=3001 npm start
```

## Next Steps

- Read full documentation: `0-docs/README.md`
- Configure OAuth: `0-docs/03-implementation/02-step2-graph-connector.md`
- Set up CalDAV: `0-docs/03-implementation/06-step6-caldav.md`
- Enable continuous sync in Settings tab

## Support

Check comprehensive docs in `0-docs/` folder for:
- Architecture details
- API documentation
- Database schema
- Troubleshooting guides
