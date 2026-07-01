Now let me write the final consolidated review.

## Summary

This paper applies a "randomized null model" sanity check (following Adebayo et al., 2020) to sparse autoencoder (SAE) evaluation. It trains SAEs on activations from trained Pythia transformers (70M–6.9B) and several randomized variants (Step-0, re-randomized with/without embeddings, plus a Gaussian-embedding control), comparing them using standard auto-interpretability metrics (fuzzing AUROC, detection AUROC) and reconstruction metrics. The core finding is that for larger models, aggregate auto-interpretability scores are surprisingly similar between trained and randomized transformers — indeed, random models can *outperform* trained ones on fuzzing AUROC (0.87–0.88 vs. 0.79). This raises important questions about what these metrics capture. A toy-model analysis sketches why random networks might preserve or amplify sparse structure.

## Strengths

1. **Well-motivated and timely sanity check.** Applying the "randomized model as null" logic to SAE evaluation is a natural and important test that should arguably be standard practice. The paper makes a clear case for why this matters to the growing SAE-based interpretability literature.

2. **Systematic multi-scale evaluation.** The paper tests Pythia models from 70M to 6.9B parameters, uses multiple randomization schemes (Step-0, re-randomized with/without embeddings), and includes a sensible Gaussian-embedding control. The finding that the gap between trained and randomized narrows at larger scales is the most interesting empirical result.

3. **Striking AUROC inversion.** From Figure 1, the trained model achieves fuzzing AUROC ≈ 0.79 while randomized variants achieve 0.87–0.88 — the random models *outperform* the trained model on this metric. This is a genuinely striking result and arguably the paper's strongest evidence that these metrics are not capturing what researchers want them to capture.

4. **Measured conclusions.** The paper explicitly stops short of claiming that SAEs fail entirely on trained models (Sections 5, 6) and correctly frames the implication: aggregate auto-interpretability scores are *insufficient* proof of meaningful features, not *irrelevant*. This restraint gives the paper credibility.

## Weaknesses

### Fatal
None.

### Major

1. **No uncertainty quantification for the headline results.** The paper samples 100 latents per SAE (out of tens of thousands) to compute auto-interpretability scores, but reports no confidence intervals, bootstrap estimates, or error bars in the main figures (Figures 1, 2). The core claim is that scores are "similar" between trained and random — but with 100 samples from a single random seed (multi-seed results are deferred to Appendix E), the reader cannot assess whether the observed gaps (e.g., 0.79 vs. 0.87–0.88, or the 0.01 difference between random variants) are stable or within sampling noise. For an empirical paper whose central thesis is a *negative* result about metric failure, statistical rigor is essential.

### Minor

2. **Title overclaims relative to the evidence.** The title "Automated Interpretability Metrics Do Not Distinguish Trained and Random Transformers" is absolute, but the paper's own results show a more nuanced picture: (a) for smaller models (Pythia-70M), the metrics *do* distinguish (line 49); (b) token distribution entropy — itself an automated metric — *does* distinguish trained from random variants (lines 125–127, Figure 2 last row). The abstract and conclusion use qualifiers ("in many settings," "under certain conditions"), but the title and headline framing are broader than the evidence supports. A more precise title would match the evidence.

3. **The most informative control is absent.** The paper compares SAEs trained on activations from trained vs. randomized transformers, but never trains an SAE *directly on token embeddings* and evaluates it with the same auto-interpretability metrics (fuzzing AUROC). The GloVe analysis in Section 4.3 uses different metrics (Pareto frontiers), so it does not directly anchor the main results. Without this control, the paper cannot distinguish whether auto-interpretability scores reflect input data statistics or transformer-architecture-specific structure. This limits the paper's explanatory power but does not invalidate the core finding.

4. **Section 4 (toy model) is a plausibility argument, not a mechanistic test.** The toy analysis uses a 2-layer MLP on toy data and GloVe vectors with Pareto frontiers — a different architecture, different data, and different metrics from the main experiments. The paper honestly characterizes this as speculative (line 131), but as a result Section 4 does not experimentally validate or predict the main empirical finding. It could be shortened or moved to an appendix without affecting the core contribution.

### Trivial
None.

## Nice-to-Haves

- **Concrete practitioner guidelines.** The paper recommends "routine randomized baselines" but does not suggest a threshold or gap size that should raise concern. Even a rough guideline would make the finding actionable.
- **State the Figure 1 AUROC values in the main text.** The striking finding that random models (0.87–0.88) *outperform* the trained model (0.79) on fuzzing AUROC is currently only in the figure caption and deserves prose emphasis.
- **A tighter control for the Gaussian-embedding condition.** Matching the token-embedding distribution but randomizing the assignment (rather than i.i.d. Gaussian) would be more informative.

## Removed Points

The following points from the input review are removed with justification:

- "Gaussian-embedding control functions as a floor check rather than a meaningful comparison" — REMOVED. A floor check is a valid and meaningful experimental condition; the paper uses it correctly as a lower bound.
- "Simulation scoring is mentioned but not tested" — REMOVED. The paper notes this is expensive to compute (line 75); the absence of an expensive alternative is not a weakness.
- "CE loss score is not comparable across the main comparison" — REMOVED. The paper explicitly acknowledges this (line 89).
- "Entropy metric does distinguish" as a standalone weakness — MERGED into the title-overclaim point. The paper itself introduces entropy as a metric that reveals differences missed by aggregate scores; this is part of its contribution, not a contradiction.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add error bars or bootstrap confidence intervals to Figures 1 and 2 for the 100-latent estimates, and report how many random seeds were used for each randomized variant in the main text.
2. Add a data-only baseline: train an SAE on the raw token embeddings (without any transformer forward pass) and report its fuzzing AUROC alongside the existing variants in Figure 2.
3. Retitle the paper to reflect the scale-dependent finding (e.g., "Aggregate Auto-Interpretability Scores Can Be Similar for Trained and Random Large Transformers").
4. State the specific AUROC values from Figure 1 (Trained: 0.79, Randomized: 0.87–0.88) in the main text and discuss the direction of the gap.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>