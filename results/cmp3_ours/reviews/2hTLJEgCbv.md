## Summary

This paper presents an empirical study of VAE encoder/decoder architectures on MNIST, varying encoder type (dense vs. convolutional), decoder type, and latent space size, and analyzing which configurations appear in the "top 25%" of models. The main findings are that small dense networks work well for encoding while multi-block CNNs work well for decoding, and that non-zero KLD is beneficial.

## Strengths

- **The question is worthwhile.** Architectural choices for VAEs are genuinely underexplored relative to modifications to the loss function or prior. The paper identifies and motivates this gap (Sections 1, 2.2.2).
- **The experimental design is reasonable in principle.** Jointly varying encoder type, decoder type, and latent size and analyzing which configurations dominate the best-performing set is a plausible high-level approach for an exploratory study.

## Weaknesses

### Fatal

None.

### Major

1. **The "top 25%" ranking criterion is never explicitly defined.** The paper repeatedly uses "top 25% of models" as the basis for all architectural conclusions (Sections 4.1–4.3) but does not state what metric determines this ranking. Section 4.1 mentions "ordered by reconstructive performance (Figure 2)" and "Visual evaluation revealed that the top 25% of models have minimal reconstruction collapse," but this remains ambiguous — it is unclear whether the ranking is by reconstruction loss, ELBO, visual inspection, or some combination. Without this definition, the reader cannot interpret Figures 4–5 or assess whether the selection introduces bias. This is the central analytical instrument of the paper and it is not properly specified.

2. **No quantitative performance metrics are reported.** The paper provides no table of reconstruction losses, ELBO values, FID scores, or estimated marginal log-likelihoods (standard for VAE evaluation). All analysis is conducted through bar charts counting how many models of each architecture type fall into the undefined "top 25%" and qualitative descriptions of latent space scatter plots. For an empirical study whose sole purpose is comparing architectures, the absence of any direct performance numbers prevents readers from assessing whether differences between architectures are meaningful or whether the "best" models are actually good in absolute terms.

3. **The entire study is conducted on a single dataset (MNIST).** The paper states "All experiments are conducted on the MNIST dataset" (line 89) but draws general conclusions about architectural preferences ("small dense networks are more effective for encoding", "decoding benefits from convolutional networks with multiple blocks"). MNIST is a 28×28 grayscale dataset with simple geometric structure. Architectural conclusions from MNIST are well known to often not transfer. An empirical study making architectural recommendations should demonstrate generality across datasets or at minimum acknowledge this limitation prominently.

4. **Architecture specifications are critically underspecified.** The method section (Section 3) states that convolutional blocks use 5×5 kernels with stride 2 and LeakyReLU, and dense layers use matrix multiplication, biases, and LeakyReLU. It does not specify: the number of filters per convolutional block, the hidden dimensions of dense layers, how the encoder outputs mean and log-variance, how the decoder upsamples from latent to image, or the total parameter/FLOP counts. Architectures like "DNN16" appear in Figure 7 without any description in the method section. Without these details, the experiments are not reproducible and the architectural preferences reported cannot be properly interpreted (e.g., capacity differences may confound architectural type).

5. **No training details are provided.** There is no mention of the optimizer, learning rate schedule, batch size, number of epochs, weight initialization, data augmentation, number of random seeds/runs, or early stopping criteria. For an empirical study whose conclusions depend on model training, these are essential for assessing robustness and reproducibility.

6. **Sample sizes in the top-25% analysis are too small to support the claimed conclusions.** From Figure 4, at latent size L25 exactly 1 model is in the top 25%; at L50, 3 models. The paper draws conclusions about encoder/decoder architectural preferences from these counts — e.g., that DNN1 is the best encoder. An analysis based on 1–3 data points per condition cannot support generalizable architectural claims. The bar charts in Figures 4–5 give a misleading sense of statistical weight.

7. **A key conclusion is contradicted by the paper's own data.** The conclusion states "powerful CNNs did not negatively impact encoding performance" (line 135). However, Figure 5 shows that at L25, L50, and L100, DNN1 is the dominant encoder in the top-performing set, while CNN encoders appear almost exclusively at L200. The data show a clear interaction between latent size and architecture that the paper does not discuss, and the claimed conclusion is at best only supported at the largest latent size. Moreover, the finding that "non-zero KLD loss is generally beneficial" (line 135) is a known property of VAEs — models with collapsed KLD have learned no useful latent representation — and does not require this experiment to establish.

### Minor

- The NVAE discussion (Section 2.2.2) correctly notes that architecture matters for generative modeling, but the architectures tested here (single-layer DNNs, basic CNNs) are far removed from NVAE's deep hierarchical design with residual connections and spectral normalization. The connection drawn is superficial.
- The presentation would benefit from showing full distributions of performance across all configurations rather than only reporting counts filtered to the top 25%.

