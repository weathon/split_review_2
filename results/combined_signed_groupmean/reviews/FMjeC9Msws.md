## Summary

This paper conducts a very large-scale (400k+ GPU-hours) empirical study of RL training recipes for LLMs, proposing a sigmoidal compute-performance curve (Equation 1) that models pass rate on in-distribution validation data as a function of training compute. The authors use this curve-fitting framework to analyze which design choices affect asymptotic performance (A) vs. compute efficiency (B), and combine the best choices into the SCALERL recipe. They demonstrate that SCALERL's training trajectory can be extrapolated from 50k→100k GPU-hours and scale across model sizes, batch sizes, and generation lengths.

---

## Strengths

1. **Scale of experimentation.** The paper reports over 400,000 GPU-hours of RL experiments on GB200 GPUs, including a single 100,000 GPU-hour run — substantially larger than typical academic RL-for-LLM studies. This scale enables observation of dynamics (e.g., methods overtaken at larger scale) invisible at smaller budgets. The leave-one-out ablation at 16k GPU-hours per variant is unusually thorough. **[impact=+9.15]**

2. **Cross-recipe sigmoid comparison (Figure 2).** Placing multiple published methods (DeepSeek GRPO, Qwen DAPO, Magistral, MiniMax) on a common scaling curve is a useful visualization. The observation that some methods differ in asymptotic performance (A) while others mainly differ in efficiency (B) is one of the paper's most interesting empirical findings. **[impact=+8.32]**

3. **Transparent limitations.** Section 7 explicitly acknowledges that generalization beyond the training distribution is not fully characterized, that in-distribution validation is the focus, and that the recipe is not claimed to be final. This candor helps readers calibrate what is and isn't demonstrated. **[impact=+4.72]**

---

## Weaknesses

### Fatal

None.

### Major

1. **Overclaimed framing relative to pre-training scaling laws.** The paper's title ("The Art of Scaling Reinforcement Learning Compute"), abstract ("brings RL training closer to the predictability long achieved in pre-training"), and introduction ("borrowing from the well-established concept of scaling laws from pre-training") draw a strong analogy to pre-training scaling laws. However, what is demonstrated is that **in-distribution validation accuracy** (pass rate on held-out prompts from the same Polaris-53k distribution) follows a sigmoidal trajectory that can be extrapolated at modest ratios (2×, e.g., 50k→100k GPU-hours). This is a useful descriptive finding about training convergence, but it is qualitatively different from pre-training scaling laws which predict test loss across different model sizes, data quantities, and compute allocations. The paper's own Section 7 acknowledges this limitation, but the framing in the title, abstract, and introduction sets expectations that the experiments do not meet. The predictive framework is a tool for monitoring convergence on the training distribution, not a law that guides *a priori* compute allocation decisions. **[impact=-9.93]**

2. **Cross-method comparison conditions are unclear.** Figure 2 claims SCALERL achieves SOTA, showing parameter fits for DeepSeek (GRPO), Qwen (DAPO), Magistral, and MiniMax alongside SCALERL. The main text does not state whether these comparisons use the same base model (was it Llama-4-8B for all?), the same training data (Polaris-53k?), the same evaluation protocol (mean@16 on 1,000 held-out Polaris prompts?), and the same compute budget. Details are deferred to Appendix A.17. Without this clarification, differences in fitted A and B parameters could reflect confounding factors (different base models, different data mixtures, different evaluation protocols) rather than intrinsic differences in recipe scalability. The SOTA claim is not interpretable without knowing whether the comparison is controlled. **[impact=-10.00]**

3. **No uncertainty quantification on any result.** Every curve, fitted parameter, and extrapolation in the paper comes from single runs. There are no multiple seeds, confidence intervals on fitted A/B/C_mid parameters, or uncertainty bands on extrapolated curves. For a paper whose central framing is a *predictive framework*, this is a significant gap. Without error bars, the reader cannot assess whether differences in A between methods (e.g., 0.61 vs. 0.59) are meaningful or within noise, or whether the extrapolation match is robust across initialization and data shuffling seeds. Running even 2–3 seeds for the most important conditions (the 100k run, the LOO comparison) would have strengthened claims substantially. **[impact=-9.99]**

### Minor

4. **Suspiciously identical fitted asymptotes in Figure 4a.** Three different off-policy RL setups (PPO-off-policy-1, PPO-off-policy-8, PipelineRL-8-off-policy) are all reported with A=0.520 exactly (to three decimal places). While the paper notes they achieve "similar" asymptotic performance, exact numerical identity is unusual and raises questions about whether the fitting procedure is constraining A or the runs were not trained long enough to observe asymptotic differentiation. **[impact=-0.33]**

