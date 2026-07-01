Now I have enough information. Let me write the final consolidated review.

## Summary

This paper introduces FF-Erase, the first machine unlearning framework for Forward-Forward (FF) neural networks. The key idea is to use a guidance model (trained on remaining data) to steer the original model's per-layer goodness distributions toward a "forgotten" state via KL-divergence minimization, with periodic recovery forward passes to maintain utility. The paper also proposes G-MIA, a membership inference attack that leverages FF models' per-layer goodness vectors as features for unlearning verification. Experiments on several benchmarks and FF architectures show the method achieves comparable unlearning effectiveness to retraining from scratch while being 1.9–3.1× faster.

## Strengths

1. **Genuine problem identification.** The paper correctly identifies that machine unlearning for Forward-Forward models is unexplored (§1, §2) and provides a well-motivated explanation of why standard gradient-ascent unlearning causes model collapse in FF models (sensitivity to parameter tuning due to no backpropagation; difficulty of deciding per-layer penalties). These challenges are specific to the FF paradigm.

2. **Goodness-based MIA is a practical and useful idea.** G-MIA (§5) exploits the natural output format of FF models—per-layer goodness vectors—as features for membership inference. The experiments show it competes with white-box methods on deeper architectures (CIFAR-100/VGG13, Figure 3), which is a nontrivial result. It fills a practical verification gap for FF unlearning.

3. **Systematic ablation of guidance model trade-offs.** Table 1 systematically varies α₁ (data proportion) and α₂ (epoch proportion) for both the distillation and mini-retraining guidance strategies. The negative control (random guidance model, R.G.M) collapses to Acc_f = 51.18%, cleanly demonstrating that a trained guidance model is necessary.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Overclaimed methodological novelty and imprecise terminology.** The paper describes FF-Erase as a "novel FF-specific gradient ascent method" (Conclusion, line 289). In reality, the mechanism is KL-divergence *minimization* (gradient descent) to match the original model's per-layer goodness distributions to those of the guidance model—effectively a distillation-based unlearning approach adapted to FF models' per-layer goodness vectors. The paper does acknowledge a "distillation-like manner" (line 164) but does not situate itself against prior distillation-based unlearning works (e.g., Chundawat et al., AAAI 2023a, which uses an "incompetent teacher" for forgetting). This is not a fatal issue—the adaptation to FF models is a genuine contribution—but the self-description inflates the algorithmic novelty. The contribution would be sharper if framed as *the first demonstration of distillation-based unlearning in the FF setting via per-layer goodness matching.*

2. **G-MIA is not a "black-box" attack in the standard MIA sense.** The paper repeatedly calls G-MIA a "black-box" attack (Abstract, §1, §2, §5). In the MIA literature, "black-box" conventionally means access only to the model's final output (logits/labels). G-MIA requires per-layer goodness vectors from *all* layers (§5, line 200). While these vectors are part of FF models' natural output (§3.1), this is strictly more access than the FL (final-layer) MIA baseline it is compared against. The outperformance over FL is therefore expected. The meaningful results are G-MIA vs. white-box methods (GR, GAP, ST), where it holds up well—those should be the headline comparison. The paper should characterize G-MIA as an architecture-specific or grey-box attack.

3. **Limited baseline comparison.** The unlearning evaluation compares FF-Erase only against retraining (RE) and direct gradient ascent (GA). GA is a naive baseline even for BP models, and no attempt is made to adapt existing approximate unlearning methods (e.g., distillation-based approaches, Fisher forgetting) to the FF setting. A stronger evaluation would show that naive adaptations of other methods *also* fail, establishing that the FF setting genuinely requires new design, or compare against a distillation-based baseline adapted to FF to isolate the contribution of the per-layer goodness interface.

4. **G-MIA scores show an inconsistency between main results.** In Figure 4(c), RE's G-MIA ACC = 0.5320 and FF-Erase(D) = 0.5245, suggesting FF-Erase slightly *outperforms* retraining. In Table 1, RE's G-MIA ACC = 0.551, and all FF-Erase variants report higher scores (0.556–0.587), indicating FF-Erase is *worse* than retraining. The paper does not explain whether these come from different random seeds, hyperparameter configurations, or other sources, and no confidence intervals are reported. This inconsistency undermines the precision of the effectiveness claims.

