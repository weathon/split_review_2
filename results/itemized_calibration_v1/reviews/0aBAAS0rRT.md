Here is the final consolidated review.

---

## Summary

The paper proposes SigMap, a wireless localization foundation model with two main innovations: (1) cycle-adaptive masked modeling that adapts masking patterns to channel periodicity during self-supervised pre-training, and (2) a "map-as-prompt" framework that encodes 3D building geometry via GNNs into soft prompts for parameter-efficient fine-tuning. Experiments on DeepMIMO and WAIR-D simulated datasets show improvements over OMP, CNN, SWiT, and LWLM baselines.

## Strengths

1. **Map-as-prompt is architecturally clean and well-motivated.** Section 3.4 describes a concrete pipeline: building mesh vertices + BS positions → Delaunay triangulation → 2-layer GCN → global mean pooling → projection → soft prompt token prepended to the frozen transformer's input. The parameter efficiency (0.085M trainable parameters during fine-tuning, 30 min total) is genuinely attractive.

2. **Multi-BS fusion mechanism (Section 3.5, Eq. 9-10) is sound.** The attention-based weighted fusion across base stations is a sensible instantiation, and the 4-BS collaborative results (0.673m MAE, 84.5% CDF@1m) represent a clear improvement over the single-BS baseline.

3. **The paper targets a technically important problem.** NLoS wireless localization for 5G/6G, and the specific difficulty of periodic shortcuts in CSI during masked pre-training, are domain-authentic issues that are well-motivated in Sections 1 and 2.1.

## Weaknesses

### Fatal

None.

### Major

1. **Cycle-adaptive masking mechanism is underspecified to the point of irreproducibility.** Equation 6 defines the mask pattern given `d_final` (detected periodicity shift), but the paper never explains how `d_final` is computed. The text states "we compute shift patterns using cross-correlation analysis" (line 133) and "computing row-wise cross-correlation" (line 41), but does not specify what signals are being correlated, how the dominant periodicity is extracted, or how the method differs from a standard sinusoidal model. Additionally, Table 3 shows adaptive masking produces *worse* RMSE (1.099m) than the simpler strip-masking (0.972m) — a reversal that is not discussed. There is also no ablation against random masking at the same mask ratio, which is the canonical control for MAE-style methods. Without these details and controls, the paper's primary claimed innovation cannot be evaluated or built upon.

2. **The "NLoS-aware attention mechanism" — described as "the key advantage" — is introduced only in the evaluation section.** Equation 11 appears in Section 4.2 (line 247) with no prior specification in Section 3 (Methodology). The method section describes standard self-attention (lines 201-205). The reader cannot determine whether this mechanism replaces standard attention, is an additional component, or belongs to the task head. Since the paper itself calls it "the key advantage," its absence from the method section is a serious specification gap that prevents attribution of the reported gains to a documented design.

3. **"Zero-shot generalization" claim is contradicted by the experimental protocol.** The abstract and contributions (lines 9, 43) claim "strong zero-shot generalization in unseen environments." However, Section 4.5 states: "only the downstream task heads are fine-tuned using limited target samples (approximately 100 instances per scenario)." This is few-shot transfer learning, not zero-shot. The headline claim in the abstract is unsupported by the experimental design.

4. **Missing relevant baselines.** The paper cites CrowdBERT, WirelessGPT, LWM, and signal-guided masked autoencoders in the introduction (line 26) as directly related self-supervised methods for wireless localization, but compares against none of them. The actual baseline set (OMP, CNN, SWiT, LWLM) does not include any modern foundation-model-style approach, making the "state-of-the-art" claim unsubstantiated against the most relevant prior work.

### Minor

5. **Data inconsistency in generalization results.** Section 4.5 (line 340) reports "1.580 m on WAIR-D Scenario-2" but the table immediately above (line 336) shows 1.880 m for the same condition. The 44.3% improvement over LWLM is computed from 1.880, not 1.580. This unexplained discrepancy undermines reader confidence in a key result.

6. **No real-world data validation.** All experiments use ray-tracing simulations (DeepMIMO, WAIR-D). The paper motivates the problem with real-world 5G/6G deployment concerns (NLoS errors "over 100 meters") but never validates on real-world channel measurements. While common in this field, the lack of real data limits the contribution's practical significance.

7. **Variance not reported.** Results are "averaged over 5 runs" but tables show only point estimates. Error bars mentioned for the 2D/3D ablation are discussed qualitatively ("near-overlapping") but not shown numerically.

8. **Transformer backbone architecture underspecified.** No description of number of layers, hidden dimension, number of heads, or patch size for CSI tokens. This hurts reproducibility.

### Trivial

None.

## Nice-to-Haves

- Add a random-masking baseline at the same mask ratio to Table 3.
- Add at least one modern wireless SSL method (e.g., CrowdBERT or a standard MAE transformer without cycle-adaptation) to the main comparison tables.
- Clarify how the geographic prompt token interacts with self-attention — is it attended to by CSI tokens?
- Discuss limitations of Delaunay triangulation for capturing radio-propagation-relevant spatial relationships (e.g., line-of-sight occlusion across streets).
- Report variance (standard deviations) in the main result tables.

## Removed Points

These points were flagged by the harsh critic but are removed or downgraded per the filtering rules:

