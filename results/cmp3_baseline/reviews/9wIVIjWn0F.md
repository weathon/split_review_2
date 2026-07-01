## Summary
This paper proposes Regression-based Test-time Adaptation (RTA) for vision-language models like CLIP. The key insight is that a regression mapping between augmented views' logits and their cross-entropy loss can be learned offline on diverse pseudo-labeled data, and then used during test-time to select confident views without needing true labels. The method trains a lightweight regression model (LightGBM) on a small set of pseudo-labeled data to predict view quality, and demonstrates strong performance across single-label, multi-label, and cross-domain benchmarks, outperforming existing entropy-based TTA methods.

## Strengths
- **Novel and well-motivated approach**: The paper identifies a fundamental limitation of entropy-based view selection—its reliance on single-instance probability distributions—and proposes a principled alternative by learning a regression mapping from logits to cross-entropy loss. The "ceiling TTA" analysis (Tables 1-2) convincingly demonstrates the large gap between entropy-based selection and ground-truth loss-based selection, providing strong motivation for the method.
- **Strong empirical results**: RTA consistently outperforms a comprehensive set of baselines (TPT, DiffTPT, TDA, Zero, BCA, ML-TTA, etc.) across diverse benchmarks including single-label (ImageNet variants), cross-domain (10 datasets), and multi-label (MSCOCO, VOC2007, NUSWIDE) settings, for both RN50 and ViT-B/16 backbones. The gains are particularly notable on challenging OOD datasets like ImageNet-A.
- **Practical efficiency**: The method requires only a single offline training of a lightweight regression model (LightGBM) on a small set of pseudo-labeled data (1,000 samples), and then can be applied to any test distribution without further updates. This is a significant practical advantage over methods that require per-instance or per-batch adaptation.
- **Well-motivated and clearly presented**: The paper provides strong empirical motivation (ceiling TTA experiments, t-SNE visualization, Spearman correlation analysis) for the core claim that logits have a predictable relationship with cross-entropy loss. The method is clearly described with algorithms and the experimental setup is thorough.

## Weaknesses
### Fatal
None.

### Major
1. **The regression mapping is trained on pseudo-labels, not true labels, which introduces a critical gap between the claimed "regression mapping" and what is actually learned.** The paper's core motivation (Section 4.1) is based on the strong performance of ground-truth label cross-entropy loss (LCE) for view selection. However, the actual RTA method trains the regression model on pseudo-labels obtained by filtering high-confidence CLIP predictions (threshold ≥ 0.8). This means the regression model learns to predict pseudo-label cross-entropy loss, not true label cross-entropy loss. The paper does not analyze how this gap affects performance, nor does it compare against a version trained with true labels to quantify the degradation. This is a significant concern because the entire motivation hinges on the superiority of true-label loss over entropy, but the actual method uses a proxy.

2. **The method's independence from downstream tasks is overstated.** The paper claims RTA "only needs to be trained once in the initial stage, and then it can directly adapt to test instances with arbitrary distributions." However, the regression mapping is trained on logits from CLIP's zero-shot predictions, which are inherently tied to the class label space of the downstream task (the text prompts "a photo of [CLASS]"). If the downstream task has a completely different set of classes (e.g., fine-grained bird species vs. general objects), the logit space and the regression mapping would need to be re-learned. The paper only evaluates on ImageNet-derived datasets and standard cross-domain benchmarks that share the same 1000-class ImageNet label space, so the claim of "arbitrary distributions" is not adequately supported.

3. **The comparison with baselines is not entirely fair for some methods.** RTA uses 64 augmented views and a 0.1 confidence filtering ratio, but some baselines (e.g., TPT, DiffTPT) may use different numbers of views or different augmentation strategies. The paper does not control for the number of views used by each baseline, nor does it report the computational cost (e.g., FLOPs, runtime) of RTA vs. baselines. Since RTA uses a fixed, pre-trained regression model, it may have a computational advantage, but this is not quantified.

### Minor
1. **The regression model choice (LightGBM) is not well justified.** The paper states that "the relationship is most likely non-linear" and that "regression models are highly suitable," but does not compare different regression approaches (e.g., neural network, random forest, linear regression) to justify the choice of LightGBM. An ablation study comparing different regression models would strengthen the paper.

