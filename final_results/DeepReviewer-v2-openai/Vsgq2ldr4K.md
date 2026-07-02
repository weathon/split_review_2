## Summary
# Final Review Report

## Summary

This paper proposes "power sampling," a training-free MCMC-based inference algorithm that targets the power distribution $p^\alpha$ of a base language model. The core idea is to iteratively resample token subsequences, accepting/rejecting based on the base model's own likelihood ratio, producing samples that concentrate in high-likelihood regions — mimicking the "distribution sharpening" effect of RL-based post-training (e.g., GRPO) without any training, reward model, or verifier. 

Experiments across three model families (Qwen2.5-Math-7B, Qwen2.5-7B, Phi-3.5-mini-instruct) and tasks (MATH500, HumanEval, GPQA, AlpacaEval 2.0) show that power sampling nearly matches GRPO on in-domain math reasoning (MATH500) and outperforms it on out-of-domain coding (HumanEval) and general helpfulness (AlpacaEval 2.0). The method also preserves generation diversity at high sample counts, unlike GRPO which suffers from diversity collapse.

**Strengths:** The paper addresses a timely and well-motivated question — whether RL-posttraining creates genuinely new capabilities or merely sharpens existing base-model distributions. The training-free, verifier-free nature of power sampling is a conceptually appealing alternative to RL-based approaches. The mathematical derivation of Proposition 1 (distinguishing power distribution sampling from low-temperature sampling) is clean and pedagogically valuable. The pass@k diversity preservation result, if verified, addresses a known limitation of RL fine-tuning.

**Key weaknesses:** (1) The computational cost of the iterative MCMC procedure ($O(T^2)$ token generation per output) is not disclosed in the abstract or adequately quantified in experiments, potentially misleading readers about practical feasibility. (2) No MCMC convergence diagnostics are reported (trace plots, R-hat, ESS), so there is no evidence that the sampler actually converges to $p^\alpha$. (3) Table 1 reports all results as point estimates without variance or significance tests, making it impossible to assess statistical reliability. (4) The GRPO baseline on Phi-3.5-mini-instruct shows near-zero improvement on MATH500 and degrades on HumanEval, raising questions about training stability and the fairness of out-of-domain comparisons. (5) The "confidence" metric (Eq. 13) is actually negative predictive entropy, not correctness confidence; the causal link drawn between distribution sharpness and accuracy is conflated.

**Overall assessment:** The paper presents a thought-provoking idea with clean mathematical motivation and promising initial results. However, the empirical support as presented is incomplete — missing statistical rigor, convergence verification, and honest computational-cost disclosure prevent the current version from being a definitive demonstration that "base models are smarter than we think" through sampling alone. The core methodological contribution (MCMC for $p^\alpha$) is potentially valuable, but the paper would benefit from substantial strengthening of the empirical evaluation and a more measured framing of its claims.

## Strengths
1. **Timely and well-motivated research question.** The paper addresses a core debate in the LLM reasoning community: whether RL-posttraining generates genuinely new capabilities or merely sharpens existing base-model distributions. By approaching this from the sampling side, the paper offers a novel perspective that could influence how the field thinks about inference-time compute.

2. **Clean mathematical contribution in Proposition 1.** The distinction between power-distribution sampling and low-temperature sampling is rigorously derived, with a clear demonstration that the two are not equivalent even though commonly conflated. The "sum of exponents vs. exponent of sums" framing (Eqs. 7-8) and the accompanying Example 1 provide excellent pedagogical value. Observation 1 (power distribution upweights tokens with few but high-likelihood future paths) gives an intuitive understanding of why $p^\alpha$ might help with planning/pivotal-token problems.

3. **Training-free and verifier-free paradigm.** The core appeal of power sampling is that it requires no training, no curated datasets, and no verifier — only access to the base model's log-likelihoods. If validated, this would significantly broaden the applicability of reasoning enhancement to domains where verifiable rewards are unavailable. The paper correctly identifies this as an advantage over RL-based methods.

4. **Pass@k diversity preservation.** The finding that power sampling maintains high pass@k at large sample counts, where GRPO plateaus, is the most practically significant empirical result. If a method can match GRPO's single-shot accuracy while preserving the base model's diversity, that addresses a recognized limitation of RL fine-tuning. This result deserves careful further investigation.

