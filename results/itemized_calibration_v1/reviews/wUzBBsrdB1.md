Now I have a solid calibration picture. Let me finalize the review.

**Bracket determination (Round 1):** The paper sits between the 5.80 anchor ("Beyond Interpretability," which had major quantification issues and questionable baselines) and the 7.00 anchors ("Canonical Units," "Principled Evaluations"). The current paper has cleaner experiments and fewer structural issues than g6Qc3p7JH5 (5.80). It has a narrower but more focused contribution than 9ca9eHNrdH (7.00) — that paper had significant novelty/presentation weaknesses that brought it down, while the current paper's weaknesses are all minor. It is clearly below the 8.00 anchors (Sparse Feature Circuits, Scaling SAEs) which have multiple novel contributions and broader scope. **Bracket: 6.0–7.0.**

Let me publish the final review.

---

## Summary

This paper studies the effect of the L0 hyperparameter (average number of active latents per token) in Sparse Autoencoders (SAEs) for LLM interpretability. Through toy model experiments with known ground-truth features and LLM experiments on Gemma-2-2b and Llama-3.2-1b, the paper shows that (1) setting L0 too low causes SAEs to mix correlated features to improve MSE reconstruction, producing polysemantic latents; (2) the standard sparsity-reconstruction Pareto tradeoff is misleading because at low L0 an incorrect SAE can outperform a ground-truth-correct SAE on reconstruction; and (3) a metric called decoder pairwise cosine similarity (c_dec) can help detect when L0 is too low. The paper argues that most commonly used SAEs have too low an L0.

## Strengths

- **Clean toy model setup with ground-truth validation (Section 3).** The paper constructs synthetic data following the Linear Representation Hypothesis with orthogonal ground-truth features and correlated Bernoulli firing. Because true features are known, the paper can directly measure whether SAE decoder latents recover them (via cosine similarity). The result is unambiguous: at L0 = true L0, the SAE perfectly recovers features; at L0 ≠ true L0, the SAE mixes correlated features. This holds for both positive and negative correlations (Figures 2–3).

- **The demonstration that sparsity-reconstruction tradeoffs are misleading (Section 3.4, Figure 4).** By comparing a ground-truth SAE (decoder = correct features) against a trained SAE at the same L0, the paper shows that at low L0, the trained SAE achieves *better* reconstruction than the ground-truth SAE — because it cheats by mixing correlated features. This is a clean, falsifiable demonstration that the standard evaluation protocol would reject the correct solution.

- **The MSE loss analysis (Section 3.3) establishes causality, not just correlation.** At L0=5, the trained SAE achieves MSE 2.73 while the ground-truth SAE achieves MSE 4.88. This single comparison directly shows that MSE minimization is the *cause* of feature mixing at low L0, not a side effect.

- **Honest about limitations (Section 6).** The Discussion explicitly acknowledges that c_dec "can sometimes remain nearly flat for a wide range of L0" and that it is "not a perfect guide." The paper frames c_dec as a diagnostic, not a training objective or definitive solution.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **The c_dec metric requires heuristic interpretation (elbow detection) in LLMs, limiting its practical reliability.** In the toy model, c_dec has a clean minimum at the true L0 (Figure 6). But in LLM experiments, the picture is messier: for Gemma-2-2b Layer 5 (Figure 8, top-left), c_dec drops sharply at L0≈250 then remains flat over a wide range (L0≈250–2000); the "elbow" heuristic is needed rather than a principled decision rule. For Gemma-2-2b Layer 12 (Figure 9), BatchTopK and JumpReLU SAEs give different c_dec minima (≈200 vs ≈250–300). The paper is transparent about these limitations, but they mean the metric alone cannot unambiguously identify the optimal L0 without external validation (e.g., sparse probing).

- **The c_dec validation in LLMs relies on correlation with sparse probing F1, not direct evidence of feature correctness.** In toy models, the paper validates against ground-truth features. In LLMs, validation is via sparse probing performance (Figures 8–9). Sparse probing measures whether SAE latents are useful for downstream classification, which is related to but not identical to feature monosemanticity. The causal link — that low-L0 SAEs mix features and c_dec detects this — is directly demonstrated in toy models but only inferred in LLMs. The paper would be strengthened by more direct LLM evidence (e.g., showing that low-L0 latents activate on more diverse token types or score worse on automated interpretability metrics).

- **The high-L0 case is underdeveloped for LLMs.** The paper's main practical claim is about low L0 being the primary problem, which is well-supported. However, the abstract states "If L0 is too high, the SAE finds degenerate solutions that also mix features." In toy models this is clean (Section 3.2), but in LLMs the evidence is inconclusive: the c_dec flat region for Gemma-2-2b Layer 5 (Figure 8) and architecture-dependent behavior for Layer 12 (Figure 9, JumpReLU vs BatchTopK) make the high-L0 picture unclear. The paper appropriately uses hedging language ("we suspect"), but the abstract's high-L0 claim is not equally supported for LLMs.

- **The probing F1 comparison lacks error bars or significance testing.** The paper reports 3 seeds per L0 for LLM SAEs (Figure 8) but does not report whether differences in probing F1 (e.g., between L0=200 and L0=2000, a ~0.04 absolute range) are statistically significant. Since the paper's validation of c_dec depends on comparing its elbow to the probing peak, statistical uncertainty matters for this comparison.

