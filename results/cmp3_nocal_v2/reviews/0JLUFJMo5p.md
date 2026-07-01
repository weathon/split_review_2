## Summary

This paper proposes Dynamic Task-Embedded Reward Machine (DTERM), a framework that replaces static reward weighting in RL for code generation with dynamic, task-conditioned reward composition. A hypernetwork takes task embeddings (from CodeBERT) and generates context-dependent weights for sub-rewards (compilation success, test case passing rate, code similarity, style, efficiency). The method further incorporates cross-task prototypes for zero-shot generalization, multi-modal fusion, and RLHF integration. Experiments on four code benchmarks with an ablation study are presented.

---

## Strengths

1. **Well-motivated problem formulation.** The core idea — using a hypernetwork conditioned on task embeddings to dynamically generate reward weights (Section 4.1, Equations 5-6) — is clearly described and intuitively reasonable: different code tasks (repair vs. translation vs. completion) plausibly need different reward emphases. This is a concrete and sensible technical contribution.

2. **Principled ablation study.** Table 2 systematically ablates the hypernetwork, task embedding, FiLM modulation, compiler feedback, and static prototypes on HumanEval. This provides internal validation that individual components contribute positively.

3. **Mathematical formalization is clear.** The key equations (5-11) for dynamic weighting, cross-task prototypes (attention over learned prototypes), compiler feedback (exponential decay over error count), and multi-modal fusion are presented in a self-contained manner.

---

## Weaknesses

### Fatal
None.

### Major

1. **Critical experimental details are missing, preventing verification.** The paper states "We train using PPO" (line 201) but never specifies what the policy network is — its architecture, parameter count, whether it is an LLM-based code generator, or how it relates to the task embeddings. The meta-training procedure for learning prototypes (Section 4.3) is invoked but the number of meta-training tasks, their composition, and the training/unseen split are entirely unspecified. The "10 unseen tasks" in Figure 2 are never defined or named, making it impossible to assess what "zero-shot adaptation" means. Without these details, the experimental results cannot be reproduced or independently assessed.

2. **No variance or uncertainty is reported despite claiming 3 random seeds.** The paper states "3 random seeds" (line 201), but Tables 1 and 2 report only single numbers with no standard deviations, confidence intervals, or error bars. For claims of "consistent improvements" and large gains (e.g., +12.7% BLEU on translation, +18.4% fix rate on repair), the absence of variability measures is a significant empirical gap.

3. **Cross-task generalization results (Figure 2) are implausible without explanation.** DTERM achieves a normalized reward of 0.70 on the first unseen task while Uniform achieves 0.28 — a gap of roughly 2.5×. Since all methods are claimed to share the same policy and sub-reward components, it is unclear how reward weight differences alone could produce such a dramatic initial gap. The paper provides no explanation and does not discuss potential confounders (e.g., non-identical policy backbone, task similarity between training and test sets, reward normalization favoring DTERM). This severely undermines confidence.

4. **Two of the three claimed contributions lack any experimental evaluation.** Section 4.4 describes multi-modal task embedding fusion (Equation 10, using CLIP visual encoder) and Section 4.6 describes RLHF integration (Equation 12). Neither is tested in any experiment. The paper claims these as contributions but provides no evidence for them — they should either be evaluated or delimited as future work.

### Minor

5. **GradNorm baseline is inconsistently characterized.** The paper groups GradNorm under "static reward approaches" (line 199) while simultaneously describing it as "dynamically balances gradients during training." GradNorm is a gradient balancing method for multi-task learning, not static reward weighting. The contradiction and the mismatch between its original purpose (multi-task gradient balancing) and its application here (RL reward weighting) require justification.

6. **"Reward Machine" terminology overclaims structural formalism.** The title and framework name invoke "Reward Machines" (Icarte et al., 2022), which are finite state automata for reward functions. Section 3.5 acknowledges the implementation differs, but the term suggests a formal structure (state transitions, propositions) that DTERM does not use — it uses soft attention over learned prototype vectors. The framing is misleading.

### Trivial
None.

---

## Nice-to-Haves

- The RLHF and multi-modal extensions could be experimentally validated or explicitly scoped as future directions.
- An error analysis or case-level breakdown for the cross-task experiments would help explain the large initial gap in Figure 2.
- The paper could clarify what the 10 "unseen tasks" are and how they differ from the meta-training tasks.

---

## Removed Points

These points are flagged to be removed per policy; treat them with caution.

- **Section 6 conclusion containing unrelated text about "Dual Selfular-Acting Machine (DSAM.Mouth Rachel)":** Per review guidelines, garbled text introduced by PDF extraction is treated as a formatting artifact, not an author error. This should be verified against the original submission.
- **"(?)"-marked citations (lines 39, 47, 197):** Per guidelines, absent-reference artifacts from PDF parsing are not valid criticisms of the paper.
- **Missing related work:** Removed per policy (cannot verify from paper alone).
- **Formatting/style nitpicks:** Removed per guidelines.

---

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis confirms that the core idea is reasonable but the experimental evidence is insufficient — a gap the paper itself would need to address.

---

## Suggestions

1. Provide full experimental details: (a) the policy network architecture, (b) meta-training task composition and size, (c) explicit list of the 10 unseen tasks and how they were selected.
2. Report means and standard deviations for all tables and figures (at minimum, Tables 1 and 2, Figure 2).
3. Explain the mechanism behind the 2.5× cross-task generalization gap on the first unseen task, or rule out confounders such as differing policy backbones or data leakage.
4. Either evaluate the RLHF and multi-modal components experimentally, or clearly delimit them as future work and remove them from the claimed contributions.

---

## Score and Decision

The paper has a well-motivated core idea and clear mathematical formulation. However, the experimental evaluation is critically incomplete: the policy network is unspecified, variance is absent, the cross-task results are unexplained, and two of three claimed contributions are unevaluated. The evidence is insufficient to support the paper's claims in its current form.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>