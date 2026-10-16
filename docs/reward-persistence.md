# CRW1 reward snapshots

The Flow-native eight-feature linear preference ranker in `src/reward.flow` can be persisted using `src/reward_persistence.flow`. This is **not** the upstream DistilBERT/TRL reward model, does not tokenize prompt/response pairs, and does not provide pretrained weights.

`chimera_reward_save(path, model)` writes an 80-byte CRW1 snapshot: four ASCII bytes `CRW1`, a little-endian 32-bit nonnegative training-update count, eight native IEEE-754 64-bit weights, and a little-endian Adler-32 checksum over the four update bytes and 64 weight bytes. The `trained` flag is reconstructed from `updates > 0`.

`chimera_reward_load(path, previous)` returns a `RewardLoadResult`. It rejects invalid headers, out-of-range updates/weights, checksum mismatches, truncation and trailing data. A failed load returns `success: false` and the unchanged supplied model. Save rejects non-finite/out-of-range weights and inconsistent training metadata.

These snapshots are native-endian and assume IEEE-754 f64; they are not portable across arbitrary architectures. Saving directly overwrites a trusted host-selected path, so it is **not** crash-atomic. Files are neither encrypted nor authenticated against deliberate adversarial modification. Model-generated paths must never be passed directly to this API.

CI executes deterministic Flow round-trip and malformed-file regression tests. No production model or training corpus is used.
