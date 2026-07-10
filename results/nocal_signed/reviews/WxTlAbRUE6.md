Thank you for the per-item impact scores. These give useful calibration. Let me adjust my assessment based on the signal that uncertainty quantification is actually a stronger concern than I initially judged, and incorporate that into the final review.

## Summary

This paper introduces GMD-25, a benchmark for evaluating compositional generalization in Machine Learning Force Fields (MLFFs). The key design innovation is that training and test molecules are disjoint, unlike standard MLFF benchmarks which test on the same molecules used for training. Four tasks probe different aspects of compositional generalization (length extrapolation, functional group composition, duplication, and combination) using AIMD trajectories computed at the GFN2-xTB level. Five MLFF architectures (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2) are evaluated, revealing that all models struggle substantially on OOD examples, and that ID performance does not reliably predict OOD generalization.

## Strengths

- **The benchmark fills a genuine gap in MLFF evaluation.** Existing benchmarks (MD17, MD22, WS22, Transition1x) train and test on the same molecules or random splits, making it impossible to distinguish interpolation from genuine physical understanding. GMD-25's design of explicitly separating training and test molecules is well-motivated and addresses a question the field needs to ask. [Impact: +9.6]

- **The evaluation reveals genuinely informative cross-model patterns.** The finding that models that perform best on ID examples are not always the models that generalise best to OOD examples, and the specific contrast between EquiFormerV2 (strong on force MAE across tasks) versus SchNet/DimeNet++ (more stable energy predictions on Length Extrapolation), demonstrate the diagnostic value the benchmark was designed to provide. [Impact: +8.6]

- **The four tasks are thoughtfully differentiated.** Each task isolates a specific compositional operation (length extrapolation, functional group composition, duplication, combination), and the augmented variants for Tasks 1 and 2 provide mechanistic insight into whether additional coverage of relevant components helps. This diagnostic specificity is uncommon in molecular benchmarks. [Impact: +5.4]

## Weaknesses

### Major

- **No uncertainty quantification for comparative claims.** The paper reports only single-run results with no confidence intervals, standard deviations, or statistical significance tests, yet makes comparative claims such as "GemNet overall performed best in the OOD region for Functional Group Composition and Functional Group Duplication" and "EquiFormerV2 consistently exhibits the lowest Forces MAE." Without any measure of variance, readers cannot assess whether these differences are meaningful or within the noise of training. Given that detecting differences in generalization is the benchmark's central purpose, this absence weakens the evidence for the paper's most specific findings. [Impact: -9.2]

- **The benchmark does not establish that the PES of test molecules in Tasks 2 and 4 is compositionally predictable from the training data.** For Task 2 (Functional Group Composition: alcohols + aldehydes → carboxylic acids) and Task 4 (Functional Group Combination: symmetric di-acids + di-amines → asymmetric acid-amine), the paper assumes the PES of the test molecules can be compositionally derived from the training components. However, a carboxylic acid involves new electronic structure (resonance stabilization, different charge distribution) not present in alcohols or aldehydes, and an asymmetric acid-amine involves zwitterionic interactions not present in either symmetric case. The paper provides no evidence — e.g., from the GFN2-xTB reference data itself — that the PES actually exhibits the assumed additive structure. Without such evidence, the finding that "all models fail" is uninterpretable: it could indicate that models lack compositional reasoning, or simply that the test molecules' PES is genuinely not predictable from the training data. This does not invalidate the benchmark, but the paper should acknowledge this ambiguity and ideally add a validation analysis. [Impact: -8.1]

- **The energy MAE metric conflates molecule size with generalization for Length Extrapolation.** The metric is defined as total energy error averaged over molecules (not normalized by atom count). For the Length Extrapolation task, the OOD set (C7–C13) contains molecules with up to ~3.7× the atoms of ID-set molecules (C2–C6). Even if per-atom energy error is constant, total energy MAE will increase roughly linearly with molecule size. The paper attributes the sharp error increase at C7 in Figure 2 entirely to a "generalization gap" and claims errors are "one to two orders of magnitude higher" for OOD examples, without acknowledging this confound. The force MAE is properly per-atom (divided by 3N) and does not share this problem, making force results the more trustworthy signal for this task, but the headline energy figures are not a clean measure of generalization. [Impact: -3.7]

