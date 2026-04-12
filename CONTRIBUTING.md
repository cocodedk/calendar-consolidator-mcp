# Contributing to Calendar Consolidator MCP

## Local Setup
1. Install Node.js 20+ and Python 3.12+.
2. Clone the repository: `git clone https://github.com/cocodedk/calendar-consolidator-mcp`
3. Install Node dependencies: `npm install`
4. Install Python dependencies: `pip install -r requirements.txt`

## Install Git Hooks
```sh
./scripts/install-hooks.sh
```

## Local Git Setup
Run these once after cloning:
```bash
git config pull.rebase true
git config core.autocrlf input
git config push.autoSetupRemote true
git config init.defaultBranch main
```

## Build and Test Commands
```bash
npm test          # Run Node.js tests
pytest            # Run Python tests
npm run dev       # Start development server
```

## Coding Style
- Follow existing Node.js and Python conventions.
- Keep files small and focused (200-line maximum).
- Use Conventional Commits for all commit messages.

## Branch Naming
| Prefix | Use for |
|--------|---------|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `chore/` | Maintenance |
| `docs/` | Documentation |
| `ci/` | CI changes |

## PR Checklist
- [ ] Tests pass (`npm test` and `pytest`).
- [ ] Manual test completed for changed functionality.
- [ ] Updated docs if behaviour changed.
- [ ] Commit messages follow Conventional Commits.
