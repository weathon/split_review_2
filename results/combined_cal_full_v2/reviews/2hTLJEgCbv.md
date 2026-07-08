## Summary

This paper presents an empirical study of encoder and decoder architectures for Variational Autoencoders on MNIST, systematically varying architecture types (dense vs. convolutional), number of blocks, and latent space size. The goal is to provide architectural guidelines for VAEs distinct from classification-focused designs.

## Strengths

- **The question is genuinely worth asking.** The paper correctly identifies that classification architectures may not be optimal for generative modeling (Section 2.2.2, referencing NVAE), and that the default practice of importing classification architectures into VAEs deserves scrutiny. This motivation is well-grounded.

- **The basic experimental design concept is sensible.** Systematically varying encoder architecture, decoder architecture, and latent size while separating reconstruction loss and KLD in the analysis (Section 4.1) is a reasonable approach for an empirical study of architectural effects.

## Weaknesses

### Fatal

None. While the paper has severe problems, they do not individually invalidate the paper's core claims in the way that a fundamentally flawed methodology or fabricated data would.

### Major

- **Critically underspecified experimental setup.** No training hyperparameters (epochs, batch size, learning rate, optimizer), no architecture sizes (hidden units per dense layer, number of filters per convolutional block), and no training protocol (fixed epochs vs. convergence) are reported. The paper specifies that CNN blocks use 5×5 kernels with stride 2 and LeakyReLU (Section 3, lines 93–101), and that dense layers use matrix multiplication with biases and LeakyReLU — but this leaves the actual model capacities unknown (e.g., "DNN1" could mean 10 hidden units or 1000). No replication or standard deviations are reported. For an empirical study that aims to establish architectural guidelines, the absence of these details makes the results impossible to reproduce or verify. (*Note: this is not a minor nitpick about trivial implementation details — the paper provides essentially no information about how experiments were conducted.*)

- **The "top 25% of models" criterion is undefined.** The paper repeatedly analyzes "the top 25% of models" (Sections 4.1, 4.2, 4.3, Figures 3–7) to draw its central conclusions, but never states what metric is used to rank them. The text says "visual evaluation revealed that the top 25% of models have minimal reconstruction collapse" (Section 4.1, line 111), suggesting either a subjective visual criterion or an unspecified reconstruction-based ranking. This makes the paper's main analytical device unfalsifiable — a reader cannot know how the subset was selected or whether the findings are artifacts of the selection method.

- **Single-dataset evaluation (MNIST) does not support the general claims of the title.** All experiments are conducted on MNIST (line 89), a simple grayscale 28×28 dataset. The title "When Encoders Should Stay Simple" promises general architectural guidelines, but no evidence is provided that these findings transfer to more complex datasets (e.g., CIFAR-10, CelebA). Prior work (NVAE, VD-VAE) has shown that architectural choices become more important on complex data, making it likely that the simple architectures that work on MNIST would fail at higher resolutions.

- **No direct evaluation of generative quality.** The paper's motivation (Sections 1, 2.2.2) centers on improving generative quality, yet the evaluation is limited to reconstruction loss (binary cross-entropy) and KLD. There is no FID, no Inception Score, and not even a single qualitative example of generated samples. The paper uses KLD as a proxy for "generative loss," but KLD is a regularization term, not a measure of sample quality. A paper making claims about generative capability cannot do so without measuring generation directly.

- **The claim that "non-zero KLD is generally beneficial" is a weak/expected finding.** KLD≈0 corresponds to posterior collapse — a well-known failure mode where the latent code carries no information — so such models cannot reconstruct well by definition. Selecting the top-performing models (by reconstruction or visual inspection) mechanically excludes collapsed models, making the finding a selection artifact rather than a novel discovery. This is a known phenomenon extensively documented in the VAE literature (e.g., Bowman et al. 2016, Lucas et al. 2019).

### Minor

- **Central claims about architecture performance are not robustly supported.** (a) "Small dense networks are more effective for encoding": in Figure 5, at L200 (high compression), CNN2 has 5 encoder appearances vs. DNN1's 0 — the relationship reverses at high compression. (b) "Decoding benefits from CNNs with multiple blocks": in Figure 4 (right), CNN4 and DNN1 are tied at 6 appearances each. Without statistical tests, error bars, or error analysis, these count differences are easily within noise, especially given confounding by latent dimension.

