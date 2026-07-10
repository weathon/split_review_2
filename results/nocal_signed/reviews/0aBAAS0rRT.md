Based on the favorability analysis, here's my assessment:

**Strengths**: The top three strengths (map-as-prompt at +10.0, cycle-adaptive masking at +9.8, large improvements at +9.6) are genuinely strong and well-evidenced. Parameter efficiency (+5.3) and WAIR-D generalization (+6.7) are solid but less central.

**Weaknesses**: The most impactful negative signals are simulation-only evaluation (-9.6), insufficient baselines for SOTA claim (-9.0), no random masking control (-6.1), and zero-shot mislabeling (-6.3). The NLoS-attention issue (-2.3), numerical inconsistency (-0.7), and causal claim evidence (-2.2) are minor by comparison.

**Balance**: The paper has real architectural novelty but the evaluation falls short of supporting its strongest claims (SOTA, zero-shot, foundation model for deployment). The fixable gap between narrative and evidence pushes this to borderline reject territory.

Here is the final consolidated review:

---

## Summary

This paper proposes SigMap, a multimodal foundation model for wireless localization that introduces two key innovations: (1) a cycle-adaptive masking strategy that dynamically adjusts masking patterns based on CSI periodicity to prevent shortcut learning, and (2) a "map-as-prompt" framework that encodes 3D building meshes and base station positions via a GNN and injects the result as a learnable soft prompt into a frozen Transformer backbone. The model is pre-trained with a masked autoencoding objective and fine-tuned on downstream localization tasks. Experiments on DeepMIMO and WAIR-D simulated datasets show large improvements over OMP, CNN, SWiT, and LWLM baselines.

## Strengths

- **The "map-as-prompt" mechanism (Section 3.4, Algorithm 1) is a genuinely novel architectural contribution.** Encoding 3D building meshes and base station positions through a GNN and injecting the result as a learnable soft prompt into a frozen Transformer backbone is well-motivated, cleanly designed, and appropriate for cross-scenario adaptation. Using the environment map as a conditioning signal rather than an additional input channel is an architectural insight that addresses a genuine gap in wireless localization.

- **Cycle-adaptive masking is grounded in a real and specific property of CSI (Section 1.1).** The observation that generic masking allows models to exploit periodic structure in CSI as a shortcut is a concrete, testable claim about the data modality. Designing a masking strategy around cross-correlation-based periodicity detection (Equation 6) rather than borrowing off-the-shelf CV or NLP masking shows genuine domain engagement.

- **Reported improvements over selected baselines are large in practical terms.** In single-BS NLoS (Table 1), SigMap (w/ map) achieves 1.564m MAE against LWLM's 2.382m (34.4% reduction) and more than doubles CDF@1m (60.5% vs 25.3%). In multi-BS (Table 2), the gains are smaller but still material.

- **Parameter efficiency is convincingly demonstrated (Table 5).** Only 0.085M trainable parameters (0.7% of total) during fine-tuning with 30-minute fine-tuning time is a practical advantage for real deployment scenarios where retraining a full model is infeasible.

