Now I have a clear calibration picture. Let me compile the final review.

**Anchor summary for comparison:**

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| LVSM | QQBPWtvtcn.md | 7.67 | Bracket | Yes | Much stronger results (outperforms baselines by 1.5-3.5dB), cleaner evaluation, accepted |
| CCM-DiT | 15lk4nBXYb.md | 3.00 | Bracket | Yes | Camera-pose video generation, weak experiments, rejected |
| ControlAR | BWuBDdXVnH.md | 6.25 | Bracket | Yes | Strong ablations, clean controlled experiments, accepted |
| Where Am I | NuHYh4YKNe.md | 6.25 | Bracket | Yes | Joint pose/view AR, mixed reviews but accepted |
| AR-1-to-3 | pOcGFvfgjS.md | 5.00 | Narrow | Yes | **Most relevant:** AR NVS from single image. Similar evaluation gaps (unfair comparison, missing ablations, unvalidated consistency claim). All reviewers at 5. Rejected. |
| ControlVAR | v46TPwU0Uy.md | 4.33 | Narrow | Yes | AR controllable generation, evaluation concerns, rejected |
| Ctrl123 | CFOQd4tqn1.md | 4.00 | Narrow | Yes | NVS with consistency focus, presentation issues, rejected |

**Round 1 bracket:** 4.0–6.0. The paper is clearly above CCM-DiT (3.00) and Ctrl123 (4.00) due to genuine novelty and more thorough evaluation. It is below LVSM (7.67) and ControlAR (6.25) due to evaluation gaps.

**Round 2 narrowing:** The closest anchor is AR-1-to-3 (5.00), which shares the same core approach (AR for NVS) and similar evaluation weaknesses (missing ablations, unvalidated claimed advantages). ARSS has advantages over AR-1-to-3 (scene-level instead of object-level, multiple datasets, camera control) but also has the internal numerical inconsistency (Table 1 vs Table 2) which AR-1-to-3 does not. On balance, ARSS sits at approximately 5.0, consistent with the AR-1-to-3 anchor.

**Favorability comparison:** My draft's most negative weakness items (camera autoencoder not ablated at -0.88, central motivation not validated at -1.41) are comparable in negativity to AR-1-to-3's weakness about the unvalidated consistency claim (favorability=0.71) and unfair comparison (1.00). ARSS's strongest strength items (13.87 for permutation strategy, 11.80 for clarity) are comparable to AR-1-to-3's strongest (11.88 for performance). The similar pattern of strong method with evaluation gaps places the paper at ~5.0.

**Final score: 5.0, Decision: Reject**

Now let me write the final review.

I need to follow the output structure. Let me compose this carefully.

For the strengths, I want to merge the generic ones and keep concrete ones. The favorability ratings tell me:
- "First application of decoder-only AR to NVS" (9.14) - good
- "Well-motivated gap identification" (11.22) - good  
- "Clean modular design" (8.23) and sub-points - good
- "Hybrid token permutation strategy" (13.87) - excellent, keep
- "Zero-shot generalization" (11.02) - good
- "Writing clarity" (11.80) - good but somewhat generic

Let me merge the strengths properly.

For weaknesses:
Major:
1. SEVA omitted from error accumulation (favorability=0.13)
2. Ablation inconsistency (favorability=0.52) 
3. Camera autoencoder not ablated (favorability=-0.88)

Minor:
4. Overclaiming (favorability=2.15)
5. Central AR advantage not validated (favorability=-1.41)

Trivial:
6. L2SM typo and notation (favorability=2.74)## Summary

This paper introduces ARSS, the first framework that applies a decoder-only autoregressive (GPT-style) transformer to camera-controlled novel view synthesis (NVS) from a single image. It addresses three challenges through a modular design: a video tokenizer for temporally consistent discretization, a camera autoencoder that encodes Plücker raymaps into 3D positional guidance tokens, and a hybrid permutation strategy that randomly shuffles spatial tokens within each frame while preserving temporal order across frames. Experiments on RealEstate10K, ACID, and DL3DV show competitive results against diffusion-based NVS methods.

## Strengths

- **First application of decoder-only autoregressive models to camera-controlled NVS.** The paper correctly identifies a gap: most NVS methods use diffusion models that generate all views jointly, making causal/incremental generation unnatural. Using next-token prediction for NVS is genuinely novel and well-motivated (Section 1, lines 13-15).

- **Clean modular design addressing three concrete challenges.** Temporal inconsistency → video tokenizer, camera control in an AR framework → camera autoencoder with Plücker raymaps, mismatch between uni-directional causal attention and bi-directional spatial context → hybrid token permutation. Each module follows from a stated problem, giving the method strong internal coherence (Section 3).

- **The hybrid token permutation strategy (spatial shuffle within frames, temporal order across frames, Eq. 6) is a sensible and effective adaptation** of prior shuffled-AR image generation to the multi-view setting. The ablation (Table 2, Figure 7) convincingly shows this outperforms both full permutation and raster-order baselines.

- **Competitive zero-shot generalization.** The method is evaluated on DL3DV (zero-shot, Table 1) and AI-generated images (Figure 5), demonstrating generalization beyond its training distribution—an important practical capability.

## Weaknesses

### Fatal
None.

### Major
- **SEVA is omitted from the error accumulation analysis (Figure 6).** The per-frame PSNR/SSIM/LPIPS comparison includes LVSM, MotionCtrl, RayZer, and ViewCrafter but not SEVA — the only baseline that is roughly competitive with ARSS in aggregate metrics (Table 1). The paper claims ARSS "accumulates significantly less error over time" (Section 4.2), but without SEVA in this plot the claim is unsubstantiated against the most relevant comparator. This directly undermines the paper's strongest argument for the AR approach.

