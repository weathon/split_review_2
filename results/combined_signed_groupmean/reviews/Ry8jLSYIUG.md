Now I have enough calibration data. Let me write the final consolidated review.

## Summary

This paper studies the gap between theoretical watermarking capacity and what current deep learning models achieve. The authors derive geometric bounds on capacity under PSNR constraints (treating images as lattice points in a hypercube intersecting a hypersphere), then conduct controlled experiments stripping away real-world complexity to show that Video Seal's architecture severely underperforms even these bounds. A scaled-up model (Chunky Seal) achieves 4× the capacity of Video Seal at comparable robustness. The paper argues that architectures, not fundamental limits, are the bottleneck.

## Strengths

- **Novel geometric framing of watermarking capacity.** The treatment of capacity as counting integer lattice points in the intersection of a hypercube (image space) and a hypersphere (PSNR ball) is conceptually cleaner than prior information-theoretic approaches that assume Gaussian channels. The bounds come with explicit validity conditions for three regimes (ball-in-cube, cube-in-ball, partial overlap), and the analysis is mathematically sound. *[Model impact: +10.00]*

- **Well-designed controlled experiments that isolate architectural failure.** Training Video Seal on a single gray image with only a PSNR constraint — stripping away all robustness, perceptual, and data-distribution complexities — is a genuinely informative diagnostic. The finding that Video Seal cannot embed 1024 bits when the theoretical bound allows ~600,000 bits, while a linear model succeeds at 2048 bits, cleanly rules out several competing explanations (robustness complexity, perceptual constraints, data distribution) and pins the blame on architectural limitations. The resolution-utilization finding (32×32 performance ≈ 256×256 performance) is a striking diagnostic result. *[Model impact: +10.00]*

- **The handcrafted embedder (Eq. 2) provides a constructive proof of achievability.** It demonstrates that the PSNR bound can be approached (456,509 bits at 42 dB on a 256×256 gray image), converting the five-way ambiguity into a single remaining explanation: architectures are the bottleneck (in the PSNR-only regime). *[Model impact: +9.96]*

- **Chunky Seal shows real practical improvement.** A 4× capacity increase (256→1024 bits) over Video Seal with comparable robustness across multiple transformations, achieved through straightforward scaling. This demonstrates that practical improvement is possible without architectural innovation. *[Model impact: +7.00]*

- **The proposed sanity checks (Section 5)** — capacity scaling linearly with image size, decreasing linearly with higher PSNR, outperforming linear baselines, showing predictable drops under augmentations — are concrete and useful for evaluating future watermarking methods. *[Model impact: +9.86]*

## Weaknesses

### Major

- **PSNR-vs-perceptual gap weakens the headline claims.** The paper's central framing ("orders of magnitude" untapped capacity) rests on bounds derived under a PSNR constraint. PSNR is well-known to correlate poorly with perceptual quality — a per-pixel independent perturbation within ±2 intensity levels satisfies ~42 dB PSNR but produces visible noise. The handcrafted model achieving 456,509 bits at 42 dB likely produces visibly noisy output, but the paper reports no SSIM, LPIPS, or human evaluation for it. The paper acknowledges perceptual constraints as hypothesis B in Section 3 and tests this by removing perceptual constraints, showing Video Seal still underperforms — but this only demonstrates that architectures are suboptimal under a PSNR constraint, not that the PSNR bound is the relevant bound for practical imperceptible watermarking. The abstract's "orders of magnitude" framing conflates PSNR-based theoretical capacity with practically achievable capacity under perceptual constraints. The paper partially addresses this in its limitations section but the headline claims remain unsupported. *[Model impact: -10.00]*

- **Robustness bounds have a 100× ambiguity that is not resolved.** Section 2.5 introduces heuristic bounds (Bounds 10–12, ~0.5 bpp for aggressive crops) and a conservative lower bound (Bound 13, ~0.005 bpp). The paper is transparent that the heuristic bounds "over-approximate" in some cases and "under-approximate" in others, and that Bound 13 is "extremely conservative and unrealistic." However, the claim that "robustness cannot explain the low watermarking capacity" depends on which bound is closer to the true capacity. If the conservative bound (~0.005 bpp, or 904 bits for 256×256px under 75% crop) is closer to reality, then Chunky Seal (0.0052 bpp) is already near the limit for robust watermarking — directly contradicting the paper's thesis. The paper states a belief that the heuristic bounds are "much closer to the true capacity" but provides no rigorous justification for this belief. *[Model impact: -9.99]*

