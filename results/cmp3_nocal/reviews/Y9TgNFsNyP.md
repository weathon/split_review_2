## Summary

This paper introduces FF-Erase, the first machine unlearning method designed specifically for Forward-Forward (FF) neural networks, along with G-MIA, a goodness-based membership inference attack for verifying unlearning. The method uses a guidance model (trained on remaining data) to provide a stable target goodness distribution, then shifts the original model's per-layer goodness toward that target via KL divergence — addressing the fundamental challenge that FF models' layer-wise independent training and parameter sensitivity cause standard gradient-ascent unlearning to collapse. Experiments on VGG13/CIFAR-10 show the method achieves unlearning effectiveness comparable to retraining while being 1.9–3.1× faster.

## Strengths

1. **Genuinely first work on a real open problem.** The paper correctly identifies that all existing unlearning methods assume backpropagation-trained models, and that FF models' layer-wise independent training and sensitivity to parameter tuning (§1, lines 38–42) make naive gradient-ascent unlearning fail (Figure 1). As FF models see growing interest across architectures (CwComp, Deeperforward, FORWARDGNN, etc.), having a dedicated unlearning method is timely and well-motivated.

2. **Principled and coherent core method.** The guidance-model approach (KL divergence between the original model's goodness distribution and the guidance model's target distribution, Equation 5) directly addresses the instability problem identified earlier. Steering the full distribution rather than simply penalizing the correct-class goodness is a more controlled intervention. The "forgetting forward + recovering forward" loop (Algorithm 1) cleanly instantiates this idea.

3. **Informative and fairly executed ablation study (Table 1).** The systematic variation of α₁ (fraction of remaining data) and α₂ (fraction of epochs) for both mini-retrained and fast-distilled guidance strategies reveals the time-effectiveness-utility trade-offs. The control experiment with a randomly initialized guidance model (R.G.M., last line of Table 1) convincingly demonstrates catastrophic utility loss (55.53% test accuracy vs. ~79% for reasonable configurations), confirming the guidance model's necessity.

4. **G-MIA is a practically useful verification tool for FF models.** By exploiting FF models' native per-layer goodness vectors, G-MIA extracts richer membership signals than a standard final-layer black-box MIA (FL). Figure 3 shows G-MIA consistently beats FL across all architectures tested, providing a verification tool that is more practical than white-box methods.

## Weaknesses

### Fatal
None.

### Major

1. **The GA baseline in the main comparison (Figure 4) is a straw man.** The paper compares FF-Erase against gradient ascent (GA) at λ=10, which it admits "fails to converge and leads to model collapse" (line 246). While §6.3 separately explores GA across λ values and finds no sweet spot (either collapse or ineffective unlearning), the central comparison figure still presents GA at its worst setting. This inflates the apparent advantage of FF-Erase. A fair comparison would use the best non-collapsing GA configuration from §6.3 (λ=10⁻² or 10⁻³, which at least runs without collapse) in Figure 4, even if those settings also fail to unlearn effectively.

2. **Inconsistent RE baseline G-MIA scores and no confidence intervals.** The retraining (RE) G-MIA score is 0.532 in Figure 4(c) but 0.550 in Figure 5(c) and 0.551 in Table 1 — a ~3.5% relative discrepancy in a metric where method-to-method differences are only 0.0075–0.03. This suggests non-trivial run-to-run variability, yet no error bars, standard deviations, or multiple-trial statistics are reported anywhere in the main text. Without these, the claim that FF-Erase achieves "comparable unlearning effectiveness as retraining" (resting on a 0.0075 G-MIA difference) cannot be evaluated for statistical significance.

3. **G-MIA's "black-box" framing is imprecise.** The abstract and contributions (§1) call G-MIA a "black-box attack," and it is contrasted with white-box methods requiring gradients or parameters. However, G-MIA requires per-layer goodness vectors from *all layers* (line 200: "the attacker can obtain... the goodness vectors from all layers"), which is more information than a conventional black-box API (which exposes only the final prediction/logits). While FF models natively output these vectors during inference (§3.1, line 88), a standard deployment API would not typically expose intermediate layer representations. The threat model is stated transparently, but the "black-box" label overstates the practical accessibility of the required signals.

### Minor

