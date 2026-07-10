Now I have a clear picture. Let me compile the final review.

## Summary
This paper investigates failure modes of naive output alignment in 1-bit post-training quantization (PTQ) for LLMs, identifying three key problems: (i) layer-wise output matching does not guarantee block-level loss reduction, (ii) quantization errors accumulate across layers, and (iii) naive output alignment degrades attention mechanisms. The paper proposes a selective output-matching strategy that applies the Output Error objective (Eq. 3) to only the last FC layer per block, combined with an Attention Matrix Preservation (AMP) mechanism, using ARB-RC weight alignment for remaining layers. Experiments on OPT (1.3B–30B) and LLaMA-2/3 (7B–13B) show consistent perplexity and zero-shot accuracy improvements over prior 1-bit PTQ methods.

## Strengths
- **Section 3's diagnostic analysis is the paper's strongest contribution.** The empirical demonstration that layer-wise output matching can *increase* block-level loss (Fig. 1), that activation-conditioned error diverges from true output error as depth increases (Fig. 2), and that token-similarity matrices drift during quantization—these findings are well-designed, clearly presented, and genuinely informative. They identify real failure modes in ARB-X that are not obvious from loss values alone. (weight: 11.13)
- **Consistent empirical improvement across a wide range of models and benchmarks.** The method outperforms every baseline (PB-LLM, BiLLM, ARB-RC, ARB-X) on nearly every metric across OPT 1.3B–30B and LLaMA-2/3 7B–13B. Gains are meaningful—e.g., OPT-1.3B C4 perplexity: 27.70 (ARB-RC) → 24.69 (Ours), OPT-2.7B C4: 21.46 → 19.90—and hold across model scales. (weight: 10.81)
- **The method components are directly motivated by the diagnosed problems.** The Output Error objective (Eq. 3) directly addresses the error-accumulation problem identified in §3.2; AMP directly addresses the attention-degradation problem identified in §3.3; the selective strategy directly addresses the block-level mismatch problem identified in §3.1. This coherence between diagnosis and treatment is a virtue. (weight: 7.92)

## Weaknesses

### Fatal
None.

### Major
- **Mathematical ambiguity in the AMP formulation (Eq. 9–11) that affects reproducibility.** In Eq. (9), the first line writes the Frobenius norm of the element-wise product ‖A⊙B‖ while the second line converts to Tr[A^T B] (the Frobenius inner product), which are different quantities—the norm squares each element product while the inner product does not. In Eq. (10), the AMP mask is defined as sign(Diag(…)), outputting values in {−1, 1}. The update rule in Eq. (11) uses M^r in (1−M^r) and M^r directly; for M=−1 this yields α_r = 2α_r − α_r^*, pushing away from the closed-form optimum—an effect that is not discussed and likely unintended. If the intent is a binary {0, 1} mask, sign is the wrong function. This underspecification makes the update rule ambiguous and the method difficult to reproduce as written.
- **Attribution gap—the method's improvement is not fully decomposed across its components.** Per §4.2, the method applies output matching to only the last FC layer per block (~14% of layers) while using ARB-RC weight alignment for the remaining ~86% of layers. The existing ablations (Tables 3, 4) show that both Output Error and AMP independently help, but they do not isolate: (a) whether the selective strategy itself (vs. full-layer output matching) is beneficial, or (b) whether the improvement on the last FC layer would persist if the same selective strategy were applied with ARB-X's Activation-conditioned Error instead of Output Error. Without these ablations, the reader cannot attribute the improvement to specific components.

