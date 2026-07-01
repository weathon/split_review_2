Now let me produce the final consolidated review.

## Summary

This paper identifies that standard RoPE, when expressed as complex multiplication, discards the imaginary component of the complex-valued attention score. The authors propose RoPE++, which re-incorporates this imaginary component as a separate group of attention heads via a simple −π/2 rotation of the query vectors. Two configurations are introduced: RoPE++_EH (equal head count, halved KV cache) and RoPE++_EC (equal cache size, doubled attention heads). Experiments at 376M and 776M scales show improvements over vanilla RoPE and other position embeddings on short- and long-context benchmarks.

## Strengths

1. **Genuine mathematical observation.** The paper correctly notes that the complex-multiplication formulation of RoPE yields an imaginary bilinear form that standard attention does not use. Extracting this component via a −π/2 query rotation (Equation 4) is clean, requires no learned parameters, and preserves RoPE's absolute–relative duality. (Section 3.1)

2. **Two practical configurations with clear tradeoffs.** RoPE++_EH halves KV cache and QKV parameters at modest performance cost, while RoPE++_EC doubles attention heads without increasing cache footprint. This provides practitioners with a meaningful efficiency–accuracy knob. (Section 3.3)

3. **Length-extrapolation insight.** The paper identifies that imaginary attention exposes certain dimension pairs to negative and full-range cosine/sine values during training, which vanilla RoPE only encounters during extrapolation (Section 3.4). This is a non-obvious secondary benefit.

4. **Empirical validation at two scales.** Pre-training from scratch at 376M and 776M with 50B + 10B tokens, with evaluation on RULER, BABILong, and multiple short-context benchmarks, provides reasonably thorough evidence. RoPE++_EC consistently outperforms vanilla RoPE across nearly all settings.

## Weaknesses

### Fatal

None.

### Major

- **Missing control for the head-count confound in RoPE++_EC.** RoPE++_EC doubles the number of attention heads relative to vanilla RoPE while keeping QKV projection parameters fixed. The paper attributes gains to the imaginary component's superior long-context modeling, but there is no ablation comparing RoPE++_EC against vanilla RoPE with the *same number of heads* (e.g., vanilla RoPE with 2N heads at the cost of larger QKV projections). Without this control, the observed improvements could partially reflect increased representational capacity from additional heads rather than anything specific to the imaginary computation. The noise experiment (Section 5.2) partially addresses this by showing asymmetrical effects from corrupting imaginary vs. real heads, but the head-count confound in the primary comparison remains unaddressed.

- **RoPE++_EH results are mixed and the paper's framing is optimistic about them.** The paper states that RoPE++_EH "delivers comparable or even superior results" (Section 3.3). However, on several long-context benchmarks it is clearly worse: 376M RULER average 18.2 vs. RoPE 18.8 (Table 2), 776M BABILong average 19.4 vs. RoPE 22.8 (Table 2), and 376M YaRN RULER average 24.7 vs. RoPE 28.2 (Table 3). These are non-trivial gaps. While some degradation from halved parameters is expected, the paper's framing understates the extent.

### Minor

- **No variance or statistical significance reported.** All results in Tables 1–3 are single-run point estimates. Many margins are small (e.g., Table 1 376M Short Avg: RoPE 40.1, RoPE++_EH 40.3, RoPE++_EC 41.0 — margins of 0.2–0.9). Without multiple seeds or confidence intervals, it is unclear whether these differences reflect meaningful signal or random seed variation. Given the computational cost of 50B-token pretraining this is understandable, but it weakens small-margin claims.

- **RoPE++_EC computational cost is understated.** The paper says "the only cost of RoPE++_EC is an additional imaginary attention computed alongside the real one" (Section 3.3), but this includes 2× attention-score FLOPs and 2× memory bandwidth for softmax outputs, in addition to the doubled W_o (which the paper does acknowledge). The efficiency comparison (Figure 4) covers only RoPE++_EH. A wall-clock throughput comparison for RoPE++_EC would help practitioners evaluate the tradeoff.

- **Noise perturbation experiment (Section 5.2) has an alternative interpretation.** Both groups are the same size, so the comparison is fair in terms of head count. However, because the real and imaginary heads are generated from the *same* Q projection and are not independent, corrupting one set could create an imbalance in the combined signal. A control where random subsets of heads of the same size are corrupted would help confirm the effect is specific to the imaginary-vs-real distinction.

### Trivial

None.

## Nice-to-Haves

- An ablation varying the rotation angle (e.g., +π/2 or other phase shifts) to test whether the specific −π/2 rotation is necessary, or whether any phase offset yields similar benefits.
- A quantification of how many frequency dimensions actually benefit from the length-extrapolation effect described in Section 3.4.
- Analysis of training curves to check whether RoPE++ converges differently or requires different hyperparameters.

## Removed Points

These points were flagged in the harsh critic input but are removed with justification:

1. **"Table 3 results are mixed / do not present a clear picture"** — Removed as factually inaccurate. RoPE++_EC *consistently* outperforms vanilla RoPE in Table 3 (RULER Avg: 27.1 vs 25.1, 29.8 vs 28.2, 31.0 vs 29.0, 34.4 vs 33.5 across all four settings). RoPE++_EH results are mixed, but this is already addressed in the RoPE++_EH weakness above.

2. **"Pythia baseline comparison is of limited value"** — Removed. Pythia (partial RoPE) is a standard baseline in the literature; including it is appropriate, and this is a subjective editorial opinion rather than a concrete weakness.

3. **"Imaginary information is discarded framing should be revised"** — Removed. The framing is mathematically accurate: the complex multiplication produces both real and imaginary parts, and standard RoPE takes only the real part (Equation 1). This is a clear statement of fact, not an error.

4. **"Missing comparison against Dai et al. 2025"** — Removed. The paper's scope (modifying RoPE's intrinsic computation) is well-anchored by the comparisons it includes (RoPE, FoPE, Pythia, ALiBi). Demanding comparison against every cited work is not a valid weakness.

5. **"No analysis of training curves"** — Moved to Nice-to-Haves.

6. **"No ablation of −π/2 rotation"** — Moved to Nice-to-Haves.

## Novel Insights

The reviews surface one genuinely novel observation beyond the paper's own contributions: the head-count confound in RoPE++_EC means the central claim — that imaginary attention specifically drives long-context gains — is not as cleanly separated from the "more heads help" explanation as the paper suggests. This reframes the contribution from a definitive demonstration to a hypothesis requiring tighter controls. Conversely, the fact that RoPE++_EH (which keeps total heads fixed) still matches or beats vanilla RoPE on short-context tasks with *half* the QKV parameters is stronger evidence for the method's parameter efficiency than the paper's own framing emphasizes.

## Suggestions

- Add a controlled experiment: compare RoPE++_EC (2N heads, N QKV projections) against vanilla RoPE with 2N heads (2N QKV projections) at the same cache size. If RoPE++_EC matches or beats vanilla RoPE with 2N heads, the imaginary computation is demonstrably more parameter-efficient. If not, the gains may be primarily from additional heads.
- Report results over at least 2–3 random seeds for key comparisons, or provide variance estimates.
- Provide wall-clock throughput/latency numbers for RoPE++_EC vs. vanilla RoPE to quantify the attention-computation overhead.
- Add a control to the noise perturbation experiment: corrupt random subsets of heads of the same size as the imaginary/real group.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>