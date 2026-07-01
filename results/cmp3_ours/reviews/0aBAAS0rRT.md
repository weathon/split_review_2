Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper proposes SigMap, a foundation model for wireless localization with two claimed innovations: (1) cycle-adaptive masked modeling for self-supervised pre-training on CSI data that dynamically adjusts masking patterns based on channel periodicity to prevent shortcut learning, and (2) a "map-as-prompt" framework that encodes 3D geographic information via GNN-generated soft prompts for parameter-efficient fine-tuning. Experiments on ray-traced simulated datasets (DeepMIMO, WAIR-D) show strong results and the parameter efficiency numbers (0.085M trainable params, 0.7% of total) are compelling.

## Strengths

- **Well-motivated, domain-specific technical contribution in cycle-adaptive masking.** The insight that CSI periodicity allows models to exploit trivial interpolation shortcuts under standard masked autoencoding is specific to the wireless domain and not a generic SSL trick. The masking strategy that dynamically detects and disrupts periodic patterns (Eq. 6) is a genuine contribution grounded in signal physics. This is clearly the paper's strongest technical idea.

- **Convincing parameter-efficiency results.** Fine-tuning only 0.085M parameters (0.7% of the model) while achieving strong accuracy, with concrete wall-clock times reported (30 min fine-tuning, 0.83 ms/sample inference in Table 5), demonstrates a meaningful practical advantage for deployment scenarios where rapid adaptation matters.

- **Informative ablation on map quality.** The comparison of 3-D mesh, 2-D bird's-eye polygon, and no-map conditions (Table 4) provides useful evidence that most of the benefit from geographic prompts comes from topological/LoS cues rather than full 3-D geometry. This finding is practically useful for deployment scenarios where 3-D maps may be incomplete.

## Weaknesses

### Major

1. **Evaluation on simulated data only, with no real-world validation.** Every experiment uses ray-traced simulated data (DeepMIMO O1_3p5, O2, WAIR-D). The paper is framed as a practical "foundation model" for real-world applications (autonomous driving, XR, smart manufacturing in the abstract) and uses strong claims like "state-of-the-art performance" and "practical deployability." However, simulated CSI differs from real-world CSI in hardware impairments, synchronization errors, non-ideal antenna patterns, and time-varying channel effects that ray-tracing does not capture. The claimed margins (e.g., 34.4% MAE reduction over LWLM in Single-BS) may not transfer. The paper describes the data as "realistic" (lines 71, 237) but this is not a substitute for real validation. This is the single most significant gap between the paper's claims and its evidence.

2. **Missing directly relevant baselines.** The related work section explicitly discusses CrowdBERT (Han et al., 2024) and signal-guided masked autoencoders (Wang et al., 2025) as existing SSL-based localization methods and describes their limitations. Yet neither is included in the experimental comparison (Section 4.2). The baselines used are OMP (classical compressed sensing), CNN, SWiT, and LWLM. Without comparison against the most directly relevant SSL-based localization methods, the reader cannot assess whether cycle-adaptive masking actually improves upon existing SSL-based localization approaches or merely outperforms weaker baselines. This is an evidential gap in the core claim of outperforming "self-supervised baselines."

### Minor

3. **Asymmetric comparison on map information.** The headline results (Tables 1, 2) compare SIGMAP (w/ map) — which has access to rich 3D geometric information — against baselines that do not use any map information. The paper does include SIGMAP (w/o map) as an ablation, which partially addresses this concern and shows the map contributes meaningful improvement. However, the main framing of "outperforming baselines by 34.4%" relies on the map-augmented version. The question of whether baselines could also benefit from map information (if it were provided as an additional input feature) is never tested, so the comparison does not isolate the benefit of the prompt mechanism itself.

