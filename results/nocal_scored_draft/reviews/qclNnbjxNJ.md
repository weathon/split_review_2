Based on the favorability signals, the strengths are very strong (0.86-1.00) but the two main weaknesses (experimental evaluation gap at 0.00, Type I limitation at 0.17) are genuine concerns that prevent a higher score. Let me produce the final review.

## Summary

This paper tackles post-treatment selection bias in interventional causal discovery — a genuine practical problem in fields like gene perturbation screens where samples are retained only after passing quality control. The authors introduce a causal formulation modeling post-treatment selection, define the FI-Markov equivalence class and a new graphical representation (F-PAG), and propose the F-FCI algorithm that uses interventions on intermediate inducing nodes to distinguish causal relations from selection-induced dependencies. The algorithm is proven sound and complete for the FI-Markov equivalence class.

## Strengths

- **Core technical insight is clever and well-motivated.** Using hard interventions on intermediate Type-I inducing nodes to break the selection/causation ambiguity (Figure 4(b)/(f)) is a genuine advance over what standard FCI or interventional FCI can deliver. The ψ₃ test that resolves whether X₁–X₂ dependence is causal or selection-induced is clearly illustrated and technically sound.

- **Complete end-to-end framework with formal guarantees.** The paper provides a coherent theoretical package: FI-Markov equivalence (Definition 2), F-PAG graphical representation (Definition 5), and F-FCI algorithm with proofs of soundness (Theorem 3) and completeness (Theorem 4). This is a self-contained contribution that extends the existing MAG/PAG literature to the interventional+selection setting in a principled way.

- **Practically important, well-articulated problem.** Post-treatment selection in interventional causal discovery is genuinely underexplored, and the motivating examples (gene perturbation quality control, clinical trial per-protocol analysis) are compelling. Figure 1 elegantly demonstrates why standard cross-intervention invariance patterns fail.

## Weaknesses

### Major

- **Experimental evaluation does not directly test the central claim.** The paper's headline contribution is distinguishing post-treatment selection from causation. Yet the main evaluation (Figure 6) reports only global DAG Precision and SHD — metrics that conflate many sources of error and are not informative about whether F-FCI correctly labels individual edges as causal vs. selection-induced. The specific distinguishing-capability assessment is relegated to Table 1 in the appendix (line 277). The real-world experiment on Norman et al. data is described qualitatively with no quantitative precision/recall results against baselines in the main text. A dedicated experiment measuring how often F-FCI correctly classifies each edge type (causal vs. selection-induced) is needed to substantiate the core claim.

- **Practical scope is limited by the Type I inducing-node requirement, and this limitation is unquantified.** As the paper acknowledges (line 291), identification depends critically on Type I inducing nodes, and Type II nodes remain an open problem. In common short inducing paths (e.g., X₁ ← L → X₂, or X₁ → S ← X₂), there is no non-endpoint observed variable — hence no Type I node — and the method cannot distinguish selection from causation. The paper does not report how often Type I inducing nodes occur in its synthetic experimental setup or in typical real-world causal graphs, leaving the practical applicability uncharacterized.

### Minor

- **Baseline comparison is asymmetric and does not isolate the specific innovation.** The baselines (GIES, IGSP, UT-IGSP, JCI-GSP, FCI-INTERVEN, CDIS) do not model post-treatment selection (CDIS handles only pre-treatment selection). While comparing against standard methods is reasonable, it does not isolate the value of the proposed Type I inducing-node test. An ablation of F-FCI that skips Step 2.3, or a comparison against FCI run on pooled interventional data, would more directly demonstrate the benefit of the distinguishing mechanism.

- **The "at least two observed variables" assumption (line 60) is stated without justification.** Many real post-treatment selection scenarios (e.g., single-gate quality control) involve selection on one variable or a function of one variable, which would not satisfy this assumption. The paper should explain why this restriction is needed.

### Trivial

None.

## Nice-to-Haves

1. Add a dedicated experiment measuring distinguishing capability directly (precision/recall for edge-type classification) in the main paper. 2. Include an ablation that skips Step 2.3 to isolate the Type-I test benefit. 3. Quantify Type I inducing-node prevalence in the synthetic graphs and discuss real-world incidence. 4. Justify or relax the "at least two observed variables" assumption. 5. Provide quantitative evaluation of the real-world gene regulatory network experiment.

## Removed Points

These points were flagged and removed with brief justifications:
- **Pseudocode garbling (identical CI patterns)**: All six orientation rules showing `(⟂,⟂,⟂,⟂)` is a parser artifact; the original paper had distinct patterns. Removed per formatting-artifact rule.
- **FI-Markov equivalence lacks graphical characterization**: The paper provides Theorem 2 connecting it to MAG equivalence (skeleton, v-structure, intervened marks). Removed as factually incorrect.
- **Completeness claim at odds with Type I limitation**: Theorem 4 states completeness for the FI-Markov equivalence class, not the full DAG. Removed as factually incorrect.
- **Missing confidence intervals**: Paper explicitly states 95% CI error bars (Figure 6 caption). Removed as factually incorrect.
- **"Post-treatment selection" framing overclaims novelty**: The paper is clear that S represents general selection bias and specializes in post-treatment scenarios. The novelty is in the solution, not the model. Removed as overclaim.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The paper would benefit most from: (a) moving the distinguishing-capability experiment (Table 1) to the main paper, (b) adding an ablation that removes Step 2.3 to isolate the effect of the Type-I inducing-node test, and (c) quantifying the prevalence of Type I inducing nodes in the experimental setups used.

## Score and Decision

The paper has genuine theoretical strengths — the core idea is clever, the framework is complete with formal guarantees, and the problem is practically important. However, the experimental evaluation does not directly substantiate the headline claim of distinguishing selection from causation, and the practical scope is limited by an unquantified constraint. The paper is not fatally flawed; the theory is sound and the idea has merit. But the evidence as presented does not fully support the strength of the claims made.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>