## Summary
STBP proposes a continual spatio-temporal forecasting framework that pairs a general-purpose backbone — a frequency-domain network (FreNet) for temporal modeling and a dual-stream linear graph attention module (DLGA) — with a scalable contextual pattern bank. After an initial joint training period (τ=1), the backbone is permanently frozen and subsequent incremental stages only fine-tune newly appended pattern bank rows. The method delivers 21%+ MAE improvements over the prior best (EAC) on two traffic benchmarks and marginal but positive gains on a meteorological dataset.

---

## Strengths

- **Strong, consistent quantitative gains on traffic benchmarks.** On PEMS-Stream and CA-Stream, STBP reduces average MAE by 21.44% and 21.93% over EAC (Table 1), consistently across all three horizons (3, 6, 12 steps) and all three metrics (MAE, RMSE, MAPE). These are not marginal differences; they represent a genuinely different performance tier.

- **t-SNE case study is non-trivially substantive.** Figures 3 and 6 show that the pattern bank autonomously learns semantically coherent clusters without explicit clustering objectives, and that new nodes added in 2017 are correctly assigned to clusters established in 2011. This provides direct, interpretable evidence for the core claim that the bank captures node heterogeneity and relevance.

- **Few-shot evaluation (Table 2) is a principled stress test.** Reducing subsequent-period training data to 10% tests robustness under data scarcity. STBP's advantage over both conventional STGNNs and CSTF methods is substantial and consistent, supporting the claim that the frozen backbone retains general representations that generalize from limited new data.

- **Efficiency analysis (Figure 8) is honest and thorough.** It reports both training time and GPU memory, contrasts linear vs. quadratic attention on a toy dataset, and honestly shows that STBP's overhead over EAC is small relative to the performance gain.

---

## Weaknesses

### Fatal
None.

### Major

- **The "catastrophic forgetting mitigation" framing overstates the mechanism.** The paper repeatedly frames its contribution as *alleviating catastrophic forgetting* (Abstract, Introduction challenge ❸, Section 4.2). However, the architecture makes forgetting structurally impossible by design: the backbone is permanently frozen after τ=1, and the pattern bank only appends new rows (Eq. 4) — old entries are never overwritten. This is parameter isolation/expansion, not a non-trivial stability-plasticity tradeoff. No comparison with a variant where the full model is fine-tuned without freezing is provided, which would be the natural ablation for a forgetting-mitigation claim. The framing inflates the conceptual contribution.

- **AIR-Stream RMSE results are occasionally worse than EAC, with no explanation.** At horizons 6 and 12, STBP RMSE (39.81, 44.97) is worse than EAC (39.63, 44.65) — confirmed in Table 1 rows 179–180. The average MAE advantage on AIR-Stream is only 2.35% versus 21%+ on traffic datasets. The Abstract and Introduction claim broad applicability across "traffic and meteorology domains," but no analysis is provided for why the gains on AIR-Stream are an order of magnitude smaller, and why STBP is occasionally inferior to EAC on RMSE. The cross-domain generality claim is not adequately supported.

### Minor

- **Backbone quality is entirely dependent on τ=1 data, but this dependency is unexamined.** If the initial training period is unrepresentative (e.g., low-traffic season or structurally atypical graph), the frozen backbone may be systematically misaligned with later periods. This is an acknowledged architectural constraint but goes completely unacknowledged as a limitation.

- **Ablation results reported as approximate bar chart values rather than precise numerical table (Figure 4).** On AIR-Stream where inter-model differences are already small, approximate values (~15, ~20, etc.) make it impossible to assess whether component contributions are statistically meaningful on that dataset.

### Trivial

- **Inconsistency in Section 5.5:** The efficiency analysis text says "PEMS-Stream and AIR-Stream" but Figure 8 shows scatter plots for PEMS-Stream and CA-Stream. Minor proofreading oversight.

---

## Nice-to-Haves

