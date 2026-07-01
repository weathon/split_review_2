## Summary

This paper identifies three scale-invariant controls—the AdamW timescale τ, tokens-per-parameter ratio (TPP), and learning-rate schedule—that govern whether training loss curves (TLCs) collapse onto a universal trajectory across model sizes. It demonstrates collapse in LLM families trained under practical scaling recipes (with weight decay, varying batch sizes, linear decay schedules), introduces the Celerity model family trained in a collapse regime, and shows two applications: deviation-from-collapse as an early diagnostic of training pathologies, and collapse-guided early stopping for hyperparameter tuning.

## Strengths

- **Systematic identification of τ as the key control of TLC shape.** Section 3 provides clean experiments (Fig. 3) where sweeping η, λ, or B produces matching TLCs when τ is matched, and connects this to a bias-variance decomposition via a noisy-quadratic model (Appendix B.3, Eq. 3). This is more principled than prior ad-hoc descriptions.

- **Collapse residuals as a practical diagnostic.** Fig. 1 (right) and the accompanying discussion (lines 204–206) demonstrate that collapse residuals flagged a numerical instability in the 1.8B run at ~60% of training, well before the raw loss curve showed any visible upward trend (~90%). This provides a concrete, quantitative tool where practitioners currently rely on subjective judgment.

- **Simpler normalization than Qiu et al. (2025).** The paper finds that simply dividing by the final training loss (Î=0 in Eq. 1) achieves optimal alignment, sidestepping the need to estimate irreducible loss or compute-optimal steps (line 101). This is a meaningful practical simplification.

- **Early stopping via collapse alignment is clearly demonstrated.** Fig. 9 shows that the "predicted best" method selects the correct λ after only 10–30% of training, while "current best" (used in practice by Falcon) fails at 1.7B. The core idea—aligning partial curves to a predicted normalized TLC to infer final loss—is clever and well-executed.

## Weaknesses

### Fatal
None.

### Major

- **The "r" values in Figure 6 captions are never defined.** The captions report "N(r=0.175)", "N(r=0.087)", and "N(234 TPP, r=0.051)" but the paper never states what "r" represents (standard deviation of residuals? RMSE? correlation coefficient?). Since collapse is the paper's central empirical claim, the absence of a defined quantitative metric means readers cannot assess how tight the collapse is, whether the deviations at 20 TPP and 234 TPP are significant, or compare against Qiu et al.'s "supercollapse" threshold (inter-run noise). The paper relies on visual inspection of figures, which is insufficient for a quantitative claim of this nature. This must be addressed.

### Minor

- **Early stopping evidence is limited in the main text.** Fig. 9 shows only λ sweeps at 1.7B/20TPP and 3.3B/30TPP. The main text does not demonstrate the method for learning rate sweeps, batch size sweeps, or combined HP sweeps. While the paper references "Further experiments are in Appendix D.2," the core claim that collapse "enables reliable early stopping" and "substantially reduc[es] tuning compute" (Key Takeaway 3) would be stronger if at least one additional HP type (e.g., LR tuning) were shown in the main paper. Additionally, Fig. 9 shows no error bars or multi-seed runs, making it unclear how stable the "predicted best" advantage is (though single-seed LLM experiments are standard practice).

- **Warmup mismatch at 20 TPP is acknowledged but not tested.** The paper attributes small early deviations from collapse at 20 TPP to differing LR warmup proportions (line 202), but does not test whether normalizing warmup (e.g., as a fixed fraction of tokens) restores collapse. This would be a straightforward ablation that would sharpen the practical guidance.

- **Celerity compute-efficiency frontier (Fig. 2) is presented without rigorous controls.** The comparison set includes models of different vintages and training methodologies, and the paper acknowledges that many comparison models use benchmark-specific data annealing while Celerity does not (line 159). The "Celerity Fit" power law is fit only to Celerity's own data points. The comparison to BTLm (the cleanest in the paper) is from 2023. The positioning is reasonable and qualified, but the frontier claim would benefit from acknowledging these caveats more explicitly inline rather than leaving them to the "Philosophy" paragraph.

### Trivial

- **Fig. 9 shows no variance/uncertainty estimates.** While single-seed LLM runs are standard due to cost, the paper should at least acknowledge the lack of statistical confidence in its quantitative early-stopping comparisons.

- **The switch to CompleteP (line 164) is mentioned but not explained.** The paper states CompleteP "was more efficient/reliable than µP (Fig. 15)" but does not explain whether CompleteP preserves the same theoretical guarantees (e.g., hyperparameter transfer, scale-invariant dynamics) that the paper's analysis of collapse builds on.

## Nice-to-Haves

- Define "r" as a quantitative collapse metric (e.g., RMSE of normalized residuals across model sizes) and report it for all TPP bands. This would make the central claim quantifiable and allow readers to assess deviations at 20 TPP and 234 TPP relative to inter-run variation.
- Run one additional early stopping experiment at a different TPP band or tuning a different hyperparameter (e.g., LR at 1.8B/80TPP) to broaden the evidence base.
- Ablate whether collapse requires τ to be *optimal* or merely *fixed across sizes* — this would sharpen the practical guidance.

## Removed Points

- **"Increment over Qiu et al. (2025) is narrower than suggested":** Removed. The paper explicitly attributes the initial collapse discovery to Qiu et al. in the abstract ("Qiu et al. (2025) recently showed… What remains unclear is whether this phenomenon persists… We show that it does") and in lines 25–27. The framing is appropriate for an extension to a new, practically relevant regime (weight decay, linear decay schedules, LLM scales up to 3.9B). The reviewer's concern about overclaiming does not hold up against the paper's actual text.
- **"Celerity frontier claim softer than visual suggests":** The paper acknowledges the heterogeneity (line 159) and presents the frontier as approximate. The comparison is clearly labeled and the paper does not overstate the result. Demoted to minor with caveats.
- **"Variance/uncertainty absent from key quantitative claims":** Demoted to trivial. Single-seed LLM training is standard practice; requesting confidence intervals for 1.8B-parameter runs is not proportionate to the paper's setting.

## Novel Insights

None beyond the paper's own contributions. The review surface confirms that the paper's main strengths (identification of τ as a control, diagnostic use of collapse residuals, simpler normalization, early stopping procedure) and weaknesses (undefined collapse metric, limited early stopping scope in main text) are correctly identified by the reviewer. No novel cross-cutting observation emerges from the meta-review.

## Suggestions

1. **Define "r"** — state in Section 4 or figure captions what metric is being reported (e.g., RMSE of normalized residuals, or standard deviation of collapse residuals).
2. **Supplement Fig. 9 with one additional tuning scenario** in the main text (e.g., LR tuning at 1.8B/80TPP) and add error bars or note the single-seed limitation.
3. **Ablate the warmup mismatch** at 20 TPP to verify whether the early deviations are indeed caused by differing warmup proportions.
4. **Briefly explain** why CompleteP was chosen over µP and whether it preserves the scaling guarantees needed for collapse analysis.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>