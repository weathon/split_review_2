## Summary
# Final Review Report

## Summary

This paper presents Guided Hybrid Policy Optimization (GHPO), a reinforcement learning framework for fine-tuning LLMs on math reasoning tasks. GHPO addresses the reward-sparsity problem in GRPO-based RLVR by adaptively injecting ground-truth solution hints when the model fails to generate any correct responses for a given problem. The framework consists of three components: (1) an automated difficulty detection module that identifies problems where all G sampled responses yield zero reward; (2) an adaptive prompt refinement mechanism that appends partial ground-truth solution traces to difficult prompts; and (3) a cold-start strategy that applies standard GRPO for the first 20 steps to build format compliance.

The method is evaluated on two 7B-scale models (Qwen2.5-Base-7B and Qwen2.5-Math-7B) across six math benchmarks. The reported results show average accuracy improvements of approximately 5% over GRPO and curriculum-learning baselines. Training-dynamics analysis shows that GHPO achieves higher accuracy reward, longer response lengths, and smaller gradient norms compared to GRPO.

**Overall assessment:** GHPO addresses a genuine problem (reward sparsity in RLVR) with a practical and intuitive idea (dynamic hint injection based on group reward analysis). The experimental results are encouraging but suffer from systematic weaknesses: missing variance/statistical significance, untested core assumption, underspecified advantage computation, and overclaimed scope. The paper would benefit from tightening the methodology exposition, adding rigorous statistical evaluation, and bounding claims to the tested setting. Novelty assessment is deferred to manual literature verification because external paper search was unavailable in this review run.

## Strengths
1. **Well-motivated problem.** The paper identifies a genuine and practically important limitation of GRPO-based RLVR: when training problems consistently exceed the model's capacity, all sampled responses yield zero reward, producing no learning signal. This "reward sparsity from capacity-difficulty mismatch" is clearly articulated and empirically demonstrated (52% failure rate on NuminaMath-1.5 for a 7B instruct model).

2. **Simple and intuitive solution.** The core idea of GHPO — detecting difficult problems via group reward analysis and injecting ground-truth hints only when needed — is elegant and practical. The switching mechanism (Eq. 2) is conceptually straightforward: if any response is correct, use standard GRPO; otherwise, augment the prompt with solution hints. This avoids complex meta-learning or auxiliary models.

3. **Consistent empirical improvements.** Across two model families (Qwen2.5-Base-7B and Qwen2.5-Math-7B) and six benchmarks, GHPO consistently outperforms GRPO and curriculum-learning baselines. The reported average gain of approximately 4-5% is practically meaningful for challenging math benchmarks. The improvement is particularly notable on harder benchmarks (AIME24: 0.122→0.163; GPQA-Diamond: 0.308→0.394).

4. **Training-dynamics analysis.** The paper provides useful diagnostic plots (Figure 4) showing accuracy reward, response length, and gradient norm trajectories. Even though the interpretation is sometimes over-extended, the raw data is informative and helps readers understand the method's behavior.

5. **Reproducibility-minded.** The source code is provided via anonymous repository, and training details (8×80GB GPUs, openrl codebase) are specified. The cold-start strategy and multi-stage guidance are described in sufficient detail for replication attempts.

## Weaknesses
The weaknesses are ordered from highest to lowest severity.

### W1. Core assumption (Assumption 1) is not experimentally validated (Major)

The paper's theoretical foundation rests on Assumption 1: training on a problem with its ground-truth trace improves OOD generalization compared to training without the trace. However, no dedicated experiment isolates this effect. The experiments in Section 4 evaluate the full GHPO system, which includes difficulty detection, cold-start strategy, and multi-stage guidance — any of these components could be responsible for the observed gains. Without a controlled ablation that directly tests Assumption 1 (e.g., training on a set of zero-reward problems with vs. without trace conditioning), the fundamental premise of the paper remains unverified.

**Impact:** If Assumption 1 is false, the entire motivation for GHPO collapses — the method's gains could stem entirely from auxiliary components rather than from trace conditioning. This is a validity-critical gap.

