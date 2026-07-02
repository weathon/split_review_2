## Summary
# Final Review Report

## Summary

This paper introduces GMD-25, a benchmark for evaluating compositional generalisation in Machine Learning Force Fields (MLFFs). The benchmark comprises four tasks—length extrapolation, functional group composition, functional group duplication, and functional group combination—each designed so that training molecules contain all required atomic/functional building blocks while test molecules recombine them in novel ways. The authors evaluate five representative MLFF architectures (SchNet, PAINN, DimeNet++, GemNet, EquiFormerV2) on these tasks and report substantial generalisation gaps, with out-of-distribution errors often one to two orders of magnitude larger than in-distribution errors. A notable finding is that the models with the best in-distribution performance are often not the best out-of-distribution performers, suggesting that current leaderboard-driven evaluation may not incentivise architectures that learn physically transferable representations. The benchmark and its associated data generation toolkit represent a timely contribution to the MLFF community, addressing an important gap in existing evaluation practices.

## Strengths
**1. Well-motivated and timely research question.** The paper addresses a genuine gap in MLFF evaluation: standard benchmarks test models on in-distribution configurations, making it difficult to assess whether models learn physically meaningful representations or simply interpolate. The compositional generalisation framing provides a principled way to probe this distinction, and the four tasks are thoughtfully designed to isolate different aspects of generalisation (length scaling, functional group recombination, duplication, and asymmetric combination).

**2. Clean experimental design with diagnostic tasks.** The benchmark tasks are constructed so that training data contains all elementary building blocks, and only their composition is novel. This design ensures that failure on OOD test sets can be attributed to a lack of compositional generalisation rather than missing atomic/functional primitives. The inclusion of both base and augmented variants for Tasks 1-2 allows controlled analysis of whether additional compositional demonstrations improve transfer.

**3. Systematic evaluation across architectural families.** The paper evaluates five models spanning invariant GNNs (SchNet), equivariant message passing (PAINN), angle-aware models (DimeNet++, GemNet), and equivariant Transformers (EquiFormerV2). This breadth allows the community to assess how architectural design choices correlate with generalisation behaviour.

**4. Important empirical findings with practical implications.** The dissociation between ID and OOD model rankings, and the decoupling of energy vs. force generalisation (e.g., EquiFormerV2 excelling on forces but failing on energies), are non-trivial findings that should influence both benchmarking practice and architecture design. The observation that all models fail on functional group composition and duplication, regardless of architectural sophistication, sets a clear challenge for future work.

**5. Reproducibility-oriented release.** The commitment to release curated data splits, preprocessing scripts, and the full dataset (118 molecules, 296,534 labelled geometries) on acceptance, together with a forked fairchem framework for model training, addresses a common weakness in benchmark papers and should facilitate rapid adoption by the community.

## Weaknesses
**1. Missing statistical rigor and variance reporting (Major).** All results are reported as point estimates without confidence intervals or multi-seed variance. Given that each training set contains only ~2000 snapshots per molecule, model performance may be sensitive to random initialization. Without standard deviations or significance tests, the reported model rankings (e.g., "EquiFormerV2 consistently exhibits the lowest Forces MAE", "GemNet overall performs best") cannot be assessed for statistical reliability. This is a critical gap because the paper's main claims depend on comparing models against each other and against their ID baselines.

*Action:* Report all metrics as mean ± std over ≥3 random seeds. Add a paired statistical test (e.g., Wilcoxon signed-rank) when comparing model pairs on OOD performance. Include a supplementary table with full numerical results.

**2. Energy metric normalization confound (Major).** The energy MAE is computed per molecule (1/M Σ|Êⱼ - Eⱼ|) while force MAE is per-atom per-component (1/(3N) Σᵢ Σ_c |...|). Since total energy is an extensive quantity that scales with system size, per-molecule energy MAE will naturally increase for larger molecules. This confounds the interpretation of energy generalisation in Task 1 (Length Extrapolation), where test molecules (C7–C13) are systematically larger than training molecules (C2–C6). The observed energy MAE increase may partly reflect system-size scaling rather than genuine generalisation failure.

