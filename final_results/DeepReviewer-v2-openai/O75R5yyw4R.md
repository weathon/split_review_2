## Summary
# Final Review Report

## Summary

This paper proposes **IterRef**, a test-time scaling method for discrete diffusion models that uses Multiple-Try Metropolis (MTM) with reward-guided noising-denoising transitions to iteratively refine intermediate states during sampling. The method is evaluated on language (MDLM, LLaDA-8B) and image (MaskGIT) domains across several reward functions (toxicity, sentiment, CoLA, perplexity, CLIPScore). IterRef consistently outperforms existing baselines (BoN, SVDD, FK Steering, SoP) under matched computational budgets, with particularly strong gains at low NFE settings. The paper also identifies that later denoising stages play a more critical role for discrete diffusion refinement (contrasting with continuous diffusion) and provides a convergence guarantee under a reversibility assumption.

**Core contributions:** (C1) A test-time scaling method IterRef using MTM-based iterative refinement; (C2) Empirical identification of task-dependent optimal timestep allocation; (C3) Theoretical convergence guarantee to the reward-aligned target distribution under reversibility.

**Overall assessment:** The paper addresses an important and timely problem (test-time scaling for discrete diffusion) with a technically sound core idea (MCMC-based in-situ refinement). The empirical results are promising and the experiments span multiple backbones and tasks. However, the paper has several major weaknesses: (1) a critical formula error in the acceptance ratio (Eq. 3), (2) no statistical variance or significance reporting, (3) an unverified reversibility assumption for the convergence proof, (4) no hyperparameter analysis for the critical temperature α, and (5) missing limitations discussion. These issues materially limit the paper's current scientific contribution. Novelty verification is deferred due to external literature search being unavailable in this run.

## Strengths
1. **Timely and well-motivated problem.** Test-time scaling for discrete diffusion is a relevant and underexplored area. The paper clearly articulates why gradient-based guidance is not directly applicable and why token fixation limits single-pass methods.

2. **Technically principled approach with convergence guarantee.** Using Multiple-Try Metropolis to iteratively refine intermediate states is a theoretically grounded design. The connection to the predictor-corrector paradigm and the formalization within MTM provides a solid conceptual foundation. Proposition 1 establishes convergence under a reversible kernel assumption, which is appropriately stated.

3. **Broad empirical evaluation.** The method is evaluated across two language backbones (MDLM, LLaDA-8B) and one image backbone (MaskGIT), with four language reward functions (toxicity, sentiment, CoLA, perplexity) and CLIPScore for images. This breadth strengthens the claim of cross-modal generality.

4. **Informative analyses.** The effective timestep analysis (Table 2) and the k vs N comparison (Table 3, Figure 4) provide useful insights into how IterRef works and where refinement is most impactful. The finding that later denoising stages are more important for discrete diffusion (contrasting with continuous diffusion) is a non-trivial empirical observation.

5. **Promising empirical results.** Under matched NFE budgets, IterRef consistently achieves higher reward scores than baselines across most settings. The gains at low compute (e.g., 2T NFE matching 32T baseline performance) are striking and suggest practical value for compute-constrained scenarios.

6. **Computational efficiency considerations.** The paper discusses practical tricks to reduce overhead (pool reuse, selective refinement via $\mathcal{U}$), showing awareness of deployment concerns. The acknowledgment that NFE aggregation can obscure cost profiles is a good practice signal.

## Weaknesses
### W1. Critical: Formula error in acceptance ratio (Eq. 3)

