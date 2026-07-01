Let me read the paper in chunks to verify the reviewer's claims.Now let me read the theoretical sections more carefully to verify the key claims:Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me run Round 1 calibration search to bracket the score.Let me read the most relevant anchor papers to calibrate:Now let me read the HexshmBu0P anchor for comparison in the 5-5.5 range:Now I have enough calibration data. Let me form my assessment.

**Round 1 Bracket**: Based on the anchors, this paper sits between **5.5 and 7.0**.

Key comparisons:
- **PRC Watermark** (jlhBFm7T2J, 6.50, Accept): Direct competitor with stronger theoretical foundations but much weaker practical performance. Spherical Watermark addresses PRC's main limitations.
- **TabWak** (71pur4y8gs, 7.20, Accept): First-in-domain novelty with thorough evaluation. Above this paper.
- **Shallow Diffuse** (1IwoEFyErz, 6.00, Reject): Less novel, weaker experiments. Below this paper.
- **Hidden in the Noise** (ll2nz6qwRG, 5.83, Accept): Solid but less thorough. Below this paper.
- **Recipe for Watermarking DMs** (HexshmBu0P, 5.33, Reject): Limited novelty. Clearly below this paper.

The theory overclaiming prevents reaching the 7+ range, but the strong practical contribution and thorough experiments place it firmly in the 6-6.5 zone. Let me now write the final review.

---

## Summary
Spherical Watermark proposes an encryption-free, lossless watermarking framework for diffusion models. The method embeds watermark bits by: (1) mixing repeated watermark bits with random padding via XOR over 𝔽₂ to produce a 3-wise independent bitstream, (2) projecting onto the unit sphere, applying an orthogonal rotation, and scaling by a chi-square-distributed radius to approximate standard Gaussian noise. This eliminates per-image key storage and heavy cryptographic decoding, achieving ~4 orders of magnitude faster extraction than PRC Watermark while maintaining competitive fidelity, undetectability, and robustness.

## Strengths
- **Elegant, mathematically grounded construction**: The decomposition into binary mixing (Algorithm 1), spherical normalization, orthogonal rotation, and chi-square scaling is clean and implementable. The use of spherical 3-designs (Theorem 3.2) as a theoretical foundation is a well-chosen formalization that connects watermark design to established mathematical theory. The design choices are well-motivated by the independence and moment-matching properties they provide.

- **Dramatic computational advantage over PRC**: Figure 4 demonstrates extraction time roughly four orders of magnitude faster than PRC Watermark. This stems directly from eliminating belief-propagation decoding and is a practically significant contribution for real-world deployment scenarios.

- **Strong empirical undetectability**: Table 1 shows FID values matching the unwatermarked baseline within noise (48.12 vs. 48.13 on COCO/SD v1.5). Figure 2 shows that both latent-level MLP and image-level ResNet-18 classifiers cannot distinguish watermarked from unwatermarked samples, achieving only chance-level accuracy (~50%). This is well-supported, multi-modal evidence.

- **Thorough ablation studies**: Section 4.3 and Tables 3–5 systematically isolate the effects of individual modules (Figure 6b–c showing both are necessary), hyperparameters (s, N), ODE solvers (DDIM, PNDM, DPM-Solver++), and timestep configurations. This level of rigor strengthens confidence in the design choices.

- **Superior scaling with watermark capacity**: Figure 6(a) shows PRC Watermark's accuracy degrades sharply and fails entirely beyond l_m = 2000 under JPEG-70 compression, while Spherical Watermark maintains high detection rates across all tested capacities. This is a meaningful practical advantage.

## Weaknesses

### Fatal
None

### Major
1. **Theoretical guarantee is substantially weaker than framing suggests** — The paper's proof chain establishes that z^(2) is a spherical 3-design (Theorem 3.2), which guarantees moment-matching up to degree 3 only. However, Lemma 3.4's converse requires *true* uniform distribution on S^{n-1}, not a 3-design approximation. The logical gap appears in the transition from Lemma 3.3 (z^(3) is a 3-design) to applying Lemma 3.4 (which needs actual uniformity). Despite this, Section 3.3 opens with "we provide theoretical guarantees that… the final latent code z_w is distributed as 𝒩(0, I)" (line 157), and the Conclusion states "provably and empirically indistinguishable from a standard Gaussian prior" (line 336). The abstract is more careful ("preserves the target prior up to third-order moments"), and Section 5 acknowledges that "higher-order moments may deviate from the true prior." The empirical evidence (FID, classifiers) strongly supports practical indistinguishability, but the theory does not establish the formal computational indistinguishability definition (Eq. 2) that the paper sets up. This gap between proven and claimed guarantees undermines the theoretical contribution.

