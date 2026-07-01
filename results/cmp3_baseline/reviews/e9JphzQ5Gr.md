## Summary
This paper identifies and theoretically characterizes an inherent label-dependency in semi-supervised learning (SSL)—the accuracy of pseudo labels and thus the utility of unlabeled data degrade sharply when labeled data is scarce or of low quality. To break this dependency, the authors propose CaPT, a portable asymmetric-modalities co-training framework that integrates a parameter-efficiently fine-tuned CLIP with a fully fine-tuned unimodal network. Co-pseudo labels generated from both branches via entropy-based weighting guide training, enabling reliable prior knowledge from CLIP to supplement weak labeled supervision. Extensive experiments show state-of-the-art results on multiple SSL benchmarks, especially under extreme label scarcity (e.g., one label per class), with modest computational overhead.

## Strengths
- **Novel and principled framework**: CaPT provides a clean and well-motivated way to incorporate vision-language models (VLMs) into SSL, breaking the traditional reliance on labeled data by exploiting CLIP’s zero-shot prior while maintaining efficiency through adapter tuning and feature-level augmentation.
- **Strong empirical performance**: The method achieves substantial improvements over existing SSL methods across a wide range of datasets and label-scarce settings—e.g., +21.38% on CIFAR-100 and +4.05% on EuroSAT with one label per class, and +9.33% on ImageNet with 10 labels per class. The gains are consistent and often large.
- **Theoretical grounding**: The paper provides a formal bound (Theorem 1.1) that connects pseudo label error to label quantity and quality, offering a theoretical explanation for SSL’s label dependency and motivating the proposed approach.
- **Careful ablation and analysis**: The ablation study (Table 6) systematically validates the contributions of each component (asymmetric co-training, adapter tuning, feature augmentation, entropy weighting), and Figure 5 demonstrates how adapter tuning mitigates CLIP’s class bias. The attention map visualization (Figure 3) supports the claim that cross-modal models provide more diverse representations.
- **Efficiency**: CaPT adds only 8% memory and 11% training time over a baseline SSL method (FreeMatch), making it practical despite involving a large VLM.

## Weaknesses
### Fatal
None.

### Major
- **Limited improvement on fine-grained datasets with weak CLIP prior**: On FGVCAircraft, CaPT does not outperform FreeMatch or RegMixMatch (Table 5). While the authors acknowledge this, it reveals that the framework’s success depends on the quality of CLIP’s prior for the target domain. This limits the generality of the “breaking label dependency” claim to domains where CLIP already has reasonable zero-shot capability.
- **Comparison fairness regarding pretrained models**: Standard SSL baselines in USB use a supervised ImageNet-pretrained ViT, while CaPT additionally leverages CLIP (trained on 400M image-text pairs). Although the authors ablate to show that CLIP alone (CaPT-Ada) is insufficient, the best-performing baselines (e.g., RegMixMatch) may not have had access to similarly massive pretraining. This makes the primary advantage not solely the co-training framework but also the richer prior.

### Minor
- The theoretical bound (Theorem 1.1) is derived under a prototype-based Gaussian-mixture generative model and is used mostly for motivation. The connection to the actual deep SSL setting is plausible but not rigorous, and the bound is not employed algorithmically.
- The paper claims to “break the label dependency”, but the method still uses labeled data for adapter tuning and full fine-tuning of the unimodal network. The dependency is reduced rather than eliminated; the title is slightly overstated.
- On the STL-10 dataset (Table 1), the improvement at 10 labels per class is smaller (+3.44% over RegMixMatch) than at 4 labels (+6.18%), suggesting diminishing returns as labeled data increases—this is expected but not discussed.

### Trivial
None.

## Nice-to-Haves
- Provide an analysis of how the co-training evolves: when does the unimodal network become the dominant supervisor? A plot of the entropy weights over training would be illuminating.
- Include results on a dataset where CLIP’s prior is poor (e.g., medical images) to better understand the robustness of the framework.

## Novel Insights
Beyond the paper’s own contributions, the key novel insight is that **the efficacy of co-training in SSL depends not only on the independence of the views but also on the **modality gap** between them**. The paper demonstrates that two unimodal vision models (even with different initializations) produce similar attention patterns, limiting information exchange, whereas pairing a vision model with a vision-language model yields genuinely complementary representations, leading to a richer mutual learning signal. This insight has implications for designing future co-training and knowledge distillation methods that leverage cross-modality.

## Suggestions
- Include results on a domain where CLIP performs poorly (e.g., satellite imagery from a different sensor or medical pathology) to test whether the co-training mechanism can still provide benefits when the prior is weak.
- Provide an analysis of the entropy-based weighting over time to show when and why the unimodal network’s weight overtakes CLIP’s.
- Discuss potential negative societal impacts: CLIP is known to encode biases from web data; adapter tuning may partially correct this (as shown in Figure 5), but a broader discussion would strengthen the paper.

## Score and Decision
MY FINAL SCORE: <score>9</score>
MY FINAL DECISION: <decision>Accept</decision>