**Repair path (Must):** Add a controlled experiment: select a subset of problems where the base model achieves zero accuracy across G samples. Train two models: (a) standard GRPO on these problems (expected to produce no learning signal), and (b) GRPO with ground-truth trace conditioning. Report accuracy on a held-out difficult set. If (b) significantly outperforms (a), Assumption 1 is supported.

### W2. All results lack variance estimates and statistical significance (Major)

Tables 1 and 2 report single-point accuracy figures without standard deviations, confidence intervals, or significance tests. Many reported improvements are small in absolute terms (e.g., Math-500: 0.774→0.776; OlympiadBench: 0.396→0.389; AIME24: 0.122→0.163). Without multi-seed variance information, it is impossible to determine whether these differences are systematic or within the noise range of a single training run.

**Impact:** The paper's central claim — "GHPO consistently outperforms GRPO" — cannot be rigorously evaluated. This directly undermines the empirical contribution.

**Repair path (Must):** Report all results as mean ± std over at least 3 independent training seeds with different random seeds. For the key GHPO vs. GRPO comparison, include a paired statistical test (bootstrap or Wilcoxon signed-rank) with explicit p-values. If multi-seed training is computationally prohibitive, at minimum report 3-seed results for the main comparison on the mixed dataset (Table 2).

### W3. Advantage computation in GHPO is underspecified (Major)

Equation (1) uses advantage estimates Â_{i,t} in the clipped surrogate loss, but the paper never defines how Â_{i,t} is computed under GHPO. Section 2.2 defines GRPO's advantage as Â_{i,t} = (R_i - μ_R)/(σ_R + ε), but Section 3.2 states "Unlike GRPO, these group rewards are not directly used for advantage estimation." If the standard GRPO advantage is not used, what replaces it? The paper provides no definition, making the objective function underspecified and non-reproducible.

**Impact:** The core mathematical object of the training algorithm is incompletely specified. A reader or practitioner cannot implement GHPO from the description alone.

**Repair path (Must):** Explicitly state how advantages are computed. The most natural choice is to use the same GRPO advantage formula but with rewards from the original (non-hint-augmented) responses. Add a sentence: "Here, Â_{i,t} is computed as Â_{i,t} = (R_i - μ_R)/(σ_R + ε) using the binary rewards {R_i}_{i=1}^G from the original responses, before any hint augmentation." If a different advantage is used, provide the exact formula.

### W4. Missing differentiation from LUFFY and thematic related work (Major)

The related work section is a chronological list rather than a thematic synthesis. Critically, LUFFY [Yan et al. 2025] also combines imitation learning with on-policy RL — a strikingly similar approach to GHPO. The paper mentions LUFFY only in passing ("balances imitation and exploration by augmenting on-policy zero RL training with off-policy reasoning demonstrations") without clearly explaining how GHPO differs. A reader may reasonably conclude that GHPO is LUFFY with ground-truth traces replacing off-policy demonstrations.

**Impact:** The novelty claim of GHPO is weakened without explicit differentiation from LUFFY. This is a positioning risk.

**Repair path (Must):** Restructure related work around thematic axes (filtering-based, curriculum-based, hybrid imitation-RL). Add a dedicated comparison paragraph: "Unlike LUFFY, which requires an external demonstration dataset and uses a fixed mixing ratio, GHPO uses the problem's own ground-truth solution trace and adaptively decides when to apply guidance via group reward analysis."

### W5. Conclusion and abstract overclaim beyond evidence (Major)

The abstract claims GHPO offers "a scalable and efficient solution for developing powerful and robust reasoning models." The conclusion similarly describes GHPO as "robust, scalable, and data-efficient." The experiments only cover 7B-scale models on math benchmarks — no evidence of scalability (larger models), robustness (distribution shift, OOD), or general reasoning capability beyond math is provided. "Robust" is particularly problematic as no robustness evaluation is conducted.

**Impact:** Overclaiming inflates the paper's apparent contribution and may trigger rejection from reviewers who value precise claim-evidence alignment.

