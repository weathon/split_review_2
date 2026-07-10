## Summary

This paper proposes SigMap, a multimodal foundation model for wireless localization that introduces two key innovations: (1) a cycle-adaptive masking strategy that dynamically adjusts masking patterns based on channel periodicity to learn robust wireless representations, and (2) a "map-as-prompt" framework that encodes 3D geographic information via a GNN into soft prompt tokens for parameter-efficient cross-scenario fine-tuning. The model is pre-trained with a masked autoencoding objective on simulated CSI data and evaluated on DeepMIMO and WAIR-D datasets.

## Strengths

- **Parameter efficiency is genuinely demonstrated and practically meaningful.** Table 5 shows fine-tuning updates only 0.085M parameters (0.7% of the total 11.73M), taking 30 minutes for 1000 epochs and 0.83ms per sample at inference. This is a clear, specific, and practically relevant advantage over full fine-tuning.

- **Multi-BS collaborative results are quantitatively strong against the provided baselines.** The multi-BS MAE of 0.673m with CDF@1m of 84.5% (Table 2) is an impressive result given the challenging urban NLoS scenario. The improvement pattern from single-BS (1.564m) to multi-BS (0.673m) is consistent with expected spatial diversity gains, lending face validity to the approach.

- **The "map-as-prompt" idea is creative and well-motivated.** Encoding 3D building geometry into a graph, processing it with a GNN, and injecting the result as soft prompt tokens into a frozen transformer backbone is a genuinely novel connection between geometric reasoning and prompt tuning that is not standard in the wireless localization literature. The map modality ablation (Table 4) showing 3-D → 2-D degrades MAE by only 8% is an informative finding that helps isolate what matters in the geographic representation.

## Weaknesses

### Fatal
None.

### Major

1. **The NLoS-aware attention mechanism — called the "key advantage" (line 247) — is introduced only in the Experiments section (Sec. 4.2, Eq. 11) and is entirely absent from the Methodology section (Sec. 3).** Section 3 describes only standard transformer self-attention (lines 201–205). The reader cannot determine whether this mechanism is part of the pre-trained backbone, used only during fine-tuning, or somehow integrated into the geographic prompt. The paper as written describes one method in Section 3 but evaluates a different method that includes this extra mechanism. This is a structural exposition problem: the headline results cannot be traced back to a clear, unified description of the method that produced them.

2. **The paper claims "state-of-the-art performance" (abstract) but does not compare against the foundation-model approaches it itself cites as the most relevant prior work.** Lines 26–27 cite CrowdBERT (Han et al., 2024), WirelessGPT (Yang et al., 2025), LWM (Alikhani et al., 2024), and signal-guided masked autoencoders (Wang et al., 2025) as prior foundation-model-style approaches for wireless. If the paper's contribution is itself a wireless localization foundation model, these are precisely the methods it should be compared against — they are more relevant than OMP (a classical compressed-sensing algorithm), a plain CNN, or SWiT (a contrastive learning method not designed for localization). A SOTA claim without comparison against the same paradigm is unsubstantiated.

3. **The masking ablation (Table 3) lacks a random masking baseline, which is the standard reference point in the MAE literature.** Table 3 compares "adaptive," "grid," and "strip" masking — all structured masks. The paper's central argument about disrupting "periodic shortcuts" rests entirely on this contrast. Without random masking, the reader cannot distinguish between (a) "cycle-adaptive masking is better because it accounts for signal periodicity" vs. (b) "any unstructured mask that prevents periodic shortcuts would achieve similar gains, and random masking is the natural control." This is a direct evidential gap for a core technical claim.

### Minor

4. **No variance or confidence information is reported despite the paper stating "All results are averaged over 5 independent runs" (line 239).** The paper even mentions "near-overlapping error bars" (line 301) without showing any error bars or standard deviations in any table. Several margins are small enough that statistical significance is not obvious (e.g., adaptive masking MAE 0.673 vs. grid-masking 0.770 in Table 3 — a 0.097m gap).

5. **All experiments use simulated data (DeepMIMO and WAIR-D ray-tracing datasets), but the paper frames its contributions around "practical wireless perception systems" for autonomous driving and smart manufacturing without acknowledging this gap.** Simulated wireless data lacks hardware impairments, thermal effects, human occlusion, and time-varying multipath that affect real deployments. This does not invalidate the method, but the claims about practical deployability outpace the evidence.