*Action:* Add per-atom energy MAE as a complementary metric. Replot Figure 2 with per-atom energy MAE to verify whether the OOD increase persists after size normalization. Discuss the scaling effect explicitly.

**3. ID-optimized hyperparameters may underestimate OOD performance (Major).** The two-stage tuning strategy uses Bayesian optimisation to minimise ID validation error. This means all models are ID-optimal before OOD evaluation. It is plausible that hyperparameters that improve OOD performance differ from ID-optimal ones (e.g., different learning rates, weight decays, or cutoff radii). Without comparing default vs. optimised OOD results, the reported OOD gaps may partly reflect ID-overfitting rather than architectural limitations.

*Action:* Report OOD errors for both default and ID-optimised hyperparameters in the appendix. If the ranking changes, discuss implications. Add a sensitivity analysis showing OOD performance as a function of key hyperparameters (e.g., cutoff radius, number of message-passing layers).

**4. Limited analysis of failure modes and architectural causes (Major).** The paper convincingly demonstrates that all models fail on compositional generalisation, but it does not analyse *why* they fail. Potential causes include: insufficient receptive field (message-passing depth), inability to count functional groups, reliance on spurious correlations (e.g., molecular weight), or insufficient many-body interaction order. Without failure-mode analysis, the benchmark's diagnostic value is reduced — it tells the community *that* models fail, but not *what to fix*.

*Action:* For each task, add one targeted analysis experiment. For example: (a) for Length Extrapolation, test whether increasing the number of message-passing layers improves OOD performance; (b) for Functional Group Duplication, test whether adding a counting mechanism or global feature helps; (c) for Composition, test whether models capture carbonyl group effects additively by comparing predicted vs. linear-combination baselines.

**5. Absence of explicit limitations section (Minor).** The conclusion summarises findings but does not bound the benchmark's scope or discuss known limitations. Critical unaddressed questions include: (a) Would results generalize from GFN2-xTB to DFT-level labels? (b) Does the benchmark cover only linear alkyl chains, excluding branched/cyclic structures? (c) How do foundation models (MACE-MP, etc.) perform — their exclusion means the benchmark's hardest baseline is unknown? Including these bounds would strengthen scientific credibility and guide appropriate usage.

*Action:* Add a "Limitations and Future Work" subsection that explicitly discusses scope boundaries, potential confounders, and the most important next experiments.

**6. Energy-force dissociation in augmented Length Extrapolation is under-analysed (Minor).** The finding that EquiFormerV2 performs best on forces but worst on energies in the augmented variant is striking and practically important, yet the paper offers no mechanistic explanation. If energy errors are systematic offsets (constant shift per molecule), they may be correctable post-hoc; if they reflect wrong PES curvature, force accuracy may also be unreliable for long trajectories.

*Action:* Add an analysis of whether energy errors are predominantly systematic offsets or structural shape errors. If possible, visualise predicted vs. true potential energy surfaces for a representative molecule.

**7. Toolkit description omits key reproducibility details (Minor).** The data generation pipeline is described at a high level, but several details needed for exact reproduction are missing: (a) whether the two trajectories per molecule use independent random seeds; (b) the SCF convergence threshold for GFN2-xTB; (c) the exact thermostat coupling constant; (d) whether any frames are discarded (equilibration period). While the full toolkit will be released, these details affect whether early adopters can reproduce the data generation process independently.

*Action:* Add a table summarising all simulation parameters (thermostat, timestep, total steps, equilibration frames, SCF threshold, random seed protocol) in the main text or appendix.

## Score
**Final Score: 6/10**

**Scoring rationale:** The paper addresses a timely and important problem with a clean experimental design. The four compositional generalisation tasks are well-conceived, and the empirical finding that ID and OOD model rankings diverge is non-trivial and practically significant. However, the current manuscript has three weaknesses that prevent a higher score: (1) the absence of any statistical variance or significance testing undermines confidence in the reported model rankings; (2) a confound in the energy metric normalization (per-molecule vs. per-atom) weakens the central Length Extrapolation analysis; and (3) the lack of failure-mode analysis limits the benchmark's diagnostic value. These issues are addressable with reasonable additional experiments and analyses. The research value of the benchmark itself is high, and once the methodological gaps are closed, this work could become a widely used evaluation standard for the MLFF community.

