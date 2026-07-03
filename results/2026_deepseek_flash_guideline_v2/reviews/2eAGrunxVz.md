Now I have all the evidence I need. Let me compose the final review.

## Summary

Spherical Watermark proposes a novel watermarking framework for diffusion models that converts binary watermarks into Gaussian-like noise via binary embedding followed by spherical mapping (unit-sphere projection, orthogonal rotation, and chi-square scaling). The key innovations are: (1) using spherical 3-design theory to prove the watermarked noise matches Gaussian up to third-order moments—a formally grounded approach distinct from prior empirical methods, (2) a fixed-key design that eliminates per-image key management required by prior lossless methods like Gaussian Shading, and (3) extraction that is ~4 orders of magnitude faster than PRC Watermark while matching or exceeding its undetectability and robustness.

## Strengths

1. **Novel theoretical grounding via spherical 3-designs**: Section 3.3 proves (Theorem 3.1, Theorem 3.2, Lemma 3.3, Lemma 3.4) that the watermarked noise matches standard Gaussian up to third-order moments. The chain—3-wise independence in the binary domain → spherical 3-design on the unit sphere → orthogonal rotation preserving the design property → chi-square scaling—is a formally proven guarantee that goes beyond what typical empirical-only methods provide and represents a genuinely novel contribution to the watermarking literature.

2. **Elimination of per-image key storage**: The method uses a single fixed signature K = {T, C} kept secret during runtime (Section 3.2), avoiding the per-image key/nonce management required by Gaussian Shading. This is a concrete and meaningful practical advantage clearly described and consistently highlighted.

3. **Substantial computational efficiency**: Extraction is ~4 orders of magnitude faster than PRC Watermark (~10⁻³·⁵ s vs ~10¹·⁰ s, Figure 4). The comparison isolates the transformation itself (excluding diffusion sampling/inversion), making it clean and directly attributable to the algorithmic design.

4. **Strong empirical undetectability**: FID values are within ~0.03 of the unwatermarked baseline across configurations (Table 1), and trained latent-level and image-level binary classifiers achieve only chance-level accuracy (~50%) for the proposed method, matching PRC and substantially outperforming lossy methods (Figure 2).

5. **Superior robustness under adversarial attacks**: Under WEvade adversarial attacks, Spherical Watermark achieves 98.12% ACC (Table 2), substantially outperforming lossy methods (~49-52% ACC) and slightly exceeding PRC Watermark (97.69% ACC). Clean extraction accuracy is 99.99%.

6. **Scalability across watermark capacity and solver configurations**: Maintains high detection accuracy for capacities beyond 2000 bits where PRC fails entirely (Figure 6a). Extraction accuracy remains above 96% across DDIM, PNDM, and DPM-Solver++, and across a grid of generation/inversion timesteps from 10 to 50 (Tables 4, 5).

7. **Controlled ablation validating both modules**: Omitting binary embedding makes the noise trivially distinguishable; omitting spherical mapping collapses robustness under brightness adjustment (Figure 6b, 6c). These controlled experiments confirm that both components are necessary and well-motivated.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Overclaim in the introduction vs. the proven guarantee**: The abstract correctly states that the method preserves the prior "up to third-order moments," but the introduction (line 26) claims the final noise is "statistically indistinguishable from standard Gaussian noise" without this qualification, and contribution 2 (line 28) repeats the unqualified claim. The abstract also describes the method as recovering "exact multivariate Gaussian noise" (line 9), while the theoretical guarantee is approximate (up to third-order moments). The limitations section (line 332) acknowledges the gap. The paper would benefit from consistent qualification throughout to match what is actually proven.

2. **Tree-Ring included in undetectability comparison without appropriate framing**: Tree-Ring is a detection-only scheme designed to create detectable patterns (line 193 notes it "supports detection only"). Including it in the undetectability comparison (Figure 2, Table 1) where it achieves 100% detectability and presenting this as a weakness is a category error—Tree-Ring's detectability is by design, not a flaw. The paper should either exclude Tree-Ring from this comparison or explicitly note that its detectability is intentional.

3. **Gaussian Shading comparison uses a non-standard configuration without qualifying the abstract**: The paper transparently discloses that Gaussian Shading is evaluated "with fixed keys" and "no longer achieves true losslessness" (line 193). However, the abstract's blanket claim of "outperforming both lossy and lossless approaches" (line 9) does not caveat that the comparison with Gaussian Shading is on a nonstandard (fixed-key) variant, not the method as intended by its authors. The body is honest, but the high-level framing could mislead a casual reader.

