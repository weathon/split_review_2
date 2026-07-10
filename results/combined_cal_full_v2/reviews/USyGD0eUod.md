Now I have sufficient calibration data to produce my final review and score. Let me synthesize everything.

**Round 1 bracket: 5.0–7.0** (above "A Principled Evaluation Framework" at 5.00, below "SAEs Do Not Find Canonical Units" at 7.00).

**Round 2 narrowing: 5.5–6.5** (comparable to "Interpretability Illusions" at 5.60 and "CATE Benchmark" at 6.00).

**Final position:** 6.0. The paper's strengths (weights 8.20–10.10) are higher than comparable anchors' strengths, and its weaknesses (weights 2.41–5.19) are all positive (no severe negative-weight issues like some anchors). However, it lacks the methodological novelty of the 7.00 anchors. The SAE training budget concern (weight 5.19) is the most impactful weakness, followed by the title/framing issue.

Now let me produce the final review.

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

Let me write this out carefully, applying all the filtering rules.

Let me verify a few more claims from the reviewer:

1. Detection AUROC being "relegated to Appendix B" — The paper says at line 77: "We include similar AUROC curves for the 'detection' scoring method in Appendix B." But Figure 2 row 5 shows "AUROC (Detection)" in the main figure. So detection IS shown in the main figure. The per-layer ROC curves for detection might be in Appendix B, but the summary AUROC-by-layer data is in Figure 2. The reviewer overstated this. I should note this.

Actually, looking more carefully at the paper text:

Line 77: "We include similar AUROC curves for the 'detection' scoring method in Appendix B."

This could mean the ROC curves themselves (TPR vs FPR plots like Figure 1) are in Appendix B, while the summary AUROC-by-layer line plots are in Figure 2. That's a reasonable division. The reviewer's claim is misleading but there's a kernel of truth - the paper doesn't discuss detection results much in the main text.

But the reviewer says "relegates detection curves to Appendix B" - if Figure 2 row 5 IS detection, then this is factually inaccurate for the summary data. I'll note this in removed points.

2. The reviewer says "The toy model section... uses GloVe embeddings rather than Pythia embeddings for the language-data experiment (line 157)" — This is factually correct as stated at line 157. But this is an intentional choice (GloVe is a standard word embedding), not a mistake. This is a valid criticism about the indirectness of the evidence.

Let me finalize my review now.## Summary

This paper applies the randomized-weights sanity check (Adebayo et al., 2020) to SAE evaluation metrics, testing whether commonly used auto-interpretability scores and reconstruction metrics distinguish trained Pythia transformers (70M–6.9B) from randomly initialized ones. The central empirical finding is that aggregate auto-interpretability scores can be surprisingly similar between trained and random transformers — especially at larger scales — while token distribution entropy does reliably distinguish them. The paper serves as an important cautionary note for the mechanistic interpretability community about relying on aggregate metrics alone.

## Strengths

1. **Important and directly actionable core idea.** Applying the randomized-weights sanity check to SAE evaluation metrics is a natural and necessary test that the field should have run earlier. The finding that aggregate auto-interpretability scores can be similar between trained and random transformers, especially for larger models, is a genuine service to the community that should change how SAE quality is reported.

2. **Well-designed experimental conditions.** The paper considers four distinct randomization schemes (Step-0, Re-randomized incl. embeddings, Re-randomized excl. embeddings, and a Gaussian-embedding control), which is more thorough than a single random baseline. The distinction between Re-randomized conditions (which preserve parameter norms) and Step-0 (initialization) is thoughtful and reveals informative divergences (lines 85–87).

3. **Scale analysis across model sizes (70M to 6.9B) reveals the most interesting trend.** The observation that the gap between trained and random narrows with model scale (line 49) would not be visible in a single-model study and is the paper's most informative empirical contribution. This scaling finding is more nuanced and useful than a blanket "metrics fail" claim.