5. **Multi-model and multi-task evaluation.** Testing across three model families (Qwen2.5-Math, Qwen2.5-base, Phi-3.5) and four task types (math, code, science QA, general helpfulness) provides broader evidence than evaluations on a single model/benchmark. The inclusion of a non-verifiable task (AlpacaEval 2.0) is particularly valuable for probing generalizability claims.

6. **Likelihood and confidence analysis (Figure 4).** The histograms of output log-likelihoods and negative entropies provide useful insight into how power sampling redistributes probability mass relative to the base model and GRPO. The observation that GRPO outputs are concentrated at the highest-likelihood peak while power sampling maintains spread aligns well with the diversity results.

## Weaknesses
### W1. Unacknowledged and unquantified computational cost (Severity: Major)
**Evidence:** Page 1 - Abstract; Page 6 - Section 4.3, Eq. (12); Page 7 - Sampling Algorithm description.

The abstract describes the algorithm as "simple" without disclosing the $O(T^2)$ inference-time token generation cost (Eq. 12: $\mathbb{E}_{\text{tokens}} \approx N_{\text{MCMC}} T^2 / (4B)$). With $T=3072$ and $B=192$, even moderate $N_{\text{MCMC}}$ yields 100k+ tokens per single output — orders of magnitude beyond standard sampling. Furthermore, Eq. (12) implicitly assumes a 100% acceptance rate ($\rho=1$), but practical MH acceptance rates are often well below 1.0. No wall-clock time or FLOPs comparison against GRPO is reported anywhere. **Impact:** Readers cannot assess whether power sampling's benefits justify its inference budget, which is the central practical tradeoff. A practitioner considering this method needs to know: is it cheaper than GRPO training for their use case?

**Recommended fix:** (a) Add one sentence in the abstract quantifying the cost tradeoff. (b) Report actual acceptance rates and wall-clock times alongside GPUs used. (c) Replace Eq. (12) with $\mathbb{E}_{\text{tokens}} \approx N_{\text{MCMC}} T^2 / (4B\rho)$ and report empirical $\rho$. (d) Add a table comparing total compute (FLOPs or GPU-hours) of power sampling vs. GRPO training + inference.

### W2. No MCMC convergence diagnostics (Severity: Major)
**Evidence:** Page 5 - Section 4.3, acknowledging exponential mixing time but providing no convergence verification.

The paper cites exponential mixing time as a key challenge for MCMC in high-dimensional token space, and proposes a block-wise annealing schedule as mitigation. However, it reports zero convergence diagnostics — no trace plots, no Gelman-Rubin R-hat statistics, no effective sample size (ESS) computation. Without these, there is no evidence that Algorithm 1 actually samples from $p^\alpha$ rather than some initialization-dependent distribution. This is especially concerning because the paper's central claim ("sampling from $p^\alpha$ matches GRPO") collapses if the sampler does not converge. **Impact:** The core empirical results are contingent on an unverified sampling target. This is a fundamental methodological gap.

**Recommended fix:** (a) Report trace plots of log-likelihood for a representative set of 20 prompts across MCMC iterations. (b) Compute and report ESS/N_MCMC ratio. (c) Run 3 independent chains with different initializations and report R-hat. (d) If these diagnostics are too expensive, explicitly state this limitation and characterize the paper's results as approximate samples.

### W3. Missing variance and statistical significance (Severity: Major)
**Evidence:** Page 7 - Table 1 and Section 5.2.

All results in Table 1 are single-point estimates with no standard deviations, confidence intervals, or significance tests. Several key comparisons involve small gaps (e.g., GPQA Qwen2.5-Math-7B: power sampling 0.389 vs GRPO 0.399, a 1% difference). Without variance estimates, readers cannot determine whether observed differences are meaningful or merely sampling noise. This is especially critical for the Phi-3.5-mini-instruct results where GRPO is unstable (MATH500: 0.406 vs base 0.400). **Impact:** The paper's headline claims ("matches and even outperforms GRPO") rest on point estimates that may not be statistically significant. The comparison cannot be properly evaluated.

**Recommended fix:** (a) Report mean $\pm$ std over at least 3 independent runs for all entries in Table 1. (b) Add paired bootstrap or McNemar significance tests for the power sampling vs. GRPO comparison. (c) Mark significant differences ($p<0.05$) explicitly.

