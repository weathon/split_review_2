Now let me write the final review.

## Summary

This paper studies gradient flow dynamics of a broad class of neural networks, analyzing embedded fixed points (Theorem 1), invariant manifolds (Theorem 3), and two distinct timescale separation mechanisms that produce saddle-to-saddle dynamics — data-driven in linear networks (Theorem 4) and initialization-driven in quadratic networks (Proposition 5). The framework makes testable predictions about how width, data distribution, and initialization affect learning.

## Strengths

- **Extension of embedded fixed point theory (Theorem 1, Eqs 6–7).** Prior work (Fukumizu & Amari, 2000) gave two constructions for embedding fixed points of narrow networks into wider networks. This paper adds two new constructions — Eq 6 for homogeneous activations (e.g., ReLU) and Eq 7 for linear/additive activations — and argues that the saddles visited during learning fall under Eqs 5–7 rather than Eq 4. This is a concrete theoretical advance relevant to dynamics, not just landscape characterization.

- **Invariant manifold characterization (Theorem 3).** Going from fixed points to invariant manifolds preserved under gradient flow is non-trivial. The four cases (equal weights, zero weights, proportional weights, linear dependence) correspond to the fixed point constructions in Theorem 1, giving a coherent geometric picture. The insight that these manifolds make networks "effectively narrower" provides a clean link between geometric structure and functional simplicity.

- **Distinction between two mechanisms for timescale separation (Sec 5.1 vs 5.2).** The paper identifies two genuinely distinct mechanisms: data-driven timescale separation from the singular value spectrum of Σ_yz (producing low-rank weights) versus initialization-driven timescale separation from differences in unit initializations (producing sparse weights). This is the paper's most original conceptual contribution and clarifies why plateau structure depends on data distribution in one architecture but not another.

- **Testable, non-trivial predictions (Section 6).** Predictions about width having no effect in linear networks but shortening plateaus in self-attention, and about power-law data exponents eliminating plateaus in linear but not quadratic networks, are specific and falsifiable.

- **Honest about limitations.** Section 7 explicitly states that the dynamics analysis "only applies to two-layer networks," acknowledges fixed points may not be exhaustive, and frames claims about deep networks as conjectures.

## Weaknesses

### Fatal
None.

### Major

- **Framing-to-evidence gap: the title, abstract, and introduction claim a "universal mechanism" but the dynamics analysis is limited to two specific two-layer cases.** The paper claims to explain simplicity bias "across neural network architectures" with a "universal mechanism." However, Theorem 4 (timescale separation between directions) is proven only for *linear* two-layer networks (Eq 8), and Proposition 5 (timescale separation between units) is proven only for *quadratic* two-layer networks (Eq 13). For ReLU networks, convolutional networks, and attention architectures, the paper shows they *exhibit* stage-like behavior (Figure 1) and that the landscape structure (Theorems 1, 3) applies, but it never establishes that the proposed mechanism (timescale separation → invariant manifold following → saddle-to-saddle dynamics) actually *causes* their dynamics. The discussion of "general nonlinear activation" (end of Section 5.2) is heuristic — it Taylor-expands around zero and immediately notes that tanh fails to produce saddle-to-saddle dynamics. The paper's own Section 7 concedes that "the analysis of dynamics in Section 5 only applies to two-layer networks." The landscape results (Theorems 1, 3) are necessary but not sufficient for the dynamical claims. This mismatch between the broad framing and the narrow technical scope is the paper's most significant weakness.

- **Experiments are illustrative rather than confirmatory.** (a) No error bars or multiple runs are reported for any simulation; given stochastic initialization (especially for Proposition 5 where the largest-initialization unit matters), variance across runs is expected to be significant. (b) There is no quantitative testing of the mechanism — e.g., measuring the relationship between singular value ratios and plateau durations in linear networks, or verifying that the unit with the largest initialization grows first in quadratic networks. (c) For ReLU networks, the paper claims they follow the homogeneous-case mechanism (Eq 6, proportional weights), but it never verifies empirically that the weights during plateaus are actually proportional — it only shows that loss curves have plateaus.

### Minor

- **Figure-reference typo.** Line 99 states that panels (E,F) correspond to Equation (5), but the figure caption assigns panels F and G to Equation (5) ("The weight structures in BC, DE, and FG correspond to three categories"). The text should reference (F,G) rather than (E,F).

- **The "carefully chosen small perturbation" (Section 4) carries conceptually heavy weight.** The paper argues that to move between invariant manifolds "we may apply a carefully chosen small perturbation that moves the weights onto the invariant manifold with effective width (h+1)." The paper's connection between landscape structure and dynamics relies on this step being taken *spontaneously* by gradient flow, but the mechanism by which this occurs is only heuristically justified even for the tractable linear/quadratic cases.

### Trivial
None.

## Nice-to-Haves

- Add error bars or multi-seed visualizations for at least the key simulations (Figures 1, 2).
- Validate the mechanism quantitatively in the linear case: measure singular value ratios of Σ_yz, compute predicted plateau durations from Theorem 4, compare against actual durations.
- For ReLU networks, verify empirically that weights during plateaus are approximately proportional (consistent with Eq 6).

## Removed Points

