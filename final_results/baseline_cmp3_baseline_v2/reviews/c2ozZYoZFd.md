## Summary

This paper presents a detailed case study of "Turning Up the Heat: MIN-P Sampling for Creative and Coherent LLM Outputs" (Nguyen et al., 2024), an ICLR 2025 Oral paper, to expose methodological flaws in empirical machine learning research. Through re-analysis of the original paper's four lines of evidence—human evaluations, NLP benchmarks, LLM-as-a-Judge evaluations, and community adoption claims—the authors demonstrate that the original conclusions are invalidated by its own data. The paper derives a blueprint for more rigorous science, including controlling for hyperparameter tuning volume, proper statistical testing, full data transparency, and scrutiny of qualitative summaries.

## Strengths

- **Timely and important contribution**: The paper addresses a genuine crisis of rigor in ML research, and the case study approach makes the abstract principles concrete and actionable. The choice of a high-visibility ICLR 2025 Oral paper as the case study amplifies the impact.

- **Thorough and systematic re-analysis**: The authors meticulously re-examine all four lines of evidence from the original paper, uncovering specific, well-documented flaws: omitted data (1/3 of human evaluation scores), incorrect statistical testing (pooling across conditions, no multiple comparison correction), selective reporting (higher score for min-p, lower for top-p in LLM-as-a-Judge), and unsubstantiated community adoption claims that were retracted.

- **Novel methodological contribution**: The "Best-of-N" hyperparameter sweep analysis (Section 3.1) is a genuinely useful methodology for fairly comparing methods that require different amounts of hyperparameter tuning. This technique could be widely adopted by the community to detect cherry-picking.

- **Reproducible and transparent**: The authors publicly released their annotations, code, and re-analysis data, practicing the transparency they advocate. The paper includes clear visualizations (Figures 1-6) that support their conclusions.

## Weaknesses

### Fatal
None.

### Major
- **The paper's own contribution is primarily negative (debunking) rather than positive (new method or theory)**. While debunking flawed work is valuable, the paper's main deliverable—a "blueprint" for rigorous science—consists of well-known best practices (control for hyperparameter tuning, correct for multiple comparisons, release data, scrutinize claims). These lessons are not novel to the ML community; they are standard in statistics and experimental design. The paper would be stronger if it offered a more novel framework or tool for detecting such issues automatically.

- **The paper does not fully address the possibility that min-p might still be useful in practice despite the flawed original evaluation.** The authors conclude that "samplers perform approximately equally if given equal hyperparameter tuning," but this conclusion is based on a limited set of benchmarks (GSM8K CoT, GPQA) and models. The paper does not explore whether min-p has advantages in other settings (e.g., creative writing, dialogue) where the original paper claimed benefits. The authors acknowledge this limitation but do not discuss its implications for the generalizability of their negative findings.

- **The paper's tone is adversarial rather than constructive in places.** While the case study approach is effective, some phrasing (e.g., "the paper's own evidence invalidates its central claim," "the authors publicly told us to focus on the high diversity setting") reads as a critique of the original authors rather than a dispassionate analysis of the science. This could undermine the paper's goal of promoting rigorous science by alienating readers who might otherwise benefit from the lessons.

### Minor
- The paper's "blueprint" lessons (Section 6) are presented as a list without prioritization or guidance on which are most critical. A more structured framework (e.g., a checklist or decision tree) would be more actionable for researchers and reviewers.

- The paper does not discuss the role of reviewers and area chairs in the original acceptance decision. Given that the original paper was an ICLR 2025 Oral, the case study implicitly critiques the review process, but the paper does not offer recommendations for improving peer review to catch such issues.

### Trivial
- The paper uses "min-p" and "min-p" inconsistently in the text (sometimes with backticks, sometimes without). This is a minor formatting issue.

## Nice-to-Haves

- A quantitative analysis of how many ICLR 2025 papers exhibit similar methodological flaws would strengthen the claim that this is a widespread problem rather than an isolated case.
- A discussion of how the blueprint could be integrated into conference review guidelines or checklists would increase practical impact.
- The paper could include a simple tool or script for detecting common statistical errors (e.g., missing multiple comparison correction) in submitted papers.

## Novel Insights

None beyond the paper's own contributions. The key insight—that controlling for hyperparameter tuning volume is critical for fair comparison—is well-illustrated but not conceptually new. The paper's main value is in the thoroughness of the case study and the concrete demonstration of how multiple methodological errors can compound to produce invalid conclusions.

## Suggestions

- Reframe the paper to focus more on the positive contribution (the Best-of-N methodology for fair comparison) and less on the adversarial case study. The case study is effective as motivation, but the paper's lasting value will be in the methodological tools it provides.
- Add a section on how the blueprint can be operationalized (e.g., a reviewer checklist, a template for reporting hyperparameter sweeps, guidelines for statistical testing in human evaluations).
- Discuss the implications for the original paper's acceptance: what should the community learn from this case about the review process, and how can future reviews be improved?

## Score and Decision

The paper makes a valuable contribution by exposing methodological flaws in a high-visibility paper and providing a concrete methodology (Best-of-N hyperparameter sweep) for fair comparison. However, the paper's main lessons are well-known best practices, and the contribution is primarily negative. The paper is well-executed and timely, but its novelty is limited. I recommend borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>