## Summary

This paper studies how the L0 sparsity hyperparameter affects feature quality in Sparse Autoencoders (SAEs) for LLM interpretability. Using toy models with known ground-truth features, the authors demonstrate that setting L0 too low causes SAEs to "cheat" by mixing correlated features together (improving MSE while corrupting feature monosemanticity), and that sparsity-reconstruction tradeoff plots can be misleading. They propose a decoder pairwise cosine similarity metric (c_dec) for detecting when L0 is too low, and validate it on Gemma-2-2b and Llama-3.2-1b. The core insight — that low L0 SAEs sacrifice feature correctness for reconstruction — is an important practical contribution.

## Strengths

- **Clean toy-model demonstration (Section 3, Figs 2–5) that low L0 causes feature mixing, with ground-truth verification.** The experiment where a trained low-L0 SAE achieves MSE 2.73 while the ground-truth SAE achieves 4.88 (Section 3.3) is particularly compelling: it shows that MSE loss actively incentivizes the SAE to learn incorrect, mixed latents rather than the true features. This is the paper's strongest and most original contribution.

- **Shows that sparsity–reconstruction tradeoff plots can be misleading (Section 3.4, Fig 4).** A ground-truth SAE with correct latents scores *worse* on variance explained than a trained SAE that mixes features, when both are evaluated below the true L0. This provides an important caution for the standard SAE evaluation methodology, which implicitly assumes that better reconstruction at a given sparsity level indicates a better SAE.

- **Validates findings on real LLMs with downstream sparse probing (Section 4, Figs 8–9).** The sharp rise in c_dec at low L0 coincides with degraded k-sparse probing performance on Gemma-2-2b and Llama-3.2-1b, providing evidence that the toy-model phenomenon generalizes beyond synthetic data. The inclusion of both BatchTopK and JumpReLU SAEs strengthens the analysis.

- **Honest and circumspect discussion of the metric's limitations (Section 6).** The paper acknowledges that c_dec "is not a perfect guide" and "can sometimes remain nearly flat for a wide range of L0." This candor is appreciated and should be retained.

## Weaknesses

### Fatal

None.

### Major

- **Framing overstates the existence of a single "correct L0" for real LLMs.** The abstract and paper frame the problem as finding *the* correct L0 for a given layer ("L0 must be set correctly for SAEs to learn correct features"). Yet Section 4.2's own evidence shows that different latents in the same SAE have different optimal firing rates: "L0 is too high for some latents while simultaneously being too low for other latents." The toy model's clean threshold (where all features fire with similar probability, p_i=0.4) has no clear analog in real LLM activations where feature sparsity varies widely across latents. The paper would be more accurate framing c_dec as detecting when L0 is *too low* (which it does robustly) rather than claiming it identifies a uniquely correct L0. The paper partially addresses this in Section 4.2 but does not reconcile it with the abstract's stronger claims.

- **The claim that "most commonly used SAEs have an L0 that is too low" (abstract, Section 6) lacks sufficient support.** The paper references only "a cursory search of open source SAEs on Neuronpedia" (Appendix A.13, not in the provided text) with no quantification, no comparison to the optimal L0 found by c_dec for those specific models, and no analysis of how optimal L0 varies with model size, layer depth, or SAE width. Given that the paper's own results show optimal L0 varies between models (Gemma vs Llama) and between layers of the same model (layer 5 vs layer 12), this headline claim needs stronger evidence. This is a secondary contribution to the paper's core argument but features prominently in the abstract.

### Minor

- **The c_dec metric requires different interpretive heuristics across settings.** For Llama-3.2-1b, c_dec has a clear global minimum at L0≈250. For Gemma-2-2b layer 5, c_dec drops sharply then remains flat from L0≈250–2000, so the paper reads the "elbow" rather than the minimum. For Gemma layer 12, BatchTopK and JumpReLU SAEs give different minima (~200 vs 250–300). The reliance on a visual "elbow" heuristic rather than a principled criterion weakens c_dec as a general-purpose diagnostic, though the paper acknowledges these ambiguities.

- **No quantitative comparison between the L0 that optimizes c_dec and the L0 that optimizes sparse probing F1.** The paper says they "coincide" (Section 4) but provides only a qualitative visual assessment. For Gemma layer 12 (Fig 9), the BatchTopK c_dec minimum is at L0≈200 while peak probing appears closer to L0≈500–1000. Providing numerical comparisons (e.g., the L0 that minimizes c_dec vs the L0 that maximizes probing F1 for each setting) would strengthen the claim substantially.

- **No analysis of how SAE width interacts with L0.** The paper uses h=32768 throughout but does not vary width. Prior work shows width affects feature splitting and absorption, and wider SAEs may tolerate low L0 differently. This limits the generality of the findings.

- **The toy model uses perfectly orthogonal feature directions (f_i·f_j=0), while the LRH posits "nearly orthogonal" features.** The paper does not discuss how small non-zero cosine similarities between underlying feature directions would affect the c_dec metric's ability to identify the correct L0. (Appendix A.6 may provide theoretical justification, but this is not in the main text.)

