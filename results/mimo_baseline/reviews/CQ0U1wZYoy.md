## Summary

This paper introduces PRISM, a prompted conditional diffusion framework for scientific image restoration that handles compound (multi-distortion) degradations while enabling selective, controllable correction via natural language prompts. The key technical contributions are a Jaccard-weighted contrastive loss that enforces compositional structure in the degradation embedding space, compound-aware supervision using mixed/subset/negative prompts, and a systematic demonstration across four scientific domains that controllable restoration yields better downstream task performance than indiscriminate "full" restoration.

## Strengths

- **Well-motivated problem framing with genuine practical value.** The paper convincingly argues that scientific image restoration requires simultaneous compound correction, precision over aesthetics, and expert control. The examples of over-denoising erasing faint galaxies or super-resolution hallucinating subcellular structures are compelling and well-referenced, grounding the work in real scientific needs rather than purely aesthetic goals.

- **Novel compositional latent space design.** The Jaccard-distance-weighted contrastive loss (Eq. 1–2) that pulls compound degradations toward the span of their constituent primitives is a principled approach to enabling compositional generalization. The quality-aware regularizer (Eq. 3) preventing clean-image embedding drift is a thoughtful addition. The ablation in Figure 3 showing that compound-aware training degrades gracefully with increasing distortion count (ΔPSNR of 8.14 vs. 11.12–11.33 for baselines) provides strong evidence for this design.

- **Genuinely important insight about controllability.** Table 3 and the microscopy analysis (Table 4, Figure 6) demonstrate that selective restoration outperforms full restoration on 3 of 4 downstream tasks, with the microscopy case showing that super-resolution helps segmentation but hurts fluorescence measurement. This task-dependence finding is non-obvious, practically significant, and supported by reasonable statistical evidence (p-values reported). This goes beyond typical restoration papers and would be valuable to the scientific imaging community.

- **Comprehensive multi-domain evaluation.** The evaluation spans microscopy, wildlife monitoring, remote sensing, underwater imagery, and urban scenes, including both synthetic MDB benchmarks and real-world zero-shot datasets (UIEB, POLED, ThapaSet). The inclusion of downstream task evaluation (classification accuracy, segmentation mIoU, fluorescence MSE) alongside standard image quality metrics is a notable methodological contribution.

- **Fair ablation design.** The comparison with OneRestore (both trained on composite data, Table 1) isolates the contribution of PRISM's architectural design from compound training alone. The primitive-aware vs. compound-aware CLIP ablation (Figure 4) and the sequential vs. composite prompting comparison provide granular insight into each component's contribution.

## Weaknesses

### Fatal
None.

### Major

- **Baseline training fairness could be more explicitly addressed.** The main comparison in Table 1 includes baselines trained on primitive distortions while PRISM is trained on compounds. While OneRestore partially controls for this, and the ablation in Figure 3 helps, the paper should more explicitly discuss why existing baselines were not retrained on compound data. Some baselines (e.g., MPerceiver, AutoDIR) might improve substantially with compound training, making the gap partly attributable to training data rather than architectural design. The paper mentions "for fair comparison, all baselines are trained on the fixed set of primitive distortions" but does not explain why compound training was not applied to them or reference any failed attempts.

- **Selective restoration methodology in Table 3 is underspecified.** The paper does not clearly explain how "selective restoration" choices were made. Was the optimal subset of distortions to remove chosen per-task via grid search? If so, this amounts to hyperparameter tuning that full restoration does not benefit from, potentially inflating the gap. A clearer description of the selection protocol (e.g., fixed rules, oracle selection, or domain-expert guidance) and whether the same tuning effort was available to full restoration would strengthen this key claim.

### Minor

- **Zero-shot generalization claims need stronger controlled evidence.** The zero-shot experiments (Table 2) test on real datasets with real distortions that may share low-level statistics with training primitives, even if specific combinations are new. A controlled experiment on specific held-out combinations of known primitives (e.g., training without haze+noise but testing on it) would more directly validate the compositional generalization claim.

- **The contribution of SCPM is not fully separated.** The Semantic Content Preservation Module is acknowledged as following Jiang et al. (2024), but its contribution to overall performance gains is not clearly delineated in the main results. If SCPM contributes substantially to the PSNR/SSIM improvements, then the headline gains are partly attributable to a prior component rather than PRISM's core novelty.

- **The Rooftop Cityscapes dataset is mentioned but barely described.** This is listed as a contribution ("our newly-introduced Rooftop Cityscapes dataset"), but the main text provides almost no detail about its construction, size, or characteristics. This limits the reader's ability to evaluate this contribution.

### Trivial

- Some figures (e.g., Figure 1, Figure 5) rely heavily on caption text to convey information that would benefit from cleaner visual presentation, but this is a formatting issue.

## Nice-to-Haves

- A failure case analysis showing when PRISM's controllable prompting fails or produces unexpected results would improve transparency and help practitioners understand limitations.
- Comparing PRISM's downstream task performance against other restoration baselines (not just PRISM variants) would contextualize the value more clearly.
- An analysis of how sensitive PRISM is to the number of distortions in the training compound mixtures (beyond the 1–4 distortion test) would be informative.

## Novel Insights

The paper's most genuinely novel insight is that restoration quality and scientific utility are not monotonically related, and that the optimal restoration strategy depends on the downstream task. The microscopy case is particularly striking: super-resolution improves segmentation (preserving structural boundaries) but degrades fluorescence measurement (introducing intensity artifacts), while denoising has the opposite effect. This task-dependence insight—demonstrated empirically across four domains—challenges the implicit assumption in the restoration literature that better perceptual metrics always translate to better utility, and motivates the need for controllable rather than fixed restoration pipelines.

## Suggestions

- Add a table or discussion explicitly comparing all baselines retrained on compound data to isolate architectural contributions from training data contributions.
- Clarify the selective restoration protocol in Table 3: whether the distortion subset was chosen by oracle, by domain expertise, by automated search, or by some fixed heuristic, and apply equivalent effort to the full restoration baseline.
- Add a controlled compositional generalization experiment on held-out combinations of known training primitives to directly validate the latent space compositionality claims.
- Expand the Rooftop Cityscapes dataset description in the main text.

## Score and Decision

This paper makes a well-motivated contribution to an important and underexplored problem at the intersection of image restoration and scientific imaging. The technical design is principled, the experiments are comprehensive, and the key insight about controllability improving downstream scientific accuracy is novel and practically valuable. The major concerns around baseline fairness and selective restoration methodology are addressable but do not invalidate the core contributions. The paper would be a meaningful addition to the ICLR program, particularly given its emphasis on scientific utility over purely perceptual metrics.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: Accept