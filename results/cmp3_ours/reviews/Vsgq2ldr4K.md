## Summary

The paper proposes Power Sampling, a training-free MCMC-based inference algorithm that targets sampling from the power distribution \(p^\alpha\) of a base LLM, motivated by the "distribution sharpening" hypothesis of RL post-training. The core theoretical contribution cleanly distinguishes power-distribution sampling (sum of exponents) from low-temperature sampling (exponent of sums). Empirically, on MATH500, HumanEval, GPQA, and AlpacaEval 2.0 across three model families, the method matches or outperforms GRPO on several tasks while preserving generation diversity that RL training collapses.

## Strengths

- **Clean theoretical insight (Section 4.1).** Proposition 1 and Example 1 provide a crisp mathematical demonstration of why low-temperature sampling is not equivalent to sampling from \(p^\alpha\) — a non-obvious point that prior work on temperature has largely glossed over. The "sum of exponents" vs. "exponent of sums" framing (Eq. 7–8) is genuinely illuminating.

- **Coherent motivation architecture.** The paper cleanly connects (a) the distribution-sharpening hypothesis about RL post-training, (b) the power distribution as an explicit mathematical target, and (c) a practical MCMC algorithm — giving the work clear intellectual unity from motivation to method.

- **Empirical results are substantively interesting.** The single-shot numbers in Table 1 are striking: matching or beating GRPO on several tasks *without any training*. The finding that power sampling preserves diversity (Figure 5, pass@k) while achieving near-RL single-shot accuracy addresses a recognized weakness of RL methods.

- **Self-contained method.** No verifier, no training data, no reward model — the method occupies a genuinely different point in the design space from RL post-training and opens up applications where verifiers are unavailable.

## Weaknesses

### Fatal
None.

### Major

- **\(N_{\text{MCMC}}\) — the algorithm's central compute-controlling hyperparameter — is undisclosed (Algorithm 1, line 213; Section 5.1).** The paper lists \(N_{\text{MCMC}}\) as a key hyperparameter in Algorithm 1 but never states what value was used. From Eq. (12), \(\mathbb{E}_{\text{tokens}} \approx N_{\text{MCMC}} T^2 / (4B)\). With \(T=3072\) and \(B=192\), the coefficient is \(\sim 12,288\) tokens per MCMC step per block — meaning even \(N_{\text{MCMC}}=1\) gives ~12k tokens per final sample. Without knowing this value, the reader cannot assess the computational cost of the reported results, cannot separate algorithmic effect from brute-force compute scaling, and cannot make a cost-adjusted comparison against GRPO. This is a structural gap that prevents evaluation of the method's practical viability.

- **No computational cost analysis (Section 5).** The paper frames the algorithm as a practical alternative to RL post-training ("simple," "training-free," line 49) but reports no wall-clock time, FLOPs, token generation ratios, or runtime comparison against either GRPO or standard base-model sampling. Relatedly, no MCMC acceptance rates are reported, so there is no evidence the chain is mixing efficiently rather than spending most compute on rejected proposals.

- **No variance or uncertainty quantification (Table 1).** All results are point estimates with no error bars, multiple seeds, or statistical significance tests. Several margins are small enough to fall within noise (e.g., GPQA: GRPO 39.9 vs. power sampling 38.9 on 198 questions; HumanEval: 57.3 vs. 53.7 on 164 problems). Without variance estimates, the reader cannot assess whether the reported differences are systematic.

- **Phi-3.5-mini-instruct GRPO baseline appears poorly configured (Table 1).** On Phi-3.5, GRPO achieves only 40.6% on MATH500 (base: 40.0%, negligible gain) and 13.4% on HumanEval (base: 21.3%, a *decrease* of 7.9 points). This is a notably poor result. The paper's headline claim of "+59.8% on HumanEval with Phi-3.5" rests on this comparison. The authors should either demonstrate the GRPO baseline can produce reasonable results (e.g., a version that does not degrade on HumanEval) or explicitly acknowledge this limitation and temper the claims that depend on it.

### Minor

- **"Out-of-domain outperformance" framing conflates an expected comparison (abstract, line 47, line 274).** The paper repeatedly claims power sampling "outperforms RL on out-of-domain tasks," but the GRPO baseline was trained *only on MATH problems*. It is expected that a method not trained on any specific dataset would generalize better to non-MATH domains than a model finetuned exclusively on MATH. The meaningful comparison is against the base model's own out-of-domain performance (which the paper does report and shows genuine improvement). The framing should be qualified.

- **"Dataset-free" claim is overstated (line 49).** The paper calls the method "training-free, dataset-free, and verifier-free," but \(\alpha=4.0\) and the proposal temperature \(\tau=1/\alpha\) were empirically selected on the evaluation tasks themselves (line 270: "Empirically, we find \(\alpha=4.0\)...to be most performant for reasoning tasks"), and a different temperature (\(\tau=0.5\)) was used for AlpacaEval. While much lighter than full RL training, this is dataset-dependent hyperparameter selection, not fully "dataset-free."

- **Connection to "critical windows" is asserted rather than demonstrated (line 163).** The paper claims power sampling inherently avoids critical windows by upweighting tokens with few high-likelihood future paths, citing Li et al. (2025). This is a plausible hypothesis, but no experiment directly tests whether power sampling specifically avoids critical windows or reduces reasoning failures from them.

### Trivial

- **AlpacaEval 2.0 cross-model comparisons.** AlpacaEval 2.0 scores are win rates against GPT-4-turbo normalized by response length. Base model scores vary drastically across models (1.61 for Qwen2.5-Math-7B vs. 14.82 for Phi-3.5-mini), making cross-model comparisons of "improvement" unreliable. The paper should note this.

