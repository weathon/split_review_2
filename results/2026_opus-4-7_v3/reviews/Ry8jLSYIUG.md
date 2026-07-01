Now let me draft the consolidated review before calibration.Now let me run Round 1 calibration — bracketing across score bands with queries related to the paper's topic.Let me read some anchor papers to calibrate. I'll focus on watermarking-related papers across score bands.Now let me read one more anchor to sharpen my calibration in the 6-8 range:Now I have sufficient calibration data. Let me compile the final review.

**Round 1 bracket: 6.0 – 8.0**

Reasoning for bracket:
- Clearly above borderline reject watermarking papers (4.0–5.5 range) which had limited novelty or significant methodological gaps
- Comparable to or stronger than "An undetectable watermark" (6.5, Accept) and "Hidden in the Noise" (5.83, Accept) — both have novel concepts with execution gaps, but this paper's question is more fundamental
- Comparable in quality to "Towards Lightweight Deep Watermarking" (7.6) — different type of contribution (conceptual vs. practical), but similarly well-executed
- The PSNR-perceptual gap limits the reach of the claims but doesn't invalidate the core finding

The paper's strongest argument holds even under the PSNR-perceptual concern: if Video Seal can't embed 1024 bits into a single gray image (where PSNR ≈ perceptual quality), this proves architectural limitations exist regardless of what happens with perceptual metrics on natural images. This narrows the bracket upward.

**Final score: 7.0** — solid contribution with genuine conceptual novelty, clean experiments, and a real (but bounded) gap between theory and practical claims.

---

## Summary
This paper investigates whether current deep learning-based image watermarking methods are near fundamental capacity limits. It derives geometric upper bounds on watermarking capacity under PSNR and linear robustness constraints via integer-lattice-point counting, uses controlled experiments to diagnose why Video Seal falls far short of these bounds even on a single gray image, and trains Chunky Seal — a scaled-up model achieving 4× capacity (1024 bits) with comparable quality and robustness — as an existence proof that higher capacities are attainable.

## Strengths

- **Clean diagnostic methodology is the paper's standout contribution.** The decision to retrain Video Seal on a single solid gray image with only a PSNR constraint (Section 3.1) is an unusually rigorous piece of experimental reasoning. By removing all confounding complexity — distribution variability, perceptual losses, augmentations — the paper isolates an architectural bottleneck. Video Seal cannot embed 1024 bits into this trivially simple image when a linear model achieves 2048 bits in 50 epochs and a handcrafted model achieves 456,509 bits at 42 dB (Table 1, Figure 5). This is a striking, hard-to-dismiss result.

- **Well-constructed hierarchy of evidence.** The progression from linear embedder (2,048 bits) → tiled 32×32 Video Seal (32,768 bits) → handcrafted scheme (456,509 bits at 42 dB, Equation 2) provides a ladder of increasingly strong evidence that theoretical bounds are approachable. Each step is simple enough to be independently verified, and the tiling result (Section 3.2) directly exposes Video Seal's failure to exploit resolution — it uses the same effective capacity at 256×256 as at 32×32.

