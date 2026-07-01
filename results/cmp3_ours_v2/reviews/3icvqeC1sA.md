Now I have a comprehensive calibration picture. Let me synthesize the final review.

**Round 1 bracket**: The paper sits between the 4–5 range (FMint at 4.50, Learning Chaotic Dynamics at 4.67) and the 5.5–6 range (ROSE at 5.75, Zero-shot Imputation at 6.25). It has stronger evaluation than FMint but a similar claim-evidence gap.

**Round 2 narrowing**: TimeMixer (5.67 Accept, multi-scale architecture) provides the closest positive anchor. Papers in the 4.25–4.75 range (Reservoir Transformer, Contrastive Meta Learning, Learning Chaotic Dynamics) tend to have weak core evidence relative to claims. ChaosNexus is above these — it has a genuinely novel architecture and comprehensive evaluation — but the attractor-metric overclaiming prevents it from reaching the 6+ level.

**Final score**: 5.5 — borderline, requiring substantive revision before being publishable. The evidence for the core claim (attractor fidelity improvement) is not cleanly supported, and the weather comparison needs reframing. These are fixable issues, but the current version overstates what it demonstrates.

---

## Summary

ChaosNexus proposes a foundation model for chaotic system forecasting built on the ScaleFormer architecture — a U-Net-style Transformer with multi-scale temporal processing, MoE layers, and wavelet-based frequency conditioning. The model is pretrained on ~20K synthetic chaotic ODE systems and evaluated zero-shot on 9.3K held-out systems and few-shot on real-world weather data. The architecture is well-motivated and the evaluation is comprehensive, but there is a significant gap between the paper's core claim (improved attractor fidelity) and the evidence presented.

## Strengths

1. **Principled multi-scale architecture for chaotic dynamics.** The observation that chaotic systems exhibit multi-scale temporal structure and that single-resolution architectures conflate dynamics at different scales is a genuine insight. The U-Net encoder-decoder with hierarchical patch merging/expansion is a natural and well-motivated design for this problem (Section 3.2).

2. **Comprehensive synthetic benchmark with multiple complementary metrics.** Zero-shot evaluation on 9,300 held-out systems uses both point-wise accuracy (sMAPE) and attractor-statistics metrics (D_frac, D_step, D_lyap, ME_LRW). The comparison spans multiple foundation models (Panda, DynaMix, TimesFM, Chronos, Moirai, Timer-XL, Parrot), providing a broad baseline landscape (Figure 2, Section 4.1).

3. **Striking zero-shot transfer to real-world weather.** A model pretrained purely on synthetic ODE systems achieving ~0.8°C MAE on 5-day global temperature forecasting without any weather fine-tuning is a non-obvious and scientifically interesting result (Figure 3, Section 4.2).

4. **Informative multi-scale attention visualization.** The analysis in Section 4.4/Figure 5 provides concrete evidence that shallow layers capture local fluctuations, deep layers capture global structure, and decoder layers act as selective aggregators — going beyond typical "attention maps exist" analysis.

5. **Cleanly designed scaling experiments.** The separation of parameter scaling, per-system data volume, and system diversity in Figure 4 cleanly isolates the factor driving generalization (system diversity, not per-system data volume).

## Weaknesses

### Major

1. **Overclaimed attractor-statistics improvement relative to evidence.** The paper's core motivation — that the multi-scale architecture improves long-term attractor fidelity — is not cleanly supported by the reported data. On D_frac (correlation dimension error, where lower is better), ChaosNexus's mean is ~0.225 compared to Panda's ~0.200. On D_step (KL divergence of attractors), both tie at ~1.2. The text states "it reduces the average correlation dimension error (D_frac) to 0.203" (line 164) — but 0.203 is the *median*, not the mean (0.225). This is misleading: it papers over the fact that the mean D_frac is *worse* than Panda's. The actual improvement over Panda is in point-wise accuracy (sMAPE), which the paper itself correctly notes is "ultimately unreliable" for chaotic systems (line 164). This creates a coherence problem: the architecture is motivated by improving attractor statistics, but the attractor metrics show parity or slight degradation, while the improvement is in a metric the paper argues is unreliable. This issue is verifiable from the figure description (lines 172–177) and the paper text (lines 164–165).

### Minor

2. **Weather evaluation comparison conflates pretraining and architecture.** The main weather result (Figure 3) compares a pretrained ChaosNexus against from-scratch baselines (CrossFormer, FEDFormer, etc.). The paper mentions the baselines "are trained from scratch without pretraining" (line 211), but the headline claim — "outperforming competitive baselines even when they are fine-tuned on more than 470K samples" (line 32) — attributes the gap to the model without controlling for the pretraining advantage. The fair comparison against other foundation models is deferred to Appendix A.6. The finding that synthetic-chaos pretraining transfers to weather is real and valuable, but the presentation implies architecture superiority that this evidence does not cleanly support.

3. **Panda parameter count not reported.** Without knowing Panda's parameter count relative to ChaosNexus's 52.63M, the sMAPE improvement could be partially due to model capacity rather than architectural design.

