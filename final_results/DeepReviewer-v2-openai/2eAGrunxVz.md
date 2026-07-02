## Summary
# Final Review Report

## Summary

This paper proposes Spherical Watermark, an encryption-free lossless watermarking framework for diffusion models. The method transforms binary watermark bits into Gaussian noise that is statistically indistinguishable from a standard normal prior, using three modules: (1) binary embedding that mixes repeated watermark bits with random padding via an invertible matrix over F_2, (2) spherical mapping that projects the bitstream onto the unit sphere, applies an orthogonal rotation, and scales by an independent chi-square radius, and (3) diffusion integration that feeds the watermarked noise into Stable Diffusion. The authors provide theoretical analysis showing the watermarked noise matches N(0,I) up to third-order moments via spherical 3-design, and extensive experiments on SD v1.5/v2.1 with COCO and SDP datasets demonstrate competitive or superior performance compared to lossy (DwtDct, DwtDctSvd, RivaGAN, Tree-Ring) and lossless (Gaussian Shading, PRC Watermark) baselines on undetectability, traceability, and computational efficiency.

**Novelty Assessment (deferred — external literature verification unavailable in this run):** The core technical contributions — the combination of binary embedding with spherical 3-design mapping for lossless watermarking — appear technically sound and well-motivated. However, without external retrieval verification, novelty judgments against the full literature are explicitly deferred. A manual literature search is required to confirm that the spherical 3-design approach to Gaussian-preserving watermarking is indeed novel relative to the complete set of existing distribution-preserving schemes.

## Strengths
**S1. Technically well-motivated design.** The paper identifies concrete limitations in prior lossless watermarking schemes — Gaussian Shading's per-image key management overhead and PRC's computational latency and error-floor issues — and proposes a clean alternative that simultaneously addresses both. The binary embedding + spherical mapping pipeline is conceptually elegant and avoids heavy cryptographic machinery.

**S2. Solid theoretical foundation.** The authors provide a step-by-step distributional analysis from binary vector through spherical 3-design to final Gaussian noise. The use of spherical t-design theory to argue moment-matching up to third order is a principled approach, even if the claim of exact Gaussianity is marginally overstated. The theoretical chain (Theorem 3.1 → Theorem 3.2 → Lemma 3.3 → Lemma 3.4) is well-structured and clearly linked to the algorithmic modules.

**S3. Comprehensive empirical evaluation.** The experiments cover two backbone models (SD v1.5, SD v2.1), two prompt datasets (COCO, SDP), six diverse baselines spanning traditional, training-based, and latent-based methods, and eight attack types including both post-processing and adversarial (WEvade). The inclusion of five independent runs with mean and standard deviation for most metrics is commendable.

**S4. Strong undetectability results.** Both latent-level MLP and image-level ResNet-18 classifiers achieve near-chance accuracy (~50%) on Spherical Watermark, matching PRC and substantially outperforming Tree-Ring and Gaussian Shading (with fixed keys). FID values closely match the unwatermarked baseline, confirming minimal distributional shift.

**S5. Dramatic computational efficiency gain.** The extraction speed (~10^-3.5 s) is roughly four orders of magnitude faster than PRC Watermark (~10^1 s), which is a practically meaningful advantage for deployment scenarios requiring real-time provenance verification.

**S6. Careful ablation studies.** The modular ablation (Section 4.3) convincingly demonstrates that both binary embedding and spherical mapping are necessary for the full benefit. Parameter sensitivity analysis (s, N, l_m, l_p, ODE solvers, timesteps) is thorough and shows the method is robust to hyperparameter choices.

