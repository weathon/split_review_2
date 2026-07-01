## Summary

This paper empirically varies encoder and decoder architectures (dense vs. convolutional, varying depth) and latent space sizes for VAEs on MNIST, then examines which configurations yield low reconstruction loss and non-zero KL divergence. It claims that small dense networks are more effective for encoding while deeper convolutional networks benefit decoding, and that non-zero KL divergence is beneficial. The question is worthwhile but the execution is severely compromised: the method section lacks basic reproducibility specifications, the quantitative evidence consists of tiny counts (0–5 per cell), the key analytical criterion ("top 25%") is never defined, and all experiments use only MNIST.

---

## Strengths

- **The question is worth asking.** Architectural choices for VAE encoders/decoders are indeed undertreated relative to work on priors, posteriors, and bounds. A careful empirical study would be valuable.
- **The combinatorial experimental design is sensible in principle.** Varying architectures systematically while holding the dataset and loss function fixed is the right starting template.

---

## Weaknesses

### Fatal

None. The paper's claims are not invalidated by a single fatal methodological error; rather, they are unsupported by a combination of major evidentiary gaps.

### Major

- **Method section critically underspecified; experiments are not reproducible.** Section 3 (~15 lines) omits: learning rate, optimizer, scheduler, batch size, number of epochs, train/val/test split of MNIST, number of independent trials, and random seeds. Crucially, the architecture variants DNN1–DNN16 and CNN1–CNN5 are never defined — the paper only describes a single convolutional block ("kernel size 5×5, stride 2, LeakyReLU") and a single dense layer, but not how capacity scales across variants, how many filters or hidden units each uses, or what distinguishes CNN2 from CNN4. An empirical study whose sole contribution is empirical observations must be reproducible; this paper is not. *(Verifiable from Section 3, lines 83–101.)*

- **Quantitative evidence is extremely thin; conclusions drawn from counts of 0–5.** The paper's central claims about which architectures perform best are supported by Figure 5, where each cell is a count of "top-performing" models ranging from 0.0 to 5.0. Many cells are 0.0 (e.g., DNN1 encoder count at L200 = 0.0; CNN3 encoder at all latent sizes = 0.0; DNN1 decoder at L200 = 0.0). The paper's stated finding that "small dense networks are more effective for encoding" is contradicted at the largest latent space (L200), where DNN1 has 0 top-performing entries while CNN2 has 5 and CNN4 has 2 — a nuance the paper does not discuss. At L25, only 1 model total qualifies as top-performing. These sample sizes cannot support the confident architectural recommendations in the abstract and conclusion. *(Verifiable from Figure 5 tables, lines 167–185; abstract lines 10–12; conclusion lines 135–136.)*

- **"Top 25%" selection criterion is never defined.** The paper repeatedly refers to the "top 25% of models" (lines 111, 115, 131) but never specifies by which metric this subset is selected — total ELBO? reconstruction loss alone? a composite threshold? The criterion is also inconsistently applied: the analysis discards the bottom 75% of models, but the paper previously notes that "nearly half" of all models have collapsed latent spaces (line 107), meaning the top 25% threshold is entirely arbitrary with no justification given. It is impossible to verify whether the conclusions are sensitive to this choice. *(Verifiable from lines 107, 111, 115; no definition provided anywhere in the paper.)*

- **Only tested on MNIST; claims are stated as general architectural principles.** All experiments use MNIST (line 89), a simple 28×28 grayscale dataset. The abstract and conclusion make unqualified claims ("small dense networks are more effective for encoding," "decoding benefits from convolutional networks with multiple blocks") that may simply reflect MNIST's simplicity — even a single dense layer can encode its digits. The paper does not acknowledge this as a limitation in its conclusions. *(Verifiable from line 89; abstract lines 10–12; conclusion lines 135–136.)*

### Minor

- **PCA-based latent space analysis is purely qualitative.** Figures 6–7 are presented with statements such as "higher compression levels degrade the quality of the latent space" and "maintain separability at moderate compression" (lines 131–132). No quantitative metric (silhouette score, mutual information, clustering accuracy) is reported. These are visual judgments with no statistical backing. *(Verifiable from lines 131–132, Figures 6–7.)*

