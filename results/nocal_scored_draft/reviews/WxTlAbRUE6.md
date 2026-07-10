Now I'll craft the final consolidated review based on all the evidence.

## Summary

This paper introduces GMD-25, a benchmark for evaluating compositional generalization in machine learning force fields (MLFFs). It consists of four controlled tasks (length extrapolation, functional group composition, duplication, and combination) where training and test molecules are distinct, unlike standard MLFF benchmarks. Evaluating five diverse models (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2), the benchmark reveals that all models show large generalization gaps, with OOD errors often orders of magnitude above ID errors, and importantly, ID performance does not predict OOD performance.

## Strengths

- **Well-motivated gap.** The paper correctly identifies that existing MLFF benchmarks (MD17, WS22, Transition1x, MD22) train and test on the same molecules, making it impossible to tell whether models learn physical principles or interpolate labeled configurations. This is a genuine limitation, and a benchmark targeting generalization is a timely contribution. (Section 1, Section 2.3)

- **Principled task design.** The four tasks are rooted in the compositional generalization literature (Hupkes et al., 2020) and cleanly isolate different aspects of generalization. Using substituted linear alkanes as a common scaffold controls for confounding variables. The finding that Task 1 shows meaningful signal while Tasks 2–4 show catastrophic failure is informative as a differentiated pattern. (Section 3.1)

- **Practically important finding.** The observation that ID performance does not correlate with OOD performance — e.g., EquiFormerV2 achieves the best forces MAE on length extrapolation but the worst energy MAE — directly challenges the implicit assumption that pushing ID accuracy is sufficient for building reliable force fields. (Section 4.3, Section 5)

- **Diverse model coverage.** The five evaluated models span invariant GNNs, equivariant MPNNs, angle-aware models, and transformer architectures. The deliberate exclusion of foundation models is correctly justified: pre-training on diverse data would obscure whether generalization failures are architectural or data-driven. (Section 4.1)

## Weaknesses

### Fatal

None.

### Major

- **The "compositional generalization" framing overstates what Tasks 2–4 actually test.** A carboxylic acid (Task 2 test molecule) involves resonance delocalization between the OH and C=O groups — a quantum-mechanical effect with no analogue in the separate alcohol and aldehyde training molecules. A dicarboxylic acid (Task 3) involves inductive and electrostatic interactions between two carboxyl groups absent from monocarboxylic acid training data. An asymmetric molecule with a carboxylic acid and an amine (Task 4) can form intramolecular hydrogen bonds or internal salts. These test molecules exhibit genuinely emergent physical phenomena that are not compositionally decomposable in the training data. The paper's framing partially acknowledges this (lines 76-77: "we do not expect the model to learn the chemical reaction pathway"), but ultimately concludes that failure shows models "do not possess a strong inductive bias for composition" (line 157). An equally plausible reading is that these tasks require extrapolation to physical interactions absent from training data — a fundamentally harder problem that no amount of compositional inductive bias would solve without additional physical priors. The paper should either reframe its contribution more modestly (as a benchmark for generalization to novel molecular configurations involving unseen interactions) or provide evidence that the tasks are compositionally solvable from training data (e.g., showing that a linear group-contribution model succeeds where MLFFs fail).

- **No statistical uncertainty reported.** All results are point estimates with no standard deviations, confidence intervals, or any mention of the number of random seeds or training runs. Without variance estimates, readers cannot assess whether the reported differences between models (e.g., "GemNet overall performed best in the OOD region for Functional Group Composition") are robust or within noise. For a benchmark paper that aims to establish empirical findings about model comparison, this is a significant evidential gap. Running experiments with at least 3–5 random seeds and reporting variance is the single most impactful improvement the authors could make.

- **Figure-caption inconsistency with the stated model set.** Figure 2's caption lists "PBE0" (a DFT functional, not an MLFF) as a compared model and omits PAINN. Figure 3's caption lists "m4s" (not mentioned elsewhere in the paper) and shows six models, whereas Section 4.1 enumerates exactly five models (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2). The text discussions in Section 4.3 are consistent with the five models from Section 4.1, so the core results remain interpretable, but the caption errors create unnecessary ambiguity about which results correspond to which architecture. The authors must clarify whether the captions are erroneous or the experimental setup differs.

