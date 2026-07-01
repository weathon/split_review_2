## Summary

The paper studies plasticity loss in deep reinforcement learning through both theoretical analysis and a practical method. It proposes that plasticity loss arises from two mechanisms: rank collapse of the NTK Gram matrix and Θ(1/k) gradient magnitude decay. Focusing on the second mechanism, the paper introduces Sample Weight Decay (SWD), a lightweight method that linearly downweights older samples in the replay buffer. Experiments across TD3, Double DQN, and SAC/SimBa on MuJoCo, ALE, and DMC benchmarks show consistent performance improvements from SWD.

## Strengths

- **Simple, lightweight, and broadly applicable method.** SWD is trivially implementable on top of any experience-replay-based RL algorithm with negligible overhead. This practical appeal is a genuine virtue.

- **Consistent and cross-domain empirical improvements.** SWD improves returns over uniform sampling across 5 MuJoCo environments (TD3, Figure 2), 3 ALE environments (Double DQN, Figure 3), and 4 DMC tasks (SAC/SimBa, Figure 4), as well as under different UTD ratios (Figure 7). The pattern is directionally reliable across algorithm families, network architectures, and task domains.

- **Demonstrated orthogonality to existing plasticity methods.** SWD combined with S&P yields the best results in Figure 8, suggesting the method's data-level intervention is complementary to network-level plasticity preservation techniques. This is a practically useful finding.

- **Hyperparameter robustness.** The paper reports low sensitivity to the two core hyperparameters (T, w_min) across a grid search (Appendix F), which strengthens the method's practical deployability.

## Weaknesses

### Fatal

None.

### Major

- **GraMa evidence for plasticity loss mitigation is internally contradictory as presented.** The paper states (Section 6.3, line 232): *"Notably, a larger GraMa value indicates a weaker learning capability of the neural network."* Figure 6 then shows that SAC+SWD maintains **higher** GraMa values than SAC throughout training, and the text claims this demonstrates that SWD "effectively alleviates the gradient sparsity" (line 234). Under the stated interpretation, higher GraMa = weaker learning, so SWD having higher GraMa would mean *worse* plasticity — directly contradicting the paper's conclusion. Furthermore, in the ablation study (Figure 5), SWA (the anti-SWD baseline) has lower GraMa and worse performance. If lower GraMa = stronger learning (the inverse of the stated interpretation), then SWA should perform better, which it does not. These contradictory patterns make the paper's primary metric-based evidence for plasticity loss mitigation uninterpretable as written. The error appears to be a simple reversal (the paper almost certainly intends that larger GraMa = stronger gradient signals = better plasticity), but as presented, the evidence cannot be read coherently. This must be fixed.

- **Theoretical framework assumes a growing replay buffer, but all experiments use fixed-size buffers — creating a structural gap between theory and practice.** Proposition 1 (lines 90–94) establishes the empirical distribution recursion μ_h^{k+1} = (k/(k+1)) μ_h^k + (1/(k+1)) d̂_h^{k+1} based on |D_h^{k+1}| = k+1 (a buffer that grows without bound). The core gradient decay result (Theorem 3, line 142) inherits this 1/k structure. However, all evaluated algorithms (TD3, DQN, SAC) use fixed-capacity replay buffers (standard sizes 10^5–10^6). In a fixed buffer, once capacity is reached, the coefficient becomes 1/N (a constant), and gradient decay from the distributional shift term would plateau rather than asymptotically approach zero. The paper never acknowledges this mismatch, never discusses how the analysis changes with bounded buffers, and offers no argument that the 1/k intuition carries over. This severs the claimed theoretical grounding for SWD's empirical success as presented.

### Minor

- **The connection between Theorem 3's 1/k factor and SWD's weighting scheme is asserted, not derived.** The paper claims SWD "neutralizes the 1/k attenuation" (line 164), but provides no mathematical derivation showing how age-based linear weighting transforms the loss gradient to cancel the 1/k term. SWD produces a different loss function (weighted MSE), not the original gradient with a corrected scaling factor. The paper should either provide a formal argument connecting the weighting to the gradient expression in Theorem 3, or soften the claim from "neutralizes" to a more measured characterization (e.g., "compensates for" or "counteracts").

