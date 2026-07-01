## Summary

This paper identifies that standard Rotary Position Embeddings (RoPE) discard the imaginary component of the complex-valued dot product in attention computation. The authors propose RoPE++, which re-incorporates this imaginary component by computing a second set of attention heads using a -π/2 rotation of the query vectors before applying standard RoPE. They introduce two configurations: RoPE++_EH (same number of heads, halved KV cache) and RoPE++_EC (same KV cache, doubled heads). Experiments at 376M and 776M scales across short- and long-context benchmarks show consistent improvements over vanilla RoPE and other position embedding methods.

## Strengths

- **Simple and elegant modification**: The core idea is clean—rotating queries by -π/2 before the standard RoPE computation yields the imaginary attention component with minimal implementation overhead. This is a practical, low-friction improvement that can be readily adopted.

- **Two practical configurations with clear trade-offs**: RoPE++_EH (halved KV cache with comparable performance) and RoPE++_EC (doubled heads with stronger gains at equal cache cost) offer concrete design choices for practitioners depending on whether memory or quality is the priority. The efficiency analysis in Figure 4 quantitatively validates the expected memory and throughput benefits.

- **Extensive experimental evaluation**: The paper evaluates across 2 model sizes (376M, 776M), multiple position embedding baselines (RoPE, FoPE, Pythia, ALiBi), combination with two long-context extension methods (YaRN, Linear PI), and multiple benchmarks (short-context Table 1, long-context Table 2-3). The noise ablation study in Section 5.2 provides direct evidence that imaginary attention contributes more to long-context performance than real attention.

- **Attention pattern analysis adds insight**: The heatmap visualization (Figure 5) shows qualitatively that imaginary heads attend more globally than real heads, and the controlled perturbation experiment quantifies this by showing larger performance drops when imaginary attention is noised compared to real attention.

## Weaknesses

### Major

1. **Theoretical support for the "longer dependency" claim is insufficient**. The paper argues that the imaginary attention's characteristic curve (sine integral) "declines very slowly beyond a certain distance" compared to the real part (cosine integral). However, both curves in Figure 1 appear to decay to near-zero at large Δt, making it visually unclear whether the imaginary component genuinely preserves more long-range signal. The mathematical discussion in Section 3.2 is largely descriptive ("counter-intuitive, since sin(θΔt) is zero at zero relative distance, rises, then falls") without a rigorous comparison of asymptotic behavior or formal proof of why this property would translate to better long-context modeling. The empirical results support the claims, but the theoretical framework promised in the abstract is not fully delivered.

2. **Scale of experiments limits generality of conclusions**. All experiments use models at 376M and 776M parameters—modest sizes by current LLM standards. While this is reasonable for a proof-of-concept, the paper's claims about "long-context LLMs" and practical adoption would be substantially strengthened by at least one experiment at 3B+ parameters. The gap between 776M and production-scale LLMs (7B-70B) is large, and it is not obvious that the benefits persist or remain significant at scale, especially since the imaginary and real heads must share the same QKV parameters.

3. **Limited comparison with relevant recent methods**. The paper baselines against RoPE, FoPE, Pythia (partial RoPE), and ALiBi. However, several competitive RoPE-improvement methods from 2024-2025 are absent: e.g., SelfExtend, CLEX, or LongRoPE. The paper does combine with YaRN and Linear PI but does not directly compare against these methods without the RoPE++ modification. Given that the paper's core contribution is a drop-in replacement for RoPE, a fair comparison against other RoPE variants that also aim to improve long-context handling would help contextualize the gains.

4. **The mechanism of "imaginary attention captures longer dependencies" is not fully disentangled from the increased head count**. In RoPE++_EC, there are effectively twice as many attention heads as the baseline RoPE model. The improvements on long-context tasks could partly arise from this increased representational capacity rather than the specific imaginary-computation property. The noise ablation study helps somewhat, but a controlled comparison where the extra heads use standard RoPE (i.e., doubling heads without the -π/2 rotation) would cleanly separate the effect of the imaginary computation from the effect of more heads.

### Minor

1. **The length extrapolation argument (Section 3.4) is heuristic**. The claim that imaginary attention exposes certain dimensions to "both negative and positive position embedding" and thus reduces extrapolation difficulty is plausible but not rigorously analyzed. The paper does not quantify how many dimensions gain complete positional coverage or under what conditions this matters.

2. **Attention pattern analysis is limited to a few example heads**. Figure 5 shows only 2 layers × 2 heads per model size. Without aggregation across all layers and heads, it is unclear how representative these patterns are. A quantitative summary (e.g., average attention distance per head, fraction of heads with global vs. local patterns) would strengthen the analysis.

## Nice-to-Haves

- An ablation where the same number of extra heads are added with standard RoPE (instead of the -π/2 rotation) would cleanly isolate the contribution of the imaginary computation from the effect of increased head count.
- Results at a larger model scale (3B+ parameters) would substantially increase confidence in the method's practical impact.
- A quantitative characterization of the attention distance statistics across all heads and layers, rather than qualitative examples from two heads.

## Novel Insights

Beyond the paper's own contributions, the observation that the -π/2 rotation of queries before RoPE yields attention heads with systematically different locality bias is a genuine insight. This suggests a general principle: modifying the phase offset in RoPE's complex formulation gives principled control over the range of positional dependencies each attention head specializes in. The finding that these heads naturally split into local (real) and global (imaginary) roles without any learned gating or architectural change is interesting and could inspire further work on designing heterogeneous positional biases within a unified framework.

## Suggestions

- Add an ablation where extra heads use standard RoPE (no -π/2 rotation) with the same head count as RoPE++_EC to disentangle the effect of additional heads from the imaginary computation.
- Provide a more rigorous theoretical comparison of the asymptotic behavior of the real and imaginary characteristic curves (e.g., integral of squared attention weight as a function of distance, or formal decay rates).
- Include experiments at a larger model scale (≥3B parameters) or provide a scaling-law-style analysis to show that the benefits extrapolate.

## Score and Decision

**Score**: 6

**Decision**: Borderline Accept

**Rationale**: This paper presents a clean, novel, and practical idea with solid empirical validation at moderate scales. The core contribution—recovering the discarded imaginary component of RoPE via a simple -π/2 query rotation—is elegant and easy to adopt. The two configurations (EH and EC) offer meaningful practical trade-offs. The experimental evaluation is extensive for the model sizes used, covering multiple baselines, benchmarks, and ablations including combination with existing long-context extension methods.

However, the paper has notable limitations that prevent a higher score: (1) The theoretical justification for why imaginary attention captures longer dependencies is less rigorous than claimed, relying on heuristic arguments rather than formal analysis. (2) The experimental scale (376M and 776M) leaves open questions about behavior at larger model sizes. (3) The comparison set omits several relevant recent RoPE variants, and the gains from RoPE++_EC are not fully disentangled from the simple effect of having more attention heads.

These weaknesses are addressable but weigh against a strong accept. The paper contributes sufficient new knowledge and practical value to warrant borderline acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>