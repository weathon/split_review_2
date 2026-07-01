Here is the final consolidated review.

---

## Summary
This paper identifies and characterizes the *priming vulnerability* in Masked Diffusion Language Models (MDLMs): if an affirmative token appears at an intermediate denoising step, subsequent generation can be steered toward a harmful response, even in safety-aligned models. The paper proposes *Recovery Alignment* (RA), which trains models to generate safe responses from intentionally contaminated intermediate states. Experiments on three MDLMs show RA dramatically reduces attack success rates from the priming vulnerability with minimal impact on general task performance, and also improves robustness against several conventional jailbreak attacks.

## Strengths
1. **Novel vulnerability with clean isolation.** The priming vulnerability is genuinely specific to the iterative denoising mechanism of MDLMs, distinct from ARM prefilling attacks. The anchoring attack (Section 4.1) cleanly isolates the issue: injecting a single token at step 1 raises ASR from 2% to 21% on LLaDA Instruct (Figure 2), providing causally informative evidence.

2. **Strong empirical mitigation.** RA reduces ASR dramatically on safety-aligned models (Table 2). For LLaDA Instruct with the anchoring attack at t=4, ASR drops from 44.0% to 1.3%; at t=16, from 88.7% to 8.3%. The RA w/o inter ablation cleanly confirms that training on contaminated intermediate states is the critical ingredient — not general RLHF.

3. **Utility preservation across diverse benchmarks.** Table 4 shows RA causes no substantial degradation across 11 benchmarks (LLaDA average: 52.2% original vs. 52.6% RA), demonstrating that the safety gains do not come at a large capability cost.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor
1. **Theorem 4.1's monotonicity assumption has limited justification in the main paper.** The theorem assumes log π_θ(\tilde{r}_{t+1}=r | q, r_t) ≥ log π_θ(\tilde{r}_1=r | q, r_0) for all t. The paper provides a plausible intuitive justification (more tokens of r are already fixed at later steps, concentrating probability mass) and references empirical validation in Appendix C.2. However, the main-paper argument alone is not fully rigorous, and the resulting bound is weakened by the 1/T factor (T=128). Since First-Step GCG works well empirically regardless (and the paper acknowledges the bound's looseness), this does not undercut the paper's contributions, but the theoretical framing could be tempered.

2. **MC GCG comparison would benefit from fuller disclosure.** Table 1 shows First-Step GCG outperforming Monte Carlo GCG (58% vs. 20% ASR on LLaDA Instruct) while being 20× faster. The paper attributes this to inherent MC variance, but the specific MC hyperparameters (number of trajectories, gradient estimator, variance reduction techniques) are only in the stripped appendix. Clarifying that MC GCG was configured reasonably would strengthen the fairness claim. (The paper's main RA defense does not depend on this comparison.)

3. **Residual failure modes are noted but not analyzed.** RA's ASR remains high under late interventions (t=32: 50.7% on LLaDA) and the DiJA attack (35.7% on LLaDA). The paper mentions these cases but does not qualitatively analyze what kinds of failures occur — e.g., do they produce refusals that leak information, or completions that are semantically unrelated? Brief characterization would make the limitations concrete.

4. **HumanEval drop is notable for code-related use.** RA reduces HumanEval from 22.0 to 17.1 on LLaDA (~22% relative decrease). While the 11-benchmark average is stable, this specific drop is worth flagging for applications involving code generation, and the paper does not probe whether it is statistically significant.

5. **Reward hacking observation is underexplored.** Section 6.4 notes that large t_max "destabilizes training" and causes the model to generate "meaningless" responses, but no analysis is provided (e.g., prevalence of meaningless responses, impact on ASR evaluation).

6. **Limitations section is narrow.** The discussion focuses only on a DPO-style alternative. Other limitations — such as reliance on GRPO hyperparameters, dependency on reward model quality, and scope of the evaluation (100 behaviors, GPT-4o as safety judge) — are not discussed.

### Trivial
None.

## Nice-to-Haves
- Direct behavioral analysis of whether RA changes the distribution of intermediate states during generation (e.g., comparing harmful-token probabilities at each step between RA-trained and original models under attack).
- Clarification of how t_min and t_max were selected for main experiments (tuned on a validation set?).
- A brief remark on whether the priming vulnerability might extend to continuous DLMs.
- Statistical significance tests for key comparisons in Tables 2–4.

## Removed Points
These points are flagged to be removed; treat them with caution.

- **"RA's robustness against conventional jailbreaks is mixed" / "abstract may overstate":** REMOVED. The data in Table 3 shows RA improves ASR in 8 out of 9 settings versus the original model. The single regression (MMaDA + ReNeLLM: 79.3→81.7) is within one standard deviation. The paper's claim "improves robustness against conventional jailbreak attacks" is factually supported. Residual high ASR on ReNeLLM (~72%) is acknowledged by the paper ("RA remains imperfect").

- **"MMaDA was not meaningfully safety-aligned, so comparisons partly reflect general safety training":** REMOVED. The paper transparently reports MMaDA's 79.7% baseline ASR, and comparisons against SFT and DPO (which also provide general safety training) control for this.

- **"Appendix C.2 not visible" / "theorem dependent on unseen appendix":** REMOVED per hard rule — appendices are stripped by the parser; the paper states empirical validation exists in Appendix C.2.

- **"No discussion of continuous DLMs" / "missing analysis of prior alignment" / "statistical testing":** REMOVED as either scope creep or standard practice not required by the field.

## Novel Insights
Beyond the paper's own contributions, the reviewer input surfaces a useful observation: the causal chain connecting the RA defense mechanism to the empirical results is theoretically well-motivated but not directly verified at the behavioral level (i.e., whether RA actually changes the token-level distribution at intermediate states). A dedicated analysis measuring intermediate-state probabilities would strengthen the mechanistic claim.

## Suggestions
- Report MC GCG hyperparameters (number of trajectories, gradient estimator, variance reduction) explicitly in the main paper, or clarify that the comparison demonstrates efficiency advantages rather than peak performance.
- Relax the theoretical framing of Theorem 4.1 by acknowledging the 1/T looseness upfront and positioning the theorem as motivation.
- Add a qualitative analysis of RA's failure modes (DiJA, late interventions) to characterize what kinds of harmful outputs survive.
- Discuss whether the HumanEval drop is statistically significant.
- Broaden the limitations section to cover evaluation scope, reward model dependency, and training stability.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>