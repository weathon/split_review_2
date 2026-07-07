Now let me write the final review.

## Summary

This paper proposes a compositional meta-learning framework where tasks are represented as structured combinations of reusable computations (modules). The key idea is to learn a generative model of tasks (gating RNN for between-module dynamics + module RNNs for within-module dynamics) from training tasks, then solve new test tasks through probabilistic inference (particle filtering) rather than parameter updates. The framework is demonstrated on two synthetic domains (rule learning with vector shifts, motor learning with trajectory chunks), showing recovery of ground-truth modules and transitions, inference from single episodes, handling of sparse feedback, and generalization to longer tasks.

## Strengths

- **Clean formalization of learning/inference separation.** The core idea — learning a generative model of task structure at training time, then solving new tasks through probabilistic inference rather than gradient-based adaptation — is clearly articulated and theoretically well-motivated. The HMM analogy (with RNNs replacing transition/emission matrices) is pedagogically effective and clarifies both the expressivity gains and the retained inference machinery.

- **Well-designed control experiments (Figure 3).** The three control models (standard RNN without task ID, RNN with task ID, architecture without gating network) cleanly isolate each component's contribution. The "flat transitions" control is particularly informative: modules alone suffice for dense-feedback inference, but the gating network is essential for sparse-feedback inference. This is a genuine ablation, not a straw man.

- **Compelling qualitative demonstrations of constrained hypothesis testing under sparse feedback (Figures 2e, 4e).** The visualization of the posterior collapsing during learned module durations and becoming uniform at switch points — driven purely by learned gating dynamics rather than sensory signal — is striking. The motor task's branching dotted-line hypotheses provide an intuitive picture of what particle filtering achieves internally.

- **Generalization to longer tasks (Figures 2f, 3f).** The demonstration that the model solves test tasks 4× longer than training tasks, while gradient-based methods with frozen recurrent weights cannot, is the strongest quantitative result. It shows genuine compositional generalization beyond pattern matching.

## Weaknesses

### Fatal
None.

### Major

- **Missing experimental comparison with the closest prior work (Alet et al., 2019, "Modular Meta-Learning").** The paper identifies this work as "most similar in spirit" and explicitly claims improvement: "We effectively replace this search by probabilistic inference on learned structure, greatly improving sample efficiency" (Discussion). Alet et al. also proposes modular composition without test-time parameter updates — making it the single most important baseline — yet no experimental comparison is provided. This claim of superiority is unsupported.

- **Narrow empirical scope relative to stated generality.** The two experimental domains are structurally isomorphic: both use 6 operations/skills paired into identical durations (3,3,4,4,5,5), concatenated 3 per task. The only substantive difference is input dependence. The paper's claims about "compositional meta-learning" as a general framework are tested on what is essentially one task structure with two surface forms. The paper acknowledges this as proof-of-principle (Discussion, line 194), but the gap between the general framing (abstract, introduction) and the narrow evidence remains substantial. Neither domain breaks the specific duration pattern, uses variable numbers of modules per task, or introduces hierarchical composition — all of which would better support the claimed generality.

### Minor

- **The paper reports the MAP sequence as argmax_z p(z_t|y_{1:T}) (full smoothing) in Figure 2d caption, but the method section only describes forward particle filtering producing p(z_t|y_{1:t}).** The paper does not clarify whether smoothing (forward-backward) is actually used for the final results or whether the filtering distribution suffices for MAP extraction. This is an important methodological detail for reproducibility.

- **Motor task required non-trivial architectural modifications.** For the motor domain the paper: removes input x_t, resets module hidden states after switches, adds module-specific weights W_~h^z, and changes the particle filter proposal distribution during training (lines 127-128). These adaptations are reasonable but suggest the architecture requires task-specific engineering beyond what "naturally accommodates both" implies. The paper does not test whether the rule-learning setup works with the motor-task configuration or vice versa.

- **No sensitivity analysis for the number of particles K.** Particle filtering is approximate inference, and both training (marginal likelihood via Equation 8) and inference quality depend on K. A sweep over K values would inform practical use of the method.

### Trivial
None.

## Nice-to-Haves