- **"No baseline with standard (non-adaptive) MAE pre-training"**: Partially addressed — Table 3 compares grid-masking and strip-masking (both non-adaptive) against adaptive masking with the same backbone. Downgraded to Nice-to-Have.
- **"Delaunay triangulation cannot capture long-range spatial relationships"**: Speculative and not verified against the paper. Removed.
- **"Pre-training data setup unclear" / "Backbone architecture unspecified"**: The paper references Appendix B for configuration details; the appendix is stripped by the parser. However, basic architecture details should be in the main paper, so the backbone concern is kept as Minor (item 8 above).
- **Criticisms about missing appendix content**: The parser strips appendices; these cannot be evaluated. Removed.
- **"No description of how the prompt interacts with self-attention"**: The paper states the prompt is prepended to the input sequence (line 199) and that attention operates on the extended sequence (lines 201-205). The description is adequate at a high level; moved to Nice-to-Have.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Specify the periodicity detection procedure.** Provide the cross-correlation formula, explain how `d_final` is estimated from data, and report statistics of `d_final` across the dataset.
2. **Move the NLoS-aware attention mechanism (Eq. 11) to Section 3** and abl ate it in experiments. Without this, readers cannot attribute the reported gains to a documented architectural choice.
3. **Correct "zero-shot" to "few-shot transfer" or "parameter-efficient adaptation"** throughout the paper. The actual experimental protocol (100 labeled samples per target scenario) is still interesting and should be honestly labeled.
4. **Add at least one relevant learning-based baseline** from the self-supervised localization methods cited in the introduction (CrowdBERT, WirelessGPT, or a standard MAE transformer).
5. **Resolve the 1.580 vs 1.880 m discrepancy** in Section 4.5.
6. **Report variance** (standard deviation or confidence intervals) in all main result tables.

---

## Score and Decision

**Calibration anchor summary** (all anchors retrieved across rounds):

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| gwZ90hFSL2 | 1.00 | R1 | No | Cross-lingual robotics; unrelated, very weak paper |
| u1cQYxRI1H | 10.00 | R1 | No | Diffusion illumination; unrelated, top paper |
| 8QTpYC4smR | 1.00 | R1 | No | LLM survey; unrelated, very weak survey |
| nSDOkm0SKo | 1.00 | R1 | No | Financial neural networks; unrelated |
| ReccFdn4zE | 2.00 | R1 | No | Cross-attention ionosphere; somewhat relevant (signal+attention), weaker paper |
| QIfzMeTyOu | 2.50 | R1 | No | HAR transfer learning; somewhat relevant (signal transfer), weaker |
| LqB8cRuBua | 2.00 | R1 | No | Signal recognition transformer; somewhat relevant (signal+transformer), weaker |
| eqKHuxIpp5 | 2.50 | R1 | No | On-device transfer learning; somewhat relevant, weaker |
| oVZ9XaOSFK | 4.40 | R1 | **Yes** | MAE masking strategy; **most relevant masking anchor** — had fatal flaw (label leakage during pretraining), my paper does not share this flaw, placing it above 4.40 |
| q6WXlm2Kxo | 5.00 | R1 | No | Masked diffusion; relevant (SSL masking), similar score band |
| nf4v09zw6O | 5.25 | R1 | No | SSL object detection; relevant (SSL), slightly above |
| JfcLYCqOkQ | 4.75 | R1 | No | Conditional MAE; relevant (MAE masking), similar |
| sP0Aev2Gis | 6.33 | R1 | **Yes** | Geographic graph pre-training; **most relevant geographic anchor** — more complete specification, fewer internal inconsistencies, placing my paper below 6.33 |
| fQSZMrjW8X | 5.80 | R1 | No | Image geolocalization; relevant (geo + localization), above |
| AEglX9CHFN | 6.50 | R1 | **Yes** | HG-Adapter for graphs; relevant (prompt tuning), below due to specification gaps |
| FRzCIlkM7I | 6.75 | R1 | No | ST graph prompt tuning; relevant, below |
| 29JDZxRgPZ | 6.00 | R2 | **Yes** | EM-GANSim; relevant (wireless EM) — had similar missing-detail issues but no misleading claims |
| Pj3ErOxlLo | 6.00 | R2 | No | NaviFormer; somewhat relevant |
| YuFUUcSUgx | 4.00 | R2 | No | LRA Transformers; somewhat relevant |
| Pxik3T6Mn9 | 4.50 | R2 | No | Human mobility; somewhat relevant |

**Round 1 bracket**: 4.5–5.5. **Narrowing rationale**: Above oVZ9XaOSFK (4.40) because the fatal methodological flaw in that anchor (label leakage during "self-supervised" pretraining) does not apply here — SigMap's pre-training is genuinely unsupervised MAE. Below sP0Aev2Gis (6.33) because that paper's specification was more complete and it lacked the internal inconsistencies present here (underspecified masking, unplaced NLoS-attention, mislabeled zero-shot). The EM-GANSim anchor (6.00) had similar missing-detail weaknesses (-4 for critical details, -3 for architecture specifics) but no credibility-undermining claim mismatch, placing my paper below it.

**Final score**: 5.0 — The map-as-prompt idea has genuine merit and the parameter efficiency is attractive, but three significant specification/credibility issues (underspecified masking mechanism, unplaced NLoS-attention described as "key advantage," mislabeled zero-shot claim) and incomplete baselines prevent a higher score. The paper is a borderline reject that could be substantially improved with the suggested revisions.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>