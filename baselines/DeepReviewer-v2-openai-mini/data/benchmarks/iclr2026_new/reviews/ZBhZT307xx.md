## Summary
# Final Review Report

## Summary

This paper presents a systematic empirical study of verifier reliability in reinforcement learning with verifiable reward (RLVR) for mathematical reasoning. The authors evaluate both rule-based and model-based verifiers across static classification accuracy and dynamic RL training dynamics. The key findings are: (1) rule-based verifiers achieve near-perfect precision (>99%) but suffer from low recall (86% on average), with false negative rates increasing as policy models become stronger; (2) a hybrid verifier (rule-based + model-based) improves RL training accuracy by up to 2.3 points over rule-based alone; (3) model-based verifiers fine-tuned on classification data become more susceptible to reward hacking during RL training despite higher static accuracy; and (4) all generative verifiers are vulnerable to simple adversarial patterns, while discriminative verifiers are more robust.

The paper addresses an important and timely topic—verifier reliability is critical for scaling RL-based reasoning systems. The empirical analysis is broad in scope, covering multiple datasets, verifier types, and evaluation paradigms. However, several methodological limitations reduce confidence in the quantitative findings: single-run RL experiments without variance estimation, reliance on GPT-4o as an unvalidated oracle for ground-truth construction, and a probing study with limited sample size (N=471). The paper is primarily diagnostic and does not propose or evaluate any robustness-enhancing methods, making the title's "From Accuracy to Robustness" framing somewhat misleading. Despite these limitations, the paper provides valuable empirical evidence documenting the accuracy-robustness tension in verifier design, which should inform future work in this rapidly developing area.

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: Verifier reliability for RLVR in math reasoning]
    |
    ├── [C1: Rule-based verifiers have low recall (86%)]
    │       └── Evidence: Static evaluation on 8K examples, 3 verifiers, 4 datasets
    │       └── Gap: No variance/CI reported; GPT-4o oracle unvalidated in main text
    │
    ├── [C2: Model-based verifiers improve recall but enable reward hacking]
    │       ├── Evidence: Hybrid verifier +2.3 pts on RL benchmark average
    │       └── Evidence: R1-Distill-Verifier-1.5B shows training-reward divergence at ~450 iters
    │       └── Gap: Single-run RL experiments; cause of fine-tuning→hackability link unexplored
    │
    └── [C3: Generative verifiers universally vulnerable to adversarial patterns]
            └── Evidence: 13 attack patterns on 471 samples, multiple verifiers
            └── Gap: Small sample; static attacks only (not adaptive); no CI reported
