Now I have all the calibration data I need. Let me compile the final review.

**Round 1 bracket analysis**: Paper sits between the 3.5-5.5 band and the 5.5-7.5 band. The most comparable anchors are DA-CLIP (5.25, Accept), InstantIR (5.25, Reject), and HAIR (4.67, Reject). PRISM's unique strengths (downstream evaluation, principled loss design) are strong, but the unfair baseline comparison (-9.93 impact) is a critical experimental confound that prevents full evaluation of the main competitive claim.

**Narrowing**: After comparing itemized impact scores, PRISM is stronger than HAIR (4.67) which had only marginal gains on composites but weaker than the best papers in the 6+ range which had cleaner experiments. PRISM sits closest to DA-CLIP (5.25) and InstantIR (5.25) — papers with genuine contributions that were held back by experimental or novelty concerns. PRISM's downstream evaluation contribution is genuinely novel and impactful, but the baseline confound is a real flaw.

**Final score: 5.0** — between borderline reject and borderline accept. The paper's contributions are real (principled loss design, downstream evaluation framework, zero-shot results) but the central competitive claim (Table 1) is confounded by comparing models trained on different data distributions.

---

## Summary

This paper proposes PRISM, a conditional diffusion framework for compound degradation restoration with controllability. PRISM combines (1) compound-aware supervision (training on mixtures of up to 3 distortions with partial/negative prompts) and (2) a weighted contrastive disentanglement objective using Jaccard distance to organize the latent space compositionally. The paper evaluates across four scientific domains and introduces downstream task evaluation showing that selective restoration can outperform full restoration.

## Strengths

- **Principled loss design.** The weighted contrastive objective (Eq. 1) using Jaccard distance to encode compositional structure is clean and well-motivated: compound degradation embeddings are pulled toward their constituent primitives, while the quality-aware regularizer (L_qual) prevents drift in clean embeddings. [impact=+9.93]

- **Downstream task evaluation is genuinely novel and informative.** Tables 3-4 and Figure 6 go well beyond pixel-level metrics. The finding that full restoration can *harm* downstream performance (microscopy mIoU: 0.475 full vs. 0.580 selective; camera traps: 0.976→0.984) and that restoration goals are task-dependent (super-resolution helps segmentation but hurts fluorescence measurement) is non-obvious and practically important. [impact=+9.98 / +10.00]

- **Zero-shot evaluation on real data (Table 2).** Testing on UIEB, POLED, and ThapaSet with real (not synthetic) compound distortions provides evidence that PRISM transfers beyond its synthetic training pipeline, leading on most metrics across all three datasets. [impact=+9.99]

- **Well-motivated problem.** The paper clearly identifies that scientific imaging involves compound degradations and that indiscriminate restoration can destroy task-relevant signal, with grounded examples from the literature (Lu et al. 2025 on over-denoising in microscopy; Cecilia & Murugan 2022 on oversmoothing in underwater monitoring). [impact=+4.09]

## Weaknesses

### Fatal
None.

### Major

