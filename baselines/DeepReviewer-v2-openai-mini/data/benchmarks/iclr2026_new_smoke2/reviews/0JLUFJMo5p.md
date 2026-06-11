## Summary
# Final Review Report

## Summary

This paper introduces Dynamic Task-Embedded Reward Machine (DTERM), a framework that uses hypernetwork-generated weights conditioned on task embeddings to dynamically compose reward components for reinforcement learning in code generation tasks. The key idea is to replace fixed-weight reward functions with an adaptive mechanism that can adjust the importance of syntactic correctness, functional correctness, code style, and efficiency based on the task description. The framework combines a transformer-based task embedding encoder (CodeBERT), a hypernetwork weight generator, and a modular reward decomposer with FiLM modulation and prototype-based adaptation.

The paper addresses a genuine practical challenge: different code generation tasks (translation, completion, repair) require different trade-offs between reward criteria, and manual tuning of these trade-offs does not scale. The proposed architecture is technically coherent, and the reported results show consistent improvements over static-weight baselines across four benchmarks.

However, the manuscript has severe presentation and rigor issues that undermine its scientific credibility. The Conclusion section contains completely corrupted/placeholder text unrelated to the paper. Multiple key components (multi-modal fusion in Sec 4.4, RLHF integration in Sec 4.6) are presented as part of the framework but never tested. Quantitative results lack variance reporting and statistical significance. Two placeholder citations "(?)" appear in the related work. Several claims are overstated relative to the evidence. The writing quality is inconsistent, with grammatical errors and garbled sentences throughout.

Due to Retrieval-Disabled Mode (external paper search unavailable), novelty verification is deferred; all contribution claims (C1: task-aware reward modeling, C2: hypernetwork-task embedding integration for zero-shot adaptation, C3: compiler feedback integration) cannot be independently assessed against prior work in this review.

## Strengths
1. **Well-Motivated Problem:** The paper addresses an important and practical challenge in RL-based code generation — the need for task-adaptive reward composition. The observation that different coding tasks (translation, repair, completion) require different trade-offs between compilation correctness, functional accuracy, and efficiency is valid and practically relevant. The motivation is clear and compelling.

2. **Technically Coherent Architecture:** The DTERM framework integrates several existing techniques (hypernetworks, task embeddings, FiLM modulation, prototype attention) into a unified reward composition pipeline. The modular design — task embedding → hypernetwork weighting → sub-reward computation → policy optimization — is logically structured. The use of hypernetworks to generate reward weights from task embeddings is a sensible approach to the stated problem.

3. **Comprehensive Benchmark Coverage:** The evaluation covers four distinct code-related benchmarks (CodeXGLUE, APPS, DeepFix, HumanEval) spanning summarization, translation, completion, repair, and competitive programming. This provides reasonable task diversity for an initial evaluation. The ablation study isolates key components (hypernetwork, task embedding, FiLM, compiler feedback).

4. **Consistent Empirical Trends:** Across all five tasks in Table 1, DTERM outperforms all three baselines (Uniform, Expert-Tuned, GradNorm). The cross-task generalization results in Figure 2 show a consistent upward trend for DTERM across 10 unseen tasks, while baselines plateau or degrade. These trends, while lacking statistical rigor, suggest the approach has genuine merit.

5. **Dynamic Reward Analysis:** Figure 3 provides useful insight into how DTERM adjusts reward weights across task types. The variation in learned weight distributions (e.g., compilation success weighted higher for repair vs. translation) provides interpretable evidence that the hypernetwork is learning meaningful task-dependent reward compositions.

## Weaknesses
### Critical

**W1. Corrupted Conclusion (Severity: Critical)**
The Conclusion section (Page 8) contains text completely unrelated to the paper: "The Dual Selfular-Acting Machine (DSAM.Mouth Rachel) A new method for analyzing the dual selfular acting machine (DSAM), a generative text model architecture akin to one employed by ChatGPT." This appears to be a placeholder or corrupted section mistakenly included. Section 7 ("The Use of LLM") is similarly unprofessional — a single sentence "We use LLM polish writing based on our original paper" without any detail about how LLMs were used, which model, or what safeguards were employed. The conclusion is the reader's final takeaway; having corrupted text here is a catastrophic presentation error. **Fix:** Completely rewrite the Conclusion to summarize validated findings, acknowledge limitations, and suggest future work. Either expand Section 7 into a proper ethics/acknowledgment statement or remove it.