1. **Main-text evaluation is limited to one configuration (VGG13/CIFAR-10).** All figures and tables in the main text present results on a single dataset-architecture pair. The paper states "Due to space limitations, we only show the results of VGG13 models trained on the CIFAR-10 dataset in the main text and put other results in Appendix §C" (line 242). Claims about generalizability across 4 datasets, 3 architectures, and the stated 1.9–3.1× speedup range cannot be verified from the main text alone. (The speedup range *can* be verified from Table 1's single-configuration data: 1107/583.5≈1.90× to 1107/353.7≈3.13×, so this criticism partly misses — but the broader point about limited configurability stands.)

2. **G-MIA's claim about outperforming white-box methods is not supported by the main-text results.** The paper states G-MIA "even presents a better performance than white-box MIAs under deeper models and complex datasets" (line 220), giving VGG13/CIFAR-100 as an example from the appendix. However, in all three main-text configurations of Figure 3 (TinyCNN, AlexNet, VGG13 on CIFAR-10), the white-box ST method achieves the highest overall accuracy, beating G-MIA in every case. The claim as stated is technically about the appendix results, but the positioning in §6.1 (which directly discusses Figure 3) is misleading.

3. **Potential leakage in the fast-distilled guidance model.** The fast-distillation strategy (Equation 8) trains a student guidance model by minimizing KL divergence against the teacher (original model θₒ), which *has* been trained on the forgetting data (line 182–184). The paper claims the guidance model is "ignorant of the forgetting data" (line 176), but since the teacher's representations on remaining data may carry traces of forgetting data through shared training dynamics, the student could inherit those traces. The comparable G-MIA scores between D and R strategies in Table 1 suggest this may not be a severe problem in practice, but the paper does not discuss this concern.

### Trivial
None.

## Nice-to-Haves

- Replace the λ=10 GA baseline in Figure 4 with the best non-collapsing GA variant from §6.3 (λ=10⁻² or 10⁻³) to provide a more meaningful comparison.
- Add confidence intervals or standard deviations over multiple runs to the G-MIA scores in Figures 4(c) and 5(c).
- Explore sensitivity to the forgetting fraction β (currently fixed at 20%).
- Discuss the scenario where forgetting data is concentrated in specific classes (e.g., removing all instances of a single class).

## Removed Points

These points from the harsh critic review were removed or demoted after verification against the paper:

- **"The 1.9–3.1× speedup claim and 1.6–3.3% degradation cannot be verified."** — The 1.9–3.1× range is actually verifiable from Table 1 (1107/583.5=1.90×, 1107/353.7=3.13×). The 1.6–3.3% degradation is approximately consistent with Table 1's accuracy values (lowest drop: 80.85→79.16 = 1.69 absolute). This criticism was removed as factually incorrect about verifiability, though the broader concern about single-configuration evidence is retained as a Minor weakness.

- **"The 'recovering forward' privacy implications are not discussed."** — The paper explicitly accounts for remaining data access in the efficiency analysis (Equation 9, K⁻¹·t_ret term), and retraining from scratch uses the same data. This is not a meaningful difference in data access patterns.

- **"The guidance model quality depends on remaining data size, creating a vicious cycle for large forgetting fractions."** — A valid speculation but no experiments in the paper test this scenario, and it amounts to asking the paper to address problems outside its demonstrated scope.

- **"Efficiency formula derivation conflates forward passes on forgetting and remaining data."** — The formula (Equation 9) is explicitly described as approximate ("t_unl ≈ ..."), and the approximation is reasonable for the purpose of providing intuition.

- **"G-MIA assumes the attacker can synthesize similar-distribution data via model inversion."** — This assumption is stated transparently (line 200) and is standard in the MIA literature (Shokri et al. 2017). It is not a weakness specific to this paper.

- **Various formatting/style nitpicks and speculations about missing appendix content** — Removed per the hard rules (parser artifacts, stripped appendices).

## Novel Insights

The harsh critiques collectively surface two insights the paper itself only partially articulates: (1) the evaluation's central claim of "comparable effectiveness to retraining" rests on G-MIA differences of ~0.01 that fluctuate across experimental conditions, and (2) the paper's taxonomy of "black-box" vs. "white-box" does not cleanly capture G-MIA's actual access requirements. The more interesting observation, however, is that FF-Erase's design reveals a deeper principle about unlearning in non-backpropagated models: because FF models lack a shared gradient signal that couples all layers, unlearning cannot rely on a global loss signal — it must be grounded in a per-layer reference distribution, which the guidance model provides. This insight about the necessary structure of unlearning in locally-trained architectures is the paper's most significant conceptual contribution, and it generalizes beyond FF models to any layer-wise greedy training paradigm.

## Suggestions

1. **Fix the GA baseline.** In Figure 4, replace GA(λ=10) with the best non-collapsing configuration from §6.3 (λ=10⁻²). Even though this variant does not effectively unlearn either, presenting it in the main comparison removes the appearance of a straw man and lets the ablation in §6.3 tell the full story.

2. **Resolve the RE G-MIA inconsistency and add error bars.** Clarify why the RE G-MIA score differs across Figure 4(c), Figure 5(c), and Table 1. Report standard deviations or confidence intervals over multiple runs for all G-MIA scores.

3. **Clarify the G-MIA access model.** Rename or qualify the "black-box" label to reflect that G-MIA requires per-layer goodness vectors — e.g., "grey-box" or "forward-output-based" — and discuss whether a standard API would expose these vectors.

## Score and Decision

The paper makes a genuine and timely first contribution to an unexplored problem with a method that is principled, clearly motivated, and accompanied by a useful verification tool. The core technical idea (guidance-model-based goodness shifting via KL divergence) is sound and well-grounded in the identified challenges of FF models. However, the evaluation in the main text has three interrelated weaknesses that prevent a conclusive assessment: a straw-man GA baseline that inflates the method's apparent advantage, inconsistent baseline metrics combined with missing confidence intervals that make the central effectiveness claim unverifiable, and an imprecise threat-model framing for G-MIA. These issues are fixable but require resolution. The contribution is real and the method is well-designed, meriting acceptance conditioned on these evaluation concerns being addressed.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>