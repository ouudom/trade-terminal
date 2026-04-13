# Claude Code Configuration - RuFlo V3

## Behavioral Rules (Always Enforced)

- Do what has been asked; nothing more, nothing less
- NEVER create files unless they're absolutely necessary for achieving your goal
- ALWAYS prefer editing an existing file to creating a new one
- NEVER proactively create documentation files (*.md) or README files unless explicitly requested
- NEVER save working files, text/mds, or tests to the root folder
- Never continuously check status after spawning a swarm — wait for results
- ALWAYS read a file before editing it
- NEVER commit secrets, credentials, or .env files

## File Organization

- NEVER save to root folder — use the directories below
- Use `backend/app/` for Python/FastAPI source code
- Use `backend/app/api/v1/` for API route handlers (one file per domain)
- Use `backend/app/core/` for config, database, dependencies, exceptions, logging
- Use `backend/app/models/` for SQLModel ORM models
- Use `backend/app/schemas/` for Pydantic request/response schemas
- Use `backend/app/services/` for business logic services
- Use `backend/app/repositories/` for database query layer
- Use `frontend/app/` for Next.js pages and layouts
- Use `frontend/components/` for React components
- Use `backend/scripts/` for backend utility scripts (seeding, staging data)
- Use `backend/alembic/versions/` for database migrations
- Use `/docs` for documentation and markdown files

## Project Architecture

- Follow Domain-Driven Design with bounded contexts
- Keep files under 500 lines
- Use typed interfaces for all public APIs
- Prefer TDD London School (mock-first) for new code
- Use event sourcing for state changes
- Ensure input validation at system boundaries

### Backend Architecture (FastAPI + SQLModel + PostgreSQL)

Layered architecture: `api/v1/` → `services/` → `repositories/` → `models/`

**API domains** (all under `/api/v1/`):
| Route prefix | File | Description |
|---|---|---|
| `/instruments` | `instruments.py` | Trading instrument list |
| `/bias` | `bias.py` | Fundamental bias snapshots |
| `/forexfactory` | `forexfactory.py` | ForexFactory calendar events |
| `/news` | `news.py` | News feed |
| `/forex-charts` | `forex_charts.py` | Chart data via yfinance |
| `/mt5` | `mt5.py` | MT5 bridge (positions, orders, account) |

**Core modules** (`app/core/`):
- `config.py` — pydantic-settings `Settings` class; reads from `backend/.env`
- `database.py` — SQLModel engine + `get_session()` dependency
- `dependencies.py` — FastAPI dependency injection factories for services
- `exceptions.py` — `NotFoundError`, `AppValidationError`, `MT5ConnectionError`, `MT5OrderError`, `ExternalServiceError`
- `logging.py` — `RequestLoggingMiddleware` + `configure_logging()`

**MT5 integration**: connects via `mt5linux` socket to a Wine-hosted MT5 terminal at `MT5_HOST:MT5_PORT`

**Database migrations** (3 existing):
- `0001` — fundamental_bias schema
- `0002` — forexfactory_events
- `0003` — new bias schema (current)

### Project Config

- **Topology**: hierarchical-mesh
- **Max Agents**: 15 (configured ceiling; use 6-8 for active coding swarms)
- **Memory**: hybrid
- **HNSW**: Enabled
- **Neural**: Enabled

## Build & Test

### Frontend (Next.js — run from `frontend/`)
```bash
cd frontend && npm run build   # Build
cd frontend && npm run lint    # Lint
cd frontend && npm run dev     # Dev server
```

### Backend (FastAPI/Python — run from `backend/`)
```bash
cd backend && uvicorn app.main:app --reload   # Dev server (uses .venv)
cd backend && python -m pytest                # Tests (if added)
cd backend && alembic upgrade head            # Apply migrations
```

**Key dependencies**: FastAPI, SQLModel, PostgreSQL (psycopg2), Alembic, Pydantic-settings, httpx, BeautifulSoup4, mt5linux, yfinance

