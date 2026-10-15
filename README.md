# Flow Chimera

A Flow 2.x native port of the orchestration and metacognitive components of [Project Chimera](https://github.com/LarytheLord/Project-Chimera).

**Status: tested partial functional parity, not complete feature parity.** The original project integrates Gemini, Chroma with Ollama embeddings, Hugging Face reward/emotion models, and real web/filesystem/terminal tools. This repo presently implements an independently testable Flow runtime and host-integration boundary; **it does not provide those external backends**. No claim of machine consciousness is made.

## Implemented in Flow

The runtime implements bounded working memory (20 records), episodic memory (64 experiences), optional eight-dimensional externally supplied embeddings with cosine-ranked retrieval, deterministic tool actions (echo, integer sum, exit), external-outcome recording, cognitive state history (32 states), configurable reflection, self-model metrics, candidate score ranking and a historical what-if heuristic. State can be saved and loaded as a versioned binary snapshot, including memory, vectors, cognitive states, step counters and reflection settings.

`src/tools.flow` includes a 16-entry registry of host-managed tool definitions with explicit enable/disable. Each registered tool has a capability category and schema string. **The registry neither executes commands nor validates JSON schema**: the embedding provider, LLM, reward model, network and filesystem tools must be implemented and isolated by an external host. External outcomes are recorded only after an enabled tool is reported as completed.

## Run tests

Requires [Flow 2.x](https://github.com/flooooooooooow/flow), Linux x86-64 or macOS arm64.

```bash
flow run src/chimera_test.flow
flow run src/parity_test.flow
flow run src/tool_test.flow
flow run src/demo.flow
```

CI runs all four programs on every push and pull request.

## Library contracts

Import `src/chimera.flow` into a Flow program, call `chimera_init()` before using it and `chimera_shutdown()` when finished. `chimera_step()` executes only the three allowlisted deterministic actions. To use a model or hosted tool, the application must generate and validate an action outside this runtime and invoke `chimera_record_external_step()` (or the gated `chimera_tool_complete()` in `src/tools.flow`) after execution.

`chimera_remember_vector(observation, action, outcome, &embedding[0], 8)` stores an eight-component numeric vector, and `chimera_recall_vector(&query[0], 8, rank)` returns a scored match in descending cosine order. A missing match has similarity `-2`. No model-generated embeddings are bundled.

`chimera_snapshot_save(path)` and `chimera_snapshot_load(path)` persist/recover the state in an `FCH2` binary format (little-endian counts and Tier-1 native 64-bit floating-point values). Paths are **application-controlled**, not accepted from model responses. Text fields are capped at 8192 bytes each. Malformed or truncated snapshots are rejected before live state changes. Saving is not crash-atomic and allocation failures during restoration can interrupt commit; see [PORTING.md](PORTING.md) for the format and constraints. Data is not encrypted.

Strings returned by `chimera_work_get`, `chimera_episode_get`, `chimera_recall_at`, `chimera_recall_vector`, `chimera_state_get` and registry lookups are borrowed and invalidated by replacement, eviction or shutdown.

## Parity map

See [PORTING.md](PORTING.md) for upstream module coverage, intentional deviations and the outstanding feature-parity requirements.

Attribution: [LarytheLord / Project-Chimera](https://github.com/LarytheLord/Project-Chimera). This is an independent Flow implementation of the behavioural interfaces, not a direct translation of the Python source.
