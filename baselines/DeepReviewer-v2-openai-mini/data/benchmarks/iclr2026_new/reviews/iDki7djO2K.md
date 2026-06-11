## Summary
# Final Review Report

## Summary

This paper proposes a general, algorithm- and task-agnostic formalism for understanding **forgetting** in learning systems. The authors define forgetting as a violation of **self-consistency** in a learner's predictive distribution over future experiences: if a learner's predictions change after updating on data that its own predictive distribution already considered likely, that change reflects information loss rather than information gain. This conceptualisation yields a quantitative measure — the **propensity to forget** $\Gamma_k(t)$ — defined as the divergence between the predictive distribution before and after $k$-step updates on learner-consistent targets (Definition 4.6).

The paper makes four contributions: (C1) a general theoretical formulation of learning as an interaction process (§3), (C2) a conceptualisation of forgetting as predictive self-consistency violation (§4.2), (C3) the operational $\Gamma_k(t)$ measure, and (C4) an empirical characterisation across classification, regression, generative modelling, continual learning, and reinforcement learning.

The strength of the work lies in its ambitious conceptual unification: reframing forgetting as a predictive property rather than a parametric or task-specific one is a genuinely useful perspective that could influence how researchers think about information retention in learning systems. The formal framework (Definitions 3.1–3.6) is technically well-structured and builds on existing agent-environment formalisms with clear adaptations.

However, the paper has significant limitations that temper its contributions. The "first generalised definition" claim requires external literature validation that is not provided. The formalism's scope boundary (§4.2) explicitly excludes target-network-based algorithms (like DQN, used in the paper's own experiments), creating a gap between theory and empirical validation. The headline empirical finding that "approximate learners benefit from non-zero forgetting" (§5.3) is based on correlational evidence without causal controls. The Conclusion overstates practical utility (algorithm design guidance) that the paper does not demonstrate. Several technical details — the divergence measure choice, estimation of $\Gamma_k(t)$, and the $q_c$ vs $q_e$ symbol inconsistency — remain underspecified.

External literature verification was not available in this run (Retrieval-Disabled Mode). Novelty and literature-comparison conclusions are therefore deferred and should be manually verified.

## Strengths
1. **Conceptual unification:** The paper's core idea — reframing forgetting as a violation of predictive self-consistency — provides a genuinely novel lens that unifies forgetting phenomena across supervised learning, generative modelling, reinforcement learning, and continual learning. This is a valuable conceptual contribution that could influence future research on information retention in learning systems.