### Minor
2. **Gaussian Shading compared under degraded configuration** — The paper evaluates Gaussian Shading with fixed keys and explicitly notes this breaks its losslessness (line 193: "with fixed keys, Gaussian Shading no longer achieves true losslessness"). Table 1 shows its elevated FID (50.70 vs. 48.13 on COCO/SD v1.5) and Figure 2 shows it is easily detected (97% latent-level classifier accuracy). While the motivation for fixed-key evaluation is practical and legitimate, the comparison should be consistently caveated throughout (Tables 1–2, Figures 2–3), or additionally include GS in its intended per-image-key mode for quality metrics to give a fairer picture.

3. **Theorem 3.1 precondition does not match deployment** — Theorem 3.1 requires "m and r consist of independent Bernoulli(1/2) bits" (line 161), but in practice m is a fixed deterministic bitstring (user ID/timestamp). The 3-wise independence result likely still holds when m is fixed (XOR with fixed bits preserves independence of the random r components, and Algorithm 1's disjoint-support structure ensures the necessary conditions), but this argument is absent. The theorem's preconditions should be stated for the conditions that actually apply.

4. **Formal cryptographic definitions are set up but not followed through** — Section 3.1 introduces a security parameter ρ and formal definitions of computational indistinguishability (Eq. 2) and traceability (Eq. 4), but ρ is never defined or related to method parameters. The traceability bound depends on majority-vote thresholds and DDIM inversion noise, neither of which are shown to be negligible in ρ. The formal framework creates expectations the paper does not meet.

5. **Post-processing robustness gap with Gaussian Shading not discussed** — Table 2 shows ACC under post-processing: Gaussian Shading 98.43% vs. Spherical Watermark 95.02%. Under adversarial attacks the relationship reverses (98.12% vs. 88.06%), but the post-processing gap is not acknowledged. The paper's claim "our method consistently achieves higher TPR and ACC" (line 273) refers specifically to comparison with PRC Watermark, which is accurate, but a more nuanced discussion of the GS comparison would be appropriate.

### Trivial
None

## Nice-to-Haves
- **Error analysis of extraction pipeline**: Analyzing how DDIM inversion noise, VAE encoding/decoding error, and post-processing distortions propagate through the inverse rotation and rounding steps. Even a rough bound on bit-flip probability would strengthen the robustness analysis.
- **Evaluation on modern architectures**: Testing on SDXL, flow-matching models, or other recent diffusion architectures to empirically demonstrate the claimed generality (Section 5 states the method generalizes to any model with Gaussian prior and invertible mappings).
- **Security analysis under multi-image access**: Analyzing what an adversary can infer about the fixed signature 𝒦 = {T, C} given access to multiple watermarked images, given that the paper frames its contribution using cryptographic definitions.

## Removed Points
*These points are flagged to be removed, treat them with caution:*

- **"Extraction normalization not shown in Eq. 13"**: The reviewer noted that Eq. 13 applies C⁻¹ directly to ẑ_T without dividing by the radius first. However, since r² ~ χ²(l_x) concentrates around l_x, the entries of C⁻¹ẑ_T are approximately ±1, and the rounding step (round((ẑ^(2)+1)/2)) absorbs the scaling. This is at most a minor presentation issue, not a methodological flaw.

- **"Only SD v1.5 and v2.1 tested"**: This is a generic request for more experiments. The method is architecturally generic by construction, and two backbone models with two datasets is a reasonable evaluation scope. Moved to nice-to-have.

- **"Missing security analysis for fixed K"**: This demands analysis beyond the paper's stated scope (undetectability and robustness, not cryptographic security under oracle access). The paper focuses on practical watermarking, not adversarial cryptanalysis. Moved to nice-to-have.

## Novel Insights
The connection between spherical t-designs and watermark undetectability is a genuinely novel theoretical lens in the watermarking literature. The insight that binary XOR mixing can produce 3-wise independent bitstreams which, after spherical projection and chi-square scaling, approximate Gaussian noise *without any cryptographic operations*, represents a meaningful conceptual contribution. This provides a clean intermediate between the full cryptographic approach of PRC (computationally expensive but formally proven) and heuristic approaches (fast but with no guarantees), demonstrating that algebraic structure alone can achieve practical indistinguishability.

## Suggestions
- Rewrite Section 3.3's opening statement and the Conclusion to clearly separate what is proven (moment-matching up to degree 3 via spherical 3-design) from what is empirically demonstrated (statistical indistinguishability by classifier and FID). Present the empirical evidence as the primary support for practical indistinguishability rather than as a consequence of the theory.
- State and prove Theorem 3.1 for the realistic case where m is fixed and only r is random, closing the precondition gap.
- Consistently caveat Gaussian Shading comparisons throughout Tables 1–2 and Figures 2–3 as reflecting a fixed-key (degraded) configuration, or additionally include GS in its intended per-image-key mode for quality/detectability metrics.
- Add a brief discussion acknowledging the post-processing accuracy gap relative to Gaussian Shading (95.02% vs. 98.43% in Table 2) and the trade-off this represents.
- Either work within the formal framework of Section 3.1 (defining ρ, proving bounds in terms of it) or present the definitions as aspirational context rather than as the standard the paper claims to meet.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to Spherical Watermark |
|-------|------|-----------|-------|----------------------------------|
| IC-Light | u1cQYxRI1H | 0.50 (mislabeled; actual 10.0) | R1 | Not relevant (illumination editing) |
| Clothing-Irrelevant L-ReID | 5lUdTogEL3 | 1.00 | R1 | Far below; fundamentally flawed paper |
| NEMESIS | 5kMwiMnUip | 1.40 | R1 | Far below; limited contribution |
| KL Divergence GFlowNets | Uj0h13lVrR | 1.00 | R1 | Far below; not relevant |
| Sample What You Can't Compress | vK8C37eHXM | 3.20 | R1 | Below; Spherical WM has clearer contribution and better experiments |
| Secure Diffusion Model | fkNsgI1nye | 3.00 | R1 | Below; less novel, different problem space |
| Pixel-Aware Reverse Diffusion | W4djmqKZC6 | 3.00 | R1 | Below; generic concerns, limited novelty |
| Self-distillation for DMs | QKqWnNkwPL | 3.00 | R1 | Below; less impactful contribution |
| Securing DGMs w/ Adversarial Sig | nR1EEDuov7 | 5.00 | R1 | Below; Spherical WM has stronger contribution and better empirical support |
| Unremovable Watermarks for LLMs | 0SpkBUPjL3 | 3.75 | R1 | Below; different domain, weaker experimental support |
| **A Recipe for Watermarking DMs** | HexshmBu0P | 5.33 | R1 | Below; limited novelty per reviewers, less rigorous experiments |
| Interpretable Boundary Watermark | xyysYa4YvF | 4.00 | R1 | Below; narrow contribution |
| **Shallow Diffuse** | 1IwoEFyErz | 6.00 | R1 | Comparable but below; less novel construction, similar experimental scope but weaker novelty |
| **Hidden in the Noise (WIND)** | ll2nz6qwRG | 5.83 | R1 | Below; Spherical WM has more systematic evaluation and clearer practical advantages |
| **PRC Watermark** | jlhBFm7T2J | 6.50 | R1 | Most directly comparable; PRC has stronger theory but much worse practical performance (speed, capacity). Spherical WM trades theoretical rigor for significant practical gains |
| **TabWak** | 71pur4y8gs | 7.20 | R1 | Above; first-in-domain novelty with thorough evaluation, stronger overall contribution |
| Lightweight Deep Watermarking | j7b4mm7Ec9 | 7.60 | R1 | Above; different subfield (image watermarking efficiency) |
| Würstchen | gU58d5QeGv | 8.00 | R1 | Above; different topic, stronger contribution |
| Progressive Compression w/ UQ DMs | CxXGvKRDnL | 8.00 | R1 | Above; different topic |
| One Step Diffusion via Shortcuts | OlzB6LnXcS | 8.00 | R1 | Above; different topic, broader impact |

**Round 1 bracket**: 5.5–7.0

**Narrowing rationale**: The paper is clearly stronger than Shallow Diffuse (6.00, Reject) and Hidden in the Noise (5.83, Accept) due to its more novel construction, stronger empirical evidence, and practical advantages. It is comparable to but slightly below PRC Watermark (6.50, Accept): PRC has formal cryptographic guarantees that Spherical Watermark cannot match, but Spherical Watermark offers dramatically better practical performance (~4 orders magnitude faster extraction, no capacity ceiling). The theory overclaiming (Major weakness #1) prevents it from reaching the 7+ range that papers like TabWak achieve. The practical contribution is genuinely strong and the experiments are thorough, placing it firmly in the borderline accept zone.

**Final score**: 6.0. The paper makes a solid practical contribution with an elegant construction, strong empirical evidence, and clear advantages over PRC Watermark in speed and capacity. However, the theoretical overclaiming—where the proven guarantee (moment-matching up to degree 3) is presented as distributional equivalence—is a real weakness that prevents a higher score. With honest reframing of the theoretical claims, this would be a stronger paper.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>