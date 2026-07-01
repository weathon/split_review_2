## Summary

This paper proposes two aggregation methods for combining responses from multiple LLMs: Optimal Weight (OW), which uses first-order accuracy information and is shown to be Bayesian optimal under conditional independence, and Inverse Surprising Popularity (ISP), which uses second-order correlation information and is proven to dominate majority voting (MV) in expectation. The paper provides theoretical guarantees (Theorems 1–3) and validates empirically on simulated data, UltraFeedback, MMLU, and a real healthcare dataset (ARMMAN).

## Strengths

1. **Bayesian optimality of OW (Theorem 1) is a clean theoretical result.** The paper shows that a linear weighted scheme with weights equal to the inverse of a sigmoid-like function achieves Bayesian optimality among *all* aggregators (not just linear) under the proposed model. The connection to the Bradley-Terry model (Corollary 1) ties the result to a widely used framework in LLM preference tuning.

2. **The ISP construction is principled and well-motivated.** The paper identifies why standard Surprising Popularity underperforms MV for LLMs (Section 4.1–4.2)—systematic biases that SP exploits in human crowds are less pronounced in LLMs—and designs ISP as a counterfactual variant. The derivation from Equations (3)–(5) is clearly explained.

3. **Consistent empirical support across multiple distinct settings.** The methods outperform MV on simulated data (Table 2), two standard LLM benchmarks (UltraFeedback, MMLU), and a real healthcare dataset (ARMMAN). Across 16 model ensembles, OW-L outperforms MV in 97.92% of cases, and MV never achieves the best performance. The ISP results independently validate the improvement without relying on the OW pipeline.

## Weaknesses

### Major

- **OW-L and OW-I produce numerically identical results across all datasets without explanation.** In Table 3, OW-L and OW-I achieve *identical* accuracy on all three datasets (73.66%, 90.37%, 85.78%). In Table 4, their per-question win/loss counts against MV are *identical* (2545/1727, 1821/659, 264/195) on every dataset. These are two fundamentally different estimation procedures: OW-L solves an empirical risk minimization problem (Eq. 7) to fit accuracies from observed conditional probabilities, while OW-I uses ISP's predictions as pseudo-ground-truth and counts agreement proportions. For these to produce identical predictions across every question on three datasets is suspicious and unexplained. The authors must explain this before the experimental claims can be fully trusted.

### Minor

- **Theorem 2 proves ordering of expected advantages, but experiments evaluate accuracy.** Theorem 2 guarantees that ISP > MV > SP in *expected advantage*. The advantage function is the score used for arg-max selection; a larger expected advantage for the correct label does not formally imply higher expected accuracy. The paper would benefit from clarifying this relationship or providing a direct derivation linking the two.

- **The t-statistics lack context for interpretability.** The reported t-statistics (12.53, 23.39, 3.22) are large relative to the ~1 pp accuracy differences, but the paper does not state the unit of analysis (question-level?), sample size, or effect sizes. Without this context, the reader cannot calibrate practical versus statistical significance.

- **The OW-L optimization (Equation 7) is underspecified.** The objective is defined but no algorithm, solver, or convergence properties are provided. While N=4 variables may make this easy to solve, the paper should state the method used for reproducibility.

- **No confidence intervals or error bars on any accuracy results.** Given finite datasets and specific question splits, reporting variability would help the reader assess the stability of the reported improvements.

### Trivial

- **Inconsistency in σ_K definition.** The abstract (line 25) defines σ_K(x) = x²/(K-1+x²), while the main text (line 73) defines σ_K(x) = eˣ/(K-1+eˣ). These are different functions and should be reconciled.

- **The position-bias assumption (line 50–51)** is stated with weak justification ("with the improvement of LLMs' long-context abilities, we assume…"). The paper should acknowledge that position bias is well-documented and discuss how the random shuffling preprocessing mitigates it even if the assumption does not hold perfectly.

## Nice-to-Haves

- **A confidence-weighted voting baseline** would be a natural comparison point, since confidence scores (log-probabilities or verbal confidences) are often available from LLM APIs and represent the simplest form of weighted aggregation. The paper cites Chen et al. (2023a) and Fu et al. (2025) on confidence-based aggregation but does not include them as baselines.

- **Practical guidance on method selection.** The paper proposes OW-L, OW-I, and ISP but does not discuss when to use which. ISP is simplest (only needs second-order information, no optimization), while OW-L/OW-I need more computation but often perform better. A clear tradeoff statement would be helpful.

- **Discussion of the overhead of random shuffling.** Shuffling labels per question changes prompts, which may multiply query costs. The practical implications are not discussed.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **Criticism about not being able to evaluate Appendix C for the conditional independence relaxation** — The parser strips appendices from all papers; they exist in the original submission. The paper's own acknowledgement of the assumption (line 63) is sufficient for review purposes.
- **Criticism that empirical gains are "modest" and the framing is "rhetorically inflated"** — The paper claims "consistently dominate majority voting," which is factually accurate. The magnitude (0.5–1.5 pp) is neither hidden nor misrepresented.
- **Algorithm 1 formula formatting artifact** — The syntactically broken `arg max` is a parser artifact; the intended formula is clear.
- **"Selective reporting" of strongest models in main text** — The paper explicitly states it reports strongest models in the main text and all 16 combinations in the appendix, which is standard practice.

## Novel Insights

Beyond the paper's own contributions, the review surfaces one genuinely novel observation: the sharp contrast between the SP rule's well-documented success in human crowds and its failure relative to MV in the LLM setting. The paper's diagnosis (systematic biases in humans are less pronounced in LLMs) and its counterfactual fix (ISP inverts the conditioning to amplify useful signal) represent an insightful adaptation of a classic information-aggregation idea to the LLM domain. However, the OW-L/OW-I identity issue needs to be resolved before the experimental component can be fully trusted.

## Suggestions

1. Explain why OW-L and OW-I produce identical predictions across all questions on all three datasets. If they genuinely coincide for theoretical reasons, state this explicitly. If rounding conceals small differences, report more decimal places.
2. Clarify the relationship between the advantage guarantee (Theorem 2) and the accuracy metric used in experiments.
3. State the unit of analysis for the t-tests and report effect sizes alongside the t-statistics.
4. Add confidence intervals or standard deviations to the main accuracy results.
5. Reconcile the σ_K definition between the abstract and main text.
6. Acknowledge position bias as a known limitation rather than asserting it is resolved by improved long-context abilities.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>