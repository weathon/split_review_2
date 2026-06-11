## Summary
# Final Review Report

## Summary

This paper introduces **Dynamic Nested Depth (DND)**, a post-training method that improves LLM performance by routing critical tokens through an additional transformer-layer pass. At the end of a transformer block, a lightweight linear router computes a selection score for each token; tokens exceeding a threshold are packed into a compact sequence, reprocessed through the same layer with new positional embeddings, and then fused with the original output via a routing-score-weighted interpolation. The training strategy employs two auxiliary losses — a Score Dispersion Loss (maximizing entropy of normalized routing scores) and a Distribution Preservation Loss (pulling scores toward 0.5 via MSE) — plus an adaptive threshold control scheme with buffer-proportional feedback and EMA synchronization.

DND is evaluated on three small dense models (Qwen3-1.7B, Llama3.2-1B, Gemma3-1B) and one MoE model (Qwen3-30B-A3B) via full-scale supervised fine-tuning. Reported average gains range from +0.87% (30B MoE) to +2.61% (Llama3.2-1B) across 11-17 benchmarks covering general knowledge, math/STEM, and coding/agent tasks, with only ~0.03M additional parameters and ~6% FLOPs overhead (91-93% inference throughput relative to baseline).

**Core Contributions (C1-C3):**
- **C1:** DND mechanism — adaptive token selection + selective nested layer re-processing.
- **C2:** Training strategy — router-controlling loss (score dispersion + distribution preservation) + threshold control scheme (buffer proportional + EMA).
- **C3:** Post-training integration into dense and MoE architectures with minimal parameter/compute increase.

**Novelty assessment:** Deferred due to Retrieval-Disabled Mode (external paper search unavailable). Qualitative comparison with cited MOR/ITT baselines suggests shared high-level goal (selective token re-computation) but with notable differences in training phase (post-training vs. from-scratch), scale (30B vs. 1B), and routing control (entropy+MSE+EMA vs. z-loss). A formal novelty verdict requires manual literature verification.

## Strengths
1. **Clean, practical idea.** The core concept — selectively routing hard tokens through an additional pass of the same transformer layer — is intuitive and well-motivated. It sits at a natural intersection of token-level adaptive computation (pruning literature) and latent-space test-time scaling. The implementation is lightweight (single linear router, shared weights for nested pass, no architectural changes to the base model).

2. **Post-training compatibility.** DND is designed as a plug-and-play post-training method that does not require pre-training from scratch. This is a genuine practical advantage over methods like MOR that require full pre-training (200B+ tokens). The demonstrated applicability to both dense and MoE architectures (Qwen, Llama, Gemma families) supports the claimed generality.

3. **Thorough ablation on training strategies.** Table 4 provides a well-structured ablation that separates the contributions of router control (RC) and threshold control (TC), tests different selection ratios (10%, 20%, 30%), and evaluates different layer ranges. This allows readers to attribute the improvement to specific components. The RC-vs-TC decomposition is informative.

4. **Efficiency-transparency reporting.** The paper reports throughput benchmarks (Table 3) showing DND achieves 91.6-93.1% of baseline speed across various input/decode length combinations, and mentions 6% FLOPs overhead for 20% token selection. This transparency about the computational cost is helpful and should be standard practice for efficiency-oriented methods.

5. **Rich analysis of routing behavior.** Section 4.5 provides empirical analysis of what tokens are selected (entropy correlation), how representations change (entropy reduction), and how the selection ratio stabilizes during training (buffer control + EMA visualizations). These analyses go beyond mere performance reporting and help build intuition about the method's internal dynamics.

## Weaknesses
### W1 (Critical) — Missing statistical variance and significance testing [Tables 1, 2, 4]
All experimental results are reported as single-point estimates without standard deviations, confidence intervals, or significance tests. Many reported gains are small (e.g., BBH +0.13, DROP +0.27, MATH +0.15, MATH-500 +0.20 in the 30B MoE evaluation) and could be within typical benchmark noise ranges. Without multi-seed variance or significance testing, the core claim that DND "consistently improves performance" cannot be fully verified. The phrase "without any performance degradation" is unsubstantiated without confidence intervals. **Severity: Critical — affects validity of all main claims. Recommended action:** Report mean ± std over ≥3 seeds for key comparisons; add paired significance tests.

### W2 (Major) — Information leakage and attention masking in nested pass [Method 3.1.2]
The nested pass packs selected tokens into a compact sequence with new positional embeddings (Eq. 3). The paper does not specify how causal attention masking is applied during this packed-sequence processing. If standard causal masking is applied per packed position order, tokens that were originally separated by many positions become adjacent, potentially leaking future-token information. If the original causal ordering is preserved, the positional re-embedding strategy must be carefully justified. The information leakage concern is mentioned regarding expert-choice routing (citing Raposo et al.) but the token-choice alternative's own masking behavior is not analyzed. **Severity: Major — affects methodological soundness. Recommended action:** Add a dedicated explanation of the attention masking strategy in the nested pass, with an analysis of whether autoregressive causality is preserved.

