Now I have enough calibration data. Let me compile the final review.

**Round 1 bracket:** [4.0, 5.5] — Anchored between AutoTrunc (4.00, same SVD-LLM compression topic) and MoE-SVD (5.00, SVD compression for MoE). ASVD (the actual baseline paper) scored 6.25 but was rejected for incremental novelty.

**Round 2 narrowing:** Comparing itemized favorabilities, AdaSVD's strengths (8.37–8.60) are solid but unexceptional — comparable to AutoTrunc's (8.22–9.55) and below ASVD's (8.35–10.71). The major weakness (iteration contradiction, favorability 1.58) is a genuine reporting flaw that AutoTrunc and MoE-SVD don't have. The paper is better than AutoTrunc (broader model evaluation, includes quantization integration) but the text-vs-data contradiction is a meaningful credibility issue. Final placement: **4.5**.

---

## Summary

This paper proposes AdaSVD, an SVD-based LLM compression method with two refinements over the SVD-LLM baseline: (1) **adaComp**, which alternately updates the retained singular matrices U and V using Moore-Penrose pseudoinverses to compensate for truncation error, and (2) **adaCR**, which assigns layer-specific compression ratios based on input-output cosine similarity. Experiments on LLaMA2-7B, OPT-6.7B, Vicuna-7B, and Mistral-7B show consistent perplexity improvements over SVD-LLM at 40–60% compression ratios.

## Strengths

- **Well-motivated problem** (favorability=8.37): The paper identifies two genuine gaps in prior SVD-based LLM compression — the lack of post-truncation compensation for retained singular vectors, and the uniform compression ratios across layers of varying importance.

- **Sensible technical solution for adaComp** (favorability=8.60): Reformulating the U/V update as a least-squares problem and solving via Moore-Penrose pseudoinverse (Eqs. 8–13) is principled and avoids numerical instability of direct matrix inversion. Figure 3(a) demonstrates smoother convergence compared to naive updates.

- **Consistent empirical improvements over SVD-LLM** (favorability=8.36): Across compression ratios 40%, 50%, and 60% in Table 1, AdaSVD achieves lower perplexity than SVD-LLM on WikiText-2, PTB, and C4. At 60% on WikiText-2, AdaSVD (50.33) substantially improves over SVD-LLM (89.90). Improvements on commonsense reasoning benchmarks are smaller but generally positive.

- **Ablation studies mostly disentangle the two components** (favorability=8.56): Table 3b shows adaCR provides additional gains on top of adaComp (e.g., WikiText-2 at 60%: 69.46 with constant CR → 50.33 with adaptive CR), and Table 3a confirms adaComp itself produces most of the gain over SVD-LLM.

## Weaknesses

### Fatal
None.

### Major

- **The paper's claim about iteration count in Section 4.3 is contradicted by its own data in Table 3c** (favorability=1.58). The text states: *"In contrast, under higher compression ratios, additional iterations lead to performance improvements."* However, Table 3c shows the opposite pattern at every compression ratio presented:

  | Target CR | 1 iter (WikiText2 / C4) | 3 iter (WikiText2 / C4) | 15 iter (WikiText2 / C4) |
  |---|---|---|---|
  | 40% | **14.76** / **56.98** | 15.47 / 57.28 | 15.84 / 57.39 |
  | 50% | **25.58** / 113.84 | 27.11 / 115.51 | 27.45 / **110.35** |
  | 60% | **50.33** / **239.18** | 64.12 / 301.19 | 62.34 / 267.29 |

  At 60% — the "higher compression ratio" the text specifically refers to — 1 iteration dramatically outperforms 3 and 15 iterations on both datasets (e.g., 50.33 vs. 64.12/62.34 on WikiText-2). The supplementary material at 70%/80% may show a different pattern, but the claim as stated with reference to the data actually presented in Table 3c is unsupported and misrepresents the evidence.

### Minor

- **Undefined parenthetical percentages in Table 1** (favorability=5.15): Entries like "14.76 (18%)", "304.62 (158%)" appear throughout the table without definition in the text or caption. It is unclear what these percentages represent.

- **adaCR importance metric lacks validation** (favorability=-0.18): Cosine similarity between input X and output WX (Eq. 17) is adopted as the importance measure without comparison against alternative metrics (e.g., output magnitude, gradient-based sensitivity, per-layer perturbation analysis). The paper notes other metrics could be used but does not justify the choice or show it correlates with actual compressibility.

- **No computational cost analysis** (favorability=3.16): The alternating update requires per-layer SVD on A (Eq. 9) at each iteration, adding overhead beyond SVD-LLM. Wall-clock time or FLOP comparisons with baselines are absent.

- **Stack-of-batch parameters not reported** (favorability=5.21): The actual values of N (total calibration samples), M (bucket size), and mini_bsz used in experiments are not stated, making it difficult to assess the memory-accuracy trade-off.

### Trivial
None.

## Nice-to-Haves

