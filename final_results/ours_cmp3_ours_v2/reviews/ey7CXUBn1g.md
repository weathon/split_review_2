Now I have a comprehensive calibration picture. Let me finalize the review.

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses
// List only reasonable points. Rank by severity.

### Fatal
None.

### Major
- weakness 1 — why it matters
- weakness 2 — why it matters

### Minor
- weakness 1 — why it matters

### Trivial
None.

## Nice-to-Haves
- suggestion that would improve but is not a core flaw

## Removed Points
Include something like this "These points are flagged to be removed, treat them with caution"

## Novel Insights
One paragraph synthesizing genuinely novel observations.

## Suggestions
- specific actionable suggestion

## Score and Decision

Now let me write the final review.

---

## Summary

AdaSVD proposes two improvements to SVD-based LLM compression: (1) **adaComp** — post-truncation alternating least-squares updates of the retained U and V matrices to minimize the *output-space* error (‖ŴX − WX‖²_F) rather than only the matrix reconstruction error, using Moore-Penrose pseudoinverse for numerical stability; and (2) **adaCR** — layer-wise adaptive compression ratios based on input-output cosine similarity to allocate more parameters to more important layers. Experiments span LLaMA2-7B, OPT-6.7B, Vicuna-7B, Mistral-7B, and LLaVA across language modeling and common-sense reasoning benchmarks.

## Strengths

1. **The core limitation it targets is real and well-motivated.** Prior SVD compression methods (FWSVD, ASVD, SVD-LLM) truncate singular values but leave the retained U/V matrices as-is. The observation that these should be adjusted to minimize output error (Eq. 4) rather than just the matrix reconstruction error is the paper's clearest insight and is convincingly set up in the introduction.

2. **Clean, informative ablation structure.** Table 3(a–d) isolates the effects of adaComp and adaCR independently and shows they combine constructively. The hyperparameter sweeps (iteration count, minimum retention ratio in Tables 3c, 3d) provide useful sensitivity information for practitioners.

3. **Reasonable model breadth.** Evaluation across LLaMA2-7B, OPT-6.7B, Vicuna-7B, Mistral-7B, and LLaVA (VLM) demonstrates the method generalizes beyond a single model family.

4. **Orthogonality to quantization is demonstrated.** Table 4 shows AdaSVD stacks with GPTQ-INT4 and consistently outperforms SVD-LLM+GPTQ-INT4, which is practically valuable.

## Weaknesses

### Fatal
None.

### Major

- **Missing runtime and memory measurements despite explicit claims about deployment efficiency.** The abstract and introduction repeatedly state that AdaSVD "reduces memory requirements for deployment" (line 9) and that SVD compression "can effectively accelerate model inference by reducing the memory requirements" (line 47), yet the paper reports *zero* actual speed, throughput, or peak-memory measurements. Parameter-count reduction (Eq. 20) is a proxy, not the quantity of practical interest. This gap is especially acute because adaCR's per-layer variable ranks produce irregular U/V matrix shapes that may not map efficiently onto hardware-optimized GEMM kernels; the paper's claim that SVD is "more versatile across different platforms because it does not require specialized hardware or custom operators" (lines 47–48) is asserted without evidence against this specific concern. For a compression paper at a top venue, this is a significant evaluative gap.

- **Iteration-ablation claim contradicts the data shown in the main text.** Section 4.3 states: "under higher compression ratios, additional iterations lead to performance improvements." Table 3(c) shows the opposite at 60% (the highest compression ratio shown in the main text): 1 iteration achieves PPL 50.33 on WikiText-2, while 3 iterations give 64.12 and 15 give 62.34 — both *worse* than 1 iteration. The same pattern holds on C4 (239.18 → 301.19 → 267.29). The claimed trend may hold at 70–80% (deferred to the appendix), but the text as written is misleading when read against the data actually presented in Table 3(c). This is a concrete factual discrepancy that undermines trust in the paper's claims about the method's behavior.

### Minor

- **Global compression-ratio enforcement in adaCR is underspecified.** Equation (19) defines CR(W) = mrr + I_n(W)·(trr−mrr). Since I_n(W) can exceed 1 (after the mean normalization of Eq. 18, average is 1), some layers can receive CR(W) > trr. The paper defines per-layer ratios but never describes a renormalization or capping mechanism to ensure the overall target compression budget is actually met. This is a missing algorithmic detail that directly affects reproducibility.

- **The SoB strategy's baseline ("NC") is undefined.** Figure 3(b) compares the stack-of-batch strategy against "NC" (naive calibration), but "NC" is never defined in the paper — leaving the reader to guess whether it means using individual samples, a single batch, or no stacking at all. This makes the empirical justification for SoB difficult to evaluate.

- **The adaCR importance metric (cosine similarity between X and Y=WX) is unvalidated against alternatives.** The paper adopts cosine similarity "for simplicity" (line 226) and cites Men et al. (2024) and Dumitru et al. (2024) for inspiration, but never compares against other plausible importance metrics (e.g., Fisher information as in FWSVD, Hessian-based importance as in SparseGPT, or actual perplexity impact of dropping a layer). While Table 3(b) shows adaCR improves over a uniform ratio, the specific choice of metric is not justified.