### Minor

- **Chunky Seal's LPIPS degradation is understated.** Table 3 shows LPIPS of 0.0085±0.0067 versus Video Seal's 0.0019±0.0011 — a 4.5× increase. The paper describes this as "only slightly higher LPIPS," which downplays a real quality degradation. The standard deviation (0.0067) suggests some images have notably worse perceptual quality. *[Model impact: -0.03]*

- **Narrow comparative evaluation for Chunky Seal.** Chunky Seal is compared quantitatively against only Video Seal (Table 3). Other methods from Figure 1 (TrustMark, WAM, HiDDeN, MiRRE, CM) appear only in the scatter plot with no quantitative comparison table, so the robustness and quality claims are only validated against a single baseline. *[Model impact: -9.98]*

- **Data distribution analysis (Section 2.6) relies on a crude proxy.** Using VQ-VAE/VQGAN codebook capacity as an upper bound on perceptually distinct images conflates compression rate with perceptual discriminability. The VQ codebook capacity (1024^{32×32}) is a loose upper bound — the true number of perceptually distinct natural images is certainly far lower. The citation of Costa's dirty-paper coding result for Gaussian channels is only loosely analogous and not rigorously justified for the PSNR-ball lattice-point counting setup. *[Model impact: -1.74]*

### Trivial

None.

## Nice-to-Haves

- Add perceptual quality metrics (SSIM, LPIPS) for the handcrafted and linear models used in the controlled experiments, to confirm that approaching the PSNR bound does not come at the cost of visible artifacts.
- Add at least one more quantitative comparison for Chunky Seal against a second baseline (e.g., TrustMark at a comparable capacity setting).
- Discuss whether Chunky Seal's LPIPS gap could be reduced via hyperparameter tuning or loss weighting adjustments.
- Include variance/error bars for the controlled experiment results in Table 1.

## Removed Points

These points from the input review are removed as they are either factually incorrect, based on misreading the paper, or nitpicks that do not affect evaluation:

- *"The handcrafted model output is almost certainly visible as grain"* → The handcrafted model's purpose is as a proof-of-concept for achievability of the PSNR bound; the paper does not claim it produces imperceptible outputs in a practical sense. The absence of perceptual metrics is noted in the weaknesses above but the severity of this specific criticism is reduced.
- *"The linear model is barely described"* → The paper describes the linear model (message → 256×256×3 residual, flattened image → 1024 outputs, with training hyperparameters). This is sufficient for a simple linear model.
- *"No variance reported in Table 1"* → These are diagnostic single-run results from hyperparameter sweeps; Table 3 does report means±std for the main results.
- *"VQ-VAE assumption is not conservative"* → The reviewer misread this. The paper's assumption that all possible VQ-latent configurations fall within the same PSNR ball is actually maximally conservative (overestimates collisions), not the opposite.

## Novel Insights

The harsh critic's review surfaces a genuine tension that the paper partially acknowledges but does not resolve: the PSNR bounds are mathematically sound, but the distance from PSNR-based capacity to perceptually-meaningful capacity is itself an open question. The controlled experiments only rule out architectural explanations within a PSNR-only regime, not for practical perceptual watermarking. This diagnostic gap — between what the paper proves (architectures underperform PSNR bounds) and what it claims ("orders of magnitude" of untapped practical capacity) — is the most important critical insight for the authors to address.

## Suggestions

1. Temper the abstract and conclusion's "orders of magnitude" framing to make clear these are PSNR-based bounds, and explicitly state that the gap to perceptually-meaningful capacity remains an open question.
2. Add perceptual quality evaluation (SSIM, LPIPS) for the handcrafted and linear models.
3. Acknowledge the 100× gap in robustness bounds more prominently in the main claims, and clearly separate what the heuristic bounds suggest from what is rigorously proven.
4. Add at least one additional baseline comparison for Chunky Seal.

---

Now let me compute the final score by comparing against my calibration anchors.

**Round 1 bracket:** Based on the initial search, the paper sits between 4.0 and 6.0. The two major weaknesses (-10.00, -9.99) place a ceiling below the 6.0+ range where anchors like Shallow Diffuse (6.00) and Undetectable watermark (6.50) were accepted or rejected for different reasons. The strong strengths (+10.00, +10.00, +9.96) place a floor above the 3.75-level papers (SuperMark), which lacked novel theory.