6. **The cycle-adaptive masking mechanism (Eq. 6) is underspecified.** The paper states that shift patterns are computed via "cross-correlation analysis" (line 133) but does not specify: (a) which cross-correlation is used (auto-correlation? across subcarriers? across antennas? across time?), (b) how the dominant period is extracted, (c) how parameters d\_final, j\_0, and w are chosen, or (d) how the mask is applied to the complex-valued CSI tensor. These details may reside in the stripped appendix, but the main text is insufficient for understanding or reproduction.

7. **Numerical inconsistency: the text (line 340) states SIGMAP achieves "1.580 m on WAIR-D Scenario-2" but Table 4.5 (line 336) shows 1.880 m for the same entry.** The claimed 44.3% improvement over LWLM is consistent with 1.880 (since (3.375−1.880)/3.375 = 44.3%), confirming that 1.880 is likely correct and 1.580 is an error. This erodes confidence in the reporting.

### Trivial
None.

## Nice-to-Haves

- Add a random masking baseline to Table 3 to make the masking ablation conclusive.
- Report standard deviations or confidence intervals for all main results, especially given the claim of 5 independent runs.
- Acknowledge the simulation-to-reality gap explicitly when discussing practical deployment.
- Describe how the 4D CSI tensor is tokenized into a sequence for the transformer backbone.

## Removed Points
- **"Inadequate handling of signal periodicity claim is presented as categorical but evidence is indirect"** — Opinion about framing, not a verifiable weakness.
- **"How 4D tensor is tokenized not described"** — Valid detail but minor; moved to Nice-to-Haves.
- **"Computational cost of GNN per-sample forward pass not discussed"** — Scope creep; paper focuses on parameter efficiency of fine-tuning, not full inference cost.
- **"Relying on appendix for basic dataset characteristics"** — Appendix stripped by parser; cannot evaluate fairness of this criticism.
- **"No comparison against recent models from other reviews"** — The human finder surfaced generic comparisons; not anchored in this paper's content.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Integrate the NLoS-aware attention mechanism (Eq. 11) into the Methodology section as a proper third contribution, with explanation of how it interacts with the geographic prompt. Alternatively, remove the claim that it is the "key advantage" and attribute gains to the two stated contributions.
2. Add comparisons against at least one foundation-model baseline from the cited related work (e.g., CrowdBERT or signal-guided MAE) to substantiate the SOTA claim.
3. Add a random masking condition to Table 3.
4. Report standard deviations for all tables.
5. Correct the WAIR-D numerical discrepancy (1.580 → 1.880 in line 340).
6. Specify the cross-correlation operation and parameter selection for the cycle-adaptive mask in sufficient detail for reproduction.

---

**Calibration Details:**

*Round 1 bracket:* 4.0–5.5.

*Anchors retrieved (all rounds):*
| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| CBraMod (NPNUHgHF2w.md) | 6.75 | R1 | Yes | Stronger evaluation (12 real EEG datasets, clear architecture). SigMap has less comprehensive evaluation and simulated-only data. |
| DASFormer (7ipjMIHVJt.md) | 5.25 | R1, R2 | Yes | Similar weakness profile (missing baselines, SSL justification). DASFormer uses real sensor data; SigMap has stronger novelty but simulated-only data. |
| SensorLLM (cDd7kg9mkP.md) | 5.50 | R2 | Yes | Similar evaluation gaps (missing baselines, marginal gains over simpler methods). SensorLLM uses real IMU data; SigMap has more creative core ideas. |
| Presto (Iip7rt9UL3.md) | 4.75 | R2 | Yes | Uses real satellite data, broader evaluation. SigMap has stronger architectural novelty but weaker evaluation. |
| Scaling Channel-Invariant SSL (aefNwingnS.md) | 4.40 | R1 | Yes | Limited novelty (applying DINOv2 with bag-of-channels). SigMap has stronger novelty but weaker real-data validation. |
| WiMTR (q3WzT2mrhB.md) | 4.00 | R2 | No | Also uses CSI data, has real-data collection. SigMap more novel architecturally. |
| Partial Channel Dependence (xVU6rY37X9.md) | 4.60 | R2 | No | Time series foundation model. Roughly comparable methodological depth. |

*Final placement:* SigMap sits between DASFormer (5.25) and WiMTR (4.00). Its creative contributions (map-as-prompt, cycle-adaptive masking) exceed those of the Channel-Invariant SSL paper (4.40) and are on par with DASFormer's framing. However, the evaluative weaknesses are more severe than any anchor in the 5.0+ range — specifically, all experiments are on simulated data (unlike any anchor above 5.0), the method description is structurally inconsistent, and the most relevant baselines from the same paradigm are omitted. These issues are addressable in revision but leave the paper's claims insufficiently supported as submitted.

## Score and Decision
MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>