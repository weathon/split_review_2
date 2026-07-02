## Summary
This paper addresses the problem of reward model extrapolation errors in offline preference-based reinforcement learning (PbRL). The authors propose SPOT (Subgoal-based Preference Optimization Through Attention Weight), a framework that identifies critical states (subgoals) from preference transformer attention weights, learns their distribution via a Conditional Variational Autoencoder (CVAE), and uses cosine-similarity reward shaping to regularize policy learning toward these preference-aligned subgoals. The core hypothesis is that anchoring policy optimization to subgoals derived from preferred trajectories constrains learning within the training distribution, thereby reducing extrapolation errors.

The paper evaluates SPOT on 10 tasks across D4RL locomotion, Robosuite manipulation, and Meta-World benchmarks, comparing against 7 baselines including Preference Transformer (PT), Inverse Preference Learning (IPL), and DTR. The main results show that SPOT achieves the highest average score (78.82) with lower variance (avg. std 7.76) compared to the best baseline PT (74.76, std 13.80). Ablations confirm the importance of top-10% attention filtering and cosine-similarity shaping with positive weighting. Query efficiency experiments show SPOT maintains competitive performance with fewer preference queries.

**Novelty assessment (deferred — manual literature verification required):** Due to external paper search being unavailable in this run, novelty claims (attention-guided subgoal discovery in offline PbRL, CVAE-based subgoal generation for reward shaping) cannot be verified against prior work. Authors should verify that SPOT's approach is distinct from existing subgoal-based RL methods (e.g., goal-conditioned RL, option discovery, hierarchical RL) and from preference-based methods that use attention mechanisms.

## Strengths
1. **Well-motivated problem formulation.** The paper addresses a genuine and practically important challenge in offline PbRL: the compounding of reward model extrapolation error with standard offline RL distributional shift. The motivation is clearly articulated, and the proposed direction of using attention-derived subgoals as structural priors is intuitively appealing.

2. **Clean, modular framework design.** SPOT decomposes into three clear stages — attention-based subgoal identification, CVAE-based subgoal generation, and cosine-similarity reward shaping — each with a well-defined purpose. The dual-criteria filtering (attention + reward threshold) is a thoughtful design choice that addresses the risk of selecting spuriously high-attention but low-quality states.

3. **Comprehensive empirical evaluation.** The paper evaluates on 10 tasks across three distinct benchmark families (D4RL locomotion, Robosuite manipulation, Meta-World manipulation), covering both locomotion and manipulation domains with varying data quality (medium, replay, expert, proficient-human, multi-human). The baseline set is broad (7 methods), and the 5-seed reporting with standard deviations provides reasonable statistical grounding.

4. **Informative ablation studies.** Section 5.2 provides useful insight into design decisions: the Top-K% analysis (Table 2) clearly demonstrates that higher-attention states yield better subgoals, and the reward shaping comparison (Table 3) systematically evaluates three methods across 6 λ values, providing practical guidance for method deployment.

5. **Query efficiency analysis.** The experiment in Table 4 showing SPOT's robustness to reduced preference queries is a practically relevant finding, suggesting the subgoal guidance does provide a regularization effect that partially compensates for sparse preference supervision.

## Weaknesses
### Major Weaknesses

