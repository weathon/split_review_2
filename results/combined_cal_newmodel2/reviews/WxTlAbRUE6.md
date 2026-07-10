Now I have all the calibration data I need. Let me construct the final review.

## Summary

This paper introduces GMD-25, a benchmark designed to evaluate compositional generalization in machine learning force fields (MLFFs). It comprises four tasks (length extrapolation, functional group composition, functional group duplication, functional group combination) each probing a distinct form of generalization. Five state-of-the-art MLFFs are evaluated, and the core finding — that all models show OOD errors 1–2 orders of magnitude higher than ID errors, with the best ID model often not being the best OOD model — is striking and actionable for the field.

## Strengths

- **A genuinely important empirical question, well-framed.** The paper identifies a real gap in MLFF evaluation: current benchmarks (MD17, MD22, WS22, Transition1x) train and test on the same molecules or very similar chemical spaces, so strong ID performance could reflect interpolation or memorization rather than understanding of physical principles. This framing is clear and well-supported by the related work discussion (Sec. 2). [favorability=10.01]

- **Task design systematically probes distinct compositional generalization abilities.** The four tasks cleanly decompose generalization into distinct challenges, each with a clear motivation. The "base" vs. "augmented" variants within Tasks 1 and 2 are a particularly thoughtful design choice — the augmented variant provides more compositional supervision, allowing the benchmark to reveal not just whether models fail but what kind of evidence helps. [favorability=12.18]

- **The core empirical finding is striking and important.** The result that all evaluated models show OOD errors 1–2 orders of magnitude higher than ID errors, even on the augmented variants, is genuinely concerning for the MLFF community. The finding that the best ID model is not always the best OOD model (EquiFormerV2 excels at forces but fails on energy OOD, while SchNet and DimeNet++ show the opposite pattern) is a valuable piece of evidence that standard benchmarks may be selecting for the wrong inductive biases. [favorability=12.32]

## Weaknesses

### Fatal
None.

### Major

- **No error bars, confidence intervals, or multiple runs are reported.** The paper reports single-point MAE values for each model on each task (Figures 2–4) with no indication that experiments were run with multiple random seeds or training restarts. For a benchmark whose stated purpose is to evaluate and compare models, the absence of uncertainty quantification means the reader cannot assess whether observed differences between models are robust or within the noise of a single training run, or whether the generalisation gap itself is statistically significant. The paper uses Bayesian hyperparameter optimisation to find the best single configuration but does not report variance across restarts with that configuration. [favorability=0.00]

- **No non-neural baselines are provided, so the severity of the failure is uncalibrated.** All evaluated models are neural network MLFFs (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2). There are no classical force field baselines (e.g., UFF, GAFF, MMFF94) or simple regression baselines. Classical force fields, despite being less accurate on ID data, might generalize better on OOD tasks because they encode explicit physical functional forms (harmonic bond potentials, Lennard-Jones non-bonded terms). Without such baselines, the claim that models "fail" on OOD tasks is hard to calibrate against the intrinsic difficulty of the generalization problem itself. [favorability=-1.08]

### Minor

- **The ground-truth labels come from GFN2-xTB, a semi-empirical tight-binding method, not from DFT.** The paper acknowledges this as a "balance between computational efficiency and accuracy," but the central question — whether models learn "underlying physical principles" — is evaluated against a reference that is itself an approximation to those principles. If GFN2-xTB's systematic errors correlate with the compositional shifts being tested (e.g., its accuracy degrades for longer alkane chains or certain functional group combinations), poor OOD performance could partly reflect models failing to replicate GFN2-xTB's particular approximation errors rather than failing to generalize physically. A sanity check comparing GFN2-xTB against a higher-level method on a small subset of OOD configurations would strengthen confidence. [favorability=1.91]

- **No consolidated results table.** The paper relies entirely on figures (Figures 2–4). A single table consolidating ID MAE, OOD MAE, and their ratio across all task×model combinations would allow readers to grasp the overall pattern much more efficiently than flipping between figures. This is a standard expectation for a benchmark paper. [favorability=0.73]

- **Algorithmic alignment (Xu et al., 2020) is introduced in Sec. 2.2 as an important concept but is never referenced in the analysis or conclusions.** For a benchmark paper, this is a missed opportunity — the results could be discussed through the lens of which architectural features align with each generalization task, and whether the observed rankings are consistent with alignment theory. [favorability=3.46]

- **No discussion of overfitting.** The training datasets are relatively small (e.g., 5 molecules × 2000 snapshots for Task 1 base). The paper does not discuss whether the poor OOD performance could be partly attributable to overfitting on limited training data, even though ID test performance is good. This is a natural question readers will ask. [favorability=2.89]

### Trivial
None.

## Nice-to-Haves

- **MD stability as an evaluation dimension.** The paper exclusively uses per-frame force/energy MAE. For molecular dynamics, a model with slightly higher per-frame MAE but systematic errors could produce stable trajectories, while a model with lower per-frame MAE but chaotic errors could produce unstable simulations. Adding a brief MD stability analysis (e.g., does the model conserve energy over a short simulation for an OOD molecule?) would directly connect the benchmark to practical relevance.