- **The claim that "every SAE latent will contain positive components of every positively correlated feature" (line 99) may overgeneralize from the specific correlation pattern tested.** The small toy model (Section 3.1) tests a specific structure where f0 is correlated with f1–f4. While this is a clean demonstration, the claim about *every* latent and *every* correlated feature is a stronger statement than what this single correlation pattern directly shows.

### Trivial
None.

## Nice-to-Haves

- Adding error bars or confidence intervals to the probing F1 plots (Figure 8) would clarify whether the observed differences are statistically significant.
- Supplementing the c_dec validation in LLMs with feature-level evidence (e.g., activation diversity across token types, automated interpretability scores) would bridge the toy-LLM gap more convincingly.
- A principled decision rule for c_dec (e.g., derivative-based threshold or margin-based criterion) would increase its practical utility beyond visual elbow detection.
- Either softening the abstract's high-L0 claim ("degenerate solutions that also mix features") to reflect LLM-level uncertainty, or adding stronger LLM evidence for the high-L0 case.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Criticism about the Neuronpedia survey methodology not being described in the main text.** The paper references Appendix A.13 for this survey. The appendix was stripped by the parser; it exists in the original submission. Per guidelines, this criticism is removed.
- **Criticism that the toy model correlation structure is "artificial."** This is a nice-to-have suggestion (naturalistic correlations from LLMs) rather than a genuine weakness, as the paper explicitly uses a controlled toy model to demonstrate a principle.
- **Criticism that c_dec requires training a sweep over L0, which is expensive.** The paper explicitly acknowledges this limitation and discusses future work (Appendix A.11). This is a recognized limitation, not an overlooked one.
- **Claim that validation of c_dec is "partially circular."** This is not supported by the paper: the toy model validation uses ground-truth features (not circular), and the LLM validation uses sparse probing as an independent external benchmark.
- **Demand for theoretical analysis incorporating non-orthogonal/non-linear features.** The paper is an empirical analysis operating within the LRH framework; demanding it handle non-linear features is scope creep beyond what any current SAE analysis addresses.

## Novel Insights

The paper's most novel insight is the demonstration that the standard sparsity-reconstruction Pareto front, which the field uses to compare SAE architectures, is not just imperfect but positively misleading: it would rank an incorrect SAE above a ground-truth-correct one at the same low L0. This reframes L0 from a free hyperparameter to a critical parameter that must be matched to the data's intrinsic sparsity. The c_dec metric, while heuristic in practice, provides a principled justification (orthogonal decoder directions indicate disentangled features) for a diagnostic the field previously lacked.

## Suggestions

- Add error bars or confidence intervals to the probing F1 plots (Figure 8) to clarify whether the observed differences are statistically significant.
- Either soften the abstract's high-L0 claim or add stronger LLM evidence.
- Provide at least one feature-level analysis for LLM SAEs (e.g., measuring whether low-L0 latents activate on more diverse inputs) to complement the sparse probing validation.

---

**Calibration summary:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| (Low-quality unrelated) | nSDOkm0SKo.md | 1.00 | 1 | No | Unrelated paper (finance), not comparable |
| (Low-quality unrelated) | gwZ90hFSL2.md | 1.00 | 1 | No | Unrelated (humanoid robots), not comparable |
| Scaling and evaluating SAEs | tcsZt9ZNKD.md | 8.20 | 1 | Yes | Much broader contribution (architecture + scaling laws + evaluation); current paper is narrower and more focused, below this |
| Sparse Feature Circuits | I4e82CIDxv.md | 8.00 | 1 | Yes | Complete pipeline with multiple novel components; current paper is below this |
| SAEs Do Not Find Canonical Units | 9ca9eHNrdH.md | 7.00 | 1 | Yes | Similar critical-analytical framing; current paper has cleaner presentation and fewer structural weaknesses |
| Principled Evaluations of SAEs | 1Njl73JKjB.md | 7.00 | 1 | Yes | Similar depth and rigor; current paper has a broader validation (toy + LLMs) vs single-task IOI focus |
| Beyond Interpretability (monosemanticity) | g6Qc3p7JH5.md | 5.80 | 1 | Yes | Weaker quantification of core concept; current paper's experiments are cleaner and claims better supported |
| Compute Optimal Inference (amortization gap) | ghH6YYDs15.md | 4.67 | 1 | Yes | Narrow theoretical results on synthetic data; current paper has more comprehensive empirical validation |

**Score determination:** The paper's clean toy-model demonstration of why low L0 causes feature mixing and its critique of sparsity-reconstruction tradeoffs are its strongest contributions — comparable in rigor to the 7.00 anchors. The weaknesses (c_dec heuristic in LLMs, underdeveloped high-L0 case, missing error bars on probing) are all minor and do not threaten the core claims. The paper is clearly above 5.80 (Beyond Interpretability), which had more significant quantification issues. It is below 8.00 (Sparse Feature Circuits), which has a complete pipeline with multiple novel components. Within the 6.0–7.0 bracket, the paper's clarity and well-demonstrated core insight place it at **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>