**W1. Temporal inconsistency between subgoal definition and reward computation (validity-critical).**
The subgoal selection in Section 4.1.3 defines subgoal triplets $(s_t, a_t, g_t)$ where "$s_t$ and $a_t$ is a corresponding state-action pairs between $g_{t-1}$ and $g_t$." This means $g_t$ is a *distant milestone* state — a critical decision point in the trajectory — *not* the immediate successor of $(s_t, a_t)$. However, the reward shaping in Section 4.2.1 computes $r_{\text{shape}}(s'_t, \hat{g}_t)$ as the cosine similarity between the *next state* $s'_t$ and the predicted subgoal $\hat{g}_t$. If $\hat{g}_t$ represents a distant milestone and $s'_t$ is the immediate next state, they may be temporally misaligned, and the cosine similarity may not meaningfully measure progress toward the subgoal. The paper does not address this temporal gap or its impact on the shaping signal's validity. 
**Impact:** This raises questions about whether the reward shaping signal actually measures what it claims to measure, potentially undermining the core mechanism of extrapolation error mitigation. 
**Fix:** Clarify the temporal relationship (is $\hat{g}_t$ a next-state prediction or a distant milestone?) and adjust the comparison target accordingly, or provide empirical evidence that the temporal gap does not harm performance (e.g., by comparing with an oracle that uses the correct temporally-aligned subgoal).

**W2. Negative-valued cosine similarity loss (Eq. 8) with missing justification (methodological defect).**
The loss function $\mathcal{L}_{\text{sim}}$ in Equation (8) is defined as:
$$\mathcal{L}_{\text{sim}} = -\frac{1}{2}\left(1 + \frac{\hat{g}_t \cdot g_t}{\|\hat{g}_t\| \|g_t\|}\right)$$
Since cosine similarity ranges in $[-1, 1]$, $\mathcal{L}_{\text{sim}}$ ranges in $[-1, 0]$, making it a *negative* loss. When added to the positive $\mathcal{L}_{\text{CVAE}}$ to form $\mathcal{L}_{\text{total}}$, this negative term effectively *rewards* the model for high similarity rather than penalizing dissimilarity. This is atypical — standard practice uses $1 - \cos(\hat{g}_t, g_t)$ (range $[0, 2]$) or $\|\hat{g}_t - g_t\|^2$ to minimize reconstruction error. The negative formulation could cause the total loss to become negative, and the model might exploit this by driving similarity arbitrarily high at the expense of reconstruction fidelity. The authors do not discuss this design choice or its implications. 
**Impact:** If the loss formulation is incorrect, the CVAE training may not converge to a meaningful subgoal generation function, potentially explaining why the method works well in some tasks but poorly in others. 
**Fix:** Replace with $\mathcal{L}_{\text{sim}} = 1 - \cos(\hat{g}_t, g_t)$, or provide explicit justification and ablation of the current negative formulation.

**W3. Circular dependence in subgoal filtering (design vulnerability).**
The dual-criteria filtering (Eq. 5-6) uses the learned reward model's estimates $\hat{r}_t$ as one of two criteria for selecting subgoals. However, the entire motivation for SPOT is that this reward model is *unreliable* due to extrapolation errors. Using its outputs to select training targets for the CVAE creates a circular dependency: if the reward model overestimates certain states (a known extrapolation failure mode), those states may be preferentially selected as subgoals, reinforcing the error. The paper acknowledges this risk for marginally preferred trajectories but does not provide a mitigation strategy. Additionally, when no states satisfy both criteria (empty $\mathcal{S}_g$), the behavior is undefined.
**Impact:** The subgoal quality may be degraded exactly when the reward model is most unreliable — in OOD regions — which is when the method most needs good subgoals. 
**Fix:** (a) Discuss the circular dependence explicitly; (b) investigate using a separate filtering mechanism not dependent on the learned reward (e.g., attention-only, or ensemble disagreement); (c) specify fallback behavior for empty $\mathcal{S}_g$.

**W4. Selective result interpretation and missing statistical testing (evidence-sufficiency gap).**
Section 5.1 claims "consistent superiority of our approach across multiple benchmarks." However, Table 1 shows that SPOT underperforms the best baseline by significant margins on lift-mh (65.17 vs MR's 95.62, a 31-point gap) and drawer-open (66.80 vs IPL's 87.64, a 21-point gap). The narrative selectively highlights favorable results (hopper, walker2d, plate-slide) while downplaying these failures as "modest but meaningful improvements" or "falling short of absolute peak performance." Moreover, the paper does not report any statistical significance test (e.g., paired bootstrap across tasks, per-task Wilcoxon signed-rank) to establish that SPOT's 4.06-point average lead over PT (78.82 vs 74.76) is statistically significant given the small sample of 10 tasks and high variance.
**Impact:** Without balanced reporting and significance testing, the strength of SPOT's empirical advantage is unclear, and the conclusions may be overclaimed. 
**Fix:** (a) Add a balanced discussion that honestly reports cases where SPOT underperforms; (b) perform paired statistical tests (bootstrap, signed-rank) across the full task set; (c) report per-task effect sizes and practical significance.

**W5. Non-potential-based shaping alters optimal policy without analysis (theoretical gap).**
Section 5.2.2 correctly notes that potential-based shaping guarantees policy invariance only with ground-truth rewards, and that this cannot be ensured with predicted rewards. However, the chosen cosine similarity shaping is *not even potential-based* — it cannot be expressed as $\Phi(s'_t) - \Phi(s_t)$ for a fixed potential function because the subgoal $\hat{g}_t$ depends on $(s_t, a_t)$. This means the shaping term explicitly changes the optimal policy. The paper claims the formulation "preserves the original task objectives" (Section 4.2.2) but provides no analysis of how the optimal policy under $r_{\text{final}}$ differs from the preference-optimizing policy under $r_{\text{model}}$.
**Impact:** The method may converge to a policy that optimizes a distorted objective, and the claimed "extrapolation error mitigation" may actually be a form of policy regularization that trades off task optimality for conservatism. Without analyzing this trade-off, the paper's central claim is incompletely supported.
**Fix:** (a) Discuss the non-potential nature explicitly; (b) analyze the fixed point of the shaped objective; (c) provide empirical evidence (e.g., correlation between shaped objective and true return) that the distortion is not harmful.

### Minor Weaknesses

**W6. Grammar and presentation errors.** "we demonstrates" (line 71-72) is a subject-verb agreement error. "This approaches are trained" (line 70) should be "These approaches are trained." The phrase "both criterias" (line 85) should be "both criteria." These errors, while individually minor, collectively reduce the professional polish of the manuscript.

**W7. Missing reprodicibility details.** The paper does not provide: (a) the Preference Transformer architecture hyperparameters (number of layers, heads, embedding dimension) used in experiments; (b) the CVAE architecture (encoder/decoder layer sizes, latent dimension); (c) training hyperparameters (learning rate, batch size, optimizer) for each component; (d) computational budget (GPU hours per experiment). These are essential for reproducibility.

**W8. Single-environment extrapolation error analysis.** Section 5.3 and Figure 2 only show extrapolation error on one environment (likely hopper). The claim that "SPOT consistently outperforms PT" in extrapolation error reduction should be demonstrated across multiple environments with varying characteristics (e.g., locomotion vs. manipulation, dense vs. sparse reward).

**W9. Overclaim on practical applicability.** The conclusion claims SPOT advances "practical applicability" of offline PbRL, but no real-world deployment, robustness to noisy preferences, or computational cost analysis is provided. The limitations section partially acknowledges this but the Summary and Conclusion still use overly broad language.

**W10. Title is descriptive but not reader-friendly.** The title "Mitigating Reward Extrapolation Errors in Offline Preference-Based RL via Attention-Guided Subgoal Discovery" accurately describes the content but is long (17 words) and uses three technical concepts (extrapolation errors, offline preference-based RL, attention-guided subgoal discovery) without communicating the practical benefit or key insight. Consider a shorter title that foregrounds the problem-solution framing.

### Novelty & Positioning (Deferred Verification)
Due to external literature search being unavailable in this run (API token not configured), novelty and related-work completeness cannot be independently verified. Key questions for manual verification include:
- How does SPOT compare to existing subgoal-discovery methods in offline RL (e.g., goal-conditioned RL, hierarchical RL with automatic subgoal discovery)?
- Are there existing PbRL methods that use attention weights for state filtering or reward shaping?
- Is the CVAE-based subgoal generation for reward augmentation novel, or does it overlap with prior work on learned shaping rewards in PbRL?
- How does SPOT compare to the most recent PbRL methods not included in the baseline set?

Authors are encouraged to add a comprehensive related-work comparison table and ensure all closely related methods are cited and discussed.

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: Reward model extrapolation error in offline PbRL]
    |
    v
[Proposed Solution: SPOT]
    |
    +-- Module 1: Attention-guided subgoal identification (Sec 4.1.1-4.1.2)
    |   +-- Extract attention weights w_t from PT
    |   +-- Dual-criteria filtering (top-K% attention + above-avg reward)
    |   +-- CIRCULAR DEPENDENCY WARNING (W3): reward filter uses unreliable model
    |
    +-- Module 2: CVAE subgoal generation (Sec 4.1.3)
    |   +-- Train on triplets (s_t, a_t, g_t)
    |   +-- NEGATIVE LOSS ISSUE (W2): Eq. (8) L_sim in [-1,0]
    |   +-- TEMPORAL MISALIGNMENT (W1): g_t = milestone? s'_t = next state?
    |
    +-- Module 3: Cosine-similarity reward shaping (Sec 4.2)
    |   +-- r_shape = normalize(cos(s'_t, g_hat))
    |   +-- POLICY DISTORTION RISK (W5): non-potential shaping
    |   +-- r_final = r_model + lambda * r_shape
    |
    v
[Empirical Evaluation]
    +-- 10 tasks, 3 benchmarks, 7 baselines
    +-- Highest average score (78.82), lower variance
    +-- SELECTIVE REPORTING (W4): underperforms on 2/10 tasks by >20 pts
    +-- SINGLE-ENV ERROR ANALYSIS (W8): extrapolation shown on 1 env
    |
    v
[Key Uncertainties]
    +-- NOVELTY (deferred): is subgoal-guided shaping for PbRL new?
    +-- REPRODUCIBILITY (W7): architecture details missing
    +-- STATISTICAL SIGNIFICANCE (W4): no test for 4-pt avg lead
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority | Problem | Fix | Expected Gain
---------+---------+-----+-------------
P0 (Must fix) | W1: Temporal mismatch in shaping | Clarify subgoal temporal definition; align comparison target | Core validity
P0 (Must fix) | W2: Negative cosine loss | Replace with L=1-cos or justify | Training correctness
P0 (Must fix) | W4: Selective reporting + no significance | Add balanced discussion + statistical tests | Credibility
P1 (Should fix) | W3: Circular filtering dependency | Add fallback + discuss | Robustness
P1 (Should fix) | W5: Non-potential shaping bias | Analyze distortion + empirical check | Theoretical rigor
P1 (Should fix) | W7: Missing reproducibility details | Add architecture/training hyperparameters | Reproducibility
P2 (Nice-to-have) | W6: Grammar errors | Proofread | Polish
P2 (Nice-to-have) | W8: Single-env error analysis | Add 2+ environments | Generalizability
P2 (Nice-to-have) | W9: Practical applicability overclaim | Bounded wording | Objectivity
P2 (Nice-to-have) | W10: Title readability | Shorten with problem-solution framing | Readability
```

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)
*(Note: The taxonomy below is based solely on manuscript content since external paper search is unavailable. Leaf reference numbers refer to papers cited within the manuscript.)*

```text
Offline PbRL Methods (Root)
├── Branch 1: Reward-model-based methods
│   ├── Leaf 1.1: Markovian reward models [Christiano et al. 2017b, MR baseline]
│   ├── Leaf 1.2: Non-Markovian / attention-based [Kim et al. 2023, PT baseline]
│   └── Leaf 1.3: Regularization-augmented [Tu et al. 2025, DTR baseline]
├── Branch 2: Reward-free / direct optimization
│   ├── Leaf 2.1: Inverse preference learning [Hejna & Sadigh 2023, IPL baseline]
│   ├── Leaf 2.2: Contrastive preference learning [Hejna et al., CPL baseline]
│   └── Leaf 2.3: VAE-based future segment prediction [Gao et al. 2024, HPL baseline]
├── Branch 3: Subgoal / waypoint methods
│   ├── Leaf 3.1: Goal-conditioned RL [Mezghani et al. 2022]
│   └── Leaf 3.2: OURS: Attention-guided subgoal discovery + CVAE + shaping (SPOT)
└── Branch 4: Extrapolation error mitigation in offline RL
    ├── Leaf 4.1: Q-function regularization [BCQ, CQL, IQL]
    └── Leaf 4.2: Reward shaping [Ng et al. 1999, Sun et al. 2022]
```

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a well-motivated problem (reward extrapolation errors in offline PbRL) with a clean, modular framework design (SPOT) that shows competitive aggregate performance across multiple benchmarks. The ablation studies are informative, and the query efficiency analysis is a practical strength.

However, the score is bounded by five major weaknesses that materially affect validity and scientific rigor:

1. **Temporal inconsistency (W1)** between how subgoals are defined (distant milestones) and how they are used (comparison with immediate next state) raises core validity questions about the shaping mechanism.
2. **The negative-valued similarity loss (W2)** in Equation (8) is mathematically atypical and potentially incorrect, threatening the CVAE training objective.
3. **Circular dependence (W3)** in subgoal filtering (using the same unreliable reward model to select training targets) is a design vulnerability that is not discussed.
4. **Selective result interpretation (W4)** with no statistical significance testing weakens the empirical claims.
5. **Policy invariance distortion (W5)** from non-potential-based shaping is neither analyzed nor empirically bounded.

Additionally, novelty cannot be independently verified in this run due to unavailable external literature search (deferred manual verification required). The paper's contribution, while plausible, may overlap with existing subgoal-based RL and attention-based PbRL methods.

The strengths are real (problem motivation, modular design, comprehensive baseline comparison, ablation studies), and the identified weaknesses are substantially fixable — none is fatal. With rigorous revision addressing the temporal consistency, loss formulation, and empirical rigor, the paper could become a solid contribution.

**Post-Revision Target:** [7, 8]/10 — achievable if the five major weaknesses are satisfactorily resolved through corrected loss formulation, clarified temporal alignment, added statistical testing, balanced reporting, and analysis of shaping distortion.