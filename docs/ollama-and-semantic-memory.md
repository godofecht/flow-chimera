# Ollama embeddings and semantic memory (Flow 2.x)

This is a genuine native Flow path from local Ollama `POST /api/embed` to cosine-ranked episodic memory. Neither the embedding call nor the retrieval code silently truncates an embedding to eight dimensions. **The tests use a deterministic local HTTP fixture and do not establish the quality or correctness of any real embedding model.**

## Local model setup

Install Ollama and `curl` (both are external executables). Run your Ollama server locally and pull the model used by upstream Project Chimera:

```sh
ollama pull qwen3-embedding:0.6b
export CHIMERA_OLLAMA_URL=http://127.0.0.1:11434/api/embed
export CHIMERA_OLLAMA_EMBED_MODEL=qwen3-embedding:0.6b
flow run src/ollama_demo.flow
```

The endpoint variable accepts **only** `http://127.0.0.1:<numeric-port>/api/embed`. Other hosts, URL paths, URL userinfo, redirects and proxies are disallowed by the Flow code. The `curl` invocation is a fixed argv array built without a shell, with connection and overall timeouts. No remote credentials or API keys are required for local Ollama.

## Main APIs

`chimera_ollama_embed(text, output, capacity)` performs an actual HTTP call and decodes the returned model vector (1–4,096 dimensions). It rejects malformed or nonfinite vectors and does not modify the output buffer on failure. `chimera_ollama_request(model, input)` serializes JSON with escaped text; release its owned string with `chimera_ollama_free`.

`chimera_semantic_init()` initializes the independent full-dimensional 64-experience store. `chimera_ollama_remember(observation, action, outcome)` requests an embedding and stores the normalized vector alongside owned experience strings. `chimera_ollama_recall_text(query, rank)` embeds the query using the same configured model and returns the rank-th nearest episode with a cosine score. The store compares only vectors of equal dimensions; mixed-dimensional histories remain separated.

`chimera_semantic_save(path)` and `chimera_semantic_load(path)` persist/reload the store. Invalid snapshot input is validated into temporary allocations before replacing the current live memory. Caller-supplied paths must be trusted; never accept model-proposed paths.

The new **CSM1** snapshot format stores an ASCII magic header, little-endian record count (up to 64), then for each experience three length-prefixed strings (each at most 8,192 bytes), a little-endian vector dimension and that many native 64-bit floats. Snapshots are unencrypted, not crash-atomic, not checksummed and native-endian for double payloads. This store is intentionally separate from the existing fixed-8D `FCH2` snapshot schema.

## Reproducible validation

```sh
flow run src/ollama_embedding_test.flow
flow run src/semantic_memory_test.flow
python3 tests/mock_ollama.py &
CHIMERA_OLLAMA_URL=http://127.0.0.1:18764/api/embed flow run src/ollama_provider_test.flow
```

These tests cover malformed JSON, numeric bounds, exact endpoint restrictions, actual socket/HTTP exchange, 1,024-dimensional memory ranking, semantic ring eviction, snapshot round-trips, and invalid snapshot load retaining existing memory.

## Parity limitation

The original project's Chroma database and Ollama embedding semantics are only partially reproduced. This is a stand-alone, local, exact-dimension cosine index, not an ANN/vector database and not a drop-in Chroma backend. Query latency is linear in at most 64 stored experiences. The existing model-driven `live_agent.flow` still uses its older episodic prompt builder; integrating this store into that live context and introducing a safe, scalable persistence format for large histories remains future work. No emotion or DistilBERT inference is supplied here.