5. **Modest extrapolation range.** The headline 100k GPU-hour demonstration extrapolates from 50k→100k (2×). The LOO experiments extrapolate from 8k→16k (2×). This is a consistency check more than a strong test of predictive power. Demonstrating extrapolation from much shorter runs (e.g., 10k→100k, a 10× range) would provide more convincing evidence for the predictive claims. **[impact=-0.00]**

---

## Nice-to-Haves

- Report numerical AIME-24 pass rates at key compute budgets so results are usable by practitioners comparing against other work.
- The paper could explicitly compare how the sigmoidal fit (Equation 1) would change if applied to out-of-distribution evaluation (downstream benchmarks) vs. in-distribution validation, to characterize generalization more precisely.

---

## Removed Points

These points from the input review are flagged for removal with justification:

1. **"Paper never reports raw numerical values"** — REMOVED (factually wrong: Figures 2 and 5 both contain tables with numerical A, B, C_mid values).
2. **"Internal tension between scientific framework and recipe"** — REMOVED (this is a framing preference, not a specific verifiable weakness; many papers legitimately make both contributions).
3. **"FP32 precision fix is a bug fix, not algorithmic innovation"** — REMOVED (identifying and fixing a numerical precision issue that limits performance is a valid empirical contribution, not a weakness).
4. **"Lacks formal comparison with pre-training scaling laws"** — REMOVED (this demands something outside the paper's stated scope).
5. **"Missing related works"** — REMOVED per policy (cannot be verified without external sources).
6. **Criticisms about missing appendix content** — REMOVED per policy (appendices are stripped by the parser; they exist in the original submission).

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. Clarify in the main text whether the Figure 2 comparisons use controlled conditions (same base model, data, evaluation protocol) or are sourced from published results. If controlled, state this explicitly; if not, state what differs and temper the SOTA claim accordingly.
2. Add multiple seeds and report bootstrapped confidence intervals on fitted parameters for the flagship 100k run and the LOO ablation.
3. Re-frame the contribution as a systematic large-scale empirical study of RL recipe scaling (which is genuinely valuable on its own terms) rather than drawing strained analogies to pre-training scaling laws.
4. Explain why the three methods in Figure 4a all produce A=0.520 (exact numerical identity), or use a fitting procedure that reports finer granularity.
5. Demonstrate extrapolation from a wider range (e.g., 10k→100k) to substantiate the predictive claims more convincingly.

---

## Score and Decision

**Calibration anchors consulted (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison to this paper |
|------|-----------|-------|-----------|--------------------------|
| xGM5shdGJD (Hitchhiker's Guide) | 5.20 | R1 | Yes | Similar profile (strong empirical data, methodological concerns about scaling law estimation). Rejected. |
| BDisxnHzRL (Downstream Scaling Laws) | 4.25 | R1 | Yes | Similar (strong empirical work, core claims contested). Rejected. |
| cijO0f8u35 (Math Reasoning Scaling) | 5.25 | R2 | Yes | Similar (solid experiments, limited scope/novelty concerns). Rejected. |
| F0GNv13ojF (RL Reward Design) | 5.17 | R2 | Yes | Similar profile (strong experiments, mixed reviews on novelty). Rejected. |
| D0XpSucS3l (Agents & World Models Scaling) | **4.50** | R3 | Yes | **Closest anchor.** Both are large-scale empirical scaling studies in RL-adjacent settings with fundamental concerns about proxy metrics and claim justification. Rejected. |
| VNckp7JEHn (Inference Scaling Laws) | 5.75 | R2 | Yes | Accepted, but had stronger theoretical grounding and cleaner methodology than our paper. |
| KnoS9XxIlK (Multi-Power Law) | 6.00 | R1 | Yes | Accepted; had clearer empirical validation and less contested framing. |
| iZeQBqJamf (Over-training Scaling) | 6.50 | R1 | Yes | Accepted; strong experimental rigor with multiple seeds and uncertainty quantification. |

**Round 1 bracket**: 4.0–5.5, based on comparison with topically similar scaling-law papers.

**Narrowing**: The closest anchor D0XpSucS3l (4.50) shares our paper's central tension — strong systematic empirical work at scale, but core claims about "scaling laws" that are contested on methodological grounds. Our paper's three major weaknesses (overclaimed framing, unclear comparison conditions, no uncertainty quantification) are each rated as decisive (~-10 impact by the scoring model). While the scale of experimentation (+9.15) and cross-recipe comparison (+8.32) are genuine strengths, they do not compensate for the foundational issues in the paper's central scientific claim. Papers with cleaner methodology and comparable empirical contributions score in the 5.75–6.50 range (accepted); our paper sits clearly below that threshold.

**Final score: 4.5, Decision: Reject.**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>