# Flow Chimera

A Flow-native port of the deterministic cognition/orchestration layer of [Project Chimera](https://github.com/LarytheLord/Project-Chimera).

**Status: partial port, not feature parity.** Flow implements bounded working and episodic memories, action dispatch, a deterministic agent step, a metacognitive observer, and preference-score ranking. The original project's Gemini generation, Chroma/Ollama vector search, model training, web/file tools, and persistence are **not** implemented here. The in-memory recall algorithm is literal substring matching, **not semantic similarity**. No claim of machine consciousness is made.

## Requirements

[Flow 2.x](https://github.com/flooooooooooow/flow), Linux x86-64 or macOS arm64.

```bash
flow run src/chimera_test.flow
flow run src/demo.flow
```

The library API lives in `src/chimera.flow`; import it with `import "chimera.flow"` from another Flow module in `src/`. Explicit `chimera_init()` and `chimera_shutdown()` manage memory. Calls to `chimera_step` consume externally selected actions; they do not contact an LLM.

See [PORTING.md](PORTING.md) for the upstream-to-Flow mapping and gaps.

This is an independent Flow implementation of upstream behavioural interfaces, not a copy of upstream Python source. Attribution: [LarytheLord / Project-Chimera](https://github.com/LarytheLord/Project-Chimera).