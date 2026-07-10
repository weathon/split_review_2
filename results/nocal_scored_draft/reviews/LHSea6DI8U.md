The favorability scores confirm the strengths are uniformly strong (1.00) and weaknesses are manageable (0.14–0.42). The most impactful negative is the undiscussed AIR-Stream gap. Let me now produce the final review.

## Summary

This paper proposes STBP, a framework for continual spatio-temporal forecasting that combines a general-purpose backbone (frequency-domain network + dual-stream linear graph attention) with an expandable contextual pattern bank that uses prompt-based gating to adapt to evolving data without retraining. The backbone remains frozen after initial training to preserve general knowledge, while the pattern bank expands to capture new node-level patterns. Experiments on three real-world streaming datasets show STBP outperforms CSTF baselines, with large margins on traffic data (21%+ MAE reduction) and modest gains on air quality data (2.35%).

## Strengths

- **Well-motivated architectural synthesis.** The paper identifies four concrete challenges for CSTF — distributional drift, dynamic spatial correlations, catastrophic forgetting, and efficient incremental adaptation — and designs components that directly address each: FreNet for drift, DLGA for dynamic correlations, frozen-backbone+expandable pattern bank for forgetting, and prompt-based gating for efficient collaboration. The coherence between problem analysis and design is a genuine strength.

- **Strong empirical results on traffic domains.** On PEMS-Stream and CA-Stream, STBP reduces average MAE by 21.44% and 21.93% respectively over the best CSTF baseline. These are large, practically meaningful improvements. The few-shot setting (Table 2) shows even larger relative gains, demonstrating effectiveness at extracting signal from limited data.

- **Efficiency-conscious design with evidence.** The paper provides both architectural reasoning (linear attention avoids O(N²) complexity) and empirical validation (Figure 8, toy dataset ablation comparing O(N) vs O(N²) variants). STBP's efficiency is competitive with simpler CSTF methods like EAC, showing that performance gains do not come at prohibitive computational cost.

- **Qualitative analysis of the pattern bank.** The t-SNE visualizations (Figures 3 and 6) show that the pattern bank autonomously discovers meaningful node clusters without explicit clustering supervision, and new nodes from later periods are correctly grouped into existing clusters. This directly validates the claimed "relevance and heterogeneity" discovery and demonstrates the pattern bank's continual adaptation capability.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Undiscussed domain-dependent performance gap.** The AIR-Stream improvement (2.35% MAE reduction) is roughly an order of magnitude smaller than the traffic-domain improvements (~21%). The paper does not discuss this discrepancy, nor does it report statistical significance to establish that the 2.35% gap is reliable. The abstract and contributions claim "significant outperformance" across datasets without caveat. The method working very well on traffic but modestly on air quality is still useful, but the framing should acknowledge this domain dependence. *(Favorability: 0.14 — the most impactful weakness.)*

- **Missing ablation isolates FreNet's contribution incompletely.** The ablation study lacks a *w/o FreNet* variant that keeps DLGA but replaces the frequency-domain network with a standard temporal module (e.g., TCN or RNN). The only test involving FreNet replacement is the *w/o Backbone* variant, which simultaneously replaces both FreNet and DLGA with CNN and GCN. This makes it impossible to determine whether FreNet's frequency-domain processing independently contributes to handling distributional drift, as claimed. *(Favorability: 0.25.)*

### Trivial

- **EAC listed as an ablation variant.** EAC is a separate published method, not a component removal of STBP. Listing it as the fifth ablation variant alongside true ablations (w/o DLGA) conflates comparison with ablation and could confuse readers about what the ablation study is designed to test. *(Favorability: 0.42.)*

- **Asymmetric baseline treatment is briefly justified.** GWNet and STID are retrained from scratch each period while iTransformer receives online fine-tuning. The paper follows the standard CSTF evaluation protocol (Chen & Liang, 2025), and the ablation study includes both "Retrain" and "Online" variants. However, the justification in the main text is brief, and a clearer caveat about the differing protocols in Table 1 would help. *(Favorability: 0.28.)*

## Nice-to-Haves

- Add a *w/o FreNet* ablation variant that replaces FFT processing with a standard temporal module while keeping DLGA intact.
- Include statistical significance tests for the AIR-Stream results.
- Discuss the AIR-Stream gap explicitly: why the gap narrows, and whether domain characteristics (hourly vs 5-min sampling, different noise patterns) explain the difference.
- Consider discussing how the pattern bank would behave under very-long-term deployment with many periods (e.g., pruning or saturation mechanisms) as future work.

## Removed Points

These points were raised in the input review but removed after cross-checking against the paper:

- **"Unfair baseline configuration" as a Critical Issue**: The reviewer claimed the GWNet/STID vs iTransformer asymmetry is unfair and "unexplained." However, (a) the paper explicitly explains the asymmetry (line 187: iTransformer is "scenario-agnostic"), (b) this follows the standard evaluation protocol in the CSTF literature (Chen & Liang, 2025), and (c) the ablation study tests both "Retrain" and "Online" variants. The primary comparison is against CSTF baselines, not conventional STGNNs, so this does not threaten the core claims. Demoted to Trivial and retained above.

- **"Intervals likely overlap substantially" for AIR-Stream**: The claim that PECPM (24.21±0.43) and STBP (23.64±0.23) intervals "likely overlap substantially" is not supported. At 1σ there is no overlap; at 2σ the overlap is marginal. The broader point about missing significance testing is retained.

- **"Numerical results are imprecise" in ablation**: Bar charts with approximate values are a standard presentation format for ablation studies.

- **Pattern bank growth over many periods**: The paper already addresses linear scaling in the efficiency analysis. Pruning/saturation mechanisms are reasonable future work.

## Novel Insights

None beyond the paper's own contributions. The review surfaces useful framing but does not identify unrecognized strengths or weaknesses that the paper itself does not discuss.

## Suggestions

- Add a *w/o FreNet* ablation variant that keeps DLGA but replaces the frequency-domain network with a standard temporal module (TCN or RNN).
- Discuss the AIR-Stream gap explicitly, including whether the improvement is statistically significant.
- Include exact numerical values in a supplementary table alongside the ablation bar chart (Figure 4).

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>