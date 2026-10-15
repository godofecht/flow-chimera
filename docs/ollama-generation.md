# Local Ollama language-model generation in Flow

`src/ollama_agent.flow` is an opt-in **real local generation backend** for the existing Chimera perceive–think–act loop. It uses `POST /api/generate` with `stream:false` and `format:"json"`, and accepts model output only after strict JSON parsing and fixed action allowlisting. The existing remote Gemini provider is unaffected.

## Usage

```sh
ollama pull qwen2.5:7b
export CHIMERA_OLLAMA_GENERATE_URL=http://127.0.0.1:11434/api/generate
export CHIMERA_OLLAMA_GENERATE_MODEL=qwen2.5:7b
export CHIMERA_TASK="Add five and ten, then exit"
export CHIMERA_MAX_STEPS=4
flow run src/ollama_cli.flow
```

`CHIMERA_MAX_STEPS` is capped at eight. An optional `CHIMERA_SNAPSHOT` path persists FCH2 working and episodic agent state. The path is host-controlled, not model-proposed.

The Flow implementation uses an exact IPv4 loopback endpoint, a fixed curl argument vector without a shell, no proxy, no redirects and bounded request/response sizes. It rejects invalid model identifiers, incomplete model responses and malformed action JSON. Actions are still **only** `echo`, `sum_numbers` and `exit`; the model is not authorized to execute terminal, filesystem or web requests.

A deterministic local fixture at `tests/mock_ollama.py` tests `/api/generate` without installing model weights. The CI verifies HTTP transport, nested JSON decoding, action dispatch, episodic recording and the bounded CLI. This does not establish that the real model emits the intended action reliably, or that the system reproduces all upstream Python behavior.

The separate [Ollama semantic-memory integration](ollama-and-semantic-memory.md) supplies persistent full-dimensional embeddings but is not yet included automatically in this generation prompt. This will require deliberate provider/model consistency and prompt-context limits.
