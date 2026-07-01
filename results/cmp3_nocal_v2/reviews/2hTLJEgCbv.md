## Summary

This paper presents an empirical study of encoder and decoder architecture choices (dense vs. convolutional networks, varying depth) for VAEs on MNIST with latent dimensions 25–200. It reports observations about which architecture combinations appear in the "top 25%" of models, concluding that small dense encoders and convolutional decoders work well. The paper does not propose a new method.

## Strengths

- **The research question is well-motivated.** The observation (drawn from NVAE, Section 2.2.2) that architectures optimized for classification may not be suitable for generative modeling is genuine, and a systematic study of basic architectural choices for VAEs could be useful. The paper correctly scopes its investigation as separate from improvements to variational inference itself (Section 1, final paragraph).

- **The factorial design (encoder type × decoder type × latent size) is the right starting structure** for this kind of empirical study, even if the paper does not fully execute the analysis.

## Weaknesses

### Fatal

1. **The "top 25%" selection criterion is never defined, rendering the central analysis uninterpretable.** The paper builds all of its main conclusions on models that fall in the "top 25%" (Figures 3–7), but "Visual evaluation revealed that the top 25% of models have minimal reconstruction collapse" (Section 4.1, line 111) is the only description of how these models were selected. It is unclear whether the ranking is by reconstruction loss, ELBO, KLD, a composite, or visual inspection. Without a defined, reproducible criterion, the counts in Figures 4 and 5 cannot be meaningfully interpreted, and none of the architecture conclusions that follow from them can be evaluated.

2. **No numerical performance tables are reported.** The paper presents only plots (loss curves, scatter plots, bar charts of architecture counts) and no table of actual performance numbers — no ELBO values, no reconstruction errors with standard deviations, no KLD values, no FID or other generative quality metric. For an empirical study that aims to compare architectures, this is a decisive gap: a reader cannot assess the magnitude of differences, cannot compare across configurations, and cannot verify the reported trends quantitatively. The claim that "a negative trend is observed in the generative inference loss when compared to reconstructive performance" (line 111) is stated without any quantitative summary (correlation coefficient, effect size, or error bars).

### Major

3. **Critical architecture details are missing, preventing capacity comparisons.** The paper specifies that DNN1 = 1 dense layer, CNN4 = 4 conv layers, etc. (Figure 1 caption, line 99), but never states the number of hidden units per dense layer or the number of filters per convolutional block. Without these, it is impossible to compare capacity across architectures. For example, "DNN1" could range from 10 to 1000+ hidden units, and "CNN2" could range from a few to hundreds of filters. The total number of configurations tested is also never reported, which means the base rate of each architecture type in the experimental design is unknown — a critical omission when drawing conclusions from counts of "top-performing" models (Figures 4, 5).

4. **Training hyperparameters and data handling are entirely unspecified.** The paper does not state the optimizer, learning rate, batch size, number of epochs, learning rate schedule, regularization (if any), train/validation/test split, or whether MNIST pixels were binarized or kept continuous. This level of underspecification makes the experiments unreproducible even in principle.

5. **The headline claims are not supported by controlled comparisons.** 
   - "Small dense networks are more effective for encoding" (Abstract, Conclusion) is supported only by a bar chart showing counts of DNN1 among top-performing models (Figure 4). Without controlling for parameter count or fixing the decoder, this does not establish that DNN1 *causes* better encoding. The bar charts conflate encoder effects with decoder effects and latent size effects.
   - "CNNs did not negatively impact encoding performance" (Conclusion, line 135) appears without any experiment that isolates encoder variation while holding the decoder fixed.
   - "Non-zero KLD loss outperforms collapsed latent space models" is presented as a finding but is well-established in the VAE literature (posterior collapse, discussed since Bowman et al. 2016 and cited by the paper itself in Section 1). This is a sanity check, not a novel insight, and framing it as a key result overstates its contribution.

### Minor

6. **Only MNIST is evaluated.** The paper acknowledges this (Section 3, line 89) but draws broad conclusions ("When Encoders Should Stay Simple") from a single small grayscale dataset. The generality of the findings to higher-resolution or more complex data is not discussed.

7. **The latent space analysis (Figures 6, 7) relies on visual inspection of PCA projections.** The paper assesses "separability" qualitatively without any quantitative metric (e.g., silhouette score, adjusted mutual information). This weakens the claims about compression and representation quality.

8. **Inconsistent and non-standard terminology.** Figure 1 labels the y-axis "ReLU divergence loss" — a non-standard term that appears to refer to KL divergence — while Figure 2 uses "KLD (log scale)" and "generative inference loss" for what seems to be the same quantity. The naming convention for model labels also shifts between figures (dots in Figure 1, underscores in Figure 2), creating unnecessary confusion.

### Trivial

None.

## Nice-to-Haves

- A single comprehensive table showing reconstruction error, KLD, and ELBO for each (encoder, decoder, latent_dim) configuration with means and standard deviations would instantly make the paper's claims evaluable.
- Reporting base rates (how many configurations of each architecture type were tested) is necessary to interpret the bar charts in Figures 4 and 5.
- Including a controlled experiment where the decoder and latent size are fixed and only the encoder varies would directly test whether encoder architecture independently affects performance.
- Engaging more concretely with prior work on VAE architectures (e.g., NVAE, ResNet VAEs, β-VAE) rather than treating the field as a blank slate would improve framing.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"DNN16 — 16 layers? 16 neurons?"**: The paper's naming convention (Figure 1 caption, line 99) explicitly defines the number after the architecture type as the number of layers. This part of the criticism is factually incorrect.
- **"Naming convention changes across figures (dots vs. underscores)"**: This is a formatting/presentation nitpick that does not affect the paper's scientific content.
- **"The paper would benefit from engaging more concretely with what prior work has and has not established"**: This is a reasonable suggestion but moves beyond weakness into optional improvement territory.
- **Criticisms about missing appendix content**: The paper's appendix section is empty, but the parser strips supplementary material; the original submission may contain additional details.

## Novel Insights

None beyond the paper's own contributions. The reviewer observations largely confirm the paper's limitations rather than providing unexpected analytical perspectives. The key insight from the review process is that the paper's empirical claims cannot be evaluated because the selection criterion for the "top 25%" analysis is undefined — this is a structural flaw that the paper's own content makes verifiable.

## Suggestions

- Define the ranking metric used to select the "top 25%" of models, and report the threshold values. Show that conclusions are robust to different cutoff choices.
- Add a full table of numerical results (ELBO, reconstruction loss, KLD) for all (encoder, decoder, latent_dim) configurations with standard deviations across multiple seeds.
- Specify all architecture details: number of units per dense layer, number of filters per convolutional block.
- Report all training hyperparameters and data preprocessing steps.
- Include at least one additional dataset beyond MNIST, or explicitly limit the scope of conclusions.
- Add controlled experiments that isolate encoder and decoder effects independently.
- Replace non-standard terminology ("ReLU divergence loss") with standard terms.

## Score and Decision

The paper addresses a reasonable question but the empirical analysis has a decisive structural flaw: the "top 25%" selection criterion is undefined, making the central results uninterpretable. Combined with the absence of numerical performance tables, missing architecture specifications, and unsupported headline claims, the paper cannot support its conclusions in its current form. Even substantial revision would require rebuilding the empirical evaluation from the ground up with proper specifications, controlled comparisons, and numerical reporting.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>