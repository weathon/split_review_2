## Summary
This paper addresses the problem of learning a discrete POMDP from action-observation sequences without prior knowledge of the state space, transition probabilities, or observation models. The key technical contribution is a spectral method that connects Predictive State Representations (PSRs) with tensor decomposition approaches to recover explicit transition and observation likelihoods, which PSRs alone cannot provide. The method first learns a linear PSR from a Hankel matrix, then estimates the unknown similarity transform via a joint diagonalization of observation matrices aggregated across all actions with full-rank transition matrices. This allows recovery of the true POMDP parameters when each state has a unique aggregated observation distribution across full-rank actions; otherwise, the method learns transitions between observability partitions (sets of states sharing identical aggregated observation distributions). Experiments on Tiger, T-Maze, and Sense-Float-Reset show that partition-level models match PSR planning performance while enabling reward specification from learned likelihoods.

## Strengths
**1. Clear problem formulation and principled approach.** The paper identifies a genuine limitation in existing spectral methods for POMDP learning: PSRs provide prediction but no explicit likelihoods, while tensor methods require restrictive assumptions. The connection between these two families via similarity transform estimation is a well-motivated and theoretically grounded approach.

**2. Novel relaxation of tensor method assumptions.** By jointly diagonalizing observation matrices across all full-rank actions simultaneously, the method relaxes the per-action unique-observation-distribution requirement of prior tensor decomposition approaches [Azizzadenesheli et al., 2016; Guo et al., 2016]. This expands the class of learnable POMDPs to include domains where observation distributions are shared across states for individual actions.

**3. Theoretical characterization of identifiability.** Theorem 1 provides a clean characterization of what can and cannot be recovered: full POMDP parameters when each state has a unique aggregated observation distribution across full-rank actions, and partition-level transitions otherwise. This gives practitioners clear expectations about the method's output.

**4. Practical downstream benefit.** The paper demonstrates a concrete advantage of explicit likelihoods: reward specification after learning. The ability to direct agent behavior via state-based rewards (rather than observation-based rewards) is a meaningful capability that PSRs cannot offer without re-learning.

**5. Carefully designed experimental evaluation.** The experiments use standard benchmarks (Tiger, T-Maze) alongside a custom domain designed to test the partition-level recovery. The comparison against PSR and EM baselines, with 100 seeds for statistical reliability, is Methodologically sound. The reward-specification experiments clearly illustrate the advantage of having explicit state-level likelihoods.

## Weaknesses
### 1. Restrictive assumptions significantly limit applicability

**Evidence:** Section 3.3 lists three key assumptions: (i) ergodicity under uniform random exploration, (ii) full-rank Forward and Backward matrices, (iii) stationarity substitution for the initial distribution. Section 4.1.1 additionally requires at least one full-rank action. The paper's Learnable Systems discussion (Sec 4.1.1) attempts to justify these, but the justification is incomplete.

**Impact:** The ergodicity assumption rules out POMDPs with absorbing states, irreversible transitions, or hierarchical structure. The full-rank condition on Forw/Back is stated as "required to exclude POMDPs that have been shown to be computationally intractable to learn" but is not further justified — this effectively restricts the method to POMDPs where the system dynamics matrix has a specific rank profile that matches the number of states exactly. Many practical POMDPs (e.g., robot navigation with terminal states, dialog systems with end-of-turn) violate these conditions. The paper provides no guidance on how to verify these assumptions from finite data.

**Recommendation:** Add a limitations paragraph explicitly listing which classes of POMDPs are learnable and which are not. Provide practical diagnostics (e.g., checking the singular value spectrum of the empirical Hankel matrix) that practitioners can use to assess assumption violations. Consider extending the theoretical analysis to characterize robustness when assumptions are approximately satisfied rather than exactly met.

### 2. Experimental evaluation lacks realistic, non-engineered POMDPs

**Evidence:** Section 5 describes experiments on Tiger, T-Maze, and Sense-Float-Reset. While these are standard benchmarks, they are small (2-10 states) and their observability structure is well-understood. The hallway domains used for reward-specification experiments are explicitly designed to be "fully recoverable by our method."

**Impact:** The method's performance on larger or more realistic POMDPs (e.g., RockSample, PocMan, or continuous-state domains) is unknown. The paper's claim of learning "a broader class of POMDPs than existing tensor methods" is supported only on small, discrete domains where the structure is known a priori. On more complex domains, the SVD truncation threshold, the identification of full-rank actions, and the joint diagonalization may all face scalability and stability challenges that the current experiments do not address.

**Recommendation:** Include at least one benchmark where the observability partition is non-trivial but the POMDP is not custom-designed for the method (e.g., a modified version of RockSample with shared observation distributions). Report scaling behavior (runtime, sample complexity) as a function of the number of states, actions, and observations.

### 3. Notation inconsistencies and mathematical clarity issues

