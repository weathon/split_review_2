Now I have enough to write the consolidated review. Let me draft it.Based on the calibration results, I can establish my bracket:
- Papers in the 3.5–5.5 range are wireless/signal papers with moderate novelty and some issues.
- The closest topically relevant anchor is `9TClCDZXeh.md` (avg 7.0): "Differentiable and Learnable Wireless Simulation with Geometric Transformers" — a wireless+geometry paper with strong technical contributions and clean evaluation.

**Round 1 Bracket:** 4.5–6.0. The core technical contribution (cycle-adaptive masking + map-as-prompt) is genuinely novel and well-motivated, placing it above the ~4.0 reject tier. However, the actively misleading "zero-shot" claim in the abstract, unsubstantiated AoA/ToA/oss_scenario axes in Figure 5, and a 16% numerical inconsistency in the primary result (1.880 vs. 1.580 m) are Major issues that prevent clean acceptance, placing it below the 6–7 tier of clean, publication-ready wireless papers.

**Final Score: 5.0** — Borderline reject. The contributions are real, but the false abstract claim, unsupported figure dimensions, and numerical inconsistency must be resolved before acceptance.

---

## Summary
SigMap is a two-stage wireless localization foundation model combining (1) cycle-adaptive masked autoencoding for CSI pre-training, where masks exploit detected periodicity to prevent shortcut learning, and (2) a "map-as-prompt" fine-tuning mechanism that encodes 3D building geometry via a shallow GCN into a single soft-prompt token prepended to the Transformer input. Experiments on DeepMIMO and WAIR-D (100 OpenStreetMap city scenes) demonstrate strong localization accuracy and parameter-efficient cross-scenario adaptation with ~100 labeled samples.

## Strengths
- **Cycle-adaptive masking (Section 3.3):** The periodicity-aware masking design is technically grounded. CSI contains genuine periodic structure from antenna arrays and OFDM subcarriers that naive random masking can be bypassed by interpolation. The cross-correlation-based periodicity detection and shift-aware masking (Eq. 6) is a motivated design, not a heuristic. Table 3 confirms a meaningful advantage over fixed masking: +4.2 pp CDF@1m over grid masking.
- **Map-as-prompt design (Section 3.4):** Encoding 3D building geometry as a single GCN-generated soft-prompt token is elegant and nearly parameter-free (0.7% of parameters, Table 5). Table 4 shows 2D bird's-eye maps retain 92% of 3D map benefit (1.692 vs. 1.564 MAE), supporting robustness of topological signal over fine geometric detail and lowering deployment cost.
- **Cross-domain transfer (Section 4.5):** Adapting with ~100 labeled samples on WAIR-D Scenario-2 (100 real-world OSM city scenes) and outperforming LWLM by 44.3% in MAE while updating only 0.4% of parameters is a compelling few-shot generalization result across substantially different environments.

## Weaknesses

### Fatal
None.

### Major
- **Zero-shot claim in abstract and Section 1.2 is factually incorrect.** The abstract states the model "exhibits strong zero-shot generalization in unseen environments," and Section 1.2 repeats "demonstrates strong zero-shot generalization." But Section 4.5 explicitly states: "only the downstream task heads are fine-tuned using limited target samples (approximately 100 instances per scenario)." Updating task heads on labeled target samples is **few-shot transfer learning**, not zero-shot inference. Zero-shot would mean predictions in a new environment with no target labels at all. This framing is actively misleading and must be corrected to "few-shot generalization." If the model genuinely supports zero-shot inference (prompt from map only, zero target labels), that experiment should be demonstrated.
- **Figure 5 radar chart includes unsubstantiated evaluation dimensions.** Figure 5 plots eight axes: Overall, oss_scenario, NLoS, AoA, ToA, SingleBS, MultiBS, and a second Overall. No AoA error, ToA error, or "oss_scenario" quantitative table appears anywhere in the paper body. These axes imply competitive evaluations that have no corresponding experimental support in the paper, materially overstating the evidential base. Either these axes must be tied to explicit quantitative experiments, or they should be removed.
- **16% numerical inconsistency in the primary cross-domain result.** Table in Section 4.5 (line 336) reports SIGMAP (w/ map) as **1.880 m** MAE on WAIR-D Scenario-2. Two sentences later (line 340), the text states "1.580 m on WAIR-D Scenario-2." A 16% discrepancy in the paper's central few-shot generalization figure is not a rounding issue and erodes confidence in the reported results.

### Minor
- **All evaluation on ray-tracing-simulated data.** All datasets (DeepMIMO O1_3p5, O2, WAIR-D) are generated from ray-tracing or OpenStreetMap-driven simulation. Real channels contain hardware imperfections, calibration errors, and non-ideal scattering not captured by standard ray-tracers. For a paper framing itself as a foundation model for real 5G/6G deployment, the practical significance claim is not directly supported. This should be acknowledged as a limitation.
- **Masking ablation lacks a random-masking baseline.** Table 3 compares grid, strip, and adaptive masking only. The obvious point of comparison for a masked autoencoder paper is standard random masking (as in the original MAE). Its absence makes it unclear whether the gain comes from adaptive periodicity detection or simply from any structured (non-random) masking pattern.
- **Section 4.4 incorrectly references Figure 1.** Line 301 states "Two-dimensional and three-dimensional map ablations are illustrated side-by-side in Figure 1," but Figure 1 shows wireless LoS/NLoS propagation paths, not map ablation comparisons. This is a copy-paste error.
- **Table reference mismatch in Section 4.5.** Line 317 references "Table 4.5," but no table in the paper bears this label — the generalization results table appears inline without a corresponding number.