- **Per-molecule breakdowns for Tasks 2–4.** The Length Extrapolation results are shown per chain length (Figure 2), which is informative. For Tasks 2–4, only aggregate ID vs. OOD bars are shown (Figure 4). Per-molecule results would be informative and could be deferred to an appendix.

- **Foundation model discussion.** The paper excludes foundation models for valid scientific reasons (avoiding confounds from pre-training), but a brief discussion of where current foundation models would fall relative to the benchmark's design would strengthen the paper's scope.

## Removed Points

These points appeared in the input review but are removed by filtering rules:

1. **"Exclusion of foundation models is a weakness"** — REMOVED. The paper explicitly addresses this in Sec. 4.1: "we did not include any foundation models... The latter have been pre-trained on large and diverse sets of molecules, making it harder to untangle memorisation and generalisation effects." This is a reasonable justification within the paper's stated scope.

2. **"Augmented variant of Task 2 description is confusing"** — REMOVED as a minor presentation issue below the threshold for inclusion as a core weakness; the description is reasonably clear upon careful reading.

3. **"Results repeated without much variation"** — REMOVED as a subjective stylistic observation, not an evidence-based weakness.

4. **"Per-molecule breakdowns for bar-chart tasks should be in main paper"** — REMOVED. The harsh critic themselves notes this is best deferred to an appendix; requesting it as a main-paper weakness is inappropriate.

5. **Generic/superficial strengths** (e.g., "the paper addressed an important problem" without specific evidence) — REMOVED. Strengths must be concrete and grounded in specific paper content.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Run all experiments with at least 3–5 random seeds and report variance (e.g., error bars in figures, ±std in a summary table). This is the single highest-leverage improvement for making the benchmark a reliable community reference.

2. Add at least one classical force field baseline (e.g., UFF or GAFF) so the community can calibrate whether the OOD results reflect a fundamental limitation of learned force fields or a specific weakness of current neural architectures.

3. Add a single consolidated table reporting ID MAE, OOD MAE, and their ratio across all task×model combinations.

4. Validate GFN2-xTB predictions against a higher-level method (e.g., ωB97X-D or PBE0 with a larger basis set) on a small subset of OOD configurations as a sanity check.

5. Include a brief discussion of whether the small training set sizes could induce overfitting, and how this relates to the observed OOD errors.

## Score and Decision

**Calibration summary:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| EGraFFBench | NvJxTjTQtq.md | 6.00 | R1/R2 | Yes | Similar MLFF benchmark paper; had severe implementation concerns (MD17 results much worse than reported, favorability -1.12) and novelty criticisms (favorability -4.22) that are not present in our paper |
| Distribution Shifts for MLFFs | Xk9Q0CrJQc.md | 6.25 | R1/R2 | Yes | Addresses OOD generalization with proposed mitigation methods; weakness favorability as low as -4.17 (performance far from chemical accuracy) |
| GDL-DS | LixGd92Wri.md | 5.67 | R2 | Yes | Broader GDL OOD benchmark; had foundational logical issues (favorability -2.45) and inaccurate claims about prior work (favorability -0.18) |
| AU-GOOD framework | qFZnAC4GHR.md | 6.67 | R2 | Yes | OOD evaluation framework for biochemical domain; had utility/novelty criticism at -5.66, more severe than any weakness in our paper |
| MatText | ihwRfc4RNw.md | 4.00 | R1 | No | Materials modeling benchmark, less directly relevant |
| BenchMol | 1JgWwOW3EN.md | 2.50 | R1 | No | Multi-modality MRL benchmark, less directly relevant |

**Round-1 bracket:** Between 5.5 and 7.5, based on comparison with EGraFFBench (6.00) and Distribution Shifts for MLFFs (6.25), which are the most topically similar papers. Those papers had weaknesses with favorability ratings substantially lower (more negative) than any weakness in the paper under review, suggesting the paper is at least as strong as those anchors.

**Round-2 narrowing:** Compared item-by-item favorability against EGraFFBench (6.00), Distribution Shifts (6.25), GDL-DS (5.67), and AU-GOOD (6.67). The paper's most negative weakness (favorability=-1.08, no non-neural baselines) is less severe than the worst weaknesses in all four anchors (EGraFFBench had -4.22, Distribution Shifts had -4.17, GDL-DS had -2.45, AU-GOOD had -5.66). The paper's highest-favorability strengths (12.32, 12.18) are competitive with or exceed the anchors' best strengths (EGraFFBench 13.72, Distribution Shifts 13.22). This places the paper at the upper end of the bracket, above the pure-benchmark papers (EGraFFBench at 6.00, GDL-DS at 5.67) and toward the level of the stronger papers (AU-GOOD at 6.67).

The benchmark design is genuinely thoughtful and the empirical finding is important. However, the two major weaknesses — no error bars and no non-neural baselines — are real methodological gaps for a paper aspiring to be a community reference benchmark. These are fixable but prevent the paper from reaching the 7+ range in its current form.

**Final score: 6.5**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>