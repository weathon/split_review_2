## Summary

This paper introduces Spherical Watermark, an encryption-free watermarking framework for diffusion models that maps binary watermarks to Gaussian noise through three reversible modules: binary embedding (mixing watermark bits with random padding), spherical mapping (projecting onto the unit sphere, rotating, and scaling by a chi-square radius), and diffusion integration. The method eliminates per-image key storage required by Gaussian Shading and avoids the cryptographic overhead of PRC, while achieving strong empirical fidelity, undetectability, and robustness.

## Strengths

- **A clean, encryption-free design that eliminates per-image key management.** The core idea — mapping watermark bits to unit-sphere points via binary embedding, then rotating and scaling by a chi-square radius — is elegant and simpler than the stream-cipher machinery of Gaussian Shading or the belief-propagation decoding of PRC. The practical advantage of avoiding key storage per generated image is real and well-motivated.

- **Empirically solid fidelity and undetectability.** Table 1 shows FID values (e.g., 48.12 on COCO/SD v1.5) essentially indistinguishable from the original (48.13), notably better than Tree-Ring, Gaussian Shading, and frequency-domain methods. Only PRC Watermark is competitive on FID. The undetectability classifiers remain near 50% accuracy for the proposed method, supporting the claim that the watermarked distribution is hard to distinguish from the original.

- **Comprehensive ablation study.** The paper ablates the binary embedding module, spherical mapping module (Figure 6b,c), hyperparameters s, N, l_m, l_p (Table 3, Figure 6d), ODE solver choice (Table 4), and generation/inversion timesteps (Table 5), providing useful insight into which design choices matter.

- **Strong robustness under adversarial attacks.** Table 2 shows that lossless methods (including this one) dramatically outperform lossy methods under WEvade adversarial attacks, where DwtDct, RivaGAN, and Tree-Ring collapse to near-chance TPR. The paper correctly attributes this to the fact that lossless embeddings cannot be learned by a surrogate classifier.

## Weaknesses

### Fatal
None.

### Major

- **The theoretical guarantee is overstated relative to what is actually proven.** The argument chain shows that the watermarked noise is a spherical 3-design scaled by a chi-square radius. Lemma 3.4 requires a *uniformly distributed* point on the sphere to yield N(0,I), but a 3-design matches the uniform distribution only through degree-3 moments — not the full distribution. The abstract says "recover exact multivariate Gaussian noise" (line 9) and the conclusion says "provably and empirically indistinguishable" (line 336), both without the 3-design caveat. To the paper's credit, the limitations section (line 332) acknowledges that "higher-order moments may deviate," and the abstract also accurately states "preserves the target prior up to third-order moments." Nevertheless, the main framing (title, abstract, conclusion) overclaims what the theory supports. This is not fatal — the empirical evidence is strong — but it needs correcting.

### Minor

- **Figure 2 caption does not match the text.** The caption (lines 217-221) describes plots comparing only "True Ring" (parser artifact for Tree-Ring) and "PRC watermark," but the text (lines 235, 254) discusses results for Tree-Ring, Gaussian Shading, PRC Watermark, and Ours. This creates a discrepancy between what the caption describes and what the text references. The authors should clarify what Figure 2 actually shows and ensure the caption matches.

- **The Gaussian Shading comparison uses that method in a deliberately weakened configuration.** The paper transparently notes that "with fixed keys, Gaussian Shading no longer achieves true losslessness" (line 193) and reports it as 97% detectable. However, with proper per-image keys, Gaussian Shading is provably undetectable. The paper should more clearly separate the two comparison axes: (a) undetectability (where Gaussian Shading with proper keys is on par) vs. (b) key-management overhead (where the proposed method wins). The current framing conflates them.

- **The paper does not analyze the security implications of using a fixed secret signature K = (T, C).** If an adversary obtains K (e.g., by reverse-engineering the API), they could remove watermarks from generated images or forge watermarks in arbitrary images. In contrast, Gaussian Shading and PRC use per-image keys that limit the damage from a single key leak. This trade-off should be explicitly discussed.

### Trivial

- The acronyms "REC ACC" and "DNR ACC" in Figure 5's caption are never defined in the main text.

## Nice-to-Haves

- The computational efficiency comparison (Figure 4) measures only the transform step, excluding diffusion. For a 50-step pipeline, the extraction time advantage (0.0003s vs. 10s) is dominated by the diffusion inversion step in both cases. Acknowledging this framing more explicitly would strengthen the presentation.

- Adding a direct statistical test (e.g., MMD or moment-based tests) comparing watermarked to unwatermarked latent distributions would further strengthen the empirical undetectability claim beyond the indirect FID and classifier metrics.

## Removed Points

These points from the input review were removed with justification:
- "PRC 'fails under strong attacks' is not a specific criticism" — REMOVED: nitpick, paper's description of PRC limitations is accurate.
- "Variable name 'r' reused for padding and radius" — REMOVED: trivial presentation nitpick.
- "Lemma 3.3 convergence claim without proof" — REMOVED: appendix is stripped by parser, proof may be in appendix.
- "Small standard deviations in Table 2" — REMOVED: ceiling effects explain near-zero std for near-100% values.
- "Limitations not mentioning 3-design gap" — REMOVED: limitations do mention higher-order moment deviation.
- "Rounding operation loses information (99.99% not 100%)" — REMOVED: paper is transparent about 99.99% accuracy.
- "No MMD/chi-square tests" — REMOVED: moved to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Reframe the theoretical claim in the abstract and conclusion as "moment matching up to third order" and "empirically indistinguishable" rather than "provably indistinguishable from standard Gaussian." The empirical evidence already speaks for itself.
- Clarify Figure 2's caption to match what the figure actually shows (all methods discussed in the text).
- Separate the undetectability and key-management aspects of the Gaussian Shading comparison more clearly.
- Add a discussion of the security implications of the fixed secret signature K.
- Define "REC ACC" and "DNR ACC" in the main text.

## Score and Decision

**Round 1 bracket**: I identified that this paper's closest competitor/ancestor paper, "An undetectable watermark for generative image models" (PRC, jlhBFm7T2J.md, avg 6.50), received strong positive weights for theoretical guarantees (+7.85) but strong negative weights for image quality degradation (-6.98, -6.21) and unconvincing undetectability (-4.58). The current paper has the opposite profile: strong positive weights for fidelity (+5.84), robust design (+4.58), ablation completeness (+5.39), and adversarial robustness (+4.45), while its single notable negative weight is the theoretical overclaim (-0.59, mild). Compared to the PRC anchor, this paper swaps better empirical evidence for a slightly weaker theoretical story. Compared to "Shallow Diffuse" (1IwoEFyErz.md, avg 6.00), the current paper has stronger empirical comparisons and a more practical contribution but shares some theoretical-precision concerns.

**Final score**: The paper's contribution — a genuinely novel, encryption-free, empirically strong watermarking scheme — is real and well-demonstrated. The central weakness (theoretical overclaim) is a framing/signaling issue rather than a methodological flaw, and the empirical evidence robustly supports practical losslessness. Scores from comparable anchors (PRC: 6.50, Shallow Diffuse: 6.00, Hidden in the Noise: 5.83) suggest placement in the upper half of the borderline-accept range, tempered slightly by the overclaim issue.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>