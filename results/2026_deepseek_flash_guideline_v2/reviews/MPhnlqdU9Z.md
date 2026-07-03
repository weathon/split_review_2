## Summary

This paper introduces *monitorability* — a neural network's intrinsic ability to have its inference errors detected from internal activations — and proposes the MIRA Score, a metric quantifying this property using only in-distribution data with FGSM perturbations. MIRA is validated across vision (CIFAR-10/100, 4 architectures), tabular (Sensorless Drive Diagnosis, 5 architectures), and NLP (SST-2, 4 transformers) by comparing against the best achievable OoD detection AUROC across ODIN, Mahalanobis, and Energy-based detectors. The paper shows consistent rank ordering between MIRA and best AUROC across all three modalities.

## Strengths

1. **Novel concept with clear practical motivation.** The distinction between "detecting failures" and "assessing whether failures are *detectable* from internal representations" is a genuine gap in the literature. The paper convincingly motivates this with a toy example (Figure 1) showing two models with identical ID accuracy but radically different feature-space separation of OoD data.

2. **Metric requires no OoD data and is efficient.** Unlike OoD detection methods that require tuning against or evaluation on external OoD datasets, MIRA (Definition 2, Eq. 4) is computed using only ID data with FGSM perturbations and Mahalanobis distance. The paper correctly notes this makes it practical as a pre-deployment model-selection tool, whereas the baselines require per-detector grid search on OoD data.

3. **Cross-modality validation with consistent rank ordering.** The evaluation spans 3 modalities with 4–5 architectures each and 4–7 OoD datasets per modality. The rank ordering between MIRA and best AUROC is consistent: ViT (MIRA=89.25, AUROC≈99%) > DenseNet (16.01, 99%) > ResNet-18 (6.05, 95%) > CustomNet (-0.07, 78%) on CIFAR-10; DeBERTaV3 > ELECTRA > RoBERTa > DistilBERT on SST-2; WideMLP > MLP > DeepMLP > Transformer > DeepTransformer on tabular. This consistency across diverse settings is the paper's strongest evidence.

4. **Principled dimension calibration.** Converting Mahalanobis distance to a χ²-survival-function surprisal score (Eq. 3) removes the dimensionality dependence of raw Mahalanobis distance, which under the GDA assumption grows with layer dimension. This is a deliberate improvement over prior Mahalanobis-based work and is necessary for comparing across layers of different sizes.

## Weaknesses

### Fatal
None.

### Major

1. **Central correlation claim lacks quantitative evidence.** The paper's primary empirical claim — that MIRA "correlates" with monitoring performance — is supported only by qualitative table inspection ("Higher MIRA scores consistently align with better global detection performance"). No correlation coefficient (Spearman's ρ, Kendall's τ) or scatter plots are reported anywhere. While the rank ordering is visually consistent across all three tables, strength and significance of the relationship cannot be assessed from the current presentation. For a paper that introduces and validates a metric, this is the most significant evidential gap. *Verification: The paper uses phrases like "correlates with monitoring performance" (abstract) and "MIRA exhibits good correlation with the best achievable OoD detection performance" (Section 4.4 Discussion), but the tables contain no correlation statistics — only MIRA values and AUROC numbers.*
   
   Note: With only 3–5 models per modality, rank correlation p-values would be of limited power, but the metric is still worth reporting alongside scatter plots that combine data across modalities.

### Minor

2. **Validation partially confounded by shared methodology.** MIRA uses Mahalanobis distance to measure feature separability (line 91: "To measure separability we use the Mahalanobis distance"), and one of the three validation detectors (Lee et al., 2018b) is also Mahalanobis-based. The paper should separately report MIRA's correlation with only non-Mahalanobis detectors (ODIN, Energy) to demonstrate the metric captures monitorability rather than just methodological alignment.

3. **Perturbation range selection confounded with robustness.** The range [ε_min, ε_max] is set per-model based on accuracy degradation (ε_min is the smallest ε reducing accuracy to a threshold, ε_max = 2·ε_min). A more robust model naturally requires larger ε to degrade accuracy, pushing the perturbation range outward and likely inflating MIRA — meaning MIRA partly captures "how much perturbation is needed to degrade accuracy," which is related to robustness. The paper does not disentangle this. *Verification: Section 4.2 (lines 131-133) describes this procedure.*

4. **Formal definition is not operationalized.** Definition 1 characterizes l-monitorability via existence of a set Z^l in feature space such that loss ≤ ε ⇔ f^l(x) ∈ Z^l. The paper explicitly notes Z^l "may be arbitrarily complex" (line 73). While not trivially satisfiable (the ⇔ condition genuinely requires the feature representation to separate high-loss from low-loss inputs), the definition is never used to derive the metric or to classify any model as monitorable/non-monitorable. The paper acknowledges this: "Definition 1 provides an abstract formalization... but it does not quantify" (line 81). This means the claimed "theoretical grounding" is primarily framing rather than an operational theory. The contribution stands on the metric and its validation, not on the formal definition.