### Trivial

None.

## Nice-to-Haves

- Report performance (ELBO, reconstruction loss, KLD) for every model configuration in a table so readers can directly compare architectures quantitatively.
- Include a comparison to the standard VAE architecture from Kingma & Welling 2014 as a baseline.
- Add at least one additional dataset (e.g., Fashion-MNIST, CIFAR-10) to test whether observed preferences generalize.
- Run experiments with multiple random seeds to characterize variance across runs.
- Control for parameter count across architectures to separate architectural type from model capacity.

## Removed Points

The following points from the input review were removed for the stated reasons:

1. **"DNN1, DNN4, CNN1, CNN2, CNN4, CNN5" naming never explained**: This is incorrect — the paper's naming convention IS defined (line 99: "L{latent size}.{Encode architecture}{number of layers}.{Decoder architecture}{number of layers}"). DNN1 = dense 1-layer, CNN4 = conv 4-block, etc. The valid criticism (kept in Major #4) is that the *internal details* of these blocks — number of filters, hidden units — are not specified.

2. **Figure 2 axis confusion**: The reviewer claimed the "grey shaded area" referencing value ~0.00012 is ambiguous about which axis it belongs to. This is a presentation issue that may partially stem from parser artifacts in figure captions. It is not a substantive weakness.

3. **"The paper is not reproducible" as a separate criticism**: This is a consequence of the underspecified architectures and missing training details, already covered in Major #4 and #5.

4. **Missing comparison to standard VAE baseline (Kingma & Welling 2014)**: The paper is internally comparative (comparing its own architectural variants against each other), so this is a nice-to-have, not a core weakness.

5. **Lack of parameter-matched controls**: This is a nice-to-have improvement, not a core flaw, since the paper does not claim to isolate capacity from architecture.

## Novel Insights

None beyond the paper's own contribution. The review surfaces no insight that the paper itself does not already attempt to state, and the paper's claimed findings are either weakly supported or already known.

## Suggestions

1. Most critically, define the ranking criterion used to determine "top 25%" of models and provide a table of quantitative performance metrics (ELBO, reconstruction loss, KLD) for every configuration tested.
2. Fully specify all architectures: number of filters per convolutional block, hidden dimensions of dense layers, encoder output mechanism, decoder upsampling approach, and parameter counts.
3. Provide complete training details: optimizer, learning rate, batch size, epochs, random seeds, number of independent runs.
4. Add at least one additional dataset to test generality of the findings.
5. Discuss the interaction between latent size and architecture preferences that is evident in Figure 5 but not addressed in the current analysis.
6. Reframe the known result about non-zero KLD as a validation check rather than a novel finding.

## Calibration Report

The following anchor papers from the human-review corpus were used for calibration:

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| KARA autoencoder (OBrTQcX2Hm) | 2.00 (3,1,1,3) | Bracket | Similar quality — limited scope, missing details, MNIST-only experiments; our paper has no novel method |
| CNN VAE ECG (v3XabZsB7j) | 2.00 (1,3,1,3) | Narrow | Similar quality — limited empirical study of VAE architectures; our paper is slightly better structured |
| DeepKDE (cSd8Eom8Zt) | 2.33 (3,1,3) | Narrow | Slightly stronger — has a well-defined method proposal despite limited scope |
| VideoDiT (lvgsPjRtLM) | 2.50 (3,1,3,3) | Narrow | Slightly stronger — proposes a concrete method adaptation despite flaws |
| Enhancing Robustness (zeeLxGw5pp) | 3.20 (8,1,1,5,1) | Bracket | Mixed reviews; has a well-defined claim and some empirical support — stronger than our paper |
| Sample what you can't compress (vK8C37eHXM) | 3.20 (6,3,1,3,3) | Bracket | Proposes a novel method with a clear hypothesis — stronger than our paper |
| Sparsity of high-dim spaces (4xEACJ2fFn) | 4.80 (3,3,6,6,6) | Bracket | Has a specific hypothesis and some theoretical grounding — substantially stronger |
| VAE architecture accept-range papers (6.25-8.00) | 6.25-8.00 | Bracket | Propose novel methods or theoretical contributions with rigorous experiments — far above our paper |

**Round 1 bracket**: 1.5–3.0  
**Narrowing**: After comparing with score-2.0 anchors (KARA, CNN VAE ECG) which share similar issues of narrow scope and missing details, the paper sits firmly in the 2.0 range. It is a complete, readable paper with a worthwhile question, but the execution has fundamental methodological gaps — no defined ranking criterion, no quantitative results table, single dataset, underspecified architectures, and missing training details — that prevent it from meeting publication standards. It is not a "strong reject" (1) because it is complete and coherent; it is clearly a "reject" (2–3).

## Score and Decision

MY FINAL SCORE: <score>2.0</score>
MY FINAL DECISION: <decision>Reject</decision>