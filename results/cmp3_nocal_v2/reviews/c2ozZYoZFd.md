## Summary

This paper presents a detailed multi-pronged case study exposing serious flaws in a high-profile ICLR 2025 Oral paper on "min-p" sampling. Through re-analysis of human evaluations, extensive NLP benchmark sweeps (requiring ~6000 A100-hours), scrutiny of LLM-as-a-Judge evaluations, and investigation of community-adoption claims, the authors show that the original paper's evidence does not support its claimed superiority for min-p. The paper contributes one genuinely novel methodological technique — a Best-of-N analysis for controlling hyperparameter tuning volume — and derives general lessons for rigorous empirical ML research.

## Strengths

- **Multi-pronged, well-documented critique with converging evidence.** The paper attacks the original claims from four independent angles (human evaluations, NLP benchmarks, LLM-as-a-Judge, community adoption), each supported with concrete evidence — public data, GitHub repositories, published tables, and author communications. The convergence of multiple independent lines of evidence makes the overall case substantially stronger than any single critique would be.

- **The Best-of-N hyperparameter-controlling analysis (Section 3) is a genuinely useful methodological contribution.** By subsampling equal numbers of hyperparameter configurations across samplers, the authors demonstrate that min-p's apparent advantage in the original paper is an artifact of unequal tuning effort. This technique is simple, intuitive, and broadly applicable for detecting cherry-picking in comparative evaluations.

- **The human evaluation re-analysis is careful and transparent (Section 2).** The authors conduct the correct statistical tests (12 one-sided paired t-tests), report results with and without Bonferroni correction, apply an Intersection-Union Test for the "consistent" superiority claim, and visualize data with confidence intervals. They also release their annotations of the qualitative responses, practicing the transparency they advocate.

- **The community adoption investigation (Section 5) documents a particularly striking finding.** The original paper claimed 54K GitHub repos and 1.1M stars — numbers that are impossible by the authors' own documentation (all major LM repos combined sum to 453K stars). These claims were retracted from the camera-ready but were cited by 3 of 4 reviewers and the Area Chair as justification for acceptance, which is a damning indictment of the review process and a genuine meta-scientific contribution.

## Weaknesses

### Fatal
None.

### Major
None. The core claims of the paper — that the original min-p paper's evidence does not support its conclusions — are well-supported by the analysis.

### Minor

1. **"Blueprint" framing overpromises relative to the content.** The title and introduction promise "a blueprint for more rigorous science," but five of the six lessons in Section 6 (apply statistical tests rigorously, demand data transparency, scrutinize qualitative summaries, ensure methodological clarity, watch for selective reporting) are standard best practices found in any research methods textbook or reproducibility checklist. Only Lesson 1 — the Best-of-N analysis for controlling hyperparameter volume — is a genuinely novel procedural contribution. The paper would be more accurately framed as "a case study demonstrating common scientific errors with one new methodological technique" rather than a full "blueprint." This does not undermine the validity of the case study itself, but the framing sets up expectations the paper does not fully meet.

2. **NLP benchmark analysis is limited to GSM8K alone.** The extensive hyperparameter sweep (9 models × 2 stages × 4 samplers × 31 temperatures × 6 hyperparameters × 3 seeds) required ~6000 A100-hours, but it covers only one task (math word problems with Chain-of-Thought). The original paper also evaluated on GPQA, and the authors do not provide a comparable sweep on that or any other task. While compute cost is acknowledged (line 150), the headline conclusion that "min-p does not outperform other samplers" is narrower than the evidence base. It remains possible that min-p has task-specific advantages (e.g., creative writing) that this analysis would not capture. The paper partially hedges ("Conclusions here are based on that evidence," line 210), but the gap between task specificity and conclusion breadth is worth noting.

3. **Abstract's strongest negative claim is slightly overbroad.** The abstract states that "min-p sampling improves neither quality, nor diversity, nor the trade-off" (line 25). This is a categorical negative that is structurally difficult to prove. The evidence supports the weaker claim — "the original paper's case for min-p's superiority is invalid; our controlled experiments find min-p is statistically indistinguishable from baselines on the tasks tested" — more strongly than the global negative. The paper's own limitation statement (line 210) appropriately hedges, but the abstract's wording does not reflect this nuance. Given that the paper criticizes others for overclaiming (Section 4.3), precision in its own claims is important.

4. **No inter-annotator reliability reported for qualitative response annotations (Section 2.3).** The paper manually annotates human evaluators' qualitative responses and visualizes preferences in Figure 2, but does not report whether multiple raters performed the annotations or what the inter-annotator agreement was. For a paper that argues for methodological rigor and transparency, this is a notable gap. If annotations were done by a single author, this should be disclosed and results treated as exploratory.

5. **Statistical power not discussed for the new human evaluation (Section 2.4).** The paper reports that min-p did not outperform baselines in the new study added by the original authors, but does not discuss whether the study had adequate statistical power to detect meaningful differences. Without a power analysis or even a reported per-condition sample size, it is impossible to distinguish between "no effect" and "insufficient data to detect an effect."

6. **Best-of-N analysis limitations not discussed.** The analysis treats hyperparameter choices as interchangeable draws, but in practice some values cover vastly different behavioral ranges (e.g., min-p p=0.01 vs. p=0.3; top-p p=0.7 vs. p=0.99). Random subsampling of N configurations may not meaningfully reflect the effective tuning effort a practitioner would invest, since some configurations are "dead zones" rarely used in practice. The paper does not discuss this limitation.

### Trivial
None.

## Nice-to-Haves

- An independent replication (or independent verification) of the LLM-as-a-Judge evaluation would strengthen this line of evidence, which currently relies on shared data from the original authors (a GitHub repository and a Telegram link).
- Formalizing the Best-of-N analysis as a standalone statistical procedure with clear assumptions and limitations would make it more portable as a methodology contribution.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Section 2.4 new human evaluation is confounded making attribution impossible"** — The paper never attributes the null result to any specific factor; it simply reports the data as additional evidence. The reviewer's criticism is directed at a claim the paper does not actually advance. The paper's interpretation — "even when the authors tried to design a study more favorable to min-p, it still didn't show superiority" — is appropriately cautious and acknowledged as fair by the reviewer. REMOVED (misreading of paper).
- **"No independent replication of LLM-as-a-Judge evaluation"** — This is inherent to the re-analysis genre; the paper uses the best available evidence. Moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The reviews largely converge on the paper's strengths and identify mostly minor framing and scope issues; no reviewer identified a structural flaw in the paper's methodology or a contradiction in its evidence that the paper itself does not already address.

## Suggestions

- Tighten the abstract's claim to match the evidence precisely, e.g., "min-p does not outperform existing samplers in the tasks and settings we tested" rather than the categorical negative.
- Either add inter-annotator agreement metrics for the qualitative annotations (Section 2.3) or clearly flag them as single-annotator exploratory analysis.
- Add a brief discussion of statistical power for the new human evaluation (Section 2.4) and a limitations paragraph for the Best-of-N analysis (Section 3) explaining that hyperparameter choices are not equally spaced in their behavioral effects.
- Consider adding at least one additional task (e.g., GPQA from the original paper) to broaden the NLP benchmark analysis, or explicitly limit the scope of the conclusion to GSM8K-type tasks.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>