- **Geometric capacity framework is elegant and well-suited to the problem.** The integer-lattice-point-counting approach (Sections 2.2–2.4) directly applies to discrete image formats, bypassing unrealistic Gaussian channel assumptions from prior work (Costa 1983, Moulin & O'Sullivan 2003). The box-ball decomposition (Figure 2) makes the analysis intuitive. The result that worst-case (corner) images lose at most 1 bpp relative to the gray-center case (Section 2.4, Figure 3 right panel) is a useful and tight bound.

- **Chunky Seal is an appropriately scoped existence proof.** Achieving 4× capacity (1024 bits) with comparable robustness across a wide variety of transforms (Table 3) is a concrete demonstration, and the paper is explicit that this is a feasibility proof, not a deployable architecture (Section 5: "we do not suggest that naively scaling Chunky Seal is a practical path forward").

## Weaknesses

### Fatal
None

### Major
1. **The gap between PSNR-based theory and perceptual-quality practice is the paper's most significant unresolved tension.** The entire theoretical framework (Sections 2.2–2.5) uses PSNR as the sole imperceptibility constraint. The paper's response to the perceptual-constraint hypothesis (hypothesis B) is to retrain Video Seal on a single gray image — a degenerate case where PSNR and perceptual quality essentially coincide due to absence of texture, edges, or structure. This cleanly proves Video Seal has *architectural* limitations, but does NOT address whether perceptual constraints on natural images are themselves a major capacity bottleneck. The theoretical bounds count all integer lattice points within the PSNR ball, many of which may correspond to perceptually visible modifications on real images. The abstract's "orders of magnitude" framing and Figure 1 rest on this PSNR-based counting. The paper is transparent about this in Section 2.5's discussion and Section 5's limitations paragraph, but the top-level messaging (abstract, Figure 1 caption) does not sufficiently distinguish between what has been proven (large capacity under PSNR alone) and what remains conjectured (large unused capacity under realistic perceptual constraints).

2. **The headline framing of heuristic vs. conservative robustness bounds could mislead.** The paper foregrounds heuristic Bounds 10–12 (Figure 1, Figure 4) which show orders-of-magnitude gaps. However, the paper itself acknowledges these "can both over- and under-approximate" the true capacity (Section 2.5). The conservative Bound 13 — the only formal lower bound — gives 904 bits for a 75% crop on 256×256 images at 42 dB (Table 2). Since current SOTA achieves ~100–256 bits, this yields a gap of ~4–9× under the most aggressive crop, not the "orders of magnitude" emphasized in the abstract. For less aggressive transforms the conservative gap is much larger (e.g., LinJPEG q=10: 26,757 bits). The paper is honest in Section 2.5 ("Bound 13 is extremely conservative and unrealistic"), but the abstract and Figure 1 create a stronger impression than the formal evidence supports.

### Minor
1. **Diagnostic experiments test only one architecture family.** Sections 3.1–3.2 demonstrate architectural limitations in Video Seal specifically, but the conclusions are stated broadly: "Our models are likely significantly underperforming" (Section 3.2). Other architectures (frequency-domain, diffusion-based) may have different failure modes. The claim is partially supported by the fact that no existing method achieves high capacity (Figure 1), and the linear/handcrafted baselines show the bounds are approachable, but testing 2–3 architecturally diverse models on the gray-image task would make the inductive claim considerably more credible.

2. **Chunky Seal's LPIPS degradation is understated.** Table 3 shows LPIPS of 0.0085 vs. Video Seal's 0.0019 — a ~4.5× increase — while the paper characterizes quality as "only slightly higher LPIPS" (Section 4). LPIPS is generally considered a better perceptual quality proxy than PSNR/SSIM. A 4.5× LPIPS increase for a 4× capacity increase is consistent with the model spending its perceptual budget to encode more bits (the expected capacity-quality tradeoff), rather than exploiting genuinely "unused" capacity. Both values are very small in absolute terms, so this may not indicate meaningfully worse perceptual quality, but the characterization should be more precise.

3. **Model scaling efficiency deserves brief discussion.** The embedder is 90× larger and extractor 23× larger than Video Seal for a 4× capacity gain (Section 4, Table 3). While appropriately framed as a feasibility proof, this diminishing-returns scaling could alternatively suggest practical architectural limits are being approached. This interpretation should be briefly discussed alongside the "unused capacity" narrative.

### Trivial
None

## Nice-to-Haves
- Estimating capacity within a "perceptual ball" (e.g., LPIPS or Watson-weighted MSE), even numerically for small images, would directly address the PSNR-perceptual gap — the paper's central open question.
- Analysis of composed transformations (crop + JPEG + resize simultaneously) rather than individual ones, since real watermarking must survive multiple transforms. Composition could reduce capacity beyond the product of individual reductions.
- Chunky Seal results at intermediate capacity points (384, 512, 768 bits) to trace the Pareto frontier more densely and disentangle capacity gains from quality losses.
- Runtime/latency numbers for Chunky Seal to contextualize practical feasibility.
- The proposed sanity checks for next-generation watermarking methods (Section 5) — scaling capacity linearly with image size, outperforming linear baselines, etc. — are valuable and could be developed further.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **VQ-VAE argument looseness (Section 2.6):** The reviewer criticized the codebook-cardinality upper bound as "extremely loose." While technically true, the paper uses this conservatively — overestimating the number of distinct natural images *reduces* the capacity estimate, making the conclusion (data distribution has negligible effect) stronger, not weaker. The result is also consistent with prior theoretical work (Costa 1983). Removed because the looseness favors the paper's claim, not against it.

- **LinJPEG modeling error:** Criticism that linearized JPEG introduces unquantified error. The paper is clear these are heuristic bounds (Section 2.5) and does not claim they are exact for real JPEG. Removed as it duplicates the framing concern already captured in Major weakness #2.

- **Optimization insufficiency in gray-image experiment:** Suggestion that Video Seal's failure at 1024 bits might be due to training issues rather than architecture. The paper trains for 600 epochs with a 3×3 hyperparameter sweep; the linear model succeeds in only 50 epochs with the same optimizer. Removed because the comparison makes optimization failure implausible as the explanation.

## Novel Insights
The paper's most genuinely novel insight is reframing watermarking capacity as a geometric lattice-point counting problem on discrete image grids, bypassing the Gaussian channel assumptions that dominated prior theoretical work. The diagnostic methodology — stripping a SOTA model to the simplest possible setup and showing it still fails — is an unusually clean experimental design that reveals architectural bottlenecks invisible in standard benchmarking. The specific observation that Video Seal achieves the same effective capacity at 256×256 as at 32×32 (Section 3.2), failing to exploit any of the additional degrees of freedom from higher resolution, is a concrete and actionable finding for architecture designers.

## Suggestions
- Temper headline claims (abstract, Figure 1 caption) to clearly distinguish between what is proven under PSNR alone versus what is conjectured under perceptual constraints. A sentence like "Under PSNR constraints, theoretical capacities are orders of magnitude larger; under realistic perceptual and robustness constraints, the gap is at least several-fold" would be more accurate.
- Replace "only slightly higher LPIPS" with a precise characterization of the 4.5× LPIPS increase and brief discussion of whether this represents a capacity-quality tradeoff or evidence of unused capacity.
- Consider testing the gray-image diagnostic on 1–2 additional architecturally diverse watermarking models to strengthen the generalization claim.
- The proposed sanity checks (Section 5) are a strong secondary contribution — consider promoting them more prominently.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison to Paper Under Review |
|-------|------|-----------|-------|----------------------------------|
| Watermark-based Detection and Attribution | O08nfMzc93 | 4.50 | 1 | Weaker: limited to one watermarking method, less novel question, writing quality issues |
| SuperMark: Robust Training-free Watermarking | T0ebbDO60R | 3.75 | 1 | Weaker: incremental method contribution, less theoretical depth |
| A Recipe for Watermarking Diffusion Models | HexshmBu0P | 5.33 | 1 | Weaker: more incremental, less conceptually novel question |
| Interpretable Boundary-based Watermark | xyysYa4YvF | 4.00 | 1 | Weaker: narrower scope, less fundamental insight |
| An undetectable watermark for generative image models | jlhBFm7T2J | 6.50 | 1 | Comparable: similarly novel concept with execution gaps, but this paper's question is more fundamental for the field |
| Watermarking using Semantic-aware Speculative Sampling | LdIlnsePNt | 6.00 | 1 | Weaker than paper under review: has proof errors and disconnected theory-practice |
| Hidden in the Noise: Two-Stage Robust Watermarking | ll2nz6qwRG | 5.83 | 1 | Weaker conceptual contribution; paper under review has stronger theoretical framework and more creative experiments |
| Towards Lightweight Deep Watermarking Framework | j7b4mm7Ec9 | 7.60 | 1 | Different type of contribution (practical vs. conceptual); comparable overall quality, this paper has a more fundamental insight |
| Sparse Watermarking in LLMs | jbfDg4DgAk | 3.00 | 1 | Much weaker: limited novelty and experimental issues |
| Unleashing Information Flow: GNNs as channels | S3zKrEQpRr | 3.00 | 1 | Much weaker: less rigorous theoretical contribution |
| Limits to Reservoir Learning | Z1E0EahS5w | 3.33 | 1 | Different domain; weaker execution |
| Window-Based Hierarchical Dynamic Attention | 6j0GH40mFt | 3.40 | 1 | Different domain (compression); weaker contribution |

**Round 1 bracket: 6.0–8.0.** The paper is clearly above the borderline-reject watermarking papers (3.75–5.33) which had limited novelty or significant gaps. It is comparable to "An undetectable watermark" (6.5) and "Towards Lightweight Deep Watermarking" (7.6) in overall quality, with a stronger conceptual contribution than both but a real gap in bridging PSNR theory to perceptual practice.

**Narrowing:** The paper's strongest argument survives the PSNR-perceptual concern: if Video Seal can't embed 1024 bits into a single gray image (where PSNR ≈ perceptual quality), this proves architectural limitations exist regardless of what happens with perceptual metrics on natural images. The hierarchy of evidence (linear → tiled → handcrafted) is compelling and well-executed. The weaknesses are real but bounded — they affect the magnitude of the claimed gap, not its existence. This places the paper above the 6.0–6.5 range and into the 7.0 range: a solid contribution that asks a genuinely novel question, provides creative multi-faceted evidence, and offers actionable insights, but whose headline claims modestly overreach the formal evidence.

**Final Score: 7.0**

The paper makes a genuine conceptual contribution to the watermarking community by reframing capacity as a geometric counting problem and providing compelling evidence — both theoretical and experimental — that current architectures are far from saturation. The PSNR-perceptual gap and headline framing issues are real but do not undermine the core finding. This is a solid contribution deserving of acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>