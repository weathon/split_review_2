Now I have all the information needed. Let me write the final consolidated review.

## Summary

This paper proposes Thoughtbubbles, a transformer variant that learns to dynamically fork (clone) or delete residual streams in latent space during pretraining with only a language modeling loss. The forking decisions are driven by learned cumulative scores, and scores attenuate attention and residual updates to provide a training signal. The method is evaluated at 150M–772M scales on OpenWebText and peS2o, showing consistent perplexity improvements over standard transformers and non-adaptive copy-based baselines, along with zero-shot evaluations on LAMBADA, HellaSwag, BLiMP, and PIQA.

## Strengths

- **Genuinely novel mechanism (Sections 2.3–2.4).** The forking operation — cloning a residual stream, adding a learned embedding, placing it left of the parent, and attenuating attention/residual updates by cumulative scores — is a creative and non-obvious architectural design. It is substantively different from pause tokens (which insert tokens at fixed positions) and from CoT (which operates in token space). The attenuation trick (Eqs. 8–10) provides a training signal that incentivizes the model to assign high scores to important streams.

- **Consistent perplexity improvements across all scales and datasets (Table 1, Figure 3).** The perplexity gains are monotonic and do not rely on cherry-picking. OpenWebText 772M: 21.22 (baseline) → 19.74 (Ours κ=4L). peS2o 772M: 14.64 → 13.77. The improvement holds at every scale (150M, 319M, 772M) and on both datasets. The FLOPs-matching between Copy-5 and κ=4L helps separate the effect of adaptivity from raw computation.

- **Interpretability analysis (Figures 4–5).** The attention analysis showing parent tokens attend strongly to their child forks (Figure 4), and the correlation between forking rate and output entropy (Figure 5), provide evidence that the learned forking policy is allocating computation at meaningful (high-uncertainty) regions rather than arbitrarily.

## Weaknesses

### Major

- **Motivation–evaluation gap.** The paper is motivated throughout (Introduction, line 13; Conclusion) by the need to solve "complex, multi-step problems" and to enable "scaling inference-time computation." Yet every evaluation is on perplexity, LAMBADA (single-word completion), HellaSwag (commonsense NLI), BLiMP (grammaticality judgments), and PIQA (physical commonsense) — none of which require multi-step reasoning. The Limitations section acknowledges that GSM8K requires multi-billion-parameter scales, but this does not close the gap: the paper's framing is broader than the evidence supports. The architecture may genuinely help with multi-step reasoning, but that claim is untested.

- **Missing the most directly relevant baselines.** The Introduction and Related Work extensively discuss pause-token methods (Herel & Mikolov, 2024; Goyal et al., 2024; Sun et al., 2025) as the closest prior work, and the paper criticizes them for lacking dynamic allocation of intermediate computation. Yet none of these methods appear as baselines. The Copy-3/Copy-5 baseline controls for naive capacity increase but does not test whether the *adaptivity* (the claimed contribution) provides gains beyond existing adaptive-stream approaches. Without this comparison, it is unclear whether the dynamic allocation itself drives the improvements.

### Minor

- **No variance or significance reporting.** Across all 30+ numerical results in Table 1, there are no standard deviations, confidence intervals, or statements about number of random seeds. Several improvements are small (e.g., HellaSwag 772M OpenWebText: 30.6 baseline → 31.1 Ours κ=2L, a 0.5% absolute gain), making it impossible to assess whether differences are meaningful or within noise.

- **Parameter matching procedure is opaque.** The paper repeatedly states models are "parameter-matched" (Table 1 caption, Sections 3.3, 4) but does not explain in the main text how this was achieved (e.g., whether hidden dimension, number of layers, or other architectural choices were adjusted). While details may reside in the appendix, the main text should at minimum summarize the approach for reproducibility.

- **BLiMP underperformance against non-adaptive baselines.** On syntax understanding (BLiMP), Thoughtbubbles consistently underperforms the Copy-3/Copy-5 baselines (e.g., peS2o 772M: Copy-3 73.3 vs. Ours κ=4L 67.4, a ~6 point gap). The paper acknowledges this in one sentence ("pruned dynamic parallel computation may not be as helpful for syntax") but provides no deeper analysis of why structured syntax tasks benefit less from adaptive computation.

- **Top-k gradient bottleneck acknowledged but untested.** Section 8 notes that hard top-k decisions create a gradient bottleneck for early-layer scores and suggests "training time randomization and noise" as a mitigation, but this mitigation is not implemented or evaluated. The impact of this bottleneck on what the forking scores actually learn is unclear.

### Trivial

- The Copy-3/Copy-5 baseline's position encoding scheme is underspecified (Section 3.3). The description says copies "can attend to each other" but does not clarify how position information is assigned to duplicated residuals.

## Nice-to-Haves

- A control experiment with random forking decisions (same budget) would isolate the value of the learned policy from the value of extra capacity.
- Wall-clock time measurements (tokens/second) would contextualize the practical cost of the dynamic forking mechanism.
- Synthetic reasoning tasks (e.g., compositional addition, parity, or grid tracking) that require multi-step computation could bridge the motivation–evaluation gap even at small scales.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Criticism about "unsupervised" phrasing being odd** — pure style nitpick; removed per Hard Rule 5.
- **Speculation about Copy baseline position encoding causing degenerate attention** — the reviewer raised a question but did not identify a concrete problem in the paper; demoted to trivial.
- **General demand for larger-scale experiments or different datasets** — the current scale (up to 772M, 2.5B tokens) is adequate for the paper's scope and claims; removed per Soft Rule 2.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add at least one diagnostic evaluation that tests multi-step reasoning (e.g., a synthetic compositional task or a structured reasoning benchmark) to match the paper's stated motivation.
2. Include a pause-token baseline to directly test whether dynamic allocation adds value over fixed-stream insertion.
3. Report variance (standard deviations over 3+ seeds) for the main results in Table 1.
4. Clarify the parameter matching procedure — a brief summary table showing architectural choices at each scale.
5. Deepen the analysis of BLiMP underperformance: is there a property of syntax tasks that makes adaptive pruning counterproductive?

## Score and Decision

Score: 6.0

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>