- **Cross-scenario generalization is tested on a held-out dataset (WAIR-D) with 100 city scenes.** This is a substantially harder generalization test than a within-dataset train/test split, and the model maintains non-trivial performance (1.880m MAE on WAIR-D vs LWLM's 3.375m).

## Weaknesses

### Major

- **Evaluation is entirely on simulated data (DeepMIMO and WAIR-D ray-tracing).** For a paper that frames its contributions around "5G/6G applications" and "practical deployability," and uses the term "foundation model" which implies broad applicability, the absence of any real-world validation is a significant gap. Real-world CSI data differs from idealized simulations in ways that systematically impact localization accuracy (I/Q imbalance, carrier frequency offset, phase noise, timing drift). The paper does not acknowledge this limitation in the conclusion or future work section.

- **Baseline set is too narrow to support the "state-of-the-art" claim.** The paper claims "state-of-the-art performance across multiple localization tasks" (abstract) but only compares against OMP (classical compressed sensing), CNN, SWiT, and LWLM. The related work section itself discusses CrowdBERT (Han et al., 2024), signal-guided masked autoencoders (Wang et al., 2025), LWM (Alikhani et al., 2024), and WirelessGPT (Yang et al., 2025) as relevant SSL-based wireless methods. Without comparing against or explaining why these are not directly comparable to the localization task, the SOTA claim is overstated relative to what was actually tested.

- **"Zero-shot" claim is inconsistent with the evaluation setup.** The abstract and Contribution (3) claim "strong zero-shot generalization in unseen environments," but Section 4.5 explicitly fine-tunes the task head on approximately 100 labeled instances per scenario and describes this as a "few-shot learning setup." Only the backbone is frozen. This is few-shot adaptation, not zero-shot. The actual few-shot results are still valuable, but the headline claim misrepresents what was evaluated. The paper should either rename the claim to "few-shot generalization" throughout or conduct an actual zero-shot experiment.

- **The "NLoS-aware attention mechanism" (Equation 11) is introduced without definition in the methodology.** Section 4.2 presents Equation 11 as a key advantage but uses a different formulation involving φ(·) and W_NLoS that is not connected to the attention mechanism described in Section 3.5 (Equation 9). The reader cannot determine whether Equation 11 is the same mechanism as Equation 9 applied to a different problem, or an entirely separate attention module that was omitted from the architecture description.

- **Numerical inconsistency in Section 4.5.** The text states "1.580 m on WAIR-D Scenario-2" but Table 4.5 reports 1.880 m for the same entry.

### Minor

- **No random masking baseline in the masking ablation (Table 3).** The ablation compares cycle-adaptive masking only against fixed grid and fixed strip patterns — not against the standard random masking used in most MAE literature. Without this control, it is unclear whether the benefit comes from the adaptive aspect or from having any structured non-random mask. The differences in Table 3 are modest (adaptive: 0.673 MAE, strip: 0.753, grid: 0.770), and adaptive masking has worse RMSE than strip masking (1.099 vs 0.972).

- **Figure 5 (radar chart) reports metrics not defined in the experimental setup.** The chart includes "oss_scenario", "AoA", "ToA", and a second "Overall" metric. Section 4.1 defines only MAE, RMSE, and CDF@1m as evaluation metrics. These additional metrics are not described — how they are computed or what data they are measured on is not explained. A figure with uninterpretable axes does not strengthen the paper.

- **The causal claim about cycle-adaptive masking is asserted without direct evidence.** Section 4.3 states that adaptive masking "forces the model to learn generalizable features instead of shortcut interpolation," but the ablation only shows downstream accuracy differences. No representation analysis, visualization of what the "periodic shortcuts" look like, or diagnostic showing that non-adaptive variants actually exploit periodicity is provided. The causal mechanism is asserted rather than demonstrated.

### Trivial

None.

## Nice-to-Haves

- Add random masking as a control condition in Table 3.
- Visualize learned prompts to support the "interpretable fusion" claim (Contribution 2).
- Conduct an actual zero-shot experiment (no fine-tuning on target scenario) or consistently rename the claim to "few-shot generalization" throughout.
- Report error bars (standard deviations/min-max) on all numerical results.
- Add a limitations paragraph acknowledging the simulation-only evaluation and discussing how real-world hardware impairments might affect the approach.

## Removed Points

*These points were identified in the original review but are removed per guidelines:*
- *Pre-training data details absent from main text*: Removed because the paper references Appendix B.3/B for configuration details. The parser strips appendices from all papers; these details are assumed to exist in the original submission.
- *Equation 6 underspecification*: Removed because the paper references the appendix for implementation details; the core idea is sufficiently described in the main text.
- *Equation 9 being standard attention*: This is an editorial observation about framing, not a concrete weakness.

## Novel Insights

None beyond the paper's own contributions. The two reviews broadly agree on the paper's strengths (map-as-prompt novelty, domain-grounded masking, strong results on selected baselines) and weaknesses (simulated-only evaluation, insufficient baselines for SOTA claim, zero-shot/few-shot inconsistency, missing experimental controls). No reviewer raised a perspective that fundamentally reframes or challenges the paper beyond what is captured in the strengths and weaknesses above.

## Suggestions

1. **Scope the SOTA claim properly** — either add comparisons to the SSL-based methods discussed in related work, or explicitly explain why they are not directly comparable, and scope the "SOTA" claim to the methods actually compared.
2. **Resolve the zero-shot/few-shot inconsistency** — the paper should consistently use "few-shot" throughout, or include an actual zero-shot experiment (no fine-tuning on the target scenario).
3. **Add random masking to the masking ablation** — this is the minimal control condition for any claim about masking strategies and would substantially strengthen the evidence for cycle-adaptivity.
4. **Define or remove the unlabeled metrics in Figure 5** — each axis should be clearly specified in the experimental setup.
5. **Add a limitations paragraph** explicitly discussing the simulation-only evaluation and potential real-world robustness concerns.
6. **Fix the numerical inconsistency** between the text (1.580m) and the table (1.880m) for WAIR-D Scenario-2.

## Score and Decision

The paper has a genuinely novel core contribution — particularly the map-as-prompt mechanism and the domain-grounded cycle-adaptive masking — and reports large improvements over the baselines it compares against. Parameter efficiency is convincingly demonstrated. However, the evaluation has three gaps serious enough that the paper in its current form does not adequately support its strongest claims: (a) the evaluation is entirely on simulated data without acknowledgement of this limitation, (b) the baseline set is too narrow to support the "state-of-the-art" claim given the methods surveyed in related work, and (c) the "zero-shot" claim in the abstract and contributions misrepresents what is actually a few-shot setup. These are fixable issues — honest scoping, additional baselines, and a limitations section would significantly improve the paper — but as submitted, the narrative consistently outruns the evidence.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>