**Environment variables required** (in `backend/.env`):
- `DATABASE_URL` — PostgreSQL connection string
- `NEWS_API_KEY` — news API key
- `MT5_HOST`, `MT5_PORT` — MT5 bridge socket server (default: 127.0.0.1:18812)
- `MT5_LOGIN`, `MT5_PASSWORD`, `MT5_SERVER` — MT5 demo account credentials (optional)

- ALWAYS run tests after making code changes
- ALWAYS verify build succeeds before committing

## Security Rules

- NEVER hardcode API keys, secrets, or credentials in source files
- NEVER commit .env files or any file containing secrets
- Always validate user input at system boundaries
- Always sanitize file paths to prevent directory traversal
- Run `npx @claude-flow/cli@latest security scan` after security-related changes

## Concurrency: 1 MESSAGE = ALL RELATED OPERATIONS

- All operations MUST be concurrent/parallel in a single message
- Use Claude Code's Agent tool for spawning agents, not just MCP
- ALWAYS spawn ALL agents in ONE message with full instructions via Agent tool
- ALWAYS batch ALL file reads/writes/edits in ONE message
- ALWAYS batch ALL Bash commands in ONE message

## Swarm Orchestration

- MUST initialize the swarm using CLI tools when starting complex tasks
- MUST spawn concurrent agents using Claude Code's Agent tool
- Never use CLI tools alone for execution — Agent tool agents do the actual work
- MUST call CLI tools AND Agent tool in ONE message for complex work

### 3-Tier Model Routing (ADR-026)

| Tier | Handler | Latency | Cost | Use Cases |
|------|---------|---------|------|-----------|
| **1** | Agent Booster (WASM) | <1ms | $0 | Simple transforms (var→const, add types) — Skip LLM |
| **2** | Haiku | ~500ms | $0.0002 | Simple tasks, low complexity (<30%) |
| **3** | Sonnet/Opus | 2-5s | $0.003-0.015 | Complex reasoning, architecture, security (>30%) |

- For Tier 1 simple transforms, use Edit tool directly — no LLM agent needed

## Swarm Configuration & Anti-Drift

- ALWAYS use hierarchical topology for coding swarms
- Keep maxAgents at 6-8 for tight coordination
- Use specialized strategy for clear role boundaries
- Use `raft` consensus for hive-mind (leader maintains authoritative state)
- Run frequent checkpoints via `post-task` hooks
- Keep shared memory namespace for all agents

```bash
npx @claude-flow/cli@latest swarm init --topology hierarchical --max-agents 8 --strategy specialized
```

## Swarm Execution Rules

- ALWAYS use `run_in_background: true` for all Agent tool calls
- ALWAYS put ALL Agent calls in ONE message for parallel execution
- After spawning, STOP — do NOT add more tool calls or check status
- Never poll agent status repeatedly — trust agents to return
- When agent results arrive, review ALL results before proceeding

## V3 CLI Commands

### Core Commands

| Command | Subcommands | Description |
|---------|-------------|-------------|
| `init` | 4 | Project initialization |
| `agent` | 8 | Agent lifecycle management |
| `swarm` | 6 | Multi-agent swarm coordination |
| `memory` | 11 | AgentDB memory with HNSW search |
| `task` | 6 | Task creation and lifecycle |
| `session` | 7 | Session state management |
| `hooks` | 17 | Self-learning hooks + 12 workers |
| `hive-mind` | 6 | Byzantine fault-tolerant consensus |

### Quick CLI Examples

```bash
npx @claude-flow/cli@latest init --wizard
npx @claude-flow/cli@latest agent spawn -t coder --name my-coder
npx @claude-flow/cli@latest swarm init --v3-mode
npx @claude-flow/cli@latest memory search --query "authentication patterns"
npx @claude-flow/cli@latest doctor --fix
```

