Now let me compose the final review.

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses
### Fatal
### Major
### Minor
### Trivial

## Nice-to-Haves

## Removed Points

## Novel Insights

## Suggestions

## Score and Decision

Let me write the final output:

---

## Summary

ARSS introduces the first GPT-style decoder-only autoregressive model for novel view synthesis (NVS) from a single image with explicit camera control. The method combines a video tokenizer for temporally consistent discrete tokens, a camera autoencoder that converts Plücker raymaps into 3D positional tokens, and a hybrid token permutation strategy that preserves temporal order while randomly shuffling spatial order. Experiments on RealEstate10K, ACID, and DL3DV show competitive results against diffusion-based NVS methods.

## Strengths

- **First AR-based approach to NVS with explicit camera control.** The paper correctly identifies that GPT-style decoder-only autoregressive models have not been applied to novel view synthesis with camera conditioning, and provides a concrete instantiation. (Section 1, Section 5)

- **Well-motivated camera token design.** The camera autoencoder maps per-pixel Plücker raymaps into tokens with matched spatial/temporal resolution as visual tokens, with geometric constraints (unit-norm rays, orthogonality of direction and momentum in Eq. 5). This avoids compressing the full camera trajectory into a single global condition vector and provides localized 3D guidance per token. (Section 3.2.2)

- **Hybrid token permutation strategy.** The approach of randomly permuting spatial order within each frame while preserving temporal order across frames is a principled adaptation of prior work to the multi-view setting. The ablation (Table 2) clearly demonstrates its advantage over both raster ordering and full spatiotemporal permutation. (Section 3.2.3, Table 2)

- **Per-frame error accumulation analysis.** Figure 6 tracks PSNR/SSIM/LPIPS over a 17-frame sequence, showing that ARSS degrades more slowly than baselines. This directly supports the paper's thesis about the benefits of causal generation for long sequences. (Figure 6, Section 4.2)

## Weaknesses

### Major

- **Unexplained numerical discrepancy between main results and ablation results.** Table 1 reports the "Ours" method on RealEstate10K with PSNR=19.02, SSIM=0.624, LPIPS=0.269, FID=47.60, FVD=50.51. Tables 2-3 report the same method as PSNR=19.22, SSIM=0.565, LPIPS=0.294, FID=60.11, FVD=52.56. SSIM differs by ~9.5% and FID by ~26%. Neither the tables nor the surrounding text specify whether the ablations use a different data split, validation set, random seed, or evaluation protocol. This gap is large enough that a reader cannot determine which numbers reflect the actual test-set performance, and the paper must clarify this.

- **Camera autoencoder — a key technical contribution — has no ablation isolating its effect.** Section 3.2.2 introduces the camera autoencoder as a core module, but there is no experiment that removes it, replaces it with simpler alternatives (e.g., sinusoidal camera pose embeddings), or evaluates the contribution of the geometric constraints in Eq. 5 versus a standard L2 reconstruction loss. Without this, the individual contribution of one of the paper's three main technical components is unmeasured.

### Minor

- **"Outperforms" framing overstates the quantitative evidence.** The abstract says "overall comparable" while the introduction claims "out-performs current state-of-the-art methods" (line 88). The results are mixed: on ACID, SEVA achieves FID 33.16 vs ARSS 47.76 (a 44% gap) and higher SSIM (0.664 vs 0.623), while ARSS wins on PSNR (21.93 vs 21.77) and LPIPS (0.265 vs 0.326). The paper's own text (Section 4.2) acknowledges "minor geometric inconsistencies" but the 44% FID gap is not minor. The framing should be calibrated to match what the evidence supports.

- **The tokenizer ablation (Table 3) confounds two changes simultaneously:** image→video tokenizer AND VQ→FSQ quantization. The improvement over the VQ baseline could be partly attributable to FSQ over VQ rather than temporal modeling. A controlled comparison using an FSQ-based image tokenizer would isolate the temporal modeling benefit.

- **No confidence intervals or standard deviations reported for any result.** For close comparisons (e.g., PSNR 19.02 vs 18.73 for SEVA), the reader cannot judge whether differences are statistically meaningful.

### Trivial

- **Eq. 7 is incomplete.** The cross-entropy loss is shown with only one argument (the prediction output) without the ground-truth target sequence, unlike the correct two-argument formulation in Eq. 3. This appears to be a formatting error rather than a conceptual mistake, but it should be fixed.

- **Camera autoencoder architecture is described in vague terms** ("stacked 3D convolutional and downsampling blocks," Section 3.2.2) with no layer counts, channel dimensions, or training details provided.

- **The paper states the method is "trained from scratch"** (Section 5), but the VidTok video tokenizer was pre-trained on large-scale video data. Only the transformer backbone is trained from scratch.

