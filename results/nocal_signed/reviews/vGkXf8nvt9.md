Now let me compose the final review with the appropriate score.

## Summary

This paper introduces **Forget-to-Focus (F2F)**, a two-stage protocol that first performs targeted unlearning on a "forget set" (with an optional retain set) and then fine-tunes on a domain-specific dataset. The core idea is to suppress interfering general pretraining knowledge before specialization, rather than hoping the model learns to ignore it during fine-tuning. Experiments span five model families (0.6B–72B parameters) across coding, math, and medical domains, showing consistent improvements in pass@1/accuracy over standard fine-tuning and parameter-efficient baselines.

## Strengths

- **Novel framing of unlearning as a preparation step for domain specialization.** The paper repurposes machine unlearning — conventionally a privacy mechanism — as a deliberate intervention to suppress interfering pretraining knowledge before fine-tuning. This is a genuine conceptual shift from the dominant use of unlearning, and the motivating question is well-motivated and clearly stated in Section 1.

- **Multi-scale, multi-domain experiments spanning five model families and sizes (Qwen-0.6B, Gemma-2B, LLaMA-8B, LLaMA-13B, Qwen-72B) across three domains (coding, math, medical).** This breadth is unusual and strengthens the claim that the phenomenon is not confined to a single architecture or scale. Substantial pass@1 gains are demonstrated (e.g., Qwen-0.6B on HumanEval: 19.50 → 42.07 with GA+GD+SFT).

- **Representation analysis via CKA and SVCCA (Section 4.5).** The attempt to probe why F2F works through representational geometry is the right kind of mechanistic analysis for this paper. Figures 4 and 5 visually distinguish the representational shifts of F2F from standard fine-tuning, lending support to the claim that F2F induces different internal reorganization.

- **Forget-set quality analysis (Section 4.4, Table 3).** The comparison of BC-Select vs. BC-Mixed vs. BC-Cosine forget sets across three domains provides practical guidance on how forget-set composition affects downstream performance.

## Weaknesses

### Fatal
None.

### Major

- **Calibration improvement claimed as a contribution but entirely unsupported in the main body.** The abstract states F2F "improves calibration on medical QA tasks, reducing overconfidence," the contribution list (Section 1) repeats this, and the conclusion restates it. However, no calibration metric — no ECE, NLL, reliability diagram, confidence analysis, or even a qualitative example — appears anywhere in the paper body. This claim cannot be evaluated as presented. If calibration evidence exists in the appendix, the main body must at minimum summarize the metric used, the direction and magnitude of the effect.

- **Table 2 (Section 4.2) is confusing and appears internally inconsistent with Table 3.** Section 4.2 is titled "F2F w/ FINE-TUNING VARIANTS" but Table 2 lists only standard fine-tuning baselines (SFT, LoRA, CurlLoRA, DAPT) without any F2F rows. The Qwen-0.6B PubMedQA score for "SFT" in Table 2 (69.60) exactly matches the F2F(GA+GD)+Tuning result in Table 3 (69.60), while the SFT-only baseline from Table 3 is 62.60. For MedMCQA, Table 2 reports SFT = 11.8 while Table 3 reports F2F(GA+GD)+Tuning = 45.31 — a large, unexplained discrepancy. The medical-domain evaluation table is uninterpretable as currently presented.

- **No variance or statistical significance reported for any result.** Every number in Tables 1–3 is a single point estimate. The forget set for the smallest model is only 100 samples (Section 4.1), and the retain set is 1,000 samples — results could be highly sensitive to which specific samples are chosen. Without error bars, confidence intervals, or at minimum a description of how many random seeds were used and whether results are stable across them, the reader cannot assess the reliability of the reported gains.

### Minor

- **Fisher information and PCA-shift analyses are listed as contributions in Section 1** ("Using centered kernel alignment (CKA), SVCCA, Fisher information, PCA-shift analyses") but are not discussed or presented anywhere in the main body. Only CKA and SVCCA appear in Section 4.5. If these analyses exist in the appendix, the main body should at least summarize their key findings.

