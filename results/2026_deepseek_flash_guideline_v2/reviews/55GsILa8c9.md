## Summary

CausalNovo introduces a causality-informed, model-agnostic framework for de novo peptide sequencing. It uses a Structural Causal Model (SCM) to motivate disentangling causal signal peaks from spurious noise peaks, operationalized through a Causality Extraction Module (CEM) with information-theoretic objectives (independence and sufficiency) and a noise-replacement data augmentation. Experiments on three public benchmarks show consistent improvements over three strong baselines (CasaNovo, AdaNovo, π-HelixNovo) at amino acid, peptide, and PTM levels, with up to ~10% gains and substantially improved robustness to noise perturbations.

## Strengths

1. **Model-agnostic framework with consistent gains across multiple independent baselines.** CausalNovo improves all three strong baselines (CasaNovo, AdaNovo, π-HelixNovo) across amino acid, peptide, and PTM levels on three datasets (Tables 1-2). For example, on Seven-species, it boosts CasaNovo AA precision by +12.0% (0.357 → 0.477), AdaNovo by +5.0% (0.403 → 0.453), and π-HelixNovo by +9.1% (0.465 → 0.536). This demonstrates generalizability beyond a single architecture.

2. **Direct empirical evidence of noise robustness via controlled perturbation experiments.** The noise-replacement perturbation analysis (Figures 1, 3; Table 6) directly shows CausalNovo reduces reliance on noise peaks. Under the strictest perturbation threshold (γ=1) with 18 ion types on HC-PT, CausalNovo achieves a 28.5% relative improvement in peptide precision (0.156 → 0.352), empirically confirming the framework's central goal.

3. **Cross-species leave-one-out validation across all 9 species.** Table 3 shows consistent improvements across every species (e.g., Human +2.0%, Mouse +3.7% peptide precision), with average +2.6% gain over the baseline. This provides stronger evidence of out-of-distribution generalization than a single train/test split.

4. **Attention-based mechanistic analysis.** Table 7 shows CausalNovo increases the proportion of predictions where all top-3 attended peaks are causal from 19.26% to 32.87%, and reduces cases where none are causal from 12.73% to 10.76%, providing interpretability evidence that links the framework to its intended mechanism.

5. **Comprehensive component-level ablation.** Tables 4-5 systematically ablate each design decision, quantifying marginal contributions (independence +1.2%, purification +0.8%, symmetric +0.4%, Replace +0.6%, Enhance +0.6% in AA precision). This decomposition is more thorough than typical ablation studies in prior de novo sequencing papers.

## Weaknesses

### Major

1. **Missing control experiments to isolate causal contribution from general regularization.** CausalNovo adds to the baseline: (a) noise-replacement augmentation, (b) contrastive learning on z_c, (c) an extra cross-entropy head on z_s, and (d) causal/non-causal decomposition via learned masks. The ablations (Tables 4-5) show each component helps incrementally, but there are no controls that add analogous training signals *without* the causal framing. Specifically: (i) Would contrastive learning on the *full* representation (no causal/non-causal split) yield similar gains? (ii) Would adding a second cross-entropy head on a *random* split of the representation boost performance? Without such controls, it is unclear whether improvements stem from the specific causal formulation or from having more training objectives and data augmentation in general. Since causal disentanglement is the paper's central framing, this distinction is important.

2. **The "purification" objective's mechanism is not clearly justified.** The paper claims maximizing I(z_s; Y) "can indirectly lead to the purification of z_c" (Section 3.3, line 97), but the mechanism is not explained. A reasonable reader would worry that encouraging z_s to be predictive of Y could incentivize the model to allocate *more* predictive information to the "non-causal" stream, reducing pressure on z_c to be truly causal. The paper references Chen et al. (2022) without making the reasoning self-contained. The ablation (Table 4) shows a modest +0.8% improvement, but whether this comes from genuine causal disentanglement or simply an additional gradient signal is ambiguous.

### Minor

3. **Gap between the theoretical I(z_c; z_c' | Y) objective and the practical InfoNCE implementation.** Equation (5) writes I(z_c; z_c' | Y) ≈ standard InfoNCE loss, but the InfoNCE uses batch-wide negatives (not Y-conditioned negatives) and no explicit Y term appears. The paper says "Y can serve as a proxy for C" (line 181) and the intervention depends on Y, which partially addresses this, but the step from conditional mutual information to unconditional contrastive loss is not formally derived. This gap means the theoretical framing is slightly overclaimed relative to the practical loss.

