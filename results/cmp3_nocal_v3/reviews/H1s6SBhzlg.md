## Summary

This paper studies how to aggregate answers from multiple LLMs beyond simple majority voting. It introduces two principled algorithms: Optimal Weight (OW), a Bayes-optimal linear aggregator using first-order information (model accuracies), and Inverse Surprising Popularity (ISP), which leverages second-order information (answer correlations) and is shown to provably dominate both majority voting and the standard Surprisingly Popular rule in terms of expected advantage. The paper provides theoretical analysis (Bayesian optimality of OW, advantage ordering of ISP > MV > SP, and a finite-sample bound), validates on synthetic data, and demonstrates consistent improvements over majority voting on UltraFeedback, MMLU, and a real-world healthcare dataset (ARMMAN).

## Strengths

1. **Clean theoretical grounding.** The paper connects LLM response aggregation to the formal information aggregation literature (Austen-Smith & Banks, Prelec et al.) and provides a principled Bayesian model with random shuffling pre-processing (Proposition 1) that yields clean symmetry properties enabling closed-form analysis.

2. **Bayesian optimality of OW (Theorem 1).** The result that a weighted linear aggregator with inverse-logistic weights is Bayes-optimal among *all* aggregators (not just linear ones) under conditional independence is the paper's strongest theoretical contribution. It is a nontrivial finding that gives a principled answer to "what weights should I use if I know each model's accuracy?"

3. **Novelty and motivation of ISP.** The inverse variant of the surprisingly popular rule (Section 4.2) is well-motivated: the paper identifies why standard SP underperforms MV in LLM settings (less systematic bias than in human crowds) and designs ISP as a principled correction. The derivation from Equations (3)–(4) shows clear reasoning from first principles.

4. **Practical methods for unsupervised settings.** OW-L (ERM-based accuracy estimation from second-order information) and OW-I (using ISP predictions as pseudo-labels) provide practical ways to apply the theoretically optimal OW scheme when ground-truth labels are unavailable, bridging theory and practice.

5. **Breadth of evaluation.** Experiments cover synthetic data (validating the theory under controlled conditions), two standard LLM benchmarks (UltraFeedback, MMLU), and a real-world healthcare dataset (ARMMAN).

## Weaknesses

### Fatal
None.

### Major

1. **The advantage-accuracy gap in Theorems 2 and 3.** Theorem 2 proves that ISP achieves a higher *expected advantage* for the correct label than MV, and MV higher than SP: 𝔼[Adv_ISP(s\*)] ≥ 𝔼[Adv_MV(s\*)] ≥ 𝔼[Adv_SP(s\*)]. The paper then describes this as ISP "outperforming" MV (line 207) and, in the abstract and introduction, as "leading to more reliable collective decisions" and "provably has an advantage over majority voting." However, the selection rule is argmax_s Adv(s), and a higher expected Adv(s\*) does not strictly imply a higher probability that s\* is the argmax—two distributions over advantages can differ in mean but also in variance, potentially reversing accuracy ordering. The paper argues on line 205 that "effective aggregation requires the correct label s\* to attain the largest advantage," which is a necessary condition but not a sufficient link between expected-advantage comparisons and accuracy comparisons. The experiments do validate ISP > MV in actual accuracy, but the theorems prove something weaker than what the text suggests. The authors should either prove the accuracy implication (which may be provable given the sum-zero structure of the advantage functions and the shuffling symmetry) or explicitly qualify the theoretical claims.

2. **Unexplained identical performance of OW-L and OW-I.** In Tables 3 and 4, OW-L and OW-I achieve *exactly* the same accuracy (73.66%, 90.37%, 85.78%) and identical per-question discrepancy counts (2545/1727, 1821/659, 264/195) across all three real-world datasets. These are two distinct methods—OW-L uses ERM to learn accuracies from second-order information (Equation 7), while OW-I uses ISP predictions as pseudo-labels to estimate accuracies. Even if both produce similar accuracy estimates, differences in weight computation could yield different aggregate predictions on individual questions. The paper does not discuss this, and the identity of results across diverse datasets is unexplained. This undermines confidence in whether the two methods are meaningfully different or whether one of them may be inadvertently equivalent to the other due to the specific model set or data characteristics.

### Minor

3. **No uncertainty quantification in main results.** Table 3 reports only point estimates—no standard deviations, confidence intervals, or error bars. The t-statistics reported (line 303) come from per-question comparison counts, not from the overall accuracy metric. For comparative claims with modest absolute gains (0.54–1.45 percentage points), the absence of uncertainty reporting makes it difficult to assess whether improvements are stable across random seeds or question splits.

