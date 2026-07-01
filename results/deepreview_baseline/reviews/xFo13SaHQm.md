## Summary
The paper identifies and formalizes the "copy-paste artifact" in identity-consistent image generation, where models overly replicate reference faces instead of preserving identity across natural variations. To address this, the authors contribute (1) MultiID-2M, a large-scale dataset of 500k group photos with paired reference images per identity and 1.5M unpaired photos; (2) MultiID-Bench, a benchmark that quantifies copy-paste artifacts and the fidelity-variation trade-off; and (3) WithAnyone, a diffusion model on FLUX that uses a four-stage training pipeline with a ground-truth-aligned ID loss and an ID contrastive loss with extended negatives. Experiments show that WithAnyone substantially reduces copy-paste artifacts while maintaining high identity similarity, breaking the typical trade-off.

## Strengths
- **Large-scale paired dataset.** MultiID-2M is a valuable resource, providing ~500k group photos where each identity has many reference images across diverse poses/expressions. This fills a clear gap in existing datasets that lack paired references for multi-identity settings.
- **Well-motivated benchmark and metric.** MultiID-Bench introduces a copy-paste metric (M_CP) that correctly penalizes models that simply clone the reference, and uses similarity to the ground-truth (Sim_GT) as the primary identity metric rather than Sim_Ref, which rewards copying. The benchmark includes 12 baselines, revealing a clear trade-off curve.
- **Effective method with thorough evaluation.** WithAnyone achieves the best or near-best Sim_GT on multi-person subsets while scoring much lower copy-paste than competing models. The four-phase training pipeline and the contrastive loss with 4096 negatives are well ablated (Table 3, Fig. 7), and user studies confirm human preference.
- **Extensive baselines and reproducible setup.** The comparison covers both general customization models (OmniGen, GPT-4o, FLUX.1 Kontext, etc.) and dedicated face customization methods (PuLID, InstantID, UniPortrait, etc.) on both single- and multi-person subsets. The project is open-sourced.

## Weaknesses
### Fatal
None.

### Major
None that invalidate the core claims. The following issues are noticeable but not fatal.

- **Reliance on a proprietary base model.** WithAnyone is built on FLUX, which is released under a non-commercial license and is not fully open. This limits exact reproducibility and downstream use by the community compared to methods built on fully open backbones. The paper should be explicit about which components are open-sourced (adapters / training scripts) versus the base model.
- **Dataset ethical and legal concerns.** Although the paper describes filtering by Creative Commons licenses and focuses on publicly known figures, constructing a dataset by scraping web images of celebrities still raises privacy and consent issues. The anonymization (using only internal IDs) is a reasonable mitigation, but the dataset's release terms and potential for misuse (identity cloning) may be a concern for some reviewers.

### Minor
- **Overclaim on "state-of-the-art" in single-person setting.** In Table 1, InstantID achieves higher Sim_GT (0.464 vs. 0.460). The paper's primary claim is about reducing copy-paste while maintaining high similarity; the phrase "state-of-the-art identity similarity" could be read as absolute SOTA, which is technically not true on that metric. Rephrasing to "competitive identity similarity with substantially reduced copy-paste" would be more accurate.
- **Complex training pipeline.** The four-phase pipeline (including fixed-prompt pre-training, caption pre-training, paired tuning, and quality tuning) is effective but increases engineering overhead. The paper does not analyze the sensitivity of phase ordering or length, which would strengthen the recipe.
- **Limited multi-person evaluation for some baselines.** In the multi-person subset (Table 2), only a subset of baselines support multi-ID input; the comparison is still fair but the set is smaller than the single-person evaluation.

### Trivial
- Several figures (e.g., Fig. 2, Fig. 4) are referenced in the text but have reduced readability due to small fonts; this does not affect the technical content.

## Nice-to-Haves
- Provide inference-time results on in-the-wild images (without a ground-truth) to demonstrate generalizability beyond the benchmark's paired setting.
- Analyze the contribution of each training phase with more granular ablations (e.g., varying the fraction of paired data in Phase 3, or the number of negatives in the contrastive loss).
- Release a smaller, non-celebrity version of the dataset for research groups that cannot use celebrity data due to ethical constraints.

## Novel Insights
The most novel insight beyond the paper's own contributions is the formal quantification of the copy-paste artifact as a measurable failure mode that is distinct from identity similarity. This reframes the evaluation of ID-consistent generation from a single-axis (similarity) to a two-axis trade-off (similarity vs. copying). The paper also demonstrates that supervised training with paired references—where the reference and target are different images of the same person—can break this trade-off, whereas reconstruction-based training inherently reinforces it. The GT-aligned ID loss is a simple but effective trick to apply ID supervision at all noise levels without needing full denoising.

## Suggestions
- Clarify the "state-of-the-art" claim in the single-person table title or text to avoid potential misinterpretation.
- Explicitly state the open-source status of each component (base model, adapter weights, dataset, evaluation code) in a single sentence in the introduction or conclusion.

## Score and Decision
Score: 8 – Accept.

The paper makes three substantial contributions (dataset, benchmark, method) that are well-motivated, technically sound, and thoroughly evaluated. The identification and formalization of copy-paste artifacts is timely and practically important. The weaknesses (reliance on FLUX, ethical dataset concerns, minor overclaiming) are not fatal and can be addressed through clearer communication. Overall, the paper provides significant value to the community and pushes the state of the art in controllable identity-consistent generation.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>