## Summary
The paper proposes the Normalized Matching Transformer (NMT), a pure deep-learning pipeline for sparse keypoint matching that combines a Swin-Transformer backbone, SplineCNN for geometric feature refinement, and a normalized transformer (nGPT) with per-layer hyperspherical normalization. Training uses a joint InfoNCE and hyperspherical uniformity loss. NMT claims state-of-the-art accuracy on PascalVOC (+5.1%) and SPair-71k (+2.2%) while converging in at least 1.7× fewer epochs than prior baselines.

## Strengths
- **Strong empirical results with informative ablations.** Table 4 decomposes contributions clearly: loss function choice (+15.1%), backbone upgrade (+4.9%), normalized transformer (+2.6%), layer-wise auxiliary loss (+0.8%), augmentation (+1.2%). This granularity gives readers actionable insights beyond the SOTA headline.
- **Coherent architectural motivation.** The decision to enforce unit-norm embeddings throughout every transformer layer (not just at the output) is well-motivated: if matching scores are ultimately computed as cosine similarities, maintaining the hyperspherical geometry at every layer allows losses to directly shape intermediate representations, and the ablation confirms this helps.
- **Practical efficiency.** Training in 6 epochs vs. 10–16 for strong baselines (BBGM, ASAR, COMMON) on the same hardware, while achieving better accuracy, is a meaningful engineering benefit.

## Weaknesses

### Fatal
None.

### Major
- **Notation inconsistency in the hyperspherical loss (Equations 2–3).** Equation 2 defines matrix C using cross-image cosine similarities cos\_sim(f_i^1, f_j^2), but the text and Figure 2 state the hyperspherical loss is applied to *same-image* features (cos\_sim(f, f) and cos\_sim(f', f')). As written, Equation 3 would operate on a cross-image similarity matrix, which contradicts the stated purpose of promoting intra-image feature diversity. The paper never defines the same-image analogue of C explicitly, leaving the actual hyperspherical loss formulation ambiguous. Readers cannot reproduce the loss from the paper alone.
- **Epoch count is an incomplete efficiency measure.** The claim of "≥1.7× fewer epochs" is hedged in the paper itself ("time per epoch might not be comparable"). NMT uses a much larger backbone (Swin-Large at 384×384) and a normalized transformer with reportedly worse kernel fusion. Wall-clock training time is reported (9 h for PascalVOC) but no comparable wall-clock figures for baselines are given, making the efficiency claim hard to verify.

### Minor
- **Comparison table anomalies.** In Table 2, both CGMPT and COMMON Liu et al. (2020) show exactly 75.2% for every single category—an implausible pattern that likely reflects OCR/parsing damage—yet second-best underlines and bold formatting are assigned relative to these entries, potentially affecting how the comparison reads.
- **Backbone-driven gains are partially confounded.** The ablation shows VGG→Swin-Large accounts for 4.9% of the 5.1% improvement over BBGM/ASAR/COMMON, which use VGG. The paper acknowledges this but does not compare NMT's transformer/loss innovations against a Swin-Large + cross-entropy baseline, which would better isolate the hyperspherical contribution over the backbone choice.
- **Hyperspherical loss formulation is non-standard.** Equation 3 uses max_{j≠i} C_{ij}, penalizing only the single most-similar non-matching keypoint per query. Standard hyperspherical uniformity losses (e.g., log-sum-exp pairwise repulsion) provide smoother gradients and more uniform coverage. The max-based variant may cause gradient sparsity; no discussion or comparison against the standard formulation is provided.

### Trivial
- Sinkhorn is noted as being used "only during inference," though differentiable Sinkhorn is standard practice; the reason for excluding it from training is not discussed.

## Nice-to-Haves
- A wall-clock training time comparison with at least one strong baseline (e.g., GMTR, which uses Swin) would make the efficiency claim more credible.
- Ablating the max-based hyperspherical loss against a log-sum-exp alternative would help the community understand the design choice.

## Novel Insights
The core technical insight—that maintaining unit-norm geometry *at every transformer layer* (not just the output) creates a consistent hyperspherical learning signal throughout the network and accelerates convergence—is a genuine contribution to the design of contrastive architectures for structured prediction problems. The combination of nGPT-style normalization with InfoNCE and hyperspherical losses in a graph matching context had not been demonstrated before, and the ablation evidence that the normalized transformer outperforms a vanilla transformer by 2.6% (with matched architecture otherwise) supports this design principle beyond simple SOTA chasing.

## Suggestions
- Fix or re-derive Equations 2–3 to clearly define same-image cosine similarity matrices used in the hyperspherical loss, aligning notation with Figure 2.
- Provide wall-clock training time (in hours) for at least the strongest baseline (GMTR, which uses a similar Swin backbone) to substantiate the efficiency claim.
- Add a baseline comparing Swin-Large + vanilla transformer + cross-entropy to help disentangle backbone, architecture, and loss contributions more cleanly.

## Score and Decision
The paper makes a clear and well-validated engineering contribution to sparse keypoint matching, achieving genuine SOTA with a principled hyperspherical design. The major weaknesses (inconsistent loss formulation, incomplete efficiency analysis) are significant but do not invalidate the core empirical results; ablations are thorough and the main findings are reproducible in spirit. Novelty is incremental (each component is existing work) but their combination is non-trivial and the paper's empirical contribution is solid.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>