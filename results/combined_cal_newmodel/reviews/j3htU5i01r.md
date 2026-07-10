Here is my final consolidated review.

---

## Summary

This paper proposes a compositional meta-learning framework where tasks are modeled as structured combinations of reusable neural network modules. During training, a gating RNN and a set of module RNNs jointly learn a probabilistic generative model of tasks by maximizing marginal likelihood via particle filtering. At test time, new tasks are solved by performing posterior inference over module sequences, requiring no parameter updates. The model is evaluated on synthetic rule-learning and motor-learning tasks, demonstrating ground-truth recovery of modules and transitions, one-shot task inference, and robustness to sparse feedback and sequence-length extrapolation.

## Strengths

- **Principled framing of meta-learning as inference.** The paper correctly identifies that most meta-learning approaches (MAML, Reptile, etc.) still require parameter updates on test tasks, and proposes a genuinely different approach: learn a generative model of tasks during training, then treat test-task solution as posterior inference in that model. Equations 1–8 formalize this clearly: the gating RNN replaces the HMM transition matrix, the module RNNs replace the emission matrix, and marginal likelihood serves as the training objective. This is conceptually clean and well-motivated.

- **Sparse-feedback demonstration is compelling.** Figures 2e and 4e show that the model maintains multiple hypotheses during periods without feedback and collapses the posterior when feedback arrives. The posterior correctly switches from "continue current module" to "branch out" at learned module boundaries—without any signal from $x_t$ or $y_t$. This is a genuine and non-trivial consequence of the architecture and the strongest single piece of evidence that the gating RNN has learned the temporal structure.

- **Generalization to longer sequences.** The model solves test tasks up to 4× longer than any training task (Figures 2f, 3f). This is a meaningful result that gradient-based methods struggle with (as shown in Figure 3f, where the frozen-recurrent-weights baseline fails to reach the same asymptote). It directly follows from the inference-based approach and distinguishes it from parameter-update methods.

- **Ground-truth recovery is convincingly demonstrated.** Figures 2b, 2c, 4b, and 4c show that the learned modules and transition matrices correspond to the true operations/skills and their durations. The learned-vs-probe methodology (running modules in isolation with probe inputs) is appropriate for verifying what was learned. This is a real strength relative to most meta-learning papers, which cannot verify what their models have learned because the tasks lack interpretable structure.

## Weaknesses

### Fatal

None.

### Major

- **The comparison to gradient-based baselines does not normalize per-episode computational cost.** The proposed method uses particle filtering during inference, requiring K forward passes per timestep, while RNN baselines use a single forward pass per episode. The paper reports results in "episodes" without accounting for this cost difference. The gradient-based methods (MAML, MLDG, from-scratch, pre-trained) may be closer in wall-clock time than Figure 3 suggests. Additionally, the comparison conflates two differences simultaneously: gradient-based vs. inference-based *and* modular vs. monolithic. The "flat transitions" ablation partially addresses the architectural confound for training but not for the test-time comparison in Figures 3e/3f. This does not invalidate the method, but it overstates the speed advantage as presented.

- **The evaluation tasks are simple and the framing overstates what is demonstrated.** Both domains use exactly 6 ground-truth components, each with fixed deterministic durations (3/4/5 timesteps), strictly sequential transitions (no branching/looping/hierarchy), exactly one module active per timestep, and exactly three modules per task. The paper acknowledges these are "proof-of-principle" tasks (lines 194-200), which is appropriate. However, the abstract and introduction use language like "combinatorial generalisation" (line 13), "grammar that generates tasks" (line 21), and "expressivity of neural networks with the data-efficiency of probabilistic inference" (line 9) that suggests broader capability than the constrained tasks actually test. The test tasks use the same modules and transition patterns as training, just reordered; they do not test genuine compositional generalization to new module-transition structures or variable-length/context-dependent durations.

### Minor

- **The gating network's role is more modest than the framing suggests.** The "flat transitions" ablation (Figure 3c) shows that the model without the gating RNN performs well on training and dense-feedback test tasks; the gating network only matters for sparse feedback. The paper presents this ablation transparently, but the introduction and architecture description (lines 21-22, 49-51) frame the gating network as central to learning the "task grammar," whereas the evidence shows it is primarily a refinement for handling sparse feedback. The key innovation is the combination of modular RNNs with particle filter inference; the gating RNN is a helpful component for a specific setting.

- **The module count is predetermined and matches the ground truth.** The paper acknowledges this (lines 180-192) and includes a supplementary experiment with data-model mismatch (Figure A1, in the appendix). Nevertheless, the main results depend on providing the model with the correct number of modules (6 for 6 operations). In realistic settings where the number of latent components is unknown, this is a significant limitation. While the paper discusses future work along these lines, the current contribution is confined to settings where the module count is known a priori.