**Round 2 narrowing:** Comparing against anchors in the 4.0–6.0 range:
- **SAT-LDM (5.50, Reject):** +9.94 theory, +9.88 robustness, but -10.00 (flawed motivation), -9.99 (lack of innovation). The paper under review has stronger theory and more novel experiments, but leans more heavily on an overclaimed thesis.
- **A Recipe for Watermarking (5.33, Reject):** +10.00 experiments, +9.94 clarity, -9.88 (limited novelty). The paper under review has greater theoretical novelty and an elegant diagnostic methodology, but the overclaiming is comparable.
- **Hidden in the Noise (5.83, Accept):** +9.97 clarity, +9.94 innovation, weaknesses up to -10.00 (overclaimed). This paper had a clearer contribution-weskness balance tilted toward acceptance.
- **Watermark-based Detection (4.50, Reject):** +8.57 theory, -10.00 (poor experiments), -10.00 (no novelty). The paper under review has stronger experiments and more novelty.

**Final placement:** The paper's two decisive major weaknesses (-10.00 and -9.99) are specific, substantive, and directly threaten the headline claims. While the geometric bounds and diagnostic experiments are genuine contributions (+10.00, +10.00), the central thesis is overclaimed relative to what is supported. This places the paper at **4.5** — borderline reject. The paper has real value but would need to (a) temper the claims, (b) evaluate perceptual quality of constructive models, and (c) address the robustness bound gap to reach acceptance.

**Calibration anchors consulted:**
| Path | Score | Round | Itemized | Comparison |
|------|-------|-------|----------|------------|
| u1cQYxRI1H | 0.50 | 1 | No | Not comparable (illumination harmonization) |
| 5lUdTogEL3 | 1.00 | 1 | No | Not comparable (person re-id) |
| gwZ90hFSL2 | 1.00 | 1 | No | Not comparable (NLP) |
| 5kMwiMnUip | 1.40 | 1 | No | Not comparable (LLM jailbreaking) |
| Uj0h13lVrR | 1.00 | 1 | No | Not comparable (GFlowNets) |
| S3zKrEQpRr | 3.00 | 1 | No | GNN channel capacity — thematic relation but different domain |
| Z1E0EahS5w | 3.33 | 1 | No | Reservoir computing capacity bounds — tangentially related |
| 6j0GH40mFt | 3.40 | 1 | No | Not comparable (image compression) |
| hYEV8QmaOt | 3.40 | 1 | No | Not comparable (anti-forensics) |
| f47c05mcOj | 3.00 | 1 | No | Not comparable (adversarial perturbations) |
| O08nfMzc93 | 4.50 | 1,2 | Yes | Watermark theory + limited experiments. Paper under review has stronger theory and experiments but overclaims more. |
| T0ebbDO60R | 3.75 | 1,2 | Yes | Training-free watermarking, low novelty. Paper under review is stronger in both theory and experiments. |
| HexshmBu0P | 5.33 | 1,2 | Yes | Diffusion model watermarking recipe. Comparable in having comprehensive experiments but limited novelty in different ways. |
| 9XEBFywIW7 | 4.40 | 1 | No | Watermark robustness — lower score due to limited contribution. |
| xyysYa4YvF | 4.00 | 1 | No | Not comparable (DNN watermarking) |
| jlhBFm7T2J | 6.50 | 1 | Yes | Undetectable watermark with strong theory. Higher quality overall. |
| 1IwoEFyErz | 6.00 | 1 | Yes | Shallow Diffuse — strong empirical work, rejected due to limited novelty vs Tree-Ring. |
| ll2nz6qwRG | 5.83 | 2 | Yes | Hidden in the Noise — two-stage watermarking, accepted. Clearer contribution. |
| 16O8GCm8Wn | 6.40 | 1 | No | Robust watermarking benchmark — different type of contribution. |
| ETFfXGM3e4 | 5.50 | 2 | Yes | SAT-LDM — strong theory but rejected due to experimental concerns. Closest comparison. |
| jln7IcheW6 | 4.33 | 2 | Yes | LLM watermark theory — different domain but similar pattern of strong theory with overclaiming. |

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>