### Major

**W2. Missing Variance and Statistical Significance Reporting (Severity: Major)**
Despite stating "3 random seeds" in the implementation details, all quantitative results in Table 1, Table 2, Figure 2, and Figure 4 are reported without standard deviations, confidence intervals, or significance tests. Key claims such as "+12.7% BLEU in translation" and "+18.4% fix rate in repair" cannot be assessed for statistical reliability. With code generation metrics known to exhibit variance across seeds, single-point estimates are insufficient to support the paper's conclusions. **Fix:** Report mean ± std over 3 seeds for all numerical results. Add error bars to Figure 2 and Figure 4. For headline improvement claims, perform paired significance tests or hedge the language.

**W3. Ablation Study Underspecified (Severity: Major)**
The ablation study (Table 2, Page 7) lacks descriptions of what each ablation configuration actually entails (e.g., what "w/o Hypernetwork" means — static learned weights? random weights? uniform weights?). The study is only performed on HumanEval (Pass@1), not across the four benchmarks used in the main evaluation. The text claims a "15% performance drop" from replacing CodeBERT with bag-of-words embeddings, but the bag-of-words result is not reported in the table and the claim is unverifiable. Variance is also missing. **Fix:** Add full ablation descriptions, report results on at least 2-3 benchmarks, include std, and add the missing bag-of-words comparison to the table.

**W4. Untested Components Presented as Core Framework (Severity: Major)**
Two significant components are presented as integral to DTERM but are never evaluated:
- **Multi-modal fusion (Sec 4.4):** Eq. (10) integrates CLIP visual encoder for multi-modal task specifications, yet all experiments use text-only benchmarks. No multi-modal evaluation is performed.
- **RLHF integration (Sec 4.6):** Eq. (12) introduces a human preference component, but no human evaluation, RLHF dataset, or preference-based experiment is conducted. The section also contains garbled text ("Bat var 'Learning from choice of model (RLHF)...'").
Presenting untested components inflates the claimed contribution scope and misleads readers. **Fix:** Either remove these sections (deferring to future work) or add corresponding experiments. Fix garbled text in Sec 4.6.

**W5. Placeholder Citations "(?)" in Related Work (Severity: Major)**
Two sections contain placeholder citations marked "(?)": Section 2.3 (hypernetworks for reward function generation — cited as the "closest to our work") and Section 2.5 (constrained optimization for RLHF). Since these are presented as directly relevant prior work, missing references prevent reviewers from assessing novelty claims. **Fix:** Replace with proper citations or remove the claims that depend on them.

**W6. Overstated Contribution Claims (Severity: Major)**
Three contribution statements in the Introduction lack appropriate scope boundaries:
- C1 claims "removing the need for manual reward engineering" — the framework still requires defining sub-reward components, training the hypernetwork, and selecting hyperparameters like λ.
- C2 claims "zero-shot adaptation to unseen coding tasks" — the cross-task evaluation uses tasks within the same benchmark families, not fundamentally different task types.
- C3 claims to "bridge the gap between formal program verification and formal schematic models of reward" — this is vague and not operationalized in experiments.
**Fix:** Bound all claims to what is actually evidenced. Replace absolute statements with scoped wording (e.g., "reduces the need for manual tuning" rather than "removing the need").

**W7. Logical Contradiction in Qualitative Evaluation (Severity: Major)**
Section 5.6 states that DTERM can make "fine-grained trade-offs as a function of understanding the task — an ability inherent to static approaches." The phrase "inherent to static approaches" directly contradicts the paper's central premise that static (fixed-weight) approaches cannot make such trade-offs. This appears to be a typo (likely intended: "superior to" or "absent from" static approaches), but as written it undermines the core thesis. **Fix:** Correct the wording and expand the qualitative evaluation with multiple systematic examples and quantitative support.

