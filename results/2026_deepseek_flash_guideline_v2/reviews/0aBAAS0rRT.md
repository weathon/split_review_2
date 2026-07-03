Here is my final consolidated review.

---

## Summary

SigMap proposes a wireless localization foundation model with two core ideas: (1) cycle-adaptive masked modeling that dynamically adjusts masking patterns based on CSI periodicity to prevent shortcut learning, and (2) a "map-as-prompt" framework that encodes 3D geographic information via GNN-generated soft prompts for parameter-efficient cross-scenario adaptation. Experiments on DeepMIMO and WAIR-D datasets show clear improvements over baselines (LWLM, SWiT, CNN, OMP) in both single-BS and multi-BS localization tasks.

## Strengths

- **Cycle-adaptive masking is validated against simpler alternatives**: Table 3 shows adaptive masking achieves 0.673m MAE and 84.5% CDF@1m versus 0.770m/80.3% (grid-only) and 0.753m/75.3% (strip-only). This ablation directly supports the claim that disrupting periodic shortcuts yields better representations, isolating the masking mechanism from other components.

- **Multi-level map ablation cleanly isolates the value of geographic prompts**: Table 4 shows monotonic degradation from 3-D map (1.564m MAE, 60.5% CDF@1m) → 2-D birdview (1.692m MAE, 55.7% CDF@1m) → no map (2.275m MAE, 31.0% CDF@1m). The near-doubling of CDF@1m from no-map to any map, and the modest gap between 2-D and 3-D (8% MAE), support the claim that topological/LoS cues drive the gain and the prompt mechanism works even with simplified geometry.

- **Cross-environment generalization demonstrated on two unseen datasets**: Section 4.5 reports SigMap achieves 1.026m MAE on DeepMIMO O2 (vs. 2.213m for LWLM, 53.2% improvement) and 1.880m on WAIR-D Scenario-2 (vs. 3.375m, 44.3% improvement), while updating only ~0.4% of parameters. These are two substantially different simulated environments, strengthening the generalization claim.

- **Parameter efficiency is concretely quantified end-to-end**: Table 5 reports fine-tuning only 0.085M parameters (0.7% of 11.73M pre-trained params), with 1.8s/epoch fine-tuning and 0.83ms/sample inference. These specific training-wall-clock and inference-latency numbers make the practical deployability argument concrete.

- **Problem formalization explicitly incorporates 3D map and base station geometry**: Equation 3 defines the objective as f_θ(H, M, P_BS) rather than f_θ(H) alone, providing a precise formulation that distinguishes the approach from conventional CSI-only methods and grounds the subsequent GNN-based prompt generation.

## Weaknesses

### Major

- **"Zero-shot" claim contradicts the experimental setup**: The abstract states the model exhibits "strong zero-shot generalization in unseen environments," and the contributions section repeats this claim. However, Section 4.5 explicitly describes a "few-shot learning setup" where downstream task heads are fine-tuned on ~100 labeled target instances per scenario. The paper's own text uses both "zero-shot" (abstract/contributions) and "few-shot" (Section 4.5) to describe the same experiment. Fine-tuning on labeled target data is by definition not zero-shot. This is a straightforward misrepresentation that needs correction — either the claim should be relabeled as few-shot generalization, or actual zero-shot results (direct inference without any target labels) should be presented. The core contribution does not depend on this label, but the inconsistency undermines trust in the paper's framing.

- **NLoS-aware attention mechanism (Eq. 11) is introduced only in the results section, never in the methodology**: Equation 11 and the associated W_NLoS parameter are presented in Section 4.2 as "the key advantage" explaining why SigMap outperforms baselines. Yet the methodology section (Section 3) contains no description of any NLoS-aware attention mechanism — no architectural definition, no training objective, no mention of W_NLoS, no integration into the backbone. The reader cannot determine whether this is part of the transformer backbone, a separate module, or a post-hoc interpretive tool. This breaks the internal coherence between the method description and its evaluation.

### Minor