- **The "SOTA" claim is unsubstantiated.** The abstract and introduction claim "achieving SOTA performance on challenging DMC Humanoid tasks" (line 28) and "consistently delivers state-of-the-art (SOTA) performance" (line 26). However, all experiments compare SWD only against the base algorithm (SAC/SimBa) and other plasticity-mitigation methods — not against published state-of-the-art results on these benchmarks. Without referencing external SOTA numbers, this claim is not supported by the presented evidence and should be qualified.

- **The limitations section is generic and does not address substantive gaps.** The limitations (line 281) cite only computational constraints and the preliminary stage of theoretical exploration. It does not discuss the growing-vs-fixed-buffer mismatch, the GraMa interpretation issue, or the lack of formal connection between Theorem 3 and SWD. The NTK degeneration section (Section 4.1) is presented as part of the paper's theoretical contribution but is purely narrative — no new theorems, no results used elsewhere in the paper. Trimming or explicitly positioning it as background would better match the paper's actual delivery.

### Trivial

- The GraMa statement on line 232 ("larger GraMa value indicates a weaker learning capability") has the direction reversed relative to the paper's own empirical evidence and likely reflects a writing error. The empirical pattern consistently shows higher GraMa associated with better performance and lower GraMa (SWA) with worse performance. This should be corrected.

## Nice-to-Haves

- **Comparison against other recency-weighting baselines.** The paper compares SWD to uniform sampling and PER (TD-error prioritization). A natural baseline for a recency-weighting method is another recency-weighting method (e.g., sampling only from the most recent N transitions, or fixed exponential recency bias). Such a comparison would help establish whether the specific linear decay form matters or whether any recency bias explains the improvement.

- **Derivation of SWD's effect on the gradient.** A formal characterization of how the SWD-weighted loss gradient relates to the unweighted gradient from Theorem 3 would substantiate the claimed connection between the theory and the method.

## Removed Points

- **Statistical significance / lack of hypothesis testing.** Removed because the paper reports 95% stratified bootstrap confidence intervals (Agarwal et al., 2021), which is the accepted standard for RL benchmarking. The critic's claim about "no significance testing" is inaccurate.
- **Hyperparameter values not reported in main text.** Removed because the paper states hyperparameters are in Appendix C (line 204), which is stripped by the parser. Per review guidelines, missing appendix content should not be counted as a weakness.
- **Theorem 3 is single-point analysis / doesn't analyze full trajectory.** Removed because analyzing the gradient at the initialization of each iteration is standard practice in optimization theory for iterative RL algorithms; this criticism reflects a mismatch of expectations about what level of theoretical analysis is standard.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the GraMa interpretation.** The statement on line 232 should be corrected to reflect that larger GraMa indicates stronger gradient signals (better plasticity), which would make the paper's evidence internally coherent. Alternatively, provide the formal definition of GraMa (from Liu et al., 2025) and explain its relationship to learning capability precisely.
2. **Acknowledge the buffer-size gap.** Either (a) explicitly note that the theoretical 1/k analysis applies to a growing-buffer setting and discuss how the picture changes with fixed buffers, or (b) provide an alternative analysis for the fixed-buffer case.
3. **Provide a derivation or weaken the claim.** Either show formally how SWD's age-weighted sampling transforms the gradient expression from Theorem 3, or replace "neutralizes" with a more measured term like "compensates for" or "counteracts."
4. **Qualify the "SOTA" claim.** Replace "state-of-the-art" with language that accurately reflects what was compared against (base algorithm and other plasticity methods, not published SOTA results).
5. **Tighten the NTK section.** Either remove Section 4.1 or explicitly position it as background discussion (which it is) rather than part of the paper's novel theoretical contribution.

## Score and Decision

The paper tackles an important problem and proposes a simple, empirically effective method. The consistent performance improvements across three algorithm families and three benchmark suites are the paper's strongest asset. However, two significant issues prevent acceptance in the current form: (1) the GraMa evidence — the paper's primary metric for plasticity loss mitigation — is presented with an interpretation that contradicts its own results, making the central claim about *why* SWD works unsupported by the reported data; (2) the theoretical framework assumes a growing replay buffer while all experiments use fixed buffers, creating a structural gap between theory and practice that is not acknowledged. Both issues are fixable, and the empirical contribution (SWD consistently improves returns) is genuine. A revised version that corrects the GraMa interpretation, honestly addresses the buffer mismatch, and tempers the overclaims would be a solid contribution.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>