### Trivial

None.

## Nice-to-Haves

- Include a computational-cost-normalized comparison (wall time or FLOPs) alongside the episode-based curves in Figures 3e/f.
- Add a task variant that tests genuine compositional generalization—e.g., training on some module-transition patterns and testing on structurally different patterns (branching, self-loops) not seen during training.
- Report the particle count K and Gumbel-softmax temperature briefly in the main text for reader convenience.
- Explicitly acknowledge the single-module-per-timestep architectural assumption as a limitation.

## Removed Points

The following criticisms from the harsh reviewer were removed for the reasons noted:

- **MAML/MLDG used outside intended domain:** MAML is a general-purpose meta-learning algorithm applicable to any differentiable model; comparing on the same sequential tasks is valid. Removed as factually overstated.
- **Training procedure under-specified (Gumbel-softmax temperature, particle count, gradient through resampling):** The paper's reproducibility statement says parameters are described in the appendix (line 217), which was stripped by the parser. Following the hard rules, criticisms about missing appendix content are removed. Implementation details are standard for particle filter training.
- **"From scratch" baseline unfair:** The paper includes "pre-trained" and "retrain input" baselines that control for this concern. The critic's phrasing was a straw man.
- **Deterministic modules as weakness:** The paper clearly describes the deterministic task structure as a deliberate design choice for ground-truth verification. This is not a weakness of the method.
- **Various section-by-section editorial observations:** These are formatting/scope nitpicks without substance. Removed.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Include a compute-normalized comparison (wall-clock time or FLOPs) alongside the episode-based curves in Figures 3e/f to clarify the speed advantage.
2. Slightly narrow the abstract and introduction claims to better match the proof-of-principle nature of the evaluation—the language around "combinatorial generalisation" and "grammar" sets expectations the current tasks do not fully meet.
3. Report K (number of particles) and the Gumbel-softmax temperature schedule in the main text for reader convenience.

## Score and Decision

**Calibration summary (all anchors):**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Discovering modular solutions that generalize compositionally | H98CVcX1eh.md | 6.50 | 1+2 | Yes | Very similar: modular composition in synthetic tasks, ground-truth identification, constrained setting. That paper had stronger theory but worse writing clarity. My paper has compelling sparse-feedback results that the anchor lacks. Overall comparable. |
| Breaking Neural Network Scaling Laws with Modularity | 5Qxx5KpFms.md | 6.00 | 1+2 | Yes | Similar: modularity benefits shown on synthetic tasks, constrained assumptions. My paper is comparable in quality and scope. |
| Scalable Modular Network | pEKJl5sflp.md | 6.00 | 1 | Yes | Similar: modular networks with routing. My paper has stronger task-structure motivation but simpler tasks. |
| Gradient-based inference of abstract task representations | 7MYu2xO4pp.md | 5.25 | 1+2 | Yes | Related: task inference without parameter updates. My paper has cleaner experiments, stronger results, and better writing. |
| Permutation Invariant Learning with High-Dimensional Particle Filters | 6XodKiDS3B.md | 5.50 | 2 | Yes | Uses particle filters but for continual learning. My paper has better theory-experiment coherence. |
| Meta-Learning Neural Procedural Biases | 8khcyTc4Di.md | 4.00 | 1 | No | Less relevant meta-learning paper. |
| Multi-Task RL with Shared-Unique Features | 4JtwtT4nYC.md | 3.00 | 1 | No | Less relevant; lower quality. |
| Compositional World Models | EHmjRIA4l2.md | 3.00 | 1 | No | Less relevant. |

**Bracket determination (Round 1):** 5.5–7.0, based on the most topically similar anchors (modular composition papers at 6.0–6.5) being closest to this paper's scope and quality.

**Narrowing (Round 2):** Comparing my draft's itemized favorability against the closest anchor ("Discovering modular solutions," 6.5), my paper's weaknesses have higher (less negative) favorability ratings (-0.59, -1.21) vs. that anchor's (-3.71, -3.21, -2.86). This paper is better written than that anchor. However, that anchor had theoretical results, whereas my paper's contribution is primarily empirical on very simple tasks. The comparison positions my paper near the same tier but slightly below the 6.5 anchor. The paper is clearly stronger than the 5.25 (rejected) and 5.5 (rejected) anchors.

**Final score:** 6.0 — The paper presents a clean, principled framework with convincing results on its chosen tasks, particularly the sparse-feedback and length-extrapolation demonstrations. The weaknesses (compute-cost normalization in baseline comparisons, simple synthetic tasks relative to the framing) are real but not fatal, and the paper acknowledges its proof-of-principle scope. The contribution is solid for a conference paper, and the limitations are addressable.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>