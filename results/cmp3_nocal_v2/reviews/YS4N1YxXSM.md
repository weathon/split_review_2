Now I'll produce the final consolidated review.

## Summary

QUOKA presents a training-free, hardware-agnostic sparse attention method for accelerating transformer inference under chunked prefill. The key insight is that queries with low cosine similarity to the mean query interact more strongly with more keys, so the method retains these "representative" queries and subselects keys using cosine similarity scoring with max-aggregation across queries. The method achieves strong empirical results across RULER, LongBench, NIAH, and Math500 on six model families, with up to 5× attention speedup and 3× TTFT reduction.

## Strengths

1. **Well-motivated problem framing.** The paper correctly identifies that existing query-dependent sparse attention methods are designed for single-query generation, not multi-query prefill, and that naive averaging over queries during chunked prefill degrades accuracy (Section 2.4). This is a genuine gap that QUOKA directly addresses.

2. **Clean, hardware-agnostic design.** QUOKA relies on standard linear algebra operations (cosine similarity, mean, top-k) rather than custom CUDA kernels, making it compatible with any dense attention kernel (FlashAttention, etc.) and portable across CPUs, consumer GPUs, and enterprise GPUs. This portability is demonstrated empirically across three hardware types in Figures 5a–5d.

3. **Decisive empirical results on core benchmarks.** On the RULER benchmark (Table 1, B_SA=1024), QUOKA outperforms all baselines across every model and every sequence length, often by 10–30+ points. The margin is large and consistent. At 25% budget (Table 2), QUOKA stays within 1–3 points of full attention across most settings — a convincing efficiency-accuracy trade-off.

4. **Broad model coverage.** Evaluation across Llama3.2-3B, Qwen2.5-3B, Qwen3-4B, Qwen3-30B-A3B (MoE), SmollM3, and GPT-OSS-20B spans diverse architectures (dense, MoE, NoPE, RoPE), strengthening the claim of generalization.

## Weaknesses

### Fatal
None.

### Major

- **Theorem 1 is not correctly stated in the main text, and its connection to the method is unclear.** The theorem (Section 3.1, lines 143–150) bounds $\text{CosSim}(M_Q, q^*)$ but the variable $q^*$ is never defined in the main text — it is introduced in the theorem statement without a definition. The text then defines the selection score as $S_q = -\text{CosSim}(M_Q, q^*)$, but because $q^*$ is undefined, the theorem cannot be evaluated from the main text alone. Additionally, the theorem concerns the relationship between a fixed $q_0$, a key $k$, and $M_Q$, but the practical scoring function $S_q$ is computed per query independently of any specific key. The paper asserts the theorem provides formal grounding for query subselection, but the logical chain from theorem to algorithm is not established in the presented text. This does not invalidate the method — the empirical observations (Figure 2) are the stronger motivation — but the theoretical framing as presented is confusing and should be corrected or removed.

- **No error bars, variance, or statistical significance reporting for any accuracy result.** Every accuracy table (Tables 1, 2, 3) reports single point estimates without confidence intervals, standard deviations, or any measure of variability. The paper's central claim is "near-baseline accuracy," but without variance information it is impossible to assess how tight "near" is. This is especially relevant where QUOKA reports normalized accuracy > 1.0 on SmollM3 (Table 3: 1.03, 1.028) — the reader cannot distinguish a real phenomenon from evaluation noise. If evaluations are deterministic (e.g., greedy decoding), the paper should state this explicitly and justify why variance is not expected.

### Minor

- **QUOKA occasionally exceeds dense attention without analysis or explanation.** Table 3 reports QUOKA achieving normalized accuracy > 1.0 on SmollM3 (1.03 at B_SA=1024, 1.028 at B_SA=2048). The paper acknowledges this ("in some cases even surpasses the accuracy of dense attention," Section 4.4) but offers no analysis of why a sparse method would outperform the dense baseline. While benign explanations exist (e.g., sparsity acting as a regularizer, or the dense chunked-prefill baseline having its own degradations), the absence of any discussion leaves the reader unable to assess whether this reflects a real property or an artifact. The "Full" baseline in Figure 4 (NIAH) also shows lower accuracy than QUOKA, raising the same question.

