## Summary

This paper argues that neural policy ensembles are sub-optimal compared to linear policy ensembles, both theoretically and empirically. It presents three theorems: (1) for stabilizable linear systems, neural ensembles underperform linear ensembles under conditions of sufficient diversity, nonlinearity, and problem complexity; (2) neural ensembles with time-varying weights can lose stability even when individual policies are stable; (3) convex (linear) mixing is optimal for a weighted-average cost, implying non-convex neural mixing is sub-optimal. Experiments compare neural ensembles against LQR controllers on linear dynamical systems and two nonlinear benchmarks.

## Strengths

- **The conceptual observation that temporal coupling breaks the variance-reduction logic of ensemble classifiers** (Section 1, paragraph 3) is a genuine and well-articulated insight. The contrast between ensemble classifiers (where independent errors cancel through averaging) and ensemble policies (where actions affect future states, creating feedback loops that may amplify errors) is the paper's strongest intellectual contribution.

- **Theorem 1 provides a formal connection between policy nonlinearity (κ₀), ensemble diversity (δ), and provable sub-optimality gaps** in linear-quadratic settings. This is a nontrivial mathematical result within its stated scope — showing that when the product L_fκ₀δ exceeds the discount rate ρ, a gap emerges between the neural and linear ensemble value functions.

- **Theorem 3 correctly identifies that for a weighted-average cost J_λ = Σλ_iJ_i, the optimal convex mixing weights are λ**, providing a concrete benchmark against which neural (non-convex) mixing can be measured and quantified via the penalty term 𝔼[x₀ᵀ(K_w−K_λ)ᵀR_λ(K_w−K_λ)x₀].

## Weaknesses

### Fatal

None.

### Major

- **Claims significantly exceed what the theorems establish.** The title ("Neural Policy Ensembles are Sub-Optimal") and abstract ("formally prove") assert categorical, domain-general sub-optimality, but each theorem has critical scope limitations that the paper does not acknowledge:

  * **Theorem 1** applies only to stabilizable *linear* systems under the specific inequality L_fκ₀δ > ρ. It is an existence claim about a narrow setting, not a general proof. The contribution list states the theorem proves sub-optimality "compared to individual policies" (Section 1.1), but the theorem actually compares Π^N (neural ensemble) to Π^L (linear ensemble), not to individual policies.

  * **Theorem 2**'s instability condition depends entirely on the rate of weight change (‖ẇ‖ ≥ β). This is a well-known phenomenon in switching control (dwell-time conditions) and applies identically to *any* ensemble with time-varying weights — linear or neural. The paper nevertheless frames it as a "Stability Violation in Neural Ensembles" and claims "a linear policy ensemble composed of stable linear policies guarantees stability" (Section 1.1), which is false when weights vary temporally. The theorem does not isolate any mechanism specific to neural computation.

  * **Theorem 3** proves that convex mixing weights matching the cost weights are optimal for J_λ. But a neural network with a softmax output layer implements convex mixing, so the theorem does not establish that neural architectures are *inherently* sub-optimal for mixing — it establishes that *non-convex* mixing (which neural networks *can* but need not perform) incurs a penalty.

- **Central experimental confound: provably optimal LQR vs. potentially suboptimally-trained neural networks.** The LQR policies solve the Riccati equation and are provably optimal for their LQR problems. The neural policies are "trained using gradient descent to minimize the cumulative cost over episodes" (Section 4.3) with no convergence guarantees, no learning curves, no report of architecture (layers, width, activation function actually used), and no evidence that individual neural policies achieve near-optimal costs on their respective regimes. A paper claiming *fundamental* sub-optimality must rule out the trivial explanation that the neural networks were undertrained or underparameterized. The observed cost gap (Mean Episode Cost: LQR Ensemble 234.06, Neural Ensemble 432.21, Figure 1) could be entirely explained by poor optimization. The same confound affects the stability experiments (Section 5).

- **Empirical scope does not support the claimed domain of relevance.** The abstract claims implications for "all neural policy ensemble research, from those based on Reinforcement Learning to Mixture-of-Expert agentic-AI policies." The experiments cover only: (a) linear dynamical systems with LQR (where linear controllers are provably optimal by construction), and (b) two simple nonlinear benchmarks (Pendulum, CartPole/van der Pol) compared against "Linearized LQR" — a questionable baseline for nonlinear systems. There are **no** experiments on standard RL benchmarks (MuJoCo, Atari, DM Control, Procgen), no MoE architectures, no LLM/agentic-AI systems, and no tasks where neural nonlinearity could be an advantage rather than a liability.

- **"2 orders of magnitude" claim is unsupported by the data.** The abstract states neural ensembles underperform "often by 2 orders of magnitude" (~100×). The largest reported gap is 647% (~6.5×) for Pendulum and 267% (~2.7×) for CartPole (Figure 4). The linear-system experiments (Figure 1) show roughly a 1.85× gap. None of the reported results approach 100×.