**Repair path (Must):** Bound every claim to the tested setting. Replace with: "Our results show that GHPO improves accuracy on math reasoning tasks for 7B-scale models and provides more stable training dynamics. Extending to larger models and other domains remains future work."

### W6. Gradient norm and response length over-interpretation (Major)

The training-dynamics analysis claims that smaller gradient norms "indicate a smoother and more stable optimization process" and that longer responses "suggest GHPO's enhanced capacity to construct more detailed reasoning processes." These are correlational observations, not causal conclusions. Smaller gradient norms could simply reflect regularization from hint conditioning rather than "stability." Longer responses could result from the model copying longer textual hints rather than genuine reasoning improvement.

**Impact:** The paper presents storytelling as evidence, which reduces scientific credibility. A skeptical reviewer will note that none of these claims are tested with controlled experiments.

**Repair path (Major):** Replace causal language with correlational language. Add a control experiment: compare GHPO with a baseline that appends random-length text (instead of solution hints) to test whether longer responses are simply a side effect of longer prompts. Consider adding a stability metric (e.g., gradient variance across updates).

### W7. Cold-start hyperparameter N=20 is unjustified (Minor)

The cold-start strategy uses N=20 optimization steps, but no ablation or sensitivity analysis is provided. The term "optional" creates ambiguity about whether this component is needed for the method's success.

**Repair path (Nice-to-have):** Add a sensitivity analysis varying N in {5, 10, 20, 50}. Clarify that the cold-start is recommended (not optional) for the reported setting.

### W8. Inconsistent notation in Eq. (2) (Minor)

Equation (2) uses `∑_{i=1}^n f(a, o_i) > 0` with `n` instead of `G` (used everywhere else), and `f` is defined vaguely as "assesses whether the prediction is equivalent to the ground truth" without linking to the reward model.

**Repair path (Must):** Replace `n` with `G`. Clarify that `f` is the answer-verification function producing binary rewards R_i.

### Novelty & Literature Comparison (Deferred)

External paper search was unavailable during this review. All novelty and literature-comparison conclusions are deferred for manual verification. A proper assessment would require a systematic search for methods that combine imitation learning with on-policy RL for LLM reasoning (e.g., LUFFY, DAGP, related work), as well as the broader field of adaptive difficulty in RL for LLMs. Without this evidence, no definitive novelty judgment can be made.

## Score
**Final Score: 5/10**

**Rationale:** The paper addresses a genuine and important problem (reward sparsity in RLVR for LLM reasoning) with a conceptually clean idea (adaptive hint injection based on group-reward analysis). The experimental results show consistent improvements over GRPO across six math benchmarks. However, several validity-critical issues prevent a higher score:

1. **Core assumption unvalidated (W1).** The theoretical foundation (Assumption 1) is never directly tested, so the mechanism behind the reported gains remains unclear.
2. **No statistical rigor (W2).** All results are single-point estimates without variance or significance tests, making it impossible to assess reliability.
3. **Underspecified algorithm (W3).** The advantage computation in the GHPO objective is not defined, preventing reproduction.
4. **Missing related-work positioning (W4).** The paper inadequately differentiates GHPO from LUFFY, which shares the same hybrid imitation-RL approach.
5. **Scope overclaiming (W5).** Abstract and conclusion claim robustness and scalability beyond the evidence.

On the positive side, the core idea is well-motivated, the empirical trends are consistent across models and benchmarks, and the training-dynamics analysis provides useful insights. With significant revision — particularly adding variance reporting, direct validation of Assumption 1, proper advantage specification, and claim bounding — the paper could reach 7-8/10 range. Without these changes, the contribution remains incompletely supported.

**As a qualified acceptance recommendation:** The paper would need (a) multi-seed results with statistical tests, (b) a controlled test of Assumption 1, (c) corrected Eq. (1)-(2) with explicit advantage definition, and (d) tightened claims. These are feasible revisions and would substantially strengthen the paper.

*Note: Novelty assessment is deferred to manual literature verification, as external paper search was unavailable in this review run. The score may need adjustment if significant overlapping prior work is identified.*