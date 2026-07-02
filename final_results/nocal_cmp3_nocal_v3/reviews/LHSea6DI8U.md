Now let me compile the final review.

## Summary

This paper proposes STBP, a framework for continual spatio-temporal forecasting that combines a frequency-domain backbone (FreNet) with linear graph attention (DLGA) and an expanding contextual pattern bank. The backbone stays frozen after initial training to preserve general knowledge, while the pattern bank expands and fine-tunes to adapt to new data distributions, using prompt-based gating and attention mechanisms to interact with the backbone. Experiments on three real-world datasets show improvements over state-of-the-art baselines, particularly on traffic datasets.

## Strengths

- **Well-motivated architectural decomposition.** The separation of a frozen general-purpose backbone (handling distributional drift and dynamic spatial correlations) from an expanding pattern bank (handling adaptation and forgetting) directly addresses a known limitation in CSTF methods — weak backbones with poorly coupled adaptation mechanisms. The design is principled and clearly explained.

- **Frequency-domain temporal processing (FreNet, §4.3).** Using FFT/IFFT with a learnable frequency embedding to emphasize stable periodic/trend components while suppressing high-frequency noise is a sensible and computationally efficient choice for continual forecasting under distribution shift.

- **Dual-stream linear graph attention (DLGA, §4.3).** Incorporating the pattern bank as an additional key stream within random-feature-map linear attention simultaneously reduces spatial complexity from O(N²) to O(N) and provides a clean mechanism for the pattern bank to influence spatial attention. This is a non-trivial integration of continual learning and efficient spatial modeling.

- **Thorough evaluation scope.** The paper evaluates on three real-world datasets (two traffic, one air quality), includes seven competitors spanning conventional STGNNs and CSTF methods, reports MAE/RMSE/MAPE across three horizons, and supplements with few-shot analysis (§5.2, Table 2), ablation (§5.3), parameter sensitivity (§5.3), t-SNE case studies (§5.4), and efficiency analysis (§5.5). This is more comprehensive than typical CSTF papers.

## Weaknesses

### Fatal
None.

### Major

1. **Results are sharply uneven across datasets, and the paper does not engage with this disparity.** On PEMS-Stream and CA-Stream (traffic), STBP beats the best baseline by ~21.44% and ~21.93% in average MAE. On AIR-Stream (air quality), the improvement collapses to 2.35% (line 238). For RMSE at horizons 6 and 12 on AIR-Stream, STBP's reported values are numerically close to or marginally above the second-best (table lines 179–180). The paper claims a "general" backbone (title, §4.3) but never discusses *why* performance is dramatically lower on the non-traffic dataset — whether due to weaker periodicity (reducing FreNet's advantage), different spatial correlation structure, or other factors. The lack of analysis weakens the generality claim and is the paper's most significant gap.

2. **No per-period performance trajectories and no direct measurement of forgetting.** The paper reports metrics averaged over all incremental periods (line 142) but never shows how performance evolves period by period — whether accuracy degrades, plateaus, or improves. For a continual learning paper claiming to "mitigate catastrophic forgetting" (abstract, §6), the absence of any direct forgetting measurement (e.g., accuracy on earlier periods after training on later ones) is a notable gap that makes it difficult to assess the method's continual-learning properties.

### Minor

3. **Ablation study would benefit from a cleaner control isolating the pattern bank's contribution.** The paper ablates the pattern bank via "Retrain" (train from scratch each period) and "Online" (fine-tune across periods), but both change the training protocol (unfreezing the backbone). A variant that keeps the backbone *frozen* exactly as in STBP but removes the pattern bank (compensating with additional backbone capacity) would more cleanly isolate whether the pattern bank — rather than the backbone architecture or freezing strategy — drives the gains. The existing ablations are still supportive (removing either component hurts performance), but this design ambiguity weakens the causal claims about the pattern bank's role.

4. **Privacy protection and storage efficiency claims are asserted without evidence.** The paper states (§4.2, line 104) that because the pattern bank "encodes high-level abstractions rather than raw historical data," it offers "privacy protection and storage efficiency." No storage comparison against replay-based baselines is provided, and the privacy claim (node-specific learned embeddings can be reverse-engineered or correlated with sensitive attributes) is much stronger than the paper can support. These claims should be removed or substantially qualified.

5. **The "general" claim is stretched by the domain coverage.** The method is evaluated on only two domains (traffic and air quality). While the traffic results are strong, the marginal improvement on air quality combined with only two domains does not warrant the "general" label without explicit qualification about where the method excels and where it does not.

### Trivial
None.

## Nice-to-Haves

- **Explicitly state the reference baseline for percentage improvements** (e.g., "against the best CSTF baseline"). The current phrasing ("best baseline," line 238) is ambiguous between all models and CSTF-only models.
- **Add a direct analysis of forgetting**, e.g., accuracy on earlier periods after training on later periods, which is standard practice in continual learning evaluations.
- **Show per-period performance trajectories** to demonstrate whether the method maintains, improves, or degrades over time.
- **Discuss why AIR-Stream sees only marginal gains** — this would strengthen rather than weaken the generality claim by making its scope more precise.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *Criticism about the FreNet output being T_h rather than T_f* — the paper explicitly states the output is "passed through a prediction layer" after the second FreNet (§4.3, line 110). The reviewer's question is already addressed.
- *Criticism about the ablation bar chart showing approximate (~) values* — these are parser-rendered approximations from a figure; the original paper has precise values.
- *Criticism that §2 (Related Work) "reads as a laundry list"* — this is a subjective formatting opinion without specific evidence of a factual gap.
- *Criticism that the conventional STGNN baselines "inflate the apparent improvement"* — the paper explicitly notes these are retrained from scratch (line 187) and the percentage improvements in context clearly refer to the CSTF best baseline; the text is sufficiently clear.
- *Criticism about the three-group design lacking rationale* — a reasonable question but not a weakness; each group's function is described. The paper could benefit from a brief justification but its absence is not a flaw.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add per-period performance metrics and a direct forgetting measurement (e.g., accuracy on earlier periods after later training) to substantiate the continual-learning claims.
2. Include a frank discussion of why AIR-Stream sees only 2.35% improvement — domain characteristics, data frequency, or spatial structure — to make the generality claim precise rather than overbroad.
3. Add the cleaner ablation control: frozen backbone without pattern bank, compensated with additional hidden dimension or layers.
4. Remove or substantially qualify the privacy claim; add a storage comparison against replay-based baselines if keeping the storage claim.

## Score and Decision

<score>6.5</score>
<decision>Accept</decision>