## Summary

This paper identifies and theoretically establishes a fundamental label dependency in semi-supervised learning (SSL), where the ability to utilize unlabeled data is bounded by the quantity and quality of labeled data. To address this, the authors propose CaPT (CLIP as a Prior Teacher), a novel asymmetric-modalities co-training framework that efficiently integrates CLIP into SSL by aggregating predictions from a fully fine-tuned unimodal network and a parameter-efficiently fine-tuned multimodal CLIP model via carefully designed co-pseudo labels. CaPT consistently achieves state-of-the-art performance across multiple SSL benchmarks, with particularly significant improvements in low-label regimes, outperforming the second-best method by 21.38% on CIFAR-100 under the one-label-per-class setting.

## Strengths

- **Strong theoretical motivation**: The paper provides both empirical evidence and a theoretical analysis (Theorem 1.1) demonstrating that SSL methods are fundamentally label-dependent, with pseudo label error bounded by the quantity and quality of labeled data. This provides a principled justification for why integrating external priors like CLIP is necessary.
- **Novel and well-designed framework**: The asymmetric-modalities co-training design is clever—it leverages CLIP's zero-shot prior while avoiding the pattern-homogeneity bottleneck of co-training two pure-vision models. The use of adapter-tuning for CLIP and feature-augmented consistency regularization balances efficiency and effectiveness.
- **Impressive empirical results**: CaPT achieves state-of-the-art performance across diverse benchmarks (CIFAR-100, STL-10, EuroSAT, ImageNet, fine-grained datasets), with particularly striking gains in extremely low-label regimes (e.g., 21.38% improvement on CIFAR-100 with 1 label per class). The results are consistent and have low variance across random seeds.
- **Comprehensive evaluation**: The paper evaluates CaPT on multiple benchmarks (USB, ImageNet, fine-grained datasets), under extreme label scarcity, and includes thorough ablation studies validating each design choice. The efficiency analysis (Table 4) shows minimal overhead compared to standard SSL methods.

## Weaknesses

### Fatal
None.

### Major
- **Limited novelty in the theoretical contribution**: The theoretical analysis (Theorem 1.1) is presented as a key contribution, but it essentially formalizes an intuitive result—that poor labeled data leads to poor pseudo labels. The bound is derived under a specific prototype-based Gaussian-mixture model and depends on several unobservable quantities (g, σ², B), making it difficult to verify or apply in practice. The theorem does not provide actionable insights beyond what the empirical observations already demonstrate.
- **Incomplete comparison with CLIP-based SSL methods**: The paper compares against DebiasPL only in a limited ablation (CaPT-Deb) but does not include it as a baseline in the main tables. Given that DebiasPL is the most directly related prior work on integrating CLIP into SSL, a full comparison on the same benchmarks would strengthen the paper. The paper also does not compare against other CLIP-based SSL approaches like CLIP-Adapter-based SSL or other vision-language model integration methods.
- **Potential data contamination concern**: The paper acknowledges this in Appendix M but does not fully address it. CLIP was trained on web-scale data that likely includes images from CIFAR, STL-10, and EuroSAT. The strong performance on these datasets could partially reflect CLIP's familiarity with the data distribution rather than genuine SSL improvement. The fine-grained dataset results partially mitigate this, but the main claims rely heavily on standard benchmarks.

### Minor
- **The entropy-based weighting mechanism (Eq. 11-12) is somewhat ad-hoc**: The paper uses average batch entropy to compute model weights, but this is a coarse measure of model reliability. A sample-level weighting scheme might be more appropriate, especially when different models are confident about different samples. The ablation shows only a modest improvement over equal weighting (0.87-1.57%), suggesting this component is not critical.
- **The feature-augmented consistency regularization (Eq. 9) uses Mixup on features from weakly augmented samples**: This is a reasonable approximation, but it is not equivalent to strong augmentation at the input level. The paper does not compare against input-level strong augmentation for CLIP (which would be computationally expensive but potentially more effective).

### Trivial
- The paper uses "co-pseudo labels" as a central concept, but the term is not clearly distinguished from standard pseudo labels in the initial introduction.

## Nice-to-Haves

- A comparison against a variant that uses a more recent vision-language model (e.g., SigLIP, EVA-CLIP) to demonstrate the "future-proof" claim more concretely.
- Analysis of which classes benefit most from CLIP's prior—does CaPT help more for classes where CLIP has strong zero-shot performance, or does it help uniformly?
- A discussion of failure cases: are there settings where CaPT underperforms standard SSL methods?

## Novel Insights

The paper's key insight is that SSL's label dependency is not merely a practical limitation but a structural one—the utility of unlabeled data is fundamentally coupled to labeled data quality. This is formalized through a theoretical bound showing that pseudo label error increases as labeled data quantity or quality decreases. The paper then demonstrates that this coupling can be broken by introducing an external prior (CLIP) that provides supervision independent of the labeled set. The asymmetric-modalities co-training design is a practical instantiation of this principle, showing that cross-modal complementarity (vision vs. vision-language) provides richer information exchange than co-training two unimodal models. This insight about modality asymmetry as a design principle for co-training is potentially applicable beyond SSL to other semi-supervised or self-supervised learning paradigms.

## Suggestions

- Add a full comparison against DebiasPL and other CLIP-based SSL methods on the main benchmarks to strengthen the empirical contribution.
- Clarify the practical implications of Theorem 1.1—what specific design guidelines does it suggest beyond "use better labeled data or an external prior"?
- Consider adding a sample-level confidence weighting mechanism instead of batch-level entropy weighting, or provide a stronger justification for the batch-level approach.

## Score and Decision

The paper makes a solid contribution by identifying and addressing a genuine limitation of SSL, proposing a well-designed framework that achieves strong empirical results. The theoretical analysis, while not groundbreaking, provides useful formalization. The main concerns are the limited comparison against directly related CLIP-based SSL methods and the potential data contamination issue. However, the strength of the empirical results, particularly in low-label regimes, and the soundness of the framework design outweigh these concerns.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>