4. **MMD regularization subtlety unaddressed.** The MMD regularization (Equation 10, Section 3.4) is applied to batches of full trajectories from the same initial condition. For chaotic systems, these trajectories are temporally correlated, not i.i.d. samples from the attractor. The paper does not discuss whether this affects the regularization's effectiveness for its stated goal of matching attractor distributions.

5. **Scaling analysis is largely confirmatory.** Finding (c) — system diversity matters — corroborates results in (Lai et al., 2025), which the paper acknowledges (line 237). Finding (b) — per-system data doesn't help — is presented as a refinement but is nearly a logical consequence of (c). No interaction effects (diversity × per-system data) are explored.

6. **No ablation study in the main paper.** The paper references "extensive ablation studies" in Appendix A, but readers of the main text cannot assess how much each component (multi-scale hierarchy, MoE, wavelet fingerprint) contributes. Given the core claim about multi-scale architecture, this is particularly informative.

### Trivial

- The ordering of variable attention before temporal attention (Equation 1) is stated but not motivated.

## Nice-to-Haves

- An ablation study in the main text quantifying the contribution of each architectural component.
- Expert routing analysis showing which MoE experts activate for different system types.
- Exploration of interaction effects between system diversity and per-system data volume.
- A variant of the MMD regularization that uses attractor re-sampling rather than trajectory-based samples.

## Removed Points

These points were flagged in the input reviews but are removed after verification against the paper:

- "Axial attention complexity assumes factorization doesn't hurt capacity" — speculative, not a verified weakness. The paper's complexity claim (O(S² + V²)) is technically correct for the described factorization.
- "No expert routing analysis" — nice-to-have, but the load balancing loss (Equation 9) mitigates the concern about collapsed expert utilization.
- "Missing related works" — cannot verify without external sources per instructions.
- "General evaluation lacks rigor" / "could be measuring a proxy" — too vague, not anchored to specific evidence.
- Generic/superficial strengths about "addressing an important problem" — these are not specific contributions of this paper.
- Formatting nitpicks and parser-artifact complaints.
- Any criticism questioning the existence/release status of cited models, tools, benchmarks, or datasets — these are assumed to exist per instructions.

## Novel Insights

The reviews surface a tension that the paper itself does not explore: the multi-scale architecture improves point-wise accuracy (sMAPE) but does not clearly improve attractor statistics (D_frac, D_step) — the very metrics that motivated the design. This could reflect a genuine tradeoff between point-wise accuracy and attractor fidelity, or a measurement issue with the current metrics, but the paper does not investigate it. If explored honestly in revision, this could become a finding rather than a weakness.

## Suggestions

1. Report both mean and median for all attractor metrics transparently, and honestly discuss what the D_frac and D_step results imply about the architecture's strengths and limitations. Reframe the core contribution around what the evidence actually supports (e.g., competitive attractor fidelity with strong point-wise accuracy improvements).
2. Move the foundation-model comparison on weather (currently in Appendix A.6) to the main paper alongside the from-scratch comparison, so readers can distinguish the pretraining effect from the architecture effect.
3. Report parameter counts for Panda and other key baselines.
4. Include a brief summary of the ablation study in the main text, even if details remain in the appendix.

## Score and Decision

The paper has genuine architectural novelty and a comprehensive evaluation spanning 9,300 synthetic systems and real-world weather data. However, the core contribution claim — that the multi-scale architecture improves attractor fidelity — is not well supported by the evidence as presented. The D_frac and D_step metrics show parity or slight degradation relative to Panda, while the improvement is in point-wise accuracy (sMAPE), a metric the paper itself argues is unreliable for chaotic systems. This claim-evidence gap is the primary factor limiting the paper. The issues are fixable with honest reframing and improved presentation, but the current version overstates what it demonstrates.

**Calibration anchors used:**
- FMint (SvjFHucuDZ, avg 4.50, Round 1): Similar domain (dynamical systems foundation model), similar claim-evidence gap, but less comprehensive evaluation.
- Learning Chaotic Dynamics (XqDM97DtMf, avg 4.67, Round 1): Chaotic dynamics, strong theoretical idea but weak experiments. ChaosNexus has stronger evaluation.
- ROSE (tdttNKCtyB, avg 5.75, Round 1): Time-series foundation model with novel components, similar evaluation breadth.
- Zero-shot Imputation for Dynamical Systems (NPSZ7V1CCY, avg 6.25, Round 1): Strong zero-shot results with clearer evidence for claims.
- TimeMixer (7oLshfEIC2, avg 5.67, Round 2): Multi-scale time series model; accepted despite score spread (6,8,3).
- Reservoir Transformer (f3NLRksLiZ, avg 4.25, Round 2): Chaotic system forecasting, weaker experimental rigor.
- MGTST (hkgULK8u4d, avg 4.33, Round 2): Multi-scale transformer for time series, limited novelty.
- Contrastive Meta Learning (S8nFZ98pmU, avg 4.75, Round 2): Dynamical systems generalization, weaker core evidence.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>