- **The geometric motivation (Figure 2) is shown for only a single setting.** The empirical observation that drives the method — queries with lower cosine similarity to the mean attend to more keys — is demonstrated on a single layer (layer 0), a single head (head 11) of a single model (Llama 3.2-3B). The PCA visualization (Figure 2b) is qualitative, and the correlation of 0.737 between $S_q$ and $\max_k(A)$ (Figure 2c) is shown for only this one setting. Showing this pattern holds across layers and heads would substantially strengthen the claimed generality.

- **The speedup analysis does not separate selection overhead from attention savings.** The paper reports 5× attention module speedup and 3× TTFT reduction (Section 4.6). However, QUOKA's selection process (computing query means, cosine similarities, top-k, gathers) has non-trivial cost. The attention module-level speedup (Figure 5a) is measured for the *sparse attention itself* relative to dense attention, but it is not stated whether this includes QUOKA's selection overhead or excludes it. If excluded, the 5× figure overstates the practical gain at the module level. The TTFT speedup (3×) being notably lower than the attention speedup (5×) is consistent with selection overhead eating into gains, but this is never analyzed or broken down.

### Trivial

- **Empty cell in Table 1.** The RULER result for GPT-OSS-20B at 32k is left blank. This should be filled or explained.

## Nice-to-Haves

- A breakdown of QUOKA's total latency into (a) selection cost and (b) sparse attention cost would make the speedup claims actionable for practitioners.
- Showing that the $S_q$–attention-strength correlation (Figure 2c) holds across multiple layers and heads would strengthen the geometric motivation.
- Including all sparse-attention baselines in the main NIAH figure (Figure 4), rather than relegating them to the appendix, would strengthen the visual comparison.

## Removed Points

The following points from the input review were removed after cross-checking against the paper:

- **"Baselines not fairly configured for prefill"** — Removed because the paper is fully transparent about this limitation (Section 2.4: "Extending these methods to the multiple-query setting... significantly degrades performance"). This is presented as motivation for QUOKA, not a hidden flaw. The paper also includes SampleAttention (a prefill-specific baseline) which QUOKA outperforms. The headline margin is partly due to this asymmetry, but the paper does not misrepresent it.

- **"Missing code"** — Removed per guidelines: nitpicks about reproducibility that involve artifacts impractical for a submission.

- **"Missing appendix content"** — The parser strips appendix sections from all papers. The theorem proof is in Appendix D and the ablation tables are in the appendix; these are assumed to exist in the original submission.

- **Generic/scope-creep criticisms** — Removed per filtering discipline. Examples: requesting error bars for evaluations where single-run is the norm, requesting more prefill baselines when SampleAttention is already included.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct or remove Theorem 1. If the geometric intuition is primarily empirical, present it as such — the empirical observations (Figure 2) are already the paper's strongest motivation. A theorem with an undefined variable does more harm than good.

2. Add variance information. Even a brief statement that evaluations are deterministic under greedy decoding (if true) would address the concern. Alternatively, report 3–5 seeds on a subset of conditions.

3. Clarify the selection overhead: state explicitly whether the attention module-level speedup (Figure 5a) includes or excludes QUOKA's selection cost, and provide a breakdown.

4. Explain the >1.0 normalized accuracy values on SmollM3 in Table 3, or add error bars to show they are within noise.

## Score and Decision

QUOKA addresses a genuine problem with a clean, well-executed method. The empirical results on RULER and LongBench are strong and consistent across diverse models. The main weaknesses — an unclear theorem statement that does not affect the empirical validity of the method, and missing variance reporting — are addressable and do not undermine the core contribution. The paper makes a solid, practical contribution.

<score>7</score>
<decision>Accept</decision>