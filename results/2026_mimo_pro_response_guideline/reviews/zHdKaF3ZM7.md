Now I have sufficient data to calibrate. Let me write the final review.

## Summary
WARP (Weight-space Adaptive Recurrent Prediction) is a novel sequence model that treats the flattened weights of an auxiliary MLP as the hidden state of a linear RNN (θ_t = Aθ_{t-1} + BΔx_t), with output produced by applying the current-weight MLP to a coordinate system (y_t = MLP_{θ_t}(τ)). The model is evaluated across image completion, time series forecasting, dynamical system reconstruction, multivariate time series classification, and in-context learning.

## Strengths
- **Novel and principled formulation**: The core recurrence combining weight-space hidden states with nonlinear decoding (Eq. 1, Section 2.2) is a genuinely new architectural paradigm. By treating network weights as the hidden state updated linearly by input differences and decoded nonlinearly through the root MLP's activation functions, it combines hardware-efficient parallelism via the scan operator with the expressivity that conventional linear RNNs lack (as argued in the introduction citing [9, 26, 66]).

- **Order-of-magnitude improvement via physics-informed root networks**: Table 3 shows WARP-Phys achieves MSE of 0.03 vs. 0.94 on MSD (≈30× reduction) and 0.04 vs. 0.32 on MSD-Zero (≈8× reduction) by embedding τ ↦ sin(2πτ + φ̂) into the root MLP. This concretely demonstrates that weight-space representations create a natural, interpretable interface for incorporating continuous physical priors — a capability structurally difficult to achieve in conventional RNN architectures.

- **Strong image completion at matched parameter count**: Table 1 shows WARP achieves best MSE and BPD on CelebA across all three context lengths (L=100, 300, 600) and best or second-best on MNIST, with all models constrained to approximately 1.68M–2M parameters. Qualitative results (Fig. 3a) show WARP is "the only model to accurately generate digits without substantial artefacts" at small parameter count.

- **SOTA classification on challenging long-sequence benchmarks**: Table 4 shows new state-of-the-art on Ethanol (36.49%, surpassing Log-NCDE's 35.9%) and Heartbeat (80.65%, surpassing LinOSS's 75.8%), with top-3 performance on 4 out of 6 UEA datasets featuring sequences up to 17,984 timesteps. These outperform specialized architectures including Mamba, S5, LinOSS, and FACTS.

- **Clean dual training modes with practical flexibility**: The convolutional and recurrent (AR and non-AR) training modes (Section 2.3) connect naturally to SSM literature and provide task-appropriate flexibility (non-AR for classification, AR with scheduled sampling for noisy forecasting). The distinction between slow-changing parameters (A, B, φ) and fast-changing weights (θ_t) is well-articulated and central to the gradient-free adaptation story.

## Weaknesses

### Fatal
None

### Major
- **PEMS08 traffic forecasting comparison is not reproduced under matched conditions**: Table 2 claims MAE 6.59 vs. prior SOTA 13.45 (>50% reduction). The baselines are "as reported in [62]" — they were not reproduced by the authors under identical preprocessing, normalization, and evaluation protocols. The paper acknowledges using a "non-causal convolution" preprocessing (line 180), which for a forecasting task could leak future information, giving WARP an unfair advantage over causal baselines. WARP also treats 170 nodes × 3 features as a flat sequence while competing against graph-specific architectures. The extraordinary magnitude of improvement demands much stronger justification of comparison fairness. This is not fatal because it is one experiment among many, and the paper's other results (classification, image completion, DSR) are better controlled.

- **Missing ablation on input differences**: The use of Δx_t = x_t − x_{t-1} instead of x_t is a central architectural design choice (Section 2.2, line 82), theoretically motivated by Kidger et al.'s work on continuous-time RNNs. However, no empirical ablation comparing Δx_t vs. x_t vs. (x_t, Δx_t) is provided anywhere in the paper. This is the feature that most distinguishes WARP from a straightforward "weights-as-hidden-state" model, and its isolated empirical impact is never measured. The theoretical motivation is sound, but the paper's core claim that "signal differences" are essential to the architecture's success remains empirically unvalidated.

### Minor
- **Hidden state dimensionality and parameter allocation not reported**: D_θ — the dimensionality of the weight-space hidden state — is never specified for any experiment in the main text. Since A ∈ R^{D_θ × D_θ} requires D_θ² parameters and likely dominates the parameter budget, the paper's claim that models have "nearly the same number of learnable parameters" (~1.68M for MNIST, ~2M for CelebA) cannot be fully verified without knowing how parameters are distributed between A, B, φ, and the root network. Section 2.2 states "self-decoding significantly saves on learnable parameter count" but this claim cannot be evaluated without the allocation breakdown. Architectural details may exist in Appendix D (stripped from this review), but should be more prominent.

