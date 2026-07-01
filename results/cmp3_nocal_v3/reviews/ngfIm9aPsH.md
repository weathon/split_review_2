## Summary

The paper proposes OF-Diff, a layout-to-image diffusion model for remote sensing that uses an Enhanced Shape Generation Module (ESGM) to extract object masks, a dual-decoder architecture with online-distillation to avoid needing real images at inference, and DDPO fine-tuning for diversity. Experiments on DIOR, DOTA, and HRSC2016 with 13 metrics across 4 evaluation dimensions show consistent improvements over baselines.

## Strengths

1. **Specific, well-motivated problem framing.** Section 1 and Figure 1 concretely identify three failure modes in prior RS L2I methods (control leakage, structural distortion, dense generation collapse), and the method design directly targets these. This is more precise than generic "prior work is limited" framing.

2. **Conceptually clean online-distillation design.** The idea of using a mix-feature decoder (with real image access during training) as a stop-gradient teacher for the shape-feature decoder (which operates without real images at inference) is well-reasoned. Eq. 3's linear annealing of the mixing ratio and the consistency loss in Eq. 6 with proper stop-gradient are sensible design choices that directly support the method's "no real image at inference" goal.

3. **Extremely thorough evaluation.** Using 13 metrics across 4 evaluation dimensions (generation fidelity, layout consistency, shape fidelity, downstream utility) is unusually comprehensive. The shape-fidelity evaluation (IoU, Dice, CD, HD, SSIM on edge maps in Table 2) directly targets the paper's central thesis of improved morphological fidelity.

## Weaknesses

### Major

1. **Table 4 contains a duplicated row with contradictory numbers — a data integrity concern.** Rows 7 and 8 both show configuration (✓ ESGM, ✓ L_c, ✓ DDPO) but report drastically different results: FID 37.98 vs 24.92, YOLOScore 47.74 vs 58.99. The FID=37.98 value is *worse* than models with fewer components (e.g., L_c-only at 36.25), which is inconsistent if adding ESGM and DDPO helps. The paper discusses captions as a potential confounding factor (lines 211, 239), but the table has no caption column, and the text states ablation experiments were "conducted based on the absence of caption input" — making the duplicate unexplained. This makes the ablation study unreliable as presented. The authors must clarify whether a column is missing or correct the table.

2. **ESGM is described as generating shapes from learned priors, but it actually retrieves masks from a pre-collected pool.** The paper states ESGM "employs learned shape priors to synthesize diverse masks of object shape" (line 116). The actual procedure (lines 120-121) is: during training, masks are extracted from real images via RemoteCLIP+RemoteSAM; at inference, "it selects enhanced shapes from a lightweight mask pool collected during or after training. In our experiments, we use masks generated during training." This is mask retrieval with random-rotation augmentation, not generative synthesis from a learned prior. The method is not invalid — remote sensing objects have quasi-invariant shapes, making retrieval practical — but the framing overstates the novelty of ESGM. This should be explicitly discussed in limitations.

### Minor

3. **DDPO reward function (Eq. 9) uses unclear notation.** The term KNN(x₀, x₀) — KNN of a single sample from itself — is not standard notation for a diversity metric. The paper clarifies (line 130) that KNN is computed in CLIP embedding space, but the notation is ambiguous. Similarly, KL(x₀, x₀') between a single generated sample and a single real sample is not standard KL divergence between distributions. These are fixable presentation issues but they hinder reproducibility from the main text alone.

4. **Table 3 has a bolding inconsistency.** OF-Diff is bolded as best for YOLOScore (49.59), but CC-Diff achieves 51.74 — a higher value (lines 223-224). This misrepresents the result on that metric.

5. **The DDPO contribution is empirically marginal.** From Table 4: ESGM+L_c achieves FID=24.98, YOLOScore=57.83, mAP50=54.31. Adding DDPO (row 8) gives FID=24.92, YOLOScore=58.99, mAP50=54.44 — improvements of 0.06, 1.16, and 0.13 respectively. The paper should acknowledge this rather than presenting DDPO as a contribution of equal weight to ESGM and online-distillation.

6. **ESGM mask pool size is not reported.** The paper mentions "a lightweight mask pool" but does not specify how many unique masks are collected per category. A small pool weakens the diversity claim; a large pool covering the training set effectively amounts to memorization.

7. **The abstract's framing of existing methods is over-broad.** The abstract states "existing methods either rely on additional textual guidance... or require extra real-image references." AeroGen — a layout-conditioned method the paper itself benchmarks against — does neither. The body correctly acknowledges AeroGen, but the abstract's dichotomy is imprecise.

### Trivial

8. **Table 3 bolding error** (as noted above).

9. **No statistical significance or confidence intervals.** Given that some advantages over baselines are small (e.g., mAP50 on DOTA: 67.89 vs AeroGen's 67.09), the paper would benefit from indicating whether differences are statistically reliable.

10. **Downstream augmentation framing slightly overstates the advantage.** The reported "mAP improved by 2.2%" is against a no-augmentation baseline, not against other generative methods. Table 1 shows OF-Diff's mAP50 margin over CC-Diff on DIOR is less than 1 pp. The per-class gains (8.3% for airplanes) are more meaningful and should be foregrounded.

## Nice-to-Haves

- An experiment where CC-Diff is given degraded or out-of-distribution reference patches and OF-Diff still succeeds would directly demonstrate the practical advantage of the "no real image at inference" claim, which is currently asserted but not empirically stress-tested.
- A brief justification in the main text for the per-timestep importance-weight formulation in Eq. 8, which differs from the standard trajectory-level ratio in DDPO, would improve self-containedness.
- A discussion of whether ESGM's diversity is fundamentally bounded by the size of the pre-collected mask pool would clarify the scope of the contribution.

## Removed Points

- The reviewer's critique of the DDPO gradient as "could introduce high variance" is removed: the paper references Appendix A.2 for the full derivation, and per-timestep importance weighting appears in some DDPO formulations. Without the (stripped) appendix, this cannot be verified as a flaw.
- The reviewer's claim that the shape-feature decoder's reliance on image features is "not fully explained" is demoted: the online-distillation mechanism (Eq. 6, line 106) explicitly addresses this — the teacher signal trains the shape-feature decoder to match the mix-feature decoder's outputs without needing c_i at inference.
- The reviewer's claim that downstream augmentation advantages are "marginal" is demoted to Trivial: the per-class gains are substantial (8.3% for airplanes), and the small overall mAP gap vs other generative methods is a secondary point.

## Novel Insights

None beyond the paper's own contributions. The core idea (online-distillation to decouple training from inference in RS L2I) is not fundamentally challenged by any of the identified issues.

## Suggestions

- Correct Table 4: either add a column distinguishing the caption/no-caption variant so rows 7 and 8 are clearly different configurations, or remove the duplicate and explain the discrepancy.
- Revise the ESGM framing to accurately describe the mask retrieval + augmentation procedure rather than claiming "learned shape priors synthesize diverse masks."
- Fix the DDPO reward notation (Eq. 9) to clearly specify the batch-level KNN diversity computation and the distributional KL term.
- Correct the bolded entry in Table 3 for YOLOScore.
- Add a brief limitations paragraph acknowledging that ESGM retrieves from a pre-collected pool rather than generating truly novel shapes, and note the pool size.
- Report confidence intervals or standard deviations for key metrics where margins are small.
- Soften the DDPO contribution claim given its marginal empirical impact in the ablation.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>