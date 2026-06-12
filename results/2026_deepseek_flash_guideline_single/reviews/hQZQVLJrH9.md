Now I have sufficient calibration. Let me finalize the review.

## Summary

This paper proves that activation steering and influence functions — previously treated as separate toolkits — are, to first order, dual views of the same sensitivity tensor. It establishes a closed-form map between steering vectors and signed training-data influences (Theorem 4.2), derives an alignment diagnostic γ that quantifies when steering can substitute for influence (Theorems 5.1, 6.2), proves spectral optimality for steering under an ℓ₂ budget (Theorem 5.3), and provides Rademacher-complexity bounds for low-rank steering (Theorem 6.1). Experiments on GPT-2 Medium and ResNet-50 test the theoretical predictions and compare the proposed Influence-Aligned Steering (IAS) against baselines.

## Strengths

1. **Genuinely novel theoretical bridge between two disconnected literatures.** The primal-dual framing (Section 3) and the constructive equivalence (Theorem 4.2) provide the first closed-form map between activation steering and influence functions. This is not an incremental result — it reorganizes how practitioners can reason about both methods within a single, principled framework.

2. **The γ(x) alignment diagnostic (Theorem 5.1, Theorem 6.2).** The bound √(1-γ²) on the relative logit error of steering vs. influence is tight, computable (two small SVDs), and directly actionable. The no-free-lunch theorem (6.2) is a clean negative result: when γ is small, the geometry itself prevents steering from fully substituting for influence. This would be useful as a standalone contribution.

3. **Spectral optimality result (Theorem 5.3).** Deriving the top eigenvector of a Fisher-influence matrix as the principled steering direction under a norm budget replaces hand-crafted heuristic directions with a theoretically grounded construction.

4. **Generalization bounds for low-rank steering (Section 6).** The Rademacher-complexity analysis showing excess risk vanishes as O(√(k/dn)) is a non-trivial addition that goes beyond what typical steering papers offer, connecting the framework to learning theory.

## Weaknesses

### Fatal
None.

### Major

1. **The claimed data-provenance workflow is asserted but entirely untested.** The paper states that ρₛ "points straight to the *most causal* training documents" (Section 4) and that it "pinpoints the *fewest* training examples to relabel/remove/examine to reproduce the behavioral change (see Section 7)" (Section 4.1, after Corollary 1). Yet the experiments contain **zero validation** of this central practical payoff: no experiment constructs a steering vector, identifies top-weighted training examples via ρₛ, and verifies (via human evaluation, leave-one-out retraining, or any other quantitative method) that those examples are causally related to the steered behavior. Section 7 does not contain any such experiment. While the core theoretical duality does not depend on this validation, the gap between the paper's own stated Contribution #4 and the provided evidence is substantial.

2. **The systematic slope miscalibration in Figure 1 (slope 1.50 vs. predicted 1.0) is reported without comment.** The first-order theory predicts that the logit shift from an influence update is matched by the minimum-norm IAS vector, implying an identity relationship (slope ≈ 1.0). Figure 1 shows a slope of 1.50 — realized logit shifts are systematically ~50% larger than predicted. The high cosine (0.978) validates directional alignment, but the magnitude discrepancy is non-negligible. The paper states this is "consistent with the expected linear regime" without any analysis of the cause (second-order effects? finite step size? implementation artifact?), whether it can be calibrated, or what it implies for the theory's predictive accuracy. Because the entire framework is built on first-order reasoning, this unexplained discrepancy weakens the empirical support considerably.

### Minor

3. **IAS underperforms the simpler CAA baseline on the only head-to-head comparison (Table 1).** IAS yields higher toxicity (0.0164 vs 0.0150) and higher perplexity (13701 vs 13291) than CAA. The paper reports this without discussion. The Introduction frames IAS as a principled alternative that overcomes "experiment[ing] blindly with steering"; the comparison results therefore deserve at least a brief analysis. The paper should explain whether this is theoretically expected (e.g., influence matching in logit space does not align with the detoxification objective) or reflects an implementation limitation.

4. **The spectral optimality experiment (Figure 3, ResNet-50) shows significance but not utility.** The spectral direction produces a logit change that is statistically significant compared to random directions (p=0.00498). However: (a) "better than random" is a low bar for a principled method; (b) no comparison to any baseline steering method (e.g., gradient ascent, class-specific Jacobian, or a simple heuristic) is provided; (c) no actual downstream steering result (classification accuracy after steering, magnitude of achieved logit change) is reported. The reader cannot assess whether the spectral recipe is practically useful.

5. **The infinitesimal regime vs. practical finite perturbations is not characterized.** The entire theory assumes α ≪ 1 and ε ≪ 1, but experiments use unspecified finite magnitudes. No analysis or sweep over α is provided to characterize where the first-order approximation breaks down. The paper acknowledges this in the conclusion but provides no guidance on the boundary.

6. **The γ=0.5 threshold for "skip steering" (Section 6) appears arbitrary.** At γ=0.5, the relative error bound from Theorem 5.1 is √(1-0.25) ≈ 0.87, i.e., up to 87% relative error. The paper recommends "when γ < 0.5, skip steering" without justifying why 87% potential error is the cutoff rather than, say, γ=0.7 (≈71% error) or γ=0.9 (≈44% error). A principled criterion for choosing this threshold would strengthen the practical guidance.

