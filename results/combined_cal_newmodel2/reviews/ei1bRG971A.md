Now I have strong calibration context. Let me produce the final review.

## Summary

This paper introduces Dynamic Nested Depth (DND), a post-training method that identifies "critical" tokens via a token-choice router and reprocesses them through the same transformer layer. The method includes a dual-loss router training strategy (score dispersion + distribution preservation) and a dynamic threshold control scheme with EMA synchronization. DND is evaluated across three dense 1B-class models (Qwen3, Llama3.2, Gemma3) and one 30B MoE model (Qwen3-30B-A3B), showing consistent improvements of +1.88% to +2.61% on small models and +0.87% on the 30B MoE model, with modest throughput overhead (7-9%).

## Strengths

- **Clean architectural design.** The paper correctly identifies the information leakage issue with expert-choice routing in autoregressive models (Sec 3.1.1) and adopts token-choice routing with a normalized fusion mechanism (Eq. 4) that gates nested-pass contributions by the token's own routing score, a sensible design choice.

- **Well-motivated router training.** The dual-loss strategy (score dispersion via entropy maximization + distribution preservation via MSE pull toward 0.5, Sec 3.2.1) addresses a genuine challenge in making token-choice router outputs sufficiently discriminative for stable threshold-based selection.

- **Reproducibility-friendly.** DND is a post-training method applicable to off-the-shelf pre-trained models via SFT, avoiding MOR's requirement of pre-training from scratch on 200B tokens. The method is evaluated across three model families (Qwen, Llama, Gemma) and both dense and MoE architectures, providing some evidence of generality.

- **Useful threshold control diagnostics.** Figures 5, 6a, and 6b provide concrete demonstrations of how buffer proportional control and EMA synchronization stabilize the selection ratio during training, which is helpful for practitioners.

## Weaknesses

### Major

- **The ablation does not test the claimed combination of router control (RC) and threshold control (TC).** Table 4 shows eight DND variants, but none has both RC=✓ and TC=✓ simultaneously. The paper's central claim (Abstract, Sec 4.4, line 251) is that RC and TC are "complementary components" and that "their combination leads to a clear improvement of approximately one percentage point in average accuracy." This claim cannot be verified from the presented data. Furthermore, the best-performing variant in the ablation (Col 2: RC=✓, TC=–, Δ=+1.88) achieves the same score as the full DND result reported in Table 1 — yet this column has TC=–, which is inconsistent with the method description (Sec 3.2.2) that presents threshold control as an integral component. The paper needs to either (a) add the RC+TC column and show its advantage over RC alone, or (b) revise the complementarity claim.

- **Baseline comparisons are insufficient for a new-method paper.** The only alternative dynamic-computation method compared is ITT, and only on Qwen3-1.7B (Table 1, ITT Δ=+0.05 vs DND Δ=+1.88). For Llama3.2-1B and Gemma3-1B, no ITT or other method comparison is shown. For the 30B MoE model (Table 2), there is **no comparison against any existing dynamic-computation method** — only vanilla SFT. The paper mentions MOR (Bae et al., 2025) as the most closely related work but dismisses it as requiring pre-training from scratch without attempting to adapt it to the post-training setting or providing a comparable baseline at scale. A new-method paper at this venue needs to demonstrate advantage over reasonable alternatives, not just over vanilla SFT.

### Minor

- **No uncertainty quantification.** On the Qwen3-30B-A3B model (Table 2), several per-benchmark improvements are very small (BBH +0.13, MATH +0.15, MATH-500 +0.20, CMMLU +0.37). Given typical benchmark variance of 1–3% on single runs, these values are uninterpretable without confidence intervals or multiple seeds. This is a common limitation in LLM papers at this scale but limits the paper's evidential strength.

- **Insufficient evidence for qualitative claims about hierarchical processing.** Section 4.5 (Fig 7b) claims that "tokens selected by shallower layers are predominantly essential nouns, while those selected by deeper layers correspond to more abstract or syntactically critical components." This claim about a hierarchical processing strategy rests on a single GPQA example, which is far too little evidence.

- **Unsubstantiated positional embedding design choice.** The design in Sec 3.1.2 (Eq. 3) assigns new positional embeddings ($\mathbf{E}_{\text{pos}}^i$) to packed selected tokens during the nested pass. Since tokens have not changed their original sequence positions, altering their position encoding could disrupt position-sensitive attention patterns. No ablation or justification for this choice is provided.

### Trivial

None.

## Nice-to-Haves

- Report the RC+TC combination in Table 4 to resolve the ablation ambiguity.
- Add a competitive baseline at scale — at minimum, reproduce ITT on Qwen3-30B-A3B.
- Include variance estimates (3 runs with standard deviations) for main results.
- Provide an ablation comparing the proposed positional embedding assignment against alternatives (e.g., keeping original position IDs).
- Explicitly discuss the cost-benefit tradeoff: DND incurs 7-9% throughput reduction for a 0.87% average gain on the 30B model.