4. **Reliance on the conditional independence assumption (Assumption 1).** All core theoretical results (Theorems 1–3, Proposition 2) depend on this assumption. The paper acknowledges it "may not hold perfectly in the LLM setting, especially when questions vary in difficulty" (line 63) and states extensions appear in Appendix C. While standard in the literature, LLMs trained on overlapping data will have correlated errors, especially on difficult questions. The practical scope of the theoretical guarantees is therefore narrower than the paper's framing suggests.

5. **The option-ordering assumption (line 51).** The paper assumes LLM outputs are unaffected by option ordering, citing one reference (Guo & Vosoughi, 2024). This is known to degrade for smaller models—exactly the types included in the experiments (e.g., Llama3.2-1B, Qwen2.5-3B). The random shuffling pre-processing (Proposition 1) depends on this assumption holding, so any position bias in weaker models could compromise the theoretical guarantees in practice.

### Trivial
None.

## Nice-to-Haves

- **Characterize failure modes.** The paper reports win counts (Table 4) but does not analyze the questions where ISP or OW underperforms MV. Understanding when the methods fail would guide practitioners.
- **Ablation of random shuffling.** The pre-processing step is central to the theoretical guarantees. An experiment comparing performance with and without shuffling would clarify whether the theory's requirement is necessary in practice or merely convenient for proofs.
- **Analyze when OW-L and OW-I diverge.** Since the paper's main empirical contribution rests on these methods, studying synthetic settings where the two approaches produce meaningfully different results would strengthen the paper.

## Removed Points

The following points from the input review were removed:

- **Inconsistent definition of σ_K across abstract and Section 3.** The abstract shows σ_K(x) = x²/(K-1+x²) while Section 3 shows σ_K(x) = e^x/(K-1+e^x). This is virtually certain to be a PDF-to-text parser artifact (e^x mis-rendered as x²). Per the rules, formatting extraction artifacts are not author errors. **Removed.**
- **Missing appendix / unverifiable extension to conditional independence.** The complaint about not being able to verify Appendix C's content is removed per the rule that parser-stripped appendix sections should not be penalized. The core concern about the assumption itself is preserved as Minor Weakness #4. **Removed.**
- **BT model connection overstatement (line 92).** The reviewer claims the BT justification "overstates it." This is a subjective reading of a reasonable statement—Corollary 1 genuinely connects OW to the BT model, and "theoretical justification for the validity" is not an overreach. **Removed.**
- **Single Best outperforms aggregation on MMLU.** The paper explicitly states "Single Best functions as a clairvoyant oracle rather than a fair baseline" (line 287). Criticizing that an oracle outperforms unsupervised methods is not a meaningful weakness. **Removed.**
- **Generic presentation and scope-creep notes.** Various section-by-section notes about presentation choices and requests for experiments outside the paper's stated scope are removed. **Removed.**

## Novel Insights

The most penetrating observation from the review process is the subtle but real gap in Theorem 2: the theorem proves an ordering of expected *advantage* for the correct label, but the paper's narrative frames this as an accuracy guarantee. Because the advantage function is the argmax objective, a higher expected Adv(s\*) does not guarantee a higher probability that s\* is argmax—the variance structure of the advantages also matters. This gap appears to be unaddressed in the paper, and closing it (either by proving the accuracy implication given the sum-zero constraint and shuffling symmetry, or by qualifying the claims) would significantly tighten the theoretical narrative. The OW-L/OW-I empirical identity raises a second novel concern: whether the two estimation methods capture genuinely different information or are structurally equivalent for the tested configurations. Both issues are addressable but currently limit the paper's precision.

## Suggestions

1. **Clarify Theorem 2.** Either prove that E[Adv_ISP(s\*)] ≥ E[Adv_MV(s\*)] implies higher expected accuracy (which may be provable given the sum-zero property of advantage functions and the symmetry from random shuffling), or explicitly state that the theorem guarantees advantage ordering rather than accuracy ordering. Adjust the abstract and introduction claims accordingly.

2. **Investigate the OW-L/OW-I identity.** Explain why the two methods produce identical results across all three datasets. If they are genuinely equivalent for the tested model configurations, describe the conditions that would cause them to diverge and test those conditions synthetically.

3. **Add uncertainty quantification.** Provide confidence intervals or standard errors for the accuracy numbers in Table 3, and describe the statistical testing procedure more completely.

4. **Discuss the practical impact of conditional independence violations.** Analyze error correlation patterns in the experimental data to assess how violations of Assumption 1 affect the empirical results.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>