### W4. Unstable GRPO baseline on Phi-3.5 confounds OOD comparison (Severity: Major)
**Evidence:** Page 7 - Table 1, Phi-3.5-mini-instruct results; Page 7 - Models paragraph.

On Phi-3.5-mini-instruct, GRPO (trained on MATH) achieves only 0.406 on MATH500 (0.6% above base 0.400) and drops to 0.134 on HumanEval (37% relative decline from base 0.213). The paper attributes OOD outperformance of power sampling to generalizability, but an equally plausible explanation is that GRPO training failed or caused catastrophic forgetting. This is a fundamental confound: GRPO was trained only on MATH data, so its OOD degradation may reflect training distribution mismatch rather than any limitation of RL-based reasoning. **Impact:** The paper's claim that power sampling "outperforms RL on out-of-domain tasks" is confounded by the training distribution gap. Without a GRPO model trained on a broader corpus (MATH + code) or multi-task objective, the comparison is not apples-to-apples.

**Recommended fix:** (a) Add a discussion paragraph explicitly acknowledging the GRPO training confound on Phi-3.5. (b) Train GRPO on a combined MATH + code dataset and re-evaluate. (c) Alternatively, use a stronger RL baseline that does not degrade on coding tasks. (d) Separate the comparison into in-domain (fair) and out-of-domain (confounded) with appropriate caveats.

### W5. "Confidence" metric conflates entropy sharpness with correctness (Severity: Major)
**Evidence:** Page 8 - Section 5.3, Eq. (13) and surrounding analysis.

Eq. (13) defines "confidence" as the average negative entropy of next-token distributions — a measure of how peaked the predictive distribution is, not of correctness. A model confidently producing wrong answers would score high on this metric. The paper then states that high confidence regions "correspond to regions of higher likelihood and correct reasoning," but this causal link is not established. The metric measures certainty, not accuracy. The conclusion that "power sampling and GRPO sample from similarly high confidence regions" only indicates similar distributional sharpness, not similar reasoning correctness. **Impact:** The analysis section draws an unwarranted causal link between distribution sharpness and reasoning quality, which could mislead readers about the mechanism underlying power sampling's effectiveness.

**Recommended fix:** (a) Rename "confidence" to "distribution sharpness" or "negative predictive entropy." (b) Explicitly state that this measures predictive peakedness, not correctness. (c) Add an analysis correlating sharpness with actual accuracy on a per-problem basis to support the claimed relationship.

### W6. GRPO hyperparameter selection fairness (Severity: Moderate)
**Evidence:** Page 7 - Models paragraph.

The paper states that for Phi-3.5, it "use[s] a set of hyperparameters selected from Abdin et al. (2024) that avoids training instabilities." However, Abdin et al. (2024) is the Phi-4 technical report, which may not have used GRPO or the same training configuration. The paper does not report key hyperparameters (learning rate, KL penalty coefficient, number of epochs, group size) for any of the GRPO baselines. Without this information, readers cannot assess whether the GRPO baselines are reasonably well-tuned or whether power sampling benefits from a poorly configured competitor. **Impact:** The GRPO-vs-power-sampling comparison may not reflect best-practice RL performance, especially on models where GRPO is known to be sensitive to hyperparameters.

**Recommended fix:** (a) Report all GRPO hyperparameters in a table. (b) Include a sensitivity analysis showing GRPO performance across different hyperparameter settings. (c) For Phi-3.5, verify that the chosen hyperparameters indeed produce optimal or near-optimal GRPO performance.

### W7. AlpacaEval 2.0 results may reflect LLM judge bias (Severity: Moderate)
**Evidence:** Page 7 - AlpacaEval 2.0 description; Page 7 - Table 1.

AlpacaEval 2.0 uses GPT-4-turbo as an automated judge. GPT-4 judges have known biases (length preference, style preference, self-preference). Power sampling produces longer responses (679 vs 600 tokens) with different likelihood characteristics; the observed win rate advantage could partly reflect these stylistic differences rather than genuine helpfulness improvements. **Impact:** The claim that power sampling "generalizes to domains beyond verifiability" is partially supported by a metric with known biases, weakening the generalizability argument.

**Recommended fix:** (a) Acknowledge LLM-as-judge bias as a limitation. (b) Report correlation between response length and win rate. (c) Consider a small-scale human evaluation (50-100 samples) to validate the AlpacaEval trends.