### Minor

- **Statistical reporting is incomplete.** Section 4.4 reports "p < 10^{-5}" without specifying the statistical test, number of independent trials beyond "5 seeds," or whether the test accounts for multiple comparisons. Standard deviations and confidence intervals are absent from all reported cost values.

- **Diversity experiments show a trend that partially contradicts the paper's narrative.** Figure 3 shows the neural ensemble's cost *decreasing* as diversity increases, with the gap narrowing toward the linear ensemble. The paper dismisses this ("no value of δ for which a gap less than around 200 exists"), but the monotonic downward trend points toward potential parity at higher diversity rather than fundamental sub-optimality.

- **Section 6 figure descriptions are internally inconsistent.** Subplot (b) ("Measured Convexity Violations") reports a significant positive violation (~1000) for Neural Non-Convex Mixing on Soft_Pendulum, while subplot (d) ("Convexity Violation") reports near-zero violations for all methods on the same system. If these measure different quantities, this is not explained. Additionally, subplot (a) shows Neural Non-Convex Mixing achieving a higher Mean Episode Count (~1500) than Linear Convex Mixing (~500) on Soft_Pendulum — which, if higher episode count is better, undermines the paper's thesis that neural mixing is uniformly sub-optimal.

- **No experiments with RL-trained policies.** Despite claiming relevance to "all neural policy ensemble research" in RL, the neural policies are trained via gradient descent on cumulative cost, not through any standard RL algorithm (PPO, SAC, DQN, etc.). The experiments therefore do not validate the claimed relevance to RL ensemble methods.

- **Section 8 introduces concepts not developed in the paper.** "Trajectory manifold mismatch" and "diversity in the linear subspace" are presented as "key insight[s]" but were neither theoretically derived nor empirically tested — they are post-hoc speculation in the conclusion.

### Trivial

- The figure caption and text in Section 5 refer to "vadDerPol" (likely a typo for "van der Pol").

## Nice-to-Haves

- Training curves showing convergence of the neural networks, along with evidence that a *single* neural policy achieves near-LQR cost on its regime, would substantially strengthen the claim that the ensemble gap is fundamental rather than an optimization artifact.
- Comparing neural ensembles against *linear* ensembles trained with the *same* gradient-based optimizer (rather than only against Riccati-derived LQR solutions) would control for optimization quality and isolate the effect of policy nonlinearity.
- Error bars / confidence intervals on all reported cost values, and a clear specification of the statistical test used to obtain p-values.
- Scoping the paper's claims to match the evidence (e.g., "in linear(-izable) settings") would make the paper more defensible.

## Removed Points

- **"Theorem 3 is a tautology"** — removed because it is factually incorrect. The theorem requires proof and is a meaningful mathematical claim, not a definitional identity. The underlying concern (that the theorem does not prove neural architectures are inherently sub-optimal for mixing, since a softmax output layer implements convex mixing) is preserved in the Major weaknesses.
- **"No hyperparameter sensitivity analysis" / "no architecture ablation"** — these are subsumed by the training confound point in Major weaknesses.
- **"Theorem 1 ambiguity about neural-LQR relationship" (Section 3.1)** — subsumed under the overclaiming point in Major weaknesses.

## Novel Insights

The reviews surface a subtle problem that the paper's framing obscures: the central question is not whether neural policy ensembles are *absolutely* sub-optimal, but whether *nonlinearity per se* causes degradation beyond what any suboptimally-trained policy would suffer. The experiments cannot answer this because they compare against a provably optimal linear baseline rather than against a fairly-trained neural baseline. A genuinely informative experiment would train both linear and neural policies with the same optimizer and capacity, then compare ensemble performance — isolating the effect of policy nonlinearity from the effect of training quality. The paper confounds these two factors, and none of the theorems resolve the confound since they assume the neural policies' nonlinearity conditions are met rather than verifying them empirically.

## Suggestions

1. **Reframe claims to match the theorems.** The title and abstract should acknowledge that the results are established for stabilizable linear systems under specific conditions (Theorem 1), and that Theorem 2's instability mechanism is about time-varying weights, not neural computation specifically. Remove or drastically moderate claims about RL, MoE, and agentic AI.
2. **Address the training confound** by: (a) showing learning curves with convergence verification, (b) verifying that a single neural policy achieves near-LQR optimal cost on its regime, (c) comparing against *linear policies trained via gradient descent* (not Riccati) as a control for optimization quality.
3. **Add error bars / confidence intervals** to all cost values and specify the statistical test used.
4. **Clarify Theorem 2's relationship to switching control theory** — acknowledge that the same instability would arise for linear ensembles with time-varying weights, and explain what (if anything) makes the neural case specifically different.
5. **Resolve the Section 6 figure inconsistencies** (subplots b vs. d) and discuss the Soft_Pendulum result where neural mixing outperforms linear mixing on Mean Episode Count.

## Score and Decision

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>