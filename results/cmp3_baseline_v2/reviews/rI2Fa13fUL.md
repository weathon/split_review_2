## Summary

The paper introduces Generative Trajectory Policies (GTP), a new policy paradigm for offline RL that learns the entire solution map of a continuous-time ODE governing the generative process. The authors first present a unified ODE framework connecting diffusion models, consistency models, flow matching, and consistency trajectory models, then derive GTP by learning the full flow map \(\Phi(x_t, t, s)\). To make this practical for offline RL, they propose two key adaptations: (1) a score approximation that replaces costly ODE integration with closed-form one-step noise perturbation, and (2) an advantage-weighted objective for value-driven policy improvement. Empirical results on D4RL benchmarks show strong performance, particularly on AntMaze tasks, outperforming prior generative policy methods in most settings.

## Strengths

- **Strong empirical results**: GTP achieves the highest average scores among generative policies on both Gym (89.0) and AntMaze (80.6) domains, with particularly large margins on AntMaze where GTP-BC (66.3) dramatically outperforms D-BC (41.2) and C-BC (44.1). The perfect score on antmaze-umaze is notable.

- **Clean theoretical framing**: The unified ODE perspective connecting diffusion, flow matching, consistency models, and CTMs is presented clearly and provides a useful organizational lens. The derivation of the Inst Map and the Trajectory Consistency Loss as complementary objectives is well-structured.

- **Addresses a real practical bottleneck**: The score approximation technique (Theorem 1) directly tackles the computational infeasibility of repeated ODE solving during training. The ablation shows this saves training time (4.26h vs 5.23h) while improving performance (112.2 vs 99.7).

- **Good ablation study**: The ablation cleanly demonstrates the necessity of both proposed techniques, showing that linear Q-term baselines diverge for most hyperparameter settings while the advantage-weighted formulation is stable.

## Weaknesses

### Fatal
None.

### Major

- **Limited conceptual novelty**: The core technical components are largely adaptations of existing ideas. The unified ODE framework is well-known in the generative modeling community (the connection between diffusion models, consistency models, and flow matching via ODEs is standard textbook material). Learning the full flow map \(\Phi(x_t, t, s)\) is directly from Consistency Trajectory Models (Kim et al., 2024), which the paper acknowledges "corresponds exactly to our Trajectory Consistency Loss." The advantage-weighted objective (Theorem 2) is a restatement of standard results from AWR/CRR that dates back to the KL-regularized RL literature. The paper's contribution is thus an engineering combination of existing techniques rather than a fundamentally new paradigm.

- **Theoretical contributions are standard**: Theorem 1 shows that using the surrogate field \(\tilde{f}\) instead of \(f^*\) changes the objective by \(O(h^p)\), which is essentially a standard ODE solver convergence result under Lipschitz continuity. Theorem 2 is a direct consequence of the KL-regularized policy optimization that appears in numerous prior works (AWR, CRR, IQL). Neither result provides deep new insight.

- **Overselling of claims**: The paper claims "state-of-the-art performance" but GTP is notably worse than C-AC on several tasks (halfcheetah-m: 53.9 vs 69.1; halfcheetah-mr: 50.8 vs 58.7; halfcheetah-me: 93.8 vs D-QL's 96.8). The claim of "perfect scores on several notoriously hard AntMaze tasks" is misleading—only antmaze-umaze achieves 100.0; antmaze-md is 94.2, antmaze-lp is 53.5. The "perfect scores" claim is based on a single task.

- **Narrow evaluation scope**: Results are limited to D4RL Gym and AntMaze domains. No evaluation on more complex tasks (Adroit, Kitchen, FrankaKitchen, MetaWorld) that would better test the claimed advantages of full-trajectory learning for long-horizon behavior. The paper claims to resolve the expressiveness-efficiency trade-off but only evaluates on standard benchmarks.

- **Missing critical comparison**: The paper does not compare training or inference efficiency (wall-clock time, FLOPs) against diffusion-based and consistency-based policies. Given that the paper's central claim is about balancing expressiveness and efficiency, this is a notable omission. The only timing information is in the ablation (4.26h vs 5.23h) but no comparison to D-QL or C-AC training time.

### Minor

- The paper does not discuss why C-AC significantly outperforms GTP on halfcheetah-medium and halfcheetah-medium-replay, which are important counterexamples to the "state-of-the-art" claim.
- The parameterization \(\phi(x_t, t, s)\) in Eq. (3) appears to have a potential division by zero when \(s = t\) (since \(\frac{t}{t-s}\) diverges), which limits the times at which this parameterization can be evaluated.
- The paper uses 5 sampling steps for GTP but does not justify why this is the right number or show sensitivity to the number of steps.

### Trivial
None.

## Nice-to-Haves

- A head-to-head wall-clock efficiency comparison (training and inference) against D-QL and C-AC would substantially strengthen the "expressiveness vs efficiency" claim.
- Sensitivity analysis on the number of sampling steps \(K\) during inference would clarify the practical efficiency trade-off.
- Evaluation on a more diverse set of tasks (Adroit manipulation, Kitchen) would test generalization of the approach.

## Novel Insights

Beyond the paper's own contributions, the key observation is that the "full-trajectory" learning approach (CTM-style) can be effectively adapted to offline RL through a clever score approximation that avoids ODE integration during training. The insight that using the empirical clean sample \(x\) instead of the conditional expectation \(\mathbb{E}[x|x_t]\) as the denoising target, combined with O(h^p) correctness guarantee, provides a practical bridge between generative modeling theory and RL training efficiency. However, this synthesis, while useful, does not generate fundamentally new understanding of either generative models or offline RL.

## Suggestions

- Tone down the "state-of-the-art" and "perfect scores" claims to accurately reflect the empirical results, and discuss the tasks where GTP underperforms baselines.
- Add a wall-clock time comparison between GTP, D-QL, and C-AC for both training and inference to directly support the efficiency claim.
- Clarify the distinction between "learning the full solution map" vs learning a standard diffusion/consistency model—the paper implies a qualitative difference but the practical implementation is a different training objective applied to a similar architecture.

## Score and Decision

The paper presents a solid engineering contribution that combines CTM-style full-trajectory learning with score approximation and advantage weighting for offline RL, achieving strong empirical results on D4RL. However, the core technical novelty is limited: the unified ODE framework is expository, the trajectory learning is directly from CTM, and the value-weighted objective is standard. The theoretical results are routine convergence bounds and standard RL derivations. The paper is methodologically sound but does not rise to the level of a significant new paradigm or deep theoretical contribution expected for acceptance at a top venue.

MY FINAL SCORE: 5.5score
MY FINAL DECISION: Borderline Rejectscore