### Trivial
None beyond the reference errors noted above.

## Nice-to-Haves
- A genuine zero-shot experiment (predict in a new environment with zero target-labeled samples, only using the new map as prompt) would be the paper's strongest contribution if achievable.
- Interpretability analysis of what the geographic prompt token attends to (e.g., correlation between prompt-token norm and LoS/NLoS fraction across test samples) would substantiate the stated mechanism (Section 4.2) rather than asserting it.
- Adding random masking as a baseline in Table 3 to isolate the specific benefit of periodicity-adaptive detection.
- Evaluation on at least one measured (non-simulated) channel dataset to ground the practical deployment claims.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Comparison unfairness (CSI-only baselines vs. map-aided SIGMAP):** The paper already includes SIGMAP (w/o map) as the fair modality-matched comparison (2.275 vs. 2.382 MAE in Table 1). Asymmetry favors baselines, so this critique is removed per filtering rules.
- **Reproducibility of d_final computation (Section 3.3):** Details are likely in the appendix, which the parser strips. Removed per rules on missing appendix content.
- **Generic problem-importance strength:** Removed as non-specific to this paper.
- **Missing related works:** Not assessed (no external sources to verify existence).

## Novel Insights
The most actionable novel insight is that the "map-as-prompt" abstraction — encoding scene geometry into a single prepended soft token via a shallow GCN — may generalize well beyond wireless localization to any task where environmental geometry modulates signal propagation (acoustic localization, indoor radar, RF fingerprinting). The finding that 2D topological maps retain ~92% of the benefit of full 3D meshes has direct practical significance: it suggests that expensive 3D scanning or LiDAR mapping is not required, and that OpenStreetMap footprints alone are sufficient for most of the gain, which is a nontrivial and deployable insight.

## Suggestions
1. Correct "zero-shot" to "few-shot (100-sample)" throughout abstract, Section 1.2, and Section 4.5; or add a genuine zero-shot evaluation to support the current framing.
2. Resolve the 1.880 vs. 1.580 m discrepancy in WAIR-D Scenario-2 MAE by auditing the actual experiment.
3. Remove AoA, ToA, and oss_scenario axes from Figure 5, or add corresponding quantitative tables to the paper body.
4. Add a standard random-masking row to Table 3.
5. Fix the incorrect Figure 1 reference in Section 4.4.
6. Correct the "Table 4.5" label reference in Section 4.5.

## Score and Decision

### Anchor Papers Retrieved
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `gwZ90hFSL2.md` | 1.00 | R1 | Humanoid robot/NLP paper; not topically relevant |
| `I0To0G5J7g.md` | 3.20 (6.25) | R1 | Embodied foundation model with two-stage finetuning; comparable scale but different domain |
| `7zJDTnogdG.md` | 3.33 | R1 | ECG foundation model with SSL; similar SSL+domain-transfer structure but weaker results |
| `XhdckVyXKg.md` | 3.00 | R1 | Wearable sensing foundation model; SSL+heterogeneous adaptation, somewhat analogous |
| `DYXl6L70aH.md` | 3.00 | R1 | Remote sensing foundation model benchmark; different contribution type |
| `q3WzT2mrhB.md` | 4.00 | R1 | WiFi CSI → 3D mesh regression; most topically adjacent in the 3.5–5.5 band |
| `b5lXUwZiD3.md` | 5.25 | R1 | Transformers on HMMs — not topically relevant |
| `9TClCDZXeh.md` | 7.00 | R1 | Wireless simulation with geometric transformers; best topical match, strong geometric+signal contribution |
| `29JDZxRgPZ.md` | 6.00 | R1 | EM-GANSim: ML for wireless EM simulation; similar simulation-only limitation |
| `gFvRRCnQvX.md` | 6.40 | R1 | CrossMPT for error correcting codes; same wireless-DL domain |
| `TPZRq4FALB.md` | 8.00 | R1 | Multimodal TTA; clean contribution with no integrity issues |

**Round 1 bracket:** 4.5–6.0.

`9TClCDZXeh.md` (avg 7.0) is the strongest topical anchor — a wireless+geometry paper with clean evaluation and no false claims. The current paper matches its contribution level in novelty of the map-as-prompt idea, but is dragged down by three verifiable Major issues: a false zero-shot claim in the abstract, unsupported radar chart dimensions, and a numerical inconsistency in the primary result. These issues individually are correctable, but together they reflect a lack of editorial rigor that would be weighed against acceptance.

`29JDZxRgPZ.md` (avg 6.0) evaluates EM propagation on simulated data only — similar to this paper's limitation — and scored 6. But that paper doesn't appear to have claim integrity issues.

**Final calibration:** The core contribution sits at ~6 quality, but the combination of false abstract claim + unsupported Figure 5 axes + numerical inconsistency justifies a step down to 5.0.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>