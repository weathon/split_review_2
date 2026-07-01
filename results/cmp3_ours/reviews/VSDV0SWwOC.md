Now I have a solid calibration picture. Let me produce the final review.

## Summary

This paper proposes LS-Merge, a framework for merging LLMs in a learned latent space using a transformer-based VAE with two-stage curriculum training. The key idea is to encode model weights into a latent space via a VAE, perform merging operations (interpolation, soup, etc.) in that space, and decode back to weights. The paper targets two capabilities: (1) self-merging (improving a single model by sampling and averaging its own latent codes) and (2) heterogeneous merging across different architectures via optimal transport alignment.

## Strengths

- **Weight distribution analysis (Section 3.1, Table 1, Figure 2).** The paper documents that LLM weights exhibit excess kurtosis routinely above 5 and up to ~15 across Gemma and LLaMA families, with near-zero means and low variance. This contradicts Gaussian assumptions in prior weight-space work and provides concrete motivation for the encoder design (transformer blocks, two-stage curriculum). The PCA analysis showing low-rank structure alongside heavy tails is informative.

- **PCA vs. VAE ablation (Table 8) cleanly demonstrates that linear compression is insufficient for weight reconstruction.** At compression ratio 1.6×, PCA drops MMLU from 41.44 to 25.50 (near random), while the VAE retains 39.89. This validates the paper's central architectural claim: pretrained weights reside on a non-linear manifold that linear projections cannot preserve. The experiment is well-designed and the result is unambiguous.

- **LoRA expert merging results (Table 3) are solid.** LS-Merge (soup) achieves 56.0 on MMLU vs. 52.5 for the best weight-space baseline (SLERP), and leads on 5 of 8 benchmarks. The gains are consistent and non-trivial in magnitude. This is the most convincing empirical result in the paper.

## Weaknesses

### Major

**1. Self-merging improvements are mechanistically unexplained and reported with suspicious variance (Section 4.1, Table 2).**

The paper reports that encoding a single model, sampling multiple codes from its VAE posterior, averaging those codes, and decoding yields *better* performance than the original pretrained model — e.g., Gemma-3-1B-it MMLU: 32.20 → 35.13 (+2.93). The problem is that averaging multiple samples from a VAE posterior  q(z|x)  should converge to the posterior mean μ(x). Decoding μ(x) is the standard VAE reconstruction. The standard VAE baseline (Table 2: 32.60) barely improves over the base model (32.20), yet the averaged posterior samples improve to 35.13. The paper provides no mechanism explaining why this should happen, and the offered explanation ("exploring the learned latent distribution") is not logically connected to the reported behavior. This undermines confidence in whether the improvement is genuine or an artifact (e.g., the VAE was trained on both 1B and 4B models, so self-merging the 1B model might inadvertently draw on structure learned from the 4B model). Additionally, several entries for LS-Merge show ±0.00 variance (e.g., Gemma-3-4B-it MMLU: 54.20 ± 0.00, HellaSwag: 50.10 ± 0.00). For a stochastic process involving posterior sampling, zero variance across multiple runs is implausible and the reporting is not justified.

**2. Heterogeneous merging—the paper's headline contribution—lacks critical baselines and the evidence is thin (Section 4.4, Table 5).**

The paper's most novel claim is cross-architecture merging, yet the evaluation has significant gaps:
- **No weight-space heterogeneous baseline.** The paper compares against "baseline parameter/latent mixing without alignment" but never tests the simplest possible approach: projecting weights to a common dimension (via padding, truncation, or SVD) and interpolating directly. Without this baseline, it is impossible to tell whether the VAE+OT pipeline adds value over a trivial procedure.
- **Gains are modest.** OT+interpolation improves WinoGrande by +0.92, ARC-C by +0.56, and HellaSwag by +1.03 over the base model. No confidence intervals are reported, so statistical significance is unclear.
- **OT-only is destructive.** Applying OT alignment alone (without interpolation) drops WinoGrande from 56.83 to 51.13 and ARC-C from 42.78 to 34.25. The paper does not analyze why OT corrupts the latents, nor whether the small net gain after interpolation justifies the complexity cost.
- **Only one cross-family experiment is shown** (LLaMA-3.2-1B → Gemma-3-1B). For a method claiming to be "architecture-agnostic," demonstrating generality on at least 2–3 heterogeneous pairs is expected.

