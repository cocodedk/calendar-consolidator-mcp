# CLAUDE.md — Calendar Consolidator MCP

## Project Overview

Calendar Consolidator MCP is a lightweight system that consolidates multiple calendars (Microsoft 365, iCloud/CalDAV) into a single unified calendar with one-way mirroring and incremental syncing. It exposes an MCP server for AI/agent control alongside a simple web UI.

- **Language / Runtime**: Node.js 20 + Python 3.12
- **Framework**: Express (Node.js), standard library (Python)
- **Architecture**: Layered — Node.js MCP/HTTP layer + Python sync engine + SQLite storage
- **Package / Namespace**: `calendar-consolidator-mcp`

---

## Required Skills — ALWAYS Invoke These

These skills **must** be invoked when the relevant situation arises. Never skip them.

| Situation | Skill |
|-----------|-------|
| Before any new feature or screen | `superpowers:brainstorming` |
| Planning multi-step changes | `superpowers:writing-plans` |
| Writing or fixing core logic | `superpowers:test-driven-development` |
| First sign of a bug or failure | `superpowers:systematic-debugging` |
| Before completing a feature branch | `superpowers:requesting-code-review` |
| Before claiming any task done | `superpowers:verification-before-completion` |
| Working on UI / frontend | `frontend-design:frontend-design` |
| After implementing — reviewing quality | `simplify` |

---

## Architecture

```
calendar-consolidator-mcp/
├── node/                # Node.js MCP server + Express HTTP
│   ├── server/          # Entry point, routes, MCP tools
│   └── admin_api/       # REST admin endpoints
├── python/              # Python sync engine
│   ├── connectors/      # API connectors (Graph, CalDAV)
│   ├── model/           # Event model and diff logic
│   ├── state/           # Database and config management
│   └── sync/            # Sync execution engine
├── tests/               # Python unit tests
├── tests-e2e/           # Playwright E2E tests
└── .github/workflows/   # CI, release, Pages automation
```

### Layer Rules
- Node.js layer calls Python via subprocess bridge
- Python layer must never depend on Node.js
- SQLite is the single source of truth for state

---

## Coding Conventions

- All models are **immutable** — use copies for mutations
- Functions are **pure** where possible — no hidden side effects
- No hardcoded strings — use constants or config
- 200-line maximum per file — extract when approaching limit

---

## Engineering Principles

### File Size
- **200-line maximum per file** — extract a class, function, or module when approaching the limit

### DRY / SOLID / KISS / YAGNI
- Extract shared logic into named utilities; never copy-paste
- Single Responsibility: one class/function does one thing
- Don't add features not yet needed
- Delete dead code immediately

### TDD
- Write the failing test first, make it pass, then refactor
- Test names describe behaviour: `"should reject duplicate event"`
- One assertion per test — keep tests focused and readable

### Commit hygiene
- Follow Conventional Commits: `feat: ...` / `fix: ...` / `chore: ...`
- The `commit-msg` hook enforces this automatically

---

## Build Commands

```bash
npm test          # Run Node.js tests
pytest            # Run Python tests
npm run dev       # Start development server
npm start         # Start production server
```

---

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | This file — project conventions and session startup |
| `version.txt` | Semantic version (MAJOR.MINOR.PATCH) |
| `.github/workflows/` | CI, release, and Pages automation |
| `.githooks/` | Pre-commit and commit-msg hooks |
| `scripts/install-hooks.sh` | One-time hook installer |

---

## Starting a New Session

1. Read this file
2. Run `npm test && pytest` to confirm everything passes
3. Invoke `superpowers:brainstorming` before touching any feature
4. Follow the Required Skills table — every skill is mandatory, not optional