---

### ASCII Diagrams

**ASCII Diagram — Paper Structure & Evidence Map**

```text
[Problem: MLFFs may interpolate rather than learn physical principles]
    |
    v
[Gap: No benchmark tests compositional generalisation of MLFFs]
    |
    v
[GMD-25 Benchmark: 4 compositional generalisation tasks]
    |
    +-- Task 1: Length Extrapolation (C2-C6 train, C7-C13 test)
    |       Evidence: Figure 2-3, Energy & Force MAE
    |       Gap: No per-atom energy normalization, no variance
    |
    +-- Task 2: Functional Group Composition (alcohol+aldehyde -> acid)
    |       Evidence: Figure 4a-d
    |       Gap: No ablation for augmentation mechanism
    |
    +-- Task 3: Functional Group Duplication (mono -> di-carboxylic)
    |       Evidence: Figure 4e-f
    |       Gap: No analysis of why models fail (receptive field? counting?)
    |
    +-- Task 4: Functional Group Combination (symmetric -> asymmetric)
    |       Evidence: Figure 4g-h
    |       Gap: Smaller gap observed but not explained
    |
    v
[Core Finding: ID vs OOD model rankings diverge; all models fail on Tasks 2-3]
    |
    v
[Weak evidence layer: No multi-seed variance, no significance tests, no failure mechanism analysis]
```

**ASCII Diagram — Revision Strategy Roadmap**

```text
Priority | Problem                          | Fix                                       | Expected Impact
---------+----------------------------------+-------------------------------------------+------------------
P0       | No statistical rigor             | Add 3+ seeds, std, significance tests     | Validates model rankings
P0       | Energy metric confound           | Add per-atom energy MAE, re-plot Fig 2   | Removes size confound
P0       | ID-optimized HPs mask OOD perf   | Compare default vs optimized OOD results  | Quantifies HP effect
P1       | No failure-mode analysis         | Add probing experiments per task          | Diagnostic value
P1       | Missing limitations section      | Add scope/limitations discussion          | Scientific completeness
P2       | Toolkit reproducibility gaps     | Add SCF threshold, seed protocol, etc.    | Exact reproducibility
P2       | Energy-force dissociation subtle | Add offset analysis, PES visualization    | Mechanism understanding
```

**ASCII Diagram — Related-Work Taxonomy Tree (Layered)**

```text
ML Force Field Evaluation (Root)
|
+-- Branch 1: Equilibrium / Near-Equilibrium Benchmarks
|   +-- Leaf 1.1: Small molecules at minima (MD17, QM9, ANI-1)
|   +-- Leaf 1.2: Flexible systems / large molecules (MD22)
|   +-- Leaf 1.3: Configurational diversity (WS22)
|
+-- Branch 2: Out-of-Equilibrium / Reactive Benchmarks
|   +-- Leaf 2.1: Reaction pathways (Transition1x)
|   +-- Leaf 2.2: Excited-state dynamics (xxMD)
|
+-- Branch 3: Generalisation / OOD Benchmarks
|   +-- Leaf 3.1: Property extrapolation (BOOM)
|   +-- Leaf 3.2: Scaffold / protein-family splits (DrugOOD)
|   +-- Leaf 3.3: Compositional & structural splits (MatBench)
|   |
|   +-- [This paper] GMD-25: Compositional generalisation for MLFFs
|       +-- Length extrapolation
|       +-- Functional group composition
|       +-- Functional group duplication
|       +-- Functional group combination
|
Note: Novelty verification is deferred to manual literature review
(Retrieval-Disabled Mode: external paper search unavailable in this run).
```

---

**Post-Revision Target: [7, 8]/10** — If the authors address the P0 items (statistical rigor, metric normalization, HP sensitivity analysis) and add at least one failure-mode analysis, the paper would merit a score of 7-8, reflecting solid methodological quality and high community value.