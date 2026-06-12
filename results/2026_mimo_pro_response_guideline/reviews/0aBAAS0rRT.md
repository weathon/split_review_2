Now I have enough calibration data. Let me write the final review.

**Round 1 bracket: 5.5–7.0**

Key anchor comparisons:
- **Wi-GATr (9TClCDZXeh.md, 7.00)**: Very topically close — wireless signal simulation with 3D geometry using transformers. Our paper has more comprehensive ablations but weaker claim-evidence alignment.
- **Foundation Model for ECC (7KDuQPrAF3.md, 6.25)**: Similar "foundation model" framing with oversold scope, but accepted.
- **EM-GANSim (29JDZxRgPZ.md, 6.00)**: Similar domain, weaker approach, rejected. Our paper is substantially more thorough.
- **DASFormer (7ipjMIHVJt.md, 5.25)**: Self-supervised pre-training paradigm but less comprehensive.
- **WiFi mesh regression (q3WzT2mrhB.md, 4.00)**: WiFi CSI-based but much less sophisticated.
- **SmartPretrain (Bmzv2Gch9v.md, 6.75)**: Self-supervised pre-training with cross-dataset generalization.

**Narrowed bracket: 6.0–6.5**. Our paper is clearly above EM-GANSim (6.00) and DASFormer (5.25), comparable to Foundation Model for ECC (6.25), but below Wi-GATr (7.00) due to claim-evidence mismatch. Final score: **6.0**.

---

## Summary
This paper proposes SigMap, a two-stage foundation model for wireless localization combining (1) cycle-adaptive masked autoencoding pre-training that disrupts periodic CSI shortcuts, and (2) geographic prompt tuning that encodes 3D environment maps via GNN on Delaunay triangulation into soft prompt tokens prepended to the frozen transformer backbone. The model achieves state-of-the-art localization accuracy on DeepMIMO and WAIR-D benchmarks with significant few-shot cross-scenario transfer.

## Strengths
- **Domain-specific cycle-adaptive masking outperforms fixed masking with clear evidence**: Table 3 shows 0.673m MAE / 84.5% CDF@1m vs. 0.770m / 80.3% (grid) and 0.753m / 75.3% (strip), directly validating the masking contribution described in §3.3.
- **Geographic prompt tuning via GNN on Delaunay-triangulated 3D geometry is novel and effective**: Tables 1–2 show map prompts reduce single-BS MAE from 2.275m to 1.564m (31.2%) and multi-BS MAE from 0.789m to 0.673m (14.7%). Table 4 shows robustness even with simplified 2D input (8% degradation), confirming topological/LoS cues drive gains.
- **Cross-scenario transfer with frozen backbone and few-shot adaptation**: The generalization table shows 1.026m MAE on unseen DeepMIMO O2 and 1.880m on 100 unseen WAIR-D city scenes using only ~100 target samples and 0.4% parameter updates, outperforming LWLM by 44–53%.
- **Clean ablation structure**: Tables 3 (masking), 4 (map modality), and the generalization table isolate individual component contributions clearly.
- **Practical parameter efficiency**: Table 5 quantifies 0.085M trainable params (0.7%), 30-min fine-tuning, 0.83ms/sample inference.

## Weaknesses

### Fatal
None.

### Major
- **Zero-shot claim unsupported by experiments**: The abstract (line 9) claims "strong zero-shot generalization" and §1.2 (line 43) reiterates "strong zero-shot generalization to unseen environments." However, §4.5 (line 317) explicitly describes "few-shot learning" with "approximately 100 instances per scenario" where "only the downstream task heads are fine-tuned." Fine-tuning on 100 labeled target samples is few-shot adaptation, not zero-shot. This is a direct claim-evidence mismatch on the paper's central contribution narrative.
- **NLoS-aware attention (Eq. 11) introduced in results, not methodology**: Equation 11 at line 248 in §4.2 is presented as "the key advantage" for single-BS NLoS localization and involves a trainable weight matrix W_NLoS, but this component is never described in §3 (Methodology). The methodology section does not mention this mechanism. A reader cannot understand or reproduce the complete model from §3 alone.
- **Generalization experiments compare against only one baseline**: Tables 1–2 compare against OMP, CNN, SWiT, and LWLM, but the generalization table drops all baselines except LWLM without explanation. If other baselines fail to generalize, showing that explicitly would strengthen the cross-scenario contribution considerably.

