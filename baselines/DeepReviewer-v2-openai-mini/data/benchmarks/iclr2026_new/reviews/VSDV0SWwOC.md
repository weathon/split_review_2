## Summary
This paper introduces **LS-Merge**, a framework that reimagines model merging by operating in a learned latent space of LLM parameters rather than directly in weight space. The core idea is to encode pretrained model weights into a compact latent representation using a transformer-based variational autoencoder (VAE), perform merging operations (linear interpolation, soup, task arithmetic) in this latent space, and then decode back to weights. This approach naturally supports both homogeneous merging (same architecture) and, crucially, heterogeneous merging across different model architectures and sizes.

The paper makes four main contributions:
1. **Weight distribution analysis**: The authors show that LLM weights exhibit heavy-tailed, leptokurtic distributions, motivating the use of non-linear, tail-sensitive encoders.
2. **Latent-space merging**: A transformer VAE with a two-stage curriculum (deterministic pre-training then VAE fine-tuning) enables stable encoding and reconstruction of billion-parameter weights.
3. **Heterogeneous alignment**: For cross-architecture merging, Optimal Transport (OT) with a closed-form Gaussian approximation aligns the latent distributions of different model families before interpolation.
4. **Empirical validation**: Experiments on Gemma-3-1B/4B, LLaMA-3-1B/2-7B/2-13B, and LoRA expert merging show consistent improvements over weight-space baselines, with the first demonstration of cross-family merging (LLaMA ↔ Gemma).

While the paper presents a novel and technically sound approach, several concerns affect its strength: limited VAE training data (Gemma only), uncontrolled multi-sample advantages in expert merging, missing statistical significance measures, underreported cross-family evaluation, and overclaimed conclusions relative to the evidence scope.

## Strengths
**S1. Novel problem framing with high practical relevance.** The paper identifies a genuine bottleneck in existing model merging — architectural homogeneity — and proposes a principled solution through latent-space encoding. The ability to merge models with different widths, depths, and model families addresses a real need in LLM reuse and composition, where practitioners often have heterogeneous checkpoints.

**S2. Strong empirical validation of the core VAE design.** The PCA vs. VAE comparison (Table 8) convincingly demonstrates that linear compression destroys functional performance even at mild ratios (r=1.6), while the non-linear VAE preserves near-original accuracy across all compression levels. This provides compelling evidence that valid pretrained weights reside on a non-linear manifold, making the VAE architecture a geometric necessity rather than a stylistic choice.

**S3. Interesting and well-documented weight distribution analysis.** The analysis of LLM weight statistics (Table 1) revealing high kurtosis (leptokurtic distributions, up to ~15) in early self-attention layers is a valuable empirical finding in itself. The connection of this observation to encoder design — that encoders must preserve tail events rather than over-regularize — is a thoughtful design insight that could influence future weight-space learning work.

**S4. First demonstration of cross-family model merging.** The cross-architecture merging results (Table 5) show that with OT alignment, latent-space interpolation between LLaMA and Gemma models improves over baselines on WinoGrande, ARC-C, and HellaSwag. Even with limited evaluation, this is a technical milestone that weight-space methods cannot achieve at all, representing a genuine advance in model composition capabilities.

**S5. Systematic ablation studies.** The ablation on component contributions (Table 6) and compression trade-offs (Table 7) provide useful insights for practitioners, particularly the finding that merging attention layers alone can degrade performance, while combining MLP and attention layers achieves the best results. This practical guidance helps users of the method know what to expect.

## Weaknesses
### W1. Uncontrolled confounds in expert merging evaluation (Major)
The expert merging experiments (Section 4.2, Table 3) give LS-Merge an inherent advantage by sampling multiple latent codes per expert before merging, effectively creating more "virtual experts." Weight-space baselines only use a single weight sample per expert. Without a control where weight-space methods also benefit from multiple perturbed samples (e.g., noisy weights + averaging), it is impossible to determine whether the improvement comes from latent-space merging or simply from the multi-sample averaging effect. Additionally, no standard deviations or significance tests are reported for any method, despite many gains being small (e.g., MMLU: 56.0 LS-Merge vs 52.5 SLERP). This threatens the validity of the "consistent outperformance" claim. **Fix**: Add a weight-space multi-sample control; report mean±std over ≥3 seeds; provide pairwise significance tests.

### W2. Conclusion overclaims relative to evidence (Major)
The conclusion states "comprehensive experiments," "for the first time," and "scalable and architecture-agnostic paradigm." However: (a) only models up to 13B are tested, not 70B+; (b) only VAE is evaluated (not other generative models mentioned in the intro); (c) the VAE is trained only on Gemma weights, so Llama results conflate generalization with merging quality; (d) cross-family evaluation covers only 3 datasets. The "first" claim for cross-family merging requires explicit literature verification. **Fix**: Replace "for the first time" with "to our knowledge"; replace "comprehensive" with "initial"; bound scalability claims to tested scales (1B-13B).

