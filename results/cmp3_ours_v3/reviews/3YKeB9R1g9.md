## Summary

This paper extends the training loss curve (TLC) collapse phenomenon—previously shown at small scale by Qiu et al. (2025)—to LLM families trained under practical scaling recipes. It identifies three controls (AdamW timescale τ, tokens-per-parameter TPP, and LR schedule) as sufficient for collapse, introduces the Celerity model family trained in a collapse regime, and demonstrates two applications: diagnostics via collapse residuals and early stopping via a parametric surrogate fitted at small scale. The core empirical finding—that fixed TPP and optimally-set τ produce TLC collapse across model sizes from ~100M to ~3.9B parameters—is robustly supported by controlled experiments in Section 3.

## Strengths

- **Clear identification of the three sufficient controls for TLC collapse (τ, TPP, LR schedule).** Section 3 systematically isolates each variable. Figure 3 is particularly clean: sweeping η, λ, or B produces the same TLC shape when τ is matched, establishing τ as the causal variable rather than any single hyperparameter. This meaningfully extends Qiu et al. (2025) from μP-based compute-optimal ladders to practical scaling recipes that co-scale width, depth, batch size, and weight decay.

- **Genuinely practical diagnostic concept.** The collapse-residual idea (Fig. 1 right, lines 204–206) detected a numerical instability at ~60% of training that the raw TLC revealed only after ~90%. The paper describes a concrete debugging process (identifying timing, running ablations with different batch sizes, tracing the issue to a loss kernel triggered at specific microbatch sizes). This is a real operational benefit, even if only demonstrated on one example.

- **Well-motivated TPP trade-off analysis.** Section 4's analysis of compute-vs.-parameter-efficiency (Fig. 5) is thoughtful. Choosing TPP=234 to achieve 62% parameter reduction at 67% extra FLOPs is grounded in clear analysis (Appendix C.1), and the paper honestly acknowledges that larger TPP values yield rapidly diminishing returns ("doubling our FLOPs… reduces N by only a further ~11%," line 145).

- **Celerity is credibly competitive.** Figure 2 shows Celerity models on the compute-efficiency frontier against a reasonable set of open models up to 3.9B parameters. The paper fairly notes evaluation complications from data annealing (line 159) and positions Celerity as a reference for pre-(mid-training) comparison.

- **The early stopping procedure is principled in design.** Rather than treating early stopping as a generic statistical problem, it exploits the collapse phenomenon: partial curves are aligned to a parametric surrogate fitted at small scale, and the normalizer is the predicted final loss. The approach is well-motivated even though its empirical validation is incomplete.

## Weaknesses

### Fatal
None.

### Major

- **Early stopping evaluation uses only weak baselines.** The paper compares its method against "choose randomly" and "choose current best" (lines 275–282). The relevant comparison in the HPO literature includes structured early-termination methods like Hyperband (Li et al., 2018), BOHB (Falkner et al., 2018), or ASHA—methods the paper cites in Related Work (line 294) but does not compare against. Without a competitive baseline, the paper cannot convincingly claim that collapse-based early stopping is better than known alternatives; it only shows it is better than two straw men. This significantly weakens the paper's third contribution.

- **Deviation-from-collapse diagnostic is demonstrated on a single anecdote.** The 1.8B story (lines 204–206) is compelling but is one data point. The paper does not report how many other training runs produced deviations, whether those corresponded to real problems or false positives, or propose any thresholding or statistical test for "significant" deviation. A systematic evaluation of sensitivity/specificity is absent. The paper's framing of this as a demonstrated contribution ("demonstrating two applications at scale," line 9) overstates the evidence.

- **Parametric surrogate is under-validated.** The functional form (Eq. 4–5) is chosen empirically with five free parameters. The paper acknowledges a 2× gap between this surrogate and an oracle fit per curve (line 273) but does not report confidence intervals, test on held-out (τ, TPP) combinations, study sensitivity to initialization of the alternating fitting procedure (lines 249–251), or compare against simpler alternatives. Given that the surrogate is the linchpin of the early stopping procedure (Step 5 of the 6-step algorithm), this lack of validation is a significant methodological gap.

### Minor

- **The contribution of normalization to collapse is not quantified.** The paper normalizes curves by dividing by the final training loss (line 101). For curves with different final losses, this normalization artificially improves visual alignment—two exponential decays with different rates, each divided by its own asymptote, will look more similar than their raw counterparts. The Llama-2 comparison (Fig. 1 left) shows normalization alone is insufficient, but the paper never quantifies how much of the observed collapse is attributable to the data (fixed TPP, matched τ) versus the normalization itself. A control experiment permuting (TPP, τ) assignments would clarify this.