**Evidence:** 
- Section 2 defines $\mathcal{Z} = \{O^a : (a, o) \in \mathcal{A} \times \mathcal{O}\}$ with superscript $a$ only, but Section 3.2+ uses $O^{ao}$. This inconsistency is confusing.
- Equations (2) and (4) use $O^{a} O^{o}$ as a product of two matrices, but the intended meaning is the single diagonal matrix $O^{ao}$ representing the observation probability for a specific $(a, o)$ pair. The product $O^{a} O^{o}$ suggests two separate matrices, which is not how observation models are defined.
- In Eq. (17), the notation $M^{a-1}$ appears to mean $(M^a)^{-1}$, but this is not explicitly defined. The superscript $a-1$ could be misread as a separate index.

**Impact:** These notational issues create ambiguity for readers trying to reproduce the method. The $O^aO^o$ confusion in particular could lead to misinterpretation of the POMDP observation model as involving two separate observation matrices per action.

**Recommendation:** Unify notation: use $O^{ao}$ throughout for single diagonal observation matrices. In Eqs. (2) and (4), replace $O^{a} O^{o}$ with $O^{ao}$. Explicitly define $(M^a)^{-1}$ rather than $M^{a-1}$.

### 4. Strong but unsubstantiated claim about Transformers in Related Work

**Evidence:** Section 6 states: "Recurrent neural nets perform particularly well, unlike Transformers, which represent a fixed circuit that cannot maintain memory internally (Lu et al., 2024)." This claim is an oversimplification. Transformer architectures with causal masking (Transformer-XL, Compressive Transformers, etc.) can maintain long-term memory through recurrent mechanisms, segment-level recurrence, or compressed memory.

**Impact:** This claim is not essential to the paper's contribution but may erode reviewer confidence in the authors' depth of knowledge. It also makes an unnecessarily adversarial comparison that is likely to be challenged during review.

**Recommendation:** Remove the comparison with Transformers entirely, as it is irrelevant to the paper's spectral method contribution. Alternatively, substantially soften it: "Recurrent architectures are a natural fit for this setting and can be trained with specialized objectives [citations], whereas standard Transformers without explicit memory mechanisms have fixed context windows that may limit their ability to represent long histories."

### 5. EM baseline comparison is potentially unfair

**Evidence:** Section 5 states that the EM baseline uses "a number of states determined by the number of components of the truncated SVD when learning a linear PSR." This locks EM into a potentially suboptimal state count — if the SVD truncation is inaccurate, EM cannot compensate.

**Impact:** The finding that "EM consistently converges to a local minimum and does not obtain correct observation or transition likelihoods" may reflect the constrained state count rather than an inherent limitation of EM. A fairer comparison would allow EM to search over candidate state counts using likelihood-based selection.

**Recommendation:** Run EM with multiple candidate state counts (e.g., $k \in \{1, \dots, K_{max}\}$) and select the best model by held-out likelihood or BIC. Report whether EM with model selection still underperforms the spectral method. This would strengthen the claim that spectral methods provide a genuine advantage over EM for this task.

### 6. Novelty verification deferred (Retrieval-Disabled Mode)

Due to the runtime retrieval environment limitations (paper_search API unavailable), this review could not perform external literature verification to assess the novelty of the proposed method against related publications. The following novelty claims from the manuscript require manual verification:
- Claim C1: Connecting PSRs with tensor decomposition via similarity transform estimation.
- Claim C2: Joint diagonalization across all full-rank actions simultaneously (rather than per-action).
- Claim C3: Recovery of partition-level transition models when aggregated observation distributions are not unique.

These claims appear technically sound based on manuscript evidence, but their novelty relative to prior work (especially recent work on joint diagonalization and POMDP learning) cannot be independently assessed here. Authors should ensure that the method is clearly distinguished from existing spectral POMDP learning approaches in terms of both assumptions and recovery guarantees.

## Score
**Final Score: 6/10**

**Reasoning:**

The paper presents a technically sound and well-motivated approach that connects PSRs with tensor decomposition methods for POMDP learning. The core theoretical contribution — joint diagonalization of observation matrices across full-rank actions to estimate the similarity transform — is a meaningful extension of prior work. The experiments demonstrate that the method can recover partition-level transition and observation models that match PSR planning performance while enabling reward specification.

However, several factors limit the score:
- **Assumption strength:** The method requires ergodicity, full-rank Forward/Backward matrices, and at least one full-rank action. These restrictions significantly limit applicability to real-world POMDPs and are not thoroughly characterized.
- **Empirical scope:** The experiments are confined to small, discrete POMDPs (2-10 states), and the custom hallway domains are designed to be fully recoverable. The method's performance on larger or more realistic POMDPs is unknown.
- **Notation and clarity issues:** Inconsistent notation across sections (O^a vs O^{ao}), ambiguous matrix product notation, and an incomplete sentence in Related Work reduce readability.
- **EM baseline fairness:** The EM comparison may be biased by fixing the number of states to the SVD-derived value, which potentially understates EM's performance.
- **Novelty verification:** External literature verification was not available in this review; the novelty claims relative to prior work should be independently assessed.

The paper has clear strengths in its theoretical framing and practical motivation. With expanded experiments on more diverse benchmarks, careful notation cleanup, a fairer EM comparison, and explicit characterization of the method's limitations, the contribution could be strengthened significantly. The current version is a solid but incomplete submission that would benefit from additional validation and clarity improvements.