### Minor
- **Text-table numerical discrepancy**: Line 340 reports "1.580 m on WAIR-D Scenario-2" but the table shows 1.880m. The 44.3% improvement matches 1.880, confirming 1.580 is a typo.
- **Error bars referenced but not shown**: Line 301 claims "near-overlapping error bars indicate that most of the topological benefit is retained" but Table 4 contains no error bars.
- **"Foundation model" framing for single-scenario pre-training**: The model is pre-trained on one DeepMIMO scenario (O1_3p5). While transfer results are encouraging, the "foundation model" label implies broad pre-training diversity not demonstrated here.
- **Cross-correlation computation for d_final underspecified**: §3.3 describes detecting periodicities via "cross-correlation analysis" (line 133) and defines the mask pattern in Eq. 6 conditioned on d_final, but does not provide the algorithm for computing d_final itself. This affects reproducibility of the first listed contribution.

### Trivial
- "Table 4.5" referenced (line 317) but the generalization table has no proper table number.

## Nice-to-Haves
- Test actual zero-shot generalization (no target-domain labels; apply pre-trained model + geographic prompt directly) to validate the abstract's central claim.
- Ablate the number of prompt tokens (single GlobalMeanPool vector vs. K tokens from different spatial regions) to assess the information bottleneck from compressing entire city geometry into one vector.
- Include all baselines in generalization experiments to show which fail to transfer.
- Acknowledge that all experiments use simulated CSI and discuss the gap to real-world deployment.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Harsh critic's concern about dedicated MLP heads scaling with number of BSs (line 225) — speculative, not tested, and not obviously problematic given the multi-BS attention fusion design.
- Harsh critic's note about single-BS masking ablation missing from Table 3 — this is a nice-to-have, not a flaw; the multi-BS results still demonstrate the masking contribution clearly.
- Critic's claim that "foundation model" framing "oversells" the contribution — partially valid (kept as minor), but the core technical contributions are genuine regardless of framing.

## Novel Insights
The paper's core technical insight — that wireless CSI has periodic structure that standard MAE masking fails to disrupt, combined with the idea that geographic topology can be encoded as soft prompt tokens via GNN on Delaunay triangulation — is genuinely novel and well-motivated by the wireless domain. The cycle-adaptive masking is a principled contribution that addresses a real problem with masked autoencoding on periodic signals. The combination of these ideas into a transferable framework with demonstrated few-shot adaptation across different ray-tracing engines is a meaningful contribution.

## Suggestions
- Either run a true zero-shot experiment or correct claims throughout to accurately describe few-shot transfer.
- Move Equation 11 and its description into §3 to make the methodology complete.
- Add all baselines to the generalization table.
- Fix the WAIR-D MAE typo (1.580 → 1.880).
- Specify the cross-correlation algorithm for computing d_final.

## Calibration Report

