Now let me compile the final review.

## Summary

This paper introduces OptMerge and the first structured benchmark for Multimodal LLM model merging. The benchmark covers five capability categories (VQA, Geometry, Chart, OCR, Grounding) across two backbone architectures (InternVL2.5, Qwen2-VL) with both full fine-tuning and LoRA regimes, plus a modality merging path toward Omni-models. The method combines SVD-based task vector denoising with a modified optimization scheme (SGD over Adam, mean initialization) to stabilize WUDI Merging. A theoretical bound (Theorem 3.1) connects merging error to learning rate η, iterations T, and cross-task interference δ. The benchmark is a genuine community resource, and the real-world Hugging Face checkpoint evaluation (Table 6) is convincing.

## Strengths

- **First structured benchmark for MLLM model merging.** Covers five capability categories, two architectures, and two fine-tuning regimes (Sec. 5.1, Table 1). The task categorization is more principled than prior dataset-level divisions, and the public release of weights/code will serve the community.
- **Real-world validation on independently developed Hugging Face checkpoints (Table 6).** Testing on math RL, Pokemon, PDF OCR, and Vietnamese VQA models — where the authors did not control training — directly supports the practical motivation. This is the most convincing empirical result.
- **Computational cost analysis (Table 7).** Concrete figures (0.22h/2.62GB for 1B, 3.78h/21.97GB for 7B vs. 25.38h/240GB and 24.56h/256GB for mixture training) demonstrate the efficiency advantage clearly.
- **Theoretical bound (Theorem 3.1).** Relates merging loss to η, T, and δ — a meaningful formal explanation of why small parameter changes aid merging, independent of the method.
- **Task vector structure analysis (Fig. 2).** Reveals distinct distribution patterns between full FT (right-skewed) and LoRA (multi-modal) models, motivating the method's design and offering diagnostic value for future work.

## Weaknesses

### Fatal
None.

### Major

- **Numerical inconsistencies in reported results.** (a) In Table 3, the WUDI Merging Avg column states 63.65 for Qwen2-VL, but computing the average from the individual per-task scores in the same row yields ~59.97 — a 3.68-point internal discrepancy. (b) The Table 4 ablation lists the WUDI baseline at 58.65, which differs from both the stated and computed values in Table 3. The ablation reports a +4.65% gain over this 58.65 baseline, and the abstract claims a 2.48% average improvement, but neither figure can be reliably verified from the data as presented. These inconsistencies must be resolved for the method's claimed improvements to be credible.

- **OptMerge is not the best method across all settings, despite being framed as universally superior.** On Qwen2-VL capability merging (Table 3), WUDI Merging's stated average (63.65) exceeds OptMerge (63.30). On modality merging (Table 5), TSV Merging (67.34 avg) outperforms OptMerge (67.00). The paper acknowledges these only in passing without analyzing *why* other methods win in these cases — precisely the analysis that would most inform the community about when to use which method.

- **Modality merging evaluation is too thin to support the claims made.** Only two datasets (MUSIC-AVQA, AVQA) are evaluated, both from the same audio-visual QA family. No video-only, audio-only, or text-only evaluation is provided to check for modality degradation. The claim that "complementarity among multiple modalities outperforms individual modalities" (abstract) rests on minimal evidence.

### Minor

- **The claim that model merging "outperforms mixture training" is overstated.** On InternVL2.5 (Table 2), OptMerge (57.44) is below mixture training (57.66). The Qwen2-VL comparison uses Qwen2-VL-Instruct as a proxy for mixture training, which has different pretraining/SFT data — an uncontrolled comparison. The strongest framing of this claim should be tempered.

- **The method combines known components** (WUDI's loss, SVD truncation from prior SVD-based methods, mean initialization, SGD over Adam). The combination is valid and the stability analysis (Fig. 4) is informative, but the contribution should be characterized as an improved optimization procedure for WUDI rather than a fundamentally new merging paradigm.

- **The theoretical bound (Theorem 3.1) is not directly connected to OptMerge.** The paper does not explain which component of the method (SVD truncation, SGD, mean initialization) reduces which term in the bound (δ, ηT). Making this connection explicit would substantially strengthen the paper.

### Trivial
None.

## Nice-to-Haves
- Expand modality merging to more diverse benchmarks, or proportionally temper the claims.
- Add per-task degradation analysis beyond what the rank ablation (Table 8) provides.
- Report results with variance or small-scale significance testing for the tightest comparisons (e.g., 57.44 vs 57.66 on InternVL2.5).

## Removed Points

These points are flagged to be removed, treat them with caution:
- *Criticism that the computational cost comparison (Table 7) does not specify the GPU setup for the proposed method.* The paper states in Sec. 5.1: "All experiments are conducted using 8× NVIDIA V100 GPUs." Both sides use the same hardware.
- *General criticism about missing variance/statistical significance.* Single-run evaluation is standard in the model merging literature; this is not a specific weakness of this paper.
- *Request for ablation on InternVL2.5 in addition to the two settings already ablated.* The existing ablation (LoRA + modality) is adequate.
- *All references to missing appendix content.* The appendix was stripped by the parser, not absent from the original.
- *Formatting/style nitpicks.*

## Novel Insights

None beyond the paper's own contributions. The most informative finding is that OptMerge helps on full FT models but may regress on LoRA models relative to WUDI — but the paper does not analyze this pattern, which is exactly the kind of diagnostic the community needs.

## Suggestions

1. **Resolve the numerical inconsistencies between Tables 3 and 4.** Recompute all averages and ensure the ablation baseline is consistent with the main results. If different evaluation protocols were used, state them explicitly.
2. **Analyze the Qwen2-VL result where OptMerge underperforms WUDI.** This is the most diagnostic result in the paper — what is different about LoRA task vectors that causes the regression?
3. **Connect each component of OptMerge to a specific term in Theorem 3.1's bound** to make the theoretical-methodological link explicit.
4. **Temper the "outperforms mixture training" claim** to reflect the actual evidence (at best "matches or approaches").
5. **Expand modality merging evaluation** or proportionally reduce the strength of claims about modality complementarity.

## Score and Decision

The paper makes a solid benchmark contribution and offers a useful theoretical bound. However, the core method claims are undermined by numerical inconsistencies that prevent independent verification of the reported improvements, and the paper overclaims in several places relative to the evidence. A carefully revised version addressing these issues would be valuable.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>