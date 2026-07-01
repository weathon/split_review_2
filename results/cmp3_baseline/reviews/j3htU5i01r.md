## Summary

The paper proposes a compositional meta-learning framework that separates task solutions into reusable module RNNs (within-module dynamics) and a gating RNN (between-module dynamics). By learning a probabilistic generative model of training tasks via particle filtering and maximising marginal likelihood, the model can solve held-out test tasks through probabilistic inference without any parameter updates. The approach is demonstrated on synthetic rule-learning and motor-learning tasks, showing one-shot acquisition, robust performance under sparse feedback, and generalisation to tasks longer than those seen during training.

## Strengths

- **Novel integration of modular networks and probabilistic inference for meta-learning.** The paper clearly separates learning the grammar of module combinations (gating) from the content of modules themselves, enabling test-time reasoning through constrained hypothesis testing without weight updates.
- **Compelling demonstration of inference under sparse feedback.** The model effectively exploits the learned gating dynamics to maintain and test multiple hypotheses during periods without feedback, which is a clean and impactful illustration of the benefit of explicit probabilistic reasoning.
- **Thorough experimental evaluation.** The authors recover ground-truth modules and transitions, compare against several baselines (standard RNN, RNN with task ID, flat-transition model, MAML, MLDG), and analyse robustness to module-task mismatch and longer test tasks. The inclusion of full code and trained weights ensures reproducibility.
- **Clear and well-structured exposition.** The paper is written with clear motivation, a logical flow from problem to method to experiments, and informative figures that illustrate the core ideas.

## Weaknesses

### Fatal

None.

### Major

- **Limited task complexity and scalability.** The experiments rely on low-dimensional (6D) synthetic tasks with a small, fixed number of modules. It is not demonstrated whether the approach scales to higher-dimensional inputs, many more modules, or real-world problems where modular structure may be less explicit. The particle filter with categorical resampling (K=20 particles) may become prohibitive as the state space grows.

- **Requires a predefined number of modules.** Although the paper shows some robustness to mismatch (Figure A1), the number of modules must be set *a priori* and is not dynamically adjusted. This limits applicability in settings where the underlying number of reusable components is unknown.

- **Comparison to meta‑learning baselines (MAML, MLDG) is not fully standard.** The baselines are applied to a setting where the test task differs from training tasks in the same way as for the proposed model, but the meta‑learning methods are typically evaluated on few‑shot classification benchmarks. The paper’s point that weight‑update–based methods are slower than inference is valid, but a more standard benchmarking (e.g., on miniImageNet or Omniglot variants with a compositional structure) would strengthen the claim.

### Minor

- **Training and inference details for the baselines are somewhat underspecified.** For the “RNN with task ID” baseline, it is unclear how task identity is provided for test tasks that are distinct from training tasks. The paper mentions retraining, but the exact protocol (e.g., how many gradient steps, learning rate) is not fully described.

- **The particle‑filter training uses the Gumbel‑softmax trick for gradients.** The impact of the temperature parameter and potential gradient variance on learning stability is not discussed. A brief analysis or ablation would be helpful.

### Trivial

- The paper occasionally uses the phrase “in‑activity learning” (likely a typo for “in‑activity learning” or “in‑memory learning”) without a standard reference. This does not affect understanding.

## Nice-to-Haves

- Evaluate the model on a more complex, high‑dimensional benchmark (e.g., compositional navigation tasks or program synthesis) to better understand scalability.
- Provide an ablation on the number of particles and proposal distribution choices in the particle filter.
- Show how the model can be extended to continuously add new modules (class‑incremental learning) as suggested in the Discussion.

## Novel Insights

Beyond the paper’s own contributions, a novel insight is that learning a “grammar” of module transitions via a gating RNN transforms the meta‑learning problem into a low‑complexity hypothesis‑testing process. This allows the model to handle sparse feedback by maintaining multiple hypotheses that branch only at points allowed by the learned grammar, and to collapse them efficiently when feedback arrives. This is a principled way to achieve compositionality that goes beyond simple mixture‑of‑experts or meta‑learning with parameter updates.

## Suggestions

- Clarify the exact training and evaluation protocol for the baselines, especially the MAML/MLDG comparisons (number of inner‑loop steps, meta‑batch size, etc.).
- Add a discussion (or appendix) on the computational cost of the particle filter relative to alternative inference methods (e.g., variational inference).
- Consider testing on a more complex domain (e.g., a lightweight robotics simulator) to further substantiate the claim of practical applicability.

## Score and Decision

**Score:** 8  
**Decision:** Accept

**Rationale**: The paper presents a clean, original integration of modular networks and probabilistic inference for meta‑learning, with strong empirical support on controlled synthetic tasks. The limitations in task complexity and scalability are acknowledged and do not invalidate the core contribution. The work is clearly presented, well‑evaluated against relevant baselines, and provides a principled alternative to weight‑update–based meta‑learning. The value to the community lies in the conceptual framework and the demonstration of inference‑based compositionality, which opens promising directions for future research.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>