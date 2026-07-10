Now I have all the information I need. Let me produce the final consolidated review.

---

## Summary

This paper studies the effect of the L0 hyperparameter on SAE feature quality. Using toy models with known ground-truth features, it shows that when L0 is too low, SAEs mix correlated features to improve reconstruction (feature hedging); when L0 is too high, they also find degenerate mixed solutions. The paper demonstrates that the widely-used sparsity-reconstruction tradeoff is actively misleading — a corrupted low-L0 SAE can achieve *better* reconstruction than a ground-truth SAE. It proposes decoder pairwise cosine similarity (c_dec) as a diagnostic to detect when L0 is too low, validating it on toy models and two real LLMs (Gemma-2-2b, Llama-3.2-1b) with sparse probing.

## Strengths

- **Clean demonstration that low L0 causes feature mixing in toy models (Sections 3.1–3.2).** The experimental design is thoughtful: a minimal 5-feature setup with controlled positive/negative correlations, scaling to a 50-feature model with a random correlation matrix, and initializing the under-capacity SAE from the ground-truth solution to rule out local-minimum arguments. Both correlation cases cleanly show the same pattern — the SAE mixes correlated features into latents when L0 is too low.

- **Important critique of the sparsity-reconstruction tradeoff (Section 3.4, Figure 4).** Figure 4 shows that at low L0, a trained SAE with corrupted latents achieves *better* reconstruction than the ground-truth SAE. This demonstrates that the primary metric used to compare SAE architectures is, in a well-defined regime, inverted relative to feature quality — a finding that should give the field pause.

- **c_dec is well-motivated (Section 3.5).** The intuition — that SAE latents containing mixtures of multiple features should be less orthogonal on average — is sound. The toy model validation (Figure 6) showing c_dec minimized at the true L0 across 5 seeds is clean.

- **Validation on two real LLMs with a meaningful external benchmark (Figure 8).** The correspondence between the c_dec "elbow" and peak sparse probing performance on Gemma-2-2b and Llama-3.2-1b provides external validation beyond reconstruction metrics.

- **Honest about limitations.** Section 6 acknowledges that c_dec can remain flat over wide L0 ranges and currently requires a sweep. Section 4.2's observation that L0 can be simultaneously "too high for some latents while too low for others" is a nuanced point that the paper discusses in good faith.

## Weaknesses

### Fatal

None.

### Major

- **The claim that "most commonly used SAEs have an L0 that is too low" (abstract, Section 6, conclusion) is supported only by a "cursory search of open source SAEs on Neuronpedia."** The paper's own wording acknowledges this is not a rigorous analysis, yet the abstract presents it as a definitive finding: "We find that most commonly used SAEs have an L0 that is too low." A systematic survey and evidence that these SAEs would benefit from higher L0 (e.g., improved downstream performance) would be needed to support this claim. This overclaim is the paper's most significant weakness, as it appears in the abstract and conclusion.

### Minor

- **The c_dec metric's LLM validation is weaker than the paper's aspirational framing.** For Gemma-2-2b Layer 5 (Figure 8, top-left), c_dec drops sharply then is essentially flat from L0≈250 to L0≈2000, showing no clear valley. The metric primarily rules out *very low* L0 rather than identifying a unique optimal value. The paper's Figure 8 caption and Section 6 appropriately note this limitation, but the abstract's phrasing ("our method finds the correct L0... and coincides with peak sparse probing performance") is slightly more optimistic than the evidence supports. The Llama-3.2-1b result (top-right) is cleaner and supports the metric better.

- **The toy model experiments cover a limited set of correlation structures.** The 5-feature model uses a single pattern (one feature correlated/anti-correlated with all others) and the 50-feature model uses one randomly generated correlation matrix. Real LLM feature correlations are likely more complex (hierarchical, overlapping groups, non-stationary). Since the paper's central mechanism relies on feature correlations, a broader exploration would strengthen confidence that the findings generalize.

- **The key MSE comparison in Section 3.3 (trained SAE MSE=2.73 vs ground-truth SAE MSE=4.88) is reported without variance across seeds or correlation structures.** While illustrative, the robustness of this inversion — central to the sparsity-reconstruction critique — would be strengthened by showing it holds across multiple random seeds and correlation matrices.

### Trivial

None.

## Nice-to-Haves