## Nice-to-Haves

- **Incremental extension experiment.** The paper's motivation emphasizes that AR models can "incrementally extend and reuse existing generations when the trajectory changes." An experiment generating N views, then extending to N+M without regenerating the full sequence, would directly demonstrate this claimed advantage over joint-diffusion approaches.

- **Quantify parallel decoding speed/throughput.** Section 3.2.3 mentions parallel decoding as an advantage of the random permutation strategy, but no wall-clock times or throughput comparisons are provided.

## Removed Points

These points from the input review are removed with justification:
- **"Central claimed advantage of AR over diffusion is never tested"** — removed from Major tier. The paper's primary contribution is the ARSS framework itself; the causal/incremental advantage is a motivation, not a claimed experimental result. Testing incremental extension would strengthen the paper but is not required to validate what is claimed. Demoted to Nice-to-Have above.
- **Criticism about DL3DV comparison (missing SEVA/ViewCrafter/RayZer results)** — removed. The paper explicitly explains that DL3DV was part of those methods' training data, making the comparison invalid as a zero-shot test. This is a valid and clearly stated methodological choice.
- **Criticism about resolution gap and missing compute comparisons** — removed as scope extensions. The paper acknowledges the resolution limitation in the Discussion; compute details (8 H100 GPUs, 100K iterations) are provided.
- **"Missing related works"** — removed per policy (cannot verify without external sources).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Clarify the numerical gap between main results and ablations.** State explicitly whether Tables 2-3 use a validation split, different seed, or different evaluation protocol, and report both validation and test numbers for all conditions.
2. **Add an ablation of the camera autoencoder** — at minimum, a baseline with simple camera pose embeddings (e.g., sinusoidal encodings of the camera extrinsics) or a variant that removes the geometric constraints from Eq. 5.
3. **Calibrate the claims in the introduction** to match the mixed quantitative results (competitive on some metrics, worse on others).
4. **Add an FSQ-image-tokenizer baseline** to Table 3 to separate the temporal modeling benefit from the quantization method change.

## Score and Decision

The paper identifies a genuinely underexplored direction and builds a reasonable method around it. The camera token design is well-motivated, the hybrid permutation strategy is sensible, and the error accumulation analysis provides useful evidence. However, the unexplained numerical inconsistency between the main results and ablation results, combined with the missing ablation of the camera autoencoder (a key claimed contribution), limit confidence in the experimental evidence. The paper has real contributions that would interest the community, but these issues need resolution before publication.

**Score: 5.5**

**Decision: Borderline (between Reject and Accept)** — the contribution is real but the experimental presentation has gaps that must be addressed. I encourage resubmission with the numerical inconsistency clarified, the camera autoencoder ablation added, and the claims calibrated to match the evidence.

**Calibration Summary:**
All anchors retrieved across rounds:

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| AR-1-to-3 | pOcGFvfgjS.md | 5.0 | R1 | Yes | Below ARSS: fewer datasets, weaker contribution frame |
| CCM-DiT | 15lk4nBXYb.md | 3.0 | R1 | No | Below ARSS: different paradigm (DiT-based), lower score |
| ControlAR | BWuBDdXVnH.md | 6.25 | R1 | Yes | Above ARSS: cleaner ablations, stronger experimental rigor |
| LVSM | QQBPWtvtcn.md | 7.67 | R1 | Yes | Above ARSS: stronger NVS results, more thorough evaluation |
| CameraCtrl | Z4evOUYrk7.md | 6.50 | R1 | Yes | Above ARSS: thorough ablations, clear contribution |
| CamTrol | KI1zldOFz9.md | 5.80 | R2 | Yes | Comparable: accepted despite weaknesses, similar quality level |
| GST/NuHYh4YKNe | NuHYh4YKNe.md | 6.25 | R2 | Yes | Above ARSS: had comprehensive ablations despite controversy |
| AnyView | GuQeZWbaGr.md | 5.50 | R2 | Yes | Similar: rejected, had limited novelty concerns |

**Round 1 bracket**: [5.0, 6.0]. Above AR-1-to-3 (5.0) due to stronger evaluation and clearer contribution, but below ControlAR/CameraCtrl (6.25-6.50) due to missing ablations and numerical discrepancy. **Final score: 5.5**, grounded in the comparison between this paper's weaknesses (numerical inconsistency at -9.98 impact, missing AE ablation at -9.99) vs. CamTrol's accepted 5.80 (which had comparable-magnitude weaknesses but was judged acceptable at that score band). The paper's first-of-its-kind contribution (+8.21) is a genuine strength that pushes it above AR-1-to-3's 5.0, but the experimental gaps prevent it from reaching the 6+ band of more rigorous papers.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>