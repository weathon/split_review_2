## Summary
# Final Review Report

## Summary

This paper introduces **Direct Optimal Action Learning (DOAL)**, a framework for policy extraction from Q-value functions in offline reinforcement learning. The core insight is that the reparameterized policy gradient of the behavior-regularized actor-critic (BRAC) objective can be approximated by a simpler behavior-clone loss toward an optimized target action. This decouples target computation from the policy, enabling the use of efficient distribution-native losses (e.g., flow-matching or diffusion losses) without backpropagating through iterative sampling chains.

The paper makes three main contributions: (C1) the DOAL framework that constructs target actions using Q-value gradients at data actions and learns them with native losses; (C2) a Batch-Normalizing Optimizer that reparameterizes the behavior-regularization coefficient α into an interpretable trust-region parameter δ via batch-level gradient normalization; (C3) an analysis showing that the sample size in MaxQ sampling must be carefully balanced to avoid overestimation bias.

Empirically, the paper tests DOAL across three Q-value estimation methods (IQL, Q-learning, regularized Q-learning) and three policy classes (Gaussian, Flow, Diffusion) on OGBench and D4RL benchmarks. Results show that DOAL yields aggregate improvements over strong MaxQ-sampling baselines on OGBench, particularly when Q-functions are well-regularized. On D4RL Adroit tasks, gains are observed only with regularized Q-learning. The paper candidly acknowledges that DOAL's effectiveness depends on Q-function gradient quality and does not always outperform baselines.

**Novelty assessment:** Due to external literature retrieval being unavailable in this run, novelty and comparison conclusions are deferred for manual verification. The core technical idea — constructing a target action using Q-gradients at the data action and then learning it with native generative losses — appears to be a reasonable contribution to the offline RL policy extraction literature, but its overlap with existing value-guidance methods (QGPO, SFBC, EDA) cannot be fully assessed without retrieval.

## Strengths
**S1. Clean theoretical motivation.** Proposition 1 provides a principled derivation showing that the BRAC policy gradient is equivalent to a squared-error gradient toward a target action. This insight cleanly motivates the decoupled learning approach and is presented with sufficient mathematical rigor. The mismatch between the point of gradient evaluation (at π_θ(s)) and the point of expansion (at a) is honestly discussed, showing intellectual transparency.

**S2. Practical hyperparameter simplification.** The Batch-Normalizing Optimizer (Proposition 2) replaces the notoriously sensitive α hyperparameter with a more interpretable δ that directly controls the expected L2 displacement of the target action. Empirical evidence (Table 3) confirms that δ varies across a much narrower range (factor of ~3 on OGBench) than α (factor of ~100), reducing tuning cost. The intuition that gradient norms vary significantly across tasks but normalizing by batch statistics compensates for this is well-motivated.

**S3. Comprehensive empirical design.** The paper systematically tests three value estimation methods (IQL, Q-learning, regularized Q-learning) with three policy classes (Gaussian, Flow, Diffusion) across 15 tasks. This 3×3 design cleanly isolates the effect of DOAL from the choice of Q-function and policy architecture. The inclusion of both baseline (MaxQ sampling without gradient access) and DOAL versions for each combination enables clear attribution of any gains to the gradient-based target construction.

**S4. Honest limitation reporting.** Section 5.1 candidly acknowledges that DOAL gains are driven by "one or two tasks" on OGBench and that "there is no performance gain from either DOAL model or even ETrigflow" on D4RL with IQL. The paper also notes that the effectiveness of DOAL "might depend on the task or quality of Q value function." This level of empirical honesty is commendable and rare.

**S5. Detailed complexity analysis.** Figure 2 provides a break-down of forward/backward calls for each algorithm variant, with actual runtime measurements. The finding that FQL runs faster than predicted due to one-step policy testing is a useful practical insight. The observation that only BPTT consumes significantly more memory helps practitioners decide when to use gradient-based methods vs. DOAL.

## Weaknesses
### W1. Conditional effectiveness limits practical impact (Major)
The paper's own evidence shows that DOAL's improvements are conditional on Q-function quality and task. On OGBench, gains are "due to one or two tasks" with "otherwise, their performance is very similar." On D4RL with IQL, "there is no performance gain from either DOAL model or even ETrigflow." On Adroit, only regularized Q-learning produces gains. This pattern reveals a fundamental limitation: DOAL relies on ∇_a Q(s,a) at the data action being a reliable indicator of the direction toward higher-value actions. When Q-function gradients are noisy or misaligned (unregularized Q-learning, IQL in high-D4RL tasks), DOAL does not improve over simple MaxQ sampling baselines. The paper does not provide a diagnostic (e.g., gradient-sign consistency, cosine similarity between gradient and true improvement direction) to predict when DOAL will help vs. hurt.