- A precise numerical table for the ablation study to replace Figure 4's bar charts.
- A separate FreNet-only ablation row; currently w/o DLGA is tested but w/o FreNet is not, despite the text claiming "FreNet makes a notable contribution."
- Reporting total parameter count over time as the bank grows would clarify practical deployability; the paper claims "storage efficiency" (Section 4.2) without quantifying total model size at end-of-stream.
- A non-continual offline oracle (backbone trained on all data jointly) to establish a ceiling and clarify how much gain comes from backbone design vs. the continual mechanism.
- A brief mechanistic explanation of why the prediction objective induces pattern-bank clustering, to complement the already-convincing t-SNE visualization.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"Prompt-Based Guidance" label is imprecise:** This is a framing nuance. The mechanism (DiT-style adaptive layernorm gating, Eq. 5) is clearly described and correctly cited (Peebles & Xie, 2023). No substantive error.
- **Conventional STGNN baselines trained from scratch inflate the comparison:** The paper explicitly states this follows prior work (Chen & Liang, 2025). The meaningful comparison is against CSTF baselines, which the paper treats as primary. The asymmetry is established practice in this subfield.
- **Clustering emergence unexplained mechanistically:** While a brief explanation would be a nice-to-have, the absence does not undermine the empirical validity of the t-SNE results.

---

## Novel Insights

The longitudinal t-SNE case study (Figure 6) — showing that nodes added to the PEMS network in 2017 are correctly assigned to semantic clusters established in 2011, purely via prediction-objective fine-tuning with no explicit cluster supervision — is the most illuminating finding beyond the core benchmarks. It suggests that per-node trainable parameters optimized for prediction form a naturally topology-preserving representation space, and that this structure is sufficiently stable to absorb unseen nodes meaningfully. This has implications beyond the CSTF setting for understanding how node embeddings generalize in evolving graphs, and warrants further theoretical investigation.

---

## Suggestions

1. Reframe the continual learning contribution as parameter expansion/isolation and explicitly acknowledge the stability-by-design nature and its trade-offs (e.g., backbone quality depends on τ=1 data, growing model size).
2. Provide a detailed analysis of AIR-Stream performance: why are MAE gains small and RMSE occasionally negative at longer horizons? Is it inherent to meteorological data (smoother distributions, less node heterogeneity)?
3. Replace Figure 4 bar chart ablation with a precise numerical table, especially critical for AIR-Stream.
4. Add a w/o FreNet ablation row to complement w/o DLGA and substantiate the FreNet contribution claim.

---

## Score and Decision

**Calibration anchors (Round 1):**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/FRzCIlkM7I.md` — EAC paper (the main baseline in STBP), avg 6.75, Round 1. STBP substantially improves on EAC on two out of three datasets; similar architectural philosophy but with a more capable backbone.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/URCfZ2NgaR.md` — Continual MTS forecasting (SKI-CL), avg 5.33, Round 1. Rejected; analogous framing issues and weaker empirical results than STBP.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/B1TnT6lUnU.md` — Same SKI-CL paper (different version), avg 4.40, Round 1. Rejected.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/uiyljVIP0k.md` — S2GNN unifying STGNN approaches, avg 5.40, Round 1. Rejected with borderline scores; narrower contribution than STBP.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rjuZyMfLSd.md` — Continual system dynamics learning, avg 6.25, Round 1. Accepted; comparable scope but narrower application.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/rLlDt2FQvz.md` — N-ForGOT open temporal graph, avg 6.25, Round 1. Accepted; comparable.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/akKNGGWegr.md` — ST graph knowledge distillation, avg 5.25, Round 1.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/mkjKqeBXkt.md` — KITS kriging with increment training, avg 5.67, Round 1.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/0je4SA7Jjg.md` — CeGNN spatiotemporal learning, avg 3.40, Round 1.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5x9kfRXhBd.md` — STGAT Forex forecasting, avg 3.00, Round 1.

**Bracketing:** The most directly comparable paper is EAC (avg 6.75), which is both the main baseline and a paper with a nearly identical architectural philosophy (frozen base model + expandable prompt pool for CSTF). STBP improves on EAC substantially on two datasets, presents a more capable backbone, and adds interpretability analysis — but shares EAC's key limitation of parameter isolation rather than genuine forgetting mitigation. The AIR-Stream weakness and framing issue are real but not fundamental. Initial bracket: **6.0–7.0**.

**Narrowing:** STBP's empirical gains over EAC are larger than what is typical to separate a borderline accept from an accept in this space. The backbone innovation (FreNet + linear graph attention) is non-trivial on top of EAC's contribution. However, the framing issue around catastrophic forgetting and the unexplained AIR-Stream degradation prevent a high-end score. The paper sits above EAC in empirical terms but has similar or slightly worse framing clarity. Final score: **6.5**.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>