**W8. Insufficient Baseline Comparisons (Severity: Major)**
The paper only compares against three baselines (Uniform, Expert-Tuned, GradNorm). Important missing comparisons include: (a) learned but task-independent reward weighting, (b) meta-learned reward functions without hypernetworks, (c) Bayesian optimization of reward weights, and (d) multi-objective RL approaches that directly handle trade-offs. Without these, it is unclear whether DTERM's improvement comes specifically from the hypernetwork-task embedding mechanism or from having any adaptive reward at all. **Fix:** Add at least one ablation that ablates only the hypernetwork (static learned weights) and one that uses a simpler adaptive mechanism (e.g., linear projection without prototypes) to isolate the benefit of each design choice.

### Minor

**W9. Writing Quality and Grammatical Errors**
The manuscript contains numerous grammatical issues: "their revolutionization" (ungrammatical), "populary" (likely misspelling), "Bat var" (garbled), "The Combination of these concepts is what drafted our theoretical structure" (awkward). These issues reduce reader confidence and should be corrected throughout.

**W10. Hypernetwork Terminology Mismatch**
The "hypernetwork" in Eq. (5) implements a linear projection + softmax, which is a standard differentiable weighting mechanism, not a hypernetwork in the sense of Ha et al. (2016) where one network generates parameters for another. The paper should clarify whether the hypernetwork refers to the weight generation process as a whole (including the prototype mechanism) or just the linear layer.

**W11. Missing Hyperparameter Reporting**
Several critical hyperparameters are not reported: λ (decay rate in Eq. 11), number of prototypes m (Eq. 8), number of FiLM layers, PPO clipping parameter, and training steps/episodes. These are needed for reproducibility.

**W12. Section 7 ("The Use of LLM") Is Inadequate**
A single sentence stating "We use LLM polish writing based on our original paper" does not meet the disclosure standards of top-tier venues. The authors should specify which LLM was used, for which parts of the text, and what verification was performed.

### Deferred Concerns (Require Manual Literature Verification)

Due to Retrieval-Disabled Mode, novelty and comparison conclusions are deferred. The following issues should be manually verified by the authors/reviewers:
- Whether hypernetwork-based reward generation for code has been previously proposed (cited as "(?)" in Sec 2.3).
- Whether "task embeddings for reward adaptation" overlaps with Task2vec (Achille et al., 2019) beyond surface-level use of the term.
- Whether CodeRL (Le et al., 2022) or related methods already incorporate task-adaptive reward elements.
- Whether DTERM's claimed "zero-shot adaptation" to unseen tasks has been demonstrated in prior multi-task RL for code generation.

## Score
**Final Score: 4/10**

**Rationale:**
The score reflects the manuscript's current state, prioritizing research value, novelty, and validity as primary dimensions.

- **Research Value (2/3):** The problem of task-adaptive reward composition in RL-based code generation is well-motivated and practically relevant. However, the presented evidence is insufficient to establish the claimed value. Key components remain untested, comparisons are limited, and the empirical foundation lacks statistical rigor.

- **Novelty (Pending):** Due to Retrieval-Disabled Mode, novelty cannot be independently assessed. The conceptual integration of hypernetworks with task embeddings for reward weighting appears technically novel within the scope presented, but the degree of overlap with prior work (particularly the unreferenced "(?)" papers) is unknown. **Novelty verification is deferred and requires manual literature review.**

- **Validity/Soundness (1/4):** The paper has a critical presentation error (corrupted conclusion), missing variance reporting, underspecified ablation studies, and untested components presented as core contributions. These issues collectively weaken confidence in all reported results. Without standard deviations, significance tests, or properly described ablation configurations, the empirical claims are not verifiable.

- **Reproducibility (1/3):** Insufficient hyperparameter reporting, missing implementation details (λ, number of prototypes, training steps), and placeholder citations make reproduction difficult. The garbled text and ungrammatical sections further reduce reproducibility.

The paper has a promising core idea and shows consistent directional improvements, but the current execution and presentation fall substantially short of the standards required for publication. A major revision addressing the critical and major issues — particularly the corrupted conclusion, missing statistics, and verification of untested components — is necessary before the work can be fairly evaluated.

**Post-Revision Target: 6/10** (achievable if all major issues are addressed: proper evaluations, statistical reporting, fixed conclusion, and either removed or validated untested components).