5. **No statistical significance reported.** All results are point estimates without variance across multiple runs. Given the stochasticity of FF training and the sensitivity of unlearning to initial conditions, confidence intervals or standard deviations are needed to assess robustness.

6. **Reproducibility gaps for hyperparameters.** Key hyperparameters (K, ε₁, ε₂) are described as empirically determined but no default values, ranges, or sensitivity analysis are provided. For K specifically, the paper notes that smaller K improves utility but degrades efficiency (§4.1, line 160) but gives no guidance on how to choose it for a new dataset.

### Trivial
None.

## Nice-to-Haves

- **Stronger evaluation scenarios.** The current setup (random 20% forgetting from the same distribution) is a reasonable starting point, but the paper would be strengthened by also evaluating class-level forgetting, removal of memorized/outlier data, or canary examples. The current setup cannot fully distinguish genuine forgetting from redundancy.
- **Quantitative evidence for the "why GA fails" claim.** The paper motivates FF-Erase with the intuition that GA causes divergent layer updates in FF models (Figure 1). Measuring this divergence directly (e.g., cosine similarity between layer-wise gradient directions during GA vs. FF-Erase) would turn the intuition into evidence.
- **Synthetic data assumption for G-MIA.** The paper assumes attackers can "synthesize data that has a similar distribution to the training data" (§5, line 200). This is standard in the MIA literature but is a nontrivial assumption; acknowledging the limitations of model inversion for complex datasets would strengthen the paper's practical framing.

## Removed Points

These points from the input review were removed during consolidation:

- **"70% of unlearning time is guidance model training, obscuring the two-part structure."** Removed because Table 1 explicitly separates t₀ and t_unl − t₀ in its columns, and §4.3 clearly discusses both components. The paper is transparent about this.
- **"Only VGG13/CIFAR-10 shown in main text; appendix results stripped."** Removed per guidelines: the parser strips appendices from all papers; they exist in the original submission.
- **"The 1.6–3.3% degradation framing."** Removed because the paper reports raw numbers (Table 1), giving readers full information to judge. The "minor" framing is an interpretation, not a factual error.
- **Section 3.1 footnote about g^l vs. h^l.** Removed as a presentation detail that does not affect the core claims.
- **"Section 4.2 guidance model generalization concern."** Removed because it is speculative and the paper's ablation (R.G.M. negative control) already shows the consequence of a poor guidance model.
- **"G-MIA verification is not independent."** Reweakened: while the concern is conceptually valid, the paper cross-validates against RE (gold standard), which partially mitigates self-verification. Removed as standalone weakness and subsumed under the inconsistency in G-MIA scores (Weakness #4).

## Novel Insights

The reviews surface one observation beyond the paper's own claims: the paper's core technical contribution—applying KL-divergence-based distillation to per-layer goodness vectors for unlearning—is best understood as a domain adaptation of distillation-based unlearning (Chundawat et al., SCRUB) rather than a fundamentally new algorithm. The genuine novelty lies in identifying that (a) per-layer goodness vectors in FF models provide a natural interface for this technique, and (b) the guidance model framework solves the layer-coordination problem unique to FF training. This reframing clarifies both the contribution's scope and its relationship to prior work.

## Suggestions

1. Add at least one stronger baseline adapted from distillation-based unlearning (e.g., an "incompetent teacher" applied to FF models' final goodness aggregation) to demonstrate that the per-layer approach matters.
2. Report all main results with variance across ≥3 random seeds.
3. Resolve the inconsistency between Figure 4 and Table 1 G-MIA scores for RE.
4. Provide default values and a sensitivity analysis for K, ε₁, and ε₂.
5. Rephrase "black-box" as "architecture-specific" or specify that G-MIA accesses all per-layer goodness vectors, and move the FL comparison to a secondary result.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>