# Project Chimera → Flow parity map

Reference: [LarytheLord/Project-Chimera](https://github.com/LarytheLord/Project-Chimera) (`master` inspected 15 October 2026). Upstream's `agi_project/src/chimera/agent/memory.py` actually uses LangChain Chroma and Ollama embeddings (`qwen3-embedding:0.6b`), despite some README references to LanceDB.

| Upstream component | Flow implementation | Parity |
|---|---|---|
| `agent/memory.py` — WorkingMemory | `chimera_work_add/get/clear`, 20-entry chronological ring | Behavioural subset |
| `agent/memory.py` — VectorEpisodicMemory | `chimera_remember_vector`, cosine-ranked `chimera_recall_vector`; lexical `chimera_recall_at`; versioned binary snapshots | Partial: 8D externally supplied vectors, 64-entry bounded memory, not Chroma/Ollama |
| `agent/agent.py` — perceive/think/act loop | `chimera_step`, `chimera_step_json`, `chimera_live_step`, bounded `live_cli.flow` | Partial: model-driven session and action execution work for a fixed allowlist |
| `agent/tool_user.py` — ToolRegistry | `src/tools.flow`: register, unregister, enumerate, allow/deny, record host-completed outcomes | Partial: schema metadata only, no JSON validation or network/filesystem/process execution |
| `consciousness/narcissus_core.py` — SelfModelingEngine | `chimera_record_state`, `chimera_self_model`, confidence/focus/load/repetition metrics | Partial: 32 states, numeric trends only, no attention maps or arbitrary personal-pattern history |
| `consciousness/narcissus_core.py` — simulation | `chimera_what_if` | Different: descriptive historical heuristic, **not** predictive sandbox simulation |
| `consciousness/integration.py` | Monitoring toggles, reflection period, external outcome recording | Partial |
| `rlhf/oracle.py` | `chimera_best_candidate`, `chimera_reward_argmax` | Partial: numerical candidate ranking; not wired to trained text model |
| `cognitive_core/prometheus_core.py` — Gemini HTTP | `provider.flow` and `protocol.flow` with POSIX curl HTTP, secret header pipe, response parsing and request serialization | Functional integration tested against local HTTP fixture; real Gemini account not tested |
| `rlhf/reward_model.py` — DistilBERT/TRL training | `reward.flow` pairwise online eight-feature linear ranker | Alternative ranker: numeric preference training verified, but no DistilBERT/tokenizer or save/load |
| `consciousness/emotion.py` / `emotion/detector.py` | None | Missing external emotion classifiers |
| `consciousness/conscious_agent.py` | Core state/reflection plus `live_agent.flow` prompt orchestration and remote model generation | Partial: numeric self-monitoring and allowlisted action loop; not full Python semantics |
| Knight Medicare integration / CLI | Bounded environment-configured session entrypoint `live_cli.flow` | CLI partial; Knight Medicare bridge missing |

## Snapshot contract

The `FCH2` snapshot stores a 4-byte magic header, six little-endian unsigned 32-bit fields (working count, episode count, cognitive count, steps, reflection period, monitoring flag), then records in chronological order. Each string uses a 32-bit byte length plus exactly that many bytes (max 8192). Episodes additionally contain a vector-present flag and, when present, eight native double values. Each cognitive state stores its decision followed by confidence, processing load and focus doubles.

Live rings are replaced only after validation of magic, caps, lengths, vector values, cognitive bounds and the end-of-file marker. Input strings containing embedded NUL bytes are rejected. All strings stored in Flow rings are owned copies, and returned references are borrowed. Saving overwrites the target path directly and is not atomic in the event of a crash. A memory allocation failure during the final application of a validated snapshot can cause a partial in-memory restore. The snapshot is not encrypted or portable to different endianness/IEEE-754 architectures.

## Safety boundary

Models cannot directly run arbitrary shell commands, read files or browse the web through `chimera_step`. A host may register metadata for external tools and enable each tool explicitly; it must independently validate structured arguments, enforce effect permissions, sandbox process/filesystem/network operations and verify that the reported result is genuine. Metadata and permission status are **not** saved in the `FCH2` snapshot. Callers must not hand untrusted model output directly to `chimera_snapshot_save/load` file paths.

The upstream terms “consciousness” and “self-awareness” are labels for introspection instrumentation, not evidence of subjective experience. Similarly, `chimera_what_if` is a deterministic difference heuristic, not an empirically calibrated forecast.

## Work remaining for complete parity

The remaining gaps are Ollama/Chroma-style **model-generated semantic embeddings** (the current eight-dimensional vectors are caller-provided), user-scoped web/file/terminal tools with JSON Schema argument validation and actual sandboxed execution, DistilBERT/TRL-compatible preference training and model loading, local Hugging Face emotion inference, unrestricted configurable model selection, arbitrary-scope Narcissus attention/emotion history, application-level Knight Medicare integration and differential tests against upstream. The Flow-native linear preference ranker is **not** upstream model parity. The live Gemini transport is verified against a deterministic HTTP fixture, not Google production. No benchmark or general intelligence/consciousness result is claimed.