- The paper could validate the cosine-similarity importance metric against at least one alternative (e.g., per-layer sensitivity analysis) to strengthen the adaCR claim.
- Reporting wall-clock time for the adaComp alternating update vs. SVD-LLM would help contextualize the computational overhead.
- The "bowl shape" observation for LLaMA layer importance (both early and late layers important) is noted but not analyzed; a brief discussion of why this pattern emerges would be beneficial.

## Removed Points

These were raised in the input review but removed per filtering rules:

- **Table 2 missing from extracted text** — Parser artifact; the original submission contains Table 2. (Rule: parser artifact)
- **Perplexity values too high for practical deployment** — Field-wide property of aggressive SVD compression, not specific to AdaSVD; the paper advances relative methodology. (Rule: scope creep)
- **Original C4 perplexity inconsistency** — Parser artifact from column misalignment in extracted Table 1. (Rule: parser artifact)
- **FWSVD/ASVD failure at 60%** — The paper acknowledges this and compares against SVD-LLM. (Rule: strawman)
- **"Bowl shape" not analyzed / CR normalization** — Minor presentation details, not core claims. (Soft rule: scope creep)
- **Missing related works** — Cannot verify without external sources. (Hard rule)

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Correct the iteration-number claim** in Section 4.3 to accurately reflect Table 3c's data. If the supplementary 70%/80% results show a different pattern (where more iterations help), move those results to the main text to support the claim. Otherwise, retract the claim and explain why 1 iteration is sufficient (e.g., the calibration set is small enough that a single closed-form pseudoinverse update suffices).

2. **Define the parenthetical percentages** in Table 1, or remove them if they are formatting artifacts.

3. **Report the N, M, and mini_bsz values** used in the stack-of-batch strategy so readers can evaluate the memory-accuracy trade-off.

4. **Add wall-clock time** comparison against SVD-LLM to show the practical cost of the alternating update.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/wg25r/.../8QTpYC4smR.md | 1.00 | R1 | No | Unrelated survey paper; far weaker |
| /home/wg25r/.../gwZ90hFSL2.md | 1.00 | R1 | No | Unrelated cross-lingual paper; far weaker |
| /home/wg25r/.../P49gSPmrvN.md | 1.00 | R1 | No | Unrelated visualization paper; far weaker |
| /home/wg25r/.../ZTvUT49JjL.md | 3.40 | R1 | No | Matrix factorization theory; tangential |
| /home/wg25r/.../04RLVxDvig.md | 3.00 | R1 | No | MoE parameter efficiency; tangential |
| /home/wg25r/.../orG37FHN4b.md | 3.00 | R1 | No | Data-free quantization; tangential |
| /home/wg25r/.../3KEwJGYNzH.md | 4.00 | R1 | Yes | **AutoTrunc**: same SVD-LLM compression topic. AdaSVD tests more model families and includes quantization, but has the iteration contradiction AutoTrunc lacks. AdaSVD is slightly better overall → 4.5 |
| /home/wg25r/.../ho7ZUS1z8A.md | 5.00 | R1 | Yes | **MoE-SVD**: SVD compression for MoE models. AdaSVD has a cleaner contribution but a more serious reporting error. Comparable quality → 4.5 |
| /home/wg25r/.../FVgizbs3o2.md | 3.75 | R1 | No | **TensorGPT**: tensor-train decomposition. Different method; AdaSVD is stronger |
| /home/wg25r/.../uAtDga3q0r.md | 6.00 | R1 | Yes | **RaNA**: adaptive rank allocation. More polished; AdaSVD is weaker |
| /home/wg25r/.../DLDuVbxORA.md | 6.25 | R1 | Yes | **OATS**: sparse+low-rank decomposition. Stronger paper; AdaSVD is weaker |
| /home/wg25r/.../HyPofygOCT.md | 6.25 | R2 | Yes | **ASVD** (original): pioneering activation-aware SVD, but rejected for incremental novelty vs. SVD-LLM. AdaSVD is similarly incremental over SVD-LLM and has the iteration flaw → lower |
| /home/wg25r/.../FA3iYp1y6z.md | 5.00 | R3 | No | Low-rank correction for quantization; tangential |
| /home/wg25r/.../s6Q7aVZWIn.md | 4.50 | R3 | No | Pruning + low-rank refinement; tangential |
| /home/wg25r/.../hHNVn4hFPk.md | 5.25 | R3 | No | LoRA serving; tangential |

**Bracket (R1):** [4.0, 5.5] — between AutoTrunc (4.00) and MoE-SVD (5.00).

**Narrowing (R2–R3):** AdaSVD's strengths (8.37–8.60 favorability) are solid but comparable to AutoTrunc's (8.22–9.55) and below ASVD's (8.35–10.71). The major weakness (1.58) about the iteration contradiction is a concrete reporting flaw absent from the closest anchors. The contribution is incremental over SVD-LLM — similar to how ASVD (6.25) was seen as incremental and rejected. AdaSVD is better than AutoTrunc (broader evaluation, quantization integration) but has a clearer reporting error. Final placement is between 4.0 and 5.0.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>