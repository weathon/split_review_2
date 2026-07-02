### Summary

This paper introduces DiSTAR, a zero-shot text-to-speech (TTS) framework that leverages a discrete residual vector quantization (RVQ) space. DiSTAR integrates an autoregressive language model with a masked diffusion model, eliminating the need for forced alignment or a duration predictor. Specifically, DiSTAR uses the autoregressive model to draft RVQ tokens and then applies parallel diffusion-based infilling to complete the sequence, enabling long-form synthesis with blockwise parallelism and mitigating exposure bias. Additionally, the discrete code space allows for explicit control during inference, supporting both greedy and sample-based decoding with classifier-free guidance, accommodating trade-offs between robustness and diversity, and enabling variable bit-rate and controllable computation via RVQ layer pruning at test time. Experimental results demonstrate that DiSTAR outperforms state-of-the-art zero-shot TTS systems in robustness, naturalness, and speaker/style consistency.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The paper is well-written and easy to follow.
2. The proposed DiSTAR framework is reasonable, and the experimental results are promising.

### Weaknesses

#### Some Related Works


#### comment

1. The authors should include subjective evaluation results in Table 1 to provide a more comprehensive comparison.
2. The authors should add a comparison of the inference time with other methods.
3. The authors should include subjective evaluation results for LibriSpeech (LC) in Table 2.
4. The authors should conduct subjective evaluations on the LibriSpeech (LC) dataset to assess the impact of different decoding strategies.
5. The authors should provide an explanation for why the greedy decoding strategy performs worse than the sampling strategy in terms of SPK in Table 3.

### Suggestions

The paper would benefit from a more thorough analysis of the subjective evaluation results, particularly concerning the comparison with other state-of-the-art TTS systems. While objective metrics like WER and SIM are useful, they do not fully capture the perceptual quality of the synthesized speech. Including Mean Opinion Score (MOS) tests, or similar subjective evaluations, would provide a more complete picture of DiSTAR's performance relative to other methods. Specifically, the authors should consider conducting CMOS (Comparison Mean Opinion Score) tests, where listeners are asked to compare the output of DiSTAR with other systems on aspects such as naturalness and intelligibility. This would allow for a more direct and nuanced comparison, highlighting the strengths and weaknesses of the proposed approach in a way that objective metrics alone cannot.

Furthermore, the paper should include a detailed analysis of the inference time of DiSTAR compared to other methods. The current discussion lacks a clear comparison of the computational cost of the proposed approach with existing state-of-the-art TTS systems. This is a critical aspect for practical applications, and the authors should provide a breakdown of the inference time for each component of the DiSTAR framework, such as the autoregressive model and the diffusion model. This analysis should also consider the impact of different decoding strategies (e.g., greedy vs. sampling) on the inference time. A clear comparison of the inference time with other methods, including both autoregressive and diffusion-based approaches, would provide a more complete understanding of the practical implications of the proposed method. This would also help to identify potential bottlenecks and areas for optimization.

Finally, the authors should provide a more detailed analysis of the impact of different decoding strategies on the quality of the synthesized speech. While the paper mentions both greedy and sampling strategies, it lacks a thorough evaluation of their impact on subjective metrics. The authors should conduct CMOS tests on both the Seed-TTS and LibriSpeech datasets to assess the naturalness and intelligibility of the synthesized speech under different decoding strategies. This analysis should also include a discussion of the trade-offs between the two strategies, such as the potential for higher variability with sampling versus the stability of greedy decoding. A more detailed analysis of the impact of decoding strategies would provide a more complete understanding of the capabilities of DiSTAR and its potential for different applications.

### Questions

Please see Weaknesses.

### Rating

6

### Confidence

3

**********