- **Criticisms about missing experimental details (data distribution, learning rate, optimizer choices, training details):** The paper states "Experimental details are provided in Appendix I." Per the filtering rules, appendix content is stripped by the parser and exists in the original submission. These criticisms are invalid.
- **"The existence of fixed points and invariant manifolds does not constitute an explanation of dynamics" (posed as a separate critical issue):** This is subsumed by the framing-to-evidence gap above. The paper *does* provide dynamics analysis for the two cases it studies; the issue is about the *scope* of what's claimed, not an absence of any dynamics explanation.
- **"No comparison with alternative mechanisms":** Removed as scope creep — the paper is proposing a mechanism, not adjudicating between all possible causes of stage-like learning.
- **"General nonlinear activation section is hand-waving":** The paper itself acknowledges its heuristic nature; flagging it as a separate weakness is duplicative given the framing-to-evidence gap already covers the limited scope of dynamics analysis.

## Novel Insights

The key structural observation is that the paper's contributions operate at two different tiers: the landscape results (Theorems 1, 3) are genuinely general, while the dynamics results (Theorems 4, Proposition 5) are narrow. The "universal mechanism" framing conflates these tiers. The paper's own Section 7 acknowledges the limitation, creating a tension where the paper simultaneously claims more than it has proven (in its title/abstract) and is honest about what it hasn't proven (in its discussion). The most valuable conceptual contribution — the distinction between data-driven and initialization-driven timescale separation — stands independently and is well-supported.

## Suggestions

1. Recalibrate the title, abstract, and introduction to accurately reflect the scope. Distinguish between what is proven for the general landscape (Theorems 1, 3) versus what is proven about dynamics (only for linear and quadratic two-layer networks). Present the paper as evidence that two distinct timescale separation mechanisms can produce saddle-to-saddle dynamics in tractable cases, with the landscape analysis providing the structural backbone that likely generalizes.
2. Add error bars or multi-seed visualizations to Figures 1 and 2.
3. Provide quantitative validation of the mechanism in at least the linear case (predicted vs. observed plateau durations from singular value gaps).
4. Fix the panel reference typo on line 99.

## Calibration Report

**Round 1 — Bracketing (score bands):**

| Band | Anchor(s) | Avg Score | Comparison to Paper |
|------|-----------|-----------|-------------------|
| Strong reject (<1.5) | nSDOkm0SKo, Uj0h13lVrR, P49gSPmrvN, 5lUdTogEL3 | 1.00 | Unrelated papers; no comparison |
| Reject (1.5–3.5) | 2NwHLAffZZ (GD linearization), NbbsRnPBoS (deep linear GD advantage), kkVTeMvC9D (Training Jacobian), a8XwgTZzE0 (Grokking dynamical systems), KNQJtoPZmz (Simplicity Bias overparam) | 2.00–3.40 | These papers have weaker or no theory; this paper is substantially stronger |
| Borderline reject (3.5–5.5) | Aq35gl2c1k (Critical Learning Periods) — 5.00; MY8SBpUece (Non-Linear Feature Learning) — 5.50; eQggPqESBr (Simplicity Bias & Optimization Threshold) — 5.50 | 5.00–5.50 | Comparable. This paper has broader landscape theory than Aq35gl2c1k (deep linear only). It has properly proven theorems unlike MY8SBpUece (conjecture-based). But the framing issue is a notable weakness. |
| Borderline accept (5.5–7.5) | CQF8mTF7qx (Simplicity Bias of SGD) — 6.00; XsHqr9dEGH (Dichotomy Implicit Biases) — 6.00; 3ROGsTX3IR (Grokking Phase Transition) — 5.80; wFD16gwpze (Scaling Laws Two-Layer) — 7.33 | 5.80–7.33 | This paper's theoretical scope (Theorems 1, 3 applying broadly) is wider than these, but its framing-to-evidence gap is larger. The 6.00 papers either have restrictive assumptions (CQF8mTF7qx) or are more tightly focused (XsHqr9dEGH). |
| Accept (7.5–8.5) | 4xWQS2z77v (Loss Landscape via Convex Duality) — 8.00; d8w0pmvXbZ (Transformer training proxies) — 8.00 | 8.00 | These papers are fully rigorous and self-contained; this paper does not reach this standard due to the framing gap. |
| Strong accept (>8.5) | None found | — | — |

**Itemized calibration comparison:**

The closest anchor is **CQF8mTF7qx (Simplicity Bias of SGD, avg 6.00)**. That anchor's heavy-weight weaknesses included: restrictive activation assumptions (weight -3, -4), unrealistic data assumptions (weight -4, -3), and unclear claim precision (weight -2). The current paper does *not* share those specific weaknesses — its activation assumptions are broader, and its theory does not require unrealistic data conditions. However, the current paper has a different heavy-weight weakness (framing-to-evidence gap) that the anchor does not. The anchor's heavy-weight strengths (weight +4 for tackling an important open problem, +3 for clean theoretical framework) are comparable to this paper's strongest contributions (Theorem 1 extensions, Theorem 3, the two-mechanism distinction). On balance, the current paper is slightly weaker than the 6.00 anchor because the framing issue is central to the paper's core claims.

The next-closest anchor is **MY8SBpUece (Non-Linear Feature Learning, avg 5.50)**. Its heavy-weight weaknesses included conjecture-based theorems (weight -5), unrealistic learning rate scaling (weight -4), and missing generalization analysis (weight -4). The current paper does not have conjecture-based theorems (its theorems are properly proven), but it has the framing gap. This paper is stronger than the 5.50 anchor.

**Score placement:** The Round 1 bracket was 4.0–7.0. After itemized comparison, the paper sits between the 5.50 anchor (MY8SBpUece) and the 6.00 anchor (CQF8mTF7qx). It is technically stronger than the 5.50 paper but the framing issue prevents it from reaching 6.00. Final score: 5.5.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>