4. **Token distribution entropy as a distinguishing metric (Figure 2, bottom row).** While presented as preliminary, this is the paper's most concrete positive contribution. The observation that trained models show increasing token entropy with layer depth while random models do not provides a genuine foothold for future metric design and is correctly identified as an important direction (lines 125–127).

## Weaknesses

### Major

1. **Title and framing overclaim relative to the evidence.** The title states "Automated Interpretability Metrics Do Not Distinguish Trained and Random Transformers," but the paper's own results show that (a) token distribution entropy clearly distinguishes them (Figure 2, bottom row), (b) smaller models (70M) exhibit a gap the paper itself acknowledges (line 49: "auto-interpretability scores for randomized models were relatively low for smaller models... but that the gap was narrowed for larger models"), and (c) detection AUROC shows separation (Figure 2, row 5). The actual finding is more precise and more interesting: *as model scale increases, the gap in auto-interpretability scores narrows, and for large models randomized variants can match or exceed trained ones on some metrics.* The title should reflect this nuance rather than making an absolute claim that the paper's own evidence undermines.

2. **Main figures (Figures 1 and 2) lack uncertainty quantification.** The paper shows single curves per condition with no error bars, confidence intervals, or shaded regions. While Appendix E addresses multiple random seeds, the central visual claims about "overlap" between trained and random conditions cannot be properly evaluated without variance information across the 100 sampled latents per SAE (line 77). The null hypothesis is not that curves would be identical — it is that they would be drawn from the same distribution. Without error bands, "the curves overlap" remains a visual judgment that could change with more samples or different random seeds.

### Minor

3. **SAE training budget of 100M tokens may be insufficient, especially for the 6.9B model.** Standard practice in the SAE literature trains on billions of tokens (e.g., Gao et al., 2024, use ~8B). If SAEs on trained models are undertrained, they may not have learned meaningful features — which would trivially explain why they resemble SAEs on random models. The paper partially addresses this with 1B-token experiments (Appendix C), but 1B tokens is still well below typical convergence requirements. Without evidence of SAE convergence (loss curves, or results at substantially larger token budgets), this remains a confound that could affect the main result. The paper does show CE loss scores (Figure 2, row 6) indicating reasonable reconstruction quality, but this is a necessary rather than sufficient condition.

4. **The toy model section (Section 4) is the weakest part of the paper.** It uses MLPs rather than transformers, does not directly test the hypotheses on the actual transformer setting (the paper explicitly says "we leave the question of which predominates... to future work," line 131), and uses GloVe embeddings rather than Pythia embeddings for the language-data experiment (line 157). The section adds speculation rather than evidence for the mechanism behind the main results and could be condensed to a brief discussion paragraph without weakening the paper's contribution.

### Trivial

None that survive filtering — presentation issues are parser artifacts, not author errors.

## Nice-to-Haves

- The paper would benefit from a direct comparison of fuzzing vs. detection score discrepancies. The paper selects fuzzing as primary (justified by correlation with simulation scores, line 77) but does not explain why detection diverges from fuzzing or what this tells us about what auto-interpretability measures.
- Per-latent variance in auto-interpretability scores (distribution across the 100 sampled latents) would help assess whether similarity between conditions holds at the latent level or only in aggregate.

## Removed Points

These points were flagged in the source review but are removed for the following reasons:

- **Claim that detection curves are "relegated to Appendix B":** Detection AUROC appears as row 5 of the main Figure 2. Only the per-layer ROC curves (like Figure 1) are in Appendix B, which is a reasonable division. The reviewer overstated this claim.
- **Request for convergence diagnostics (loss curves):** The paper reports CE loss scores (Figure 2, row 6) as a reconstruction quality check. This is a reasonable proxy; requesting full training curves is a nice-to-have, not a core weakness.
- **"Ablation on SAE training data" suggestion:** This speculative direction goes beyond the paper's stated scope and is not necessary to evaluate its contribution.
- **"Per-latent variance" as a missing analysis:** Noted in Nice-to-Haves above; it would strengthen but is not a missing requirement.

## Novel Insights