- A direct measure of feature monosemanticity on real LLMs (e.g., auto-interp scores) at different L0 values would strengthen the empirical case beyond sparse probing, though this is beyond the paper's stated scope.
- An exploration of how the degree of feature correlation affects the severity of mixing (varying correlation strength systematically) would make the toy-model mechanism more concrete.

## Removed Points

These points were considered but removed as they either restate limitations the paper already acknowledges, misunderstand the paper, or constitute scope creep:

- *"The notion of 'true L0' for real LLMs is philosophically underspecified"* — The paper explicitly acknowledges this in Section 3 ("In a real LLM, we do not have ground-truth knowledge of the 'true features'...") and frames LLM results as a heuristic validated by sparse probing, not as identifying a Platonic true L0.
- *"Section 4.2 undermines the paper's thesis about a single correct L0"* — The paper directly discusses this as an interesting nuance and frames it as a limitation of global L0, not as contradictory to its findings.
- *"JumpReLU 'sticking' mechanism unexplained"* — The paper attributes this to the cited training method (Conerly et al., 2025); explaining the training method in detail is outside the paper's scope.
- *Formatting artifacts, style nitpicks, missing appendix content* — These are parser artifacts, not author errors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- **Reframe the abstract claim about "most commonly used SAEs."** Replace "We find that most commonly used SAEs have an L0 that is too low" with a more measured statement such as "A cursory survey suggests that many commonly used SAEs operate at L0 values where our analysis predicts feature mixing may occur." This would align the paper's claims with its evidence.
- **Add variance reporting for the MSE comparison in Section 3.3** across multiple seeds to confirm the sparsity-reconstruction inversion is robust.
- **Consider exploring additional correlation structures** (e.g., hierarchical, group-structured) in the toy model to test the generality of the mechanism.
- **Tone down the "finds the correct L0" framing for LLM results** in the abstract to better match the evidence, which primarily supports c_dec as a tool for ruling out very low L0.

---

## Score and Decision

**Round 1 bracket: 5.5 – 7.5**

I place this paper at **6.0** based on comparison with calibration anchors:

| Anchor Paper | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|
| Sparse Autoencoders Find Highly Interpretable Features | 4.80 | R1 | Yes | Weaker overall; had more severe weaknesses (novelty concerns, -4.87 favorability item). Our paper has cleaner experiments and more honest limitations. |
| Interpreting and Steering LLM Representations | 5.00 | R2 | Yes | Comparable scope but our paper's core empirical contribution is stronger; our weaknesses are milder (min -0.99 vs -4.79). |
| Mechanistic Permutability: Match Features Across Layers | 6.50 | R1 | Yes | Proposes novel method (SAE Match); our paper's empirical critique is solid but less of a technical contribution. Comparable favorability on weakness severity. |
| Residual Stream Analysis with Multi-Layer SAEs | 6.50 | R2 | No | Proposes novel MLSAE architecture; similar empirical rigor. Our paper has similar strength on toy-model evidence but less novelty. |
| Sparse Autoencoders Do Not Find Canonical Units | 7.00 | R1 | Yes | Proposes two novel techniques (stitching, meta-SAEs) plus BatchTopK. Our paper's single c_dec metric is less novel, though our sparsity-reconstruction critique is a significant finding. |
| Towards Principled Evaluations of SAEs | 7.00 | R1 | Yes | Proposes a novel evaluation framework with supervised dictionaries. Our paper has cleaner toy-model evidence but less methodological novelty. |

**Grounding in favorability comparison:** My paper's strongest items (real LLM validation at 13.86, experimental design at 13.28) are comparable to the 7.0 anchors' strongest items. However, my paper's weakest item (-0.99 for the overclaimed "most SAEs" finding) is milder than the 7.0 anchors' weakest items (around -2.8 to -3.9), yet those papers contribute novel methods rather than primarily empirical analysis. The paper makes a genuine and timely contribution — particularly the sparsity-reconstruction tradeoff critique — but the overclaim about "most commonly used SAEs" and the limited LLM validation of c_dec prevent it from reaching strong-accept territory. A score of 6.0 reflects a solid borderline-accept paper with real merit and addressable weaknesses.

**Final Score: 6.0 — Accept (borderline)**

**Key reason:** The toy-model demonstration that low L0 corrupts features and that the sparsity-reconstruction tradeoff is misleading is a significant, well-executed empirical contribution. The main reservation is that the paper overclaims in the abstract ("most commonly used SAEs have an L0 that is too low" supported only by a cursory search) and slightly overstates c_dec's precision on real LLMs. These are addressable in revision and do not undermine the core contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>