## Available Agents (16 Roles + Custom)

### Core Development
`coder`, `reviewer`, `tester`, `planner`, `researcher`

### Specialized
`security-architect`, `security-auditor`, `memory-specialist`, `performance-engineer`

### Coordination
`hierarchical-coordinator`, `mesh-coordinator`, `adaptive-coordinator`

### GitHub & Repository
`pr-manager`, `code-review-swarm`, `issue-tracker`, `release-manager`

Any string can be used as a custom agent type — these are the typed roles with specialized behavior.

## Memory & Vector Search

### MCP Tools (use via ToolSearch to discover)

| Tool | Description |
|------|-------------|
| `memory_store` | Store value with ONNX 384-dim vector embedding |
| `memory_search` | Semantic vector search by query |
| `memory_retrieve` | Get entry by key |
| `memory_list` | List entries in namespace |
| `memory_delete` | Delete entry |
| `memory_import_claude` | Import Claude Code memories into AgentDB (allProjects=true for all) |
| `memory_search_unified` | Search across ALL namespaces (Claude + AgentDB + patterns) |
| `memory_bridge_status` | Show bridge health, vectors, SONA, intelligence |

### CLI Commands

```bash
# Store with vector embedding
npx @claude-flow/cli@latest memory store --key "pattern-auth" --value "JWT with refresh" --namespace patterns

# Semantic search
npx @claude-flow/cli@latest memory search --query "authentication patterns"

# Import all Claude Code memories into AgentDB
node .claude/helpers/auto-memory-hook.mjs import-all
```

### Claude Code ↔ AgentDB Bridge

Claude Code auto-memory files (`~/.claude/projects/*/memory/*.md`) are automatically imported into AgentDB with ONNX vector embeddings on session start. Use `memory_search_unified` to search across both stores.

## Key MCP Tools (314 available — use ToolSearch to discover)

### Most Used Tools

| Category | Tools | What They Do |
|----------|-------|-------------|
| **Memory** | `memory_store`, `memory_search`, `memory_search_unified` | Store/search with ONNX vector embeddings |
| **Claude Bridge** | `memory_import_claude`, `memory_bridge_status` | Import Claude memories into AgentDB |
| **Swarm** | `swarm_init`, `swarm_status`, `swarm_health` | Multi-agent coordination |
| **Agents** | `agent_spawn`, `agent_list`, `agent_status` | Agent lifecycle |
| **Hive-Mind** | `hive-mind_init`, `hive-mind_spawn`, `hive-mind_consensus` | Byzantine/Raft consensus |
| **Hooks** | `hooks_route`, `hooks_session-start`, `hooks_post-task` | Task routing + learning |
| **Workers** | `hooks_worker-list`, `hooks_worker-dispatch` | 12 background workers |
| **Security** | `aidefence_scan`, `aidefence_is_safe` | Prompt injection detection |
| **Intelligence** | `hooks_intelligence`, `neural_status` | Pattern learning + SONA |

### Swarm Capabilities

- **Topologies**: hierarchical (anti-drift), mesh, ring, star, adaptive
- **Consensus**: Raft (leader-based), Byzantine (PBFT), Gossip (eventual)
- **Hive-Mind**: Queen-led coordination with spawn, broadcast, consensus voting, shared memory
- **12 Background Workers**: audit, optimize, testgaps, map, deepdive, document, refactor, benchmark, ultralearn, consolidate, predict, preload

### Memory Capabilities

- **ONNX Embeddings**: all-MiniLM-L6-v2, 384 dimensions — real neural vectors
- **DiskANN**: SSD-friendly vector search (8,000x faster insert than HNSW, perfect recall at 1K)
- **sql.js**: Cross-platform SQLite (WASM, no native compilation)
- **Claude Code Bridge**: Auto-imports MEMORY.md files into AgentDB on session start
- **Unified Search**: `memory_search_unified` searches Claude memories + AgentDB + patterns
- **SONA Learning**: Trajectory recording → pattern extraction → file persistence

