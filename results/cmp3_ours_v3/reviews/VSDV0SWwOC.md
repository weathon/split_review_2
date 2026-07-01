## Summary

LS-Merge proposes shifting model merging from weight space to a learned latent space using a transformer-based VAE. The key idea is to encode LLM weights into a compressed latent representation, perform merging (via interpolation or soup) in latent space, and decode back to weights. The paper claims three contributions: (1) enabling "self-merging" (averaging multiple posterior samples of a single model), (2) expert merging of LoRA adapters in latent space, and (3) heterogeneous cross-architecture merging via OT-based latent alignment.

## Strengths

- **Novel and well-motivated problem formulation.** Shifting model merging from weight space to a learned latent space to enable heterogeneous merges is genuinely underexplored. The framing of heterogeneous merging as a manifold registration problem (Section 3.3) is conceptually clean and addresses a real limitation of existing weight-space methods.

- **Informative weight-distribution analysis (Section 3.1, Table 1).** The documentation that LLM weights are leptokurtic (kurtosis up to ~15) with near-zero means and low variances is a concrete empirical observation with design implications for weight-space encoders. The point that Gaussian-prior VAEs may need special handling for such distributions is well-taken.

- **Broad experimental scope across multiple merging scenarios.** The paper evaluates four distinct scenarios (self-merging, expert merging, cross-architecture, ablations) across model families (Gemma, LLaMA), providing a richer picture than a single-task evaluation. The comparison against Task Arithmetic and AIM (Table 4) is informative.

## Weaknesses

### Major

**1. Self-merging results lack a plausible mechanism and contain suspicious variance estimates (Section 4.1, Table 2).** The paper reports that averaging multiple posterior samples of the same model's latent code and decoding the result improves over the original model by ~4%. However:
(a) The paper offers no theoretical explanation for why averaging samples from a posterior encoding uncertainty about a *fixed* set of weights should systematically improve performance. This is not obvious.
(b) The reported standard deviations include entries of exactly 0.00 (e.g., `54.20 ± 0.00`, `50.10 ± 0.00` for the 4B model in Table 2), which are essentially impossible for a stochastic sampling process and suggest either rounding artifacts or insufficient independent trials.
Without a mechanistic understanding, these results cannot be trusted to generalize.

**2. The cross-architecture merging evidence is substantially weaker than the claims (Section 4.4, Table 5).** The paper's headline claim is enabling heterogeneous merging, yet:
(a) The "OT only" row in Table 5 *destroys* performance (WinoGrande 56.83→51.13, ARC-C 42.78→34.25), meaning the OT alignment alone is destructive rather than facilitative.
(b) The method only recovers at λ=0.1 (90% target, 10% aligned source), so the "merge" is essentially staying very close to the target with a tiny source injection.
(c) The gains over the base model are modest (WinoGrande 56.83→57.75, ARC-C 42.78→43.34) and within typical benchmark variance, with no error bars reported.
The claim of "successfully merging models with heterogeneous architectures" (Conclusion) is overstated relative to this evidence. The OT alignment appears to distort the source manifold, and the method recovers only by heavily weighting the target.

**3. Potential data leakage in expert merging from overlapping VAE training data (Section 4.2, line 153).** The VAE used for the expert merging experiments (Table 3) is trained on "pretrained weight snapshots for Gemma-3-1B-it and Gemma-3-4B-it, **plus LoRA experts from Feng et al. (2024b)**" (line 153). The LoRA experts from Feng et al. (2024b) are the same experts being merged in Table 3, meaning the VAE has been trained on the test experts. The paper evaluates generalization to unseen checkpoints in Section 5.2 (Table 7), but this is a separate experiment disconnected from the expert merging. If the expert merging results depend on in-distribution VAE training, the method's practical utility is significantly more limited than claimed.

### Minor

**4. Inconsistent evaluation frameworks across experiments.** The paper uses at least three evaluation setups: (i) the Feng et al. (2024b) subset for main merging experiments, (ii) *lm-eval* for the Task Arithmetic/AIM comparison (Section 4.3), and (iii) *lm-eval* again for cross-family evaluation (Section 4.4)—noting "some issues with llama model when using the previous evaluation code" (lines 228-229). Results across sections are not directly comparable, and the evaluation pipeline fragility is a concern.

**5. Key architectural parameters missing from the main text.** The chunk size *c*, latent dimension *d*, downsampling strategy, and a formal definition of compression ratio *r* are not provided in the main text. The symbol *r* is used throughout (Tables 7, 8) but never formally defined—it appears to be the ratio of original parameter count to latent code size, but this is not stated. These omissions hinder reproduction from the main paper.

**6. The PCA comparison does not justify the specific VAE design choices (Section 5.3).** Comparing a multi-million-parameter non-linear Transformer VAE against per-matrix PCA shows that non-linear > linear on weight data, which is unsurprising. The comparison does not justify the specific choices (transformer architecture, VAE with Gaussian prior, two-stage curriculum) over other non-linear encoders. This is better framed as a sanity check than a meaningful ablation.