2. **Technically rigorous formalism:** The agent-environment interaction framework (§3) is carefully constructed with well-defined measurable spaces, update functions ($u$ and $u'$), and predictive distributions. The formalism draws from established foundations (Hutter, 2005; Fong et al., 2023) and adapts them appropriately for the study of forgetting. The distinction between learning-mode and inference-mode updates is a thoughtful design choice that enables the definition of induced futures.

3. **Clear desiderata:** Section 4.1 lays out four explicit desiderata (4.1–4.4) that any valid notion of forgetting should satisfy. This provides a principled foundation for evaluating and comparing different conceptualisations, and the paper's own definition demonstrably satisfies all four.

4. **Broad empirical scope:** The experiments span classification, regression, generative modelling (MMD evaluation), class-incremental learning, and reinforcement learning (DQN on CartPole with 10 seeds, including confidence intervals). This diversity supports the claim that forgetting is not confined to any single paradigm.

5. **Honest scope boundaries:** The "Scope and boundary of validity" paragraph (§4.2) explicitly identifies cases where the formalism does not apply (buffer reinitialisation, target-network lag, algorithms without predictive mappings). This transparency is commendable and helps prevent over-claiming — though the paper does not fully carry this caution into its broader conclusions.

6. **Pedagogical value:** The paper is generally well-written with clear definitions, useful takeaways (Takeaway 1–4), and illustrative figures (especially Figure 2 showing self-consistent vs. non-self-consistent learners). The insight statement ("If a learner updates its predictions on data it already expects...") is memorable and captures the intuition effectively.

## Weaknesses
The following weaknesses are ordered by severity and impact on the paper's validity, novelty, and research value.

### W1. Gap between formalism scope and empirical validation (Severity: Major)

The formalism's scope boundary (§4.2) states that it applies only when "the learner's predictive distribution accurately represents the learner's state," explicitly excluding "target-network lag" from the validity window. However, the RL experiments (§5.4) use DQN — which relies on a target network — without acknowledging that the formalism's applicability is undefined during target-switch intervals. This creates a direct contradiction between the stated boundary condition and the experimental design. The paper either needs to extend the formalism to cover target-network architectures (e.g., by including both online and target networks in the state space) or restrict the RL claims accordingly.

**Fixability:** Fixable. Add an extension in §4.2 and a caveat in §5.4.

### W2. Correlational evidence for the "benefit of forgetting" claim (Severity: Major)

Section 5.3 claims that "a moderate amount of forgetting improves learning efficiency" and Takeaway 3 states "the trade-off between training efficiency and forgetting determines the optimal amount to forget." The evidence, however, is purely correlational: varying momentum or model size simultaneously changes both forgetting and training dynamics through multiple confounders. The paper does not manipulate forgetting independently (e.g., via replay ratio, regularisation strength, or explicit forgetting control) and does not report held-out test performance alongside training efficiency. The causal language ("utilise forgetting as a mechanism") is not supported.

**Fixability:** Fixable. Replace causal language with correlational wording. Add controlled experiments where forgetting is directly manipulated while keeping other hyperparameters fixed.

### W3. "First generalised definition" claim requires external validation (Severity: Major — Deferred)

The Conclusion asserts that this is "the first generalised definition of forgetting." Due to Retrieval-Disabled Mode, external literature verification could not be performed in this run. The paper's own literature review covers CL, RL, and related formulations, but a systematic survey of formal definitions from adjacent fields (cognitive science, information theory, predictive coding, Bayesian nonparametrics) is not provided. The novelty claim should be tempered until external validation is conducted.

**Fixability:** Deferred. Manual literature verification is required. Recommended wording: "To our knowledge, this is the first unified definition framed in terms of predictive self-consistency — a perspective that complements existing parameter- and performance-based definitions."

### W4. Symbol inconsistency and underspecified measure (Severity: Major)

Definition 4.5 (Equation 8) uses $q_c$ for the hybrid distribution, while §3.2 (Equation 3) uses $q_e$ for the same object. This inconsistency breaks traceability. Additionally, Definition 4.6 leaves the divergence $D(\cdot \mid \cdot)$ unspecified — it must be chosen by the practitioner (KL for regression/classification, MMD for generative modelling in the experiments), but the paper does not justify why different divergences are appropriate or whether results across tasks are comparable. The estimation of $\Gamma_k(t)$ from finite samples (number of Monte Carlo rollouts, bias-variance tradeoffs) is not discussed, and the sensitivity to the choice of $k$ (which ranges from 1 to 40 in experiments) is reported through shaded bands but never analysed.

**Fixability:** Fixable. Correct $q_c$ to $q_e$ in Equation (8). Add a subsection on divergence choice and estimation.

### W5. Backward transfer vs. forgetting conflation at the formalism level (Severity: Major)

The paper motivates its work by criticising CL metrics for conflating backward transfer and forgetting (§1, §2), and claims the proposed definition "disentangles forgetting from backward transfer" (Conclusion). However, $\Gamma_k(t)$ measures the total divergence between predictive distributions — which would increase both when the learner improves on past tasks (positive backward transfer) and when it degrades (negative forgetting). The measure cannot distinguish these cases without additional task-specific context. This is a conceptual limitation that should be disclosed.

**Fixability:** Fixable. Add a clarifying paragraph that $\Gamma_k(t)$ measures predictive inconsistency magnitude, not its valence, and discuss how signed variants could be defined.

### W6. Insufficient RL experiments to support "essential component" claim (Severity: Major)

Section 5.4 concludes that "forgetting is an essential component of RL" based on a single algorithm (DQN) and a single environment (CartPole). The observation that $\Gamma_k(t)$ co-occurs with TD error dynamics does not establish that forgetting is "essential" or "deliberate" — it could be an incidental byproduct. Additional RL algorithms (PPO, SAC) and environments (Atari, MuJoCo) are needed to assess the generality of the finding.

**Fixability:** Fixable. Add experiments with at least one additional algorithm and environment. Replace "essential component" wording with "co-occurs with and may facilitate" language.

### W7. Abstract over-claims generality (Severity: Minor)

The Abstract claims an "algorithm- and task-agnostic theory" but the formalism's scope boundary (§4.2) restricts applicability. This mismatch reduces the paper's credibility. Recommend qualifying the Abstract to reflect the actual scope.

**Fixability:** Easily fixable. Rephrase the Abstract claim as described in Annotation #1.

### W8. Introduction lacks a concrete research gap statement (Severity: Minor)

The Introduction's opening paragraph documents the phenomenon of forgetting but does not explicitly identify why existing conceptualisations are insufficient — a missed opportunity to establish stakes. The transition from "forgetting occurs everywhere" to "we need a general formalism" feels abrupt.

**Fixability:** Easily fixable. Add a sentence (see Annotation #2).

### W9. Bayesian example does not fully connect to predictive consistency (Severity: Minor)

Section 5.1 shows that the Bayesian posterior is self-consistent (Equation 10) but does not derive predictive self-consistency over $k$-step futures from this parameter-level consistency. The formal link between the two is asserted rather than proven.

**Fixability:** Fixable. Add a short derivation or citation (see Annotation #9).

### W10. Conclusion promises algorithm design guidance not demonstrated (Severity: Minor)

The Conclusion states that the work provides "guiding the design of algorithms that can adapt while retaining previously acquired knowledge," but no algorithm design guidance is derived from the formalism in the paper. This over-promises.

**Fixability:** Easily fixable. Replace with a more modest statement.

### Deferred Novelty & Literature Comparison

Due to Retrieval-Disabled Mode, external paper search was not available. The following novelty-related conclusions are deferred for manual verification:
- Whether the predictive-consistency definition of forgetting is genuinely novel relative to existing formal frameworks (predictive Bayesianism, general RL, information-theoretic accounts of forgetting).
- Whether related formulations exist in cognitive science, neuroscience, or psychology that also define forgetting distributionally.
- The paper's positioning relative to the strongest prior baselines for forgetting quantification.

**External literature verification status:** Not available in this run. See the runtime note at the top of this report.

## Score
**Final Score: 6/10**

**Rationale:** The score reflects the paper's strengths in conceptual unification and technical formalism weighed against the significant gaps between claims and evidence described in the Weaknesses section. The primary scoring dimensions are research value and novelty.

**Novelty (5/10):** The core idea — defining forgetting as predictive self-consistency violation — is conceptually fresh and offers a genuinely new perspective on a well-studied problem. However, the "first generalised definition" claim requires external literature validation that could not be performed in this run. The formalism builds on existing frameworks (agent-environment interfaces, predictive Bayesianism) with incremental adaptations, so the novelty lies more in the reframing than in technical invention. Deferred manual verification is needed before a higher novelty score can be assigned.

**Research Value (6/10):** The paper makes a useful conceptual contribution by providing a unified vocabulary and measure for discussing forgetting across learning paradigms. If validated, the $\Gamma_k(t)$ measure could serve as a diagnostic tool. However, the practical utility is currently limited because (a) the estimation protocol is underspecified, (b) the scope excludes important practical scenarios (target networks), and (c) the paper does not demonstrate how the formalism guides algorithm design. The trade-off finding (§5.3) is intriguing but requires causal validation.

**Validity/Soundness (6/10):** The formal framework is internally consistent and well-structured. However, the empirical sections contain significant gaps: the RL experiments do not match the formalism's boundary conditions, the efficiency-forgetting relationship is confounded, and measure specifications are incomplete. The conclusions overstate the strength of the evidence.

**Reproducibility (5/10):** Without specification of the divergence measure properties, number of Monte Carlo rollouts, sensitivity to $k$, and the $q_c$ vs $q_e$ symbol inconsistency, independent reproduction would require substantial guesswork.

**Overall:** The paper presents a thought-provoking conceptual framework that merits attention from the community, but its current empirical validation and technical specification are insufficient to support its strongest claims. The most impactful revision path would be: (1) address the scope-validation gap (W1), (2) re-run forgetting-efficiency experiments with controlled manipulation of forgetting (W2), (3) temper novelty and causality claims (W3, W5, W6), and (4) fully specify the $\Gamma_k(t)$ estimation protocol (W4).

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: No unified definition of forgetting]
    |
    v
[Proposal: Predictive self-consistency view]
    |
    +-- [Theoretical framework: §3]
    |       Formal interaction process (X_t, Y_t, Z_t)
    |       Induced futures q(H^{t+1:∞}|Z_t, H_{0:t})
    |
    +-- [Definition: §4]
    |       Consistency condition (Def 4.5)
    |       Propensity to forget Γ_k(t) (Def 4.6)
    |       Scope: fails for target-network lag, buffer reinit.
    |
    +-- [Empirical: §5]
    |       +-- 5.1: Bayesian learners (self-consistent ✓)
    |       +-- 5.2: Deep learning (Γ always > 0)
    |       +-- 5.3: Efficiency-forgetting trade-off (correlational only)
    |       +-- 5.4: RL on CartPole (DQN, scope boundary ❌)
    |
    v
[Claim: "Forgetting is everywhere" — partially supported]
    Gap: scope vs experiments mismatch (W1)
    Gap: causal claim from correlational evidence (W2)
    Gap: novelty requires external validation (W3)
```

```text
ASCII Diagram — Revision Strategy Roadmap

W1 [≈ Scope-Experiment Gap]
    -> Extend formalism to cover target-network architectures
    -> Add caveat in RL experiments
    -> Expected: internal consistency restored

W2 [≈ Causal Claim Gap]
    -> Replace "utilise forgetting as mechanism" with correlation wording
    -> Add controlled experiment (vary replay ratio, fix momentum/params)
    -> Expected: claim matches evidence level

W3 [≈ Novelty Claim]
    -> Conduct manual literature survey
    -> Replace "first generalised definition" with bounded claim
    -> Expected: defensible novelty positioning

W4 [≈ Measure Specification]
    -> Fix q_c → q_e symbol
    -> Add divergence properties and estimation details
    -> Expected: full reproducibility

W5+W6 [≈ Interpretation Overreach]
    -> Clarify Γ_k(t) measures magnitude not valence
    -> Add more RL algorithms/environments
    -> Expected: conclusions matched to evidence
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)
(Note: External literature unavailable in this run; tree structure is proposed based on manuscript content)

Forgetting Definitions (Root)
├── Branch 1: Performance-based definitions
│   ├── Leaf 1.1: CL backward-transfer metrics [Chaudhry, Kirkpatrick]
│   ├── Leaf 1.2: Accuracy-decay measures [Kemker, Jagielski]
│   └── Leaf 1.3: RL policy/value degradation [Shenfeld, Schaul]
├── Branch 2: Parameter/representation-based definitions
│   ├── Leaf 2.1: Parameter drift [McCloskey, French, Kirkpatrick (EWC)]
│   ├── Leaf 2.2: Representational shift [Kim, Rusu]
│   └── Leaf 2.3: Policy drift [Shenfeld, Ring]
├── Branch 3: Predictive/distributional definitions (This paper)
│   └── Leaf 3.1: Predictive self-consistency violation
│       - Core idea: forgetting = change in predictive distribution after
│         updating on learner-consistent targets
│       - Value contribution: unifies CL, RL, i.i.d., and generative settings
│         under a single measure
│       - Open question: relationship to predictive Bayesianism [Fortini, Fong]
│         and general RL frameworks [Hutter, Dong] needs external clarification
└── Branch 4: Mechanistic/interference accounts
    ├── Leaf 4.1: Associative memory interference [Hopfield, Amit]
    └── Leaf 4.2: Generative model collapse [Alemohammad, Shumailov]

Note: Branch 3 requires external literature verification to confirm
the novelty of the predictive-consistency framing relative to existing
predictive Bayesian formulations and information-theoretic accounts.
```

**External literature verification:** Not available in this run (Retrieval-Disabled Mode). Novelty and literature-comparison conclusions are intentionally deferred. The final score and verdict should be reconsidered after external verification is performed.