## Nice-to-Haves

- Report \(N_{\text{MCMC}}\) and provide a compute-accuracy curve (accuracy vs. total tokens or wall-clock time across \(N_{\text{MCMC}} = 1, 2, 5, 10, 20\)) so the reader can assess the compute-accuracy tradeoff.
- Report acceptance rates for the MCMC procedure.
- Provide variance estimates (e.g., 3 seeds) for main results in Table 1.
- Qualitatively analyze cases where the MCMC chain fails to improve over the base model.
- Discuss whether results would likely hold against RL models trained on diverse data (not only MATH).

## Removed Points

- **"Reverse proposal probability computation is not discussed."** The paper does address this: line 181 states it is "easy to calculate by symmetry." While a fuller explanation would help, the criticism overstates the gap. Demoted to Nice-to-Have.
- **Speculative criticisms about computational cost without evidence.** The critic asserted that the method "may be computationally extravagant" but the paper's failure to report \(N_{\text{MCMC}}\) is the real issue — the speculative framing is removed in favor of the concrete missing-hyperparameter weakness.
- **"Better approximation to the full Bayesian posterior" comparison removed.** Not relevant to this paper.

## Novel Insights

The harsh reviewer's identification that the Phi-3.5 GRPO baseline appears broken — HumanEval drops from 21.3% (base) to 13.4% (GRPO) — is the most penetrating observation. This directly undermines the paper's strongest claimed advantage (+59.8% on HumanEval) and reveals that a headline result depends on a comparison against a demonstrably suboptimal RL baseline. The reviewers across the calibration corpus consistently penalize papers whose central empirical claim relies on a poorly-configured baseline, and this paper is vulnerable on that front.

None beyond the paper's own contributions.

## Suggestions

1. **Report \(N_{\text{MCMC}}\)** and provide a compute-accuracy tradeoff curve across different \(N_{\text{MCMC}}\) values with total token cost and wall-clock time.
2. **Add variance estimates** (multiple seeds or confidence intervals) to Table 1.
3. **Address the Phi-3.5 GRPO baseline** — either re-run with hyperparameters that avoid the HumanEval degradation, or explicitly acknowledge the limitation and temper claims that depend on it.
4. **Report acceptance rates** for the MCMC procedure.
5. **Qualify the "out-of-domain outperformance" and "dataset-free" claims** in the abstract and main text.

## Calibration Anchors

The following papers were retrieved from the human-review corpus for score calibration:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `8QTpYC4smR.md` (LLM survey) | 1.00 | R1 strong-reject | Unrelated survey paper — not comparable |
| `P49gSPmrvN.md` (UMAP discourse) | 1.00 | R1 strong-reject | Unrelated — not comparable |
| `V4Xs283LHH.md` (FlashSampling) | 2.50 | R1 1.5–3.5 | About efficient exact sampling — less novelty than current paper |
| `sK2A7Ve2co.md` (a-GPS sampler) | 2.50 | R1 1.5–3.5 | About Bayesian NN posterior sampling — less direct relevance |
| `n7iwmPacDt.md` (Polybasic Speculative Decoding) | 3.00 | R1 1.5–3.5 | About speculative decoding theory — less empirical and theoretical novelty |
| `RDFkGZ9Dkh.md` (LLMs as Markov Chains) | 5.00 | R1 3.5–5.5 | Theoretical paper with weaker empirical validation; current paper is stronger empirically but shares evaluation gaps |
| `DQfHkEcUqV.md` (Extrapolative MCMC) | 4.75 | R1 3.5–5.5 | MCMC + LLM paper with flawed validation; current paper has cleaner methodology |
| `0gDQgwjoX0.md` (Stochastic Gradient Discrete Langevin) | 4.67 | R1 3.5–5.5 | Discrete MCMC theory paper; different scope |
| `6BjEqGn1OO.md` (Timed Diarized Transcripts) | 5.25 | R1 3.5–5.5 | Different application area |
| `0xUEBQV54B.md` (Large Language Monkeys) | 5.00 | R2 4.5–6.5 | Inference-time compute scaling; rejected despite interesting results, similar evaluation gaps |
| `77gQUdQhE7.md` (Inference-Aware Fine-Tuning) | 5.67 | R2 4.5–6.5 | Accepted; cleaner evaluation than current paper |
| `VNckp7JEHn.md` (Inference Scaling Laws) | 5.75 | R2 4.5–6.5 | Accepted; extensive empirical analysis exceeding current paper |
| `Ouj6p4ca60.md` (Amortizing Intractable Inference) | 5.50 | R2 4.5–6.5 | Accepted; related inference-time method with stronger evaluation |
| `sL2F9YCMXf.md` (Energy-Based Diffusion LMs) | 6.75 | R1 5.5–7.5 | Accepted; significantly more rigorous evaluation |
| `88TC1AWV27.md` (PICASO) | 6.00 | R1 5.5–7.5 | Accepted; stronger empirical evaluation |
| `xoXn62FzD0.md` (SMC Controlled Generation) | 8.00 | R1 7.5–8.5 | Strong accept; comprehensive evaluation far exceeding current paper |
| `tyEyYT267x.md` (Interpolating AR and Diffusion) | 8.00 | R1 7.5–8.5 | Strong accept; state-of-the-art contribution |

**Round 1 bracket:** 4.5–6.5. **Narrowing:** Comparison with the 4.5–6.5 anchors shows the paper has a stronger theoretical contribution than "Large Language Monkeys" (5.00, rejected) but weaker empirical rigor than "Inference Scaling Laws" (5.75, accepted). The missing \(N_{\text{MCMC}}\) and Phi-3.5 baseline issues are more severe than the gaps in the accepted papers at 5.5–5.75.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>