The reviews collectively surface that the paper's most impactful contribution is more nuanced than its title suggests: the *narrowing* of the interpretability-metric gap with model scale, combined with the token-entropy measure that successfully distinguishes trained from random models. This positive finding is undersold by the paper's framing as a purely negative result. Both the harsh critic and the calibration anchors reveal a pattern: the strongest papers in this evaluation-of-interpretability space combine a cautionary empirical finding with either a proposed improvement (like the token entropy measure here) or a new methodological framework (like the anchor papers at 7.0). The current paper has the former but undersells it.

## Suggestions

1. **Reframe the title and abstract** around the scaling finding rather than the absolute claim. Something like "The Gap Between Trained and Random Transformers Narrows with Model Scale for Automated Interpretability Metrics" would be more accurate and more interesting.
2. **Add uncertainty quantification** to the main figures (confidence bands or error bars across seeds and sampled latents). Without it, the central visual claim of "overlap" is difficult to evaluate rigorously.
3. **Provide stronger evidence of SAE convergence** at more standard token budgets, or at minimum report per-latent score distributions to address the undertraining concern.
4. **Either substantially strengthen or cut the toy model section** (Section 4). As it stands, it adds length without evidence for the mechanism behind the main results.

---

## Score and Decision

**Calibration Anchors (all rounds):**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| Strong Reject (n=4) | Various | 1.00–1.40 | R1 | No | Not comparable; these are clearly non-viable papers |
| A Principled Evaluation Framework for Neuron Explanations | todLTYB1I7.md | 5.00 | R1 | Yes | Similar evaluation-of-evaluation approach but narrower scope; current paper is stronger |
| Interpretability Illusions in Generalization of Simplified Models | v675Iyu0ta.md | 5.60 | R2 | Yes | Similar negative-result empirical study on interpretability, but on toy tasks; current paper has real LLM results |
| ALMANACS: Simulatability Benchmark | KJzwUyryyl.md | 5.00 | R2 | Yes | Benchmark for LM explainability with sobering results; current paper is better scoped |
| Benchmarking Deletion Metrics | bXeSwrVgjN.md | 6.00 | R2 | Yes | Evaluation-of-metrics paper that proposed new method (TRACE); current paper lacks new-method contribution |
| Do Contemporary CATE Models... | Q2bJ2qgcP1.md | 6.00 | R2 | Yes | Large-scale negative-result benchmark with novel evaluation framework (Q statistic); accepted despite similar weaknesses |
| Sparse Autoencoders Do Not Find Canonical Units | 9ca9eHNrdH.md | 7.00 | R1 | Yes | Similar cautionary SAE paper that proposed three novel methods (stitching, meta-SAEs, BatchTopK) |
| Towards Principled Evaluations of SAEs | 1Njl73JKjB.md | 7.00 | R1 | Yes | SAE evaluation paper that proposed a new framework using supervised dictionaries |

**Round 1 bracket:** 5.0–7.0 (above the evaluation framework paper at 5.00, below the novel-method SAE papers at 7.00).

**Round 2 narrowing:** 5.5–6.5 (comparable to "Interpretability Illusions" at 5.60 and "CATE Benchmark" at 6.00).

**Weighted-item comparison:** The paper's strengths (weights 8.20–10.10) are higher than comparable anchors, and its weaknesses are all positive (2.41–5.19), unlike anchors with negative-weight weaknesses. The highest-impact weakness (SAE budget, weight 5.19) is a Minor concern partially addressed by Appendix C. The two Major issues (title overclaim, no uncertainty quantification) have lower weights (2.93, 2.41), indicating they are real but not structurally damaging. The paper lacks the methodological novelty of the 7.00 anchors, placing it below that threshold. Overall, the paper makes a solid, actionable contribution with addressable weaknesses.

**Final score: 6.0 — Borderline Accept.** The paper addresses an important question with careful experimental design and delivers a nuanced finding that should influence SAE evaluation practice. The main weaknesses (overclaiming title, missing error bars, SAE budget concerns) are fixable and do not invalidate the core contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>