**Required action:** Add a gradient-quality diagnostic experiment (e.g., measure correlation between ∇_a Q(s,a) and the true action improvement direction on a validation set) across tasks where DOAL helps vs. does not help. Explicitly state the conditions under which practitioners should expect DOAL to be beneficial.

### W2. The Batch-Normalizing Optimizer is a reparameterization, not a new algorithm (Major)
As the authors themselves acknowledge (Page 4, Section 3.2): "We are not claiming that this batch normalized scheme can find better a^{target} than not using batch-normalized gradient. In fact, if the gradient statistics is stable, you can always get the same result by having g(s,a) = C·∇_a Q_φ(s,a)." This admission means the core technical contribution of Proposition 2 is a reparameterization of α into δ via a dataset-dependent constant — mathematically equivalent to scaling the learning rate by the inverse mean gradient norm per dataset. The claimed advantage (δ varies less than α) is a statement about units and ranges, not about algorithmic novelty. While practically useful, this is not a fundamentally new optimization principle.

**Required action:** Either (a) present the batch-normalizing optimizer as a practical hyperparameter reduction technique (which is still useful and publishable) rather than as a novel algorithmic contribution, or (b) provide evidence that the batch-normalized update finds better fixed points than any constant scaling factor, i.e., that the normalization interacts beneficially with optimization dynamics beyond mere rescaling.

### W3. DAO (redudant α parameter after batch normalization) (Major)
Section 3.3 (Eq. 16-17) retains the α hyperparameter from FQL even after introducing δ as the trust-region parameter. The paper states "We still keep the α parameter from (Park et al., 2025c) for all experiments for consistency. In ablation study in Appendix F, we find setting it to 1 is fine." This creates confusion about the independent roles of α and δ. If α=1 is fine (as the ablation indicates), then α serves no independent function and should be removed from the main formulation. If α serves a different purpose (e.g., controlling behavior-regularization strength separately from the target-action trust region), this should be explicitly stated and empirically demonstrated with a sensitivity analysis showing when α ≠ 1 is beneficial.

**Required action:** Either (a) set α=1 as default, remove it from Eq. (16), and clearly state that δ alone controls the exploration-exploitation trade-off, or (b) design an ablation that varies both α and δ independently to demonstrate their distinct functional roles, and update the formulation accordingly.

### W4. Proposition 3's assumptions limit practical relevance (Minor)
The informal Proposition 3 about MaxQ sampling overestimation assumes independent Gaussian Q-estimates for each action. In practice, Q-estimates for different actions are correlated through the shared neural network, and action spaces are bounded (e.g., [-1,1] in OGBench). The asymptotic divergence claim (n→∞) relies on unbounded Gaussian noise and would not occur with bounded noise or truncated distributions. The practical takeaway — that n_sample should be tuned, not set to a large value — is valuable and empirically supported, but the formal proposition overstates the theoretical grounding.

**Required action:** Add a finite-sample analysis or bounded-noise variant, and explicitly note the independence and unbounded-noise limitations. The practical recommendation (tune n_sample) is already well-supported by the experimental results (Tables 1-2) and does not require strong asymptotic assumptions.

### W5. Missing comparison with value-guidance baselines (Major)
The Related Work section (Section 6) lists QGPO, SFBC, EDA, QVPO, and CFGRL as methods that use Q-function gradients for action generation, but none of these are included as baselines in the experiments. Since DOAL also uses Q-function gradients (albeit in a simplified manner), comparing against these methods is essential to establish DOAL's relative efficiency and effectiveness. Without such comparisons, the claim that DOAL is "efficient, effective, and versatile" (abstract) cannot be fully evaluated. The paper relies heavily on comparison with FQL (which is also from the same research group), raising concerns about baseline selectivity.

**Required action:** Add at least one representative value-guidance baseline (e.g., QGPO-style guided sampling with IQL) to the main experiments. Provide a clear comparison on computational cost (function calls) and performance across OGBench tasks.

### W6. Time complexity claim requires qualification (Minor)
The paper states that "DOAL costs one extra forward and backward call of the Q value net, compared to baselines" (Page 1, Introduction). However, as analyzed in Section 5.2 (Table on Page 7), computing ∇_a Q(s,a) requires a backward-through-input operation (computing dQ/da), which is more memory-intensive than a standard parameter-gradient backward pass because it requires storing intermediate activations. The paper's function-call counting treats all backward calls as equivalent, but the memory footprint differs. This could be a practical concern for large Q-networks or resource-constrained settings.