- Report wall-clock training time and training data requirements for a fairer comparison with gradient-based methods (test-time efficiency is demonstrated, but the training-side trade-off is opaque).
- Describe the gumbel-softmax temperature schedule (or note it in the main text rather than deferring entirely to the appendix), since backpropagating through discrete module selections is central to training stability.
- Compare against Alet et al. (2019) on the same synthetic tasks — this would directly substantiate the claimed advantage and is the single highest-leverage improvement.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- "Training cost comparison is one-sided": The paper's comparison is about test-time inference vs test-time gradient adaptation, which is a fair basis. Both sides incur training costs; the framing is appropriate for the claim made.
- "MAML/MLDG hyperparameters not specified in main text": The paper provides code as supplementary material; implementation details are standard and would be in the appendix/code (stripped by parser).
- "\"One-shot task acquisition\" heading is imprecise": Semantic nitpick about terminology that does not affect the paper's substance.
- "Abstract over-promises on 'without parameter updates'": The paper clearly refers to no test-time parameter updates, which is standard inference.
- "Frozen recurrent weights finding undermines baselines": This is the paper's own interesting finding discussed in its results section, not a weakness.
- "Thalamic gating discussion is tangential": Subjective opinion about discussion section content; the authors are entitled to include broader connections.
- "Gumbel-softmax temperature not detailed in main text": The appendix covering this exists in the original submission but was stripped by the parser.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Compare against Alet et al. (2019) on the same synthetic tasks** — this is the most important missing evidence. The paper already claims superiority; an experimental comparison would convert an unsupported claim into substantiated evidence.
2. **Add at least one task with a genuinely different structure** (e.g., different module durations per task, variable numbers of modules, hierarchical composition) to demonstrate the framework's generality beyond the single (3,3,4,4,5,5) structure appearing in both current domains.
3. **Clarify whether the MAP sequence (red dots) uses forward filtering or forward-backward smoothing**, and document the smoothing procedure if used.
4. **Report sensitivity to the number of particles K** and provide the gumbel-softmax temperature schedule in the main text.

## Score and Decision

**Calibration summary:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| H98CVcX1eh (Discovering modular solutions) | calibration | 6.50 | R1 | Yes | Stronger theory, similar synthetic scope, but clarity weakness (-6.44); our paper has weaker theory but stronger clarity |
| D1w3huGGpu (Compositional Interfaces) | calibration | 4.75 | R1 | Yes | Much more severe weaknesses (-10.52 limited contribution, -9.79 no comparison); our paper is stronger |
| pEKJl5sflp (Scalable Modular Network) | calibration | 6.00 | R1 | Yes | Similar limited experimentation weakness (-6.74) and missing comparison (-4.35); our missing Alet comparison is similarly severe |
| 7MYu2xO4pp (Gradient-based task inference) | calibration | 5.25 | R1 | Yes | Similar profile — strong conceptual contribution with moderate empirical scope; our strengths have higher weights (+5.61 vs +4.29 max) |
| 6XodKiDS3B (Particle filter continual learning) | calibration | 5.50 | R2 | Yes | Mixed reviews (3,8,6,5); extreme -13.06 weakness (theory-experiment mismatch) much worse than any issue in our paper |
| nnicaG5xiH (Interpretable Meta-Learning) | calibration | 6.33 | R2 | Yes | Strong theory/interpretability contribution; similar weakness severity (-9.75 novelty) but had theoretical results our paper lacks |
| VZTFUtldbC (MeMo) | calibration | 4.75 | R1 | No | Weaker than our paper on strength weights |
| I7kpf3mZ4n (Meta-OCL) | calibration | 5.25 | R3 | No | Comparable profile |

**Round-1 bracket:** 4.0–5.5. The paper's weighted-item profile — very strong strengths (+5.61, +4.99, +4.84, +3.89) paired with severely weighted major weaknesses (-7.24, -5.42) — places it clearly above the 4.75 anchors (which have -10+ weaknesses) but below the 6.0+ anchors (which have stronger theoretical contributions or broader experiments). The -7.24 weight on the missing Alet comparison is the decisive factor: the paper claims superiority over the closest prior work without providing evidence. This gap prevents a score above 5.5.

**Round-2 narrowing:** 4.5–5.5. Comparison with 5.25–5.50 anchors confirms that papers at this level have similar weakness profiles (one or two major empirical gaps) but compensations our paper lacks (e.g., 6XodKiDS3B had theoretical guarantees despite the -13.06 weakness; I7kpf3mZ4n had a broader investigation of the phenomenon across modalities). The paper under review has no theoretical component that could compensate for its empirical narrowness.

**Final score: 5.0** — a paper with a genuinely novel and well-articulated core idea, clean ablations, and compelling qualitative results, but whose empirical scope (structurally isomorphic toy tasks) and missing critical baseline (Alet et al., 2019) leave its central claims of generality and improvement over prior work unsupported. The idea is solid and could be competitive with strengthened experiments.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>