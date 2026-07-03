I'll proceed with my assessment since the calibration corpus is unavailable. Let me finalize the review.

## Summary

STBP proposes a framework for continual spatio-temporal forecasting that combines a frequency-domain backbone (FreNet) with a dual-stream linear graph attention mechanism (DLGA) and an expandable contextual pattern bank. The backbone remains frozen after initial training to preserve general knowledge, while the pattern bank is incrementally expanded to capture evolving node-level patterns and mitigate catastrophic forgetting. Experiments on three streaming datasets show strong improvements over CSTF baselines on two traffic datasets (~21% MAE reduction) and more modest gains on an air-quality dataset (2.35%).

## Strengths

1. **Well-motivated architectural design with clean separation of concerns.** The core idea—separating stable spatio-temporal modeling (frozen backbone with frequency-domain processing and linear attention) from adaptable node-specific knowledge (expandable pattern bank updated via parameter expansion)—is principled and clearly articulated. The ablation study validates this separation: the "w/o Backbone" variant (retaining the pattern bank but replacing FreNet+DLGA with CNN+GCN) degrades substantially, confirming that the backbone design contributes independently beyond the continual-learning strategy.

2. **Dual-stream linear graph attention with verified efficiency gains.** DLGA combines random-feature-mapping linear attention (O(N) complexity) with the contextual pattern bank as an additional key stream (Eq. 7–9). The efficiency study (Section 5.5, Figure 8) directly demonstrates the computational benefit: on a toy dataset, the O(N) variant scales to far more nodes at the same GPU memory budget compared to the O(N²) variant, and STBP's overall training time is competitive with lightweight CSTF methods like EAC despite having a more expressive backbone.

3. **Few-shot forecasting evaluation under data scarcity.** Table 2 evaluates all methods with only 10% of training data per incremental period. STBP achieves MAE of 13.58 vs. EAC at 16.13 on PEMS-Stream—a larger relative gap than in the full-data setting—providing evidence that the pattern bank generalizes from limited observations, which is a realistic deployment scenario for new sensors.

4. **t-SNE visualization confirms structured pattern bank representations.** Figures 3 and 6 show that learned pattern bank parameters form meaningful clusters corresponding to distinct traffic patterns, and that new nodes from later periods are correctly grouped into existing clusters without explicit clustering supervision. While qualitative, this supports the claimed relevance/heterogeneity distinction.

## Weaknesses

### Fatal
None.

### Major