### Minor

- **The choice of GFN2-xTB as the reference method is underexamined.** The paper uses a semi-empirical tight-binding method, which is reasonable for scalability, but does not discuss how GFN2-xTB's specific error characteristics might interact with the generalization tasks. If GFN2-xTB has systematic biases (e.g., different functional group additivity properties than DFT, different sensitivity to chain length), the benchmark may partly measure how well models reproduce GFN2-xTB's quirks rather than how well they generalize physical principles. A brief comparison against a higher-fidelity reference (e.g., ωB97X-D or PBE0 on a subset) would strengthen the case.

- **No numerical table in the main text.** Results are presented only in log-scale figures, making it difficult for readers to extract precise MAE values for comparison or to evaluate new methods against this benchmark. A table reporting numerical MAE values for key ID vs. OOD comparisons would improve usability.

- **The logic of the augmented variant of Task 2 is unclearly motivated.** The augmented training set adds amines and amides, where "the functional group of the latter is a composition of the functional groups of aldehyde and amines" (line 74). However, the test set still consists of carboxylic acids (alcohol + aldehyde composition). The paper should explain more clearly how seeing one compositional example is expected to help the model generalize to a qualitatively different composition.

### Trivial

None.

## Nice-to-Haves

- Adding a classical force field (GAFF, UFF) or linear group-contribution model as a simple baseline would calibrate the difficulty of the tasks and help interpret whether "orders of magnitude higher error" means the MLFFs are failing gracefully or catastrophically.
- The hyperparameter tuning strategy (optimizing on ID data, then evaluating OOD) is standard but worth flagging: optimal ID hyperparameters may not be optimal for OOD generalization. A brief sensitivity analysis would be helpful.
- Comparing GFN2-xTB against DFT-level calculations for a small subset of molecules would help bound the benchmark's dependence on the reference method choice.

## Removed Points

The following points from the input review are removed per filtering rules:
- Concern about data availability ("will be made open-source upon paper acceptance"): Removed per hard rule that criticisms about release status/availability of cited resources must be removed. If the paper cites it, it exists.
- Allegation that the model discrepancy makes results "uninterpretable": Removed as factually too strong — the text discussions in Section 4.3 are consistent with the five models from Section 4.1, so results remain interpretable despite the caption errors. The underlying caption inconsistency concern is retained as a Major weakness above.
- Request for "task difficulty calibration" (ID error magnitudes): The paper already reports extensive ID vs. OOD gap analysis, including orders-of-magnitude differences. This concern is partially addressed.

## Novel Insights

The most incisive observation emerging from the review is the distinction between compositional generalization proper (recombining learned sub-components without new physics) and the actual experimental setup of Tasks 2–4, where the OOD molecules involve genuinely emergent quantum-mechanical interactions (resonance, inductive effects, hydrogen bonding) absent from the training data. This distinction explains a pattern in the results: Task 1 (length extrapolation) shows some signal because adding CH₂ units is genuinely compositional (no new bond types or interactions emerge), while Tasks 2–4 show catastrophic failure across all models because they require extrapolating to physical regimes the model has never observed. This suggests the benchmark may be better described as testing generalization to unseen molecular configurations involving novel inter-atomic interactions, rather than compositional generalization per se.

## Suggestions

- Correct the figure captions (Figures 2 and 3) to match the model set described in Section 4.1, or clarify if different experiments were conducted for the augmented variant.
- Reframe the contribution of Tasks 2–4 as a test of generalization to molecular configurations with novel inter-atomic interactions, or provide evidence (e.g., linear group-contribution model analysis) that the tasks are compositionally solvable from training data alone.
- Add results from multiple random seeds (at least 3–5) with standard deviations or confidence intervals to support comparative claims about model performance.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>