## Weaknesses
**W1. [Major/Method] Theoretical guarantee overstated: "z_w is distributed as N(0,I)" vs. 3-design bound.** The paper claims that the watermarked noise is "distributed as N(0,I)" but the spherical 3-design argument only guarantees moment-matching up to third order. Lemma 3.4 requires exact uniform spherical distribution + independent chi-square radius for exact Gaussianity, yet the construction provides only an approximate uniform distribution (3-design). The total variation distance between the true distribution and N(0,I) is not quantified, and the asymptotic convergence in l_x is stated but not bounded. This overstatement appears in the Abstract, Section 3.3, and Conclusion.  
*Evidence:* Page 5 — Section 3.3, Theorem 3.2 + Lemma 3.4.  
*Impact:* Overclaims the theoretical guarantee; a mathematically informed reviewer will note the gap.  
*Fix:* Replace "distributed as N(0,I)" with "matches N(0,I) up to third-order moments" throughout. Add a bound on the total variation distance or KL divergence as a function of l_x.

**W2. [Major/Method] Security formalism (Eq. 2-4) does not match deterministic implementation.** The undetectability definition uses computational indistinguishability with a security parameter ρ, but the actual construction is essentially statistical (based on spherical design properties) and deterministic given the fixed signature K. The parameter ρ is never mapped to concrete hyperparameters (l_r, s, N), and the negligible function negl(ρ) is never instantiated. Eq. (3) assumes G is deterministic, which holds only when the diffusion seed is fixed — this assumption is not stated.  
*Evidence:* Page 3 — Section 3.1, Eq. (2)-(4).  
*Impact:* The cryptographic formalism gives an impression of provable security that the construction does not fully deliver.  
*Fix:* (a) Map ρ to l_r/N and provide a concrete bound on the statistical distance. (b) State that Eq. (3) holds for deterministic G (fixed-seed sampling). (c) Clarify that the guarantee is statistical, not computational.

**W3. [Major/Experiment] Extraction reliability analysis missing.** The extraction pipeline (Eq. 13) uses a hard rounding step to recover binary values from continuous latents. ODE inversion and VAE encoding both introduce errors, yet the paper provides no analysis of bit-flip probability, error propagation as a function of the sparsity parameter s, or worst-case robustness guarantees. Table 3 shows empirical robustness, but the mechanism by which errors arise and are corrected (majority voting) is not formally characterized.  
*Evidence:* Page 4 — Eq. (12)-(13), extraction description.  
*Impact:* For security-sensitive provenance applications, the extraction reliability under worst-case (rather than average) conditions is critical. Without error analysis, deployment confidence is reduced.  
*Fix:* Add a subsection modeling inversion distortion as additive noise, deriving per-bit flip probability, and bounding majority-vote error rate as a function of attack strength.

**W4. [Major/Writing] Unbounded superiority claims.** The Abstract states "outperforming both lossy and lossless approaches" and the Conclusion states "superior robustness under realistic distortions" without specifying the comparison scope. Table 2 shows that on Clean ACC, Gaussian Shading achieves 100% while Ours achieves 99.99%; on Post-Processing ACC, Gaussian Shading achieves 98.43% while Ours achieves 95.02%. The method does not uniformly outperform all baselines on all metrics.  
*Evidence:* Page 0 (Abstract), Page 7 (Table 2), Page 9 (Conclusion).  
*Impact:* Unbounded claims reduce credibility and invite reviewer pushback.  
*Fix:* Replace global superiority statements with scoped claims that specify the comparison set and acknowledge trade-offs.

**W5. [Major/Writing] Vague comparative language in contribution statements.** The contribution list (Page 2) uses "novel framework," "simple yet effective mapping strategy," and "excellent trade-off" — promotional qualifiers that do not convey technical differentiation. The reader cannot determine what is concretely novel or excellent without reading the entire paper.  
*Evidence:* Page 2 — contribution paragraph.  
*Impact:* Weakens the impact of the contribution claims; reviewers may perceive hype.  
*Fix:* Replace each promotional qualifier with a concrete, evidence-anchored statement, e.g., quantifying the efficiency gain ("four orders faster than PRC") and the undetectability margin.

