## Summary

This paper introduces a new Bayesian Optimization setting where evaluating a design yields both a scalar reward f(x) and high-dimensional auxiliary information h(x), with a history of related tasks available for meta-learning. The authors propose a transformer-based neural process model that learns to exploit h(x) for few-shot prediction of f(x) on unseen tasks, and create a new robotic gripper design benchmark (4.28M evaluations across 997 ShapeNet objects) using tactile feedback as auxiliary information. The method significantly outperforms an f-only baseline on both prediction and optimization metrics.

---

## Strengths

- **Novel and well-motivated problem setting.** The paper cleanly formalizes the gap between standard BayesOpt (scalar feedback only) and realistic experimental setups (rich side information + task history). The three-way combination—auxiliary h(x), multi-task history, and the need to *generalize* h representations to new tasks—has not been jointly addressed before.
- **Meaningful benchmark contribution.** The gripper design task is a realistic, non-trivial benchmark: 21-dimensional design space, MuJoCo simulation, high-dimensional tactile observations (two 16×16 images + scalar readings), and 4.28M evaluated designs across 997 diverse objects. This is a genuine artifact the community can build on.
- **Clear empirical gains.** Auxiliary information provides consistent MSE improvements at every context size (e.g., 171 vs. 200 at context=5), and the model with context=10 beats f-only at context=30. The parameter-matched f-only(+p) ablation rules out model capacity as a confound. Optimization gains (34.4% vs. 26.7% max-reward tasks; 67.2% vs. 58% for regret ≤ 0.5) are meaningful.
- **Clean architecture.** The transformer-based design, use of a [CLS]-token to encode time-series h(x), and the separation of context/target encoders are clearly described and sensibly motivated by prior TNP work.

---

## Weaknesses

### Fatal
None.

### Major

1. **Single-benchmark evaluation.** All empirical claims rest on one task. The practical applications mentioned (drug design, hyperparameter tuning, microrobotics) are left as motivation only. Without results on at least one additional domain—even a synthetic one—it is impossible to assess whether the gains are specific to the tactile gripper setting (e.g., because tactile images happen to be strongly predictive) or genuinely general.

2. **Absent comparison to existing composite BayesOpt methods.** The paper discusses composite BayesOpt (Astudillo & Frazier, 2019; Maus et al., 2023) as related work but never compares against it. Even if those methods are designed for single-task, adapting or naïvely applying them to the multi-task gripper setting would establish a stronger baseline and validate the claim that multi-task learning of h is essential. Without this comparison, the core claim—that the proposed method's particular approach to h is what matters—rests on a single f-only ablation.

3. **Optimization results are under-described.** Section 6.2 presents aggregate summary statistics but no learning curves or per-trial reward plots are included in the extracted text. Given that optimization efficiency is the ultimate goal, the absence of these curves makes it difficult to judge the practical speedup or the trajectory of improvement.

### Minor

1. **Ablation of h components is missing.** The auxiliary information comprises tactile images (Ti_L, Ti_R) and scalar contact readings (Tf_L, Tf_R). It is unclear which components drive the gains. This would clarify whether the benefit comes from spatial tactile patterns or simpler contact statistics, informing how to apply the method in other domains.

2. **Context construction during optimization is unexplained.** During BayesOpt, context grows as evaluations accumulate. The paper does not describe how context points are selected (e.g., random subset, most recent, highest reward), which affects both performance and runtime, and matters for practitioners replicating the method.

### Trivial

- The nearest-neighbors baseline MSE (~400) is stated without specifying the context size used, making it an incomplete comparison point.

---

## Nice-to-Haves

- A second benchmark domain (even synthetic, e.g., function optimization with side channel) would significantly strengthen the generality claim.
- Visualizations of what the model has learned to attend to in h(x) (e.g., attention maps over tactile images) would provide interpretability insight.
- Reporting wall-clock cost of a BayesOpt loop iteration would be useful for practitioners.

---

## Novel Insights

The paper's most genuine insight is the identification of auxiliary information exploitation as a *representation learning problem* that becomes tractable only in the multi-task transfer setting: a single task's data is too sparse to learn a useful encoder for high-dimensional h(x), but the task history provides enough diversity to learn a generalizable encoding. This reframes composite BayesOpt from an acquisition-function design problem to a meta-learning problem, which is a meaningful conceptual shift. The gripper tactile setting operationalizes this insight concretely, showing that dynamics-based reasoning (learning *how* a grasp fails from tactile images rather than just *whether* it fails) enables qualitatively different optimization strategies.

---

## Suggestions

- Add at least one additional benchmark or synthetic task to demonstrate generality beyond gripper design.
- Include a comparison (or at least a discussion of why comparison is infeasible) with a single-task composite BayesOpt baseline applied per test task.
- Plot optimization curves (reward vs. trial number, averaged over test tasks and seeds) to show the efficiency profile over time.
- Ablate the contribution of different h components (tactile images vs. scalar readings) to clarify what information is most useful.

---

## Score and Decision

The problem setting is novel and practically relevant, the benchmark is a real contribution, and the method shows clear empirical improvements. The main limitations are the narrow experimental scope (one benchmark) and the lack of comparison with existing composite BayesOpt methods. These are significant but not fatal—the paper's framing contribution and benchmark stand regardless. This is a borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>