4. **Partial circularity in the attention analysis (Table 7).** The analysis shows CausalNovo attends more to peaks labeled "causal," but these are defined by the same theoretical spectrum matching used during training — the model is being evaluated on whether it learned the labeling scheme it was trained on. While still a useful sanity check (the model could have failed to learn this), it does not independently validate discovery of causal structure beyond the training signal.

### Trivial

5. **Hyperparameters α (fraction of noise peaks replaced) and γ (m/z tolerance) are not numerically specified in the main text.** The paper defines them symbolically (Eq. 4, Section 3.4.1) but omits the numerical values used in experiments. These may appear in the appendix (stripped by the parser), but their absence in the main text is a minor completeness issue.

## Nice-to-Haves

- The "symmetric" training strategy (alternating which example is the anchor) is mentioned briefly (line 185) and adds +0.4% in the ablation. A brief explanation of the mechanism would be helpful.
- The paper notes the noise identification requires ground-truth peptide labels during training. The framework is designed so that the learned robustness transfers to inference despite this training-time reliance, which is an inherent aspect of the approach rather than a flaw.

## Removed Points

- Harsh Critic's point (Critical Issue #4) about the SCM-to-mask mapping not being formally justified: The paper explicitly states it operates in latent space because "direct causal modeling in the raw spectrum space is challenging" (Section 3.3). This is a standard practical approximation made clear in the text.
- Harsh Critic's claim about the "enhance" step adding theoretical peaks being unrealistic: The paper explains its purpose (preserving causal relationships), and the ablation shows a +0.6% gain. This is a design choice, not a flaw.
- Harsh Critic's note that the vulnerability analysis measures noise robustness rather than causal learning: These are not opposing claims; noise robustness IS the operationalization of causal learning in this domain.
- Harsh Critic's concern about retrained baselines outperforming original reported numbers: Retraining baselines under the same setup is standard practice and creates a fair (and conservative) comparison.
- Harsh Critic's point about γ/α values: This is a minor completeness issue (moved to Trivial #5).
- Strength Finder's generic/superficial points that lack specific evidence: All retained strengths are specific and grounded.

## Novel Insights

None beyond the paper's own contributions. The two reviewers largely converge: the paper has strong empirical results with clear practical value, but the causal framing makes claims that are partially aspirational relative to what the experiments can definitively isolate.

## Suggestions

1. **Add control experiments:** Apply contrastive learning to the full representation (no causal/non-causal split) and add a second cross-entropy head on a random split of the representation. If the gains shrink or disappear, the causal decomposition is doing useful work; if not, acknowledge that benefits may come from regularization.
2. **Clarify the purification mechanism:** Walk through a concrete example showing how maximizing I(z_s; Y) pushes predictive information out of z_s and into z_c rather than the reverse.
3. **Bridge the theory-practice gap:** Either modify the contrastive loss to explicitly condition on Y (e.g., via within-class negative sampling) or clearly state that Eq. (5) approximates unconditional I(z_c; z_c') rather than conditional I(z_c; z_c' | Y), and argue why this is acceptable.
4. **State numerical values for α and γ** in the main text.

## Score and Decision

**Score: 7.0**

**Decision: Accept**

**Rationale:** CausalNovo delivers a well-engineered, model-agnostic framework that demonstrably improves de novo peptide sequencing across multiple architectures, datasets, and granularity levels. The empirical evidence is strong: consistent gains of 2-14% across three baselines, cross-species validation on all 9 species, controlled perturbation experiments showing 28.5% relative improvement, and thorough component ablations. The main weaknesses are (1) missing control experiments that would definitively isolate the causal contribution from general regularization effects, (2) an unclearly justified purification objective, and (3) a modest gap between the theoretical causal framing and the practical loss functions. None of these are fatal — the method's value does not depend on the strong causal interpretation, and the paper already acknowledges limitations in Section 5. The contribution is real and practically useful; the paper would benefit from either adding the controls or softening the causal claims to match the evidence.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>