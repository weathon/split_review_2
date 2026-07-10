## Summary

This paper applies the Adebayo et al. (2020) sanity-check paradigm to sparse autoencoders (SAEs) and automated interpretability pipelines. It trains SAEs on the residual stream of Pythia models (70M–6.9B) under multiple randomization schemes (step-0, re-randomized with/without preserved embeddings, Gaussian embedding control) and compares aggregate metrics across trained vs. randomly initialized transformers. The central finding is that auto-interpretability AUROC scores and several reconstruction metrics are surprisingly similar between trained and randomized models, while a token-distribution entropy measure does reveal differences. The paper argues that aggregate metrics are insufficient to guarantee that learned, computationally relevant features have been discovered.

## Strengths

1. **Well-constructed randomization baselines** — The paper uses four meaningful variants (Step-0, re-randomized with/without embeddings, Gaussian embedding control) that allow attribution of effects to specific components (trained embeddings vs. trained weights). This design goes beyond a simple trained-vs-random comparison and is a real methodological strength. [favorability=10.54]

2. **Systematic scale sweep across Pythia 70M–6.9B** — Testing five model sizes reveals that the AUROC gap between trained and random narrows as models get larger — a non-obvious finding that adds nuance to the core result. [favorability=12.31]

3. **Token distribution entropy as a differentiating metric** — The entropy analysis shows that random models' SAE latents remain token-specific even at deep layers, while trained models' latents become more abstract (higher entropy). This serves as a proof-of-concept for a metric that **does** reveal differences that aggregate AUROC misses. [favorability=8.49]

4. **Appropriate epistemic caution** — The paper explicitly states (Section 5) that its results do not imply SAEs fail to capture useful features from trained models, only that aggregate metrics are insufficient. This honest scoping is welcome in a literature that often overclaims. [favorability=11.74]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Abstract slightly overgeneralizes reconstruction metrics.** The abstract states that "reconstruction metrics" are "similar" between trained and randomized models. However, the body acknowledges (line 89) that the CE loss score "only makes sense for the trained variant: for any of the randomized variants, the loss is very poor, regardless of whether the original or reconstructed activations are used." Of the four reconstruction metrics considered, one (CE loss score) is fundamentally not comparable across conditions. The abstract should either specify which reconstruction metrics behave similarly or qualify this claim more carefully. [favorability=5.49]

2. **Auto-interpretability pipeline lacks a direct control for the LLM-as-evaluator confound.** The token entropy analysis (Section 3) shows that random models produce more token-specific (simpler) latents, which the paper acknowledges. However, a direct experimental control — e.g., shuffling explanation-to-latent assignments and verifying that the fuzzing AUROC drops accordingly — would strengthen the claim that the pipeline is measuring something beyond pattern simplicity. The paper identifies the conceptual issue but does not run this control. [favorability=5.85]

3. **Central quantitative results lack uncertainty estimates in the main text.** The main figures (Figures 1, 2) and the reported AUROC values do not include confidence intervals or variance estimates. The paper mentions multiple random seeds in Appendix E, but for a negative-finding paper (metrics *fail* to distinguish), showing that the failure is robust across seeds in the main presentation would substantially strengthen the core claim. [favorability=4.94]

4. **Toy model section (Section 4) is loosely connected to the main experiments.** The toy analysis studies a two-layer MLP, not a transformer, and measures reconstruction sparsity rather than auto-interpretability. The paper is appropriately cautious ("leave…to future work"), but the section contributes little to the core narrative and requires multiple inferential leaps to bridge to the main results. [favorability=1.58]

5. **Only the Pythia model family is tested.** While the paper acknowledges this limitation, the generalizability of the negative result would be considerably strengthened by testing at least one other architecture (e.g., Gemma, Llama-2, OLMo), especially given the paper's broad title about "transformers" generally. [favorability=4.25]

### Trivial
None.

## Nice-to-Haves