- **Data composition confounds the compute-efficiency comparison.** Figure 2's comparison across models with different data strategies (line 159: Celerity emphasizes educational, math, and coding data) is inherently confounded. Celerity's position on the frontier may partly reflect its data choices rather than the collapse-based training strategy. The paper acknowledges this philosophy but does not control for it.

- **Statistical uncertainty is absent throughout.** Accuracy measurements in Fig. 2 and Table 10 have no error bars. MAE in Table 11 is reported without variance. The early stopping results in Fig. 9 show single trajectories without error bands. This limits the reader's ability to assess reliability.

- **The "scale invariance" claim rests on an unverified assumption.** The claim (lines 131–132) depends on the assumption that "residual bias at end-of-training is negligible relative to the variance floor." This is asserted but not empirically verified.

- **The claim about recognizing saturation (line 29) is not fully delivered.** The paper shows how to detect deviations from a reference curve but does not propose a criterion for saturation of the reference itself.

- **"CompleteP" is mentioned without explanation in the main text** (line 164), and the divergence from μP is not justified.

### Trivial
None.

## Nice-to-Haves

- Evaluate on a broader set of benchmarks (e.g., GSM8K, MMLU, HumanEval) to strengthen the "compute-efficiency frontier" claim, though the paper's stated philosophy (line 159) scopes this out.
- A control experiment randomly permuting (TPP, τ) assignments across model sizes to quantify how much of the collapse comes from normalization versus the data regularity.

## Removed Points

These points from the input review are flagged as removed; treat them with caution:

- *"Smoothing over 100 steps could dampen genuine differences"* — Standard smoothing; purely a formatting/methodology nitpick.
- *"The Celerity training data mix is not fully specified in the main paper"* — The appendix is stripped by the parser; the original submission contains it (Appendix Table 6).
- *"Missing detail on μP vs. CompleteP"* — Kept as minor; the term is unexplained in the main text but Fig. 15 (in the stripped appendix) may address it. The point about generalizability to other architectures is too speculative.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Compare against a structured HPO baseline.** The early stopping evaluation should include Hyperband, ASHA, or BOHB on the same sweep. If collapse-based selection wins, that is a strong result; if not, identify where the approach is complementary.
2. **Systematically evaluate the diagnostic.** Run the collapse-residual analysis on all Celerity training runs (not just the 1.8B example). Report precision/recall against a ground-truth log of training incidents (restarts, hardware issues, loss spikes).
3. **Validate the surrogate on held-out (τ, TPP) regimes with confidence intervals.** Hold out specific (τ, TPP) combinations from the 111M training data and measure prediction error. Report sensitivity to initialization of the alternating fitting procedure.
4. **Add error bars/confidence intervals** to key quantitative results (accuracy in Fig. 2, MAE in Table 11, early stopping in Fig. 9).
5. **Perform a control experiment** permuting (TPP, τ) assignments across model sizes while keeping the same per-curve final-loss normalization, to quantify the normalization's contribution to collapse.

## Score and Decision

**Calibration anchors retrieved (all rounds):**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Scaling Law with Learning Rate Annealing (o9YC0B6P2m) | 6.75, Reject | 1 | Similar topic (loss curve prediction); our paper has stronger empirical finding but weaker validation on applications |
| A Multi-Power Law for Loss Curve Prediction (KnoS9XxIlK) | 6.00, Accept | 1,2 | Similar topic and weaknesses; our paper is at comparable scale (3.9B vs 400M) with more novel core finding |
| Scaling Optimal LR Across Token Horizons (WYL4eFLcxG) | 6.00, Accept | 1,2 | Similar empirical methodology; our paper has broader scope but similar validation gaps |
| Straight to Zero (hrOlBgHsMI) | 6.33, Accept | 2 | Highly similar (τ framework, SlimPajama, GPT-2-like models); our paper has broader contributions but weaker application validation |
| Small-scale proxies for large-scale instabilities (d8w0pmvXbZ) | 8.00, Accept | 1 | Cleaner execution and stronger validation; our paper is not at this level |
| Time Transfer (MLhquJb1qN) | 5.25, Reject | 1 | Narrower scope and less practical impact |
| Deep Neural Networks without Normalization (nmRY3BAll4) | 4.25, Reject | 1 | Different topic but similar methodology concerns |

**Round 1 bracket:** 5.5–7.5 (based on comparison with anchors in that range)

**Final score determination:** The paper is most similar to "Straight to Zero" (6.33, accept) and "A Multi-Power Law" (6.00, accept). It has a stronger core empirical finding (collapse with identified controls) than both, but weaker validation on the applied components (early stopping, diagnostics). The three major weaknesses (weak early-stopping baselines, single-anecdote diagnostic, under-validated surrogate) keep the paper from being a clear accept (8), while the well-supported core finding (Section 3) and competitive model family (Celerity) place it above borderline reject territory. Score 6.0 reflects a paper whose main contribution is solid but whose applied claims need substantially stronger evidence.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>