- **Ablation results (Table 2) are inconsistent with main results (Table 1).** Table 2 reports "ours" as PSNR 19.22, SSIM 0.565, LPIPS 0.294, FID 60.11. Table 1 reports the same method on Re10K as PSNR 19.02, SSIM 0.624, LPIPS 0.269, FID 47.60. The SSIM differs by 9.4% relative and FID by 26% relative. These discrepancies exceed normal statistical fluctuation and suggest different evaluation protocols or test subsets. The paper provides no explanation, making it difficult to interpret the ablation improvements against the main results.

- **The camera autoencoder—presented as a core contribution (Section 3.2.2)—is never ablated.** There is no controlled experiment that removes or replaces the camera tokens (e.g., with simpler view-index embeddings or no camera conditioning) to measure their actual contribution. The paper claims camera tokens "provide accurate 3D position" but provides no quantitative evidence for their necessity.

### Minor
- **Stated claims are inconsistent across sections.** The abstract accurately says results are "overall comparable" to SOTA, but the introduction (line 88) and conclusion (line 281) assert the method "outperforms" SOTA. Against the strongest competitor SEVA, results are genuinely mixed: ARSS wins on PSNR (+1.5% on Re10K) and LPIPS (-23% on Re10K) but loses on SSIM (-6.9% on Re10K) and FID (-44% on ACID). The paper acknowledges this trade-off in Section 4.2, but the stronger wording in the intro and conclusion overstates the evidence.

- **The paper's central motivation—that AR enables causal/incremental generation that diffusion cannot easily support (Section 1, lines 13-15)—is never experimentally validated.** There are no experiments demonstrating incremental generation, trajectory editing, or causal reuse. This claimed advantage remains entirely hypothetical and untested.

### Trivial
- Figure 6 caption refers to "L2SM" which is a typo for "LVSM." The camera autoencoder loss (Eq. 5) uses the symbol **d** for both the ray direction and the momentum term, making the loss description ambiguous (the equation itself uses **m** for momentum, suggesting a text typo).

## Nice-to-Haves
- Include SEVA in the error accumulation analysis to directly test the "slower degradation" claim.
- Add an ablation of the camera autoencoder to quantify the contribution of 3D positional guidance.
- Reconcile the Table 1 vs. Table 2 numerical discrepancy by clarifying the evaluation protocol.
- Provide at least one experiment demonstrating the claimed causal/incremental generation advantage (e.g., timing comparison or trajectory editing scenario).
- Report inference cost (time, FLOPs) to give context for the AR approach's practical trade-offs.

## Removed Points
- **Missing baselines (CAT3D, ReconFusion, Zero-1-to-3, etc.):** The paper already compares against 6 baselines (SEVA, LVSM, Genwarp, MotionCtrl, ViewCrafter, RayZer) that cover the main single-view NVS approaches. Many of the mentioned methods operate under different settings (multiple input views, object-centric, different training data). The existing baseline set is adequate for positioning.
- **Low absolute PSNR values:** The paper acknowledges it trains from scratch at 256×256 (line 281-282), and relative comparisons in Table 1 are at consistent resolutions. The absolute numbers criticism conflates different evaluation protocols.
- **World model framing dropped:** The paper primarily focuses on NVS, which is a substantive contribution. The world model framing is motivation, not a core claim requiring validation.
- **Parallel decoding unspecified:** A useful implementation detail to clarify but does not affect the paper's core evaluation.
- **Notation ambiguity:** Partially a parser artifact; the equation (Eq. 5) uses **m** in the formulation, so the text likely has a minor typo.

## Novel Insights
The meta-review reveals a pattern: the paper's modular design is well-motivated and the AR approach to NVS is genuinely novel, but the evaluation systematically undermines its own claims. The three major weaknesses are each gatekept by a missing comparison or analysis that the paper should trivially include: (1) SEVA is the strongest competitor yet omitted from the very analysis (error accumulation) that is supposed to showcase the method's defining advantage; (2) the ablation table's numerical discrepancy with the main table prevents confident interpretation of the method's components; (3) a core claimed module (camera autoencoder) has no ablation at all. These gaps are individually fixable but collectively erode trust in the experimental methodology.

## Suggestions
1. Include SEVA in the per-frame error accumulation analysis.
2. Reconcile Table 1 vs. Table 2 numbers by clarifying the evaluation protocol or re-running one set consistently.
3. Add an ablation study where camera tokens are replaced with a simpler alternative (e.g., learnable view index embeddings) to measure the autoencoder's contribution.
4. Soften the "outperforms" language in the introduction and conclusion to match the mixed results against SEVA.
5. Add a timing/throughput comparison or a simple demonstration of incremental generation to validate the AR advantage argument.

## Score and Decision

**Score Calibration Summary:** Round 1 (bracketing) identified anchor papers from 3.00 to 7.67. ARSS is clearly above CCM-DiT (3.00, weak camera-control video generation) and Ctrl123 (4.00, presentation issues). It is clearly below LVSM (7.67, much stronger quantitative results with cleaner evaluation) and ControlAR (6.25, strong ablations). Round 2 (narrowing) centered on AR-1-to-3 (5.00), the most directly comparable paper (AR for NVS from single image) with all four reviewers at 5.0 and similar evaluation gaps (missing ablations, unvalidated consistency claims). ARSS has advantages over AR-1-to-3 (scene-level evaluation, more datasets, camera control) but also has the internal numerical inconsistency between Table 1 and Table 2, which AR-1-to-3 does not. Comparing favorability: ARSS's most negative items (camera autoencoder not ablated at -0.88, central motivation unvalidated at -1.41) are comparable in impact to AR-1-to-3's weakest items (unfair comparison at 1.00, unvalidated consistency claim at 0.71), placing the paper at a similar level.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>