### Minor

**1. Key hyperparameters omitted.** The chunk size  c , latent dimension  z_d , and the exact operational definition of "compression ratio" (parameter count reduction? total bit count?) are not specified, which hurts reproducibility.

**2. Layer pairing for heterogeneous architectures is ambiguous.** Algorithm 1 sets  N = min(|L_src|, |L_tgt|)  and "defines pairs" without specifying how layers are matched when depths differ (e.g., 24-layer Gemma vs. 16-layer LLaMA). Is it one-to-one from the first layer? By functional role (attention vs. MLP)? This is a critical design choice left unspecified.

**3. Evaluation conflates reconstruction quality with downstream robustness when making "compression" claims (Section 5.2, Section 5.3).** The paper measures VAE quality exclusively via downstream task accuracy. While this is standard for model merging papers, claims about *compression fidelity* (Section 5.2 "compression trade-off", Section 5.3 "functional reconstruction fidelity") would be strengthened by also reporting direct weight-space reconstruction error (e.g., per-layer MSE, cosine similarity). Without this, it is unclear whether performance degradation at high compression (Table 7) reflects poor reconstruction or genuine functional changes.

### Trivial

None.

## Nice-to-Haves

- Reporting computational cost (GPU hours, VAE parameter count, training time) would help practitioners assess the practical trade-off.
- The self-merging experiment would benefit from an ablation varying the number of posterior samples to test whether improvement saturates or grows monotonically.
- The heterogeneous merging evaluation could be strengthened by testing VAE generalization where the VAE is trained on one model family and applied to merge a different held-out family.

## Removed Points

These points were flagged by the harsh critic but are removed with justification:

- **"Data leakage / VAE trained on both models"** – The VAE is naturally trained on the data it encodes. The paper's generalization experiment (Section 5.2) explicitly tests on unseen models (trained on Gemma-3-4B-it, tested on Gemma-3-1B-it and LLaMA-3.2-1B-it), partially addressing this. Removed as overblown.
- **"Self-merging improvement might come from exposure to larger model during VAE training"** – This is a potential explanation but speculative; it's already covered under the unexplained mechanism concern above. Removed as redundant.
- **"Comparison to Task Arithmetic and AIM uses lm-eval, introducing uncontrolled variable"** – The paper explicitly notes this is "for fair comparison" with baselines, which is standard practice. Removed as a nitpick.
- **"Section 3.1 theoretical compressibility argument is standard and doesn't add insight"** – The empirical PCA analysis is the real contribution; the theoretical framing provides context. Removed as unfair.
- **"Related work does not cover prior weight-space learning in enough detail"** – The paper cites the key references (Schürholt et al., Peebles et al.). Level of detail is a judgment call. Removed per rules about not criticizing depth of related work discussion beyond identifying actual missing references.
- **"PCA baseline ambiguity (per-layer vs per-matrix)"** – PCA on flattened weight vectors per layer and per-matrix truncated SVD are closely related (both capture the same low-rank structure). The distinction is technically correct but does not materially affect the paper's conclusions. Demoted to removed.
- **"Scale limited to ≤4B"** – The paper works with what's feasible for full-weight VAE encoding. The approach is demonstrated on models up to 4B and LoRA experts on 7B. Not a fatal limitation. Removed.
- **"No analysis of computational cost"** – Fair to flag but noted as a nice-to-have, not a weakness.
- **"Self-merging improvement marginal on 4B"** – Actually the improvement on 4B is small (54.10→54.20), but on 1B it's substantial (32.20→35.13). The unclear mechanism is the real issue, not the magnitude on one model.

