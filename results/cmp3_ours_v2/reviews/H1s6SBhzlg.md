Now I have a clear calibration picture. Let me write the final review.

**Bracket**: Round 1 suggested a band between 5.5 and 7.0. Narrowing: compared to "Balancing Act: Diversity and Consistency in LLM Ensembles" (6.25, accepted) — a topically similar paper that was accepted despite having questionable experiments and unclear connections between sections — our paper has cleaner theory and better motivation but a concrete σ_K inconsistency and weaker empirical gains. Compared to "SpecFuse" (5.33, rejected) — which had missing baselines and logit-access limitations — our paper has stronger theory and doesn't require logit access. I narrow to **6.0**.

**Anchor papers used**:

| Path | Human Score | Round | Comparison |
|------|------------|-------|------------|
| `8QTpYC4smR` (LLM survey) | 1.00 | R1 | Much weaker; our paper has original contributions |
| `5kMwiMnUip` (jailbreaking) | 1.40 | R1 | Unrelated topic, much lower quality |
| `k7pnwqrpKB` (Deep Bagging) | 2.50 | R1 | Weaker theory, less timely problem |
| `fTdhM7q1o2` (Reward Learning) | 3.00 | R1 | Similar theoretical style but narrower contribution |
| `ioprnwVrDH` (Rethinking MoA) | 3.75 | R1 | Similar topic; our paper has sounder theoretical foundations |
| `lhLQpS33YL` (SpecFuse) | 5.33 | R1 | Topically similar; our paper has stronger theory, weaker empirical gains |
| `grM2Yv49cI` (Model aggregation) | 6.00 | R1 | Similar theory+experiments structure; our problem is more timely |
| `ecIvumCyAj` (Filtered not Mixed) | 5.75 | R1 | Similar structure; their empirical gains are larger (17%) |
| `NO6Tv6QcDs` (Limits to eval) | 6.50 | R1 | Strong theory + modest empirical; accepted despite modest gains |
| `E60SIDItyT` (Aggregate responses) | 6.00 | R1 | Clean theoretical paper, accepted |
| `Dl6nkKKvlX` (Balancing Act) | 6.25 | R2 | Most similar topic; accepted despite questionable experiments |
| `tbx3u2oZAu` (RAG Theory) | 6.00 | R2 | Clean theory paper, accepted |

---

## Summary

This paper studies aggregation of multiple LLM responses using higher-order information beyond majority voting. It proposes Optimal Weight (OW), a Bayesian-optimal linear weighting scheme using first-order information (agent accuracies), and Inverse Surprising Popularity (ISP), which uses second-order information (answer correlations across models). The paper proves SP < MV < ISP in expectation (Theorem 2), derives closed-form advantage gaps, and validates empirically on synthetic data, UltraFeedback, MMLU, and a healthcare dataset. Practical adaptations OW-L and OW-I (heuristic accuracy estimation from second-order information) are also proposed.

## Strengths

1. **The Bayesian optimality of OW is cleanly derived.** Theorem 1 proves that a linear weighted aggregator with weights proportional to log((K−1)x_i/(1−x_i)) achieves Bayes optimality under conditional independence with uniform priors induced by random shuffling. This is a rigorous theoretical foundation for weighted LLM aggregation.

2. **The SP < MV < ISP ordering (Theorem 2) is a non-trivial theoretical result.** The paper shows counterintuitively that the classic Surprisingly Popular rule underperforms MV in the LLM setting and proposes a corrected version (ISP) with a provable advantage. The closed-form expressions for expected advantage gaps (lines 209–213) are concrete and interpretable.

3. **Evaluation spans diverse settings.** Experiments cover synthetic data (matching model assumptions), two standard LLM benchmarks (UltraFeedback, MMLU), and a real-world healthcare dataset (ARMMAN), demonstrating consistency across settings.

4. **The practical estimation framework (Section 4.3, Theorem 3) bridges theory to practice.** The finite-sample guarantee for ISP's advantage over MV with estimation error quantified by an O(√((1/M) log(1/δ))) term is a useful addition.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **σ_K inconsistency between abstract and main text.** The abstract (line 25) defines σ_K(x) = x²/(K−1+x²), while the main text (line 73) defines σ_K(x) = e^x/(K−1+e^x). These are different functions. The e^x version is the correct one for the claimed Bayesian optimality (weights should be proportional to log((K−1)x/(1−x))). The abstract's x² version would lead to a different weighting scheme. This is a concrete error that must be corrected — the abstract should match the main text.

