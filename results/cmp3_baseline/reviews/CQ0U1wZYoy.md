## Summary

The paper introduces **PRISM**, a conditional diffusion framework for compound and controllable restoration of scientific images. It combines compound-aware supervision (training on mixtures of up to three distortions) with a weighted contrastive disentanglement objective that aligns degradation mixtures and their primitives in CLIP’s latent space. The model is evaluated on synthetic mixed degradations, zero-shot real-world datasets, and downstream scientific tasks (remote sensing, ecology, microscopy, urban monitoring), showing improvements over baselines and demonstrating that selective, distortion-specific restoration can improve scientific accuracy.

## Strengths

- **Important and well-motivated problem.** The focus on compound degradations in scientific imagery (microscopy, wildlife monitoring, remote sensing) and the need for controllable restoration that preserves scientific signal rather than just perceptual quality is timely and valuable.
- **Controllability study is a highlight.** The experiments in Tables 3 and 4 convincingly show that indiscriminate restoration can harm downstream task performance, and that allowing selective removal of only certain distortions provides meaningful improvements. This insight is clearly articulated and supported.
- **Zero-shot generalization is demonstrated.** The model is evaluated on three real-world datasets (UIEB, POLED, ThapaSet) with unseen compound distortions, and achieves strong results, suggesting the compositional latent representation does generalize beyond training.
- **Downstream task evaluation is a strength.** Using off-the-shelf pretrained models on real scientific tasks (landcover classification, species identification, pit segmentation, urban scene segmentation) provides a practical measure of restoration utility beyond pixel metrics.

## Weaknesses

### Fatal

- **Unfair comparison to baselines undermines the central claims.** The paper states “For fair comparison, all baselines are trained on the fixed set of primitive distortions” while PRISM is trained on compound mixtures (up to three overlapping distortions). This means the performance gains in Tables 1 and 2 may simply reflect training data differences rather than the proposed method itself. The paper attempts to control for this by comparing PRISM (primitive-aware) vs PRISM (compound-aware) in Figure 3, but the main comparisons against AutoDIR, MPerceiver, OneRestore, etc. are not controlled for training distribution. Without training these baselines on the same compound dataset, the claim that PRISM “outperforms state-of-the-art baselines” is not fairly supported.

### Major

- **Downstream evaluation only compares PRISM variants, not other methods.** The downstream experiments (Table 3) only compare PRISM full restoration vs PRISM selective restoration. We do not know whether PRISM’s restoration (full or selective) is better for downstream tasks than restoration from any competing method (e.g., AutoDIR, MPerceiver). This limits the practical significance of the controllability claim.
- **The selective restoration protocol is underspecified.** It is unclear how the “Selective Restoration” set of distortions was chosen for each domain. Was it based on expert knowledge, ablation over all subsets, or some heuristic? Without a systematic procedure, the results risk cherry-picking the most favorable combination.
- **Limited evidence for compositional latent geometry.** The paper claims a “structured, compositional latent space” and “separable embeddings for primitives and their mixtures,” but the evidence is largely qualitative (Appendix t-SNE) and an indirect gap analysis (Figure 4). More rigorous tests (e.g., linear interpolation, analogy completion, or quantitative disentanglement metrics) would substantially strengthen this core design claim.

### Minor

- The “novel benchmark for scientific utility” is not clearly defined as a reusable resource; it appears to be a collection of four evaluation protocols rather than a standardized benchmark with leaderboard or canonical splits.
- The Rooftop Cityscapes dataset is introduced but its construction, size, and use beyond the single row in Table 3 are deferred to the appendix. Its contribution as a general benchmark is unclear.

### Trivial

- None.

## Nice-to-Haves

- Train all baselines on the exact same compound degradation dataset as PRISM and rerun Tables 1 and 2 to enable a clean, fair comparison.
- Extend the downstream evaluation by including other restoration methods (e.g., AutoDIR, MPerceiver) to measure whether PRISM’s restoration is actually more useful for scientific tasks.
- Provide a systematic study of selective restoration: report results for each possible subset of distortions, or a simple automatic selection rule, to avoid ambiguity about how choices were made.
- Add quantitative disentanglement metrics (e.g., DCI, FactorVAE score) on the fine-tuned CLIP embeddings to directly measure compositional structure.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

1. **Rerun baselines with compound training data.** This is the most critical fix: train AutoDIR, MPerceiver, and other methods on the same mixture dataset used for PRISM and re-evaluate. Without this, the core empirical claims are not valid.
2. **Clarify selective restoration protocol.** Describe the exact method by which the “selective” distortion set is chosen in Table 3. Ideally, pre-define a simple, repeatable rule (e.g., “remove only the distortion type that degrades the downstream model most”).
3. **Add downstream comparisons against other methods.** Evaluate the downstream tasks using outputs from AutoDIR, MPerceiver, etc. (trained on compound data) and compare to PRISM (full and selective). This would demonstrate practical superiority.
4. **Strengthen latent space analysis.** Show that the embedding space supports arithmetic operations (e.g., e(clean + haze + rain) ≈ e(clean + haze) + e(clean + rain) − e(clean)) or measure linear separability of distortion primitives.
5. **Provide a clear definition of the benchmark.** Specify fixed train/test splits, metrics, and evaluation scripts for the four downstream tasks so others can reproduce and compare.

## Score and Decision

**Weaknesses:** The fatal comparative unfairness invalidates the central experimental evidence for state-of-the-art claim. While the problem framing and controllability study are valuable, the core methodological advantage is not convincingly demonstrated. Major issues with the downstream evaluation scope and latent space evidence further weaken the paper.

**Overall assessment:** Interesting ideas with insufficiently rigorous experimental support for the claimed contributions. The paper would benefit substantially from controlled baselines and broader comparisons.

**Score:** 4  
**Decision:** Reject

MY FINAL SCORE: 4
MY FINAL DECISION: Reject