### Trivial
None.

## Nice-to-Haves

- Validate the steering→training-data mapping empirically: construct a steering vector for a known behavior, compute ρₛ, inspect the top-weighted training examples, and verify causal relevance (the paper's own stated workflow).
- Explain or resolve the slope discrepancy in Figure 1, e.g., by identifying whether it comes from second-order effects, finite step size, or an implementation issue.
- Add standard errors, confidence intervals, or significance tests to all experimental results.
- Characterize the relationship between steering magnitude α and deviation from first-order linearity via a sweep over α.
- Describe the CAA baseline implementation to enable fair comparison assessment.
- Add a non-random baseline to the spectral optimality experiment.
- Clearly differentiate the "two backward passes" cost model: it applies to computing IAS for a given Δθ; the spectral direction (Theorem 5.3) requires power iteration over data.

## Removed Points

- **Introduction framing overstated (Section 1, lines 19–20).** Subjective opinion about rhetorical framing; not a substantive weakness. **REMOVED.**
- **Equation (2) formatting issue (Section 3.2, line 84).** Likely a PDF-parser artifact; the mathematical content is clear from context. **REMOVED.**
- **Feasibility assumption (Section 2, line 44) criticized as "strong."** The paper immediately provides the γ diagnostic to quantify when it holds and the error bound when it does not; the assumption is explicitly scoped as "when stated." **REMOVED** (addressed by the paper).
- **"No variance or confidence intervals reported."** While true, single-run evaluation on 500 prompts is standard in this literature. Demoted to Nice-to-Have.
- **"Two backward passes" claim vs spectral optimality cost.** The claim is correctly scoped to computing IAS, not the spectral direction; the differentiation could be clearer. Demoted to Nice-to-Have.
- **"Missing related works."** Cannot be independently verified; removed per instructions.

## Novel Insights

The harsh critic's key insight is that the paper's most distinctive claimed application — mapping steering vectors back to causal training examples — is entirely untested, and the slope miscalibration (1.50 vs 1.0) in the central empirical validation of the first-order theory is unexplained. These two gaps form a symmetric pair: the *forward* direction (steering matching influence) has a magnitude discrepancy that goes unanalyzed, and the *backward* direction (influence tracing back to training data) has no empirical demonstration at all. Together, they mean the empirical package does not substantiate the paper's own stated contributions, even though the core theoretical framework is sound and novel.

## Suggestions

1. Add an experiment validating the steering→training-data mapping — the paper's signature practical claim.
2. Explain or resolve the slope discrepancy in Figure 1.
3. Discuss why IAS underperforms CAA in detoxification and whether this is theoretically expected.
4. Add a non-random baseline to the spectral optimality experiment.
5. Provide a sensitivity analysis over α to characterize the first-order approximation's operating regime.

---

### Calibration Report

**Round 1 — Bracketing:** Searched the human-review corpus across six score bands (1.5–11.0) with queries related to activation steering, influence functions, duality, and theory papers.

**Anchors retrieved:**
- **z1yI8uoVU3** — "Measuring Effects of Steered Representation in LLMs" (avg 3.0, Reject). Empirical evaluation paper with limited novelty. Our paper is clearly stronger (more novel theory).
- **2XBPdPIcFK** — "Steering Language Models with Activation Engineering" (ActAdd) (avg 5.0, Reject). Pioneering but simple method paper. Our paper has substantially stronger theoretical depth.
- **9wjGUN65tY** — "Steering Vectors to Conceptors" (avg 5.0, Reject). Theory+empirical on conceptor-based steering. Our paper has cleaner mathematics and more novel duality result.
- **KjBG4JNOc2** — "Enhancing Training Robustness through Influence Measure" (avg 6.2, Accept). Applied influence functions with good experiments but limited theory. Our paper has stronger theory but weaker experiments.
- **dTQmayPKMs** — "Understanding Impact of Human Feedback via Influence Functions" (avg 6.33, Reject). Applied influence functions to RLHF with good experiments; rejected for limited novelty. Our paper has stronger novelty but weaker experiments.
- **wozhdnRCtw** — "Improving Instruction-Following in Language Models through Activation Steering" (avg 7.0, Accept). Strong empirical paper with clear experiments. Our paper has weaker experiments but stronger theory.

**Round-1 bracket:** [5.5, 6.5]

**Final calibration:** Compared against the Conceptors paper (5.0, Reject) — our paper has better theoretical novelty and cleaner presentation. Compared against the influence function application papers (6.2, Accept; 6.33, Reject) — our paper has stronger theory but notably weaker experimental validation of its own claims. The instructions-following paper (7.0, Accept) sets an upper bound on experiments that our paper does not reach. The final score of **6.0** reflects a paper with a genuinely novel theoretical core that is not fully matched by its experimental package — the theory warrants acceptance, but the two major gaps (untested data-provenance claim, unexplained slope) are significant enough to hold the score below the 6.5+ range that would indicate a cleanly strong paper.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>