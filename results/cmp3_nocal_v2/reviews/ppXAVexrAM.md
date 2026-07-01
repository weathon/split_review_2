Now I'll write the final consolidated review.

## Summary

ARSS proposes the first GPT-style decoder-only autoregressive transformer for novel view synthesis (NVS) from a single image, conditioned on a camera trajectory. It uses a video tokenizer (VidTok) for temporally consistent discrete tokenization, a camera autoencoder that maps Plücker raymaps into token-aligned 3D positional features, and a spatial-permutation strategy (random shuffle within frames, temporal order preserved) to adapt the causal transformer to bi-directional visual data. Experiments on RealEstate10K, ACID, and zero-shot on DL3DV show competitive performance against diffusion-based and feed-forward baselines.

## Strengths

- **First AR model for NVS with explicit camera control.** The paper is genuinely the first to apply a decoder-only causal autoregressive transformer to novel view synthesis with camera conditioning (lines 49–50, 86, 281). This is a meaningful and underexplored direction, well-motivated by the sequential nature of long camera trajectories.

- **Principled camera conditioning design.** The camera autoencoder (Section 3.2.2) that compresses Plücker raymaps into token-aligned latent features with geometric regularizers (Eq. 5: unit-norm ray directions, orthogonality of direction and momentum) is a clean solution to injecting 3D positional information into a next-token-prediction framework without breaking causality.

- **Spatial-permutation adaptation validated by ablation.** The hybrid strategy of random spatial permutation with preserved temporal order (Section 3.2.3) is a sensible extension of prior image-level work to the multi-view setting. The ablation in Table 2 confirms it outperforms both raster order and full (spatial+temporal) permutation.

- **Informative error-accumulation analysis.** Figure 6 reports per-frame metrics across the 17-frame sequence, showing that ARSS degrades more gracefully than baselines. This is a concrete advantage that connects directly to the causal/sequential motivation of AR models.

## Weaknesses

### Fatal
None.

### Major

- **Overstated "outperforms" claims relative to the evidence.** The Introduction (line 88: "our method out-performs current state-of-the-art methods") and Discussion (line 281: "outperforms state-of-the-art methods leveraging diffusion models and transformers") make unqualified claims that are not fully supported by Table 1. Against SEVA (the strongest diffusion baseline), ARSS wins 3/5 metrics on RealEstate10K and 2/5 on ACID, with notable deficits: SSIM lags by ≈6–7% relative (0.624 vs 0.670 on Re10K; 0.623 vs 0.664 on ACID), and FID on ACID is substantially worse (47.76 vs 33.16, a 44% gap). The abstract's phrasing ("comparable to," line 9) and the quantitative section (line 231, which acknowledges the SEVA comparison honestly) are more accurate. The paper's real contribution — showing that AR models can achieve competitive NVS with better long-horizon behavior — is meaningful and does not require unqualified "outperforms" claims. The framing mismatch between the strong headline claims and the mixed evidence needs correction.

- **Unexplained inconsistency between main results and ablation numbers, with unspecified evaluation split.** Table 1 reports "Ours" on RealEstate10K as PSNR 19.02, SSIM 0.624, LPIPS 0.269, FID 47.60, FVD 50.51. Tables 2–3 report "ours" as PSNR 19.22, SSIM 0.565, LPIPS 0.294, FID 60.11, FVD 52.56. These differ substantially — SSIM by 9.5% relative and FID by 26%. Neither table caption nor the surrounding text (lines 249–277) specifies the evaluation dataset or split used in the ablations. Without this information, readers cannot assess whether the ablations are comparable to the main evaluation, and the magnitude of the discrepancies raises questions about whether the reported ablation improvements are robust. The authors must specify the evaluation split and explain the source of these differences.

### Minor

- **Zero-shot evaluation on DL3DV excludes SEVA without supporting evidence.** The Table 1 caption states that SEVA, ViewCrafter, and RayZer are excluded because "DL3DV was part of its training data," but no citation or evidence is provided to support this claim. Since SEVA is the closest competitor in the in-domain evaluation, its absence limits the informativeness of the zero-shot comparison. The authors should either include SEVA with appropriate discussion of data leakage, or provide evidence for the training-data overlap claim.

