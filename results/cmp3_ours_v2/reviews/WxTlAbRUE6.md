Here is the final consolidated review.

---

## Summary

GMD-25 is a benchmark for evaluating whether machine learning force fields (MLFFs) can compositionally generalize to unseen molecules. It introduces four systematically designed tasks — length extrapolation, functional group composition, functional group duplication, and functional group combination — that go beyond standard in-distribution evaluation. Experiments across five architectures (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2) show consistent and large OOD generalization gaps.

## Strengths

1. **Well-motivated gap-filling.** Standard MLFF benchmarks (MD17, MD22, Transition1x) train and test on the same molecules, conflating interpolation with genuine physical understanding. The paper correctly identifies this blind spot and addresses it directly (lines 9, 15).

2. **Systematic task design grounded in cognitive science literature.** The four tasks probe specific dimensions of compositional generalization (length generalization, systematicity) from Hupkes et al. (2020), rather than being ad hoc OOD splits. The base/augmented variants for Tasks 1 and 2 are a useful design feature for measuring whether additional relevant data closes the gap (Section 3.1).

3. **Honest empirical reporting.** The paper does not claim any model "solves" these tasks. Results show large generalization gaps across all architectures, and the decoupling between energy and force accuracy (EquiFormerV2 winning on forces but collapsing on energy OOD) is a genuinely informative finding (Section 4.3).

## Weaknesses

### Fatal

None.

### Major

1. **No uncertainty estimates for a benchmark paper.** All results are single-run point estimates with no error bars, standard deviations, or multiple-seed experiments. The training sets are small (~2000 snapshots per molecule), and neural network training on such data is seed-sensitive. For a benchmark intended as a community reference, the absence of any measure of variability means the reported numbers cannot be interpreted with confidence. The qualitative finding (all models show large OOD degradation) is robust, but specific performance rankings and gap magnitudes may not be reproducible.

2. **Inconsistent model labels in figures.** Section 4.1 lists the five evaluated models as SchNet, PAINN, DimeNet++, GemNet, and EquiFormerV2. However:
   - **Figure 2** caption lists "PBE0" (a DFT functional, not a model) instead of PAINN among its five models. If PBE0 is a reference baseline, the paper never explains this. If it is a labeling error for PAINN, it needs correction.
   - **Figure 3** caption lists "m4s" (undefined) alongside PAINN as a sixth model, with no explanation of what "m4s" refers to.
   
   These inconsistencies mean the reader cannot confidently map results to models, directly affecting the interpretability of every reported result.

### Minor

3. **Task 2 (Functional Group Composition) has a chemically questionable decomposition premise.** The paper states that a carboxylic acid (-COOH) "can be seen as a composition" of an alcohol (-OH) and an aldehyde (-CHO) (lines 68–72). Chemically, the electronic structure, resonance stabilization, and inductive effects of -COOH are not straightforwardly additive from -OH and -CHO. The paper partially acknowledges this (line 76: "we do not expect the model to learn the chemical reaction pathway"), but this does not resolve whether poor performance reflects a genuine failure of compositional generalization or an ill-posed decomposition. The task would benefit from quantitative evidence that -COOH energy/forces can be decomposed into -OH + -CHO contributions using the GFN2-xTB reference calculations themselves.

### Trivial

4. **Typo in method name.** Line 56: "GNF2-xTB" should be "GFN2-xTB" per the cited reference (Bannwarth et al., 2019).

## Nice-to-Haves

- Include at least one non-foundation model more recent than the evaluated set (e.g., MACE) to strengthen the claim that the benchmark tests "state-of-the-art" models.
- Add analysis of error types (which atoms/bonds concentrate errors, systematic vs. random errors) to increase diagnostic value. The appendix may contain some of this, but it would strengthen the main text.

## Removed Points

These points were flagged by the harsh critic but removed from the final review for the following reasons:

