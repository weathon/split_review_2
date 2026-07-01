Now I have a clear calibration picture. Let me write the final review.

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses
### Fatal
### Major
### Minor
### Trivial

## Nice-to-Haves
## Removed Points
## Novel Insights
## Suggestions
## Score and Decision

Let me compile the final review.

Round 1 bracket: between 3.5 and 6.5, anchored by "How transformers learn structured data" (5.00), "Depth Extrapolation" (4.50), "Mastering Syntax, Unlocking Semantics" (3.75), "A Percolation Model of Emergence" (7.00).

After narrowing: the paper is closest in quality to "Depth Extrapolation" (4.50) and "How transformers learn structured data" (5.00). It has more conceptual novelty than both but also more presentation issues than the former.

Final score: 4.5

Let me now write the full review.## Summary

This paper introduces a framework for studying how language models learn context-free grammars (CFGs) through the lens of "subgrammar" structure (inner and outer subgrammars, Definitions 3.3–3.5). The core theoretical contribution is a decomposition theorem (Theorem 4.3) stating that KL divergence between the true PCFG distribution and a learned model can be expressed as a sum over subgrammar-specific divergences. Empirically, the paper studies parallel learning dynamics, curriculum learning via subgrammar pretraining, and depth generalization limitations.

## Strengths

1. **Novel conceptual framing.** The notions of inner and outer subgrammars (Definitions 3.3–3.5) and the claim that KL divergence decomposes recursively over subgrammar structure (Theorem 4.3) are genuine contributions. The paper correctly identifies that prior work on CFGs and neural networks has focused on static representations or expressivity, not how learning interacts with grammar substructure. This framing opens a productive direction for studying learning dynamics in formal languages.

2. **Well-designed depth-vs-length experiment (Section 6, Figure 3).** The controlled experiment on nested parentheses cleanly separates length from recursive depth and shows that models fail on deep recursion but not on long sequences at shallow depth. Figure 3 includes variance bands, and the results confirm an important known limitation (cited as Bhattamishra et al. 2020, Lampinen 2024) with a clean, reproducible design.

3. **CKA analysis with 30 random seeds (Section 5.2, Table 1).** The representational similarity analysis showing that subgrammar pretraining leads to more aligned internal representations across attention layers is a meaningful mechanistic result. The paper varies both model size (2-layer vs 4-layer) and pretraining duration (10 vs 20 epochs), providing some breadth.

## Weaknesses

### Major

1. **Theoretical presentation is not self-contained and uses unclear notation.** The derivation from equations (1) to (4) in the main text (lines 122–132) is not presented in a verifiable form — the rendered output contains uninterpretable artifacts (ratios of logarithms) that prevent a reader from following the argument without the appendix. Definition 4.2 (lines 134–138) introduces the notation `D_KL(P_G || Q | ¬s)` where `¬s` is not standard and is never defined, yet this definition is the foundation for Theorem 4.3. While the conceptual claim ("KL divergence decomposes as a sum over subgrammars") is clear, the in-text mathematical presentation is not coherent enough for a reviewer to verify that the theorem follows from the definitions as written. The proofs are deferred to an appendix (standard practice), but the main text should contain a clean, parseable sketch.

2. **Experimental reproducibility is compromised by underspecified training details.** The paper says "small transformer" and "2-layer, 2-head transformer" but provides no information about embedding dimension, hidden dimension, number of parameters, training set size, number of training steps, learning rate, optimizer, regularization, or any hyperparameter choices. Without these details, the experiments cannot be reproduced or compared to future work.

3. **Loss curves lack error bars.** Figures 1 and 2 show KL divergence trajectories without any indication of variance across seeds. The paper mentions "30 random seeds" for CKA analysis (line 240) but the loss curves appear to be single trajectories. Figure 3 does include a variance band, making the omission in Figures 1–2 more conspicuous.

### Minor

4. **Corollary 4.7 is essentially vacuous.** The corollary states (informally) that if gradient updates on one subgrammar do not harm performance on other subgrammars, then all subgrammars are learned in parallel. The assumption (non-interference at every step of gradient descent) is so strong that it essentially *is* the conclusion. The paper acknowledges this is informal, but including it as a "corollary" inflates the theoretical contribution. The empirical observation that subgrammar losses all decrease together is still interesting — it just does not need this corollary.

5. **Table 1 is missing the 20-epoch condition for the 4-layer transformer.** The table shows two-layer results at 10 and 20 epochs of pretraining, but the four-layer column only shows 10 epochs. This asymmetry makes it hard to assess whether the pattern of increased CKA with longer pretraining holds for larger models.

6. **GPT-5.1 anecdote (Section 6, 5 examples per condition) is underpowered.** The paper correctly disclaims this as "purely anecdotal" (footnote 3), but including a 5-sample-per-condition test with no statistical testing in the main text of a conference paper undermines scientific credibility even with a disclaimer. Either remove it or run a proper experiment.