- The paper could directly test whether individual latents that combine **high AUROC with high entropy** (candidate abstract features) exist predominantly in the trained model. The scatter plot in Appendix H presumably addresses this but is not discussed in the main text — this is a missed opportunity to sharpen the paper's main argument.
- A shuffled-explanations control (as described in Weakness 2 above) would cleanly address the LLM confound.
- Including bootstrap confidence intervals or standard errors for the central AUROC values in Figures 1 and 2 would make the negative-finding claim more robust.

## Removed Points

These points from the input review were removed, with justification:

- **Issue 1 (Directionality: random models outperform trained).** The reviewer argued that the paper's framing of "similar" is misleading because randomized models score ~0.08 higher on AUROC (0.87 vs. 0.79). This is not a genuine weakness: the paper's core claim is that metrics *do not distinguish* trained from random models — the direction of the gap is irrelevant to this claim and in fact strengthens it. The paper presents the raw AUC values in its figure captions, so readers can see the numbers. Removed as a framing preference, not a substantive flaw.
- **Request for individual-latent AUROC distributions.** The paper states (line 93) that Appendix H shows individual latent AUROC vs. entropy scatter plots. The data exist in the appendix. Removed because the paper already addresses this.
- **Generic strengths removed:** "Timely and important research question" — generic praise applicable to any paper. Removed.

## Novel Insights

The harsh critic's observation about the directionality of the gap (random > trained) is worth noting even though it does not undermine the paper's thesis — it strengthens it by showing the metric is not merely insensitive but systematically biased. More importantly, the critic points out that the token-entropy analysis could be sharpened: the paper has the data to ask whether latents with both high AUROC *and* high entropy (abstract features) are exclusive to trained models. This question is visible in the Appendix H scatter plots but is not discussed in the main text, representing a missed analytical opportunity.

## Suggestions

1. Scope down the abstract's reconstruction-metrics claim to exclude or qualify the CE loss score.
2. Add a shuffled-explanations control to the auto-interpretability pipeline to directly test whether the LLM-as-evaluator confound drives the results.
3. Include bootstrap confidence intervals or inter-seed variance ranges for the core AUROC comparisons in the main figures.
4. Either strengthen the connection of the toy model section to the main experiments (e.g., train SAEs on the toy MLP outputs and measure auto-interpretability) or move most of Section 4 to the appendix.
5. Explicitly analyze whether individual latents that combine high AUROC with high entropy exist in the trained model but not in randomized variants.

## Score and Decision

**Bracket determination (Round 1):** Initial bracketing spanned all score ranges. The most relevant anchors were:
- "Interpretability Illusions in the Generalization of Simplified Models" (5.60, Reject) — similar negative-finding paper about interpretability limits; narrower scope (single toy task) than the reviewed paper.
- "Benchmarking Deletion Metrics" (6.00, Reject) — similar metric-evaluation paper; had a proof error and presentation issues not present here.
- "Towards Best Practices of Activation Patching" (6.67, Accept) — similar best-practices paper about methodological choices in interpretability; more thorough experiments but conceptually analogous.

Initial bracket: **5.5–6.5**.

**Narrowing (Round 2):** Compared itemized favorability profiles. The reviewed paper's weaknesses (all favorability 1.58–5.85, mean ~4.4) are milder than "Interpretability Illusions" (weaknesses as low as -3.38, mean ~3.0) but its strengths (8.49–12.31) are comparable. The paper has no fatal flaws, no major issues, and a clear, reproducible core finding. However, its scope is limited to one model family and it lacks a crucial experimental control for the LLM confound — gaps that the "Activation Patching" anchor addresses more thoroughly.

**Final placement:** The paper sits between the negative-finding "Interpretability Illusions" (5.60) and the more comprehensive "Activation Patching Best Practices" (6.67). Its experimental design is stronger than the former (multiple randomization schemes, scale sweep) but weaker than the latter (single model family, missing LLM control). The paper makes a clear and timely contribution, but its limitations keep it from being a strong accept.

