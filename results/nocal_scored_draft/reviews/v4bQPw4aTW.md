Now I have all the information needed. Here is my final consolidated review.

---

## Summary

This paper proposes AdaBoN, a two-stage adaptive allocation policy for Best-of-N inference-time alignment. Given a batch of prompts and a per-prompt LM call budget, AdaBoN first explores each prompt with a fixed budget to estimate its reward distribution (via Gaussian KDE), then uses the concavity of the expected-max function (Proposition 3.1) to greedily allocate the remaining budget where marginal gains are highest. The method requires no auxiliary training and is evaluated on 12 LM-RM pairs across 3 datasets.

## Strengths

- **Well-motivated practical problem.** The observation that Best-of-N applies uniform sampling budgets regardless of prompt difficulty is clearly articulated (Section 2.3), and the resource allocation framing is natural and timely for on-device/latency-sensitive settings.

- **Clean method with theoretical grounding.** The two-stage design is well explained. Proposition 3.1—that the expected-max function is concave and monotone for any distribution with finite first moment—is a genuinely useful result that justifies the greedy algorithm and makes the method broadly applicable.

- **Broad empirical evaluation.** The paper tests 12 LM-RM pairs across 3 datasets with 50 distinct batches per setting, substantially more comprehensive than the closest prior work (Damani et al., 2024). The systematic variation of K and B in the appendices strengthens the analysis.

- **No auxiliary training required.** AdaBoN works out-of-the-box for any LM-RM combination without retraining, which is a genuine practical advantage over methods that require learning a gain-prediction model.

## Weaknesses

### Major

1. **No empirical comparison with the most closely related prior work (Damani et al., 2024).** The paper explicitly contrasts AdaBoN with Damani et al. on three dimensions (Section 1.1), positions itself as a superior alternative, and states that Damani et al. "does not observe significant improvements for large inference budgets" (line 54)—a claim AdaBoN should be tested against. Yet it never provides any empirical comparison. The reasons given (Section 4.2: no existing implementation, prohibitive training cost of 216K MLPs) are practical constraints, but they leave a central evidential gap: the paper can only claim to outperform the simplest non-adaptive baseline (uniform), not a prior adaptive method. This directly limits support for the paper's strongest claims about being a better adaptive allocation strategy.

2. **The exploration budget d = 0.75B consumes 75% of per-prompt compute on uniform exploration, leaving only 25% for adaptive allocation.** With B=120 and d=90, only (B-d)K = 150 samples across K=5 prompts are allocated adaptively. The ablation on d is narrow (tested only in {0.60B, 0.70B, 0.75B, 0.80B}, never below 0.60B). This makes it difficult to assess how much of the reported gain comes from prompt-adaptive allocation versus simply running uniform sampling with a larger effective budget. The core methodological claim—that adaptivity drives the gains—cannot be cleanly separated from the experimental design.

### Minor

3. **Effect sizes are modest and framing emphasizes upper-tail results.** Median BWRs range from 0.54 to 0.62 across 12 LM-RM pairs (Table 1). For Qwen-Armo, median BWR is 0.54 [0.51, 0.56] and only 78% of batches achieve BWR > 0.50 (Table 2b), meaning AdaBoN loses to uniform on 22% of batches for that pair. The paper frames results with "as high as 70%" and "outperforms across all" rather than centering the overall distribution.

4. **The left-skewed distribution failure case (Qwen-Armo) deserves more prominent treatment.** This case is mentioned briefly in the main text with analysis relegated to Appendix G.1. Given that one of 12 LM-RM pairs shows notably degraded performance, and the paper's limitations section does not discuss distribution-shape dependency, this is an under-analyzed failure mode that may affect generalizability.

5. **Monte Carlo sample size m = 1024 is stated but not justified.** No sensitivity analysis is provided to show whether smaller values (e.g., 64 or 128) would suffice or how this parameter affects allocation quality.

6. **No wall-clock time analysis.** The paper claims latency benefits from parallelizing LM calls (Section 3), but the KDE fitting + Monte Carlo estimation step (up to K × (B-d)K ≈ 750 estimates per batch, each requiring m=1024 samples) is not measured. The practical runtime overhead of the post-processing phase is unquantified.

7. **The claim that reward distributions are "smooth and easy to learn" (contribution 1) is supported primarily by visual inspection of a few histograms (Figure 1).** The paper does compare KDE against parametric alternatives (Gaussian and Skew-Normal MLE, Appendix K.3), which provides some support, but the "smooth and easy to learn" characterization itself lacks rigorous evidence.

### Trivial

None.

## Nice-to-Haves

- Comparison with simple heuristics (e.g., allocate more budget to prompts with higher variance in initial samples) would provide a sanity check.
- A sensitivity analysis for the Monte Carlo sample size m would help justify the choice of 1024.
- Expanding the exploration budget ablation to include d < 0.60B would clarify whether a more adaptive variant would perform better or worse.

## Removed Points

These points from the input review were removed with justification:
- **"EST values don't support the 'at least 20%' claim."** Factually incorrect: EST of 148 corresponds to 23.3% above B=120, and the claim is "competitive against" not "saves." The data support the claim.
- **Figure caption corruption (references to "Medical, Math, ArXiv" datasets and "Random" method).** This is a PDF parser artifact, not an author error.
- **Missing simple heuristic baselines.** A nice-to-have suggestion, not a core weakness.
- **Missing related works.** Rule prohibits raising this without external confirmation.
- **Formatting/style nitpicks.** Parser artifacts or out of scope.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add a comparison with Damani et al. (2024), even on a limited subset of settings (2–3 LM-RM pairs, 10 batches). A simplified proxy implementation would substantially strengthen the paper's central claims.
- Expand the exploration budget ablation to include d ∈ {0.2B, 0.4B, 0.5B} to test whether a smaller exploration budget (which leaves more room for adaptivity) improves or degrades performance. This would clarify the method's actual operating regime.
- Report wall-clock time including the KDE fitting and Monte Carlo estimation phase to substantiate latency claims.
- Add a sensitivity analysis for the Monte Carlo sample size m.
- Discuss the Qwen-Armo left-skewed distribution case in the main limitations section.

## Score and Decision

This paper addresses a real problem with a clean, practical method and provides a broad evaluation. However, two significant gaps limit its contribution: (1) the lack of empirical comparison with the most closely related prior work (Damani et al., 2024), despite positioning against it; and (2) the experimental design where 75% of the budget is spent on uniform exploration, making it unclear how much adaptivity contributes to the reported gains. These issues are addressable with additional experiments, but in the current form they weaken the paper's core claims.

MY FINAL SCORE: 5.5

MY FINAL DECISION: Reject