1. **Conventional STGNN baselines evaluated under an unnecessarily weak protocol.** Section 5.1 states that GWNet and STID are "retrained from scratch at each incremental stage using only data from the current period"—no parameter reuse, no historical data. Meanwhile, iTransformer gets online training (initialized from previous period's weights), and the CSTF baselines naturally use their own continual-learning mechanisms. The paper justifies this by citing prior work (Chen & Liang, 2025) and by noting that GWNet/STID rely on static graph structures. However, the result is that the main results table conflates "model quality" with "training protocol" for the conventional-STGNN entries. The ablation study's "Online" variant (Section 5.3) partially addresses this by showing that online training on the STBP backbone produces competitive results, but that variant uses the STBP backbone, not the actual GWNet/STID architectures. The paper should also evaluate GWNet/STID under an online (warm-start) protocol to produce a more informative comparison. This does not invalidate the CSTF baseline comparisons (PECPM, STRAP, EAC—which are the main competitors), but it means the conventional-STGNN entries in Table 1 serve as floor markers rather than meaningful competitors.

2. **Advantage over the best CSTF baseline is marginal on AIR-Stream.** The paper reports 2.35% MAE improvement on the meteorological dataset. On RMSE, the gap is tiny (~0.2%, 37.76 vs. 37.83). At horizon 6, a baseline (39.63) actually outperforms STBP (39.81) on RMSE. Standard deviations on several AIR-Stream metrics show overlapping error ranges between STBP and the best baseline. The paper attributes the smaller gap to the nature of the meteorological domain but does not investigate why, nor does it provide statistical significance tests. This weakens the blanket claim of "significantly outperforming state-of-the-art baselines" and suggests the method's advantage is not uniform across domains.

### Minor

3. **Ablation results reported only as approximate values rather than exact numbers.** Figure 4 and its accompanying text show values like "~15", "~20", "~22" instead of exact metrics with standard deviations. Since the ablation study is the most direct evidence for the contribution of individual components (pattern bank, backbone, DLGA, FreNet), presenting approximate values read off bar charts undermines the evidential value. The paper needs a proper ablation table with exact numbers.

4. **No discussion of node removal or graph contraction.** The problem formulation (Definition 1) only describes incremental addition. Real urban sensor networks also contract (decommissioned sensors, road closures). Since the pattern bank stores one vector per node, there is no mechanism described for handling node deletion. This is a real-world limitation that should at least be acknowledged.

### Trivial

5. **The distinction from HimNet's "contextual pattern bank" is unclear.** The Related Work section mentions that HimNet (Dong et al., 2024) uses a "contextual pattern bank," and the proposed method uses the same terminology. The paper describes its own mechanism in detail and notes it is "distinct from existing work" (Section 4.2), but it never explains how STBP's pattern bank differs technically from HimNet's (e.g., construction, update mechanism, role in architecture). A brief clarifying sentence would avoid confusion.

## Nice-to-Haves

- A frequency-response analysis of the learned FreNet embedding could verify the claim that low-frequency components are favored.
- An acknowledgment of the per-node pattern bank's scalability limits for very large sensor networks (e.g., tens of thousands of nodes), with possible mitigations (shared pattern vectors for node groups).
- Zero-shot evaluation for entirely new distributions (frozen backbone, pattern bank only) would directly test the claim that the pattern bank enables adaptation to "new scenarios and distributions."

## Removed Points

These points from the inputs were reviewed against the paper and removed for the following reasons:

- **"t-SNE circular reasoning"**: Removed. The t-SNE is presented as qualitative interpretation of what the pattern bank learns (Section 4.2: "To validate this hypothesis, we conduct a t-SNE-based analysis"), not as primary evidence of effectiveness. The quantitative results and ablation provide the primary evidence.
- **"FreNet frequency response not analyzed"**: Removed. The paper claims the learnable embedding can adaptively highlight stable features; this is a mechanism design claim, and not providing a frequency-response plot is a minor omission, not a weakness.
- **"DLGA dual-stream is just feature concatenation"**: Removed. The dual-stream formulation (Eq. 9) explicitly integrates the pattern bank into the attention computation: (QK^T + QP^T)V. The w/o DLGA ablation validates its empirical contribution. The framing as "just feature concatenation" is dismissive of a legitimate technical integration.
- **"Missing zero-shot evaluation"**: Removed. The paper scopes to continual/incremental learning; zero-shot/few-shot on entirely new distributions is outside this scope.
- **"Modern STGNNs already use adaptive graphs"**: Removed. The introduction's critique is about static *assumptions* and offline training, not about adaptive vs. fixed adjacency matrices. This is a misreading of the paper's motivation.
- **"Conventional STGNN backbones comparison is unfair because it favors the baseline" (asymmetric complaint)**: The asymmetry favors the baseline (iTransformer gets online training while GWNet/STID don't). The critic's complaint is about the protocol difference, not about unfair favoritism toward the proposed method. This is already captured in Major weakness #1.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add exact numerical values with standard deviations to the ablation table (Figure 4) — this is the single most impactful fix.
2. Evaluate GWNet and STID under an online (warm-start) protocol as a supplementary comparison to isolate the effect of the pattern bank + backbone from the effect of parameter reuse.
3. Add a limitations paragraph discussing: (a) the smaller gains on AIR-Stream and potential reasons, (b) how node contraction would be handled, (c) scalability limits of the per-node pattern bank for extremely large graphs.
4. Clarify the technical distinction between STBP's pattern bank and HimNet's pattern bank in one sentence.
5. Report statistical significance tests for the AIR-Stream results to establish whether the remaining gap is meaningful.

## Score and Decision

The paper makes a genuine contribution with a well-motivated architectural separation of stable backbone and adaptable pattern bank for continual spatio-temporal forecasting. The evaluation is thorough on the CSTF baseline front and includes informative ablations, a few-shot study, and efficiency analysis. The two main weaknesses—the unfair conventional-STGNN protocol and the marginal AIR-Stream results—are real but do not invalidate the core contribution, which is supported by strong results on two traffic datasets and well-designed ablation studies. The paper falls in the solid accept range: it has a clear novel contribution, reasonable experiments, and fixable issues that do not threaten the main claims.

**Bracket**: Based on my reading, the paper is clearly above the borderline-accept threshold (it has real contributions and solid evidence) but below the top tier (the evaluation has some weaknesses and the advantage is not uniform). This places it in the **6.5–8.0** range. Within that range, the well-motivated design and good ablation work push it toward the upper end, while the baseline protocol concern and approximate ablation values pull it slightly down.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>