### W3 (Major) — Ablation interpretation inconsistent with data [Section 4.4, Table 4]
The text claims "router and threshold control function as complementary components... each method individually provides marginal gains." However, the RC-only condition achieves Δ=+1.50 (80% of the full DND gain of +1.88), which is the opposite of "marginal." The TC-only condition achieves Δ=+1.01. Furthermore, RC+TC together (1.88) is less than the sum of individual gains (1.50 + 1.01 = 2.51), suggesting overlapping rather than complementary effects. The narrative should be revised to accurately state that RC accounts for the majority of gains while TC provides supplementary regularization. **Severity: Major — affects interpretation of the core technical contribution. Recommended action:** Rewrite the ablation discussion to reflect the quantitative dominance of RC.

### W4 (Major) — Score Dispersion Loss normalization bias [Eq. 6]
The Score Dispersion Loss (Eq. 6) normalizes sigmoid scores within each sequence (p̂^i = p^i / Σ_j p^j) before computing entropy. This normalization disproportionately amplifies high-score tokens while collapsing low scores near zero, meaning the loss primarily diversifies the top-ranked tokens rather than improving distinguishability around the decision threshold τ — which is where distinguishability matters most for stable selection. Additionally, per-sequence normalization makes the gradient magnitude dependent on sequence length. **Severity: Major — affects the claimed "precise control" of token selection. Recommended action:** Add a margin-based loss around the threshold region, or discuss the known limitation of entropy-based dispersion near the boundary.

### W5 (Major) — Missing λ_sd and λ_dp values and sensitivity analysis [Eqs. 5-7]
The router loss ℒ_router = λ_sd ℒ_sd + λ_dp ℒ_dp is central to DND's training strategy, but the paper does not report the values of λ_sd and λ_dp used in any experiment. No sensitivity analysis is provided. Since ℒ_sd operates on normalized scores while ℒ_dp operates on raw scores (different scales), the balance hyperparameters critically affect training dynamics. **Severity: Major — affects reproducibility. Recommended action:** Report λ_sd, λ_dp values and add a sensitivity study showing performance at 2-3 different ratios.

### W6 (Major) — Causal overclaim in token selection analysis [Section 4.5]
The section states that entropy reduction "proves the effectiveness of our method" based on a correlation (r=0.3359, r²≈0.11) and a pre-post entropy comparison without controls. The observed entropy reduction could be driven by regression to the mean, the weighted fusion mechanism (Eq. 4), or simply additional computation rather than the routing mechanism specifically. **Severity: Major — affects claims about why DND works. Recommended action:** Replace "proving" with "is consistent with"; add control experiment (randomly selected tokens with matched initial entropy run through the same nested pass).

### W7 (Major) — No limitations or failure-case analysis [Section 5]
The conclusion does not mention any limitations. Important unacknowledged limitations include: unknown scaling behavior for larger dense models (>7B), interaction with inference optimizations (KV cache, speculative decoding), the 6% FLOPs overhead and 7-9% throughput reduction for latency-sensitive deployments, and the lack of OOD generalization testing for the router. **Severity: Major — affects completeness and scientific honesty. Recommended action:** Add a limitations paragraph covering scaling, efficiency trade-offs, and generalization boundaries.

### W8 (Minor) — Abstract claims beyond evidence scope [Abstract]
The abstract states "improves performance for off-the-shelf LLMs" suggesting general applicability, but experiments cover only three small dense models (1-1.7B) and one MoE model. The phrase "minimal parameter and computing increase" lacks concrete numbers in the abstract. **Recommended action:** Bound claims to the evaluated model scale and report key efficiency numbers in the abstract.

### W9 (Minor) — Introduction logical gap [Introduction P2]
The transition from token pruning (discard/keep binary) to nested reprocessing is presented as "the natural next step" but the paragraph does not establish why standard single-pass processing is insufficient for hard tokens. The token difficulty and pruning literatures are cited but not directly connected to the depth-insufficiency hypothesis. **Recommended action:** Add a bridging argument explaining why additional depth (rather than just retention) is expected to benefit hard tokens.

### W10 (Minor) — Related-work comparison lacks quantitative evidence [Section 2.2]
The comparison with MOR/ITT is qualitative and claims superiority without controlled experiments. Claims about MOR's limitations (from-scratch training, 1B-only) are presented as inherent disadvantages, but no experiment applies MOR-style routing in the post-training setting to confirm DND's advantage. **Recommended action:** Add a matched-setting comparison or qualify the comparison as speculative.

## Score
**Final Score: 5.5/10**

**Rationale:** The paper presents a clearly motivated, post-training-compatible method with reasonable empirical gains across multiple model families. The core idea (selective nested re-processing via lightweight routing) is practical and the ablation study provides useful decomposition of components. However, the absence of any statistical variance or significance testing across all experiments is a critical weakness that prevents full confidence in the reported improvements. Several methodological details (attention masking in nested pass, loss hyperparameters, normalization behavior) are underspecified, and the conclusion overstates contributions without acknowledging important limitations. The strength of the experimental evidence does not yet match the strength of the claims. With major revisions addressing the statistical rigor, methodological transparency, and claim-bounding, the paper has clear potential for acceptance.

**Summary of key issues driving this score:**
- Critical W1: No statistical variance — most core results unverifiable (validity risk)
- Major W2: Attention masking in nested pass underspecified (soundness risk)
- Major W3-W6: Claims not fully supported by evidence (overclaiming risk)
- Major W7: No limitations discussion (completeness)
- Minor W8-W10: Scope and narrative issues (presentation)