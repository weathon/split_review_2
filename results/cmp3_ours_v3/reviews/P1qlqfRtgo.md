## Summary

This paper compares three neural network architectures (MLP, a "U-Net-style" residual network, and a "DeepONet-style" model) for surrogate modeling of chemical kinetics in hydrogen-oxygen-air combustion. It uses a multi-step training loss with decaying 1/k weights and reports that the residual network achieves substantially lower MSE than the other two. The paper honestly acknowledges that "the problem remains unresolved" due to a large spread in prediction errors.

## Strengths

- **Addresses a real computational bottleneck.** The paper correctly identifies stiff ODE integration for chemical kinetics as a major cost in combustion CFD (~90% of runtime). Replacing it with learned surrogates is a legitimate, practically motivated goal.
- **Multi-step training loss (Eq. 4) with decaying weights.** Weighting future steps by 1/k is a sensible design that encourages the model to handle error accumulation in auto-regressive rollout without over-weighting long horizons.
- **Honest self-assessment.** The abstract explicitly states "Despite testing various architectures and using a fairly large dataset, the problem remains unresolved." This candor about the limitations of the results is rare and should be recognized.
- **95% confidence intervals reported.** Table 1 provides confidence intervals on the MSE, going beyond simple point estimates.

## Weaknesses

### Major

**1. The "U-Net" is a residual MLP, not a U-Net, and the mechanistic claims about its performance are inconsistent with the actual architecture.**

The architecture described in Section 4.2 is a 5-layer fully-connected network with two residual skip connections — no convolutional layers, no downsampling/upsampling, no multi-resolution feature hierarchy. These are the defining characteristics of a U-Net (Ronneberger et al., 2015). The paper calls it "U-Net-like" in Section 4.2 but refers to it simply as "U-Net" in the abstract, conclusions, and Table 1, which is misleading.

More importantly, the paper attributes the model's superior performance to its "encoder-decoder design" and ability to capture "multi-scale representation" (Section 5, line 157). A 3-layer dense block with residual connections does not constitute an encoder-decoder and has no mechanism for multi-scale representation. The residual connections improve gradient flow — a well-known property of ResNet-style architectures — but this is distinct from any U-Net-specific advantage. The mechanistic explanation is at odds with what the architecture actually is, undermining the paper's core interpretative claim.

**2. The test evaluation metric is underspecified, making the results impossible to interpret or reproduce.**

The training loss (Eq. 4) uses 30-step recursive prediction with a weighted MSE. However, the test evaluation is described only as "MSE on an identical test set" (line 143) without stating whether this is one-step-ahead prediction error or multi-step rollout error. These measure fundamentally different things: one-step error can be low even when multi-step rollout diverges. Without specifying the evaluation protocol, the reported numbers in Table 1 cannot be meaningfully interpreted or compared by readers.

**3. The standard deviations reveal an extreme heavy-tailed error distribution that the paper acknowledges but does not adequately characterize.**

From Table 1: U-Net has STD/mean = 0.02183/0.001374 ≈ 15.9×; MLP ≈ 3.4×; DeepONet ≈ 3.2×. A standard deviation 16× larger than the mean implies that most test cases produce near-zero error while a small fraction produce errors large enough to dominate the variance. The paper acknowledges "certain test trajectories remain challenging" (line 153) but then claims the U-Net offers "more stable predictions" (line 157). A model whose error distribution is this heavy-tailed is not "stable" — it is reliable on easy cases and unreliable on hard ones. The paper does not characterize what fraction of test cases fall into the catastrophic-failure regime, nor does it analyze how error correlates with physical regimes (e.g., induction vs. ignition vs. equilibrium).

### Minor

**4. The DeepONet comparison is not faithful to the operator-learning paradigm it claims to represent.**

The paper's DeepONet variant (Section 4.3) takes only the 12 current state variables as branch input and the scalar `dt` as trunk input — it does not learn a mapping between function spaces. Standard DeepONet (Lu et al., 2021) encodes an *input function* (evaluated at multiple sensor points) in the branch and *query coordinates* in the trunk. The paper's version is a differently-factorized Markovian state predictor. The paper does qualify it as "DeepONet-style" and "DeepONet-inspired" throughout most of the text, and the main conclusions only compare three specific architectures. However, statements about "operator-learning architectures such as DeepONet" (line 28) and "DeepONet-based models" (line 190) over-interpret what is essentially a factorized MLP.

**5. Missing reproducibility details.**
- The normalization procedure is never specified (lines 159–160 mention "normalized space" but not what normalization was applied).
- Only 1,000 gradient updates (batch=5,000, 100 epochs, 10 batches/epoch) for ~40–50k parameter networks, with no exploration of longer training or learning rate schedules.
- The output clamp to [-10,10] (line 117) is stated without discussing whether it is ever active or how it interacts with the normalization.
- Single training run per architecture; no mention of random seeds or run-to-run variance. The CIs in Table 1 are across test samples, not training runs.

**6. Claim about computational cost is unsubstantiated.**

Section 5 (line 157) states the U-Net "does not increase computational cost relative to the simpler models" without reporting FLOPs, parameter counts, or wall-clock inference times for any model. Since the entire motivation is computational acceleration (Section 1), the absence of any speed comparison is a gap, even if the paper's primary focus is accuracy.

### Trivial