### Minor

- **Figure label inconsistencies.** Figures 2 and 3 contain model names ("PBE0" in Figure 2, "m4s" in Figure 3) that do not appear in the Models section (Section 4.1) or the results discussion. PBE0 is a DFT functional, not an MLFF, and is never mentioned anywhere in the paper text. This mismatch between the figures and the documented experimental setup needs clarification — if these are extraction artifacts or if additional models were evaluated, this must be explicitly stated. [Impact: -1.2]

### Trivial

- None.

## Nice-to-Haves

- **Report per-atom energy MAE** alongside (or instead of) total energy MAE for the Length Extrapolation task, to cleanly separate size effects from true generalization. If the sharp error increase at C7 persists in per-atom energy, the claim is much stronger.
- **Add a simple baseline** (e.g., predicting mean training force, or a classical force field like UFF/GAFF) to help calibrate the difficulty of each task.
- **Discuss GFN2-xTB limitations** and how the benchmark's relative comparisons transfer to DFT-level settings where MLFFs are ultimately deployed.
- **Add a Limitations paragraph** to the Conclusions covering at minimum: the energy metric confound in Length Extrapolation, the GFN2-xTB reference level, and the scope of claims about models not tested.

## Removed Points

These points from the input review are removed with justification:

- **GFN2-xTB limiting relevance** — Demoted from a standalone weakness to Nice-to-Have. The benchmark is designed for relative model comparisons, not absolute accuracy. While the paper should discuss this, it is not a structural flaw.
- **16 fs timestep concern** — Removed. FlashMD is explicitly designed for this purpose and the paper cites the method. A methodological design choice, not a flaw.
- **Missing simple baselines (classical FF, trivial baseline)** — Removed. Helpful but not required; the benchmark's contribution is the task design, not establishing absolute difficulty.
- **Foundation model exclusion** — Removed. Paper explains the rationale (contamination of memorization/generalization signals) and the reviewer acknowledges it is reasonable.
- **"EquiFormerV2 as 'defining the current frontier' is an overstatement"** — Removed as subjective opinion, not a substantive weakness.
- **"Paper does not operationalize 'learning underlying principles'"** — Removed; the benchmark design is precisely the operationalization.
- **Missing train/validation split details** — The paper provides molecule ranges, trajectory counts (~2000 snapshots each), and notes secondary trajectories for ID test sets. Sufficient information is given.

## Novel Insights

None beyond the paper's own contributions. The reviews surface genuine methodological concerns (energy metric confound, compositional justification gap, lack of uncertainty quantification, figure inconsistencies) but do not produce a novel synthesis beyond what the paper's results imply.

## Suggestions

1. **Report per-atom energy MAE** for the Length Extrapolation task to cleanly isolate generalization from size effects.
2. **Add validation that the PES is compositionally decomposable** for Tasks 2 and 4 — e.g., test whether a simple additive model trained on the GFN2-xTB reference data can predict the test molecules' energies from group contributions.
3. **Reconcile figure legends with the Models section.** Clarify whether PBE0 and m4s are evaluated models not mentioned in Section 4.1, or extraction artifacts in the PDF rendering.
4. **Add confidence intervals or standard deviations** from multiple runs to substantiate cross-model comparison claims.
5. **Add a Limitations paragraph** to the Conclusions acknowledging the energy metric confound, the GFN2-xTB reference level, and the scope of claims.

## Score and Decision

The paper addresses a genuine gap in MLFF evaluation with a well-designed benchmark and reveals informative cross-model patterns. However, three substantive weaknesses limit the paper in its current form: (1) the lack of any uncertainty quantification undermines the comparative claims, (2) the compositional decomposability of the PES for Tasks 2 and 4 is assumed without evidence, making the "all models fail" result partially uninterpretable, and (3) the energy MAE metric for Length Extrapolation has an acknowledged confound with molecule size. These are all addressable, but the paper needs revision before it is ready for acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>