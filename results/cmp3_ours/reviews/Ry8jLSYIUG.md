Now I have enough information for calibration. Let me write the final review.

## Final Review

**Calibration Summary:**

I examined multiple anchor papers from the human review corpus. Key anchors:

| Anchor | Avg Score | Round | Comparison |
|--------|-----------|-------|------------|
| "Limits to Reservoir Learning" (Z1E0EahS5w) | 3.33 | 1 | Much weaker — unclear contribution, poor presentation. Our paper is far stronger. |
| "SuperMark" (T0ebbDO60R) | 3.75 | 1 | Weaker — overclaims, lacks novelty in core method. Our paper has genuine theoretical novelty. |
| "SAT-LDM" (ETFfXGM3e4) | 5.50 | 1 | Similar — method paper with some theory, clear limitations acknowledged. |
| "A Recipe for Watermarking Diffusion Models" (HexshmBu0P) | 5.33 | 2 | Similar — analysis-oriented paper with practical guidelines and moderate framing issues. |
| "Hidden in the Noise" (ll2nz6qwRG) | 5.83 | 1 | Slightly stronger — accepted, solid method with theory, minor weaknesses. |
| "Shallow Diffuse" (1IwoEFyErz) | 6.00 | 1 | Stronger — clean theory+empirics, though rejected due to missing ablations. |
| "An Undetectable Watermark" (jlhBFm7T2J) | 6.50 | 2 | Stronger — accepted, novel theoretical guarantee with clean experiments. |

**Round 1 bracket:** 4.5–6.5. **Round 2 narrowing:** The paper's strongest contribution (PSNR-only bounds + controlled experiments) is solid, but the framing overreach and the Chunky Seal weakness are real. Compared to "Hidden in the Noise" (5.83, accepted) and "A Recipe for Watermarking" (5.33, rejected), the paper sits between them — stronger theoretical novelty than "A Recipe" but with more significant framing issues than "Hidden in the Noise." I calibrate to **5.5**.

---

## Summary

This paper asks whether current image watermarking methods are near fundamental limits or have substantial unused headroom. The authors develop a geometric bounding framework for watermarking capacity under PSNR constraints (rigorous) and linear robustness constraints (heuristic). They then demonstrate empirically that Video Seal, a state-of-the-art model, fails to approach even the PSNR-only bounds in a maximally simplified setting (single gray image, no augmentations), while a handcrafted encoder nearly matches the bound. A scaled-up model (Chunky Seal) achieves 4× higher capacity (1024 bits) at 90× parameter cost. The core contribution is the bounding framework and the experimental demonstration of an architectural bottleneck.

## Strengths

1. **Genuinely novel theoretical contribution.** The PSNR-only bounding framework (Section 2.3–2.4, the box-ball counting problem) is the first serious attempt I am aware of to bound watermarking capacity from first principles for realistic (non-Gaussian) image models. The three-case treatment (cube-in-ball, ball-in-cube, non-trivial intersection) is clear and well-executed.

2. **Clean, informative controlled experiments.** Section 3 is well-designed: stripping away all complexity (single gray image, PSNR-only constraint, no augmentations) and progressively testing Video Seal → linear model → tiled model → handcrafted encoder. The finding that a 32×32px model achieves the same capacity as a 256×256px model (Figure 5, Table 1) is a striking demonstration of an architectural bottleneck.

3. **The handcrafted encoder (Equation 2) proves the PSNR-only bounds are not vacuous.** Providing a concrete construction that nearly matches the theoretical bound is the strongest evidence in the paper.

4. **The proposed sanity checks (Section 5)** are useful methodological guidelines for the community.

## Weaknesses

### Fatal
None.

### Major

1. **"Orders of magnitude" framing conflates PSNR-only and robustness-constrained bounds without sufficient caveat in the abstract and introduction.** The abstract claims "theoretical capacities are orders of magnitude larger than what current models achieve" under "PSNR and linear robustness constraints." This is well-supported for the PSNR-only case (~2.5 bpp at 45 dB vs 0.001 bpp in practice) and for the heuristic robustness bounds (Bounds 10–12, suggesting ≈0.5 bpp). However, the paper's own rigorous lower bound (Bound 13, Table 2) tells a more modest story: for Crop&Rescale 75% at 42 dB, it gives 904 bits — comparable to Chunky Seal's 1024 bits. While Bound 13 is explicitly described as "extremely conservative and unrealistic," the headline narrative does not distinguish between bound regimes. A reader who does not study Table 2 carefully will overestimate the proven gap under realistic robustness constraints. This is a framing problem, not a factual error, but it materially affects how the contribution is perceived.