- **Limited model coverage.** Only two models (Gemma-2-2b, Llama-3.2-1b) and a few layers are tested. While computationally understandable, this limits the generality of claims about how L0 affects SAE features across different model families and scales.

### Trivial

None.

## Nice-to-Haves

- Show concrete examples of LLM SAE latents that appear monosemantic at the "correct" L0 and polysemantic (feature-mixed) at low L0, similar to the toy-model analysis. The decoder projection histograms (Fig 9, right) are a step in this direction but do not isolate individual latents.
- Test more diverse correlation structures in the toy model beyond the simple star-shaped correlation pattern used in the 5-feature experiment (e.g., clusters, hierarchies, chains).
- Consider varying SAE width to explore whether wider SAEs can tolerate lower L0.

## Removed Points

These points from the input review were flagged for removal:

1. **"No analysis of feature-level effects in LLM SAEs"** — Moved to Nice-to-Haves. The paper does show decoder projection histograms and aggregate metrics for LLMs; a full feature-level analysis would strengthen the paper but is not a core weakness given the difficulty of ground-truth identification in real models.

2. **"BatchTopK and JumpReLU SAEs give different c_dec minima"** — Incorporated into the Minor weakness about interpretive heuristics. The paper explicitly reports and discusses this discrepancy; presenting it as an independent weakness would be redundant.

3. **"The concept of a single correct L0 for real LLMs is not well-defined" merged into Major weakness #1** — Restructured: the framing criticism is correct, but the paper partially addresses it in Section 4.2, so the merged version acknowledges the partial addressal.

4. **Generic "Strengthening the Paper" suggestions (broaden toy model, reframe claims)** — Moved to Nice-to-Haves and Suggestions, respectively. These are forward-looking improvements, not weaknesses in the current submission.

5. **"Section-by-section notes" about JumpReLU sticking behavior and related work** — These are observations, not weaknesses. The JumpReLU observation is actually a finding the paper reports.

6. **Various speculative claims about missing appendix content** — Removed per Hard Rules (parser strips appendices from all papers).

## Novel Insights

None beyond the paper's own contributions. The key insight — that low L0 causes SAEs to mix correlated features for better reconstruction at the expense of feature correctness, and that this can be detected via decoder pairwise cosine similarity — is well-articulated by the paper itself.

## Suggestions

1. **Reframe the core claim.** Replace the framing around a single "correct L0" for real LLMs with the well-supported finding that *low L0 uniformly degrades feature quality*. The c_dec metric is most reliable on the low-L0 side (sharp rise), and this is where it provides genuine practical value. The paper should be explicit that the "correct L0" in a real LLM is likely a range, not a single value — consistent with the Section 4.2 findings.

2. **Provide numerical comparisons** between c_dec-optimal L0 and probing-optimal L0 for all tested settings. At minimum, report the L0 value that minimizes c_dec and the L0 value that maximizes k-sparse probing F1 for each model/layer/architecture combination.

3. **Either remove or substantially strengthen the "most SAEs have too low L0" claim.** If retained, provide a systematic comparison rather than a "cursory search," and acknowledge the variation across models and layers documented in the paper itself.

## Score and Decision

**Round 1 bracket (initial bracketing):** The paper sits between the "Compute Optimal Inference" anchor (avg 4.67, Reject) and the "Sparse Autoencoders Do Not Find Canonical Units of Analysis" anchor (avg 7.00, Accept). Its strengths on toy-model experiments and sparsity-reconstruction critique are comparable to the 7.00 anchor, but its two major weaknesses (framing overclaim and unsupported headline claim) are more substantial than any weakness in that anchor. Its weaknesses are less severe than the theoretical and citation gaps that pulled the 4.67 anchor down.

**Round 2 narrowing:** Comparing itemized favorability ratings: the canonical-units anchor's lowest weakness favorabilities are 1.83–5.33 (all minor/trivial), while this paper has two weaknesses at 0.08 and -1.12. This gap accounts for roughly 1 point of score difference. The compute-optimal anchor's lowest weakness favorabilities are -3.40 and -2.92 (severe), placing this paper comfortably above that anchor.

**Final score: 6.0.** The paper makes a genuine and important empirical contribution (the toy-model demonstration is clean, the sparsity-reconstruction critique is well-targeted), but it needs to recalibrate its claims in the abstract and discussion to match what the evidence actually supports.

**Anchors retrieved across rounds:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| canonical-units (9ca9eHNrdH) | 7.00 | R1+R2 | Yes | Stronger: no major framing weaknesses, clearer claims |
| principled-evals (1Njl73JKjB) | 7.00 | R1+R2 | Yes | Stronger: more rigorous evaluation framework, clearer scope |
| compute-optimal SAE (ghH6YYDs15) | 4.67 | R2 | Yes | Weaker: theoretical issues, limited real-model experiments |
| Cunningham SAE (F76bwRSLeK) | 4.80 | R1+R2 | Yes | Comparable overall quality but different contribution type |
| multi-layer SAE (XAjfjizaKs) | 6.50 | R2 | No | Similar tier but different topic |
| permutability (MDvecs7EvO) | 6.50 | R2 | No | Similar tier but different topic |

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>