**Required action:** Add a note in the complexity analysis distinguishing between backward-through-parameter (standard) and backward-through-input (for ∇_a Q) calls, with a brief discussion of memory implications. Provide peak memory usage numbers for at least one representative configuration.

### W7. Abstract overstates conclusions (Minor)
The abstract claims "our baseline models outperformed the previous best models, and DOAL improves over strong baseline models while simplifying hyperparameter search" without mentioning the conditional nature of these improvements (task-dependent, Q-function-quality-dependent). This creates an expectations mismatch with the paper's own nuanced discussion in Section 5.1.

**Required action:** Revise the abstract to reflect the conditional nature of the findings, as suggested in Annotation #1.

### W8. Flow matching direction convention unclear (Minor)
The flow matching formulation (Eq. 3-4) reverses the standard p₁/p₀ convention (using p₁ as noise and p₀ as data) but does not clearly explain the direction of the learned velocity field. The reverse Euler step a_{t-Δt} = a_t + Δt·v_θ(a_t,t) moves from noise to data, but this convention differs from some flow matching literature. While mathematically consistent, the sign and direction conventions should be explicitly stated to avoid confusion.

**Required action:** Add a clarifying sentence after Eq. (4) stating that v_θ predicts the displacement toward the clean action, as suggested in Annotation #10.

### W9. Conclusion could be more structured (Minor)
The conclusion is brief but does not clearly separate validated findings, limitations, and future directions. It introduces new unsupported claims (e.g., "better uncertainty aware Q estimation should be explored") without concrete hypotheses or expected impact.

**Required action:** Restructure the conclusion into three parts: what has been shown, under what conditions, and what specific next steps are most promising (as suggested in Annotation #11).

### W10. Missing limitation: α sensitivity (Minor)
While the paper extensively discusses α sensitivity in BRAC methods and presents δ as a solution, the α parameter still appears in the DOAL objective (Eq. 16). If DOAL's key advantage is reduced hyperparameter sensitivity, the continued presence of α undermines this message. The paper should either demonstrate that DOAL is robust to α (which the ablation in Appendix F apparently does) or remove α from the formulation entirely.

**Required action:** Clearly state in the main text that α can be fixed to 1 without loss of performance, citing the Appendix F ablation, and remove α from the main DOAL equation for clarity.

## Score
**Final Score: 6/10**

**Scoring rationale:**

The paper presents a technically sound framework (DOAL) with clean theoretical motivation (Proposition 1) and practical hyperparameter simplification (batch-normalized δ). The empirical design is comprehensive, testing across multiple value functions and policy classes, and the honest reporting of mixed results is commendable.

However, the score is constrained by several factors:

1. **Research value is moderate.** The core technical insight — decoupling target computation from policy via gradient-equivalent target actions — is useful but incremental. The batch-normalizing optimizer is acknowledged by the authors themselves to be mathematically equivalent to a constant scaling factor per dataset, reducing its novelty. DOAL's practical gains are conditional (task-dependent, Q-function-quality-dependent) and driven by a few tasks, limiting its broad applicability.

2. **Missing baseline comparisons** with value-guidance methods (QGPO, SFBC, EDA) that also use Q-gradients make it difficult to assess DOAL's relative efficiency and effectiveness. The paper relies heavily on comparison with FQL from the same research group.

3. **Formulation clarity issues** (retained α parameter with unclear role after δ introduction, flow-matching convention ambiguity) and an abstract that overstates the conditional findings reduce overall polish.

4. **External novelty verification could not be performed** in this run (retrieval-disabled), so novelty conclusions are conservative and may change with full literature review.

**Strengths that support the score:** Clean theoretical motivation, practical hyperparameter reduction, comprehensive 3×3 experimental design, honest limitation reporting, detailed complexity analysis.

**Weaknesses that constrain the score:** Conditional effectiveness, batch-normalizing optimizer is a reparameterization not a new algorithm, missing value-guidance baselines, unclear α vs. δ roles, overstated abstract, and inability to verify novelty against existing literature.

The paper is a solid contribution to the offline RL policy extraction literature and would likely be accepted at a venue like NeurIPS or ICML with revisions addressing the missing baselines and formulation clarity issues. The core idea (learning optimized target actions with native generative losses) is likely to be useful for practitioners working with expressive policies and regularized Q-functions.