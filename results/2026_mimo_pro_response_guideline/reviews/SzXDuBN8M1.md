Now I have enough calibration. Let me finalize the review.

**Round 1 bracket: 6.0–7.5**
**Round 2 narrowing: 6.5–7.0**

Key comparisons:
- **Proto Successor Measure (6.75, Reject):** Very relevant (zero-shot RL, successor features) but had simplistic experiments (gridworld, fetchreach only). TD-JEPA has far more comprehensive experiments (65 tasks, 13 datasets, pixels + proprioception). TD-JEPA is clearly stronger.
- **Bridging State and History (6.75, Accept):** Self-predictive RL theory with unified framework. Broader theory but weaker experiments. TD-JEPA has comparable theoretical novelty and much stronger experiments.
- **FB-CPR / Zero-Shot Humanoid (6.50, Accept):** Directly relevant — zero-shot unsupervised RL with FB. Narrower evaluation (humanoid only) but strong application story. TD-JEPA has broader contributions.
- **Conservative World Models (4.75, Reject):** Extending FB. Incremental, clarity issues. TD-JEPA is clearly stronger.
- **Predictive auxiliary objectives (8.00, Accept):** Different focus (brain-like learning). TD-JEPA doesn't reach this level due to theory-practice gap and baseline novelty concerns.

**Final score: 7.0** — TD-JEPA is a solid paper with genuine algorithmic novelty (TD-based latent prediction), coherent theory (gradient matching), and extensive strong experiments. The Major weakness (theory-practice gap in Theorem 2) is real but carefully framed. The Minor weaknesses (baseline novelty, missing decompositions, A3 assumptions) are addressable. The paper sits above the 6.50–6.75 range of relevant accepted/rejected anchors due to its broader experimental validation and stronger overall contribution.

---

## Summary

TD-JEPA introduces a temporal-difference latent-predictive representation learning method for zero-shot unsupervised RL. The core contribution is a TD-based loss (Eq. 7/9) that trains policy-conditioned multi-step predictors approximating successor features, enabling zero-shot policy optimization for any downstream reward from offline, reward-free data. The paper provides a theoretical chain (gradient matching theorems connecting the latent-predictive loss to successor measure approximation) and extensive evaluation across 65 tasks on 13 datasets from ExoRL and OGBench.

## Strengths

- **Novel TD-based latent-predictive loss enabling multi-step, policy-conditioned, off-policy learning (Eq. 7/9, Section 3.1):** Prior latent-predictive methods were limited to one-step prediction, single-task learning, or on-policy data. TD-JEPA's loss bridges temporal-difference learning with latent prediction, targeting long-term dynamics while requiring only single-step offline transitions.

- **Coherent theoretical chain via gradient matching (Theorems 1, 3, 4):** Theorems 1 and 3 establish that gradients of TD-JEPA's latent-predictive loss match those of successor measure approximation losses — a novel analytical tool. Theorem 4 bounds policy evaluation error by the successor measure approximation loss, connecting the method to zero-shot RL guarantees. The paper notes this generalizes prior results for one-step latent-predictive representations (line 157).

- **Extensive and rigorous empirical evaluation:** 65 tasks across 13 datasets covering locomotion, navigation, and manipulation with both proprioceptive and pixel-based observations. Probability-of-improvement analysis (Figure 2) provides statistically rigorous cross-domain comparison. TD-JEPA achieves best suite-aggregated performance in DMC_RGB (628.8 vs 582.4 next best) and is competitive across all suites.

- **Well-motivated asymmetric encoder design with empirical validation (Section 3.2, Figure 3 right):** The separation of state encoder φ and task encoder ψ is motivated by a concrete argument that control-relevant state information differs from task-relevant contextual features. The ablation in Figure 3 (right) shows this design improves performance more often than not.

- **Practical demonstration of fast downstream adaptation (Figure 4):** Frozen TD-JEPA representations are often sufficient for downstream learning, enabling sample-efficient fine-tuning via TD3.

## Weaknesses

### Fatal

None.

### Major

