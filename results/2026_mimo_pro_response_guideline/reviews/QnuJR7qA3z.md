## Summary
This paper presents HARA, a unified framework for replacing computationally expensive non-linear operators in Transformers (GELU, Softmax, LayerNorm, etc.) with a single canonical architecture based on arithmetic primitives and a shallow ReLU network. The core algorithmic contribution is a dynamic-programming-based parameter initialization pipeline that finds optimal piecewise-linear breakpoints and analytically converts them to ReLU network parameters. The paper demonstrates orders-of-magnitude better approximation accuracy over NN-LUT and RI-LUT baselines, projects hardware area savings of ~62% via synthesis estimation, and shows negligible end-to-end performance impact across BERT, Swin, LLaMA, and Stable Diffusion.

## Strengths
- **Orders-of-magnitude improvement in approximation accuracy**: Table 3 shows HARA achieves MSE values several orders of magnitude lower than NN-LUT and RI-LUT across all operators (GELU, Softmax, LayerNorm) and all HD values (e.g., GELU at HD=2: HARA 2.36e-05 vs NN-LUT 2.07e-03 and RI-LUT 8.13e-05). HARA's error decreases predictably with HD, demonstrating robustness where baselines stagnate or behave erratically.
- **DP-based initialization is the key driver, cleanly isolated via ablation**: Table 4 shows MSE decreasing by orders of magnitude at each pipeline stage: Naive (GELU: 1.38e-03) → DP (1.34e-06) → DP w/ FT (1.89e-07). This validates that the principled optimization, not just the architecture, drives the accuracy advantage.
- **Elegant mathematical decomposition of operators**: Table 1 systematically identifies symmetry/asymptotic properties of activation functions (GELU, SiLU, Sigmoid, Tanh, Softplus), enabling transformation from infinite to finite domain approximation. Equations 2-3 decompose Softmax and LayerNorm into Pow2/Log2 primitives, eliminating hardware for exp, sqrt, and div.
- **Broad end-to-end evaluation across four diverse architectures**: Table 6 shows <0.1% change across BERT (EM: 80.038→80.02, F1: 87.616→87.615), Swin (Top-1: 81.182→81.170), LLaMA (PPL: 7.814→7.819), and DiT (HPSv2: 0.2724→0.2731). Breadth across NLU, CV, language generation, and image generation supports generalizability.
- **Projected hardware savings from unification**: Table 5 provides synthesis estimations showing a single URN block (7,560 μm²) replaces three specialized units totaling 20,056 μm², yielding 62.3% area reduction and 51.7% power reduction, directly motivating the unified architecture.

## Weaknesses

### Fatal
None.

### Major
- **No error bars on end-to-end results (Table 6)** — The performance differences are extremely small (e.g., BERT EM -0.013, LLaMA PPL +0.005). Without standard deviations, confidence intervals, or multi-seed reporting, it is impossible to determine whether these represent genuine preservation of model performance or are within typical run-to-run variance. If differences fell within confidence intervals, that would *strengthen* the drop-in replacement claim, but the paper cannot make this argument without the data.
- **Hardware comparison baseline is against a sum of specialized units (Table 5)** — The 62% area savings compares one unified URN against three independent specialized LUT-based units (Softmax, LayerNorm, GELU). This implicitly assumes a designer would build three separate monolithic units. More informative baselines include a shared-LUT architecture with memory reuse across functions, or the cited prior work (NN-LUT, RI-LUT) implemented in hardware. The comparison does demonstrate the benefit of unification per se, but not HARA's specific advantage over other possible unification strategies.
- **HARA approximation inseparable from 8-bit quantization in Table 6** — The end-to-end experiment applies both HARA approximation and 8-bit post-training quantization simultaneously, making it impossible to isolate the contribution of approximation alone. A separate HARA-only (no quantization) result would clarify whether the negligible accuracy change is from the approximation, from quantization masking approximation error, or both.