- **No evaluation of the camera autoencoder in isolation.** The camera autoencoder is a key design component (Section 3.2.2), but the paper reports no reconstruction accuracy metrics for Plücker maps, no ablation on the λ weights in Eq. 5, and no analysis of how encoding errors propagate to view synthesis. This makes it difficult to assess the quality of the 3D positional conditioning.

- **No tokenizer reconstruction quality reported.** The paper uses a VidTok video tokenizer but never reports reconstruction metrics (e.g., rFVD, encode-decode PSNR) that would bound the best possible generation quality. The large FVD improvement over VQ in Table 3 (137.68 → 52.56) is expected since VQ processes frames independently; tokenizer reconstruction benchmarks would make this comparison more informative.

- **Parallel decoding claimed but not demonstrated.** Lines 177–178 state the system "has the capacity to predict multiple tokens at one time," but no experiments measure parallel decoding speedup or quality tradeoffs. This is an unsubstantiated claim.

- **Minor typographical issues.** The text describing Eq. (5) (line 153) says "d is the momentum term" where it should read "m is the momentum term." The Figure 6 caption (line 235) refers to a baseline "L2SM" which does not appear elsewhere in the paper and is likely a typo for "LVSM."

### Trivial
None.

## Nice-to-Haves

- **Error bars / variance measures.** All metrics are point estimates. While single-run evaluation on standard benchmarks is the norm in this area, variance information would strengthen confidence in the rankings (especially where margins are small, e.g., PSNR 19.02 vs 18.73 on Re10K).
- **Runtime or inference speed comparison.** Given the paper's emphasis on the AR paradigm's potential for incremental generation, reporting per-frame generation time vs. diffusion baselines would be informative.
- **Analysis of what drives the SSIM/FID gap vs. SEVA.** Understanding whether this stems from the tokenizer bottleneck, the 256×256 resolution, or the random-permutation training would sharpen the contribution and identify the most impactful future directions.
- **Make the error-accumulation analysis (Figure 6) the centerpiece of the contribution.** This is the paper's most differentiated evidence and directly supports the causal/sequential motivation.

## Removed Points

The following points from the input review were filtered per the consolidation rules:

- **Criticism about Eq. (7) being malformed:** This is a PDF-parsing artifact, not an author error.
- **"No error bars" framed as a major methodological gap:** Demoted to Nice-to-Have because single-run evaluation on public benchmarks is standard practice in this area.
- **"No runtime comparison" framed as a weakness:** Demoted to Nice-to-Have as it exceeds the paper's stated scope.
- **Strength about error accumulation analysis being "superior to competing methods":** The data does show slower degradation, so the specific framing is fine; the overclaim correction is handled in the Major weakness section.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the need for better calibration between claims and evidence and flag transparency gaps in the ablation setup, but do not identify a new technical insight missing from the paper.

## Suggestions

1. **Recalibrate the headline claims.** Change "outperforms" in the Introduction and Discussion to language reflecting the mixed results against SEVA (e.g., "competitive with state-of-the-art diffusion-based methods and superior on LPIPS and long-horizon error accumulation"). The abstract's tone is appropriate and should be the standard.

2. **Specify the evaluation split for all ablation tables.** State whether Tables 2–3 use the same test split as Table 1, and explain the source of the numerical differences (different seed, model checkpoint, or data subset?).

3. **Either include SEVA in the DL3DV evaluation or provide evidence for its exclusion.** If data leakage is the concern, cite the specific training sets from the SEVA/ViewCrafter/RayZer papers.

4. **Add camera autoencoder reconstruction metrics** (e.g., Plücker-map PSNR and orthogonality error) **and tokenizer reconstruction metrics** (e.g., rFVD).

5. **Either demonstrate parallel decoding experimentally or remove the claim.**

6. **Fix the notation typo in Eq. (5) text and the L2SM/LVSM typo in Figure 6.**

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>