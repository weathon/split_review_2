## Summary

This paper presents **PRISM**, a conditional diffusion framework for restoring scientific images affected by *compound* (mixed) degradations. The key technical contribution is a weighted contrastive loss with Jaccard-based alignment that structures the CLIP latent space compositionally, enabling both simultaneous removal of multiple distortions and selective, prompt-driven restoration of individual distortions. The paper evaluates PRISM across four scientific domains (remote sensing, wildlife monitoring, microscopy, urban scenes), demonstrating state-of-the-art performance on compound restoration benchmarks, zero-shot generalization to unseen distortions, and improved downstream task accuracy when controllability is used to selectively remove only certain degradations.

## Strengths

- **Compelling problem formulation and motivation.** The paper makes a clear, well-supported case that scientific images suffer from compound, overlapping degradations that existing single-distortion or sequential pipelines handle poorly. The argument that "more restoration is not always better" is backed by concrete downstream task evidence (Table 3, 4) and is genuinely valuable for the community.

- **Thorough evaluation across multiple scientific domains and downstream tasks.** The paper goes far beyond standard perceptual metrics and evaluates restoration through actual scientific utility (landcover classification, species identification, pit segmentation/fluorescence, panoptic segmentation) using off-the-shelf models. This is a rare and praiseworthy evaluation protocol that directly addresses practical value.

- **Clear demonstration of the value of controllability.** Table 3 shows that selective restoration significantly outperforms full restoration in three of four domains (camera traps, microscopy, urban scenes), and Table 4 provides a striking example where super-resolution and denoising trade off differently against segmentation vs. fluorescence tasks. This establishes controllability as a necessity, not a convenience.

- **Strong zero-shot generalization results.** Table 2 shows PRISM achieves best or second-best metrics on three zero-shot benchmarks (underwater imagery, under-display cameras, fluid lensing) where degradation types were not seen in training. This supports the claim that compositional latent structure aids generalization.

## Weaknesses

### Fatal

None identified.

### Major

- **Unfair baseline comparison.** The paper states that "all baselines are trained on the fixed set of primitive distortions" (Section 3.2), while PRISM is trained on composite mixtures with compound-aware supervision. This gives PRISM a fundamental advantage on the MDB benchmark (Table 1) where test images contain up to three distortions. The ablation in Figure 3 comparing PRISM (Primitive-Aware) vs. PRISM (Compound-Aware) partially addresses this, but the main result table should have included baselines retrained on the same composite data for a genuinely fair comparison.

- **Moderate technical novelty.** The core method combines existing components (CLIP fine-tuning, contrastive learning, latent diffusion, cross-attention conditioning, SCPM from AutoDIR). The weighted contrastive loss with Jaccard distance is a straightforward extension of standard contrastive objectives, and the quality-aware regularizer is simple. While the *combination* is well-engineered and the application domain is important, the paper does not introduce a fundamentally new algorithmic principle or widely reusable theoretical insight.

- **Limited evaluation of expertise-in-the-loop.** The paper claims "expert-guided" restoration (Figure 1, Section 3.3) but all experiments use automated or pre-defined prompts. The selective restoration results in Table 3 were determined by the authors, not by actual domain experts interacting with the system. A user study with scientists from the target domains would substantially strengthen the claim that PRISM enables useful expert-in-the-loop restoration.

### Minor

- **Synthetic-to-real gap is acknowledged but not bridged.** The model is trained entirely on synthetic degradations (Gaussian blurs, weather effects, etc.). While zero-shot results on real datasets are encouraging, the mismatch between synthetic augmentations and real physical distortions (e.g., actual underwater scattering, optical aberrations) remains a limitation for direct deployment in scientific workflows.

- **Statistical reporting in Table 3 is incomplete.** The p-values reported lack specification of the statistical test used (paired t-test? Wilcoxon?) and whether correction for multiple comparisons was applied. Given that four domains are tested, some correction should be considered.

- **The "Rooftop Cityscapes" dataset is mentioned as a contribution but receives minimal description.** Only one sentence in Section 3.4 describes its size, construction, or the specific degradation types, and Appendix C is not provided in the main text.

### Trivial

- Table 2 contains "DiffPlusGin" which is likely a parsing artifact for "DiffPlugin".
- Table 1 lists "MPerciever" (spelling inconsistency with the rest of the paper).

## Nice-to-Haves

- A user study with actual domain experts (ecologists, microscopists, remote sensing analysts) interacting with PRISM's prompt-based control would significantly strengthen the "expert-in-the-loop" claims.
- Training selected baselines (e.g., MPerceiver, AutoDIR) on the same composite data as PRISM would eliminate the comparison fairness concern.
- Analysis of how robust PRISM is to prompt wording variation (e.g., "remove haze" vs. "dehaze" vs. "clear the fog") with systematic perturbation tests.
- Discussion of failure cases: what types of compound degradations does PRISM still struggle with?

## Novel Insights

The paper's most genuinely novel insight is that *controllability of restoration is not merely a user-interface convenience but a scientific necessity* because different downstream analyses (e.g., segmentation vs. intensity measurement in microscopy) require different trade-offs between distortion removal and signal preservation. This observation — backed by quantitative results showing that a single restoration strategy cannot satisfy both objectives simultaneously (Table 4) — challenges the common assumption in image restoration that "cleaner" is always better. This insight has practical implications beyond the paper's specific method.

## Suggestions

- Retrain the most competitive baselines (MPerceiver, AutoDIR, OneRestore) on the same composite training data as PRISM and report a fair comparison in Table 1. If the gap holds, the paper's claims are much stronger.
- Add a small user study (even 3-5 domain experts) where participants are asked to use prompt-based control to achieve a specific analysis goal, and measure task accuracy improvements.
- Clarify the statistical testing methodology in Table 3 (specific test, sample size, correction method).
- Provide more details on the Rooftop Cityscapes dataset in the main text (image count, degradation types, collection protocol).

## Score and Decision

The paper addresses an important and under-studied problem, provides a well-engineered solution, and backs its claims with thorough multi-domain evaluation including downstream scientific tasks. The demonstration that controllability matters for downstream accuracy is a genuinely valuable finding. However, the unfair baseline comparison (training baselines only on primitive distortions while PRISM trains on composites) weakens the main quantitative claims, and the technical novelty is moderate. The paper is solid but falls short of the strong empirical demonstration needed for a high acceptance score.

**Score**: 6 (borderline accept)

**Decision**: Accept

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>