**W6. [Moderate/Writing] Related Work organized as chronological list rather than categorized comparison.** The Related Work paragraph (Page 1-2) moves from traditional methods to training-based to latent-based in roughly chronological order, without organizing around explicit comparison axes (e.g., model modification required? detection vs. extraction? distribution-preserving?).  
*Evidence:* Page 1 — Section 2, lines 21-22.  
*Impact:* The reader cannot easily see how Spherical Watermark differs from each category of methods.  
*Fix:* Restructure around 2-3 comparison axes with explicit positioning of the proposed method.

**W7. [Moderate/Method] Notational ambiguity in Eq. (6) and Eq. (10).** In Eq. (6), the symbol l_m is reused to mean N·l_m after being defined as the original watermark length. In Eq. (10), the symbol r is used for both the chi-square radius and the padding vector r (from Eq. 5).  
*Evidence:* Page 3 — Eq. (6): "l_m = N × l_m"; Page 4 — Eq. (10): "draw r such that r^2 ~ χ^2(l_x)".  
*Impact:* Notation overloading can confuse careful readers, especially those checking the derivations.  
*Fix:* Use distinct symbols: L_m = N·l_m for the extended dimension; use ρ (or s) for the chi-square radius.

**W8. [Moderate/Experiment] Missing statistical significance tests for close comparisons.** FID differences between Ours and PRC Watermark (e.g., 48.1224 vs 48.1348 on COCO SD v1.5) have overlapping 1-sigma error bars (1.5489 vs 1.3074), yet the paper claims superiority without statistical testing.  
*Evidence:* Page 6 — Table 1.  
*Impact:* Claims of FID-based improvement are not statistically supported.  
*Fix:* Add bootstrapped confidence intervals for the FID difference or a paired significance test against the strongest baseline.

**W9. [Minor/Method] Pseudorandom generator dependency not discussed.** The random padding vector r and permutation π in Algorithm 1 depend on a pseudorandom generator. The security of the scheme implicitly assumes this generator is cryptographically secure, but this is not stated. If a weak PRG is used, the "3-wise independence" property could be compromised.  
*Evidence:* Page 3 — Algorithm 1 uses RandomPermutation; Page 3 — "drawn i.i.d. from Bernoulli(1/2)."  
*Impact:* A deployment engineer might use a non-cryptographic PRG (e.g., Python's random module) and unknowingly weaken the guarantee.  
*Fix:* Add a note specifying that cryptographically secure pseudorandom generation is required for the security guarantees.

**W10. [Minor/Writing] Scope exclusion of editing/forgery attacks requires justification.** The Discussion states "Since editing and forgery may involve different adversarial, such cases are outside our scope" — the phrase "different adversarial" appears incomplete, and the exclusion lacks justification.  
*Evidence:* Page 9 — Discussion section.  
*Impact:* A security-focused reviewer will question why a primary threat model is dismissed.  
*Fix:* Complete the phrase ("different adversarial objectives") and provide a brief justification: editing attacks are a separate research challenge requiring semantically robust embedding.

## Score
**Final Score: 6/10**

**Rationale:** The paper presents a technically sound and well-motivated lossless watermarking framework with a clean theoretical backbone (spherical 3-design) and comprehensive empirical validation. The computational efficiency gain over PRC-based watermarking (four orders of magnitude) is practically significant. However, the score is constrained by three cross-cutting issues: (i) the theoretical guarantee of exact Gaussianity is overstated — the 3-design only guarantees moment-matching up to third order, and the approximation error is unquantified; (ii) the cryptographic security formalism (Eq. 2-4) creates an impression of provable security that the deterministic construction does not fully deliver; and (iii) several writing choices (unbounded superiority claims, promotional qualifiers in contribution statements, missing statistical significance tests) weaken the overall presentation and scientific defensibility. These issues are fixable with targeted revisions. Novelty assessment is deferred pending external literature verification, which was unavailable in this run.