- **No variance or statistical significance reported despite stating "5 independent runs"**: The paper states all results are averaged over 5 independent runs but never reports standard deviations, confidence intervals, or any variance measure for any result in any table (Tables 1-4, generalization table). Without this, the reader cannot assess whether the reported gaps are meaningful or within noise — particularly for the close margins (e.g., adaptive masking 0.673 vs. strip-masking 0.753 in Table 3, or 3-D map 1.564 vs. 2-D birdview 1.692 in Table 4). The paper already runs 5 seeds; reporting standard deviations would be trivial.

- **Numerical inconsistency in WAIR-D generalization results**: The generalization table reports SIGMAP (w/ map) on WAIR-D Scenario-2 as MAE **1.880 m**. The text two paragraphs later states: "SIGMAP reaches 1.026 m MAE on DeepMIMO O2 and **1.580 m** on WAIR-D Scenario-2." The numbers 1.880 and 1.580 do not match. While likely a typo, this discrepancy undermines confidence in the reported numbers more broadly.

- **Periodicity detection algorithm is underspecified**: Equation 6 uses d_final (the detected periodicity shift) to generate adaptive masks, and the text mentions "computing row-wise cross-correlation and generating shift-aware patterns." However, the paper never explains how d_final is computed from cross-correlation — what lag maximizes which correlation, over what window, or how the "shift patterns" are derived. This is the paper's claimed first contribution and is not reproducible from the current description.

### Trivial

- **Figure reference error in Section 4.4**: The text states "Two-dimensional and three-dimensional map ablations are illustrated side-by-side in Figure 1," but Figure 1 (described in Section 2.1) is the LoS/NLoS wireless propagation figure, not a map ablation comparison. This appears to be an incorrect figure reference.

## Nice-to-Haves

- The baseline set could be broadened to include more recent SSL-based methods cited in related work (e.g., CrowdBERT, signal-guided masked autoencoders) for a more comprehensive comparison.
- Adding real-world measured CSI data would strengthen the practical applicability claims, though this is scope-expansion.

## Removed Points

- **"Baseline set is too narrow"**: The paper compares against 4 baselines (OMP, CNN, SWiT, LWLM). Methods like WirelessGPT and WirelessLLM address different task formulations (protocol reasoning, channel estimation, not localization). The criticism overstates the omission. Moved to Nice-to-Haves.
- **"No real-world validation"**: While true, the paper uses two different simulated datasets including WAIR-D with 100 real-world city scenes extracted from OpenStreetMap. Demanding real-world data is a scope-expansion request. Moved to Nice-to-Haves.
- **"Pre-training cost not contextualized"**: 36 hours of pre-training is reasonable for a foundation model; the paper provides concrete numbers. Not a meaningful weakness.
- **"Data size for pre-training not specified"**: The paper references Appendix B.3 for detailed configuration; the appendix is stripped by the parser. Removed per policy.
- **Generic strengths from Strength Finder** (e.g., "the paper is clearly written," "the problem is important"): Removed as lacking specific evidence anchors.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Relabel "zero-shot" to "few-shot"** throughout the paper, or add a genuine zero-shot experiment (direct inference on unseen environments without any fine-tuning).
2. **Describe the NLoS-aware attention mechanism in the methodology section** (Section 3) — either as a model component or clarify that Eq. 11 is a post-hoc interpretive tool.
3. **Report standard deviations** alongside all means in every table — the paper already runs 5 seeds.
4. **Fix the numerical discrepancy** (1.880 vs. 1.580) in the WAIR-D results.
5. **Specify the periodicity detection algorithm**: how d_final is computed from cross-correlation (window size, lag selection criteria, etc.).
6. **Fix the Figure 1 reference** in Section 4.4.

## Score and Decision

**Score: 5.0**

**Decision: Reject**

**Rationale**: The paper proposes genuinely interesting ideas (cycle-adaptive masking and geographic prompt tuning) and provides reasonable experimental support with clean ablations. However, the combination of the zero-shot misrepresentation (the headline claim in the abstract does not match the actual few-shot experiment), the NLoS-aware attention gap (a component invoked as "the key advantage" but never described in the method), missing variance reporting, and a numerical inconsistency collectively weaken the paper's credibility in its current form. These issues are fixable — none are fatal to the core contributions — but they require substantial revision before the paper can be accepted.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>