2. **Chunky Seal provides weak evidence for easy capacity scaling, in partial tension with the paper's optimistic framing.** Table 3 shows Chunky Seal (1024 bits) requires a 90× larger embedder and 23× larger extractor than Video Seal (256 bits), with some quality/robustness degradation (LPIPS 0.0085 vs 0.0019, lower bit accuracy on 6 of 10 transforms). The paper acknowledges this in the conclusion ("we do not suggest that naively scaling Chunky Seal is a practical path forward"), but the abstract frames it as "proof that larger capacities are indeed possible." A 4× capacity gain at 90× parameter cost is inefficient scaling; if anything, it suggests architectural *design* (not just size) is the bottleneck, which undercuts the optimistic headroom narrative.

### Minor

1. **The controlled experiments (Section 3) test only the PSNR-only case.** The finding that models fail even when all robustness constraints are stripped away rules out real-world complexity as *the* explanation for the gap, but it does not independently quantify how much of the robustness-constrained gap is architectural vs. inherent to the task. The claim that robustness "cannot fully explain the low watermarking capacity" (Section 2.5) relies primarily on the theoretical bounds, not these experiments.

2. **No diagnosis of why Video Seal fails to scale.** The paper attributes the gap to "architectural limitations" without investigating the specific failure mode (vanishing gradients, poor optimization landscape, representational bottlenecks). This limits actionable guidance for future architecture design.

3. **No baseline comparison with other DNN architectures in the simplified setup.** Video Seal is compared against trivial models (linear, handcrafted). A small CNN or MLP baseline would help clarify whether the bottleneck is specific to Video Seal's architecture or a more general DNN issue.

4. **Inference cost and latency not reported for Chunky Seal.** Given the model is dramatically larger, practical considerations matter beyond the limitation statement in the conclusion.

### Trivial
None.

## Nice-to-Haves

- Include the conservative Bound 13 as a separate reference curve in Figure 1 so readers can immediately see the gap between heuristic and rigorous bounds.
- Extend the handcrafted encoder to show partial behavior under robustness constraints (e.g., combined with error-correcting codes).
- Report statistical significance for the Chunky Seal vs. Video Seal comparison.

## Removed Points

- **Data distribution argument (Harsh Critic Critical Issue 4):** The critic argues the VQ-VAE-based estimate is not rigorous because natural images concentrate on a low-dimensional manifold. The paper's analysis is explicitly *conservative*: it assumes ALL 2^10240 representable images could fall in the same PSNR ball. If the critic's objection is correct (fewer images collide), the capacity reduction would be *smaller*, strengthening the paper's conclusion. This objection does not weaken the paper and is removed.
- **"Orders of magnitude" as a fatal flaw:** The critic frames this as structural/invalidating. It is a real framing imprecision but not fatal — the PSNR-only bounds and heuristic robustness bounds both support the claim, and Bound 13 is explicitly caveated as unrealistic. Demoted from Fatal to Major.
- **Criticism about Costa (1983) citation being inapplicable:** The Costa reference is supplementary context ("This aligns with prior findings"), not a core pillar. Removing the reference changes nothing. Removed.
- **Generic formatting/style nitpicks:** Removed per filtering rules.
- **Missing appendix content/completeness concerns:** Removed per filtering rules (parser strips appendices).

## Novel Insights

The reviews surface an interesting tension that is latent in the paper itself. The heuristic robustness bounds (Bounds 10–12) and the conservative bound (Bound 13) span a wide gulf — the heuristic bounds suggest ≈100,000 bits, while the conservative bound gives 904 bits for the same setting. The paper's "orders of magnitude" narrative relies on trusting the heuristic bounds, while the conservative bound tells a much more modest story (1–4× gap). The paper is transparent about this but does not explicitly acknowledge how radically different the two narratives are. A sharper paper would center this very tension as a finding: "the gap between heuristic and provable bounds is itself large, and narrowing it is an important open problem."

## Suggestions

1. Reframe the abstract and introduction to explicitly distinguish between the PSNR-only capacity gap (rigorous, orders of magnitude) and the robustness-constrained gap (depends on which bound regime one trusts).
2. Add the conservative Bound 13 as a reference curve in Figure 1 so the gap between heuristic and rigorous bounds is visible at a glance.
3. Acknowledge Chunky Seal's scaling inefficiency more prominently (not just in the conclusion) to avoid misleading readers about the ease of capacity scaling.
4. Diagnose *why* Video Seal fails at higher capacities (gradient analysis, representation rank, etc.) to provide actionable insight.

## Score and Decision

**Round 1 bracket (initial):** 4.5–6.5  
**Round 2 narrowing:** Compared to SAT-LDM (5.50, rejected), Hidden in the Noise (5.83, accepted), and A Recipe for Watermarking (5.33, rejected), the paper has stronger theoretical novelty than "A Recipe" but more significant framing issues than "Hidden in the Noise." The controlled experiments and handcrafted encoder are genuine strengths. The framing overreach and weak Chunky Seal evidence are real but addressable weaknesses.  

**MY FINAL SCORE: <score>5.5</score>**
**MY FINAL DECISION: <decision>Reject</decision>**