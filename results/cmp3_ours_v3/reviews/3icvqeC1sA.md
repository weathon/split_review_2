## Summary

ChaosNexus proposes ScaleFormer, a U-Net-inspired multi-scale Transformer architecture for chaotic system forecasting, augmented with Mixture-of-Experts layers, wavelet-based frequency fingerprint conditioning, and MMD distributional regularization. Pretrained on ~20K synthetic chaotic ODE systems, it achieves improved zero-shot sMAPE (~69 vs ~75 for Panda) on 9.3K held-out systems and dramatically outperforms general-purpose time-series foundation models. The scaling analysis cleanly separates system-diversity effects from per-system volume effects, providing a practically useful design principle.

## Strengths

- **Well-motivated multi-scale architecture with evidence from attention-map analysis (Section 4.4, Figure 5).** The paper identifies a concrete limitation of prior work—single-resolution processing—and provides evidence that shallow encoder layers capture high-frequency fluctuations while deep layers synthesize long-range dependencies, with attention patterns that adapt to system regularity (Toeplitz-like for regular dynamics, block-structured for complex ones). This goes well beyond typical architectural motivation.

- **Solid zero-shot results on the synthetic benchmark.** On 9.3K held-out systems, ChaosNexus improves sMAPE@128/sMAPE@512 over Panda from ~75 to ~69 (roughly 7-8%), with statistically significant differences. The KL divergence of attractors (D_step ≈ 1.2) is dramatically better than all non-Panda baselines (which cluster at 5-20), supporting the claim that domain-specific pretraining matters. The dramatic gap over general-purpose time-series foundation models (TimesFM, Chronos, Moirai-MoE) is convincing.

- **Clean scaling analysis with a practically useful finding (Section 4.3, Figure 4).** Figure 4(c) (system diversity scaling) versus 4(b) (per-system volume scaling) cleanly separates two data-growth strategies and demonstrates that only diversity helps. This refines the Panda scaling result by adding the controlled negative result that volume alone does not help—a genuinely useful finding for anyone building a foundation model in this space.

- **Attention-map analysis (Section 4.4, Figure 5) provides unusually detailed insight into model internals.** The visualization of encoder/decoder attention at different depths across systems of varying regularity is one of the more informative internal-mechanism analyses in a time-series forecasting paper. It provides genuine evidence that the U-Net structure is functioning as designed.

## Weaknesses

### Fatal
None.

### Major

- **The WEATHER-5K few-shot comparison (Figure 3) compares pretrained+finetuned ChaosNexus against from-scratch baselines, which conflates the benefit of pretraining with the benefit of the architecture.** The paper explicitly states (Section 4.2) that "ChaosNexus is first pretrained on the synthetic chaotic systems corpus and then fine-tuned on exactly the same WEATHER-5K subsets as the baselines, which are trained from scratch without pretraining." The headline Figure 3—which readers will primarily remember—shows ChaosNexus at <1°C MAE versus baselines at 3-4°C, creating the misleading impression of architectural data efficiency. This asymmetry is the primary driver of the gap. The paper does report foundation-model comparisons (Panda, Chronos-S-SFT) in Appendix A.6 and notes that "ChaosNexus also outperforms Panda on many variable forecasting tasks," but these are not in the main figure. The "few-shot" framing inflates the real-world claim relative to the evidence presented in the main text. **Fix**: Add Panda (and Chronos-S-SFT, if applicable) to the main Figure 3 under the same fine-tuning regime.

### Minor

- **Selective reporting of the D_frac result undercuts the "superior fidelity" claim.** The text (Section 4.1) states "ChaosNexus exhibits superior fidelity. It reduces the average correlation dimension error (D_frac) to 0.203" without mentioning that Panda achieves a mean D_frac of ~0.200 (Figure 2 caption)—which is *better* (lower). This is a central attractor-statistics metric; reporting it without comparison to the leading baseline on the same metric is misleading. The paper should transparently acknowledge this and pivot to the metrics where ChaosNexus genuinely improves (D_step, D_lyap, ME_LRW from Appendix A.4).

- **Ablation studies are entirely in the appendix, making it hard to attribute gains to specific components.** The architecture has five novel or modified components (U-Net multi-scale encoder-decoder, axial attention, MoE layers, wavelet scattering fingerprint, MMD regularization). The paper mentions "extensive ablation studies" in Appendix A but includes none in the main body. Given that the sMAPE improvement over Panda is modest (~7%) and D_frac is tied, at least one key ablation in the main text (e.g., replacing the U-Net with a linear stack of Transformer blocks at matched parameter count) would substantially strengthen the attribution of improvements to the multi-scale design versus other components.

- **The MMD training procedure is underspecified.** Equation 10 computes MMD on "batches of the full predicted and ground-truth trajectories." The architecture's linear readout head (Equation 7) produces the full H-step forecast in one shot, so MMD can be computed without autoregressive backpropagation. But the paper tests models "autoregressively" at evaluation time (Section 4.1), and does not clarify whether training uses one-shot or autoregressive prediction. This should be explicitly stated for reproducibility.

