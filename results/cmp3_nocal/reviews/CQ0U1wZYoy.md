## Summary

PRISM presents a conditional diffusion framework for compound degradation restoration in scientific imaging. It combines compound-aware supervision (training on mixtures of up to three distortions) with a weighted contrastive disentanglement objective that uses Jaccard distance to structure the latent space compositionally. The paper makes two main contributions: a principled embedding method for representing compound degradations, and a systematic study showing that selective (rather than full) restoration improves downstream scientific accuracy across microscopy, camera trap, and urban scene benchmarks.

## Strengths

- **Downstream task evaluation is a genuine contribution.** Rather than relying solely on PSNR/SSIM/FID, the paper evaluates how restoration affects classification accuracy, segmentation mIoU, and fluorescence measurements using off-the-shelf pretrained models (SpeciesNet, MicroSAM). Table 3 shows that full restoration can hurt downstream accuracy while selective restoration often does better — a finding that standard benchmark evaluations would not have surfaced.

- **The microscopy task-dependence analysis (Table 4) cleanly demonstrates why controllability matters.** The finding that super-resolution improves segmentation mIoU but increases fluorescence MSE, while denoising does the opposite, is a concrete example of "restoration is task-dependent." This goes beyond claiming controllability by showing that even within a single image, different downstream tasks demand different restoration strategies.

- **The weighted contrastive loss using Jaccard distance (Section 3.2, Eq. 1–2) is a principled design.** Pulling composite embeddings toward the span of their primitives in proportion to set overlap is mathematically natural and avoids ad-hoc tuning. The inclusion of partial prompts and negative prompts in training (Section 3.1) is well-motivated for the controllability use case.

- **Well-motivated problem framing.** The three design principles (simultaneous over sequential, precision over aesthetics, control over automation) connect directly to real scientific requirements and guide the experimental design.

## Weaknesses

### Fatal

None.

### Major

**1. Training distribution mismatch undermines the headline comparison (Table 1).** The paper states (line 120): "For fair comparison, all baselines are trained on the fixed set of primitive distortions." Meanwhile, PRISM is trained on images with up to three simultaneous degradations, including submixtures and partial/negative prompts (Section 3.1). The MDB test set evaluates on images with up to three distortions. This means most baselines are evaluated on compound mixtures they were never trained on, while PRISM is evaluated on a distribution it was explicitly trained on. The 1–3 PSNR gap over the strongest baselines (22.08 vs 20.84 for MPerceiver) is therefore at least partly a training distribution artifact.

The comparison against OneRestore (also trained on composites, 19.36 vs 22.08) is fairer, but the gap is partially attributable to PRISM using a diffusion backbone while OneRestore does not. The paper's own ablation (Fig. 3, Primitive-Aware vs Compound-Aware PRISM, ΔPSNR 10.56 vs 8.14) provides internal validation that compound-aware training helps, but this does not appear alongside the baselines in Table 1. The paper never disentangles "compound-aware supervision" from "diffusion backbone" from "contrastive disentanglement" as sources of improvement. This weakens the headline claim that "PRISM outperforms state-of-the-art baselines on complex compound degradations."

**2. Zero-shot evaluation protocol is underspecified for non-prompt baselines (Table 2).** The paper states (lines 203–204): "For each dataset, we use the compound-aware CLIP encoder to identify the fixed set of distortion types… We then apply the same manual prompts over this standardized set for all models." However, many baselines in Table 2 (AirNet, Restormer_A, NAFNet_A) are not prompt-conditioned models. The paper does not explain how these baselines received prompts or whether they were evaluated without prompts while others received them. Without this specification, the comparison across categories cannot be properly assessed.

### Minor

**3. "Selective Restoration" per domain is underspecified.** The paper gives qualitative examples (camera traps: "restoring only contrast"; urban: "removing haze"; microscopy: "super-resolution alone"; lines 242, 253) but does not systematically specify, for each domain in Table 3, which distortions were selectively removed, whether this was decided a priori or post hoc, and how the selection relates to the reported p-values. This limits reproducibility.

**4. Compositionality claim rests on indirect evidence.** The paper claims (line 222) that the model learns to represent composites as joint embeddings of constituent parts, enabling "interpolation" of restoration strategies. The evidence (Fig. 4 showing similar PSNR between sequential and composite prompting; Fig. 5 showing qualitative stepwise restoration) is consistent with compositionality but does not directly test it — e.g., removing A from an {A+B} image and comparing to B-only ground truth, or showing that sequential removal matches single-step removal at the pixel level.

**5. Small practical effect in camera traps.** The camera traps improvement (Table 3: 0.976 → 0.984, p=0.032) is a 0.008 gain on an already-high baseline (degraded input: 0.921). The paper discusses significance but not effect sizes.

### Trivial

- The claim that "current frameworks perform sequential/iterative removal of single distortions" (line 24) is imprecise for methods like MPerceiver that handle multiple distortions in a single forward pass; the paper's later characterization (line 116) is more accurate.
- The L_qual regularizer (Eq. 2) uses a classifier p̂(c|e_clean) whose training is not described in the main paper.

## Nice-to-Haves

- Compare PRISM's controllability against a modular alternative: a non-controllable SOTA method (e.g., MPerceiver or OneRestore) combined with a separate distortion classifier. This would test whether integrated controllability adds value beyond a modular pipeline.
- Add a direct compositionality test: remove A from {A+B} and compare to B-only ground truth; compare sequential (remove A then B) to single-step removal at the pixel level.
- Run selective restoration experiments with an oracle or domain expert choosing which distortions to remove, rather than post-hoc author selection.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Selective Restoration is a within-model comparison"** — removed because the paper's claim (contribution 3) is about whether controllability matters for scientific accuracy, not whether PRISM's controllability is better than other methods'. The within-PRISM comparison is the correct design for this question. Comparing against other controllable methods would be a nice-to-have but is not required to support the claim made.
- **"The word 'guarantees' is doing too much work"** — removed as a semantic nitpick about language in the related works section. The term is used to describe prior work's limitations, not PRISM's properties.
- **Missing appendix content (L_qual classifier training)** — per meta-review guidelines, appendix sections are stripped by the parser and existed in the original submission. The reviewer's concern about the main paper lacking detail is noted in Trivial.
- **"Sequential/iterative characterization of prior work is inaccurate"** — partially valid but only a minor imprecision (listed in Trivial). The paper later acknowledges MPerceiver's approach accurately.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Retrain key baselines on compound degradations** for a fairer comparison in Table 1, or clearly separate comparisons where training distribution matches from those where it does not.
2. **Fully specify the zero-shot protocol:** state explicitly, for each baseline category in Table 2, whether and how prompts were used during evaluation.
3. **Add a supplementary table** specifying, for each domain in Table 3, exactly which distortion(s) were selectively removed and whether selection was a priori or post hoc.
4. **Consider leading with the controllability study** as the paper's central contribution — it is the most distinctive and best-supported finding.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>