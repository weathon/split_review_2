## Summary

This paper presents an empirical study investigating how encoder and decoder architectural choices (dense vs. convolutional networks, varying depths) affect Variational Autoencoder (VAE) performance on the MNIST dataset. The authors systematically vary latent space sizes and architecture combinations, analyzing reconstruction loss, KL divergence, and latent space projections. The main findings are that simple dense encoders perform best, while decoders benefit from deeper convolutional architectures, and that non-zero KL divergence is beneficial for representation quality.

## Strengths

- **Timely and relevant research question**: The paper addresses an underexplored aspect of VAE design—the impact of encoder/decoder architecture on latent representations—which is practically important for practitioners building VAEs.
- **Systematic experimental design**: The authors vary both encoder and decoder architectures independently across multiple latent space sizes, creating a comprehensive grid of configurations (25 combinations × 4 latent sizes = 100 experiments).
- **Clear, actionable findings**: The conclusion that "small dense networks are more effective for encoding, while decoding benefits from architectures with structural processing capabilities" is a concrete, practically useful insight that could guide architecture selection.

## Weaknesses

### Fatal
None.

### Major

1. **Limited evaluation metrics and no quantitative comparison**: The paper relies entirely on loss values (reconstruction BCE and KL divergence) and qualitative visual inspection of latent space projections. There are no standard generative quality metrics (FID, IS, NLL), no quantitative measures of representation quality (e.g., classification accuracy on latent codes, mutual information estimation), and no statistical significance tests. The "top 25%" and "top 50%" thresholds are arbitrary and not justified.

2. **Single dataset (MNIST) severely limits generalizability**: MNIST is a simple, low-resolution, grayscale dataset. The findings may not transfer to more complex datasets (CIFAR, ImageNet, CelebA) where architectural choices matter more. The paper's title and abstract claim general insights about "when encoders should stay simple," but the evidence only supports conclusions for MNIST.

3. **No comparison to established baselines or prior work**: The paper does not compare its best architectures against standard VAE baselines (e.g., the original VAE architecture from Kingma & Welling, or the NVAE architecture discussed in related work). Without baselines, it's impossible to know whether the findings represent genuine improvements or are specific to the authors' particular implementation choices.

4. **Incomplete reporting of experimental details**: The paper does not specify training hyperparameters (learning rate, optimizer, batch size, number of epochs, weight initialization, number of random seeds). The number of runs per configuration is not stated, making it impossible to assess result variability or statistical significance.

### Minor

1. **The "top 25%" analysis is potentially misleading**: Selecting the top 25% of models by reconstruction loss and then analyzing their architecture distribution introduces selection bias. A model with a simple encoder might appear in the top 25% simply because it has a powerful decoder, not because the encoder is inherently better. A more rigorous approach would be to control for decoder capacity when comparing encoders.

2. **Figure quality and readability**: Figures 1-7 are described in captions but the actual images are not visible in the provided text. The table representations of Figure 4 and 5 data are helpful but the bar charts themselves are missing. The axis labels in the text descriptions are sometimes unclear (e.g., "ReLU divergence loss" in Figure 1 caption is likely a typo for "KL divergence loss").

3. **Limited architectural variation**: The paper only tests DNNs with 1-16 layers and CNNs with 1-5 convolutional blocks. Modern VAE architectures use residual connections, batch normalization, attention mechanisms, and hierarchical latent spaces. The study does not explore these more relevant architectural choices.

### Trivial

- The paper uses "ReLU divergence loss" in Figure 1 caption, which appears to be a typo for "KL divergence loss."
- The grammar notation for model labels (e.g., "L25_DNN1_DNN1") is explained but could be clearer in the main text.

## Nice-to-Haves

- Include standard generative quality metrics (FID, IS) to complement loss-based evaluation.
- Add experiments on at least one more complex dataset (e.g., CIFAR-10 or CelebA) to test generalizability.
- Report results with multiple random seeds and include error bars or confidence intervals.
- Compare against a standard VAE baseline architecture from the literature.

## Novel Insights

None beyond the paper's own contributions. The finding that simple encoders and complex decoders work well is consistent with the DGSN insight cited in the paper (Section 2.2.1) and with the general principle that the decoder bears more of the generative burden. The paper's main value is in providing empirical confirmation of this principle in a controlled VAE setting, rather than introducing a fundamentally new insight.

## Suggestions

1. Add quantitative evaluation metrics (FID, IS, or at minimum, classification accuracy on latent representations) to support the qualitative claims about representation quality.
2. Run experiments on at least one additional dataset (e.g., Fashion-MNIST or CIFAR-10) to assess generalizability.
3. Include standard VAE baselines (e.g., the original VAE architecture from Kingma & Welling, 2014) for comparison.
4. Report all hyperparameters and run each configuration with at least 3 random seeds to assess variability.
5. Clarify the selection criteria for "top 25%" and "top 50%" and consider using more rigorous statistical methods (e.g., ANOVA or Bayesian hierarchical models) to compare architecture families.

## Score and Decision

The paper addresses a relevant and practical question with a systematic experimental design. However, the evaluation is limited to loss values on a single simple dataset without standard generative quality metrics, baselines, or statistical rigor. The findings are plausible but not sufficiently supported to warrant acceptance at a top venue. The paper would benefit from additional experiments, metrics, and baselines before being suitable for publication.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>