## Removed Points

These points are flagged to be removed, treat them with caution:
1. "The 6% FLOPs claim for 20% token reprocessing is unsubstantiated" — This criticism references content in the appendix (Sec A), which was stripped during PDF parsing. Per policy, missing appendix content cannot be used as a weakness.
2. "ITT baseline claims are insufficient because ITT may not have been well-tuned" — This is speculation about implementation quality, not a verified weakness.
3. "The paper's framing as the first to propose adaptive computation for hard tokens is overstated" — The paper acknowledges ITT and MOR as related work.
4. "Correlation analysis (r=0.34) is weak" — The paper describes this honestly as a modest correlation, not an overclaim.
5. "Cost-benefit discussion missing" — Moved to Nice-to-Haves as it's scope-appropriate for a suggestion but not a core weakness.
6. "Generalization to different DND depths not explored" — Nice-to-have extension, not a core weakness.

## Novel Insights

None beyond the paper's own contributions. The review surfaces one important gap not discussed in the paper itself: the combination of RC and TC is never explicitly tested in the ablation, even though the paper's central claim about complementarity hinges on it.

## Suggestions

1. **Complete the ablation.** Add the RC+TC column to Table 4. If RC+TC outperforms RC alone, the complementarity claim is supported. If not, revise to acknowledge that most gain comes from the router loss alone, with threshold control being primarily a stabilization mechanism for training.
2. **Add competitive baselines at scale.** At minimum, compare against ITT on Qwen3-30B-A3B to demonstrate that DND outperforms existing methods, not just vanilla SFT.
3. **Report variance.** Include 3 runs with standard deviations for main results (at least for the 30B model) to confirm that small per-benchmark gains are statistically reliable.
4. **Address the positional embedding design.** Either justify why new positional embeddings are assigned to packed selected tokens, or ablate this choice.

## Score and Decision

### Calibration Anchors

| Path | Avg Human Score | Round | Itemized? | Comparison |
|------|----------------|-------|-----------|------------|
| `/home/.../ulGwcj1egv.md` (FiRST) | 3.00 | R1 | Yes | Also a post-training router method for adaptive computation. Scored lower due to missing ablation and weaker evaluation. This paper has stronger evaluation breadth. |
| `/home/.../jIAKjjEmWi.md` (A-MoD) | 4.00 | R1 | Yes | Token routing for MoD. Similar limitations in baseline scope. Score 4.00. |
| `/home/.../7igPXQFupX.md` (CoTFormer) | 5.75 | R1 | Yes | Adaptive computation depth via weight-tying. Stronger novelty claims but also faced evaluation concerns. |
| `/home/.../UvYrFbKj8j.md` (Stutter) | 4.50 | R2 | Yes | Very similar approach (selective additional layers for hard tokens). Scored 4.50 with concerns about unconvincing improvements and missing baselines. |
| `/home/.../J2FyEVg8HR.md` (CITER) | 4.75 | R2 | Yes | Token-level routing for collaborative inference. Better evaluation but similar novelty concerns. |
| `/home/.../PPjpGTPG5K.md` (PERFT) | 5.33 | R2 | Yes | MoE-focused PEFT. Higher but inconsistent across reviewers (5, 3, 8). |
| `/home/.../tI3eqOV6Yt.md` | 5.00 | R1 | No | Adaptive computation over task complexity. Less directly related. |

### Calibration Path

**Round 1 bracket:** 4.0–5.0, between FiRST (3.00) and Stutter (4.50)/CITER (4.75). The paper's evaluation is broader than FiRST, but its core evidential gap (ablation of RC+TC not tested) is more damaging than Stutter's weaknesses. The item comparisons: FiRST's negative items included missing ablation (0.45) and insufficient baselines (-0.68, -2.00). My paper's ablation gap (0.08) and baseline gap (-1.99) are similarly severe, but my positive items (11.32–12.16) substantially exceed FiRST's positives (5.07–8.38). Against Stutter (4.50), my negative items (0.08, -1.99) are somewhat less severe than Stutter's worst negatives (-3.95), and my positives (11.32–12.16) are comparable. However, the ablation gap directly undermines a central claim, which is a more fundamental issue than Stutter's concerns about inconsistent gains.

**Round 2 narrowing:** Comparing against Stutter (4.50) and CITER (4.75), the ablation gap is the decisive factor — the paper claims complementarity of RC and TC without testing the combination. This pushes the score below the Stutter paper's 4.50. The insufficient baselines further weigh against it. **Final score: 4.0**, placing it clearly in the Reject range but acknowledging the genuine architectural and training contributions.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>