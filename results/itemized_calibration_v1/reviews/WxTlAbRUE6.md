## Summary

This paper introduces GMD-25, a benchmark for evaluating compositional generalization in machine learning force fields (MLFFs). It comprises four tasks—Length Extrapolation, Functional Group Composition, Functional Group Duplication, and Functional Group Combination—designed so that all atomic/molecular components appear in training but their combinations are withheld. Experiments on five diverse MLFF architectures (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2) show that all models fail systematically on OOD tasks, with errors 1–2 orders of magnitude above in-distribution errors, and that ID and OOD performance are not correlated.

---

## Strengths

- **Well-motivated and clearly articulated gap.** Existing MLFF benchmarks (MD17, MD22, WS22, Transition1x) test configurational diversity or reaction pathways but do not systematically probe compositional generalization to unseen molecules. The paper's central premise—that standard in-distribution evaluation conflates interpolation with genuine physical understanding—is well-supported and timely. The four tasks are directly grounded in the compositional generalization literature (Hupkes et al., 2020) and designed so that all atomic/molecular components appear in training, isolating the compositional gap.

- **Honest and informative empirical findings.** All five evaluated models fail on OOD tasks. The paper does not spin this result or claim a SOTA improvement; it straightforwardly documents that current architectures do not compositionally generalize. The observation that ID and OOD performance are not correlated (e.g., EquiFormerV2 excels on forces but collapses on energy OOD) is informative and nontrivial, making the benchmark valuable as a diagnostic tool.

- **Diverse architectural coverage.** The benchmark spans invariant GNNs (SchNet), equivariant MPNNs (PAINN, GemNet, DimeNet++), and equivariant Transformers (EquiFormerV2). This breadth allows the paper to identify that no architectural family handles compositional generalization, strengthening the conclusion that the problem is structural, not architecture-specific.

---

## Weaknesses

### Fatal
None.

### Major

- **No uncertainty quantification across training runs.** All results are reported as point estimates with no standard deviations, confidence intervals, or any indication of variance. The paper makes comparative claims (e.g., "GemNet overall performs best" for Tasks 2–3, "EquiFormerV2 demonstrates the strongest OOD performance" for Task 4) without statistical backing. Given the small training sets (e.g., 5 molecules × ~2000 snapshots for base Length Extrapolation) and inherent neural network training stochasticity, the reader cannot assess whether observed differences between models are systematic or simply noise. Reporting results over at least 3 random seeds is needed to support comparative claims in a benchmark whose purpose is model comparison.

- **The small training set sizes confound generalization failure with data insufficiency.** The training sets are deliberately small (e.g., 5 molecules for base Length Extrapolation, ~10 molecules across the chain length range for Functional Group Composition), placing every model in a low-data regime where even in-distribution errors may be high. The central claim—that models fail at compositional generalization—is confounded with the possibility that models simply lack sufficient data to learn the potential energy surface for the training molecules themselves. The paper does not address this, e.g., by (a) showing how ID performance scales with more training data for a fixed molecule, (b) providing a learning curve analysis, or (c) comparing to a simple classical force field baseline (UFF, MMFF94) that might capture basic physics with minimal data. Without this, the headline result is ambiguous about *why* models fail.

### Minor

- **GFN2-xTB reference labels limit the scope of the "physical principles" claim.** The paper frames the benchmark as testing whether models learn "the underlying physical principles" (Abstract) or "capture fundamental physical principles rather than dataset-specific patterns" (Conclusion). However, all labels come from GFN2-xTB, a semi-empirical tight-binding method. The benchmark therefore tests generalization within the GFN2-xTB approximation, not to ground-truth physics (e.g., DFT or CCSD(T)). If GFN2-xTB makes systematic errors for certain molecular configurations (e.g., longer alkanes, specific functional group interactions), the benchmark may measure how well MLFFs replicate those errors. A more precise framing would strengthen the paper.

- **Limited diagnostic analysis of *how* models fail.** The paper reports *that* models fail but offers almost no analysis of error modes. For example: do errors concentrate on specific atoms (e.g., near the functional group vs. on the carbon chain)? Are force directions systematically wrong, or just magnitudes? For Length Extrapolation, does error grow linearly with chain length or jump catastrophically at the OOD boundary? Such diagnostics are what make a benchmark useful for guiding architecture design, and their absence limits the paper's impact.

- **Missing discussion of task feasibility from first principles.** The paper asserts that "the training data is chosen such that generalisation to the test examples should be feasible for models that learn the physical principles" (Abstract), but does not discuss substantive challenges. For Functional Group Composition, is it known that a carboxylic acid's PES can be accurately decomposed into alcohol and aldehyde contributions? If cooperative effects between the carbonyl and hydroxyl exist that are not reducible to separate contributions, even a perfect physical model would fail. Acknowledging this subtlety would improve the paper.

### Trivial
None.

---

## Nice-to-Haves

- Including a simple non-learned baseline (e.g., UFF or GFN2-xTB itself recomputed on test molecules) would establish the reference error floor and contextualize the ML failures.
- Adding a data-scaling control (e.g., training on varying amounts of in-distribution data to observe ID error saturation) would help disentangle compositional failure from data insufficiency.
- Reporting results over multiple random seeds with error bars would strengthen the comparative claims.

