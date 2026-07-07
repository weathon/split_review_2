## Summary

This paper presents PRISM, a conditional diffusion framework for restoring scientific images affected by compound (mixed) degradations. PRISM combines compound-aware supervision (training on overlapping degradations) with a weighted contrastive disentanglement objective that structures the latent space compositionally, enabling both high-fidelity joint restoration and selective, prompt-guided removal of specific distortions. Evaluated across microscopy, wildlife monitoring, remote sensing, and urban imaging, PRISM outperforms prior methods on synthetic compound benchmarks and zero-shot real-world datasets, with a downstream scientific utility evaluation showing that selective restoration often beats full restoration for task-specific accuracy.

## Strengths

- **Well-motivated problem with a clear thesis.** The paper identifies a genuine gap: scientific imaging restoration must handle *compound* degradations and offer *selective* control, because blanket restoration can erase meaningful signals (lines 26–28, 279). The three principles — simultaneous over sequential correction, precision over aesthetics, control over automation — are grounded in specific examples (denoising erasing faint galaxies, super-resolution hallucinating subcellular structures), giving the framing more substance than typical "all-in-one" restoration papers.

- **Downstream scientific utility evaluation is a genuine contribution.** Table 3, Table 4, and Fig. 6 go beyond standard pixel metrics. The finding that super-resolution and denoising have opposing effects on segmentation vs. fluorescence measurement (lines 255–265) concretely demonstrates that restoration decisions are task-dependent. Using off-the-shelf downstream models (SpeciesNet, MicroSAM) avoids overfitting the evaluation to the restoration method, and the three-seed variance reporting in Table 3 sets a good standard.

- **Controlled ablation cleanly isolates the benefit of compound training.** Comparing Compound-Aware PRISM vs. Primitive-Aware PRISM within the same architecture (Figs. 3–4) provides clean evidence that training on mixed degradations is the key driver of performance, separate from other architectural choices. This is more informative than the cross-model comparisons in Table 1 for understanding what drives performance.

- **The contrastive loss weighting (Eq. 1) is correctly designed.** The Jaccard-based weight \(w_{jk} = \exp(1 - |\cap|/|\cup|)\) ranges from ~1.0 (identical distortion sets) to ~2.718 (disjoint sets), multiplying negative-pair similarity terms so that disjoint distortions receive stronger repulsion while similar distortions are repelled less. This produces the intended compositional geometry (lines 94–100).

## Weaknesses

### Fatal
None.

### Major

1. **Asymmetric training comparison in Table 1.** The paper states "all baselines are trained on the fixed set of primitive distortions" (line 120), while PRISM is trained on compound/mixed degradations drawn from the same pipeline used to construct the MDB test set (which contains overlapping degradations). This systematically advantages PRISM: the baselines are evaluated on a distribution they were never exposed to. OneRestore is the one baseline also trained on composites and is called out separately (line 175), but the rest of the table compares methods with a built-in disadvantage. The zero-shot results (Table 2) and internal ablations (Figs. 3–4) partly mitigate this, but the paper should acknowledge the asymmetry and ideally retrain the strongest diffusion baselines (AutoDIR, MPerceiver) on compound data.

2. **No variance estimates on main quantitative results.** Tables 1 and 2 report only point estimates — no standard deviations, confidence intervals, or significance tests. The margins between PRISM and the second-best method are sometimes small enough that variance could matter (e.g., MDB LPIPS: 0.218 vs. 0.235 — a 0.017 difference). Table 3 *does* report mean ± std, making the omission in the main tables conspicuous.

3. **Selective restoration protocol is underspecified.** Table 3 shows that selective restoration outperforms full restoration in three of four domains, but the paper does not specify how the "selective" subset was chosen. If the authors manually explored configurations and selected the best per domain, this risks overfitting the hypothesis. The p-values (0.032, 0.018, 0.041) are used as evidence, but without correction for multiple comparisons (4 domains) the weakest result (p=0.041 for urban scenes) would not survive Bonferroni correction. The remote sensing result (p=0.11) is correctly called non-significant, but the overall claim ("controllability significantly improves downstream performance in three of four domains") rests on marginal evidence.

4. **Factually inaccurate claim about FID.** The paper states "PRISM achieves the best results across both fidelity (PSNR/SSIM) and perceptual metrics (FID/LPIPS)" (line 177). However, Table 1 shows MPerceiver achieves FID=48.18 (bold=best) while PRISM achieves 48.97 (underlined=second best). This statement is incorrect and should be corrected.

### Minor

5. **The automated prompting mode is described but never evaluated.** Lines 129–130 describe an MLP that predicts distortion sets from the image embedding for automated restoration, but the evaluation uses only manual restoration with predefined prompts (line 135). A comparison of automated vs. expert-guided restoration would strengthen the claim that the model can operate without human input.

