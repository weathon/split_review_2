## Summary

MolMiner proposes a fragment-based, order-agnostic autoregressive model for molecular generation that unifies several capabilities: symmetry-aware fragment attachment, dynamic 3D geometry updates via forcefield relaxation, and conditional generation over 12 molecular properties. The paper introduces a GMM-based mechanism for partial conditioning (users specify a subset of properties) and proposes calibration plots and Wasserstein distances as evaluation methodology.

## Strengths

- **Symmetry-aware attachment modeling (Sec 3.2).** Fragment symmetries (e.g., benzene's six equivalent carbons) create ambiguous training targets that prior fragment-based models largely glossed over. The paper's approach — exploiting the cyclic structure of ring/bond fragments, using Morgan fingerprints + Tanimoto similarity to identify valid cyclic permutations, and selecting a consistent common frame — is technically principled and clearly articulated. This is a genuine engineering contribution that future fragment-based systems should adopt.

- **GMM-based partial conditioning (Sec 3.6).** Allowing users to specify any subset of target properties while the GMM fills in the remainder addresses a practical workflow need. The mechanism is cleanly integrated and provides flexibility beyond standard all-or-nothing conditioning.

- **Calibration-plots-based evaluation framework.** Rather than relying only on aggregate mean values or correlation coefficients, the paper proposes plotting predicted properties against prompted values across the full conditioning range (μ±2σ) with ±1σ bands. This reveals whether control is monotonic and accurate across the dynamic range, not just at the mean. The approach is well-motivated and could reasonably be adopted more widely.

## Weaknesses

### Fatal

None.

### Major

- **No baselines for the paper's central claim — conditional generation — despite the unconditional comparison being unfavorable.** The conditional generation evaluation (Sec 4.3) consists of calibration plots for MolMiner alone. There is no comparison against any alternative: not HierVAE with latent-space conditioning, not a property-prediction-plus-filtering baseline, not a conditional diffusion model, not G-SchNet (which supports conditioning natively). This absence is structurally consequential: the paper pivots from unconditional results (Table 1, where MolMinerD loses on 12 of 15 metrics to HierVAE, with gaps of 3× on molWt, TPSA, and MR) to conditional generation as the domain where MolMiner excels, but then offers no comparative evidence in that domain. The paper claims to be "the first model to support simultaneous conditioning across as many as twelve molecular properties," which would limit direct baselines at that exact specification, but simpler baselines (e.g., sampling + filtering by property proximity, conditioning via latent manipulation on HierVAE) would still provide meaningful context. Without them, the reader cannot determine whether MolMiner advances the state of the art or merely demonstrates feasibility.

- **No quantitative calibration metrics — the conditional evaluation relies entirely on visual inspection.** The paper's central claim is "calibrated conditional generation across most properties," but no R², Spearman ρ, mean absolute error, or any other quantitative measure of calibration is reported for any of the 12 properties. The paper itself acknowledges "QED is a notable exception, where control accuracy degrades" and "molWt and MR exhibit systematic deviations" — but without numbers (e.g., does QED have R² of 0.3 or 0.6?), these are untestable qualitative judgments. This makes it impossible for future work to compare against MolMiner and weakens the paper's own evaluation framework, which the paper proposes as good practice but then does not use to produce quantitative scores.

- **Multi-property conditioning is evaluated one property at a time, not as genuine joint control.** The experimental protocol (Sec 4.3) varies one property across its range while the GMM fills in the remaining 11. This tests single-signal response, not the model's ability to simultaneously satisfy multiple user-specified constraints (e.g., logP=3, molWt=350, QED>0.7 at the same time). The paper's framing ("simultaneous conditioning across as many as twelve molecular properties" and "simultaneous, multi-property control") suggests the latter capability, but the experiments only demonstrate the former. Joint multi-property control requires resolving trade-offs between potentially conflicting targets; the current evaluation sidesteps this challenge entirely.

- **The paper overclaims on unconditional performance.** The abstract states "offers competitive unconditional performance," but Table 1 shows MolMinerD underperforming HierVAE on 12 of 15 metrics, with several gaps being large (molWt: 47 vs. 15, TPSA: 7.6 vs. 2.3, MR: 11.9 vs. 3.8). The paper's characterization "slightly below" (Sec 4.2) understates these differences. While the paper's main contribution is conditional generation, the unconditional results should be characterized more precisely.

### Minor

- **No quantitative ablation results in the main text.** Section 4.1 states three ablation findings (conditioning on more properties helps; geometry-aware attention helps with positive bias; rollout resampling regularizes) without reporting any supporting numbers. The reader is directed to the appendix for actual results. Key quantitative takeaways should be in the main paper.

- **Dynamic geometry update is not isolated as an ablation.** The paper states that unlike G-SchNet, MolMiner updates geometry during generation via forcefield relaxation, but there is no experiment running MolMiner without this dynamic update (e.g., with frozen geometry as in G-SchNet) to measure its impact. This is a natural ablation that would isolate the contribution of the dynamic 3D component.

- **No validity metric reported.** The paper says it "omit[s] validity, as our model enforces valence constraints during generation and consistently produces valid molecules." Even if this rate is near 100%, reporting the exact number is standard practice and avoids leaving the reader to wonder.

### Trivial

None.

## Nice-to-Haves

- **Evaluate on genuinely 3D properties.** All 12 properties are computed from 2D structure via RDKit. Given the model incorporates 3D geometry, evaluating on properties where 3D awareness would matter (e.g., conformer energies, docking scores) could demonstrate a practical benefit of the 3D component. This is outside the paper's current scope but would strengthen it.
- **Address the early-termination bias.** The paper honestly acknowledges this limitation (Sec 5) — balancing termination actions or using RL fine-tuning as proposed fixes would strengthen the method's calibration, especially for molWt, TPSA, and MR.

## Removed Points

- **MoLeR exclusion handling.** The reviewer questioned the fairness of excluding MoLeR from the main table. However, the paper documents a concrete attempt (7 days of training, poor results, consistent with known VAE prior-posterior mismatch issues). The results are in the appendix. This is a reasonable handling of an attempted baseline that did not produce usable results, not a flaw.
- **MoLeR training time / "mini-epoch" ambiguity.** Same reasoning as above — the paper provides a clear account of the attempt.

## Novel Insights

The harsh reviewer correctly identifies that the paper's strongest contribution is the combination of design choices (symmetry handling, order-agnostic rollout, geometry-aware attention, multi-property conditioning) rather than absolute state-of-the-art performance on any single metric. The most novel observation from the review is that the paper's evaluation framework (calibration plots) is well-conceived but incompletely executed — the paper proposes a methodology for assessing conditional generation quality but then does not follow through with quantitative metrics that would make that methodology operational for the field. This gap between methodological ambition and empirical execution is the paper's central weakness.

## Suggestions

1. **Add conditional generation baselines.** Even simple ones would help: (a) HierVAE with latent-space property manipulation; (b) unconditional generation + property filtering; (c) G-SchNet conditional generation. Show calibration plots for these baselines alongside MolMiner.
2. **Report quantitative calibration metrics.** For each property, report R² or mean absolute error between prompted and predicted values. This converts the visual claim into a benchmark the field can use.
3. **Demonstrate joint multi-property control.** Show at least one experiment where 2–3 properties are simultaneously specified and the model tracks all of them (e.g., a Pareto-style analysis of trade-offs).
4. **Move key ablation numbers into the main text.** Even a brief table showing the impact of each ablated component on one or two representative metrics would substantially strengthen Section 4.1.
5. **Report the validity rate.** A single number confirms the claim that valence constraints produce valid molecules.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>