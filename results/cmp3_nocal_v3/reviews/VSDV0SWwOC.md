## Summary

LS-Merge proposes shifting model merging from raw weight space to a learned latent space, using a transformer-based VAE to encode LLM weights and perform interpolation in the latent manifold. The framework enables self-merging (sampling multiple latents from one model), homogeneous merging, and heterogeneous (cross-architecture) merging via an optimal transport alignment step. Experiments on Gemma, LLaMA, and LoRA-expert models compare against weight-space methods (Soup, SLERP) and representation-based methods (AIM, Task Arithmetic).

## Strengths

- **Novel and well-motivated framework.** Shifting merging from weight space to a learned latent space directly addresses architectural homogeneity constraints — a genuine limitation of prior work that neither weight-averaging nor activation-based methods can handle. (Section 1, Figure 1)

- **Principled weight-distribution analysis (Table 1).** The kurtosis measurements (5–15 across layers) provide concrete empirical grounding for the encoder architecture, justifying a design that preserves tail events rather than assuming Gaussianity. This finding is independently useful beyond this paper.

- **OT-based alignment for heterogeneous models is technically sound.** Recognizing that latent dimensionality matching alone is insufficient (Figure 9b) and treating heterogeneous merging as manifold registration with a closed-form Gaussian OT solution (Section 3.3) is principled. The ablation in Table 5 cleanly shows that OT alignment + interpolation is necessary, not just alignment alone.

- **PCA vs. VAE comparison (Table 8) is clean and informative.** Testing across compression ratios 1.6×, 2.0×, 4.0× and showing PCA collapses at all ratios while the VAE remains stable is a convincing demonstration that LLM weights do not lie on a linear subspace. This directly supports the non-linear manifold claim.

## Weaknesses

### Fatal
None.

### Major

- **Unexplained VAE reconstruction improvement over the base model (Table 2) + evaluation protocol ambiguity.** The VAE reconstruction (single latent sample, lossy 2× compression) outperforms the original base model on most metrics — e.g., Gemma-3-4B-it MMLU goes from 53.10→54.10±0.36, HellaSwag from 47.40→49.03±0.70, GSM8k from 29.90→31.27±0.55. A lossy autoencoder should not systematically improve upon the original, yet the improvement is consistent across 3/4 benchmarks for the 4B model. The paper provides no explanation. Additionally, the evaluation switches between an unspecified harness (Tables 2–3) and *lm-eval* (Section 4.3 onward), and base-model scores lack standard deviations, making it impossible to assess whether the improvements are within noise. The authors must (i) confirm a shared evaluation harness for all rows within each table, (ii) report base-model standard deviations, and (iii) explain why a lossy reconstruction consistently improves over the original.

- **VAE training data composition is critically underspecified.** The paper states "pretrained weight snapshots for Gemma-3-1B-it and Gemma-3-4B-it, plus LoRA experts" without saying how many snapshots. The manifold-learning claim (Section 5.3) depends on the VAE seeing diverse weight configurations during training. If this is only 1–2 final checkpoints per model, the VAE could be memorizing rather than learning a manifold. This detail must be reported to evaluate the generalization claims.

### Minor

- **Self-merging lacks a weight-space stochastic averaging baseline.** The ≈4% improvement in Table 2 could potentially be replicated by adding noise to weights and averaging in weight space. Without this comparison, it is unclear whether the advantage comes from the latent representation or simply from stochastic averaging.

- **Heterogeneous merging evaluated on limited scope.** The cross-family result (Table 5) reports only 3 benchmarks (WinoGrande, ARC-C, HellaSwag) at a single λ=0.1 value, with modest gains (≤1.03 points). No statistical significance is reported. Expanding to the full benchmark suite and testing multiple λ values would strengthen the claim of robust cross-architecture merging.

- **VAE trained on constituent model weights in AIM comparison (Table 4).** The VAE is trained on the combined weights of the code and instruct fine-tuned models before merging. AIM and Task Arithmetic do not train on target model weights. While the VAE learns reconstruction (not task performance), this asymmetry should be discussed.

- **"Posterior collapse" claim (Section 5.2) asserted without verification.** Performance degradation at higher compression is attributed to posterior collapse, but no KL divergence or latent variance measurements are provided to support this.

- **Scalability claims unsupported.** The abstract claims "scalable" and "efficient" but no evidence is provided — VAE parameter count, encoding/decoding runtime, and memory footprint are not reported. Given the transformer VAE (6 encoder + 6 decoder blocks) plus per-merge encoding/decoding, this omission is notable.

### Trivial

- **Chunk size c (Section 3.2) is not ablated or justified.** The flatten→pad→chunk strategy involves a free parameter c whose effect on reconstruction quality is not analyzed.

## Nice-to-Haves

- A weight-space stochastic averaging baseline for self-merging
- Comparison to heuristic shape-matching methods (pad/truncate and apply SLERP) for heterogeneous merging
- Ablation of the two-stage curriculum (deterministic pretrain → KL fine-tune)
- Reporting of VAE parameter count and encoding/decoding time

## Removed Points

- "Section 1 frames requiring multiple source models as a limitation" — subjective opinion, not a technical weakness
- "Section 3.1 PCA analysis at single-layer level is insufficient" — the VAE processes per-layer chunks, so this analysis is appropriately scoped
- "No comparison to weight-space methods with shape-matching heuristics" — moved to Nice-to-Haves
- "Two-stage curriculum not ablated" — moved to Nice-to-Haves
- "Memory footprint not discussed" — absorbed into the scalability Minor weakness
- "Standard deviations of base model evaluations not reported" — absorbed into the first Major weakness

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify evaluation protocols.** Specify which harness was used for each table and confirm all rows within a table share an identical setup. Report base-model scores with standard deviations.
2. **Explain or resolve the VAE reconstruction improvement.** If this is an artifact, correct it. If the VAE acts as a denoiser, provide evidence and discussion.
3. **Report the number of weight snapshots used for VAE training.** This detail directly determines whether the manifold-learning claim is defensible.
4. **Expand heterogeneous merging evaluation** to more benchmarks and multiple λ values with significance tests.
5. **Report VAE size, encoding/decoding cost, and memory footprint** to support the scalability claim.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>