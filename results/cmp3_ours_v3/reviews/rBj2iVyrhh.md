Now let me write the final consolidated review.

## Summary

This paper proposes Classifier-Constrained Alternating Training (CCAT) for multimodal learning, addressing modality imbalance. The core idea is a two-stage framework: (1) pretrain a shared classifier using bidirectional cross-attention with a regularization term that penalizes modality contribution disparity, then (2) freeze this classifier during alternating training (preventing structural bias toward fast-converging modalities), while using modality-specific LoRA adapters and sample-level secondary updates. Experiments on CREMA-D, Kinetic-Sound, and MVSA show consistent improvements over baselines.

## Strengths

1. **Well-motivated problem and clean core idea.** The paper correctly identifies that existing alternating training methods (MLA) mitigate encoder-level gradient interference but leave the classifier structurally biased toward faster-converging modalities. The solution—pretraining an unbiased classifier then freezing it during alternating training—is logically sound and directly addresses this identified gap. (Sec. 1, lines 15–22; Fig. 1)

2. **Coherent two-stage framework design.** The pretrain-then-freeze pipeline with modality-specific LoRA adapters for distribution mismatch has clear internal logic. The use of LoRA (rather than fine-tuning the frozen classifier) respects the freezing constraint while allowing modality-specific adaptation. (Sec. 3.2–3.3, Algorithm 1)

3. **Ablation study confirms component contributions.** Table 2 systematically ablates each component (classifier freezing, alternating training, secondary updates, LoRA). The full configuration achieves the best result on all three datasets, and the relative contribution of each component can be assessed, with classifier freezing alone contributing a meaningful increment.

## Weaknesses

### Fatal
None.

### Major

1. **No variance or statistical significance reported for any experiment.** The paper reports only point-estimate averages of three random seeds (Table 1 caption) without standard deviations, confidence intervals, or significance tests. For the smaller gaps on CREMA-D and MVSA (~2 percentage points), the reader cannot assess whether these differences are meaningful or within run-to-run noise. Even for the large +6.76% gain on Kinetic-Sound, variance would help establish credibility. This is a basic reporting deficiency that weakens the entire experimental case.

2. **Discrepancy between abstract claim and Table 1 for CREMA-D.** The abstract (line 9) claims "+1.35% on CREMA-D" over state-of-the-art methods. However, Table 1 shows the best non-CCAT result on CREMA-D is LFM at 83.62%, and CCAT achieves 85.89%—a difference of +2.27%, not +1.35%. The numbers do not match, and this must be corrected.

3. **Mutual information estimation (Eq. 5) is underspecified.** The formula MI(zᵢᵐ, fᵢ) = log(N) + 𝔼_𝒟[log(exp(𝐟̄ᵢ, 𝐳̄ᵢᵐ) / Σₗ exp(𝐟̄ᵢ, 𝐳̄ᵢˡ))] uses variables **𝐟̄ᵢ** and **𝐳̄ᵢᵐ** that are never defined in the paper. The expression structurally resembles a normalized similarity score with softmax normalization, not a standard mutual information estimate. Since this MI quantity is used both for the regularization term (Eq. 7) that guides classifier pretraining and for detecting imbalanced samples during secondary updates, its correctness matters. The paper cites Zhou et al. (2025b) but does not make the derivation self-contained.

### Minor

1. **Theoretical "isomorphism" between class and modality imbalance is overstated.** Section 3.1 presents gradient formulas for both settings and claims a "profound theoretical isomorphism" and a "proof of their underlying similarity" (line 59). In reality, Eq. 2 is textbook class-imbalance gradient suppression, and Eq. 3 uses "implicitly learned modality utilization coefficients" γ₁, γ₂ that are never formally defined or grounded in the model architecture. The connection is a basic observation that both involve early-dominance gradient suppression. Claiming this as a "new theoretical framework for understanding multimodal imbalance" (line 26) overreaches. The method does not depend on this framing; the paper would be stronger presenting it as motivation rather than a theoretical contribution.

2. **Kinetic-Sound result disproportionate and unexplained.** The +6.76% gain on KS (79.29% vs. LFM 72.53%) is roughly 3–5× larger than the gains on CREMA-D (+2.27%) and MVSA (+1.92%). The paper offers no analysis of what makes KS respond differently to CCAT. This large differential raises questions about whether the result reflects a genuine methodological advantage or a dataset-specific artifact; an explanation would strengthen the empirical case.

