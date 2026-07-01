## Summary

AdaSVD proposes two improvements to SVD-based LLM compression: (1) **adaComp** — an alternating least-squares post-hoc optimization of the truncated SVD factors using the Moore-Penrose pseudoinverse, and (2) **adaCR** — a layer-adaptive compression ratio assignment based on cosine-similarity between layer inputs and outputs. The method is evaluated on LLaMA2, OPT, Vicuna, and Mistral families plus LLaVA, showing consistent perplexity improvements over the prior SOTA SVD-LLM.

## Strengths

1. **Principled alternating-update formulation.** The paper correctly identifies that after SVD truncation, the remaining low-rank factors U and V^T can be re-optimized against the original reconstruction objective. Casting this as alternating least squares (Eqs. 8–13) and solving via the Moore-Penrose pseudoinverse is mathematically sound. Figure 3a shows this is more stable than a naive direct update — a genuine empirical finding.

2. **Clean ablation structure.** Table 3 systematically disentangles adaComp and adaCR contributions, the effect of iteration count, and the minimum retention ratio. This is the right way to present the evidence.

3. **Multi-family evaluation.** The method is tested on LLaMA2, OPT, Vicuna, and Mistral families (Table 2), plus the LLaVA VLM (Figure 5), strengthening the generality claim.

4. **Real gains at high compression ratios.** At 60% compression, AdaSVD achieves a 44% relative perplexity reduction on WikiText-2 (89.90 → 50.33) and 57% on C4 (561.00 → 239.18) over SVD-LLM — non-trivial improvements.

## Weaknesses

### Fatal
None.

### Major

1. **Framing does not match the evidence strength.** The paper claims AdaSVD "effectively narrows the performance gap between compressed and original models" (contribution bullet 3), but at 40–60% compression *all* SVD-compressed models — including AdaSVD — suffer catastrophic degradation:
   - WikiText-2 perplexity rises from 5.68 (original) to 14.76 at 40% CR (2.6×) and 50.33 at 60% CR (9×).
   - On commonsense reasoning, AdaSVD at 40% achieves roughly 23–42% accuracy across tasks versus 69–79% for the original. MMLU drops to approximately 23–24 — near random chance (25%).
   The improvement over SVD-LLM is real but modest at 40–50% CR (6–12% relative), and in a regime where the model has already lost most practical capability. The contribution is in reducing *how much* performance is lost, not in preventing catastrophic degradation. The language throughout (abstract, contributions, conclusion) should be recalibrated to match what the evidence actually supports.

### Minor

2. **Stack-of-batch averaging is not equivalent to "utilizing more data."** Equations 14–15 average calibration samples into buckets. This reduces sample-level variation and is not the same as genuinely using more data. The improvement in Figure 3b could be a regularization effect (smoothing reduces overfitting to noisy calibration samples). The paper does not compare against a baseline using the same number of samples *without* averaging (i.e., directly using a smaller batch size), nor does it discuss the regularization interpretation.

3. **Adaptive CR formula has unspecified boundary behavior.** Equation 19 defines CR(W) = mrr + I_n(W)·(trr−mrr), where I_n(W) is a mean-normalized cosine similarity. Cosine similarity can be negative, and after normalization I_n(W) could theoretically be negative or arbitrarily large, potentially producing compression ratios below mrr or above 1. The paper does not specify clipping or bounds. While the experiments may avoid this regime, the method as specified is incomplete.

4. **Figure 1 is not informative.** The log10-scale plot clusters all modern methods at roughly 10^1.1, making differences visually imperceptible. A table or linear-scale inset would be more useful.

### Trivial
None.

## Nice-to-Haves

- Report statistical significance or variance across calibration-data seeds. All results are single numbers; given the small calibration set (256 samples), it is unclear whether the reported improvements (e.g., 14.76 vs 16.11) are statistically robust.
- Include a summary row for 70% and 80% compression in the main perplexity/accuracy tables (Table 4 includes these ratios for the quantization study, but the primary Table 1 stops at 60%).
- Test at lower compression ratios (10–30%) where models retain more capability, to see whether AdaSVD's benefits persist in regimes with practical utility.

## Removed Points

These points were raised by the input review but are excluded from the final weaknesses after cross-checking:

- **adaCR ablation confounded (input Issue 3):** The reviewer claimed adaCR alone underperforms SVD-LLM (Table 3a, AdaSVD without adaComp gives C4=66.29 vs SVD-LLM's 61.95). However, the paper's claim is that adaCR outperforms *uniform CR* (Table 3b), which it does: AdaSVD+Uniform CR beats SVD-LLM, and adding adaCR further improves. The criticism conflates adaComp and adaCR ablations.

- **Quantization orthogonality claim undermined (input Issue 5):** The claim is that AdaSVD+GPTQ outperforms SVD-LLM+GPTQ, which Table 4 supports for every entry. The fact that adding quantization to SVD hurts both methods is a known property of compounding lossy compressions, not a failure of orthogonality.

- **Equation transposition concerns and Algorithm 1 whitening description:** These are either deferred to supplementary or follow standard practice from SVD-LLM. Not verifiable flaws from the paper as presented.

- **Related work positioning, iteration analysis, baselines staged as straw-man (input Issue 1):** The paper includes standard baselines from the literature; these are not staged — prior SVD papers use the same set. The point about modest gains against SVD-LLM at 40–50% is already captured in the Major weakness about framing.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Recalibrate the framing throughout (abstract, contributions, conclusion) to accurately describe the compression regime: AdaSVD reduces *how much* performance is lost during SVD compression but does not prevent substantial degradation at 40–80% CR.
- Add a baseline for the stack-of-batch strategy that uses the same number of samples without averaging to clarify the mechanism.
- Specify clamping behavior for Eq. 19 (e.g., I_n(W) clamped to a range that keeps CR(W) ∈ [mrr, trr]).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>