- **The choice of BookCorpus as the forget set (the proxy for "interfering general pretraining knowledge") is under-motivated.** The pretraining corpora for Qwen, LLaMA, and Gemma include web text, code, scientific papers, and many other sources far beyond book text. The paper provides limited justification for why unlearning BookCorpus text specifically removes knowledge that interferes with coding, math, or medical tasks. The BC-Select and BC-Cosine curation strategies partially address this, but the foundational choice of BookCorpus itself is not justified.

- **The conclusion does not discuss limitations or failure cases** despite the paper's own evidence of catastrophic performance drops (e.g., GA-only unlearning reduces LLaMA-8B HumanEval to 1.20, and Gemma-2B exhibits fragile behavior under unlearning). A balanced discussion of these boundary conditions would strengthen the paper.

### Trivial

- **The theoretical analysis (Proposition and Corollary, Section 2)** uses a convex linear surrogate with strong assumptions that are acknowledged not to hold for LLMs. While the theory provides useful intuition about the contraction effect, no attempt is made to connect it to the experimental setting. This limits its contribution but does not undermine the empirical findings.

- **The unlearning hyperparameter T_u (number of unlearning steps)** is mentioned in the protocol description but not reported in Section 3.4 for any model or configuration, which affects reproducibility.

- **Asymmetric training epochs** (Qwen-0.6B: 8 epochs; all other models: 1 epoch). The paper states this is intentional to avoid overfitting, but it prevents clean across-scale comparison of F2F's relative benefit.

- **Inconsistent naming for Qwen versions:** text references both "Qwen-2 72B-Instruct" and "Qwen-3-0.6B" while tables use "Qwen 72B" and "Qwen 0.6B". Clarity on which version was used matters for reproducibility.

## Nice-to-Haves

- **CKA control with random perturbation:** Adding a comparison where the "unlearning" step is replaced by gradient descent on random noise or a held-out irrelevant dataset would help distinguish whether F2F's benefit comes from the specific *direction* of forgetting (suppressing interfering features) rather than just any perturbation of the initialization.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **CKA missing comparison with randomly perturbed initialization:** Reasonable experimental control but a nice-to-have addition, not a flaw in the existing analysis. The paper already compares F2F against multiple strong baselines.
- **Abstract percentage clarity:** The 32.5% / 11.95% figures are clear in context as relative improvements. Minor presentation preference.
- **Gemma-2B SFT degradation not deeply investigated:** The paper acknowledges this observation (observation 4, Section 4.1). Deeper investigation would be nice but its absence is a scope limitation.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Either provide calibration metrics** (ECE, NLL, reliability diagrams) in the main body for the medical QA tasks, or retract all calibration claims from the abstract, contribution list, and conclusion.
2. **Reconcile Table 2 with Table 3:** clarify whether Table 2 reports baseline fine-tuning methods or F2F-enhanced results, and explain the large discrepancy in MedMCQA numbers (11.8 vs. 45.31).
3. **Add variance information** (error bars or confidence intervals) to the main result tables, or at minimum report the number of random seeds and confirm result stability.
4. **Summarize Fisher information and PCA-shift findings** in the main body if they appear in the appendix.
5. **Report T_u** (number of unlearning steps) for each configuration.
6. **Justify the BookCorpus choice** more explicitly, or include an ablation using forget sets from other general-domain sources.
7. **Discuss limitations and failure cases** in the conclusion (e.g., conditions under which F2F degrades performance).

## Score and Decision

The paper asks a genuinely interesting question and pursues it across an admirably broad set of models and domains. The core evidence for F2F's accuracy benefits in coding (Table 1) and across domains (Table 3) is substantive and consistent. However, three major issues prevent unconditional acceptance: (1) a central claimed contribution (calibration improvement) has zero supporting evidence in the main body; (2) the main medical-domain evaluation table (Table 2) is internally inconsistent with Table 3; and (3) no variance information is reported anywhere, which is especially concerning given the small forget-set sizes. These issues are fixable — providing or retracting calibration evidence, clarifying Table 2, and adding variance information — but they must be addressed.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>