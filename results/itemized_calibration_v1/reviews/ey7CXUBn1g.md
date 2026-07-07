Now let me finalize the complete review with the calibrated score.

**Round 1 bracket: 4.0–5.5.** The strongest anchor is AutoTrunc (4.00, similar SVD-for-LLM paper with presentation issues scoring -4/-5 weights for poor presentation) and MoE-SVD (5.00, similar SVD compression paper). ASVD (6.25) had weaknesses about novelty but *no* numerical errors — our paper has concrete verifiable data inconsistencies that ASVD lacked, placing it clearly below that anchor. AutoTrunc's heavy presentation penalties (multiple -4 weights for poor presentation) most closely match our paper's numerical table issues. However, our paper's method (pseudoinverse-based compensation) is technically cleaner than AutoTrunc's learning-based truncation approach. Score: 4.5.

**Anchor summary for score report:**

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| Systematic Review of LLMs | 8QTpYC4smR.md | 1.00 | 1 | No | Irrelevant (survey paper) |
| Implicit Bias in MF | ZTvUT49JjL.md | 3.40 | 1 | No | Different topic (matrix factorization theory) |
| FeDeRA | GtlRN48XYA.md | 3.00 | 1 | No | Different topic (federated learning) |
| CVXQ Quantization | 0T8vCKa7yu.md | 3.00 | 1 | No | Different topic (quantization) |
| TensorGPT | FVgizbs3o2.md | 3.75 | 1 | Yes | Low-rank decomp for LLMs, older models, limited novelty → similar sentence but our paper is less novel |
| MoE-SVD | ho7ZUS1z8A.md | 5.00 | 1 | Yes | SVD compression for MoE; had accuracy degradation issues → comparable scope, our paper has fewer baselines but cleaner results |
| AutoTrunc | 3KEwJGYNzH.md | 4.00 | 1 | Yes | SVD truncation selection; had severe presentation issues (weight -4/-5) → most similar in weakness profile |
| ASVD | HyPofygOCT.md | 6.25 | 1 | Yes | Directly competing SVD method; accepted with weaknesses about novelty/scope. Our paper has verifiable numerical errors this one lacked → below |
| Basis Sharing | gp32jvUquq.md | 6.50 | 1 | Yes | SVD+layer-sharing; accepted, stronger credentials → well above |
| Compressing LLMs (Truth) | B9klVS7Ddk.md | 6.75 | 2 | No | Compression critique paper; different contribution type |
| Table Instruction Tuning | GLmqHCwbOJ.md | 6.33 | 2 | No | Different topic |

**Item-level comparison:** Like AutoTrunc (4.00), this paper has verifiable presentation problems in its main table. Unlike AutoTrunc, the method is clean and the empirical advantage is consistent. AutoTrunc's strongest negative weights came from "Poor Presentation" (-4/-5) and missing experiments (-3). Our paper shares the presentation problem but has fewer missing-experiment issues. This puts it slightly above AutoTrunc (4.00) but below MoE-SVD (5.00) which had no numerical table errors. The decisive factor: numerical inconsistencies in the main results table are a concrete integrity concern, not a subjective judgment.

---

## Summary

AdaSVD proposes two enhancements to SVD-based LLM compression: (1) adaComp, which compensates for SVD truncation errors by solving a least-squares problem via the Moore-Penrose pseudoinverse to update the retained singular matrices, and (2) adaCR, which assigns layer-specific compression ratios based on a cosine-similarity importance metric. The method is evaluated on several LLM families (LLaMA2, OPT, Mistral, Vicuna) and compared against prior SVD-based approaches (vanilla SVD, FWSVD, ASVD, SVD-LLM).

## Strengths

1. **Well-motivated architectural insight.** The paper correctly identifies two genuine limitations of prior SVD-based LLM compression methods: they do not adjust retained singular vectors after truncation (so the remaining components are suboptimal), and they apply a uniform compression ratio across layers despite evidence (Figure 4) that layers differ substantially in importance.

2. **Principled technical solution for the compensation problem.** Reformulating the post-truncation optimization as a least-squares problem (Eq. 8) and solving it via the Moore-Penrose pseudoinverse (Eq. 10) is a sound departure from the numerically unstable direct matrix-inverse approach (Eq. 6). Figure 3(a) visually demonstrates the stability advantage.

3. **Consistent empirical advantage over SVD-LLM across multiple settings.** In Tables 1, 3, and 4, AdaSVD consistently improves over the strongest prior SVD baseline (SVD-LLM) at compression ratios from 40% to 80%, across multiple datasets and model families (LLaMA2-7B, OPT-6.7B, Vicuna-7B, Mistral-7B). The relative improvements are substantial at high compression ratios (e.g., WikiText-2 at 60%: 50.33 vs 89.90).

4. **Orthogonality with quantization demonstrated.** Table 4 shows AdaSVD can be combined with GPTQ 4-bit quantization and outperforms SVD-LLM+GPTQ, confirming complementarity with other compression techniques.

## Weaknesses

### Fatal
None.

### Major