### Minor
- **No latency or cycle-count analysis for the unified design** — The paper discusses area and power savings but not latency. Softmax via Eq. (2) requires multiple sequential Pow2/Log2 evaluations plus summations through the time-multiplexed URN, which may involve more cycles than a direct specialized implementation. The area savings could be partially offset by increased latency.
- **DP algorithm complexity not stated** — Algorithm 1 performs DP over a discretized domain; the paper does not state its time complexity. This is a one-time offline cost, but practitioners need to know it.
- **No error propagation analysis for chained approximations** — Softmax (Eq. 2) chains Pow2 → sum → Pow2, and LayerNorm (Eq. 3) chains multiple Log2 and Pow2 evaluations. While end-to-end results implicitly validate this, an analytical or empirical error propagation analysis would strengthen confidence in the decomposition.

### Trivial
None.

## Nice-to-Haves
- Report HARA-only results (without quantization) in Table 6 to isolate the effect of approximation.
- Add a latency/cycle-count estimate or analytical comparison even without full ASIC implementation.
- Compare against a shared-LUT hardware baseline to strengthen the efficiency claims beyond simple unification.
- State the DP algorithm's time complexity and wall-clock initialization time.
- Add 3-5 seed runs for Table 6 with standard deviations.

## Removed Points
These points are flagged to be removed, treat them with caution:
- **Hardware savings are "unverified" / "unsupported"**: The paper consistently uses "project/estimation" language (abstract, Section 4.2.3, Section 5) and acknowledges that "a full ASIC synthesis would be required to obtain definitive measurements." This is a limitation, not a fabrication.
- **He et al. (2015) citation is tenuous**: Minor related work nitpick. Not substantive.
- **Input distribution shift for out-of-distribution inputs**: Speculative concern not grounded in a specific problem.
- **No comparison against efficient inference engines**: Scope creep.
- **HD parameter semantics differ between methods**: Minor comparison fairness point; HD is used consistently.

## Novel Insights
The DP-based parameter initialization pipeline is a genuinely principled contribution to function approximation in hardware contexts. The insight that PWL breakpoints can be optimally found via dynamic programming and then analytically converted to ReLU network parameters — rather than relying on unstable direct training — is well-validated by the ablation and represents a meaningful advance over heuristic approaches. The systematic exploitation of activation function symmetry properties (Table 1) to transform infinite-domain approximation into finite-domain problems is also elegant and practically useful for the hardware co-design community.

## Suggestions
- Add 3-5 seed runs for Table 6 with standard deviations. If differences fall within confidence intervals, explicitly state this — it would strengthen the drop-in replacement narrative.
- Add a HARA-only (no quantization) column to Table 6.
- Add a brief latency analysis comparing the URN's cycle count for Softmax/LayerNorm against direct specialized implementations.
- Consider comparing against a shared-LUT hardware baseline.
- State the time complexity of the DP algorithm in Algorithm 1.

## Score and Decision

**Round 1 bracket:** 5.5–6.5. HARA is clearly above the reject range (Addition is All You Need at 4.50, PolySketchFormer at 5.00, SuFP at 4.67 — all rejected) given its stronger algorithmic contribution, broader evaluation, and cleaner mathematical framework. However, gaps in experimental rigor (no error bars, hardware baseline weakness, conflated approximation/quantization) place it below the clean accepts at 6.5–7.0 (PADRe at 6.75, KAT at 6.80, Spatio-Temporal Approximation at 7.00).

**Round 2 narrowing:** PADRe (6.75, accepted) is the closest comparable — both are unified frameworks replacing expensive transformer components with hardware-friendly approximations. HARA covers more operators (not just attention but also normalization, activations) and has a stronger algorithmic innovation (DP-based initialization). However, HARA's hardware evaluation is weaker (synthesis estimation against a straw-man baseline, no latency analysis) and the end-to-end results lack error bars and conflate approximation with quantization. This places HARA slightly below PADRe at 6.0.

**All anchors:**
- Addition is All You Need (4.50, R1) — Similar HW estimation weakness; HARA has stronger experiments
- PolySketchFormer (5.00, R2) — Replaces softmax with polynomial; HARA is broader and better validated
- SuFP (4.67, R2) — Piecewise quantization + HW; HARA is more complete
- PADRe (6.75, R2) — Unified polynomial attention replacement; very similar scope; accepted
- Kolmogorov-Arnold Transformer (6.80, R1) — Replaces MLP with KAN; accepted; similar level
- Multilinear Operator Networks (6.67, R1) — Eliminates activation functions; accepted
- Spatio-Temporal Approximation (7.00, R1) — Approximates non-linear ops for SNN HW; accepted; has theoretical bounds HARA lacks

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>