### W3. VAE training data limited — conflates reconstruction and merging (Major)
The VAE is trained exclusively on Gemma-3-1B-it and Gemma-3-4B-it weights (plus LoRA experts). All Llama evaluations (Tables 4, 5, 7) therefore involve zero-shot VAE generalization. Table 7 shows significant performance degradation at r=2 (Gemma-3-1B-it MMLU drops from 40.76 to 32.22), but the main experiments do not separate VAE reconstruction error from merging effectiveness. This means some of the reported gains/losses may be artifacts of VAE generalization quality rather than intrinsic properties of latent-space merging. **Fix**: Add a column in Tables 2-4 indicating VAE training coverage; report reconstruction fidelity (weight MSE or performance retention) per model separately.

### W4. Missing statistical rigor and variance reporting (Major)
Across all experiments, no confidence intervals or significance tests are provided. Table 2 shows some zero-variance entries (LS-Merge std=0.00 for MMLU on 4B), which is suspicious — either the evaluation is deterministic (single seed, greedy decoding) or there is a reporting error. Many compared baselines in Table 3 differ by small margins (e.g., 2-3 points). Without variance estimates, the stability and reliability of the claimed advantages cannot be assessed. **Fix**: Report all metrics with variance over ≥3 evaluation seeds; explain zero-variance entries; add effect-size analysis.

### W5. Two-stage curriculum not ablated; β unreported (Major)
The two-stage training curriculum (deterministic AE → VAE fine-tuning) is presented as a key technique for stabilizing training on heavy-tailed weights, but its effect is never isolated. Without comparing (a) standard VAE training from scratch, (b) two-stage curriculum (current), and (c) deterministic AE only, the contribution of the KL fine-tuning stage is unknown. Furthermore, the β value in Eq. (1) is not reported, making the VAE objective underspecified. **Fix**: Add the curriculum ablation experiment; report β and how it was selected.

### W6. Cross-family merging underreported (Minor)
The cross-family merging experiment (Section 4.4) has only 3 datasets (WinoGrande, ARC-C, HellaSwag) and a single λ=0.1. The degradation baseline ("mixing without alignment") is mentioned but not shown quantitatively. The note about "issues with llama model when using the previous evaluation code" raises concerns about evaluation consistency. **Fix**: Add the no-alignment baseline row; clarify the Llama evaluation issue; expand to MMLU and GSM8k.

### W7. PCA argument inconsistency (Minor)
Section 3.1 uses PCA to argue that weights are compressible (low-rank structure), but Section 5.3 shows PCA collapses functional performance even at r=1.6. This creates a rhetorical contradiction. The paper should directly acknowledge that variance-preserving compression ≠ function-preserving compression, and use PCA only as motivation for why non-linear methods are needed. **Fix**: Restructure Section 3.1 to frame PCA as evidence that *linear* methods fail, not as evidence that compression is easy.

### Additional Minor Issues
- The chunk size c and latent dimension z_d are not reported in the main text, hindering reproducibility.
- OT alignment assumes Gaussian latents without justification; computational cost (O(d^3) per layer) is not reported.
- Self-merging improvement (~4%) lacks a control for stochastic averaging effects.
- The attention merging degradation hypothesis (co-adaptation) is not distinguished from reconstruction quality differences between attention and MLP layers.
- Abstract claims "scalable" without any scaling experiments or efficiency analysis.

### Novelty and Comparison Note
External literature verification is unavailable in this run (Retrieval-Disabled Mode). Novelty verdicts for contributions C1-C3 and detailed related-work positioning are deferred — manual verification is needed to confirm the "first" claim for cross-family merging and the novelty of the OT-based latent alignment approach relative to prior weight-space learning work (Schürholt et al., Peebles et al., etc.).

## Score
**Final Score: 6/10**

This score reflects the paper's genuine conceptual novelty (latent-space model merging with OT-based cross-architecture alignment) and strong preliminary evidence (PCA vs. VAE comparison, consistent improvements in expert merging), weighed against significant validity concerns that reduce confidence in the reported results. The key issues are: (1) uncontrolled multi-sample advantage gives LS-Merge an unfair edge over weight-space baselines, (2) no statistical significance or variance reporting despite small performance margins, (3) VAE training data limited to Gemma models conflates reconstruction quality with merging effectiveness for Llama evaluations, and (4) the conclusion overclaims relative to the tested scope. These weaknesses are fixable with additional controls, statistical reporting, and more measured claims, but in their current form they prevent the paper from being a definitive contribution. The paper is suitable for further development and would benefit from addressing the major concerns listed above before final publication.