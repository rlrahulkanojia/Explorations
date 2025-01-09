# KV Cache Experimentation to find the speedup attained using cache in generation process.


## Findings
1. On MAC with gpt2, 
    - with KV caching: 21.49 +- 0.887 seconds
    - without KV caching: 203.982 +- 11.649 seconds
2. The speedup depends on following factors:
    - The depth of decoder network.
    - Number of output tokens.
    - Hardware


References:

1. https://huggingface.co/blog/kv-cache-quantization
2. https://medium.com/@joaolages/kv-caching-explained-276520203249