7. **Abstract's "show definitively" overstates what CKA establishes.** The claim that alignment analysis "show[s] definitively" that pretraining produces representations "more aligned with the grammar's substructure" (line 9) is too strong. CKA measures representational similarity between models, not alignment with a ground-truth grammar, and the percentage changes are modest (e.g., +8.9%).

### Trivial

8. Minor presentation: Definition 3.3 says `P'` is "the set of all rules with non-terminals in N'" — this could be read as either rules whose LHS is in N' or rules whose RHS non-terminals are also in N'. The standard interpretation (LHS in N') is clear enough in context but could be clarified.

## Nice-to-Haves

- **Alternative curriculum baselines.** Subgrammar pretraining is compared only to training from scratch. Comparing with random-order curricula or anti-curricula would help isolate whether the subgrammar structure specifically drives the benefit.
- **Architectural ablations.** The paper does not vary model width or depth (beyond 2 vs 4 layers) or ablate attention vs MLP contributions beyond the CKA analysis.

## Removed Points

These points were raised in the input but removed after verification against the paper:

- **Equations (1)–(4) being "mathematically wrong":** The rendered output contains parser artifacts (ratio-of-logs format that would not appear in the original PDF). The text clearly states that "the KL-divergence evaluates to a sum of conditioned KL-divergences," which is the correct conceptual claim. The proofs are in Appendix A. Removed because the criticism relies on parser rendering artifacts.
- **"No baselines":** The paper does compare "from scratch" vs "with pretraining," which is a valid baseline. Removed as factually incorrect.
- **Theorem 4.6 / E[R] > 1 concern:** The paper already explains that "if the expected recursion is 1 or greater, the PCFG sampling process... will in expectation never terminate" (line 184). Removed as already addressed.
- **Section 7 being "too speculative":** Discussion sections are expected to discuss open questions and future work. Removed.
- **Definition 3.3 ambiguity as a serious issue:** The standard reading is clear in context despite minor phrasing imprecision. Demoted to Trivial.

## Novel Insights

The most penetrating observation from the review process is that the paper's framing of subgrammar decomposition is genuinely novel, but its central empirical claim — "models learn all subgrammars in parallel" — is at odds with the paper's own mathematical framework. If the KL decomposition theorem holds, subgrammar losses must sum to the total loss; observing that they all decrease together is arithmetically necessary and not the informative dynamical claim it is presented as. The truly interesting question would be whether the *relative ordering* of convergence rates across subgrammars reflects structural complexity (e.g., depth in the grammar DAG), and on this the paper's data is suggestive but under-analyzed. The paper would be strengthened by reframing this as a question about which subgrammar properties predict convergence speed, rather than claiming parallel learning as a finding.

## Suggestions

1. Replace the garbled equation (4) derivation with a clean, step-by-step walkthrough that uses standard chain-rule factorization of KL divergence over the autoregressive product. Show explicitly how `D_KL(P||Q) = Σ_i D_KL(P||Q)_{A_i}` follows from the generative process.
2. Define `D_KL(P_G || Q)_A` with standard conditional KL notation (e.g., `D_KL(P_G(·|s) || Q(·|s))`) instead of the non-standard `¬s` notation.
3. Report full architectural and training hyperparameters (embedding dimension, learning rate, batch size, optimizer, training corpus size, number of steps).
4. Add error bars (shaded confidence bands or error regions at minimum) to Figures 1 and 2.
5. Either drop the GPT-5.1 anecdote or replace it with a properly powered experiment (≫5 examples per condition with significance testing).
6. Remove or substantially revise Corollary 4.7; the informal statement as written adds no insight.

## Score and Decision

Round 1 bracket: 3.5–6.5, anchored by comparison with:

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| "How transformers learn structured data" | 5.00 | R1 | Similar setting (transformers on PCFGs) but stronger experimental rigor; our paper has more conceptual novelty but weaker presentation |
| "Depth Extrapolation of Decoders" | 4.50 | R1 | Similar in having interesting ideas but presentation issues; our paper is slightly more novel conceptually |
| "Mastering Syntax, Unlocking Semantics" | 3.75 | R1 | Stronger theoretical claims but more questionable assumptions; our paper has cleaner experiments |
| "A Percolation Model of Emergence" | 7.00 | R1 | Better executed overall; clearer experiments, better writing, stronger empirical contributions |
| "Recovering Knowledge by Hardening LMs" | 3.00 | R1 | More limited contribution; our paper is more novel |
| "Training Neural Networks as Recognizers" | 6.25 | R1 | Better experimental methodology but less novel framing |
| "Geometric Signatures of Compositionality" | 5.40 | R1 | Similar in having mixed reviews and interesting but incomplete analyses |

After narrowing: the paper has genuine conceptual novelty comparable to the 5.0–5.4 papers, but the theoretical presentation issues (unclear notation, garbled equation rendering) and experimental reproducibility gaps (no architectural details, missing error bars on key figures) pull it down relative to those anchors. The most closely matched paper is "Depth Extrapolation of Decoders" (4.50), which also combines interesting ideas with significant presentation issues.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>