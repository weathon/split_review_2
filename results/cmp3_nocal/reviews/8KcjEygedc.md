## Summary
This paper develops a theoretical framework for data curation in high-dimensional binary classification with Gaussian features, ridge regression, and linear models. It derives exact asymptotic test error curves for label-agnostic and label-aware pruning strategies, uncovering a phase transition: when the data generator is strong, "keep hard" is optimal; when the generator is weak, "keep easy" is optimal. The theory is validated on synthetic data, connected qualitatively to LLM reasoning results (LIMO, s1), and demonstrated on ImageNet with a pseudo-labeling setup.

## Strengths
1. **Clean theoretical setup with interpretable geometric quantities.** The parameterization in terms of ρ (generator quality), ρ_* (oracle quality), and ρ_g (generator-oracle alignment) is elegant and captures key intuitions in a way that admits analytical treatment. Theorem 2 provides a crisp, memorable phase transition: strong generator → keep hard; weak generator → keep easy.

2. **Rigorous asymptotic analysis with convincing synthetic validation.** The paper commits to a well-defined high-dimensional limit (n,d→∞, d/n→φ) and derives exact closed-form expressions using random matrix theory. The match between theoretical curves and synthetic empirical curves in Figure 1 (solid vs. dashed lines) constitutes genuine validation of the mathematics within its chosen assumptions.

3. **Conceptual unification of contradictory empirical results.** The theory provides a coherent lens for understanding when "less is more" versus "more is more," offering a unified perspective on results that would otherwise appear inconsistent (e.g., why LIMO/s1 succeed on average AIME but not on hard subsets).

## Weaknesses

### Major
1. **Overclaimed explanatory power for LLM reasoning results.** The paper claims to provide a "rigorous justification" (contributions) and "principled explanation" (abstract) for why methods like LIMO and s1 succeed. However, Section 4.2 conducts no LLM experiments, measures none of the theoretical quantities (ρ, ρ_*, ρ_g) on any LLM or benchmark, and simply reinterprets existing tables from prior work. The mapping from the theory (linear separators on isotropic Gaussian data, squared loss) to LLMs (transformers producing reasoning traces, trained with cross-entropy on discrete tokens) is asserted by analogy, not empirically verified. Phrases like "rigorous justification" substantially overstate what Section 4.2 demonstrates.

2. **Under-specified ImageNet experiments.** Section 4.3 describes the central large-scale validation in only two paragraphs plus figure captions, omitting many details needed to evaluate or reproduce the results: (a) the model architecture is not stated; (b) how "difficulty" is operationalized on image data (the theory uses |x^T w_o| as the margin-based difficulty measure) is not specified; (c) the pseudo-label generation protocol is not described; (d) "Error Rate" is undefined (top-1? top-5? how was ImageNet binarized to fit the binary classification theory?); (e) training hyperparameters, number of seeds/random trials, and how the 160K subset was selected from the 1.2M training set are all absent. Without these details, the ImageNet experiment cannot be assessed or reproduced, which fundamentally limits the paper's empirical contribution.

3. **Model collapse claims misrepresent what the theory provides.** The contributions state: "We show analytically that data curation can avert model collapse under label shift." However, the theory analyzes a one-shot learning problem (a single training set is pruned once and used to train a single model). The model collapse experiment in Figure 3 involves iterative retraining over multiple rounds, where the model's own outputs become the training signal for the next round — iterative dynamics that the theory does not analyze. The paper provides no extension of the theory to this multi-round setting; the connection is entirely qualitative. Claiming analytical results for a setting that was not theoretically analyzed is misleading. The paper should either separate the model collapse demonstration from the theory (labeling it as an independent empirical observation consistent with the theory's intuition) or provide a genuine analytical treatment.

### Minor
4. **Theorem conditions not fully met in validation experiments.** Theorem 2(B) requires ρ_* → 1 (excellent pruner) for "keep easy" to be optimal. In the ImageNet setup, w_o = w_g (the same model serves as generator and pruner), so ρ_* = ρ_g = ρ. When the generator is weak (small-n regime), ρ < 1 and therefore ρ_* < 1. The synthetic experiments in Section 4.1 similarly set ρ_* = ρ (footnote 1). Neither experiment meets the exact conditions of Theorem 2. The qualitative predictions appear to hold under weaker conditions, which is interesting, but the paper presents the experiments as direct validation without discussing the condition mismatch.

5. **Statistical characterization of synthetic experiments incomplete.** Figure 1 mentions "error bars" but never defines them (standard deviation over how many trials? what is the variance?). This matters because the "less is more" optimum in the bottom-left panel involves comparing error rates at different p values, and error bars would establish whether the observed differences are statistically significant.

### Trivial
6. **The τ parameter** (Eqn 7: τ := ρ_g/√(1-ρ_*²)) is described as a "cotangent" but its role in the constants β, β̃ is never explained intuitively in the main text. A brief sentence clarifying its geometric interpretation would help the reader.

## Nice-to-Haves
- In Figure 1, the "random" baseline uses an orthogonal pruner (ρ_* = ρ_g = 0), which conflates the effect of the selection rule (keep hard vs. random) with the quality of the pruner (informative vs. uninformative). Adding a baseline comparing "keep hard" with pruner ρ_* = ρ vs. "keep easy" with the same pruner would directly test Theorem 2's predictions.
- Provide a more explicit mapping between the theoretical quantities (w_g, w_o, w_*, |x^T w_o|) and their practical counterparts in both the ImageNet and LLM settings.
- Clarify that the double limit φ→0, λ→0 used in Theorem 2 (data-rich, unregularized regime) may differ from the finite φ, non-negligible λ regime of the ImageNet experiments.

## Removed Points
- **"Theorems deferred to appendix making core derivations unevaluable":** Standard practice at ML venues; removed per hard rules (missing appendix content should not be treated as a weakness).
- **"Timely and well-motivated question":** Generic framing praise; removed per rules about dropping generic strengths.

## Novel Insights
None beyond the paper's own contributions. The key insight — that the optimal pruning strategy exhibits a phase transition depending on generator quality — is the paper's own contribution, not something surfaced by the reviews.

## Suggestions
1. Reframe Section 4.2 explicitly as a qualitative case study showing *consistency* with the theory, not as validation or justification. Remove "rigorous justification" from the contributions and temper similar language throughout.
2. Add full experimental specifications for ImageNet: architecture, training hyperparameters, difficulty metric, pseudo-label generation protocol, error rate definition, number of seeds/repetitions.
3. Either (a) extend the theory to iterative training (even a sketch in the main text), or (b) clearly separate the model collapse demonstration from the theoretical claims and explicitly acknowledge the gap between one-shot theory and multi-round experiment.
4. Add a brief discussion addressing why the qualitative phase transition from Theorem 2 is expected to hold when ρ_* < 1.
5. Define the error bars in Figure 1 and provide the number of trials.

## Score and Decision
The paper's theoretical core — exact asymptotics for data pruning with a generator-quality-dependent phase transition — is a genuine contribution that extends prior work (Sorscher et al., 2022; Feng et al., 2025). However, the paper systematically overstates what its evidence supports: the LLM discussion is interpretive, not evidential; the ImageNet experiments are critically under-specified; and the model collapse claims misrepresent analytical scope as applying to iterative dynamics. These are fixable in revision, but as submitted, the gap between claims and evidence is too large.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>