The acceptance ratio in Equation (3) is written as $\beta = \min(1, \exp((r(x_t') - r(x_t)/\alpha)))$. The parentheses are misaligned: the exponent computes $\exp(r(x_t') - r(x_t)/\alpha)$ rather than $\exp((r(x_t') - r(x_t))/\alpha)$. This means the current-state reward $r(x_t)$ is divided by $\alpha$ while the proposed-state reward $r(x_t')$ is not, creating an asymmetric acceptance criterion. The intended form (matching standard reward-guided generation and MTM theory) is $\beta = \min(1, \exp((r(x_t') - r(x_t))/\alpha))$. If the published equation is implemented as written, the chain targets a different distribution and may exhibit systematic bias against states with lower $r(x_t)$. **Severity: Critical** — this directly affects the correctness of the sampling algorithm.

### W2. Major: Complete absence of statistical reporting

All experimental results are reported as single-point estimates without variance, standard deviation, confidence intervals, or significance tests. This includes Figure 2 (main comparison), Table 1 (MaskGIT), Table 2 (timestep analysis), Table 3 (k vs N), and Figure 5(a) (detoxification). The language experiments use only 3 seeds, which together with no variance reporting means the reader cannot assess whether the reported improvements are statistically reliable or driven by seed-specific variation. The paper uses strong language ("consistently outperforms," "far surpassing") but provides no statistical basis for these claims. **Severity: Major** — this undermines the core empirical contribution.

### W3. Major: Ungrounded convergence guarantee (Proposition 1)

Proposition 1 asserts convergence to the optimal distribution $p^*(x_t)$ under the assumption that $q$ and $p_\theta$ form a reversible Markov kernel. However: (a) The reversibility condition is non-trivial for learned denoisers $p_\theta$ that only approximate the true reverse process; (b) No empirical verification (e.g., acceptance rate monitoring, trace plots, Gelman-Rubin diagnostics) is provided to check whether the chain actually converges in practice; (c) The proposition states convergence as $k \to \infty$, but the practical number of iterations $k$ is small (typically 4-8 in experiments), making asymptotic guarantees of limited value. The theoretical claim thus has a significant gap between the assumptions and the practical setup. **Severity: Major** — Contribution 3 is weakened.

### W4. Major: Missing hyperparameter analysis for $\alpha$

The temperature/regularization parameter $\alpha$ controls (a) the KL divergence strength in the target distribution, (b) the acceptance probability $\beta$, and (c) the intermediate reward function $r(x_t)$. Despite this central role, $\alpha$ is never ablated, its default value is not reported, and its sensitivity is not discussed. Without this analysis, it is unclear whether IterRef requires careful per-task tuning of $\alpha$ or is robust to its choice. The acceptance rate dynamics (how often the chain accepts lower-reward proposals) are also undocumented. **Severity: Major** — one of only four hyperparameters, left unexamined.

### W5. Major: Detoxification case study lacks fluency validation

The safety alignment case study (Section 4.5) measures only toxicity reduction without evaluating whether the generated text remains fluent/coherent. The qualitative examples raise concerns: IterRef's outputs appear to change the topic (e.g., generating "so over this place called Trinidad" as a response to a hate speech prompt), which may bypass the toxicity classifier through topic shift rather than genuine detoxification. Additionally, Figure 5(a) confusingly distinguishes "IterRef" from "Ours" as separate methods — this needs clarification. The small prompt set (15 prompts, 20 samples each) is also a limited basis for safety claims. **Severity: Major** — the case study's most striking claims lack necessary controls.

### W6. Major: No OOD or generalization evaluation

All experiments are conducted on in-distribution benchmarks (controlled prompts, ImageNet classes). The paper claims practical value for real-world deployment but provides no out-of-distribution evaluation, domain shift tests, or failure case analysis. Given that reward-guided generation methods are known to exhibit reward over-optimization (Goodhart's law), the absence of any robustness/stress testing is a significant omission. **Severity: Major** — generalization claims cannot be evaluated.

### W7. Major: Related work is a listing rather than structured comparison

The related work section lists prior methods sequentially without organizing them along clear comparison axes (e.g., single-trajectory vs multi-trajectory, whether intermediate states can be revised, use of gradients). This makes it harder for readers to understand how IterRef specifically differs from each prior work. The claim that all prior methods "share a common focus: selecting better samples" oversimplifies the diversity of approaches (particle resampling vs importance weighting vs tree search). **Severity: Major** — the positioning of IterRef's novelty is less clear than it could be.

### W8. Minor: Overclaiming language in abstract and title

The abstract uses "far surpassing prior state-of-the-art baselines" and "striking gains" without specifying the baselines, budgets, or margins. The title claims "Effective Test-Time Scaling" without qualifying the conditions under which IterRef is effective (the method's effectiveness varies by task, as shown in Section 4.2). The contribution claims state "consistently outperforms" — but the CoLA results with LLaDA show BoN outperforms IterRef, contradicting "consistently." **Severity: Minor** — affects credibility but not technical validity.

### W9. Minor: NFE aggregation conflates different cost types

The paper acknowledges that aggregating generative model calls and reward model calls into a single NFE "may obscure meaningful differences" (Section 3.3), but then reports all main results using aggregated NFE without providing the breakdown in the main text. Readers cannot determine whether IterRef's advantage comes from more efficient use of generative model calls (the expensive component for large models) or from better reward model utilization. **Severity: Minor** — partially addressed in appendix.

### W10. Minor: Conclusion omits limitations

The conclusion summarizes contributions without acknowledging any of the limitations discussed above (reversibility assumption, task-dependent effectiveness, $\alpha$ sensitivity, statistical reliability). Including limitations would improve scientific credibility. **Severity: Minor** — straightforward to fix.

## Score
**Final Score: 5/10**

**Rationale:** The paper tackles an important and well-motivated problem with a principled technical approach. The core idea (MCMC-based iterative refinement for discrete diffusion) is timely and the empirical evaluation spans multiple backbones and tasks. However, the paper is held back by several serious issues that prevent it from being a strong contribution in its current form:

1. **Critical formula error (W1)** in the acceptance ratio (Eq. 3) raises doubts about whether the implemented algorithm matches the theoretical derivation. This must be corrected and verified before the paper can be assessed on its technical merits.

2. **Major empirical validity concerns (W2, W4, W5):** The complete absence of statistical reporting (no variance, no significance tests) with only 3 seeds makes it impossible to assess the reliability of the claimed improvements. The key hyperparameter $\alpha$ is left unexamined. The detoxification study lacks fluency controls.

3. **Theoretical gap (W3):** The convergence guarantee depends on an unverified reversibility assumption, with no empirical diagnostics to bridge theory and practice.

4. **Novelty is promising but unverifiable in this review:** The combination of MTM with discrete diffusion appears novel, but without external literature verification (unavailable in this run), a definitive novelty judgment is deferred.

**Bottom line:** The paper has a solid core idea and broad experiments, but the current manuscript has too many validity gaps to support its strong claims. A major revision addressing the formula error, adding statistical rigor, analyzing $\alpha$, verifying convergence in practice, and adding limitations would substantially strengthen the paper. With these fixes, the paper could potentially reach 6-7/10.

**Score breakdown by dimensions:**
- Research value / significance: 6/10 (important problem, well-motivated)
- Novelty of contribution: ~6/10 (deferred — external verification unavailable)
- Technical soundness: 4/10 (formula error, unverified assumption, no statistics)
- Empirical rigor: 3/10 (no variance, small seeds, missing controls)
- Reproducibility: 5/10 (method clearly described but hyperparameters and acceptance rate missing)
- Clarity and presentation: 6/10 (generally well-written, but related work needs restructuring)