1. **Numerical inconsistencies in Table 1 (the paper's main results table) undermine trust in the evaluation.** Two specific problems are verifiable from the paper as written:
   - **MMLU baseline is impossible.** The uncompressed LLaMA2-7B is reported scoring 7.34 on MMLU (Table 1). LLaMA2-7B's MMLU accuracy is approximately 45% (5-shot) and well above random chance (25%) even zero-shot. A score of 7.34 is physically impossible for this model and indicates a broken evaluation pipeline for that dataset.
   - **C4 perplexity differs between tables.** The uncompressed model's C4 perplexity is reported as 45.30 in Table 1 but 7.34 in Table 4. The standard C4 perplexity for LLaMA2-7B is approximately 7–8, so Table 1's 45.30 is clearly wrong. Since Table 1 is the paper's headline results table, these inconsistencies mean the reader cannot take the quantitative evidence at face value. The paper offers no explanation.

2. **Undefined parenthetical percentages in Table 1.** Every AdaSVD perplexity cell in Table 1 contains a parenthetical percentage (e.g., "14.76 (18%)", "304.62 (158%)", "56.98 (18%)") that is never defined anywhere in the paper. These cannot be interpreted — they are not consistent with relative improvement over the best baseline (e.g., 14.76 vs SVD-LLM's 16.11 is an 8.4% improvement, not 18%). This is a basic presentation failure for the central results table.

3. **Ablation evidence contradicts the multi-iteration framing of adaComp.** Table 3c shows that at every compression ratio tested (40%, 50%, 60%), **1 iteration outperforms both 3 and 15 iterations**. The paper frames adaComp's core mechanism as "alternately updating U and V" (Eq. 16, Algorithm 1, abstract), which strongly implies multiple iterations are part of the value proposition. The paper acknowledges possible overfitting but does not confront the fact that the ablation provides zero evidence that alternating updates beyond a single step are beneficial. Furthermore, the paper claims "under higher compression ratios, additional iterations lead to performance improvements" — yet at 60%, 1 iteration (50.33) beats 3 iterations (64.12), directly contradicting this statement in the same paragraph. The paper either needs to reframe adaComp as a single-step pseudoinverse correction (which is still a valid contribution) or provide evidence from the supplementary 70–80% data if it supports the multi-iteration claim.

### Minor

1. **Paper claims inference acceleration but reports no speed measurements.** The introduction states "SVD compression can effectively accelerate model inference by reducing the memory requirements" (p. 1), but no wall-clock latency, throughput, or tokens/second measurements are reported. Compression ratio alone does not guarantee speedup on target hardware. The practical value for resource-constrained deployment is therefore unclear.

2. **Stack-of-batch component is not independently ablated.** The ablation in Table 3b combines adaCR and data whitening changes but does not isolate the stack-of-batch strategy's independent contribution. Since this is introduced as a distinct technique (Eq. 14–15), its individual effect should be quantified.

3. **mrr ablation boundary issue.** In Table 3d, the best perplexity at 60% is achieved at mrr=0.30, which is the smallest value tested (the boundary of the sweep). The paper cannot conclude optimality without testing lower values.

### Trivial
None.

## Nice-to-Haves
- Report wall-clock inference speed (tokens/second) or latency to substantiate acceleration claims.
- Report the computational overhead (time/memory) of adaComp itself.
- Ablate the stack-of-batch bucket size M.
- Add a brief discussion contextualizing the absolute perplexity gap between compressed models and the uncompressed baseline.

## Removed Points
These points from the input review were removed with justification:
- **"Absolute performance is poor for practical deployment."** Removed: the paper compares against other SVD-based methods as advertised. Absolute numbers are transparently reported and the reader can judge the gap.
- **"No comparison to non-SVD compression methods."** Removed: out of scope. The paper explicitly focuses on SVD-based methods.
- **"Stack-of-batch memory claim skepticism."** Removed: the paper states it was "challenging" on 80GB GPU without specifying sequence length or batch config. This is too speculative to retain as a weakness without being able to verify the exact setup.
- **"Missing Table 2."** Removed: reference to Table 2 in the text is clear; the table likely exists in the appendix (which was stripped by the parser).
- **Reviewer's "Issue 3 (Structural): absolute performance raises questions about practical significance."** Removed: the paper is about advancing SVD-based compression relative to other SVD methods, not about achieving production-ready perplexity. The numbers are reported transparently.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions

1. **Fix the numerical errors in Table 1.** Correct the C4 baseline perplexity (45.30 → correct value ~7.34) and the MMLU baseline accuracy (7.34% → actual accuracy for LLaMA2-7B). Verify every entry in the table against evaluation output to ensure no other transcription errors exist.

2. **Define the parenthetical percentages** in Table 1 in the table caption or a footnote (e.g., "% change relative to the original model perplexity" or "% improvement over the best baseline").

3. **Reframe adaComp honestly.** If 1 iteration consistently outperforms more iterations, state this clearly and position the contribution as a single-step pseudoinverse correction. Remove or heavily qualify the multi-iteration framing. Correct the text in Section 4.3 that claims "under higher compression ratios, additional iterations lead to performance improvements" — this is contradicted by the 60% data in the same table.

4. **Add wall-clock inference speed measurements** (tokens/second) to substantiate the practical acceleration claims in the introduction.

## Score and Decision

The paper addresses a genuine limitation in SVD-based LLM compression with a technically sound pseudoinverse approach, and demonstrates consistent empirical gains over prior SVD methods. However, the main results table contains verifiable numerical inconsistencies (C4 perplexity differs between tables; MMLU baseline is impossible) and undefined annotations — problems that prevent the reader from trusting the headline quantitative evidence. Additionally, the central framing of adaComp as a multi-iteration alternating update is unsupported by the ablation data, which consistently shows 1 iteration is optimal. These are fixable issues, but in their current form they are sufficiently serious to preclude acceptance. The paper needs a corrected evaluation table, honest reframing of the compensation contribution, and completion of missing experimental support before it can be reconsidered.

MY FINAL SCORE: 4.5
MY FINAL DECISION: Reject