5. **Cross-modality scale incomparability.** MIRA scores span drastically different ranges (vision: -0.07 to 89.25; tabular: 4.37 to 63.51; NLP: 2015–3793). While the χ² calibration makes scores theoretically comparable *within* a fixed dimension, the absolute values are not interpretable across modalities with different penultimate-layer dimensionalities. This limits the generality of MIRA as a single numerical scale. The paper does not discuss this limitation.

6. **The distribution p(ε) used in experiments is not specified.** Equation 4 defines MIRA with a user-defined p(ε), and the paper gives "uniform" as an example, but never states what was actually used in the experiments. This is a reproducibility gap; the appendix (stripped) may contain this, but it should be stated in the main text.

### Trivial
None.

## Nice-to-Haves

- **Ablation of perturbation methods.** Showing that FGSM and random perturbations (or PGD) produce similar MIRA rankings would strengthen the claim that the gradient direction is not the key driver.
- **Ablation across layers.** The paper computes MIRA only on the penultimate layer. Showing that the metric works at earlier layers would support the stated goal of guiding layer selection.
- **Per-detector correlations.** Reporting MIRA's correlation with each detector individually (not just best-of-three) would strengthen the evidence.

## Removed Points

- **"Definition 1 is trivially satisfiable by any model" (Harsh Critic).** Removed as factually incorrect. The ⇔ condition requires that f^l(x) ∈ Z^l implies L(f(x),y) ≤ ε, which is not trivially satisfiable — if a high-loss and low-loss input produce the same feature vector, no Z^l can separate them. The definition imposes a genuine constraint. The *actual* limitation (that the definition is not operationalized) is retained as Weakness #4 above.

- **"Negative MIRA scores not convincingly explained" and speculation about gradient quality.** Removed. The paper does explain negative MIRA: "perturbed data are less detectable than ID data, showcasing very bad monitoring capabilities." The critic's speculation that negative scores indicate "saturated or broken gradients" is a hypothesis not verifiable from the paper. The request for deeper analysis is valid but belongs in Nice-to-Haves.

- **"t-SNE visualizations are qualitative."** Removed. t-SNE visualizations are standard supporting evidence in the literature and are presented as complementary, not primary. The paper explicitly states they "provide an intuitive perspective" (line 269).

- **Missing error bars / variance estimates.** Removed. The paper fixes seeds and uses deterministic algorithms. Reporting variance from model training runs would strengthen but is not standard expectation for this type of empirical setup.

- **Missing ablations of design choices.** Moved to Nice-to-Haves. These would strengthen the paper but are not weaknesses given the scope of the current validation.

- **Formatting/reproducibility nitpicks.** Removed as parser artifacts or minor points that don't affect the paper's substance.

## Novel Insights

The Harsh Critic's observation about the perturbation range selection (Weakness #3) is genuinely insightful: the procedure of setting ε_min based on accuracy degradation creates a confound where more robust models naturally receive wider perturbation ranges, which likely inflates MIRA scores. This means MIRA may partly reflect robustness rather than purely monitorability. The Strength Finder correctly identifies that MIRA's integration over perturbation magnitudes (as opposed to a single-ε proxy) is a deliberate methodological improvement that makes the metric more robust than a naive alternative. Neither the paper nor the reviews fully explored how the interaction between these two design choices affects the metric.

## Suggestions

1. **Report quantitative correlation statistics.** Compute Spearman's rank correlation between MIRA and best AUROC (and per-detector AUROC) across all model/dataset combinations, with scatter plots. This is the single most important addition — the paper's central claim requires it.
2. **Re-validate excluding the Mahalanobis detector.** Show that the correlation holds for {ODIN, Energy} alone to eliminate the methodological confound.
3. **Acknowledge and discuss the robustness confound.** The perturbation-range procedure may conflate monitorability with robustness. Discuss this limitation and consider an alternative range-setting strategy (e.g., using a fixed ε across models with different accuracy thresholds).
4. **Specify p(ε).** State explicitly what distribution was used in experiments (presumably uniform).
5. **Reframe Definition 1.** Acknowledge that it is a conceptual characterization rather than a formal definition that the paper uses to derive results. The contribution is the metric and its validation, not a restrictive formalization.

## Score and Decision

**Calibration note:** The calibration search was unavailable due to a data access issue, so the score is based on direct analysis of the paper content against the ICLR scale. The paper introduces a genuinely novel concept with a practical metric and cross-modality validation. The consistent rank ordering across all three domains (vision, tabular, NLP) provides meaningful support for the metric. However, the central claim of "correlation" is made without any quantitative correlation statistic, which is a significant evidential gap for a metric-validation paper. All weaknesses are fixable without re-architecting the method. The paper sits in the borderline range — contributions are real and novel, but the empirical validation of the core claim is incomplete.

**Score:** 5.5  
**Decision:** Accept

The paper's core contribution — the concept of monitorability and the MIRA metric that quantifies it without OoD data — is genuinely novel and practically motivated. The cross-modality validation consistently supports the metric's utility, even absent formal correlation statistics. The weaknesses (missing correlation coefficients, methodological confounds) are all addressable through additional analysis and discussion; none invalidate the core contribution. The paper would be strengthened considerably by addressing the suggestions above.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>