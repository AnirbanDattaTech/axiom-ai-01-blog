---
title: "Transformer Memory Mechanics: Encoder-Decoder vs Decoder-Only"
date: 2026-09-22
draft: false
summary: "Analyzing attention layouts, KV cache footprint, and memory bandwidth across sequence lengths."
cover:
  image: "transformer.png"
  alt: "Transformer Architecture"
  caption: "Attention layers and memory flow"
  relative: true
---

Analyzing attention layouts, KV cache footprint, and memory bandwidth across sequence lengths.

```python
# Head dimension 256 requires FlashAttention-3 kernels.
head_dim = 256
```

![Transformer Flow](transformer.png)