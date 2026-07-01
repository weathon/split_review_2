## Summary

STBP proposes a framework for continual spatio-temporal forecasting (CSTF) that combines (1) a general-purpose spatio-temporal backbone with a frequency-domain network (FreNet) for handling distributional drift and a dual-stream linear graph attention (DLGA) for efficient dynamic spatial modeling, and (2) an expanding contextual pattern bank with prompt-based gating to mitigate catastrophic forgetting. The backbone is frozen after initial training; only the pattern bank expands and fine-tunes in later stages. Evaluated on three real-world streaming datasets (two traffic, one meteorological), STBP achieves strong results on traffic data and competitive results on the meteorological dataset.

## Strengths

- **Clear problem-to-component mapping.** The paper identifies four specific CSTF challenges (distributional drift, dynamic correlations, catastrophic forgetting, backbone-pattern bank coupling) and designs a distinct architectural component for each: FreNet (§4.3, Eq. 6), DLGA (§4.3, Eq. 7–9), expanding pattern bank (§4.2, Eq. 4), and prompt-based gating (§4.2, Eq. 5). The mapping is explicit and the components are functionally distinct.

- **Strong results on traffic datasets.** On PEMS-Stream and CA-Stream, STBP reduces average MAE by ~21–22% relative to the best CSTF baseline (PECPM), with consistent gains across all forecast horizons (3, 6, 12). The few-shot results (Table 2) are also compelling — STBP maintains its advantage when later-period training data is reduced to 10%.

- **Informative efficiency analysis.** Figure 8 directly compares accuracy against training time and GPU memory in a single scatter plot, making the accuracy-efficiency trade-off transparent. The toy-dataset comparison of linear vs. quadratic attention cleanly demonstrates DLGA's computational benefit.

- **t-SNE visualization of the pattern bank provides genuine insight.** Figure 6 shows that the expanding pattern bank produces meaningful clustering of nodes by behavioral pattern without explicit clustering supervision, and that new nodes from later periods are assigned to existing clusters. This directly supports the claim that the pattern bank captures node-level heterogeneity and relevance.

## Weaknesses

### Fatal

None.

### Major

- **Results on AIR-Stream (meteorological data) are marginal and inconsistent with the paper's unqualified claims.** On AIR-Stream, STBP achieves only a 2.35% MAE reduction over the best baseline (PECPM). On RMSE at horizons 6 and 12, STBP is **worse** than PECPM (H6: 39.81 vs. 39.63; H12: 44.97 vs. 44.65). The average RMSE (37.76 vs. 37.83) is within confidence intervals. Despite this, the abstract and introduction claim STBP "significantly outperforms state-of-the-art baselines" and "validat[es] its effectiveness for continual spatio-temporal forecasting" without domain qualification. The paper does not discuss this domain dependence anywhere — not in Section 5.2, the case study (Section 5.4), or the conclusion (Section 6). The claims should be qualified to reflect that the advantage is clear on traffic data but limited on meteorological data, and the paper should discuss possible reasons (e.g., different sampling rates: 5-min vs. hourly; different periodicity structures; different noise characteristics).

### Minor

- **The ablation study raises an inconsistency that needs clarification.** Figure 4 reports EAC as the worst-performing variant across all datasets (e.g., approximate MAE ~26 on PEMS-Stream per the figure description, vs. ~15 for full STBP). However, in the main results (Table 1), EAC is one of the strongest CSTF baselines. If the ablation uses different experimental conditions (e.g., different data splits, hyperparameters, or training protocol), this must be stated explicitly. If the values in Figure 4 are correct, the comparison against EAC in the main table is called into question.

- **The prompt-based gating mechanism (Eq. 5) is underspecified.** The function `h_θ` is described as "an arbitrary submodule within the backbone" without specifying which submodule is used in practice (per FreNet layer? per attention layer?). This affects reproducibility.

- **The random feature mapping φ in DLGA is not fully specified.** The paper states "with Softmax used for approximation in our implementation" (line 130) but does not state the exact feature map used (e.g., the ELU+1 feature map from Katharopoulos et al. 2020, or positive random features). Without this, the linear attention mechanism is not precisely reproducible.

- **No statistical significance test for the AIR-Stream results.** Given that STBP's advantage on AIR-Stream is marginal (2.35% MAE, with RMSE at some horizons actually worse), a pairwise significance test (e.g., Wilcoxon, paired t-test) is needed to verify that the overall improvement is meaningful rather than within noise.

- **The number of incremental periods per dataset is not stated in the main text.** The continual learning scenario (3 periods? 10?) is critical for understanding the setting but must be inferred from dataset descriptions that appear only in the (stripped) appendix.

- **The efficiency claim for FreNet vs. RNNs/TCNs (lines 116–118) is asserted without runtime comparison.** The paper states FreNet offers "higher computational efficiency" than RNNs or TCNs but provides no direct benchmark of this claim in the same setting.

### Trivial

- The privacy protection and storage efficiency advantages claimed for the pattern bank (line 104) are asserted but not experimentally demonstrated.

## Nice-to-Haves

- Add a single ablation variant that removes only FreNet (keeping DLGA + pattern bank) to cleanly separate the contributions of the frequency-domain component from the spatial attention component.
- Include a brief summary of training details (learning rate, optimizer, batch size, number of periods) in the main text for self-containedness, even if full details are in the appendix.

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **"Conventional STGNN baselines are set up as straw men, inflating the apparent improvement."** — REMOVED because it is factually incorrect. The paper explicitly states the improvement is "compared with the best baseline" (line 238), which is a CSTF method (PECPM), not the retrained-from-scratch STGNNs. The 21–22% figures are against the best CSTF competitor, not against weak baselines. The conventional methods are included for completeness and their setup follows prior work (Chen & Liang, 2025).

2. **"w/o Backbone ablation conflates different architectures."** — REMOVED as a minor methodological quibble that does not affect core claims. The ablation replaces the proposed backbone with CNN+GCN, which is a representative backbone used in other CSTF methods. This is a meaningful comparison even if not perfectly controlled for every architectural variant.

3. **"Only one hyperparameter (d) analyzed."** — REMOVED because the paper states additional parameter sensitivity analysis exists in Appendix A.4.5, which is stripped by the parser. The main text shows the most important hyperparameter (feature dimension d), which is reasonable.

4. **"FreNet efficiency claim not benchmarked"** — Kept as a minor weakness (see above) rather than removed entirely, since the claim is made in the main text without direct support.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Qualify the scope of claims in the abstract and introduction to reflect domain-dependent performance. Discuss why STBP excels on traffic (5-min sampling, strong periodicity) but shows limited gains on meteorological data (hourly sampling, different spatio-temporal structure).
2. Reconcile the EAC performance values between the ablation study (Figure 4) and the main results (Table 1), clarifying whether different experimental settings were used.
3. Specify `h_θ` in Eq. 5 (which backbone submodule it selects) and state the exact random feature map `φ` used in DLGA.
4. Add a statistical significance test, particularly for AIR-Stream where the margins are small.
5. State the number of incremental periods per dataset explicitly in the main text.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>