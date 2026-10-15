# Flow Chimera

A Flow 2.x native port of the orchestration and metacognitive components of [Project Chimera](https://github.com/LarytheLord/Project-Chimera).

**Status: tested partial functional parity, not full parity.** The Flow 2.x implementation now includes a real Gemini-compatible HTTPS transport using the installed curl executable, schema-shaped JSON action decoding, a bounded model-driven agent loop and a separately trainable pairwise linear preference scorer. Live API connectivity has been verified against a local Gemini-compatible HTTP server in CI, **not with a real Google API key**. Full Ollama/Chroma semantic embedding support, DistilBERT reward inference, Hugging Face emotion classification, unrestricted tools and Knight Medicare integration remain unimplemented. No machine-consciousness claim is made.

## Implemented in Flow

The deterministic core implements bounded working memory (20 records), episodic memory (64 experiences), optional eight-dimensional externally supplied embeddings with cosine-ranked retrieval, deterministic tool actions (echo, integer sum, exit), external-outcome recording, cognitive state history (32 states), configurable reflection, self-model metrics, candidate score ranking and a historical what-if heuristic. State can be saved and loaded as a versioned binary snapshot, including memory, vectors, cognitive states, step counters and reflection settings.

`src/tools.flow` includes a 16-entry registry of host-managed tool definitions with explicit enable/disable. Each registered tool has a capability category and schema string. **The registry neither executes commands nor validates JSON schema**: the embedding provider, LLM, reward model, network and filesystem tools must be implemented and isolated by an external host. External outcomes are recorded only after an enabled tool is reported as completed.

## Prometheus / live agent

`src/provider.flow` implements a real HTTPS POST transport with a child `curl` process. The API key is passed through a private inherited header pipe, rather than a shell command or command-line argument. `src/protocol.flow` validates JSON and decodes the first Gemini candidate; `src/live_agent.flow` builds an observation/context/reflection prompt and passes the selected action into the existing allowlisted dispatcher. `src/live_cli.flow` offers an eight-turn maximum session runner with optional snapshot restore/save.

```bash
export CHIMERA_LLM_API_KEY="your_key"
export CHIMERA_TASK="Add five and ten, then exit"
# CHIMERA_LLM_API_URL is optional; defaults to Gemini generateContent
CHIMERA_MAX_STEPS=4 CHIMERA_SNAPSHOT="./chimera-state.bin" flow run src/live_cli.flow
```

Only `echo`, `sum_numbers` and `exit` are executable through this host; other tool names are explicitly denied. The default remote model name may need updating as the Gemini service evolves. Runtime snapshots are not encrypted; keep them private. `curl` and POSIX `fork/exec` must be available. This does **not** execute arbitrary model-proposed shell commands.

`src/reward.flow` provides a learnable eight-feature pairwise logistic preference ranker. The tests demonstrate that it learns to prefer one numerical feature vector to another. It is not equivalent to upstream DistilBERT training, is not connected to the live candidate loop, and must not be described as a semantic reward model.

## Run tests

Requires [Flow 2.x](https://github.com/flooooooooooow/flow), Linux x86-64 or macOS arm64.

```bash
flow run src/chimera_test.flow
flow run src/parity_test.flow
flow run src/tool_test.flow
flow run src/protocol_test.flow
flow run src/provider_test.flow
flow run src/reward_test.flow
flow run src/demo.flow
```

CI compiles and runs the deterministic, vector-memory, reflection, tool, JSON, provider and reward tests, plus a local HTTP mock integration for the live agent and CLI.

## Library contracts

Import `src/chimera.flow` into a Flow program, call `chimera_init()` before using it and `chimera_shutdown()` when finished. `chimera_step()` executes only the three allowlisted deterministic actions. To use an external hosted tool, the application must validate its action independently and invoke `chimera_record_external_step()` (or the gated `chimera_tool_complete()` in `src/tools.flow`) after execution.

`chimera_remember_vector(observation, action, outcome, &embedding[0], 8)` stores an eight-component numeric vector, and `chimera_recall_vector(&query[0], 8, rank)` returns a scored match in descending cosine order. A missing match has similarity `-2`. No model-generated embeddings are bundled.

`chimera_snapshot_save(path)` and `chimera_snapshot_load(path)` persist/recover the state in an `FCH2` binary format (little-endian counts and Tier-1 native 64-bit floating-point values). Paths are **application-controlled**, not accepted from model responses. Text fields are capped at 8192 bytes each. Malformed or truncated snapshots are rejected before live state changes. Saving is not crash-atomic and allocation failures during restoration can interrupt commit; see [PORTING.md](PORTING.md) for the format and constraints. Data is not encrypted.

Strings returned by `chimera_work_get`, `chimera_episode_get`, `chimera_recall_at`, `chimera_recall_vector`, `chimera_state_get` and registry lookups are borrowed and invalidated by replacement, eviction or shutdown.

## Parity map

See [PORTING.md](PORTING.md) for upstream module coverage, intentional deviations and the outstanding feature-parity requirements.

Attribution: [LarytheLord / Project-Chimera](https://github.com/LarytheLord/Project-Chimera). This is an independent Flow implementation of the behavioural interfaces, not a direct translation of the Python source.

## Native Ollama semantic-memory integration

The [Ollama semantic-memory adapter](docs/ollama-and-semantic-memory.md) provides real local /api/embed POST requests, validated 1–4096D vectors, a bounded full-dimensional cosine index, transactional CSM1 snapshot loading, and a runnable example in `src/ollama_demo.flow`. It requires a running Ollama server and installed embedding model; CI exercises the transport with a deterministic local HTTP fixture. This independent memory store is **not yet wired into the Gemini agent prompt loop** and is not a replacement for Chroma/ANN search.

## Local language-model generation

An independent [Ollama /api/generate backend](docs/ollama-generation.md) now provides an **opt-in** local alternative to Gemini, including bounded JSON model responses, safe action dispatch, and a runnable `src/ollama_cli.flow`. Inference requires a separately installed and running local model. Tests exercise its HTTP interface with a local fixture, not the actual weights. Arbitrary tool execution, full RLHF integration and embedding retrieval inside agent prompts are still missing.