## Novel Insights

The harsh critic's analysis of the self-merging paradox is genuinely insightful: averaging posterior samples from a VAE should converge to the posterior mean, producing the same reconstruction as the standard VAE decoding. The paper's reported improvement over the standard VAE reconstruction therefore requires an explanation the paper does not provide. This observation points to either (a) an undisclosed difference in experimental setup, (b) an interesting property of the VAE decoder that makes it benefit from small perturbations to the latent code, or (c) data contamination from the VAE seeing multiple model checkpoints. Resolving this would strengthen the paper's contribution.

## Suggestions

1. Provide the missing weight-space heterogeneous baseline (e.g., zero-pad or SVD-project weights to a common dimension, then average) for Table 5. Without this, the headline claim of enabling heterogeneous merging is unsubstantiated.
2. Explain or retract the self-merging claim. If the improvement is genuine, the mechanism must be clarified. Report the number of posterior samples used and show variance across random seeds properly.
3. Add at least one additional cross-family heterogeneous merging experiment (e.g., LLaMA → Gemma on different model sizes) to demonstrate generality.
4. Report key hyperparameters (chunk size c, latent dimension, compression ratio definition) and specify the layer-pairing strategy in Algorithm 1.

## Score and Decision

**Calibration anchors.** All scores are human average scores from the deepreview_13k calibration corpus.

| Anchor Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| ATM: Alternating Tuning and Merging | 3.00 | R1 | Less novel core idea; stronger evaluation but flawed assumptions about multi-task data access |
| Structure and Behavior in Weight Space Representation Learning | 4.25 | R1 | Similar domain (weight-space autoencoders); limited to CNNs, but cleaner experimental design |
| Few-shot Style-Conditioned LLM Text via Latent Interpolation | 4.25 | R2 | Uses VAE for LLM weight latents (similar technique); different application, comparable evidence strength |
| SUPERMERGE | 4.33 | R2 | Gradient-based merging; strong results, insufficient baselines — similar gap pattern |
| CABS: Conflict-Aware Sparsification | 4.75 | R2 | Model merging with sparsification; well-validated but incremental contribution |
| Extend Model Merging from FT to PT LLMs | 5.67 | R2 | More thorough evaluation of a less ambitious extension; rejected despite stronger evidence |
| MAP: Amortized Pareto Fronts | 6.33 | R1 | Well-evaluated method with clear baselines and practical utility; accepted |
| Model Merging by Uncertainty-Based Gradient Matching | 6.00 | R1 | Clean ablation study; accepted — represents a well-supported acceptance threshold |

**Bracket.** Round 1 bracketing: the paper sits between the 3.5–5.5 band (where weight-space autoencoder papers with incomplete evaluations reside) and the 5.5–7.5 band (where well-supported merging papers reach borderline accept). The paper's novel core idea is above the typical 3–4 reject band, but the experimental gaps in its headline claim prevent it from reaching the 5.5+ band. Round 2 narrowing: compared to SUPERMERGE (4.33) which also had baseline omissions, the current paper has a more novel contribution but also more significant evidence gaps. Compared to "Structure and Behavior in Weight Space" (4.25), the current paper addresses a more impactful problem (LLM merging) but has weaker validation. **Final bracket: 4.0–5.0.**

**Final score: 4.5.** The paper addresses an important problem and the core idea is interesting. The weight distribution analysis, PCA vs. VAE ablation, and LoRA expert merging are genuine contributions. However, the paper's headline heterogeneous merging claim lacks the most basic weight-space baseline, is evaluated on only one cross-family pair with modest gains, and the OT-only condition is destructive without analysis. The self-merging results are mechanistically unexplained and reported with suspicious variance. These gaps are addressable, but in the current form the evidence does not support the central claims as presented. Decision: **Reject**.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>