```

## Strengths
**S1. Timely and practically important research question.** The paper addresses a critical gap in the RLVR pipeline: verifier reliability. As LLM reasoning systems (DeepSeek-R1, Kimi-k1.5) increasingly rely on RL with verifiable rewards, understanding verifier limitations is essential for scalable and trustworthy training. The paper identifies and documents a concrete accuracy-robustness tension that is directly relevant to ongoing research.

**S2. Broad empirical scope.** The evaluation covers multiple dimensions: three rule-based verifier implementations, multiple model-based verifiers (general-purpose and fine-tuned), four math datasets plus a general science dataset, and both static classification and dynamic RL training paradigms. This breadth strengthens the generalizability of the core findings.

**S3. Clear demonstration of the classification-RL mismatch.** The key empirical finding—that fine-tuned verifiers with higher static accuracy become more susceptible to reward hacking during RL training—is counterintuitive and important. The oracle reward analysis (Figure 3) provides compelling visual evidence of training-reward divergence for R1-Distill-Verifier-1.5B, which supports the central claim.

**S4. Systematic adversarial probing methodology.** The construction of 13 hacking pattern types and evaluation across multiple verifiers (Section 6) provides a useful template for robustness evaluation. The finding that discriminative verifiers (xVerify) are substantially more robust than generative verifiers is actionable and contributes to understanding the relationship between CoT faithfulness and adversarial vulnerability.

**S5. Transparent handling of known limitations.** The paper correctly identifies the hybrid verifier design choice and acknowledges that the probing study reveals vulnerabilities without immediate defense solutions. The admission that the evaluation datasets "already represent a relatively easy setting for verification" (Section 3.1) demonstrates appropriate scope awareness.

**S6. Reproducibility-friendly experimental design.** The use of publicly available models (Qwen2.5, DeepSeek-R1-Distill), open-source verifier implementations (Verl, HuggingFace Math Verifier, Qwen-Math Verifier), and standard benchmarks facilitates reproduction and extension by the community.

## Weaknesses
**W1. [CRITICAL] Single-run RL experiments without variance estimation (Page 5 — Section 4.2, Figure 3 caption).** All RL training results are reported from single runs with the explicit caveat "All benchmarks are reported with a single sample due to computational constraints." This is a fundamental methodological limitation. GRPO-based training is known to exhibit seed-to-seed variance in math reasoning tasks. Without multi-seed reporting, readers cannot assess whether the key 2.3-point improvement (55.0 to 57.3) is statistically reliable or within the noise range. The "best result from each run" reporting style (Table 2 caption) further raises cherry-picking concerns. **Impact:** The paper's central quantitative claims about hybrid verifier effectiveness rest on unverifiable statistical ground. **Required action:** Report all key RL results as mean ± std over at least 3 independent training seeds. If computational constraints are prohibitive, provide seed-sensitivity analysis on a subset of configurations and explicitly bound the confidence intervals.

**W2. [MAJOR] GPT-4o as ground-truth oracle without sufficient validation disclosure (Page 1—Section 3.1; Page 7—Section 5.2).** The paper uses GPT-4o as the oracle for constructing the 8,000-example static evaluation dataset and for computing oracle rewards during RL training. This creates a circular dependency: the evaluation of verifier accuracy depends on the accuracy of another LLM which may share systematic biases with the verifiers being evaluated. Human validation is relegated to Appendix B without key statistics (agreement rate, Cohen's kappa, disagreement pattern analysis) in the main text. **Impact:** The absolute recall/precision numbers throughout the paper are contingent on GPT-4o's judgment, which is not established as an unbiased ground truth. **Required action:** Move the key human-GPT-4o agreement statistics to the main text, including per-subset breakdowns. Additionally, conduct a sensitivity analysis using an alternative oracle (e.g., human rating on a 200-example subset) to bound potential oracle bias.

**W3. [MAJOR] Title and framing overstate the contribution scope (Title, Abstract, Conclusion).** The title "From Accuracy to Robustness" implies a transition from diagnosing accuracy problems to providing robustness solutions. However, the paper is almost entirely diagnostic: it identifies verifier limitations, demonstrates reward hacking, and probes adversarial vulnerabilities, but does not propose, implement, or evaluate any robustness-enhancing method. The abstract and conclusion likewise frame the work as a "comprehensive analysis" (accurate) rather than a solution-oriented contribution. **Impact:** Readers and reviewers may perceive a mismatch between the claimed contribution arc and the actual deliverable. **Required action:** Revise the title and framing to accurately reflect the diagnostic nature of the contribution. Suggested alternative title: "Diagnosing Verifier Failures in RL for Mathematical Reasoning: Accuracy Limitations and Adversarial Vulnerabilities."

**W4. [MAJOR] Discussion and Limitations sections are critically underdeveloped (Page 9).** The Discussion (Section 7) is a single paragraph that merely restates findings without synthesis, design recommendations, or a research agenda. The Limitations section is one sentence. This is inadequate for a paper that identifies important but unresolved problems. Missing elements include: (a) no discussion of why fine-tuning increases hackability (mechanism hypothesis), (b) no connection to broader RL safety literature, (c) no proposed evaluation protocol for verifier robustness, and (d) no discussion of the accuracy-robustness trade-off as potential fundamental tension. **Impact:** The paper reads as an unfinished empirical report rather than a self-contained research contribution. **Required action:** Expand Discussion to at least 3 paragraphs covering synthesis, mechanistic hypotheses, and a concrete research agenda. Expand Limitations to 4-5 specific constraints as detailed in the PDF annotation.

**W5. [MAJOR] Model-based verifier evaluation uses a conditional subset without clear disclaimers (Page 3 — Table 1, Section 3.3).** The evaluation of model-based verifiers is performed exclusively on the subset of examples that the HuggingFace Math Verifier classified as incorrect. This means all precision/recall metrics in Table 1 are conditional on this filtered subset, not representative of the full data distribution. While the paper acknowledges this design choice, the Table 1 caption and surrounding text do not clearly communicate that these are conditional metrics. **Impact:** Readers may misinterpret the absolute performance numbers (e.g., "general-verifier achieves 0.90/0.86 precision/recall") as general-purpose performance rather than hard-subset performance. **Required action:** Add explicit notation in Table 1 that all metrics are "conditional on HF-verifier-incorrect subset" and discuss how this selection bias affects interpretation.

**W6. [MAJOR] Hybrid verifier false-positive risk is unexamined (Page 5 — Section 4.1).** The hybrid verifier design achieves recall improvement but does not analyze the false-positive risk introduced by the model-based component. Since the rule-based verifier has >99% precision, all new false positives come from the model-based verifier's errors on the filtered subset (where model-based precision ranges from 0.66 to 0.90). These false-positive rewards could harm RL training dynamics, but this is not analyzed or discussed. **Impact:** The paper's recommendation to use hybrid verifiers may be premature without understanding the false-positive cost. **Required action:** Add an analysis quantifying the false-positive rate introduced by the hybrid design and discuss its potential impact on RL training stability.

**W7. [MAJOR] Naming inconsistency between trained and untrained verifiers causes confusion (Page 7 — Section 5.2).** The text states "In contrast, the untrained verifier, R1-Distill-Verifier-1.5B, and the rule-based verifier do not exhibit such instability." R1-Distill-Verifier-1.5B is explicitly described as a fine-tuned verifier (Section 5.1), making the phrase "untrained verifier, R1-Distill-Verifier-1.5B" contradictory. The intended reference is likely to DeepSeek-R1-Distill-Qwen-1.5B (the base model). This naming confusion affects Figure 3, Table 2, and Table 3. **Impact:** Readers cannot reliably distinguish which model is the trained vs. untrained variant, undermining a core comparison in the paper. **Required action:** Audit all model name references throughout the paper, use distinct and consistent names (e.g., "DS-R1-Distill-Qwen-1.5B" for the base model and "R1-Distill-Verifier-1.5B" for the fine-tuned variant), and add a nomenclature table in the appendix.

**W8. [MAJOR] Adversarial probing study has limited sample size and no confidence intervals (Page 8 — Section 6).** The probing study uses approximately 471 samples with 13 attack patterns. For rare events (e.g., xVerify at 0.0-0.4% success rate), this sample size yields wide confidence intervals—the difference between 0% and a non-zero low rate is statistically indistinguishable at N=471. No confidence intervals or bootstrapped estimates are reported for any attack success rate in Table 3. **Impact:** Readers cannot assess the reliability of the reported attack success rates, particularly for fine-grained comparisons between verifiers. **Required action:** Add bootstrapped 95% confidence intervals to all attack success rates in Table 3. Acknowledge that static (non-adaptive) attacks likely underestimate true vulnerability.

**W9. [MODERATE] Unexamined causal mechanism for fine-tuning→hackability link (Page 7 — Section 5.1).** The paper observes that fine-tuned verifiers become more hackable but does not investigate why. The rejection fine-tuning applied to R1-Distill-Verifier-1.5B specifically targets CoT verbosity reduction ("reduce overthinking"). If CoT faithfulness is a defense mechanism (as Section 6.2 suggests), then training for shorter CoT may directly undermine robustness. This potential causal pathway is neither discussed nor tested. **Impact:** The paper misses an opportunity to provide mechanistic insight beyond the observational finding. **Required action:** Add a paragraph analyzing the relationship between CoT characteristics and adversarial robustness, ideally with a comparison of CoT length and content between robust (xVerify) and vulnerable (R1-Distill-Verifier) verifiers.

**W10. [MODERATE] Abstract and introduction lack explicit research gap statement (Page 1 — Introduction).** The introduction begins with a generic description of RL's success before gradually narrowing to verifier limitations. A clearer problem-driven opening would strengthen the motivation: readers should understand within the first paragraph why verifier reliability is a critical gap that, if unaddressed, limits the field's progress. **Required action:** Restructure the first two paragraphs to establish the verifier reliability problem before reviewing RL's successes, as detailed in the PDF annotations.

## Score
**Final Score: 5.5/10**

**Scoring rationale:**

The paper addresses a timely and practically important question—verifier reliability in RLVR for mathematical reasoning—and provides broad empirical documentation of verifier limitations across multiple dimensions (static accuracy, RL training dynamics, adversarial robustness). The core findings (rule-based verifiers have low recall; fine-tuned model-based verifiers become more hackable; generative verifiers are universally vulnerable) are useful for the community.

However, the score is constrained by several critical methodological weaknesses that limit confidence in the quantitative conclusions:

1. **Statistical reliability is unverifiable.** All RL results come from single training runs with no variance estimation. The paper's central quantitative claim (2.3-point improvement from hybrid verifier) cannot be assessed for statistical significance. This is a must-fix issue.

2. **Evaluation foundation depends on an unvalidated oracle.** GPT-4o serves as the ground-truth for both static evaluation and RL oracle rewards without sufficient validation statistics in the main text. This creates circularity concerns.

3. **The paper is diagnostic only.** Despite the "From Accuracy to Robustness" framing, the paper does not propose or evaluate any robustness solution. The contribution is limited to problem identification.

4. **Key analyses are incomplete.** The fine-tuning→hackability causal mechanism is unexplored. The hybrid verifier's false-positive cost is unquantified. The Discussion and Limitations sections are critically underdeveloped.

5. **Naming inconsistencies** between trained and untrained verifiers create confusion around a core comparison.

The paper has clear value as a diagnostic empirical study that documents important verifier failure modes. With the required revisions—particularly multi-seed RL experiments, expanded Discussion/Limitations, clearer evaluation framing, and resolution of naming issues—the work could become a solid contribution at the 6.5-7.0 level. In its current form, the methodological limitations prevent confident interpretation of the quantitative findings.

```text
ASCII Diagram — Revision Strategy Roadmap

[Problem]                                         [Fix]                                          [Expected Gain]
W1: Single-run RL results               →   Multi-seed (≥3) with μ±σ                 →   Statistical reliability
W2: GPT-4o oracle without validation     →   Move human-agreement stats to main text   →   Foundation credibility  
W3: Overclaimed "robustness" framing     →   Title → diagnostic/audit framing          →   Honest contribution scope
W4: Underdeveloped Discussion/Limitations → 3+ para Discussion + 5-point Limitations  →   Self-contained paper
W5: Conditional metrics without disclaimer → Clarify Table 1 as "hard-subset only"     →   Correct interpretation
W6: Hybrid verifier FP risk unanalyzed    →   Add FP rate analysis                      →   Complete trade-off picture
W7: Naming confusion                      →   Consistent model names + nomenclature    →   Readability + precision
W8: Probing without CI                   →   Bootstrap CIs on attack success rates     →   Statistical grounding
W9: Unexamined causal mechanism          →   CoT faithfulness analysis                  →   Mechanistic insight
W10: Weak research gap statement         →   Problem-driven intro rewrite              →   Stronger motivation
```