2. **The pseudo-label filtering threshold (≥ 0.8) is somewhat arbitrary.** The paper does not analyze the sensitivity of RTA to this threshold. A lower threshold might include noisier pseudo-labels, while a higher threshold might reduce the diversity of training data. The impact of this choice on the regression mapping quality is not explored.

3. **The paper claims RTA "eliminates complex algorithmic designs required by existing TTA methods," but this is somewhat overstated.** RTA still requires: (a) a separate offline training stage with pseudo-labeling, (b) a regression model training step, and (c) the standard TTA augmentation and ensemble pipeline. While the regression model itself is lightweight, the overall pipeline is not necessarily simpler than methods like Zero, which requires no training at all.

### Minor
1. The paper uses "regression mapping" and "regression model" somewhat interchangeably, but the actual method is a decision tree regressor (LightGBM), not a general regression model. This is fine, but the paper could be more precise about what type of regression is used.
2. The t-SNE visualization (Figure 2) is qualitative and hard to interpret quantitatively. The Spearman correlation analysis (Figure 3) is more informative but only shows correlations for the top 10 features, not the overall predictive power of the full logit vector.
3. The paper claims RTA "eliminates complex algorithmic designs" but the method still requires generating 64 augmented views and running CLIP inference on all of them, which is the same computational bottleneck as other TTA methods.

### Trivial
- The paper has a duplicate entry for "TDA [CVPR 2024]" in Table 4 for ViT-B/16.
- Some figure captions are overly long and contain redundant descriptions.

## Nice-to-Haves
- An ablation study comparing RTA trained on pseudo-labels vs. true labels (on datasets where true labels are available) to quantify the gap between the ideal and practical regression mapping.
- A comparison of different regression models (e.g., neural network, random forest, linear regression) for the mapping function.
- An analysis of the sensitivity to the pseudo-label confidence threshold.
- A runtime comparison with baselines to demonstrate the claimed "negligible additional cost."

## Novel Insights
The paper's key insight—that a regression model can learn to predict view quality (cross-entropy loss) from logits alone, and that this mapping can be learned offline on diverse pseudo-labeled data and transferred to unseen test distributions—is genuinely novel and well-supported by the ceiling TTA experiments. The observation that the logit-loss relationship has a structural correlation that can be captured by a simple regression model is a valuable finding that could inspire further work on learned view selection for TTA. However, the novelty is somewhat tempered by the fact that the regression is trained on pseudo-labels rather than true labels, and the method's transferability to truly arbitrary label spaces is not demonstrated.

## Suggestions
- **Address the pseudo-label gap**: Either (a) train the regression model on true labels for a subset of datasets and compare performance with the pseudo-label version to quantify the gap, or (b) provide a theoretical or empirical analysis of why pseudo-labels are sufficient for learning the regression mapping.
- **Evaluate on tasks with different label spaces**: Test RTA on a scenario where the regression model is trained on one label space (e.g., ImageNet-1k) and applied to a completely different label space (e.g., CIFAR-100, Oxford Pets with different class names) to validate the claim of "arbitrary distributions."
- **Add an ablation on the regression model choice**: Compare LightGBM with at least one alternative (e.g., a simple MLP, random forest) to justify the design choice.
- **Report computational cost**: Include a table comparing the runtime (ms per instance) and FLOPs of RTA vs. baselines to substantiate the "negligible additional cost" claim.

## Score and Decision
The paper presents a novel and well-motivated approach to test-time adaptation for vision-language models, with strong empirical results across a wide range of benchmarks. The core idea of learning a regression mapping from logits to cross-entropy loss is creative and addresses a genuine limitation of entropy-based methods. However, the major weakness regarding the gap between the ideal (true-label loss) and the practical (pseudo-label loss) regression mapping, combined with the limited evidence for transferability to truly arbitrary label spaces, prevents this from being a top-tier contribution. The paper is solid and makes a clear contribution, but these issues need to be addressed for it to be considered a strong accept.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>