**7. The OT alignment uses a Gaussian assumption that may conflict with the paper's own findings.** Section 3.3 assumes Gaussian latent distributions per layer to obtain a closed-form OT map, yet the paper itself notes that heterogeneous model latents "lie on disjoint manifolds with different covariance structures" (line 115). A Gaussian approximation implies unimodal, elliptically contoured support, which sits uneasily with the manifold claim.

### Trivial

**8. Reference to "algorithm 2" (line 145) while only Algorithm 1 appears in the main text.** Likely refers to the (stripped) appendix but is unclear in the main paper.

## Removed Points

- **"Self-merging is not a meaningful form of merging"** — subsumed into Weakness #1.
- **"Missing related works"** — removed per rule: cannot verify existence of works not cited.
- **Formatting and typo nitpicks** — removed per rule: parser artifacts, not author errors.
- **"Algorithm 1 and algorithm 2 discrepancy as a serious issue"** — downgraded to Trivial #8 since "algorithm 2" likely lives in the (stripped) appendix.
- **"The theoretical compressibility argument does not clearly connect to the VAE design"** — removed as it is a subjective judgment; the paper uses this as high-level motivation, which is reasonable for a conceptual section.

## Nice-to-Haves

- A controlled heterogeneous merging demonstration where the merge at a meaningful λ (e.g., 0.5) outperforms both the target model *and* any weight-space baseline, with error bars.
- Analysis isolating whether self-merging gains come from posterior sampling or from the VAE decoder introducing a beneficial bias (e.g., test with deterministic latent averaging vs. posterior sampling).
- Computational cost analysis (runtime, memory, FLOPs) for the encoding-decoding pipeline, which is a practical necessity for a methods paper.
- Comparison against EvolMerge or other recent methods cited in Related Work.
- A formal definition of compression ratio *r* and disclosure of chunk size *c* and latent dimension *d* in the main text.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Either drop the self-merging claims entirely or provide a controlled experiment isolating *why* posterior averaging improves performance, with proper error bars from independent trials.
2. For heterogeneous merging, either show that at λ=0.5 (equal contribution) the method outperforms the target and weight-space baselines, or substantially moderate the claims to reflect what the evidence supports.
3. Train the VAE on a held-out set of checkpoints and re-run the expert merging to control for data leakage; if performance degrades, report this honestly as a limitation.
4. Adopt a unified evaluation framework across all experiments and explain the "llama model evaluation issues" (line 229) that necessitated switching frameworks.
5. Define compression ratio *r* explicitly and report chunk size *c* and latent dimension *d* in the main text.

## Score and Decision

**Round 1 Bracket:** I determined that the paper sits between a reject (3) and a borderline reject (4), corresponding to an initial bracket of approximately 3.0–4.5.

**Anchor papers used for calibration (all retrieved from Round 1):**

| Paper | Avg Score | Decision | Comparison |
|-------|-----------|----------|------------|
| Collective Model Intelligence Requires Compatible Specialization | 3.40 | Reject | Topic (model merging limitations) is related; that paper had conceptual issues with its central claim, similar to how LS-Merge's central claim is not well-supported. LS-Merge has more experiments but its evidence gaps are more consequential for its core claims. |
| ATM: Improving Model Merging by Alternating Tuning and Merging | 3.00 | Reject | Similar model-merging topic; ATM had a stronger core insight (connecting merging to multi-task gradients) but was rejected for paradigm fit. LS-Merge's idea is more novel but evidence is weaker. |
| Few-shot Style-Conditioned LLM Text Generation via Latent Interpolation | 4.25 | Reject | **Most directly relevant anchor.** Also uses a VAE to construct a latent space of LLM weights and performs latent interpolation. Was rejected despite the novel approach, with reviewers citing insufficient experimental results to justify the VAE's computational cost. LS-Merge has broader experiments but also faces the same VAE-utility question plus additional data leakage and self-merging concerns. |
| SUPERMERGE | 4.33 | Reject | Gradient-based model merging with strong empirical results; rejected due to narrower contribution. LS-Merge is less empirically clean. |
| Extend Model Merging from Fine-Tuned to Pre-Trained LLMs via Weight Disentanglement | 5.67 | Reject | Extended merging to a genuinely harder setting (FT+PT) with clear results; was still rejected due to assumption concerns. LS-Merge has weaker evidence for its central heterogeneous-merge claim. |
| Model Merging by Uncertainty-Based Gradient Matching | 6.00 | Accept | Strong theoretical grounding linking merging to gradient mismatch, with consistent empirical improvements across LLMs and vision models. LS-Merge lacks this level of theoretical support for its core mechanism. |

**Narrowing to final score:** The two most relevant anchors—the VAE-for-LLM-weights paper (4.25, Reject) and the merging-limitations paper (3.40, Reject)—bracket LS-Merge. LS-Merge's experimental scope is broader than the 4.25 paper, but its core claims are undermined by verifiable issues (suspicious self-merging variance, data leakage, weak heterogeneous evidence) that the 4.25 paper did not have. Compared to the 3.40 paper, LS-Merge has a clearer contribution but also more fundamental evidentiary problems. The final score of 3.5 reflects a paper with genuine novelty in its approach but serious gaps between its claims and the evidence provided.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>