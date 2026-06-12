Now I have enough calibration data. Let me finalize my analysis and write the complete review.

**Round 1 bracket**: Based on the calibration anchors, the paper sits between 4.0 and 5.5. The most comparable papers are:
- "Large Scale Video Continual Learning" (4.50, Reject): Similar topic, limited baselines, missing comparisons
- "PrAViC" (4.25, Reject): Online video classification, overstated claims
- "FSCIL" (5.00, Reject): New benchmarks/metrics + pipeline, but limited analysis depth
- "Anomalies Streaming" (5.71, Reject): Novel task + benchmark for CL in video, but questionable pioneer claims
- "EgoVideo" (6.00, Accept): Egocentric video, consistent improvements across all metrics

The paper has a more thorough ablation than the 4.25-4.50 reject papers, and a more useful dataset contribution than the FSCIL paper. But it shares the overclaiming and limited-baseline issues with the lower-scored anchors, and lacks the consistent strong results that characterize the 6.0 papers. I place it at **5.0**.

**Round 2 bracket**: Confirmed 5.0 based on comparison with FSCIL (5.00) — both introduce useful benchmarks and evaluation protocols but have overstated contributions and limited baselines.

Now let me write the final review.

---

## Summary

This paper introduces Continuous Online Action Detection (COAD), a task formulation enabling models to continuously learn from streaming egocentic video at deployment time without data storage or multiple passes. The paper contributes the Ego-OAD benchmark (87 action classes, 263h curated from Ego4D) and three training strategies—state continuity, orthogonal gradient projection, and non-uniform loss—adapted from prior continuous video learning work. Experiments on Ego-OAD and EPIC-KITCHENS-100 demonstrate improved out-of-stream generalization over naive online training.

## Strengths

- **Comprehensive component ablation**: Table 3 tests all 8 combinations of the three binary components in both in-stream and out-of-stream settings, clearly showing each component's individual contribution. Non-uniform loss provides the largest out-of-stream mAP gain (+4.2), orthogonal gradient adds +4.5 Top-5 Recall out-of-stream, and state continuity provides smaller but consistent gains. This is a genuinely thorough evaluation of each technique.

- **Progressive improvement toward IID upper bound**: Figure 4 shows COAD's out-of-stream performance steadily improving over the course of in-stream training, approaching the IID training baseline. Ablated variants (w/o orthogonal gradient, w/o non-uniform loss) show significantly lower curves, demonstrating that the full combination is important for this convergence. This is the paper's most compelling piece of evidence.

- **Useful Ego-OAD dataset**: The curation from Ego4D MQ provides 87 action classes across 263h with multi-label temporal grounding and 36% action overlap, addressing a genuine gap—prior egocentric OAD datasets like EPIC-KITCHENS are limited to kitchen settings.

- **Demonstrated adaptation-generalization balance on Ego-OAD**: Table 1 shows COAD consistently outperforms the w/o COAD baseline on out-of-stream generalization (e.g., +6.9% vs +2.5% Top-5 Recall with Ego pretrain, +6.5% vs +2.3% with Exo pretrain) while maintaining strong in-stream Top-5 Recall, demonstrating effective management of the adaptation-generalization trade-off on the proposed benchmark.

## Weaknesses

### Fatal
None

### Major

- **Headline numbers conflate paradigm benefit with technique benefit**: The abstract claims "improves adaptation to the user's environment by up to 20% in top-5 accuracy, and improves generalization to new scenarios by up to 7%." These deltas are computed against a Pretrained Only baseline (zero online adaptation). However, Table 3 reveals that the "w/o COAD" row (naive online training without any proposed techniques) already gains +18.7 in-stream Top-5 Recall (Exo pretrain, from Table 1) and +5.4 out-stream mAP over Pretrained Only. The COAD-specific techniques contribute only +3.8 additional in-stream Top-5 Recall and +0.5 out-stream mAP. While the paper's contribution includes the task formulation itself, the abstract and contribution bullet (line 30) frame these as "the proposed method" improvements, attributing the full gap—including the benefit of simply doing any online learning—to COAD. This significantly overstates the technique-specific contribution by roughly an order of magnitude.

- **Limited baselines — no comparison with established continual learning methods**: The only baselines are Pretrained Only (no adaptation) and w/o COAD (naive single-pass online training without any of the three proposed strategies). There is no comparison with methods from the continual learning literature (e.g., EWC, replay-based methods with small buffers, learning rate regularization). The w/o COAD baseline is deliberately naive—it resets hidden states, uses uniform loss, and applies no gradient decorrelation. Comparing only against a strawman leaves readers unable to assess the marginal value of the specific techniques.

### Minor

- **Mixed EPIC-KITCHENS results undermine generalization claims**: On EPIC-KITCHENS in-stream (Table 2), COAD underperforms Pretrained Only on several metrics: Action mAP drops from 9.6 to 7.9, Action Top-5 Recall drops from 22.9 to 20.5, Noun Top-5 Recall drops from 14.7 to 13.9. The paper attributes this to "fine-grained nature of the actions" (line 188), but EPIC-KITCHENS is the primary alternative benchmark chosen to validate the method, and continuous adaptation actively hurting in-stream performance on this dataset suggests limited robustness. The out-of-stream gains on EPIC (e.g., Noun mAP from 31.4 to 37.1) are more positive but not discussed with sufficient depth.