- **Baseline table presentation could mislead.** Table 1 includes FWSVD and ASVD alongside the meaningful baselines. The paper itself acknowledges that "FWSVD and ASVD fail on these LLMs with compression ratios under 60%" (line 307), producing perplexities in the thousands. Including non-functional baselines in the main comparison table without a clear visual distinction (a footnote or separator in the table itself) can mislead a casual reader into overestimating the improvement margin. The paper is transparent in the prose but the table presentation is at odds with that transparency.

### Trivial
None.

## Nice-to-Haves

- Report wall-clock inference time and peak GPU memory for compressed models at representative compression ratios across at least one model family. This would directly substantiate the deployment-efficiency claims.
- Validate the cosine-similarity importance metric against alternatives (Fisher information, Hessian-based metrics, or the empirical perplexity change when a layer is entirely removed).
- Report multiple seeds / error bars for main results, since calibration data is only 256 randomly sampled sentences.

## Removed Points

These points from the harsh-critic input are removed, with justifications:

1. **"SoB is conceptually flawed — averaging text sequences destroys information"** (Harsh Critic #1): This overstates the problem. Averaging input representations to fit more calibration data into GPU memory is a pragmatic approximation for least-squares weight updates. The critic's suggested alternative ("gradient accumulation") does not apply here because the SVD/pseudoinverse update (Eqs. 9–10) requires the full data at once. The valid sub-concern (undefined "NC" baseline) is retained as a Minor weakness above.

2. **"Eq. 6 vs Eq. 10 difference is just standard numerical advice"** (Section-by-Section notes): Technically correct but irrelevant to the paper's contribution, which is applying the ALS framework in the SVD-truncation context, not inventing a new numerical method.

3. **"Two-fold strategy framing overstates the contribution"**: A presentational choice, not a substantive weakness.

4. **"Hsu et al. citation inconsistency"**: Parser artifact, not a paper error.

5. **"Table 2 is missing"**: Parser truncation issue (the appendix is stripped).

6. **"No limitations section"**: A formatting preference, not a flaw. Many papers do not include an explicit limitations section.

7. **"Missing related works"**: Removed per instruction — external sources are unavailable to verify existence of cited works.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's most useful observations are about concrete evaluative gaps (missing runtime benchmarks, the iteration-claim data mismatch) rather than novel analytical insights about the method itself.

## Suggestions

1. Add actual latency and peak-memory benchmarks for compressed models at 40–80% compression ratios. This is the single highest-leverage improvement.
2. Correct the iteration-ablation claim in Section 4.3: either clarify that the improvement holds only for 70%+ compression (and move those results to the main text), or revise the claim to match the shown data.
3. Define "NC" (naive calibration) explicitly.
4. Describe how the global compression budget is enforced under adaCR when some layers exceed trr.
5. Add a visual separator or explicit footnote in Table 1 to distinguish non-functional baselines (FWSVD, ASVD at ≤60%) from meaningful comparisons.
6. Provide a brief comparison against or discussion of alternative importance metrics for adaCR.

## Score and Decision

**Calibration anchors (all from the deepreview_13k_calibration corpus):**

| Path | Avg Human Score | Round | Comparison to AdaSVD |
|------|----------------|-------|----------------------|
| ASVD (HyPofygOCT.md) | 6.25 | Q4 | Direct baseline; similar strengths and the same missing-runtime weakness. AdaSVD has a clearer novel component (post-truncation compensation) but also has the claim-data mismatch issue. |
| AutoTrunc (3KEwJGYNzH.md) | 4.00 | Q3 | SVD compression paper; narrower model scope and weaker evaluation. AdaSVD is stronger on both method and evaluation. |
| MoE-SVD (ho7ZUS1z8A.md) | 5.00 | Q3 | SVD-based compression; similar missing-runtime criticism and also rejected. AdaSVD has better ablation structure. |
| Low-Rank Correction for Quantized LLMs (FA3iYp1y6z.md) | 5.00 | Q3, read | Similar missing-efficiency-measurements criticism; comparable overall quality. |
| Basis Sharing (gp32jvUquq.md) | 6.50 | Q4 | SVD compression accepted paper; includes throughput measurements which AdaSVD lacks. |
| CVXQ (0T8vCKa7yu.md) | 3.00 | Q2 | Quantization paper rejected for ignoring hardware constraints — similar missing-efficiency critique but weaker overall. |

**Bracket (Round 1):** The paper sits above AutoTrunc (4.00) and CVXQ (3.00) but below ASVD (6.25) and Basis Sharing (6.50) in overall quality. The closest matches are MoE-SVD (5.00) and Low-Rank Correction (5.00). Plausible range: **4.5–5.5**.

**Final score:** 5.0. The paper has a genuine contribution (adaComp's post-truncation compensation is novel and well-motivated) and clean ablation experiments across multiple model families. However, the absence of any runtime or memory measurements is a significant gap for a compression paper claiming deployment benefits, and the iteration-ablation text contradicts the data shown in Table 3(c). These issues prevent the paper from meeting the acceptance bar at a top venue, but the core idea is worth publishing after the gaps are addressed.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>