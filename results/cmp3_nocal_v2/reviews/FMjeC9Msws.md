## Summary

This paper presents a large-scale empirical study (400,000+ GPU-hours) of RL training design choices for LLMs, organized around a sigmoidal compute-performance scaling framework. It proposes SCALERL, a recipe integrating existing best-practice components, and demonstrates that its validation performance follows a predictable sigmoidal trajectory that can be extrapolated from early training (e.g., fit on 50k GPU-hours to predict 100k GPU-hours). The study systematically ablates design choices (loss type, precision, normalization, off-policy setup, etc.) in terms of their effects on asymptotic performance (A) and compute efficiency (B).

## Strengths

- **Exceptional experimental scale and systematic design.** The paper reports 400,000+ GPU-hours of experiments with a three-stage design (initial ablations at 3.5k–4k hours → LOO ablations at 16k hours → scaling validation at 100k hours). Individual LOO runs at 16k GPU-hours are substantially larger than typical academic RL-for-LLMs studies, giving the analysis real statistical weight.

- **Validated predictive extrapolation at 100k GPU-hours.** The central claim—that sigmoidal curves fit on the first 50k GPU-hours can predict performance up to 100k GPU-hours—is directly validated in Figure 1(a). The extrapolated trajectory closely matches the actual extended training, which is the paper's strongest single piece of evidence.

- **Multi-axis scaling analysis (Section 5).** The paper demonstrates that the sigmoidal framework holds when scaling batch size (2×), generation length (32k tokens), and model size (17B×16 MoE). This is important evidence that the framework generalizes beyond a single configuration.

- **Honest scope boundaries.** The paper explicitly states (Section 7, line 241) that its primary focus is in-distribution validation performance, not downstream generalization. It does not oversell the novelty of SCALERL's components, which are credited to prior work.

## Weaknesses

### Fatal
None.

### Major

- **Internal inconsistency in the LOO fixed-A re-fitting (Figure 5).** The LOO table in Figure 5 reports individually fitted A values that range from 0.590 to 0.610 (average ≈ 0.604). The paper states: "we average the asymptotic reward A across all runs, re-fit the curves with this fixed A" and then reports "fitted B w/ fixed A = 0.685" in the table. The value 0.685 is ~0.08 higher than any individual A in the table—a ~13% relative discrepancy on a bounded [0,1] metric. This is not a minor rounding issue. Since the fixed-A re-fitting is the basis for the efficiency (B) comparisons in the LOO analysis, this inconsistency needs a clear explanation or correction. If it is a typo (e.g., 0.605 mis-rendered as 0.685), the authors should state this explicitly; if it comes from a different experiment, that context must be provided.

### Minor

- **"State-of-the-art" claim is overstated relative to MiniMax.** The paper states that SCALERL "achieves higher asymptotic performance" (line 68) and "surpasses all other methods" (Figure 2 caption). However, in Figure 2, both SCALERL and MiniMax have the same fitted A = 0.610. SCALERL has higher B (1.97 vs. 1.77), meaning better compute efficiency—a genuine and useful advantage. But the paper should accurately describe this as "competitive asymptotic performance with better compute efficiency" or "matches the best asymptote while reaching it faster," not as categorically higher asymptotic performance. The claim in line 228 ("near state-of-the-art") is more accurate and conflicts with the stronger statements elsewhere.

- **Extrapolation factor is modest relative to the claims.** The paper demonstrates extrapolation at roughly 2× the fitting range (fit on 50k GPU-hours → extrapolate to 100k; fit on 8k GPU-hours → extrapolate to 16k). Pre-training scaling laws routinely extrapolate over 10–100×. The paper claims the framework "enables extrapolation from smaller-scale runs" and "cost-effectively predicting the scalability of new RL algorithms," but the demonstrated factor is modest. This does not invalidate the contribution, but the scope of the predictive claim should be calibrated to the evidence.

### Trivial
None.

## Nice-to-Haves

- **Confidence intervals on fitted parameters (A, B, C_mid).** The paper's utility for decision-making depends on these estimates. Even bootstrap-sampled intervals would strengthen trust in the comparisons.
- **Sensitivity analysis for the fitting cut-off.** The paper excludes the first ~1,500 GPU hours. A brief sensitivity analysis (or a clear summary from Appendix A.7 in the main text) showing how extrapolated A and B shift when the cutoff moves would address a natural concern.

## Removed Points

- **Base model and SFT checkpoint not specified.** The paper states "More details about training, including SFT and hyper-parameters, are in Appendix A.3" (line 74). The appendix is stripped by the PDF parser; the information exists in the original submission. Per policy, this criticism is removed.
- **Confidence intervals suggested as a weakness.** Moved to Nice-to-Haves; this is a desirable addition, not a flaw in what was presented.
- **Sensitivity to fitting cutoff.** Moved to Nice-to-Haves; the paper references Appendix A.7 for robustness checks.

## Novel Insights

The harsh critic identifies one genuinely novel observation that is not simply restating the paper's own claims: the juxtaposition that SCALERL ties with MiniMax on the asymptote (A=0.610) while having better efficiency, combined with the observation that the paper's SOTA framing masks this nuance. This reveals a pattern common in RL scaling papers—claiming categorical superiority based on a composite advantage (efficiency + asymptote) when the asymptote alone is tied. The insight is that the paper's own sigmoidal framework, which cleanly separates A and B, makes this ambiguity explicit and could itself serve as a template for more precise claims in future work. Beyond this, the review's novel observations are largely confined to the paper's own contributions.

## Suggestions

- Resolve the A=0.685 inconsistency in Figure 5: clarify where this value comes from, or correct it to the actual average of the individual A values (~0.604). If it is a typo, state the correct value.
- Reframe the SOTA claim to accurately reflect the MiniMax comparison: "competitive asymptotic performance with better compute efficiency" rather than "higher asymptotic performance" or "surpasses all other methods."
- Add a brief statement in the main text clarifying which 8B pre-trained/SFT checkpoint was used (the appendix reference is fine for details, but the base model identity should be clear in the main paper).
- Consider adding confidence intervals to the fitted parameters in a camera-ready version.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>