- **Theory-practice gap in Theorem 2 (non-collapse guarantee):** Theorem 2 is proved for a "continuous-time relaxation" where optimal predictors are computed before each gradient step on representations (line 161). The practical algorithm (Algorithm 1) uses jointly updated SGD with EMA target networks and orthonormality regularization (lines 126-127), where the predictor is never at its optimum. The practical collapse prevention mechanism (orthonormality regularization with coefficient λ) is outside the theoretical framework, and no analysis connects it to the theorem. While the abstract carefully says "idealized variant," the gap between the theoretical guarantee and the practical mechanism is substantial, and no sensitivity analysis on λ is provided to empirically bridge it.

### Minor

- **Assumption A3 (symmetric transition matrices) restricts theoretical generality:** The core theorems require P^{π_z} to be symmetric for all policies (line 148), meaning dynamics must be time-reversible. The paper says this "can be relaxed" in Appendix C (line 157), but the main text does not summarize what the relaxed versions yield for the gradient matching results.

- **Baseline novelty and missing decomposition of improvement sources:** Five of eight baselines are either used in a zero-shot framework for the first time or augmented with the paper's explicit state encoder (footnote 5, line 251). While honestly disclosed, the paper does not decompose TD-JEPA's advantage into contributions from the TD-JEPA loss, policy conditioning, asymmetric encoder design, and the explicit state encoder protocol. Figure 3 partially addresses the latter two for latent-predictive methods, but direct ablation of the first two is missing.

- **Fine-tuning results use selected tasks:** Figure 4 reports results "for the task in which the gap between online and zero-shot algorithms is largest" (line 289), introducing selection bias. While Appendix D.3 reportedly contains further results, the main paper shows only the most favorable cases.

- **No sensitivity analysis on policy set size |Z|:** The number and diversity of policies sampled during training should significantly affect successor measure quality, but no analysis is provided.

### Trivial

None.

## Nice-to-Haves

- Decompose improvement sources via ablation: replace TD-JEPA's loss with one-step/policy-agnostic variants while controlling for architecture
- Provide sensitivity analysis for λ (orthonormality coefficient) and policy set size |Z|
- Briefly summarize what the relaxed versions of A1-A3 from Appendix C yield in the main text
- Show fine-tuning results across all tasks, not just the largest-gap ones, or at minimum discuss the distribution of improvements

## Removed Points
These points are flagged to be removed, treat them with caution:
- Harsh critic's concern about missing appendix proofs: The appendix is stripped from the parsed paper, not missing from the submission. The paper explicitly references Appendix C for relaxed assumptions.
- Harsh critic's concern about Theorem 4 bounding average vs worst-case performance: This is a standard theoretical formulation, correctly stated in the paper, and not a weakness.
- Strength finder's claim about the fair comparison protocol being a strength: While the unified architecture is fair, the paper itself acknowledges that explicit state encoders improve baselines (footnote 6), which complicates attributing gains to the method itself. This conflicts with the verified baseline novelty weakness.

## Novel Insights

The gradient matching argument (Theorems 1 and 3) is the most novel theoretical contribution: showing that gradients of a latent-predictive TD loss match those of a non-latent-predictive successor measure approximation loss provides a clean analytical tool that subsumes prior results for one-step latent-predictive representations. The practical demonstration that TD-based latent prediction outperforms MC-based and one-step alternatives for zero-shot RL (Figure 3 left) makes a convincing case that temporal-difference learning is the right bridge between latent-predictive representation learning and successor feature methods, particularly in the challenging pixel-based setting.

## Suggestions

- Add a sensitivity analysis for λ and |Z| to strengthen the empirical case for robustness
- Decompose improvement sources: ablate TD-JEPA loss vs policy conditioning vs asymmetric encoders
- Show fine-tuning results across more tasks beyond just the largest-gap ones
- Summarize the relaxed versions of A1-A3 from Appendix C in the main text for readers without appendix access

## Calibration Report