---

## Removed Points

These points were flagged by the input reviews but are removed per the filtering rules; they should be treated with caution:

1. **Figure inconsistencies (PBE0 and m4s).** The Harsh Critic flagged "PBE0" (Figure 2) and "m4s" (Figure 3) as undefined model names. These strings appear in OCR-extracted text from figure images, not in the paper's written content. Per Hard Rules, criticisms about garbled text / OCR artifacts from figure extraction are formatting artifacts and are removed. The original submission figures likely have correct labels.

2. **16 fs timestep concern.** The Harsh Critic questioned the 16 fs timestep as too large for AIMD. However, the paper's pipeline uses FlashMD (a fast approximate MD surrogate) at this timestep for *conformational sampling* only; the energy/force labels are subsequently recomputed at high fidelity with GFN2-xTB. The reviewer appears to have missed this two-stage pipeline. This concern is not applicable.

3. **Missing appendix content (hyperparameters, data splits).** Criticisms about absent appendix details, missing proof steps deferred to the appendix, or underspecified hyperparameter search ranges in the main text are removed per Hard Rules: the parser strips appendices from all papers, and these details exist in the original submission.

4. **Reproducibility nitpicks.** Criticisms about undisclosed implementation details or training log availability are removed per Hard Rules.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Add multiple random seeds.** Report all results over at least 3 random seeds with standard deviations or confidence intervals. This is essential for a benchmark that makes comparative claims between models.
2. **Disentangle data insufficiency from compositional failure.** Add a learning-curve or data-scaling experiment (e.g., train on increasing subsets of in-distribution data) to show whether ID error saturates at a reasonable level given the full training set. Add a simple classical force field baseline (UFF, MMFF94) to establish whether minimal-data physics can partially solve the tasks.
3. **Add diagnostic error analysis.** Report per-atom errors, directional force error decomposition, and chain-length scaling of OOD error. This would make the benchmark substantially more actionable for guiding architecture improvements.
4. **Reframe the "physical principles" language.** Acknowledge more explicitly that the benchmark evaluates generalization within the GFN2-xTB approximation, not to ground-truth quantum mechanics.

---

## Calibration Anchors

| Anchor | Path | Avg Score | Round | Itemized? | Comparison to reviewed paper |
|--------|------|-----------|-------|-----------|------------------------------|
| EGraFFBench | NvJxTjTQtq.md | 6.00 | Round 1 | Yes | MLFF benchmark paper. EGraFFBench had severe result-correctness doubts (weight -5) not present here, and was more comprehensive (MD simulation metrics). GMD-25 has clearer task design but less thorough evaluation. |
| Distribution Shifts for MLFFs | Xk9Q0CrJQc.md | 6.25 | Round 1 | Yes | Combined diagnostic analysis + proposed mitigation method. Stronger empirical contribution (proposed method improved OOD), but had weaknesses about practical utility (weights -5, -4). GMD-25 is a pure benchmark without a proposed solution. |
| Steering 3D Molecule Generation | an3kPpce6b.md | 5.25 | Round 2 | No | OOD molecule generation with proposed method. Less topically aligned; scores suggest 5–6 range for OOD-in-molecules contributions with methodological gaps. |
| BenchMol | 1JgWwOW3EN.md | 4.80 | Round 2 | Yes | Molecular representation learning benchmark. Had more severe weaknesses (simple labels, non-functional link, weight -4 each). GMD-25 is more focused and avoids those issues, justifying higher placement. |
| MatText | ihwRfc4RNw.md | 4.00 | Round 2 | Yes | Materials benchmark. Criticized for limited novelty and thin contributions (weights -3, -3). GMD-25 has stronger contribution clarity. |

**Round 1 bracket:** 4.0–6.5, with the strongest topical similarity to EGraFFBench (6.00) and the Distribution Shifts paper (6.25).

**Narrowing:** GMD-25 shares the "thorough benchmark with clear task design" positive from EGraFFBench (+4) but lacks EGraFFBench's MD simulation evaluation breadth. Its two core weaknesses (no error bars, data confound) are serious but not fatal—they weaken comparative claims and interpretation rather than invalidating the core finding. The Distribution Shifts paper had a weight -5 weakness (performance far from chemical accuracy) that is not applicable here since GMD-25 is a diagnostic benchmark, not a proposed method. Compared to BenchMol (4.80) which had severe reproducibility and contribution issues, GMD-25 is notably stronger. The weighted-item comparison places it between BenchMol (4.80) and EGraFFBench (6.00).

**Final score:** 5.5 — a solid benchmark contribution with a well-motivated core and thoughtful task design, but with two meaningful methodological gaps (no error bars, data-insufficiency confound) that need to be addressed before it can serve as a definitive diagnostic. The paper is above a strong reject because the core idea and task design are sound, but below borderline acceptance because the evaluation methodology needs substantive strengthening.

---

## Score and Decision

**MY FINAL SCORE:** <score>5.5</score>
**MY FINAL DECISION:** <decision>Reject</decision>