### Minor
- **The PTB result for LLaMA-2-7B (perplexity 3166 vs. ARB-RC's 763.19) is worse than the baseline, yet the paper dismisses it by saying "the metric cannot provide a meaningful evaluation" (line 233).** This is a weak post-hoc explanation. While PTB results are generally high for LLaMA-2-7B across all methods, the proposed method is notably worse than ARB-RC on this specific setting while claiming consistent improvement elsewhere. A genuine explanation (or removal of this specific result) would be more informative.
- **The choice to apply output matching only to the last FC layer per block is not empirically motivated.** The paper states it has "the most direct impact on the block loss" (§4.2) but provides no ablation comparing different layer choices (first, middle, random, or all layers). An ablation substantiating this design choice would strengthen the paper.
- **Missing implementation details that affect reproducibility.** What constitutes a "block" and "last fully connected layer" is not specified for OPT vs. LLaMA architectures. Calibration data size and composition are not reported, and whether the same calibration data is used consistently across methods is not stated.
- **Contribution 1 overstates what was done.** The paper claims to "systematically examine the influence of calibration data on 1-bit post-training quantization" (line 27), but §3 examines failure modes of output alignment strategies using a fixed calibration set, not the influence of different calibration data (distribution, size, sampling strategy). The contribution should be reframed as an analysis of failure modes in output alignment.

### Trivial
- The references include two entries for PiQA (Bisk et al., 2020a and 2020b) that appear to be the same paper listed twice.
- The paper uses "1-bit" throughout, but the methods (including the proposed one) operate at ~1.06–1.11 bits due to scaling factors. While consistent with the literature, the title and abstract could be more precise.

## Nice-to-Haves
- Report variance (mean ± std) across calibration subsets or calibration runs. Single-point estimates make it hard to assess whether reported improvements (e.g., 0.22–2.22 PPL reduction) are statistically reliable. However, this is not standard practice in current PTQ literature and the baselines also report single numbers, so this is a nice-to-have rather than a requirement.
- Include a brief overhead analysis (runtime, memory) in the main text rather than deferring entirely to the appendix.

## Removed Points
- **Variance/statistical significance not reported**: All baselines in the paper also report single numbers without variance, which is standard practice for this class of quantization papers. Demand for significance testing is disproportionate here.
- **Overhead analysis deferred to appendix**: The paper notes overhead analysis is in Appendix D, which the parser stripped. The paper should not be penalized for content that exists in the original submission.
- **Eq. (2) typo (both terms identical)**: The original text shows ∥X̂Ŵ−X̂Ŵ∥²_F, but the surrounding description and the trace expansion confirm the intended correct form (∥X̂W−X̂Ŵ∥²_F). This is a parser formatting artifact.
- **Pure formatting nitpicks about table bold formatting**: These are parser artifacts, not author errors.

## Novel Insights
The review reinforces that the paper's primary contribution is Section 3's diagnostic analysis, which cleanly identifies failure modes of naive output alignment in 1-bit LLM quantization. The attribution gap concern (method ~86% ARB-RC) is a genuine limitation, but it is partially mitigated by the existing component-level ablations (Tables 3 and 4). The AMP mathematical ambiguity stands out as the most actionable concern. No genuinely novel synthesis emerges beyond the paper's own claims.

## Suggestions
1. **Clarify the AMP formulation**: Resolve the Eq. (9) notation inconsistency (Frobenius norm vs. inner product), and clarify whether the AMP mask in Eq. (10)–(11) is intended to be {0, 1} or {−1, 1}, with the corresponding update rationale. If {0, 1} is intended, replace sign() with an appropriate binarization function.
2. **Add ablations to decompose contributions**: Test (a) full-layer output matching with Output Error, (b) selective strategy with ARB-X's Activation-conditioned Error, and (c) selective strategy with Output Error but without AMP.
3. **Address the PTB anomaly**: Either provide a genuine explanation for why LLaMA-2-7B specifically suffers on PTB, or remove this specific result from Table 2.
4. **Specify implementation details**: Define "block" and "last FC layer" for each architecture, and report calibration data size and composition.

## Score and Decision

**Calibration summary.** I retrieved anchors across all score bands. The most relevant are:
- **ARB-LLM** (avg 7.00, Accept) — directly comparable 1-bit PTQ paper cited by the current work. Its strengths (innovation 8.79, experiments 8.85, ablations 9.43) and minimal weaknesses put it slightly above the current paper.
- **PB-LLM** (avg 6.75, Accept) — another directly comparable 1-bit PTQ baseline. Its strengths (importance of problem 9.05, thoroughness 9.39) are comparable, but its weaknesses (missing ablations, practicality concerns) are similar in severity to the current paper's.
- **OmniQuant** (avg 6.40, Accept) — broader-scope quantization paper with novelty concerns (-3.51) but solid experiments. The current paper's diagnostic analysis is stronger than anything in OmniQuant.
- **STBLLM** (avg 6.00, Accept) — sub-1-bit quantization paper with incremental novelty concerns.
- **FPTQ** (avg 4.00, Reject) — weaker paper with novelty and claim-support issues.

**Bracket and final score.** Round 1 bracketing placed the paper in the 5.5–7.5 band (between PB-LLM/ARB-LLM/STBLLM). Round 2 narrowing compared weighted items: the current paper's diagnostic analysis (11.13) and empirical results (10.81) are heavier positives than even the strongest anchor items (ARB-LLM's ablations at 9.43, PB-LLM's thoroughness at 9.39). However, its structural weaknesses—attribution gap (2.65) and AMP math ambiguity (1.84)—are more significant than any single weakness in ARB-LLM. The paper sits between PB-LLM (6.75) and ARB-LLM (7.00): stronger on diagnostic insight but weaker on methodological clarity. I assign **6.5**.

**Final Decision**: Accept. The paper makes a genuine contribution through its diagnostic analysis of output alignment failures in 1-bit PTQ, and its proposed method yields consistent empirical improvements. The major weaknesses (AMP math ambiguity, attribution gap) are fixable with clarifications and additional ablations.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>