**All anchors retrieved:**
| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| gwZ90hFSL2 (Chinese NLP for humanoid robots) | 1.00 | 1 | Unrelated topic, strong reject |
| 8QTpYC4smR (LLM systematic review) | 1.00 | 1 | Survey paper, strong reject |
| nSDOkm0SKo (Financial market neural networks) | 1.00 | 1 | Unrelated, strong reject |
| 7zJDTnogdG (ECG foundation model) | 3.33 | 1 | Self-supervised FM for ECG; weaker generalization claims |
| I0To0G5J7g (Online self-improvement for embodied FMs) | 3.20 | 1 | Different domain |
| XhdckVyXKg (Wearable sensing FM) | 3.00 | 1 | Foundation model for wearable data |
| DYXl6P70aH (FM robustness for remote sensing) | 3.00 | 1 | FM benchmarking paper |
| 7ipjMIHVJt (DASFormer, earthquake monitoring) | 5.25 | 1 | SSL pre-training paradigm, less comprehensive |
| 72MSbSZtHv (RedMotion, motion prediction) | 5.33 | 1 | Self-supervised redundancy reduction |
| uiBLOcyTIA (NextLocLLM) | 5.25 | 1 | LLM for location prediction |
| nf4v09zw6O (SSL for object detection) | 5.25 | 1 | SSL pre-training with ViT |
| ReccFdn4zE (Cross attention for oddly shaped data) | 2.00 | 1 | Different topic |
| q3WzT2mrhB (WiFi mesh regression) | 4.00 | 1 | WiFi CSI-based, much weaker than our paper |
| Q53QLftNkA (MW-MAE for audio) | 5.25 | 1 | Masked autoencoder variant |
| JfcLYCqOkQ (Conditional MAE) | 4.75 | 1 | MAE masking study |
| 9TClCDZXeh (Wi-GATr, wireless simulation) | 7.00 | 1 | Topically closest; wireless + 3D geometry + transformers. Our paper is comparable in novelty but has claim-evidence issues |
| klpdEThT8q (MA²E, multi-agent RL) | 6.25 | 1 | Masked autoencoder for MARL |
| PvyOYleymy (Masked completion via diffusion) | 6.75 | 1 | White-box transformer for unsupervised learning |
| 29JDZxRgPZ (EM-GANSim) | 6.00 | 1 | EM simulation GAN; our paper is more thorough |
| PdwrCm5Msr (MapLearn, indoor mapping via audio) | 4.75 | 1 | Indoor mapping from audio signals |
| pQOHbTpAwf (DeepNT, network tomography) | 5.25 | 1 | GNN for network inference |
| F8l0llkMk0 (Map equation goes neural) | 3.33 | 1 | Community detection |
| S2WUJUETyc (DAS + PINN for sound localization) | 4.00 | 1 | Acoustic sensing localization |
| 5sjxMwWmk8 (GNNSync, angular synchronization) | 6.25 | 1 | GNN for synchronization problems |
| Pj3ErOxlLo (NaviFormer, navigation) | 6.00 | 1 | Transformer for path planning |
| 7KDuQPrAF3 (FM for Error Correction Codes) | 6.25 | 1 | Very similar concept: FM for comm domain, oversold scope but accepted |
| JYTQ6ELUVO (Specialized FMs struggle) | 6.50 | 1 | Meta-analysis of FM claims |
| Bmzv2Gch9v (SmartPretrain, motion prediction) | 6.75 | 1 | SSL pre-training with cross-dataset generalization |
| PdaPky8MUn (Never Train from Scratch) | 8.00 | 1 | High-quality theory paper |
| vrBVFXwAmi (LLM4QPE) | 8.00 | 1 | Pre-training paradigm for quantum |
| qssVptHTPN (Locality Alignment for VLMs) | 6.00 | 1 | ViT post-training for spatial reasoning |
| fQSZMrjW8X (LocDiffusion, geolocalization) | 5.80 | 1 | Diffusion for image geolocalization |
| QaQrWKPWdG (Few-shot species range) | 5.75 | 1 | Few-shot spatial estimation |
| MBBRHDuiwM (URLOST) | 6.40 | 1 | Unsupervised representation learning |
| IAFStwZPNu (Brain speech decoding SSL) | 5.67 | 1 | SSL for brain signal decoding |

**Round 1 bracket: 5.5–7.0.** Our paper sits clearly above EM-GANSim (6.00, rejected) and DASFormer (5.25, rejected), comparable to Foundation Model for ECC (6.25, accepted with similar oversold claims), and below Wi-GATr (7.00, accepted with stronger methodology).

**Final score: 6.0.** The paper makes genuine technical contributions (cycle-adaptive masking, geographic prompt tuning) with comprehensive experiments, but is held back by the zero-shot claim being unsupported (experiments are few-shot), a key model component missing from the methodology, and incomplete baseline comparison in the generalization setting.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Reject</decision>