**All retrieved anchors:**

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| KL Divergence GFlowNets | Uj0h13lVrR | 1.00 | 1 | Irrelevant topic, clearly weaker |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.00 | 1 | Irrelevant topic |
| Lifelong Person Re-ID | 5lUdTogEL3 | 1.00 | 1 | Irrelevant topic |
| Scientific Discourse UMAP | P49gSPmrvN | 1.00 | 1 | Irrelevant topic |
| Distributed Hebbian Temporal Memory | fnO5h1CFyh | 3.00 | 1 | Relevant (successor features) but limited experiments, rejected |
| Reward as Observation | 473sH8qki8 | 2.00 | 1 | Somewhat relevant (zero-shot transfer) but weaker method |
| Decoupled RL | Q1Hr9dVfDS | 3.00 | 1 | Relevant (representation learning for RL) but weaker |
| Foundation Policies with Memory | It4KL6XnPq | 3.00 | 1 | Relevant (unsupervised RL benchmarks) but weaker method |
| π2vec | o5Bqa4o5Mi | 5.25 | 1 | Relevant (successor features) but narrower scope, accepted |
| Conservative World Models | X5qi6fnnw7 | 4.75 | 1 | Very relevant (FB zero-shot RL) but incremental, rejected |
| Structured Predictive Representations | sEv6vHIUnu | 4.80 | 1 | Relevant but weaker evaluation |
| Combinatorial Generalization | PH7ja3T0vN | 4.50 | 1 | Somewhat relevant, rejected |
| Proto Successor Measure | s9SVlWOcLt | 6.75 | 1+2 | Very relevant (zero-shot RL, successor features) but simplistic experiments, rejected |
| Distributional Successor Measure | OMwD6pGYB4 | 5.75 | 1 | Relevant (successor measure theory) but different focus |
| Bridging State and History | ms0VgzSGF2 | 6.75 | 1+2+3 | Very relevant (self-predictive RL theory) broader theory but weaker experiments, accepted |
| DHTM (accept version) | wYJII5BRYU | 5.75 | 1 | Relevant but different focus |
| Predictive Auxiliary Objectives | agPpmEgf8C | 8.00 | 1 | Relevant (predictive objectives in RL) but different focus (brain-like learning), accepted |
| Interpreting Planning | DzGe40glxs | 8.00 | 1 | Different focus (interpretability), accepted |
| DeepLTL | 9pW2J49flQ | 8.00 | 1 | Different focus (temporal logic), accepted |
| Identifying Representations | 3cuJwmPxXj | 8.00 | 1 | Different focus (causal representation), accepted |
| FB-CPR / Zero-Shot Humanoid | 9sOR0nYLtz | 6.50 | 2 | Very relevant (zero-shot unsupervised RL, FB) narrower evaluation, accepted |
| Reasoning with Latent Diffusion | tGQirjzddO | 6.33 | 2 | Relevant (offline RL) but different method |
| Locality Sensitive Sparse Encoding | i8PjQT3Uig | 6.67 | 2 | Somewhat relevant (world models) but different focus |
| Episodic Novelty Through Temporal Distance | I7DeajDEx7 | 6.75 | 2 | Less relevant (exploration) |
| Generalized TD for Supervised Learning | dxI1HLatWw | 6.25 | 2 | Somewhat relevant (TD learning) but different setting |
| Transformers Learn TD | Pj06mxCXPl | 6.67 | 2 | Somewhat relevant (TD in transformers) but different focus |

**Round 1 bracket: 6.0–7.5.** TD-JEPA is clearly stronger than Conservative World Models (4.75) and π2vec (5.25), comparable to FB-CPR (6.50) and Bridging State and History (6.75), and well below the 8.0 anchors.

**Round 2 narrowing: 6.5–7.0.** TD-JEPA has stronger experiments than Bridging State and History (6.75) and a more novel method than FB-CPR (6.50), while the theory-practice gap in Theorem 2 and baseline novelty concerns prevent it from scoring higher.

**Final score: 7.0.** TD-JEPA's combination of genuine algorithmic novelty, coherent theoretical framework, and extensive empirical validation across 65 tasks places it above the 6.50–6.75 accepted anchors, while the Major weakness (theory-practice gap) keeps it below the 8.0 tier.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>