### How to Discover Tools

Use ToolSearch to find specific tools:
```
ToolSearch("memory search")     → memory_store, memory_search, memory_search_unified
ToolSearch("swarm")             → swarm_init, swarm_status, swarm_health, swarm_shutdown
ToolSearch("hive consensus")    → hive-mind_consensus, hive-mind_status
ToolSearch("+aidefence")        → aidefence_scan, aidefence_is_safe, aidefence_has_pii
```

## Quick Setup

```bash
claude mcp add claude-flow -- npx -y @claude-flow/cli@latest
npx @claude-flow/cli@latest daemon start
npx @claude-flow/cli@latest doctor --fix
```

## Claude Code vs MCP Tools

- **Claude Code Agent tool** handles execution: agents, file ops, code generation, git
- **MCP tools** (via ToolSearch) handle coordination: swarm, memory, hooks, routing, hive-mind
- **CLI commands** (via Bash) are the same tools with terminal output
- Use `ToolSearch("keyword")` to discover available MCP tools

## Trade Terminal: 3-Agent Swarm Setup

### Configured Agents

1. **backend-dev** — API endpoints, database, backend logic
   - Location: `.claude/agents/development/backend/`
   - Triggers: "api", "endpoint", "backend", "server"
   - Paths: `backend/`, `backend/app/`

2. **frontend-dev** — React components, UI, styling, Next.js
   - Location: `.claude/agents/development/frontend/`
   - Triggers: "ui", "component", "frontend", "react", "css"
   - Paths: `frontend/`, `frontend/components/`, `frontend/app/`

3. **code-reviewer** — Code standards, structure validation, quality checks
   - Location: `.claude/agents/analysis/code-reviewer/`
   - Triggers: "review", "check standards", "audit structure"
   - Paths: `frontend/`, `backend/`, `src/`

### Running the 3-Agent Swarm

#### Option 1: Auto-routing (recommended)
Just describe your task and mention the domain:
```
"Add a trading dashboard component to the frontend"
→ auto-routes to frontend-dev
→ code-reviewer validates structure

"Create a new API endpoint for price tracking"
→ auto-routes to backend-dev
→ code-reviewer validates standards
```

#### Option 2: Explicit agent spawn
```bash
# Start background daemon
npx @claude-flow/cli@latest daemon start

# Spawn specific agents
npx @claude-flow/cli@latest agent spawn -t backend-dev --name api-worker
npx @claude-flow/cli@latest agent spawn -t frontend-dev --name ui-worker
npx @claude-flow/cli@latest agent spawn -t code-reviewer --name quality-gate
```

#### Option 3: Via Claude Code Agent tool
```
/agents spawn backend-dev, frontend-dev, code-reviewer
→ All 3 agents work in parallel on your task
```

### Swarm Coordination Rules

- **Hierarchical topology**: One coordinator (usually code-reviewer) oversees others
- **Message routing**: Auto-routes tasks based on file patterns and keywords
- **Consensus**: code-reviewer validates all code changes before merge
- **Memory sharing**: All agents share context via AgentDB memory store
- **Fallback**: If a task touches multiple domains, spawns ALL 3 agents

### Memory & Learning

The swarm learns successful patterns:
```bash
# Search learned patterns
npx @claude-flow/cli@latest memory search --query "react component patterns"

# View agent performance metrics
npx @claude-flow/cli@latest agent list --with-stats
```

### Troubleshooting

```bash
# Check daemon status
npx @claude-flow/cli@latest daemon status

# View agent logs
npx @claude-flow/cli@latest agent logs --name backend-dev

# Full health check
npx @claude-flow/cli@latest doctor --fix
```

## Support

- Documentation: https://github.com/ruvnet/ruflo
- Issues: https://github.com/ruvnet/ruflo/issues
