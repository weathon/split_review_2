## Summary

This paper proposes a general, algorithm-agnostic definition of forgetting based on predictive self-consistency. Rather than measuring forgetting through accuracy degradation or parameter drift, the authors define it as a violation of consistency in the learner's predictive distribution when updating on self-generated targets. The formalism yields a measure Γ (propensity to forget) and is validated through experiments spanning regression, classification, generative modeling, continual learning, and RL at small scale.

## Strengths

- **Principled definition that genuinely generalizes prior notions of forgetting.** Defining forgetting through self-consistency of the predictive distribution (Definition 4.5) cleanly separates forgetting from backward transfer, parameter drift, and task-performance decay — a genuine advance over the CL literature's accuracy-based proxies that conflate these distinct phenomena. The formalism's ability to classify exact Bayesian inference as unforgetful (Section 5.1, Equation 10) is a strong sanity check: the definition correctly identifies what should be the ideal case.

- **Well-motivated desiderata (§4.1).** Desiderata 4.2 (not conflating forgetting with belief changes) and 4.4 (forgetting as a property of the learner, not the environment) correctly identify weaknesses in existing metrics like backward transfer. These desiderata provide a useful benchmark that any future definition of forgetting should be held to.

- **The separation of learning-mode (u) and inference-mode (u') updates (§3.1–3.2) is a clean modeling choice.** It captures the distinction between "learning from new observations" and "simulating an internal rollout," which is essential for the predictive-consistency definition.

- **Strong theoretical anchor: exact Bayesian inference satisfies the consistency condition (§5.1).** Showing that the Bayesian posterior is permutation-invariant under exchangeability and satisfies the consistency condition is a convincing validation. The contrast with approximate learners (diagonal posterior, point estimate) illustrates why practical algorithms forget and why parameter drift does not equal forgetting.

## Weaknesses

### Fatal
None.

### Major

- **The claim of a forgetting-efficiency trade-off (§5.3) rests on thin evidence.** Training efficiency is defined as the inverse of normalized area under the training loss curve — a proxy the paper itself acknowledges — and the relationship is shown on only a single regression task with two hyperparameter sweeps (momentum, number of parameters). No held-out performance metric is reported, the causal direction is correlational rather than established, and the "optimal forgetting level" is task-dependent (it peaks at momentum 0.9 and 20 parameters for this particular task). A single regression experiment does not support the framing as a "fundamental trade-off" (Takeaway 3, line 279).

- **No empirical comparison to existing forgetting measures.** The paper's central motivation is that existing CL metrics (backward transfer, accuracy degradation) conflate forgetting with other phenomena. Yet the experiments never show Γ behaving differently from these metrics in a controlled setting where the theory predicts divergence. Adding even one comparison — e.g., showing that Γ registers non-zero forgetting in an i.i.d. setting where backward transfer is zero — would directly validate the paper's central critique.

- **The empirical scope is limited relative to the paper's framing.** The abstract describes the experiments as "comprehensive" and claims to show forgetting "plays a significant role in determining learning efficiency." In reality, the experiments use only shallow/single-layer networks on synthetic data (regression, classification, generative), one CL setup (two-moons, single-layer network), and one RL environment (CartPole with DQN). The experiments validate that Γ registers non-zero values in small models on simple problems, which is consistent with the theory, but this does not constitute the "comprehensive" characterization the framing suggests. The mismatch between claim strength and evidence damages the paper's credibility.

### Minor

- **The Γ measure requires access to quantities unknown in practice, limiting it to a conceptual tool.** Computing Γ requires rolling out the predictive distribution k steps into the future using the hybrid distribution q_e, which borrows environment components (input distributions in supervised learning, transition dynamics in RL) that are generally unknown. The paper acknowledges this implicitly but does not discuss how approximations could scale or whether the measure is reliable for realistically-sized models. This is fine for a theoretical contribution but should be explicitly stated as a limitation.

- **The RL experiment's compatibility with the formalism's own validity conditions is not fully explained.** The paper notes (line 227) that forgetting is "undefined" during transitory phases where the predictive distribution does not represent the state (e.g., target-network lag). The DQN experiment uses a target network, but how this is handled when computing Γ is not explained. (The paper does explicitly include replay buffers as part of the learner state Z_t, line 103, so the replay buffer itself does not create a decoupling — the reviewer's concern on this specific point is addressed by the paper.)

- **The forgetting-efficiency trade-off in Figure 4 does not report variance or error bars.** While the RL experiment (Figure 5) shows confidence intervals across 10 seeds, Figure 4 shows only point estimates for the regression task, making it difficult to assess the robustness of the claimed "elbow" relationship.

### Trivial
None.

## Nice-to-Haves

- A comparison between Γ and backward transfer (BWT) on a simple CL task where the metrics should disagree would substantially strengthen the paper's validation of its central critique.
- A discussion of how Γ could be approximated for larger-scale models (e.g., neural likelihood approximations, lower-dimensional projections of the predictive distribution) would improve practical relevance.
- The formalism in §3 could be compressed without losing the core insight, improving accessibility for readers.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"The RL experiment uses a DQN with a replay buffer which creates decoupling, making Γ meaningless."** — The paper explicitly includes replay buffers as part of the learner state Z_t (line 103: "including predictive parameters and auxiliary components, such as replay buffers") that evolve under u. The "scope and boundary" paragraph clarifies that only *transitory phases* like buffer reinitialisation cause decoupling, not the presence of a buffer per se. The target-network concern remains as a Minor weakness above.

- **"No discussion of the computational cost of computing Γ" and "No discussion of how Γ is estimated in practice."** — These are implementation details that would belong in the appendix, which is stripped by the parser. Per instructions, missing appendix content is not penalized.

- **"The 'first generalised definition' claim is difficult to verify."** — The priority claim is not central to the paper's contribution and does not affect its validity.

- **Formatting/style nitpicks and grammar/typo complaints.** — Parser artifacts, not author errors.

- **"The related work criticism of Chaudhry et al. conflates BWT with the broader CL literature."** — The paper accurately characterizes accuracy-centric views; the fact that Chaudhry et al. distinguished BWT from FWT does not invalidate the criticism that these metrics conflate forgetting with backward transfer.

- **"The RL experiment is on a single environment, not demonstrating generality."** — Demanding multi-environment RL validation is scope creep for a primarily theoretical paper. The single environment is acknowledged as a limitation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the empirical sections as targeted validations of the theory** rather than a "comprehensive empirical characterization." This would eliminate the mismatch between claim strength and evidence. The experiments serve to illustrate that the formalism behaves as expected, not to establish a "fundamental trade-off."

2. **Add a controlled comparison between Γ and backward transfer** on a simple CL problem (e.g., two-moons) where the theory predicts they diverge. This is the single experiment that would most directly validate the paper's central motivation.

3. **Report error bars on the forgetting-efficiency relationship** (Figure 4) and ideally validate the efficiency proxy against held-out performance.

4. **Explicitly acknowledge the practical limitations** of computing Γ for large-scale models, positioning it as a conceptual tool rather than a deployable diagnostic.

---

**Calibration.** All anchor papers used:

| Anchor | Avg Score | Decision | Round | Comparison |
|--------|-----------|----------|-------|------------|
| Replay can provably increase forgetting (kf9phcBvQ5) | 3.0 | Reject | R1 | More restrictive theory (linear models), similar experiment scale. Our paper is more general and cleaner. |
| Towards Understanding Memory buffer CL (vNGv3dJATp) | 3.75 | Reject | R1 | Theoretical analysis in linear models with no real-data experiments. Our paper has cleaner theory. |
| Replay concurrently or sequentially? (nSYycd5tEC) | 4.0 | Reject | R1 | Theory + DNN experiments but linear-model analysis. Comparable balance. |
| Why Fine-Tuning Struggles with Forgetting (CGfWyU28Pd) | 4.5 | Reject | R2 | Theory in linear regression for unlearning. |
| A Unified Framework for CL (BE5aK0ETbp) | 5.25 | Accept | R1 | Framework paper with standard benchmark experiments. Stronger empirically, less novel theory. |
| Spurious Forgetting in CL of LMs (ScI7IlKGdI) | 6.33 | Accept | R2 | Novel conceptual claim + LLM experiments. Stronger empirically, comparable conceptual depth. |
| Dual Process Learning (jDsmB4o5S0) | 6.0 | Accept | R2 | Conceptual contribution about weight forgetting. |

**Round-1 bracket:** 4.0 – 6.5. The paper's theoretical contribution is more general and clean than papers scoring 3–4 (which are CL-specific, linear-model theory). It is weaker empirically than papers scoring 5.5+ (which have standard benchmark experiments). Within the bracket, the paper sits near 5.5: the theory is the strongest part and is a genuine contribution, but the empirical overclaiming and thin evidence prevent it from reaching the 6+ level of the anchors in that range.

---

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>