**All anchors retrieved:**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| P49gSPmrvN.md | 1.00 | R1 | No | Unrelated (UMAP+word embeddings) |
| nSDOkm0SKo.md | 1.00 | R1 | No | Unrelated (financial news) |
| Uj0h13lVrR.md | 1.00 | R1 | No | Unrelated (GFlowNets) |
| u1cQYxRI1H.md | 0.50/10.0 | R1 | No | Unrelated (diffusion illumination) |
| tcsZt9ZNKD.md | 1.75/8.20* | R1 | Yes | Discrepant metadata; Scaling SAEs — much stronger paper |
| Wxl0JMgDoU.md | 2.50 | R1 | No | SAEs on chess — similar area, lower quality |
| 89wVrywsIy.md | 3.40 | R1 | No | SAE circuit analysis — mixed reviews |
| UbLvSPMvMA.md | 1.67 | R1 | No | Sparsity beyond TopK — lower quality |
| MOtZlKkvdz.md | 3.67 | R1 | Yes | LLMs as explainers — weaker methodology |
| o6eUNPBAEc.md | 5.00 | R1 | No | LLMs struggle to explain — tangentially related |
| vc1i3a4O99.md | 5.00 | R1 | No | Steering with SAEs — method paper, not critique |
| ZXO7iURZfW.md | 5.25 | R1 | No | Auto feature engineering — unrelated |
| 1Njl73JKjB.md | 7.00 | R1 | Yes | Principled evaluations of SAEs — stronger paper |
| 9ca9eHNrdH.md | 7.00 | R1 | Yes | SAEs not canonical — stronger paper |
| XAjfjizaKs.md | 6.50 | R1 | No | Multi-layer SAEs — method paper |
| imT03YXlG2.md | 6.50 | R1 | No | SAEs visual concepts — different domain |
| I4e82CIDxv.md | 8.00 | R1 | No | Sparse feature circuits — stronger paper |
| kbjJ9ZOakb.md | 8.00 | R1 | No | Neuronal invariance — unrelated |
| uHLgDEgiS5.md | 8.00 | R1 | No | Training data influence — unrelated |
| DzGe40glxs.md | 8.00 | R1 | No | Emergent planning in RL — unrelated |
| bXeSwrVgjN.md | 6.00 | R2 | Yes | Benchmarking deletion metrics — similar concept |
| 6KZ80APcxf.md | 5.50 | R2 | No | Benchmarking XAI — different domain |
| Hf17y6u9BC.md | 6.67 | R2 | Yes | Activation patching best practices — closest analog |
| bpheRCxzb4.md | 6.50 | R2 | No | Measuring info in text explanations — tangentially related |
| VJvbOSXRUq.md | 5.75 | R2 | No | GNN explainer benchmarking — different domain |
| v675Iyu0ta.md | 5.60 | R2 | Yes | **Interpretability illusions — closest negative-finding analog** |
| ZtvRqm6oBu.md | 5.25 | R2 | No | SAEs to unlearn knowledge — different focus |
| ZLAQ6Pjf9y.md | 5.60 | R2 | No | SAEs for radiology — applied domain |
| MDvecs7EvO.md | 6.50 | R2 | No | Mechanistic permutability — method paper |
| 5lIXRf8Lnw.md | 5.50 | R2 | No | Auto-interpreting millions of features — method paper |

*\*Metadata discrepancy on this file; not used as primary anchor.*

**Grounding in favorability comparison:** The reviewed paper's highest-favorability weak items (abstract overgeneralization at 5.49, missing LLM control at 5.85) are comparable to the moderate weaknesses in the 6.00–6.67 anchors. Its lowest-favorability weak item (toy model connection at 1.58) is milder than the -3.38 item in the 5.60 anchor. The paper lacks the strongly negative weak items that drag down the 5.60 anchor. This places it above 5.60 but below papers with more thorough empirical validation (6.67).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>