- **"No comparison with foundation models"** — REMOVED. The paper explicitly justifies excluding foundation models (line 104: "to untangle memorisation and generalisation effects"), which is a reasonable scoping decision.
- **"No baseline comparison with classical force fields (UFF, GAFF)"** — REMOVED. Not standard for MLFF benchmark papers and would not meaningfully probe compositional generalization.
- **"Reproducibility statement says 'will be made open-source upon paper acceptance'"** — REMOVED per hard rules: criticisms about release status/availability of cited entities must be removed.
- **"Include MACE"** — DEMOTED to Nice-to-Have.
- **"Add analysis of error types"** — DEMOTED to Nice-to-Have.
- **Section-by-section notes about related work completeness** — REMOVED. The critic's observations were descriptive, not pointing to specific omissions that harm the paper.
- **Several generic strengths** (e.g., "the motivation is well-grounded") — REFRAMED into specific, evidence-grounded strength statements.

## Novel Insights

None beyond the paper's own contributions. The key finding — that compositional generalization in MLFFs is systematically poor across architectures and that ID performance does not predict OOD performance — is the paper's own empirical contribution.

## Suggestions

1. **Rerun all experiments with at least 3 random seeds and report mean ± std.** This is the single most impactful improvement for establishing GMD-25 as a reliable benchmark reference.
2. **Resolve the PBE0/m4s labeling inconsistencies** in figure captions and legends. Clarify whether PBE0 is a reference baseline or a labeling error.
3. **Provide a quantitative chemical justification for Task 2's decomposition premise** or reframe the task as a general OOD probe without the "compositional" claim.
4. **Fix the "GNF2-xTB" typo** (line 56).

## Calibration Report

**Round 1 bracket:** 4.0–6.0 (narrowed to 5.0–6.0).

**Anchors retrieved:**

| Paper | Avg Score | Round | Comparison to GMD-25 |
|-------|-----------|-------|----------------------|
| EGraFFBench (NvJxTjTQtq.md) | 6.00 | R1 | Topically closest (MLFF benchmarking). Had more serious concerns (questionable experimental quality). GMD-25 has cleaner experiments but lacks error bars. |
| SimXRD-4M (mkuB677eMM.md) | 6.25 | R1 | Benchmark paper with larger dataset volume but lower task novelty. Both have limited real-world validation. |
| MatText (ihwRfc4RNw.md) | 4.00 | R1 | Materials benchmark with limited empirical insights over prior work. GMD-25 provides stronger empirical findings. |
| ECD (SBCMNc3Mq3.md) | 6.50 | R1 | Electronic charge density benchmark. Well-executed but different domain. |
| BenchMol (1JgWwOW3EN.md) | 4.80 | R1 | Multi-modal molecular benchmark with serious design concerns. GMD-25 has a clearer contribution focus. |
| DynamicsDiffusion (kKXIYUi8ff.md) | 3.00 | R1 | MD trajectory generation, different contribution type. |
| ACHIEVING DYNAMIC ACCURACY… (ItPYVON0mI.md) | 3.00 | R1 | CG potential paper, different contribution type. |
| Physics-Informed Weakly Supervised… (qfU5S4cddQ.md) | 5.00 | R1 | MLIP training method, not a benchmark paper. |

GMD-25 is most comparable to **EGraFFBench** (6.00, Reject). Both benchmark MLFFs on OOD tasks. EGraFFBench had more serious weaknesses (reviewers questioned whether experiments were run correctly). GMD-25's core experiments appear sound, but the absence of uncertainty estimates and figure-label inconsistencies are meaningful gaps for a benchmark paper. The paper's systematic task design grounded in compositional generalization theory gives it stronger novelty than EGraFFBench's general evaluation approach.

**Final calibrated score: 5.5** — reflecting that the paper has a genuine and well-motivated contribution, but the methodological gaps (no error bars, figure inconsistencies) prevent it from serving as a reliable reference benchmark in its current form.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>