# Port mapping and parity

Reference: [Project Chimera (upstream)](https://github.com/LarytheLord/Project-Chimera), `master` inspected 15 October 2026. The upstream README calls the vector database LanceDB; `agi_project/src/chimera/agent/memory.py` at that time actually imports `langchain_chroma` and `langchain_ollama`, and uses an Ollama embedding model (`qwen3-embedding:0.6b`). The current port does not claim either database.

| Upstream module | Flow implementation | Status |
|---|---|---|
| `agent/memory.py`: WorkingMemory | `chimera_work_add/get/clear` | Bounded 20-record ring; in-memory |
| `agent/memory.py`: VectorEpisodicMemory | `chimera_remember/recall_at` | Bounded 64 episodes; substring only, not semantic or persistent |
| `agent/agent.py`: action execution | `chimera_act` | Allowlisted echo, sum_numbers, exit only |
| `agent/agent.py`: loop | `chimera_step` | One deterministic step at a time; caller supplies observation and selected action |
| `consciousness/narcissus_core.py`: state and heuristics | `chimera_record_state`, confidence/focus/load/repetition functions | Numeric subset, 32-state history; excludes full self-simulation |
| `rlhf/oracle.py`: ranking | `chimera_best_candidate` | Selects maximum externally supplied score, no learned model |
| `cognitive_core/prometheus_core.py`: Gemini HTTP | none | Not ported |
| `rlhf/reward_model.py`: DistilBERT/TR L | none | Not ported |
| `agent/tool_user.py`: web search, filesystem, terminal | none | Not ported; omitted for safety and dependency separation |
| `consciousness/conscious_agent.py` integration | `chimera_step` records cognitive state | Partial |
| Knight Medicare therapy integration | none | Not ported |

## Runtime contract

The caller invokes `chimera_init()`, then drives `chimera_step(observation, action, payload, a, b, confidence, load, focus)` and finally invokes `chimera_shutdown()`. The caller owns model inference, parsing and proposal scoring. No side effects beyond in-memory bookkeeping and known actions occur.

`chimera_recall_at` and `chimera_work_get` yield borrowed strings, invalidated by later evictions or shutdown. All ring entries own copies of their input strings. Flow Tier-1 64-bit ABI is required due to eight-byte pointer allocation. Initialization and shutdown are idempotent.

The source author's terminology (consciousness, self-awareness) describes metacognitive instrumentation, not evidence of phenomenal consciousness.

## Subsequent parity work

To reach functional parity, implement a provider abstraction for model generation with explicit network permissions, bounded response and JSON validation; add semantic embeddings plus durable vector storage; support extensible, capability-checked tool schemas; implement reward inference/training behind a separately tested backend; and add structured persistence and end-to-end equivalence fixtures.

Those are missing features, not implemented stubs.