- **No error bars or statistical significance**: All results are single-run numbers without confidence intervals, standard deviations, or statistical tests. For a paper making specific quantitative claims about percentage improvements, and where the COAD-specific gains over w/o COAD are often small (e.g., +0.5 mAP out-stream), this limits confidence in the findings.

- **Non-uniform loss trade-off not adequately discussed**: Table 3 shows non-uniform loss dramatically shifts the adaptation-generalization trade-off: removing it causes in-stream mAP to jump from 36.8 to 42.4 while out-stream drops from 26.0 to 21.8. This suggests the non-uniform loss functions primarily as a regularizer that suppresses in-stream fitting rather than enabling better learning. The paper does not discuss this trade-off or its implications for deployment.

### Trivial

- **Typo on line 66**: "Continuous OAD (CODA)" should be "COAD" to match the rest of the paper.

## Nice-to-Haves
- Discussion of the frozen backbone as a limitation: continuous learning only affects the lightweight GRU head while the feature extractor remains fixed. Updating the backbone could significantly change the conclusions.
- Deeper analysis of why each component helps—beyond ablation numbers, what does each technique do to the learned representations?
- The IID upper bound is shown in Figure 4 but not tabulated in the main results tables, making direct numerical comparison difficult.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Missing Appendix A details (action class grouping) — appendix content is stripped by the parser; it exists in the original submission.
- Missing limitations section — while a limitations section would be desirable, its absence is a presentation choice, not a substantive flaw.
- Reproducibility concerns about hyperparameters — the paper provides implementation details in Section 5.2 sufficient for the main experiments.

## Novel Insights
The paper's key insight is that even with a frozen backbone and a lightweight RNN head, single-pass continuous learning from streaming video can substantially improve online action detection over offline-only training, approaching the IID upper bound. The ablation also reveals that non-uniform loss acts primarily as a regularizer controlling the adaptation-generalization trade-off—an observation worth deeper exploration.

## Suggestions
- Reframe the abstract to clearly distinguish between the gain from online learning itself (the bulk of the improvement) and the additional gain from COAD-specific techniques.
- Add at least 2-3 established continual learning baselines to contextualize the specific contribution.
- Report results across multiple runs with confidence intervals.
- Discuss the EPIC-KITCHENS in-stream failures in more depth rather than attributing them to dataset characteristics alone.

## Calibration Anchors

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| `5lUdTogEL3` — Lifelong Person ReID | 1.00 | 1 | Fundamentally different quality; not comparable |
| `gwZ90hFSL2` — Cross-Lingual Humanoid Robots | 1.00 | 1 | Off-topic/novelty-free; not comparable |
| `WM5G2NWSYC` — Projected Subnetworks | 2.00 | 1 | Weak method, limited contribution; our paper is stronger |
| `JIlIYIHMuv` — LVLM-CL | 2.50 | 1 | CL for VLMs, limited novelty; our paper has better experiments |
| `HCCkCjClO0` — Online Weight Approximation | 3.00 | 1 | CL method, solid but narrow; our paper has broader scope |
| `7L2bpe7lfm` — Video CL Compression | 4.50 | 1 | Very similar topic (video CL), missing baselines, similar weaknesses |
| `G9Ea7mlqGO` — CLIP Online CL | 3.80 | 1 | Online CL with CLIP, limited novelty; our paper more thorough |
| `jawV7vhGHw` — PrAViC | 4.25 | 1 | Online video classification, overstated claims—similar pattern |
| `oO3oXJ19Pb` — Online Dense Captioning | 4.80 | 1 | Online video understanding, mixed reviews |
| `UrmnIDCzLA` — FSCIL | 5.00 | 2 | New benchmarks + pipeline, limited analysis depth—similar profile |
| `Y7jJN0VQ4y` — Anomalies Streaming | 5.71 | 1 | Novel CL task for video, benchmark, but pioneer claim questioned |
| `JbPb6RieNC` — StreamChat | 5.80 | 1 | Streaming video with strong benchmark; accepted |
| `P6G1Z6jkf3` — EgoVideo | 6.00 | 2 | Egocentric video, consistent SOTA results; accepted |
| `TLADT8Wrhn` — TiC-CLIP | 6.25 | 1 | Web-scale continual training benchmarks; accepted |
| `9Cu8MRmhq2` — Multi-granularity Correspondence | 8.00 | 1 | Much stronger contribution; not comparable |
| `nc0XGK40dn` — TTA for Human Motion | 4.67 | 2 | Continual TTA, mixed results; similar issues |
| `EKfcngSxwD` — VLM Task Codebook | 4.67 | 2 | Incremental VLM adaptation; similar profile |

**Scoring rationale**: The paper's genuine contributions (Ego-OAD dataset, comprehensive ablation, task formulation) place it above the 4.0-4.5 reject papers that share similar baseline/experimental weaknesses. However, the overstated headline numbers, limited baselines, incremental techniques adapted from prior work, and mixed EPIC-KITCHENS results keep it below the 5.5-6.0 accept papers (EgoVideo, StreamChat, TiC-CLIP) which showed either consistent strong results or novel large-scale contributions. The closest anchor is FSCIL (5.00, Reject), which similarly introduced new benchmarks and evaluation protocols but had overstated contributions and limited analysis depth.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>