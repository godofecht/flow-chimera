# Parity evidence — 15 October 2026

This document is a point-in-time audit, **not** a declaration of upstream equivalence.

## Pinned inputs

Upstream `LarytheLord/Project-Chimera` `master`: `576f6ee291250c59122d377cfb1ed41c07ea62b1`.

Flow compiler `flooooooooooow/flow` `main`: `69c8ec453941a1738ac06343bdcb440025610c67`.

Flow Chimera `main`: `456e34f5e524d43cc619b53e2ba3a92a88f70694`.

Existing Flow Chimera CI: [run 38782787230](https://github.com/godofecht/flow-chimera/actions/runs/38782787230), success. Its steps compile/run the deterministic Flow tests and exercise a local Gemini-compatible mock. This run **does not** establish live Google Gemini connectivity, Ollama embedding quality, production safety, or upstream test equivalence.

## Evidence-based capability matrix

| Capability | Upstream reference | Flow reference | Evidence | Unresolved |
| --- | --- | --- | --- | --- |
| Working memory | `agent/memory.py` | `src/chimera.flow` | Ring operations and `chimera_test.flow` | Generalized record types and configurable limits |
| Episodic recall | Chroma + `OllamaEmbeddings(model="qwen3-embedding:0.6b")` | Eight-dimensional caller-supplied vectors + FCH2 snapshots | `parity_test.flow` tests deterministic vector ranking and restore | Ollama HTTP embeddings, model dimension discovery, Chroma interoperability, persistent semantic recall with actual generated vectors |
| Model inference | Gemini cognitive core and separate OpenRouter/Ollama graph | `provider.flow`, `protocol.flow`, `live_agent.flow` | `provider_test.flow` and `live_test.flow` with local mock | Real Gemini credentials, local Ollama generation, provider failover and response variants |
| Tool execution | Python ToolRegistry with web, file and terminal tools | `tools.flow` registry + three internal allowlisted actions | `tool_test.flow`, `protocol_test.flow` | Schema validation, approved host execution, per-call capability enforcement, path/network/process isolation |
| Narcissus | CognitiveState with attention weights, emotional state, thought process and decision path | `introspection.flow` numeric summaries | `parity_test.flow` | Rich state recording, reflection-history equivalence and structured simulation |
| Preference learning | DistilBERT tokenizer/sequence classifier + TRL RewardTrainer | `reward.flow` eight-feature online pairwise linear ranker | `reward_test.flow` | Text feature extraction, model save/load, upstream architecture/training and reward integration |
| CLI | Python `cli.py` plus separate interactive graph script | `live_cli.flow` bounded session | Local mock CI invocation | Cross-provider flags, interactive conversation parity, session persistence choices |

## Upstream test audit

The upstream tree contains `test_agent_logic.py`, `test_agent_graph.py`, `test_consciousness.py`, and `test_consciousness_simple.py` under `agi_project/tests`. No differential test harness executes these Python tests alongside Flow tests in Flow Chimera CI.

`test_agent_logic.py` has a vector-memory test with LanceDB-oriented mocks; upstream `memory.py` currently imports Chroma and Ollama embeddings instead. The test therefore cannot be treated as a validated Chroma contract without fixing the mismatch.

`test_agent_graph.py` contains top-level interactive input and network/model initialization; it is not an isolated hermetic unit test. It includes an unconditional `process -> tools` edge in addition to a conditional edge, which warrants upstream verification before using it as an oracle.

`test_consciousness.py` asserts cognitive-state counts, analysis keys and self-modification proposal/risk fields using a fake memory backend. `test_consciousness_simple.py` asserts four top-level introspection keys. Flow has partial numeric introspection but does not produce these full shapes.

## Pending implementation

A separate CRW2 binary checkpoint patch for the Flow-native eight-feature reward ranker was prepared, with a round-trip/corruption test and CI invocation. It has **not** been added to this repository or compiled. It is not evidence of a passing test or of upstream DistilBERT parity. Checkpoint files should use trusted paths, bounded reads, checksum verification and explicit non-atomic-write documentation.

## Release gate

Do not declare full parity until a pinned compiler build and hermetic Flow tests pass, Gemini and local inference integration tests pass against deterministic fixtures, Ollama embedding/recall persists across process restarts, capability-denial tests demonstrate default-deny external effects, preference model training/save/load is verified, and every applicable upstream behavioral test has a corresponding documented differential result. Non-hermetic or broken upstream tests must be repaired or explicitly excluded with evidence, not silently counted as passed.