4. **"Encryption-free" is imprecise**: The method requires a secret signature K = {T, C} that is "kept fixed and secret during runtime to prevent unauthorized removal" (line 82). The innovation is a single fixed secret rather than per-image secrets—a meaningful advantage—but "encryption-free" could be misinterpreted as requiring no secrets at all. "Fixed-key" or "without per-image key management" would be more precise descriptors.

### Trivial
- **Typesetting issue in Equation 6**: The dimension notation `l_m = N × l_m` is circular; it should be `l_{Nm} = N × l_m` (consistent with line 78).
- **PRNG seeding not specified**: Algorithm 1 uses random permutations without specifying the pseudorandom number generator seeding, which affects fine-grained reproducibility of the matrix construction.

## Nice-to-Haves
- A discussion of security against inference attacks: if K = {T, C} is a fixed secret and the API serves many queries, could an adversary with many image outputs estimate the transform? This threat model is not discussed but is relevant for deployment.
- A quantitative analysis of bit-error rates before and after majority voting, especially near the rounding decision boundary in Eq. 13, to characterize sensitivity to DDIM inversion errors.
- A brief discussion of why the empty-prompt DDIM inversion mismatch (unconditioned reverse process vs. conditioned forward process at guidance scale 7.5) does not significantly degrade extraction accuracy.

## Removed Points
These points from the reviewer inputs were evaluated and removed with justification:

1. **"Gaussian Shading comparison is structurally unfair and fatal" (harsh critic's point 1)**: The paper transparently discloses the fixed-key configuration (line 193: "with fixed keys, Gaussian Shading no longer achieves true losslessness"). The comparison is informative for understanding what happens when other lossless methods are forced to use fixed keys—a precisely relevant comparison for a paper whose contribution is fixed-key losslessness. The critic's assertion that this "undermines the paper's core claims" is not supported given the transparent disclosure. This is a framing subtlety, not a fatal issue.

2. **"Encryption-free label is misleading" (harsh critic's point 3)**: The paper is clear about the secret signature and its role. "Encryption-free" reasonably conveys that the method does not use cryptographic encryption/decryption operations (unlike Gaussian Shading's stream cipher or PRC's error-correcting codes). The meaning is clear from context and the paper is not misleading.

3. **"FID evaluation not statistically significant" (harsh critic's note on FID)**: The critic's claim that "differences are not statistically significant for most methods" is presented without statistical tests. With overlapping error bars, the null finding is that these methods are indistinguishable from the original—which supports, not undermines, the paper's undetectability claim. The paper correctly states "only PRC Watermark and our method match the original in FID."

4. **Generic/superficial strengths from Strength Finder**: Various generic strengths ("well-executed," "solid empirical validation") lacking specific evidence anchors were removed.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Qualify the theoretical claim in the introduction**: Replace "statistically indistinguishable from standard Gaussian noise" with "matches standard Gaussian up to third-order moments" (consistent with the abstract). This would align the high-level claim with what is actually proven.
2. **Either exclude Tree-Ring from the undetectability comparison or add explicit framing**: A brief note that "Tree-Ring's 100% detectability is by design and does not represent a weakness of that method" would resolve the issue cleanly.
3. **Add a brief qualification in the abstract**: A phrase like "under fixed-key operation" alongside the comparison claim would prevent misinterpretation.
4. **Specify PRNG seeding for the random permutations** in Algorithm 1 to improve reproducibility.
5. **Move from "encryption-free" to "fixed-key" or "without per-image key management"** for precision, though this is a minor framing preference.

## Score and Decision

Base on the ICLR scoring scale (1=strong reject, 3=reject, 4=borderline reject, 6=borderline accept, 8=accept, 10=strong accept):

**Score: 8.0 — Accept**

**Decision: Accept**

**Rationale**: The paper presents a genuinely novel approach to diffusion model watermarking with a formally grounded theoretical component (spherical 3-designs), a clear practical advantage (fixed-key operation eliminating per-image key management), and a dramatic computational speedup over the primary lossless competitor (PRC). The experimental evaluation is thorough: multiple datasets (COCO, SDP), multiple models (SD v1.5, SD v2.1), multiple attack types (post-processing, adversarial), multiple ODE solvers, and controlled ablations validating each module. The weaknesses are primarily presentation/framing issues—overclaiming in the introduction about "statistical indistinguishability" vs. the third-order guarantee, including Tree-Ring in an undetectability comparison that is a category error, and an abstract that could be more precisely qualified. None of these threaten the core contribution. With minor textual revisions, these issues are straightforward to address.

The calibration search was unavailable due to a data access issue, so I cannot report anchor comparisons. However, based on the ICLR scoring criteria, this paper demonstrates sufficient novelty, rigor, and significance to warrant acceptance.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>