- **Abstract slightly overclaims on classification**: The abstract claims "matching or surpassing state-of-the-art baselines on diverse classification tasks" but Table 4 shows WARP is best on only 2/6 datasets and not particularly competitive on EigenWorms (70.93% vs. LinOSS's 95.0%). The more measured claim of "featuring in the top three in 4 out of 6" is accurate.

### Trivial
None

## Nice-to-Haves
- Add stronger baselines (Mamba, Transformers) to the image completion and dynamical system reconstruction experiments, as these modern architectures are included in the classification experiments but omitted elsewhere.
- Explore structured A matrices (block-diagonal, low-rank) as a preliminary result to address the acknowledged scaling limitation (Section 4.2).
- Provide wall-clock time comparison for the ICL extractable-network advantage claimed in Section 3.4.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Harsh critic's concern about missing ablation studies and appendix content — the paper references Appendix E for ablations (line 267: "Appendix E.3 illustrates the excellent computational efficiency") and Appendix D for experimental details. These were stripped from the parsed paper but likely exist in the original submission.
- Harsh critic's concern about thin baseline coverage for classification (Table 4 baselines taken from [96]) — this is standard practice, and the paper does include modern baselines (Mamba, S5, LinOSS, FACTS, Griffin). Asking for reproduced baselines in every experiment is scope creep.
- Strength finder's claim about PEMS08 being a "strong empirical demonstration" — contradicted by the Major weakness identified above regarding non-reproduced baselines and non-causal preprocessing.

## Novel Insights
The WARP-Phys demonstration is the paper's most genuinely novel insight: that weight-space representations create a natural, interpretable interface for injecting continuous physical priors that conventional RNN architectures lack. The order-of-magnitude error reductions when embedding domain-specific functions into the root MLP (Table 3) concretely demonstrate a capability that is structurally difficult to achieve in standard hidden-state RNNs. This suggests a broader paradigm where domain knowledge is encoded directly into the network architecture rather than into loss functions or data augmentation — a direction with significant potential for scientific machine learning.

## Suggestions
- Report D_θ and full parameter allocation tables for every experiment in the main paper.
- Add an input-difference ablation (Δx_t vs. x_t vs. combined) to empirically validate the core design claim.
- For PEMS08: either reproduce baselines under matched conditions or provide detailed analysis (e.g., preprocessing matching, data normalization comparison) of why cross-paper comparison is fair despite the non-causal convolution preprocessing.

## Calibration Report

**Anchors retrieved across all rounds:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Linear Recurrent Neural Networks with a Feature-Sequence Twist | 2.50 | R1 | Generic LRNN variant, weak results — WARP is clearly stronger |
| On the Dynamics of Learning Time-Aware Behavior with RNNs | 3.00 | R1 | Theoretical study with limited scope — WARP has broader impact |
| Enhancing Performance of MLPs by Knot-Gathering Initialization | 2.83 | R1 | Initialization trick paper — unrelated scope |
| FSFC RNN for Text Classification | 2.33 | R1 | Narrow text classification RNN — WARP is far more novel |
| MLPs for NLP | 3.75 | R1 | Shows MLPs inferior to transformers for NLP — limited contribution |
| Mimetic Initialization Helps SSMs Learn to Recall | 4.50 | R1 | Initialization improvement for Mamba — narrower than WARP |
| Learning Sequence Attractors in Recurrent Networks | 5.25 | R1 | Neuroscience-inspired sequence memory — different focus |
| RotRNN: Modelling Long Sequences with Rotations | 4.00 | R1 | Linear RNN variant with rotations — less novel than WARP |
| Linear-Time Sequence Modeling with MLPs (CausalRNs) | 6.33 | R1 | Novel MLP architecture, comparable to Linear Transformers — WARP has broader experiments and stronger results |
| Deep Linear Probe Generators (ProbeGen) | 6.00 | R1 | Weight-space learning paper, accepted — WARP is more ambitious |
| MambaTS | 5.60 | R1 | Incremental Mamba improvements for time series — WARP is significantly more novel |
| Mamba | 6.25 | R1 | Revolutionary SSM architecture — more impactful than WARP but WARP is more novel in its specific approach |
| MLPs Learn In-Context | 6.20 | R1 | Interesting ICL finding, accepted — WARP has more diverse experiments |
| FLDmamba | 6.00 | R1 | Mamba + Fourier/Laplace for time series — incremental vs. WARP's novelty |
| Never Train from Scratch | 8.00 | R1 | Methodological insight about fair evaluation — stronger contribution than WARP |
| LinOSS (Oscillatory SSMs) | 8.00 | R1 | Theoretical proofs + strong empirical results — more rigorous than WARP |
| When can transformers reason with abstract symbols | 7.60 | R1 | Theoretical transformer analysis — different contribution type |
| Scaling Laws for Associative Memories | 7.60 | R1 | Theoretical scaling laws — different focus |

**Round 1 bracket**: Based on these anchors, WARP sits between 5.5 and 7.5. It is clearly more novel and has stronger results than the rejected papers in the 5.0-5.6 range (MambaTS, RotRNN), comparable to the accepted/rejected papers at 6.0-6.3 (ProbeGen, CausalRNs, Mamba, MLPs Learn In-Context), but below the 7.5+ papers (LinOSS, Never Train from Scratch) which have stronger theoretical foundations or broader methodological impact.

**Final score**: 6.5. WARP's genuine architectural novelty, strong WARP-Phys results, and broad experimental coverage place it above the 6.0 threshold. However, the PEMS08 comparison concerns and missing input-difference ablation prevent it from reaching 7.0+. The paper would benefit significantly from addressing these two major weaknesses in a revision.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>