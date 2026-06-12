## Summary

This paper identifies a fundamental limitation in semi-supervised learning (SSL): the ability to exploit unlabeled data is tightly coupled to the quantity and quality of labeled data. To address this, the authors propose CaPT, an asymmetric-modalities co-training framework that jointly trains a fully fine-tuned unimodal vision network with a parameter-efficiently fine-tuned CLIP model, using co-pseudo labels to exchange complementary supervision. CaPT achieves state-of-the-art results across multiple SSL benchmarks, with particularly striking improvements in extreme low-label regimes (e.g., 21.38% over the second-best method on CIFAR-100 with one label per class).

## Strengths

- **Well-motivated problem with theoretical grounding.** The paper provides both empirical evidence (Figure 1) and a formal theorem (Theorem 1.1) establishing that pseudo label error depends on labeled data quality/quantity through an effective margin term. This gives principled motivation for why CLIP's zero-shot prior can help break this dependency.

- **Strong and convincing empirical results.** CaPT consistently outperforms all baselines across USB benchmarks (Table 1), ImageNet (Table 2), and extreme one-label-per-class settings (Table 3). The 21.38% improvement on CIFAR-100 and 9.33% on ImageNet (10 labels/class) are substantial margins. The low standard deviations indicate stable training.

- **Practical efficiency.** Table 4 shows CaPT adds only 8% memory and 11% training time over FreeMatch while achieving significantly better accuracy, and is more efficient than RegMixMatch. The use of adapter-tuning and feature-level augmentation (avoiding re-encoding high-resolution images) is a sensible engineering choice.

- **Comprehensive ablation studies.** Table 6 systematically validates each component: the full co-training framework, adapter-tuning for debiasing CLIP (supported by Figure 5), bidirectional information flow, feature-augmented consistency, and entropy-based weighting. Each ablation shows meaningful performance differences.

- **The asymmetric co-training insight is novel and well-supported.** Figure 3 provides compelling visual evidence that CLIP's cross-modal representations attend to different image regions than pure-vision ViTs, directly addressing the pattern-homogeneity bottleneck in prior co-training methods like CLS.

## Weaknesses

### Fatal
None.

### Major

- **Missing direct comparison with DebiasPL in main tables.** DebiasPL is a closely related method that also integrates CLIP into SSL, and the paper discusses it extensively in the introduction and Figure 2. However, it does not appear in any of the main experimental tables (Tables 1–5). While the paper argues DebiasPL suffers from biased predictions, a direct numerical comparison would strengthen the claims about CaPT's advantages. The ablation CaPT-Deb partially addresses this but is not a full DebiasPL implementation.

- **Mixed results on FGVCAircraft.** CaPT underperforms FreeMatch (50.12% vs. 51.43%) with 5 labels per class on FGVCAircraft, which the authors attribute to CLIP's weak prior on this dataset. While acknowledged, this raises questions about the robustness of the framework when CLIP's prior is uninformative or harmful. The paper would benefit from a more systematic analysis of when and why CLIP's prior helps versus hurts, beyond a brief appendix mention.

### Minor

- **Theorem 1.1's scope is limited.** The theoretical analysis assumes a Gaussian mixture model with nearest-prototype classification, which is a significant simplification from the actual SSL pipeline (deep networks, consistency regularization, adaptive thresholds). While useful for intuition, the gap between the theoretical model and the practical system is large. The theorem motivates the problem but doesn't directly analyze CaPT's solution.

- **Single CLIP variant used throughout.** All experiments use ViT-B/32 as CLIP's visual encoder. Given that CLIP comes in multiple sizes (ViT-B/16, ViT-L/14, etc.) with varying zero-shot performance, understanding the sensitivity to CLIP capacity would strengthen the paper's generality claims.

- **Entropy-based weighting is relatively simple.** The weighting mechanism (Equation 12) uses batch-level entropy, which could be noisy for small batch sizes. More sophisticated approaches (e.g., per-sample weighting, curriculum-based scheduling) might further improve performance, though the current approach works well empirically.

### Trivial
None.

## Nice-to-Haves

- A comparison showing how CaPT performs as the number of labeled samples increases toward moderate levels (e.g., 100, 400 per class), to understand where the CLIP prior becomes less critical and the method converges to standard SSL performance.
- Analysis of failure cases: which classes or image types cause CLIP's prior to be misleading, and whether the entropy-based weighting successfully downweights these cases during training.

## Novel Insights

The paper's key novel insight is that SSL's label dependency is not merely a practical limitation but a structural one: the utility of unlabeled data is fundamentally bounded by labeled data quality, as formalized through the effective margin in Theorem 1.1. This reframes the problem from "how to better use unlabeled data given labels" to "how to provide an alternative supervision source that is decoupled from labels." The asymmetric co-training design is a natural consequence—by using CLIP's pre-trained cross-modal knowledge as an independent prior, the framework can bootstrap pseudo labels even when labeled data is extremely scarce. The observation that cross-modal representations break the pattern-homogeneity bottleneck in co-training (Figure 3) is a genuinely useful insight for the co-training literature beyond SSL.

## Suggestions

- Include DebiasPL in the main experimental tables to provide a complete comparison with the most directly related CLIP-integrated SSL method.
- Add experiments with at least one additional CLIP variant (e.g., ViT-L/14) to demonstrate the framework's sensitivity to CLIP capacity and its potential for improvement with stronger VLMs.
- Provide a more explicit analysis of when CLIP's prior is beneficial versus detrimental, potentially with a dataset-level metric that predicts CaPT's expected gain over standard SSL.

## Score and Decision

The paper presents a well-motivated framework with strong empirical results, particularly in the extreme low-label regime that is its primary focus. The asymmetric co-training design is a genuine contribution supported by both theoretical analysis and visual evidence. The practical efficiency and comprehensive ablations add to the paper's value. The main weaknesses—missing DebiasPL comparison and mixed results on certain datasets—are notable but do not invalidate the core contribution. The paper advances the important problem of reducing label dependency in SSL and provides a practical, extensible framework.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: Accept