**7.** The DeepONet matrix product (Section 4.3, line 121) is underspecified: branch output reshaped to 12×10, trunk output is 32×10 — how these produce a 12-component fused vector is not clearly defined.

## Nice-to-Haves

- Report per-trajectory error breakdown (decile plots, or error by combustion regime) to characterize the heavy-tailed distribution, which would directly address the paper's own acknowledgment that "the problem remains unresolved."
- Include ignition delay error, the standard physics-relevant metric in combustion surrogate modeling, alongside MSE.
- Separately report one-step and multi-step rollout errors to distinguish approximation capacity from stability.
- Compare on additional fuels/mechanisms to strengthen generality claims.
- Provide inference time comparisons against the ODE solver to directly address the computational motivation.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **CO/NO species in Figures 3–4 not matching the species list:** Likely a parser artifact from figure caption extraction. The original figures may label different species than the text describes. Removed because it reflects a parsing issue, not a paper error.
- **Missing FNO/PINN/NeuralODE baselines:** Scope creep beyond the paper's stated comparison of three specific architectures. The paper does not claim to benchmark all scientific ML methods.
- **Only one chemical system:** Scope creep. The paper studies H₂-O₂-air which is a standard starting point; requesting additional fuels is a nice-to-have, not a weakness.
- **Figure 1 not showing thermal explosion / extreme transients:** Figure 1 shows one sample trajectory. The paper explicitly states the dataset covers diverse regimes including "abrupt ignition events" (line 92) over T ∈ [250, 5000] K and wide pressure ranges. A single representative figure does not invalidate the dataset claims.
- **Abstract "non-explanation" about error spread:** A stylistic judgment about writing quality, not a factual error.

## Novel Insights

The key insight that emerges from cross-referencing the reviewer analysis against the paper is the *gap* between the architectural labels the paper uses and the actual structures implemented. The "U-Net" has no convolutional or multi-resolution machinery, and the "DeepONet" is not learning an operator between function spaces. This means the paper's empirical finding — that the residual MLP outperforms the plain MLP and the factorized MLP — is better described as "skip connections help" rather than "U-Net-style encoder-decoders capture multi-scale combustion dynamics." The heavy-tailed error distribution (STD 16× mean) further reveals that the reported summary statistics conceal a bimodal failure pattern that the paper does not investigate, weakening the claim about "stable predictions."

## Suggestions

1. **Rename the architectures accurately.** Call the best-performing model a "residual MLP" or "skip-connected MLP." Reserve "U-Net" for architectures with actual encoder-decoder hierarchies and convolutional down/upsampling. This would make the paper's mechanistic claims (about residual connections helping training) consistent with the architecture.
2. **Clearly specify** whether Table 1 reports one-step or multi-step rollout MSE. Ideally, report both: one-step error measures approximation capacity; multi-step error measures stability.
3. **Characterize the error distribution** beyond mean and STD. A decile plot of per-trajectory MSE, or a breakdown by combustion regime (long induction vs. abrupt ignition vs. near-equilibrium), would honestly address the acknowledged limitation that "the problem remains unresolved" and would be the single most impactful improvement.
4. **Report computational cost** (inference time or FLOPs) for all architectures to match the motivating claim about acceleration.
5. **Run multiple trials** with different random seeds to quantify training stability.

## Score and Decision

**Calibration anchors considered:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| `nSDOkm0SKo.md` (Financial NN survey) | 1.00 | R1 | Literature review with no experiments — far weaker than this paper. |
| `otXB6odSG8.md` (Atmospheric Radiation Neural ODE) | 3.00 | R1 | Architecture comparison for scientific surrogate, more comprehensive (25 models + real-world coupling) but still rejected. Comparable scope but stronger evaluation. |
| `yGdoTL9g18.md` (Res-F-FNO for 3D turbulence) | 3.00 | R1 | Minor architectural modification with limited evaluation — comparable severity of issues. |
| `rEEjYlzXUD.md` (Committor Functions DASTR) | 4.25 | R2 | Stronger method novelty but mixed reviews; this paper has less novel methodology. |
| `QPVK1ne9gI.md` (MPFBench dataset) | 5.00 | R2 | Large benchmark with many baselines, more thorough evaluation than this paper. |
| `4KKqHIb4iG.md` (Backprop-free neural PDE solver) | 5.60 | R2 | Novel method with thorough experiments across many PDEs. Stronger evidence and novelty. |

**Round 1 bracket:** 2.0–4.5, narrowed by comparison with similar architecture-comparison papers in scientific ML (the atmospheric radiation paper at 3.00 and Res-F-FNO at 3.00 have comparable limitations and are rejected).

**Final justification:** The paper addresses a real problem and is honestly written, but has several significant weaknesses that prevent acceptance. The headline architecture is misnamed and the mechanistic claims about it are inconsistent with the actual design. The evaluation metric is underspecified (one-step vs. multi-step), the error statistics reveal an extreme heavy-tailed distribution that the paper does not adequately characterize, and critical reproducibility details are missing. The evidence presented — one MSE comparison on one dataset with one run per architecture — is too thin to support strong conclusions about architectural superiority. The paper reads as an early-stage exploration rather than a mature comparative study. With major revisions (accurate architectural naming, properly specified evaluation, characterization of the error tail, multiple trials) the work could form a useful empirical note, but it is not ready for acceptance.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>