### W8. Lack of sensitivity analysis for key hyperparameters (Severity: Moderate)
**Evidence:** Page 7 - Sampling Algorithm paragraph.

The paper reports using $\alpha=4.0$, $B=192$, $T_{\max}=3072$, and $N_{\text{MCMC}}$ (unspecified value) based on empirical tuning, but no sensitivity analysis is provided. How does performance change with $\alpha$ (e.g., 1.0, 2.0, 8.0)? How sensitive is it to block size $B$? What is the tradeoff between $B$ and $N_{\text{MCMC}}$? Without this analysis, the reported results may reflect lucky hyperparameter choices, and practitioners cannot adapt the method to new models or tasks. **Impact:** The method's robustness is unknown, limiting reproducibility and practical adoption.

**Recommended fix:** Add a sensitivity analysis (in appendix if space-constrained) showing: (a) performance vs. $\alpha$ over a grid $\{2,4,8\}$, (b) performance vs. $B$ over $\{64,128,192,256\}$, (c) performance vs. $N_{\text{MCMC}}$ over at least 3 values, (d) interaction between $\alpha$ and the proposal temperature.

### W9. Pass@k claims overstate the advantage (Severity: Minor)
**Evidence:** Page 9 - Figure 5 caption and data table.

The caption claims "our performance curve is strictly better than both GRPO and the base model." However, the data shows that at k=14-16, both Ours and Base achieve 0.98. The curves converge. "Strictly better" is mathematically incorrect — the base model catches up at high k. The correct description is that power sampling outperforms in the low-to-mid k regime (k=2 to k=10) before converging. Additionally, pass@k on a 500-problem set has non-trivial standard error ($\approx \sqrt{p(1-p)/500}$), which the plot omits. **Impact:** The overstatement reduces precision but does not change the core finding; this is a presentation fix.

**Recommended fix:** Replace "strictly better" with "consistently better for low-to-mid k (k ≤ 10)" and add confidence bands to the pass@k plot.

### W10. Conclusion lacks limitation disclosure (Severity: Minor)
**Evidence:** Page 9 - Conclusion section.

The conclusion is purely positive, stating results "on par with and sometimes even better than" RL and pointing to "a promising direction." None of the paper's significant limitations (computational cost, convergence unverified, GRPO baseline confounds, missing variance) are acknowledged. **Impact:** Omitting limitations reduces scientific credibility and can mislead readers about the maturity of the approach.

**Recommended fix:** Replace the generic final sentence with a structured conclusion: (1) what has been shown, (2) key limitations, (3) specific next steps. See annotation on Page 9 - Conclusion for a concrete rewrite.

## Score
**Final Score: 5/10**

**Rationale:** The paper presents an intriguing idea — approximating the effect of RL post-training through inference-time MCMC sampling from the base model's power distribution — with clean mathematical motivation for why $p^\alpha$ differs from low-temperature sampling. The core research question (can sampling alone match RL?) is timely and important. However, the current empirical validation contains several significant gaps that prevent the paper from being a definitive demonstration:

- **Evidence sufficiency (low):** No variance estimates, significance tests, or MCMC convergence diagnostics are reported. Without these, the headline comparisons cannot be properly evaluated.
- **Fairness of comparison (low):** The GRPO baseline on Phi-3.5-mini-instruct shows signs of training instability, confounding the out-of-domain comparison that is central to the paper's claims.
- **Computational honesty (low):** The substantial $O(T^2)$ inference-time cost of power sampling is not disclosed in the abstract or adequately quantified, creating a misleading impression of simplicity.
- **Novelty relative to prior work (moderate):** The Algorithm 1 MH+resampling structure is similar to Faria et al. (2024); the key distinction (targeting $p^\alpha$ without external reward) is clearly stated but the incremental nature could be more explicitly acknowledged.
- **Methodological soundness (moderate):** The mathematical derivation of Proposition 1 is rigorous, but the practical algorithm's convergence to the claimed target distribution is unverified.

The paper's strengths — clean motivation, a testable hypothesis about distribution sharpening, and the diversity-preservation result — are real but currently outweighed by the empirical gaps. A revised version addressing the statistical rigor, convergence verification, and computational honesty could substantially raise this score. External literature verification was unavailable in this run (Retrieval-Disabled Mode); novelty and comparison conclusions are marked as deferred manual verification, which may affect the score if significant prior work overlaps are identified.