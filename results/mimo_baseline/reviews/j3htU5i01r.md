## Summary
This paper proposes a compositional meta-learning framework that learns a probabilistic generative model of tasks, consisting of modular RNNs (for reusable computations) and a gating RNN (for sequencing statistics). New tasks are then solved through particle-filter-based probabilistic inference rather than parameter updates, enabling one-shot task acquisition even under sparse feedback. The approach is demonstrated on synthetic rule-learning and motor-learning tasks where it recovers ground-truth components and outperforms gradient-based meta-learning baselines in sample efficiency.

## Strengths
- **Novel and elegant framing**: Casting compositional meta-learning as inference in a learned probabilistic generative model — essentially an HMM with RNN-extended transition and emission functions — is a genuinely original conceptual contribution. The separation of "task syllables" (modules) from "task grammar" (gating) provides a clear inductive bias and a compelling narrative.
- **Strong control experiments**: Figure 3 systematically ablates the architecture (no task ID, uniform transitions, full model) and compares against gradient-based approaches (scratch, pre-trained, frozen-recurrent, MAML, MLDG), convincingly demonstrating that single-episode inference is qualitatively different from learning-based approaches.
- **Sparse feedback and length generalization**: The model handles sparse feedback through constrained hypothesis testing (Figures 2e, 4e) and generalizes to tasks four times longer than training tasks (Figure 2f) — both demonstrations that showcase the power of learned compositional structure beyond what standard meta-learning achieves.
- **Clean probabilistic formalism**: The generative model (Equations 1–8) and the particle filtering procedure are specified with mathematical precision, and the connection to HMMs is well articulated.

## Weaknesses
### Fatal
None.

### Major
- **Extremely narrow experimental scope**: Both task domains (shift operations, motor trajectories) share nearly identical structure — concatenation of fixed-duration segments drawn from a small pool. This structure perfectly matches the model's inductive bias. There is no evaluation on standard meta-learning benchmarks, continuous control tasks, or tasks with variable/dynamic modular structure. The paper acknowledges being "proof-of-principle," but for a top venue, two synthetic domains with the same temporal template are insufficient to convincingly demonstrate generality.
- **No experimental comparison to the closest prior work**: Alet et al. (2019) is discussed at length in the discussion as "most similar in spirit," using fixed modules with simulated annealing for test-time configuration search. Yet there is no empirical comparison to this method, which would have been the most informative baseline for evaluating the particle-filter inference approach.
- **Fairness of MAML/MLDG comparisons**: The tasks are discretely compositional with no continuous task parameters to adapt — precisely the setting where gradient-based meta-learning is weakest. The comparison demonstrates the qualitative speed difference between inference and learning, but doesn't disentangle whether the advantage comes from the compositional architecture, the probabilistic inference, or simply the problem being ill-suited for the baselines.

### Minor
- **Chicken-and-egg training instability**: The paper acknowledges that jointly learning modules and gating risks local minima but provides no experimental analysis (e.g., failure rate, sensitivity to initialization, module count) beyond showing single-seed learning curves.
- **Fixed module count**: The number of modules is predefined and must match or exceed the true number of operations. The model's behavior under over/under-specification (Figure A1) is discussed only briefly, and the paper offers no mechanism for automatic module discovery despite mentioning continual learning as future work.

### Trivial
None.

## Nice-to-Haves
- An experiment on a less synthetic benchmark (e.g., few-shot classification with compositional structure, or a procedurally generated environment with modular structure) to test robustness.
- Quantitative analysis of training stability across seeds and hyperparameters (module count, particle count, task diversity).
- Explicit comparison to Alet et al. (2019) on at least one shared task.

## Novel Insights
The paper's most compelling conceptual contribution is reframing meta-learning as "thinking" (inference over a learned compositional space) rather than "learning" (parameter updates), and showing that this distinction is not merely semantic but produces qualitatively different sample efficiency. The demonstration that the gating RNN learns non-Markovian transition statistics that constrain hypothesis spaces during sparse feedback — effectively enabling the model to "look ahead" based on learned task grammar — is a genuinely interesting finding that connects probabilistic graphical models with modular neural architectures in a principled way.

## Suggestions
- Add experiments on at least one domain with different structural assumptions (e.g., variable segment lengths, overlapping modules, or a standard meta-learning benchmark adapted to the compositional setting).
- Provide an empirical comparison to Alet et al. (2019) to substantiate the claimed improvement in sample efficiency through probabilistic inference over simulated annealing.
- Include quantitative analysis of training robustness: how often do runs converge to correct module assignments, and how sensitive is this to initialization and module count?

## Score and Decision
The paper presents a novel and theoretically grounded approach to compositional meta-learning with clean probabilistic formalism and interesting demonstrations of one-shot inference and sparse feedback handling. However, the experimental validation is limited to two very similar synthetic domains that perfectly match the model's inductive bias, with no comparison to the closest prior work and no evaluation on standard benchmarks. This limits confidence in the framework's generality beyond the demonstrated proof-of-concept.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: Reject