2. **The best-performing methods in the real-data experiments (OW-L, OW-I) are heuristic and lack theoretical grounding, while the theoretically principled method (ISP) shows only marginal gains.** The paper transparently describes OW-L and OW-I as heuristics (line 29, Section 5.2), but the headline results in Table 3 are driven by these methods. ISP's absolute gains over MV are 0.69–1.05%, while OW-L/OW-I add another ~0.3–0.4% without any theoretical guarantees. The paper would benefit from clarifying this gap between what is provable and what performs best empirically.

3. **A natural baseline — confidence-weighted voting using per-question model confidence — is absent.** The related work (line 35) cites Chen et al. (2023a) and Fu et al. (2025) showing that confidence-based aggregation improves accuracy. Confidence scores from LLMs do not require ground-truth labels, making them a directly comparable baseline to the proposed methods (which also operate without labels). Its absence makes it harder to assess whether the proposed methods add value beyond this simpler alternative.

4. **No variance or confidence intervals in the main results.** Table 3 reports only point estimates of accuracy. The only uncertainty measure is t-statistics for paired comparisons (line 303), which do not convey the magnitude of variation across model selections or random shuffles. Adding error bars or confidence intervals would strengthen the empirical claims.

5. **Modest absolute gains over MV.** On real datasets, the absolute improvements are 0.54–1.45%. On ARMMAN, the gain for all methods is 0.54% (85.78% vs 85.24%), which is practically small even if statistically significant (t=3.22). The practical significance of these gains should be contextualized more carefully.

### Trivial
None.

## Nice-to-Haves
- Adding a confidence-weighted voting baseline would significantly strengthen the empirical contribution.
- Reporting accuracy with error bars across random shuffles or model ensemble selections.
- A cost-benefit analysis for practitioners: how many ground-truth labels are needed before OW outperforms ISP?

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Formatting error in Algorithm 1 (`s ∈ ∑` should be `s ∈ S`)"** — Parser artifact; the original PDF does not have this issue.
- **"Equation 7 is underspecified; expanded expressions relegated to appendix"** — The appendix exists in the original submission but was stripped by the parser. This is not the authors' fault.
- **"Section 4.1 explanation is entirely post-hoc"** — The paper provides an intuitive explanation consistent with its theoretical results and cites prior work. The reviewer's demand for additional evidence is beyond the paper's stated scope.
- **"Abstract uses 'mitigate' which overstates the result"** — Nitpick; Theorem 2 does prove ISP has higher expected advantage than MV, which is a genuine mitigation of MV's limitations.
- **"Overclaiming superiority over individual models on MMLU"** — The paper's claim (line 301) is specifically about UltraFeedback and ARMMAN, where it is factually correct. The paper clearly labels Single Best as a "clairvoyant oracle" (line 287).

## Novel Insights

The harsh critic correctly identifies the σ_K inconsistency between abstract and main text — a concrete error that the authors should fix. The observation that the heuristic methods (OW-L/OW-I) produce the best results while lacking theoretical support is accurate, though the paper is transparent about their heuristic nature. The missing confidence-weighted baseline is a useful suggestion for strengthening the evaluation. Beyond these points, the paper's core theoretical contributions (Bayesian optimality of OW, SP < MV < ISP ordering) stand as genuine and well-supported.

## Suggestions

1. **Fix the σ_K inconsistency.** The abstract (line 25) should use σ_K(x) = e^x/(K−1+e^x) to match the main text.
2. **Add a confidence-weighted voting baseline.** Compare ISP and OW-L/OW-I against per-question confidence-weighted voting using each LLM's self-reported probabilities.
3. **Include variance estimates** (confidence intervals or standard deviations) in the main results table.
4. **Clarify the theory–practice gap.** Discuss the extent to which the heuristic OW-L/OW-I methods' success is theoretically expected and whether the small additional gains over ISP justify their use without guarantees.
5. **Contextualize the practical significance** of the performance gains, especially on ARMMAN where the improvement is 0.54%.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>