4. **Numerical inconsistency in WAIR-D generalization results.** The text (line 340) reports SIGMAP reaching **1.580 m** MAE on WAIR-D Scenario-2, but the accompanying table (lines 335-338) shows **1.880 m**. The stated improvement over LWLM (44.3%) is consistent with 1.880 m (vs LWLM's 3.375 m), confirming the text value is erroneous. While this specific error is minor, it signals a proofreading lapse in reported numbers.

5. **NLoS-aware attention mechanism introduced only in results.** Equation (11) in Section 4.2 introduces an "NLoS-aware attention mechanism" described as a "key advantage," but this mechanism is never defined or motivated in the methodology section (Section 3). The reader cannot determine whether this is a separate attention head, a modification to the prompt mechanism, or part of the backbone. This is a reproducibility gap.

### Trivial

6. **Main results report only point estimates.** The paper states "All results are averaged over 5 independent runs" (line 239) and mentions "near-overlapping error bars" for the map ablation (line 301), but the main tables (Tables 1, 2, 3) report only point estimates without variance or confidence intervals. Statistical significance of the reported improvements cannot be assessed.

## Nice-to-Haves

- Include error bars / confidence intervals for all main results tables.
- Add hyperparameter sensitivity analysis for the cycle-adaptive masking parameters (mask width $w$, detected periodicity $d_{\text{final}}$, starting offset $j_0$), as these likely affect performance.
- Consider adding interpretability/probing experiments to understand what representations the model learns (e.g., do representations correlate with physical quantities like delay, AoA, or LoS/NLoS status?).
- Discuss why fine-tuning requires 1000 epochs while pre-training uses only 200 epochs (line 352). Even though total fine-tuning time is short (30 min), the asymmetry is worth explaining.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Harsh critic's point about "fine-tuning requiring 5× more epochs than pre-training is a concern":** This is not a genuine weakness. The total fine-tuning time is only 30 minutes because only 0.7% of parameters are updated. More epochs for a tiny parameter set is not unusual. Removed as non-issue.
- **"No hyperparameter sensitivity analysis for mask parameters":** This is a reasonable suggestion but is moved to Nice-to-Haves rather than kept as a weakness, since the paper already provides a useful ablation (Table 3) comparing masking strategies.
- **Formatting/style nitpicks about proofreading:** Removed per formatting rules. The numerical inconsistency (1.580 vs 1.880) is retained as a real error.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observations largely mirror the paper's own identification of gaps in the literature, and the strengths/weaknesses identified are conventional evaluation criteria rather than novel cross-paper insights.

## Suggestions

1. **Validate on real-world measured CSI data.** This is the single highest-leverage improvement. Even a small-scale indoor mmWave testbed evaluation would transform the paper from "promising simulation results" to "demonstrated practical contribution." If real experiments are infeasible, explicitly acknowledge this as a limitation and temper the practical claims (autonomous driving, XR, smart manufacturing) accordingly.

2. **Include CrowdBERT and Wang et al. as baselines.** Since these methods are discussed in related work as the most directly relevant SSL-based localization approaches, their omission from the comparison is a noticeable gap. This is likely addressable since code for these methods may be available.

3. **Fix the numerical inconsistency in the WAIR-D results** (1.580 m → 1.880 m in the text on line 340).

4. **Move the NLoS-aware attention mechanism description** (Eq. 11) to the methodology section and explain how it integrates with the rest of the architecture.

5. **Report variance** for all main results given that 5 independent runs were conducted.

## Score and Decision

**Bracket determination (Round 1):** The calibration search retrieved 22 anchor papers across score bands. The most topically similar anchors in the 5.5–7.5 band included the wireless simulation paper ("Differentiable and Learnable Wireless Simulation with Geometric Transformers," avg 7.00, which had real-world validation) and "CBraMod" (avg 6.75, EEG foundation model with real data across 12 datasets). The MapLearn paper (avg 4.75, simulated pre-training with real testing) and the ECC foundation model (avg 6.25, synthetic-only but with a narrower scope of claims) provided lower-band anchors. Comparing these: our paper has stronger domain-specific technical novelty than MapLearn but less thorough evaluation than either the wireless simulation paper (which had real data) or CBraMod (which had extensive real-data evaluation). The initial bracket is **4.0–5.5**.

**Narrowing:** Within this bracket, the paper's genuine technical contributions (cycle-adaptive masking, map-as-prompt) are specific and well-motivated, but the evaluation gaps — particularly simulation-only validation for a paper claiming practical deployment, and missing directly relevant baselines — are substantial. The paper is stronger than papers scoring ~4.0–4.5 in the calibration set (which often have shallow contributions or flawed methodology) but weaker than papers scoring ~5.5–6.0 (which typically have either real validation or more complete baselines). The final score of **5.0** reflects a paper with real, domain-specific contributions that is not yet ready for acceptance due to evaluation gaps that need to be addressed.

**Anchors consulted:**
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/9TClCDZXeh.md` (avg 7.00, Round 1) — wireless simulation with geometric transformers, had both synthetic and real validation → our paper is weaker on evaluation comprehensiveness.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NPNUHgHF2w.md` (avg 6.75, Round 1) — EEG foundation model with real data across 12 datasets → our paper has less thorough evaluation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/7KDuQPrAF3.md` (avg 6.25, Round 1) — ECC foundation model, synthetic-only but narrower claims → comparable contribution level but our paper has more evaluation issues.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/PdwrCm5Msr.md` (avg 4.75, Round 1) — MapLearn, simulated pre-training + real testing, less technical novelty → our paper has stronger technical ideas but even less real validation.
- `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OxrDTroSNP.md` (avg 4.25, Round 1) — mobile network simulator, simulation-only → our paper has stronger technical contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>