- **No comparison to standard VAE baselines.** The paper never establishes what a standard VAE architecture (e.g., the original 2-layer MLP with 500 hidden units from Kingma & Welling 2014) achieves on MNIST, so the reader cannot assess whether any of the studied combinations improves over the basic standard.

- **No analysis of which architectures lead to posterior collapse.** The paper notes that "nearly half the experiments result in collapsed latent spaces" (Section 4.1) but provides no breakdown by architecture type or latent size. Understanding when and why posterior collapse occurs would be a genuine contribution that the paper misses.

- **Figure 1 y-axis reads "ReLU divergence loss"** — clearly a typo for "KL divergence loss."

- **Superficial treatment of the most relevant prior work (NVAE, Section 2.2.2).** NVAE's architectural insights (residual connections, depthwise separable convolutions, batch norm in generative models) are not connected to the experimental design, which uses basic 5×5 convolutions and single-layer dense networks.

### Trivial

None.

## Nice-to-Haves

- Report computational cost (parameter counts, training/inference efficiency) so practitioners can weigh architectural choices.
- Show qualitative generated samples across different architectures to substantiate claims about generative quality.
- Run the same experiment on at least one additional dataset (e.g., Fashion-MNIST, CIFAR-10) to test generality of the findings.

## Removed Points

These points from the harsh critic input are removed with justification:

- **"Framing of VAEs vs. MCMC methods overstates the comparison"** — This is a presentational preference. The paper does discuss DBMs and DGSNs; the framing, while unusual, is not incorrect. Removed as a style criticism not bearing on the paper's core claims.
- **"No discussion of computational cost"** — Moved to Nice-to-Haves. Reasonable to request but not standard for a short empirical study.
- **"No error bars or standard deviations"** — Already subsumed under the underspecified setup weakness. Duplication removed.

## Novel Insights

None beyond the paper's own contributions. The input reviews surface no genuinely novel observation that the paper itself does not already make.

## Suggestions

- **Fully specify the experimental setup.** Provide architecture sizes (hidden units per layer, filter counts per block), all training hyperparameters, and the total number of model combinations tested. This is a prerequisite for the paper to function as an empirical study.
- **Define the "top 25%" ranking criterion explicitly** in the methodology section. If it is based on reconstruction loss, state this directly and acknowledge the implication that the analysis is conditional on reconstruction quality.
- **Add direct generative quality evaluation** (at minimum qualitative generated samples; preferably FID) to support claims about generative improvement.
- **Include at least one additional dataset** to justify the general claims of the title.
- **Add standard deviations or error bars** over multiple runs and report the number of seeds used.
- **Analyze which specific architectures and latent sizes lead to posterior collapse** — this missed opportunity would be a genuine contribution.

## Score and Decision

**Round-1 bracket:** between 1.0 and 3.2, anchored by the ECG VAE paper (avg 2.00, reviews 1,3,1,3). The ECG paper shares key weaknesses (limited evaluation, underspecified methods) but had two datasets and a downstream task; our paper has a better-motivated question and a more sensible study design, yet suffers from an undefined analytical criterion and no generative evaluation at all.

**Weighted-item comparison:** Our strongest negative items ("non-zero KLD weak claim" at -2.18, "top 25% undefined" at -1.04) are less severe than the ECG paper's strongest negatives ("lack of novelty" at -3.96, "no comparison to alternatives" at -4.21). However, our strengths (7.40, 7.95) are somewhat higher. The underspecification issue, while fatal to the paper's utility, carries a weight of only -0.25 — lower than comparable criticisms in the GFlowNet anchor (weight -4.27) — likely because our paper at least reports kernel sizes, strides, and activation functions.

**Final placement:** Score 2.0. The paper asks a good question and designs a reasonable study, but the execution is critically incomplete: the experimental setup is underspecified, the main analytical criterion is undefined, the evaluation covers only one simple dataset with no generative quality metrics, and the central findings are either weak or expected. The paper is a clear reject, though not a "strong reject" (1), because the core idea and design concept are salvageable. To meet publication standard, the paper would need a fully specified, reproducible experimental protocol, evaluation on at least two datasets of differing complexity, direct measurement of generative quality, and statistical analysis of the results.

MY FINAL SCORE: <score>2.0</score>
MY FINAL DECISION: <decision>Reject</decision>