### Trivial
- The variable `C` (number of wavelet scattering paths) in $\mathbf{F}_w \in \mathbb{R}^{C \times T' \times V}$ (Section 3.3) is never defined in the main text; it is referenced to Appendix C.3.

## Nice-to-Haves

- **Training/inference cost comparison with Panda.** Given the more complex U-Net + MoE + axial attention architecture and only modest gains over Panda (especially on D_frac), reporting training time, inference speed, and memory usage relative to Panda would help readers gauge the practical trade-off.

## Removed Points
These points are flagged to be removed; treat them with caution.

- **Missing hyperparameters not in main text (λ₁, λ₂, D, M, K).** Standard practice to place in appendix; not a valid criticism of the submission.
- **Axial attention complexity O(S²+V²) omitting dimension factors.** Standard shorthand; no substantive issue.
- **MMD training procedure requiring BPTT through 512 steps.** The reviewer speculated about autoregressive BPTT, but the linear readout head (Eq. 7) produces the full forecast in one shot, making BPTT unnecessary. The paper should clarify, but the concern as framed is not well-grounded.
- **Criticism that "oversmooth fast oscillations" claim is asserted without evidence.** This is architectural motivation for multi-scale design, not a claim requiring proof; the attention analysis (Section 4.4) partially addresses it.
- **Criticism that ablations in appendix make it "impossible to evaluate."** The ablations exist in the original submission (Appendix A); relegating them to the appendix is a space-constraint choice common at ICLR. Retained as a minor weakness above, but the "impossible" framing is an overstatement.
- **Criticism about Panda/DynaMix being described as "single resolution" when Transformers can capture multi-scale through depth.** The paper's point is about *explicit* multi-scale down/up-sampling, not whether implicit multi-scale can emerge through depth. A reasonable distinction.

## Novel Insights

The harsh review's most valuable observation is that the paper's ensemble of claims ("superior fidelity," "exceptional data efficiency") outruns the evidence in specific places where the comparison is asymmetric (weather) or the metric favors the baseline (D_frac). The review correctly identifies that the paper would be strengthened not by adding more experiments, but by presenting the existing ones more honestly—particularly by putting the fair comparison (Panda on weather) in the main figure and acknowledging where the baseline ties or beats the proposed method. This is a calibration issue more than a methodological flaw.

## Suggestions

1. **Fix the weather comparison**: Add Panda (and Chronos-S-SFT if space permits) to Figure 3 under the same fine-tuning regime. If ChaosNexus still wins, this is strong evidence for the multi-scale architecture's real-world value.

2. **Report D_frac transparently**: Explicitly state that Panda's mean D_frac (~0.200) is slightly better than ChaosNexus' (~0.225) and explain why the improvements on D_step, D_lyap, and ME_LRW are the more important differentiators for the thesis.

3. **Move one key ablation to the main text**: A variant without the U-Net (a linear-stack Transformer of matched parameter count) would most directly test whether the multi-scale design or other components (MoE, MMD, wavelet fingerprint) drive the gains.

4. **Clarify the MMD training procedure**: State explicitly whether the MMD loss is computed on one-shot or autoregressive predictions during training.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| PowerGPT (rejected) | ntSP0bzr8Y | 3.00 | R1 | Weak time-series foundation model; less well-executed than ChaosNexus on all fronts |
| MPP (rejected) | fH9eqpCcR3 | 5.20 | R1 | Physics pretraining paper with similar scope/ambition; had concerns about transferability across physics tasks similar in severity to ChaosNexus' weather comparison issue |
| TRENDy (accepted) | NvDRvtrGLo | 5.00 | R1 | Equation-free spatiotemporal dynamics paper; had missing ablation on key design choice, similar to ChaosNexus' issue |
| PhyDL-NWP (rejected) | QMkYEau02q | 4.25 | R1 | Physics-guided weather forecasting; weaker evaluation than ChaosNexus |
| DAM (accepted) | 4NhMhElWqP | 7.00 | R1 | General time-series foundation model; had "too dependent on appendix" weakness but broader scope and stronger results |
| AtmosArena (rejected) | 5GI6BGToyw | 5.75 | R1 | Benchmark paper for atmospheric foundation models; different type of contribution |

### Bracketing

**Round 1 bracket:** 5.0 – 7.0. The paper is clearly stronger than PowerGPT (3.0) and weaker than the top time-series foundation models like DAM (7.0). It is comparable to MPP (5.2, rejected) and TRENDy (5.0, accepted) in terms of contribution-to-weakness ratio, but has a cleaner scaling analysis and stronger internal-mechanism analysis than either.

**Narrowing:** The paper has genuine contributions (novel architecture, clean scaling analysis, informative attention analysis) but two real presentation flaws (asymmetric weather comparison, selective D_frac reporting) that prevent it from reaching the DAM tier. These flaws are fixable, which places it above the MPP/TRENDy tier where concerns were more structural. 

**Final score: 6.0.** A borderline accept. The core architecture and synthetic benchmark are solid. The main issues are presentation/transparency rather than methodology, and they are addressable in a revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>