- **Unfair baseline comparison in Table 1 (the paper's headline results).** Line 120 states all baselines are "trained on the fixed set of primitive distortions" while PRISM is trained on compound distortions (mixtures of up to three primitives, plus partial and negative prompts). The MDB test set evaluates on compound distortions. This conflates the advantage of training on the test distribution with the advantage of the method's design. OneRestore is an exception (trained on composite data, line 173-175), but the remaining baselines are not. Figure 3's ablation (PRISM Primitive-Aware vs. Compound-Aware) partially addresses this, but it compares PRISM variants, not retrained baselines. The claim "PRISM outperforms state-of-the-art baselines" is not properly supported by this experiment. [impact=-9.93]

### Minor

- **Zero-shot evaluation uses prompts from PRISM's own encoder (Table 2).** Line 203: "we use the compound-aware CLIP encoder to identify the fixed set of distortion types." While the same manual prompts are used for all methods, PRISM's diffusion backbone was trained on the output of its own encoder. If the classifier misidentifies distortions, all methods get the same prompts — but PRISM may be more robust because it was trained on its encoder's output distribution. [impact=-0.00]

- **The MDB test set is entirely synthetic (held-out subset of the authors' own augmentation pipeline, line 137).** The zero-shot results on real data (Table 2) partially mitigate this, but the confound from the weakness above limits their force. The paper acknowledges this limitation (line 269). [impact=-7.98]

- **Automated restoration pipeline (MLP, line 129) is described but never evaluated.** All experiments use manual prompting (line 135). The MLP's accuracy at predicting distortion sets from image embeddings is not reported. [impact=-5.94]

- **Controllability experiment (Table 3) lacks comparison against alternative controllable methods.** The experiment compares PRISM full vs. PRISM selective restoration, which demonstrates controllability has value as a concept but does not validate that PRISM's specific controls are effective relative to alternatives. The paper's Claim 3 ("controllability is not a convenience but a necessity") is about the problem domain, not method comparison, but the framing could be clearer. [impact=-2.37]

- **CLIP architecture variant not specified.** The paper refers to "CLIP" (lines 80, 112) without stating ViT-B/32, ViT-L/14, or other variant. [impact=-0.03]

### Trivial

- Statistical significance (error bars, p-values) is reported for Table 3 but not for the main MDB comparisons in Table 1. [impact=-0.05]

## Nice-to-Haves

- Retrain the strongest baselines (AutoDIR, MPerceiver, PromptIR) on the same compound degradation data used for PRISM, then re-run the MDB comparison. This single experiment would separate the data-distribution advantage from the method advantage.
- Use multiple prompt sources (e.g., known distortion labels from the UIEB literature) rather than only PRISM's encoder for zero-shot evaluation.
- Report the automated MLP pipeline's accuracy.

## Removed Points

These points are flagged to be removed, treat them with caution:
- **Jaccard weight concern** — The reviewer claimed non-overlapping variants are "upweighted" which is opposite to the goal. The weight w_jk is applied in the denominator (repulsion term), so higher weight for dissimilar sets = more repulsion = correct behavior. Removed as a misreading.
- **Rooftop Cityscapes undescribed** — Paper refers to Appendix C. Removed per parser-instruction rules (appendix content not evaluable).
- **Distortion library not fully specified** — Refers to appendix. Removed per parser-instruction rules.
- **4-distortion PSNR values low / ThapaSet SSIM values low** — Describing data characteristics, not method weaknesses.
- **Generic "important problem" strength** — Removed as insufficiently specific to this paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Retrain baselines on compound data** — This is the single highest-leverage improvement. It would either confirm or undermine the paper's central competitive claim.
2. **Use multiple prompt sources for zero-shot evaluation** — E.g., querying human experts or using known degradation taxonomies for UIEB rather than only PRISM's encoder.
3. **Report automated restoration accuracy** — The MLP pipeline is mentioned but never evaluated; reporting its precision/recall for distortion detection would strengthen the paper.
4. **Specify CLIP variant** — For reproducibility.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| u1cQYxRI1H (IC-Light) | 0.50 | R1 | No | Irrelevant topic (illumination harmonization), much stronger paper |
| 5lUdTogEL3 (L-ReID) | 1.00 | R1 | No | Irrelevant topic |
| Uj0h13lVrR (GFlowNets) | 1.00 | R1 | No | Irrelevant topic |
| 8QTpYC4smR (LLM survey) | 1.00 | R1 | No | Irrelevant topic |
| vK8C37eHXM (Diff compression) | 3.20 | R1 | No | Related (diffusion autoencoder) but different task |
| AjunxrcKa2 (Cond LoRA) | 3.40 | R1 | No | Related (conditional diffusion) but different task |
| dAavOuxZvo (VIPaint) | 3.00 | R1 | No | Related (diffusion inpainting) but different task |
| 2o58Mbqkd2 (SuperDiff) | 3.25 | R1 | No | Not directly comparable |
| Ec2rYpP42y (UFODM) | 3.75 | R1 | Yes | Weaker paper with fundamental formulation issues |
| V2x5ZTHMae (Diff Posterior) | 4.00 | R1 | No | Related but different focus |
| kALZASidYe (Enhanced Control) | 3.75 | R1 | Yes | Related (controllable diffusion) but poorer experiments |
| ONWLxkNkGN (InstantIR) | 5.25 | R1 | Yes | BIR diffusion; weaknesses about novelty/performance; PRISM has stronger conceptual contributions but similar experimental concerns |
| YOKnEkIuoi (Cond Var Diff) | 5.80 | R1 | No | Different problem setting |
| TRWxFUzK9K (Video Inverse) | 6.50 | R1 | No | Stronger paper in a different domain |
| PacBhLzeGO (DCPT) | 6.25 | R1 | Yes | Cleaner experiments, stronger comparative results |
| cCRlEvjrx4 (CoInD) | 6.20 | R1 | Yes | Strong theoretical grounding, but simpler datasets |
| 6O3Q6AFUTu (NoiseDiffusion) | 8.00 | R1 | No | High-quality paper, not directly comparable |
| zMoNrajk2X (CADS) | 8.00 | R1 | No | High-quality paper, different focus |
| I5lcjmFmlc (Robust Classif) | 8.00 | R1 | No | Different task |
| fV0t65OBUu (OCM) | 8.00 | R1 | No | Different focus |
| t3vnnLeajU (DA-CLIP) | 5.25 | R2 | Yes | Most comparable anchor; CLIP-based multi-task restoration with mixed degradations; had similar experimental-rigor concerns |
| ob9vuDv4yl (HAIR) | 4.67 | R2 | Yes | All-in-one IR; weaker contributions but fewer confounds |
| zLaayPL8f0 (Decomp Synergistic) | 4.75 | R2 | No | Different approach |
| AKMOrcobBE (ReSyn) | 4.33 | R2 | No | Different focus (dataset) |
| C0Ubo0XBPn (Hi-IR) | 5.25 | R2 | No | Stronger experiments than PRISM |
| rUxr9Ll5FQ (InterLCM) | 5.20 | R2 | No | Face restoration, different domain |
| MtoklWYQus (DyNet) | 4.00 | R2 | No | All-in-one IR, weaker |
| RJG7fCVkhQ (Modumer) | 3.50 | R2 | No | All-in-one IR, weaker |

**Round 1 bracket:** 3.5–5.5 (the paper's strengths in downstream evaluation and principled loss design push it above 3.5, but the experimental confound prevents it from reaching 5.5+.)

**Narrowing:** Comparing itemized impact scores against the closest anchors: PRISM's unique strength is the downstream task evaluation (+9.98) — an item no anchor has. Its principled loss design (+9.93) is comparable to HAIR's theoretical proof (+9.97). However, the unfair baseline comparison (-9.93) is a critical flaw that DA-CLIP (-10.00 for experimental simplicity) and InstantIR (-9.22 for non-superior performance) also suffered from — and those papers scored 5.25. PRISM's downstream evaluation contribution is stronger than either of those papers', which places it slightly above HAIR (4.67) but the baseline confound is serious enough that a score above 5.5 would not be justified without stronger evidence.

**Final score: 5.0** — between borderline reject and borderline accept. The paper makes genuine contributions (downstream evaluation framework, principled loss design, zero-shot results) but the central competitive claim in Table 1 is confounded by comparing models trained on different data distributions. The contributions are real but cannot be fully evaluated as presented.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>