3. **β threshold sensitivity not discussed.** The imbalance threshold β varies substantially across datasets (0.05 for MVSA, 0.15 for CREMA-D, 0.30 for KS), selected via validation-set grid search. Fig. 4 suggests performance can be sensitive to β (e.g., CREMA-D drops from 85.89 at β=0.15 to ~84 at most other values). The paper does not discuss robustness to β perturbations or the risk of validation-set overfitting during hyperparameter selection.

4. **Reconboost not included as an experimental baseline.** Reconboost (Hua et al., 2024) is cited in related work (line 53) as also using alternating training—making it the most natural comparator for isolating the effect of classifier freezing. Its absence from Table 1 is a gap in the empirical comparison.

5. **Inference fusion rule underspecified.** The paper states predictions are "fused at the decision level for final output" (line 185) without specifying the fusion rule (e.g., averaging, weighted combination, learned weights). This is needed for reproducibility.

### Trivial

- t-SNE clustering metrics (CH, SH, DB in Fig. 5) are reported as single values without uncertainty. Since t-SNE is stochastic and these metrics are hyperparameter-sensitive, single-point comparisons (CH: 198.98 vs. 200.01 vs. 242.55) have limited evidentiary value.

## Nice-to-Haves

- Adding standard deviations to all tables would be the single highest-impact improvement.
- Including Reconboost as a baseline.
- Brief analysis of why Kinetic-Sound benefits disproportionately from CCAT.

## Removed Points

These points were removed or demoted during filtering:

- **"Baseline comparison not controlled enough (different fusion architectures)"** — The paper explicitly states (lines 232–233) that ResNet18 encoders are used for audio and visual modalities across all datasets and that all models use identical SGD hyperparameters, indicating a controlled reimplementation. The different fusion strategies (feature-level vs. decision-level) are inherent to each method and cannot be standardized without breaking the methods themselves.
- **"Pure formatting/style nitpicks"** — Removed per instructions.
- **"Missing related works"** — Removed per instructions (no external sources to confirm).
- **Generic/superficial strengths** from the harsh critic input that lack specific paper grounding were removed.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's observations about the MI formula being underspecified and the abstract/table discrepancy are concrete and actionable but do not add novel analytical insight beyond what the paper's framework provides.

## Suggestions

1. Report standard deviations for all 3-seed runs in Tables 1 and 2.
2. Correct the CREMA-D gain figure in the abstract to match Table 1 (or clarify which baseline is being compared against).
3. Define **𝐟̄ᵢ** and **𝐳̄ᵢᵐ** in Eq. 5, or replace with a proper MI derivation; state explicitly whether this is a proper MI estimate or a heuristic.
4. Include Reconboost or explain its omission.
5. Add discussion of β robustness and the disproportionate KS result.
6. Tone down the "theoretical isomorphism" framing to "motivational analogy."

## Score and Decision

**Calibration details.** Round 1 bracket: 4.5–5.5.

Anchor papers retrieved:
- "A Theory of Unimodal Bias in Multimodal Learning" (avg 5.25, Reject) — Theor. paper on modality imbalance in linear networks. CCAT has more directly applicable method but lacks comparable rigor in its theoretical framing.
- "Can One Modality Model Synergize Training of Other Modality Models?" (avg 6.33, Accept) — Stronger theory and broader experimental validation. CCAT's experiments are more limited in scope and have reporting gaps.
- "Robust Multimodal Learning with Missing Modalities via Parameter-Efficient Adaptation" (avg 4.50, Reject) — Similar method+experiments structure but unclear math. CCAT has better motivation and clearer core idea.
- "Visual Instruction Tuning with 500x Fewer Parameters through Modality Linear Representation-Steering" (avg 6.25, Reject) — Addresses modality imbalance in MLLMs; rejected despite higher score due to insufficient ablations and unclear implementation. CCAT has similar structural issues.
- "Towards Holistic Multimodal Interaction" (avg 5.50, Reject) — Information-theoretic analysis of multimodal interaction.
- "Revealing the Illusion of Joint Multimodal Understanding in VideoQA Models" (avg 5.25, Reject) — Analysis paper with strong empirical methodology.

After narrowing: CCAT's core idea is well-motivated and the framework design is coherent, but three major reporting issues (no variance, abstract discrepancy, underspecified MI formula) substantially weaken the experimental presentation. It sits between the 4.50 (missing modalities paper) and 5.25 (unimodal bias theory) anchors, closer to 5.0.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>