6. **Marginal statistical evidence for the controllability claim.** Even setting aside the protocol underspecification, the p-values in Table 3 are 0.032, 0.018, and 0.041. Under a Bonferroni correction for four domains, the threshold would be 0.0125, which only the microscopy result (p=0.018) would approach. The paper's claim that controllability "significantly improves downstream performance in three of four domains" overstates what the data supports.

### Trivial
None.

## Nice-to-Haves

- Retrain the strongest diffusion baselines (AutoDIR, MPerceiver) on the same compound degradation data that PRISM uses, then recompute Table 1. This would cleanly separate the effect of compound training from architectural differences.
- Add error bars to Tables 1 and 2 by running each experiment with multiple seeds or bootstrapping.
- Specify the selective restoration protocol as a reproducible procedure: e.g., validate optimal distortion subsets on a held-out validation split before testing on the evaluation split.
- Evaluate the automated prompting mode or clearly state why it was not assessed.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"MDB is a self-constructed test set"** — Removed because the paper clearly states MDB is a held-out subset of their own data (line 137), which is standard practice. Constructing a benchmark is recognized as a contribution, not a weakness.
- **"Missing details about L_qual classifier and SCPM"** — Removed per rule about missing appendix content; these details likely reside in the appendix (the parser strips appendices).
- **"Baselines like AirNet and Restormer have no text conditioning — how were outputs generated?"** — Removed because this is a specification question about the evaluation protocol that is likely addressed in the full submission's appendix.
- **"The three principles (Section 1) are presented as a contribution when they largely follow from the problem statement"** — Removed as a subjective framing criticism, not a substantive weakness.
- **"Missing domain shift discussion between synthetic and real distortions"** — Removed because the paper explicitly acknowledges this at line 269: "Our training still depends on synthetic augmentations that cannot fully capture real distortions."

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Correct the overclaimed FID statement on line 177 to accurately report that PRISM is second-best on FID (behind MPerceiver) while leading on other metrics.
2. Retrain AutoDIR and MPerceiver on compound degradation data to enable a fair Table 1 comparison that separates training distribution from architectural benefit.
3. Add standard deviations or confidence intervals to Tables 1 and 2.
4. Specify the selective restoration protocol as a reproducible decision rule, and apply multiple-testing correction to the p-values (or report them without "significant" claims for the borderline ones).
5. Evaluate the automated prompting mode (Section 3.3) or remove it from the method description.

## Score and Decision

**Bracket determination (Round 1):** After comparing the weighted items of my draft against the calibrated anchors, the strongest negatives in my draft (-0.58 to -3.13) are substantially milder than the strongest negatives in comparable anchors: DCPT (avg 6.25) has negatives reaching -7.20 and -5.29; HAIR (avg 4.67) has negatives at -4.37; InstantIR (avg 5.25) has negatives at -9.47 and -8.80; DA-CLIP (avg 5.25) has a -10.75 negative. Meanwhile, my draft's positive weights (+3.49 to +4.55) are competitive with these anchors' positive weights. The initial bracket is 5.5–7.0.

**Narrowing (Round 2):** Against the most comparable anchor — DCPT (avg 6.25), a universal restoration pre-training paper that also received generally positive reviews but with some motivation/design clarity concerns — my paper's strengths are comparable while its weaknesses are less severe. Against HAIR (avg 4.67), which was criticized for poor composite degradation results, my paper's downstream evaluation and compound training are clearly stronger contributions. The paper sits cleanly between these two: above 4.67 due to stronger evidence and contributions, at or slightly below 6.25 due to the Table 1 asymmetry, missing error bars, and overclaimed FID — each addressable but collectively preventing the 6.5+ range.

**Final score:** 6.0, reflecting a solid paper with real contributions that is held back by fixable evaluation weaknesses.

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| t3vnnLeajU.md (DA-CLIP) | 5.25 | R1 | Yes | Simpler task setting, stronger negatives (-10.75); PRISM has stronger contributions but similar weakness severity |
| ONWLxkNkGN.md (InstantIR) | 5.25 | R1 | Yes | More novel pipeline but weaker quantitative results; PRISM has better empirical evidence |
| M5t0WvjfCg.md (AdaIR) | 6.00 | R1 | Yes | Strong frequency-domain motivation but some missing comparisons; PRISM comparable in quality |
| PacBhLzeGO.md (DCPT) | 6.25 | R2 | Yes | Cleaner experimental design but weaker downstream evaluation; PRISM slightly below due to Table 1 issues |
| ob9vuDv4yl.md (HAIR) | 4.67 | R2 | Yes | Novel hypernetwork approach but poor composite results; PRISM clearly stronger |
| Ec2rYpP42y.md (UFODM) | 3.75 | R1 | No | Significantly weaker empirical support; not directly comparable |

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>