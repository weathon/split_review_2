## Summary

This paper proposes a compositional meta-learning framework that explicitly represents tasks as structured combinations of reusable computations. The model learns a probabilistic generative model consisting of a gating RNN (capturing between-module dynamics) and module RNNs (capturing within-module dynamics) from training tasks, then solves new test tasks through probabilistic inference (particle filtering) without any parameter updates. The authors demonstrate successful recovery of ground-truth components and one-shot task acquisition in rule learning and motor learning domains, including under sparse feedback conditions.

## Strengths

- **Principled probabilistic formulation**: The paper formalizes compositional meta-learning as inference in a learned generative model, which is a clean and theoretically grounded departure from gradient-based meta-learning approaches. This framing naturally enables test-time inference without parameter updates.

- **Strong empirical demonstration of compositional generalization**: The model successfully recovers ground-truth modules and transition statistics, and generalizes to test tasks that are four times longer than training tasks (Figure 2f) and to sparse feedback settings (Figure 2e, 4e). These are non-trivial generalization challenges.

- **Thorough ablation and comparison**: The paper includes well-designed control experiments (Figure 3a-d) that isolate the contributions of the gating network and modular architecture, and compares against standard meta-learning baselines (MAML, MLDG) showing qualitative differences in sample efficiency (Figure 3e-f).

## Weaknesses

### Major

- **Limited task complexity and scale**: The empirical evaluation is restricted to synthetic, low-dimensional tasks (6D vectors, simple shift operations, motor primitives with fixed durations). While the authors acknowledge this as proof-of-principle, the paper would be significantly strengthened by demonstrating the approach on more realistic or higher-dimensional problems where compositional structure is less obvious. The current tasks are essentially designed to be perfectly modular, which is a strong assumption.

- **Fixed number of modules**: The model requires the number of modules to be specified a priori and fixed throughout training and inference. The paper briefly discusses this as future work, but it is a significant limitation for practical application. The experiments with mismatched module counts (Figure A1) show some robustness, but the model cannot discover the appropriate number of modules dynamically.

- **No comparison to in-context learning approaches**: The paper claims that in-context learning (e.g., transformers) lacks modularity and probabilistic reasoning, but does not provide any empirical comparison. Given that transformer-based models can also perform compositional generalization and few-shot learning without parameter updates, a direct comparison would help contextualize the advantages of the proposed approach.

### Minor

- **Training stability concerns**: The "chicken-and-egg" problem between learning modules and gating is mentioned but not systematically analyzed. The paper does not report training failure rates or sensitivity to hyperparameters, which would be useful for practitioners.

- **Particle filter computational cost**: The paper does not discuss the computational overhead of running particle filtering during inference, nor how the number of particles K scales with task complexity. This is relevant for practical deployment.

### Trivial

- The motor learning task does not require input x_t, which is a simplification that may limit generality.

## Nice-to-Haves

- An analysis of how the number of particles K affects inference quality and computational cost would be valuable.
- A discussion of how the model could handle tasks where modules need to be composed in parallel rather than sequentially.
- Exploration of whether the gating RNN could be replaced by a more expressive model (e.g., transformer) as suggested in the discussion.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add an empirical comparison to transformer-based in-context learning on the same tasks to directly support the claim that modularity and probabilistic reasoning provide advantages.
- Include an analysis of training stability (e.g., success rate across random seeds, sensitivity to learning rate or module count) to help practitioners understand when the approach is likely to work.
- Discuss or demonstrate how the model could be extended to discover the number of modules dynamically, perhaps through a non-parametric prior or a continual learning setup.

## Score and Decision

The paper presents a clean, principled framework for compositional meta-learning with strong proof-of-principle results. The probabilistic inference approach to test-time task acquisition is novel and the empirical demonstrations are convincing within the chosen synthetic domains. However, the limited task complexity and the fixed-module assumption significantly constrain the current contribution. The paper would benefit from scaling to more realistic problems or providing a path to do so. Given the ICLR 2026 score distribution, this paper is above average in quality and novelty but falls short of the strongest contributions.

MY FINAL SCORE: 6.0score</score>
MY FINAL DECISION: Borderline Accept</decision>