- **The claim that non-zero KLD is beneficial is already well-established.** Posterior collapse (KLD = 0) is a known failure mode of VAEs, extensively documented in prior work (e.g., Bowman et al. 2016, Alemi et al. 2018). Framing this as a finding of the study overstates its novelty.

- **Figure axis labeled "ReLU divergence loss" — non-standard terminology.** The figure caption (lines 95, 97) uses "ReLU divergence loss" where the standard term is KL divergence. This is not a parser artifact; it appears in the caption content itself and would confuse readers.

- **No generated samples shown despite generative framing.** The introduction motivates the work by discussing generation quality and blurry outputs from VAEs, but the experiments never show any generated samples (only reconstructions) and report no generative quality metric. The framing and evidence are mismatched. *(Verifiable from lines 21–35 vs. results section which shows only loss curves, PCA plots, and architecture counts.)*

### Trivial

None.

---

## Nice-to-Haves

- Provide a supplemental experiment on at least one additional dataset (e.g., CIFAR-10, SVHN, or a non-image dataset) to test whether the architectural conclusions generalize beyond MNIST.
- Include a standard convolutional VAE baseline (e.g., from Kingma & Welling 2014) for comparison.
- Report results with multiple random seeds and include variance/standard deviations.

---

## Removed Points

These points are flagged to be removed per filtering rules; treat them with caution.

1. *"The paper needs a Limitations section."* — This is a suggestion about presentation, not a specific identified flaw. The weakness about single-dataset scope (retained above) covers the substance.
2. *"Figures captions are repeated multiple times."* — The repetition is a PDF-parsing artifact, not a paper error. Removed per formatting-artifact rule.
3. *"No comparison to standard VAE baselines."* — This is a scope suggestion, not a flaw in the paper's own experimental design. Moved to Nice-to-Haves.
4. *"The VAE derivation (2.1) is textbook material and adds no value."* — Many papers include background sections; this is a presentation preference, not a substantive weakness.
5. *"The paper does not acknowledge this limitation except implicitly by only mentioning MNIST in Section 3."* — Redundant with the already-retained single-dataset weakness.
6. *"The method section spans roughly 15 lines of text"* — The brevity is a framing observation; the substantive point (missing specifications) is already captured in the first Major weakness.
7. *"Several figure descriptions contain text that appears to be from the original caption plus an automated description"* — Parser artifact. Removed.
8. *"The paper should not be accepted in its current form... too modest for a venue like ICLR."* — This is an overall judgment, not a specific weakness. The specific flaws above justify the recommendation.

---

## Novel Insights

None beyond the paper's own contributions. The review surfaces that the headline claims are contradicted by the paper's own data at the largest latent space (DNN1 encoder = 0 top-performing entries at L200), a tension the paper never addresses. This is a finding *about* the paper's analysis quality, not a novel scientific insight.

---

## Suggestions

1. Fully specify all architecture variants (DNN1–DNN16, CNN1–CNN5) in a table with layer-by-layer specifications for filters, hidden units, and number of layers.
2. Report all training hyperparameters (optimizer, learning rate, batch size, epochs, data split) and run each configuration with multiple seeds reporting mean and std.
3. Define the "top 25%" selection criterion transparently and justify the threshold choice; test sensitivity to this threshold.
4. Report tabulated ELBO, reconstruction loss, and KL divergence values alongside the figure visualizations.
5. Add at minimum one additional dataset to test generalization.
6. Clarify that "ReLU divergence loss" in Figure 1 is a mislabeling of KL divergence.

---

## Score and Decision

This paper addresses a reasonable question but the execution is not publication-ready. The method is unreproducible, the quantitative evidence is too thin to support the claims (counts of 0–5), the key analytical criterion is undefined, and all experiments use a single simple dataset. These are not minor presentation issues — they are fundamental evidentiary gaps that prevent the paper from meeting the standards of a rigorous empirical study.

**Score: 3 (Reject)**

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>