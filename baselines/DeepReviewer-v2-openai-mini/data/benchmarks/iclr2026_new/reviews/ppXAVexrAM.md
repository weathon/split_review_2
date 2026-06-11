## Summary
# Final Review Report

## Summary

This paper introduces ARSS, a framework that applies a GPT-style decoder-only autoregressive transformer to novel view synthesis (NVS) from a single input image conditioned on a predefined camera trajectory. The core technical contributions are: (C1) a video tokenizer (based on VidTok/FSQ) that encodes multi-view image sequences into discrete tokens with temporal consistency; (C2) a camera autoencoder that converts Plücker raymaps into per-token 3D positional guidance tokens; and (C3) a hybrid token permutation strategy that randomly shuffles tokens within each spatial frame while preserving temporal order, enabling a causal transformer to model bidirectional spatial context. The method is evaluated on RealEstate10K, ACID, and zero-shot on DL3DV, achieving competitive results against diffusion-based baselines (SEVA, Genwarp, MotionCtrl, ViewCrafter) and feed-forward methods (LVSM, RayZer).

The paper tackles a timely and interesting question — whether causal AR models can serve as an alternative paradigm to diffusion models for sequential view synthesis. The idea of using per-token 3D positional conditioning from Plücker rays is an elegant adaptation of AR visual generation to the multi-view setting. However, the current manuscript has several significant weaknesses that must be addressed before publication: (1) experimental results are reported without variance or significance testing, making it unclear whether observed gains are reliable; (2) the claim of "outperforming SOTA" is contradicted by the paper's own Table 1 (ARSS trails SEVA on SSIM and FID); (3) the training loss in Eq. (7) is incompletely specified, and Eq. (5) contains a symbol typo; (4) the ablation tables use inconsistent metrics (FID vs. FVD) without justification; (5) novelty claims cannot be fully verified due to deferred external literature comparison. 

**Novelty note:** Per the runtime retrieval status, external paper search was not available in this run. All novelty/comparison conclusions below are marked as deferred manual verification. The authors' claim of being "first" to apply GPT-style causal AR to NVS with camera control appears plausible given the literature surveyed in the paper, but requires independent verification against the complete prior-art landscape.

## Strengths
**S1. Timely and well-motivated research direction.** The paper identifies a genuine gap in the NVS literature: most diffusion-based methods generate all target views simultaneously, which limits their ability to incrementally extend sequences or condition on previously generated content. Applying causal autoregressive models to this problem is a natural and interesting idea that could open a new paradigm for sequential view synthesis, particularly for world-model applications requiring long-horizon generation.

**S2. Clean technical design with three complementary components.** The method decomposes the AR NVS problem into three modular components (video tokenizer, camera autoencoder, autoregressive transformer with spatial permutation), each addressing a specific challenge. The use of Plücker raymaps as per-token 3D positional guidance (via the camera autoencoder) is a technically sound way to inject geometric information into the autoregressive generation process, and the hybrid spatial-permutation strategy is a principled adaptation of bidirectional visual data to causal modeling.

**S3. Competitive experimental results across multiple datasets.** Table 1 shows that ARSS achieves the best PSNR and LPIPS on both RealEstate10K and ACID among all compared methods, and the best FVD on RealEstate10K. The error accumulation analysis (Figure 6) indicates that ARSS maintains higher quality over longer sequences compared to baselines, which is a meaningful result for the claimed advantage of causal generation. The zero-shot evaluation on DL3DV and the AI-generated image experiments provide初步 evidence of generalization.

**S4. Reasonable ablation studies.** The two ablation experiments (token permutation strategy and tokenizer type) directly validate the key design choices. The comparison between raster, full permutation, and the proposed spatial-only permutation cleanly demonstrates the importance of preserving temporal order. The tokenizer ablation shows that temporal encoding in the video tokenizer contributes substantially to performance, especially temporal consistency (FVD improvement of ~62%).

**S5. Transparent about limitations and future work.** The Discussion section acknowledges that generation quality is limited by the tokenizer and that the method is trained from scratch at relatively low resolution. This candid assessment helps readers understand the current scope and limitations of the approach.

## Weaknesses
**W1. Experimental reporting lacks statistical rigor (Critical).** 
All results in Table 1, Table 2, and Table 3 are reported as point estimates without standard deviations, confidence intervals, or significance tests. Given that several key margins are small (e.g., +0.29 PSNR over SEVA on RealEstate10K, −6.6% SSIM behind SEVA), readers cannot assess whether observed differences are statistically meaningful or within noise. The paper does not state how many random seeds were used, whether the same train/val/test splits were applied consistently across methods, or whether paired significance tests were conducted. This is a fundamental reproducibility and credibility gap.

*Required action (Must):* Report mean±std over at least 3 random seeds for all metrics and all methods. Add pairwise significance tests (e.g., paired bootstrap or Wilcoxon) between ARSS and the strongest baseline (SEVA) for the primary metrics. Disclose the exact data splits used for evaluation.

**W2. Overclaiming of "outperforms SOTA" contradicted by own data (Critical).**
The Introduction (line 71) and Discussion (line 356) both claim that ARSS "outperforms current state-of-the-art methods" and "outperforms state-of-the-art methods leveraging diffusion models and transformers." However, Table 1 shows a mixed picture: SEVA achieves higher SSIM (0.670 vs 0.624 on Re10K, 0.664 vs 0.623 on ACID) and lower FID (46.98 vs 47.60 on Re10K, 33.16 vs 47.76 on ACID). ARSS leads in PSNR and LPIPS but trails in these other metrics. Blanket "outperforms" language is misleading and must be replaced with precise, metric-specific comparisons.

*Required action (Must):* Reword all "outperforms" claims to reflect the metric-by-metric reality. For example: "ARSS achieves competitive or superior results on perceptual quality (LPIPS) and temporal consistency (FVD), while geometric fidelity (SSIM) and distributional similarity (FID) trail the strongest diffusion-based baseline."

**W3. Incomplete/correctness issues in mathematical formulations (Major).**
Two specific issues in the Method section:
(a) Eq. (7) writes $\mathcal{L} = CE(f_\theta([\mathcal{S}, ...]))$ with a single argument, but the cross-entropy loss requires two arguments (predictions and targets). Compare with Eq. (3) which correctly provides both. The intended target sequence is not specified, making the training objective ambiguous.
(b) Eq. (5) and its description contain a symbol error: the text reads "d is the normalized camera ray direction, d is the momentum term" — the second "d" should be "m." Additionally, the four loss weights $\lambda_i$ are never specified, reducing reproducibility. A spelling error ("perpetual loss" → "perceptual loss") further indicates insufficient proofreading.

*Required action (Must):* Fix Eq. (7) to show both the input and target sequences explicitly. Fix the symbol typo in Eq. (5). Report the $\lambda$ values used in experiments.

**W4. Inconsistent metrics across ablation tables raises cherry-picking concern (Major).**
Table 2 (token permutation ablation) reports PSNR, SSIM, LPIPS, and **FID**, while Table 3 (tokenizer ablation) reports the same first three metrics but replaces FID with **FVD**. The text claims Table 3 uses FVD "to validate temporal consistency," but temporal consistency is also relevant for the permutation ablation. Reporting FID in one table and FVD in another without explanation makes the experimental design appear selective. 

*Required action (Must):* Report both FID and FVD in both ablation tables, or provide a clear, principled reason for the metric choice. If the goal is to measure temporal consistency, FVD should be reported in both tables.

**W5. Missing experiment setup details (Major).**
Several crucial experimental details are absent: (a) data splitting protocol for RealEstate10K and ACID (exact training/validation/test proportions, whether overlapping scenes exist across splits); (b) whether baselines were evaluated using official checkpoints or retrained, and whether any hyperparameter tuning was performed for each baseline; (c) no reporting of model parameters, training time, or inference speed for any method. Without these, the fairness of the comparison and the practical feasibility of the approach cannot be assessed.

*Required action (Must):* Add a supplementary table or appendix section with all data split details, baseline evaluation protocols, and compute cost comparisons (parameters, FLOPs, training hours, inference speed).

**W6. Error accumulation analysis is qualitative only (Moderate).**
Figure 6 is discussed in terms of visual slope comparisons ("noticeably flatter"), but no quantitative degradation rates are reported. The paper's main claimed advantage is causal sequential generation with less error accumulation — this should be quantified explicitly (e.g., PSNR/frame degradation rate, cumulative error at final frame).

*Required action (Nice-to-have):* Report per-frame degradation rates and the cumulative error at the last frame for all methods. Include a table with numerical values corresponding to Figure 6.

**W7. Limited novelty verification (Moderate).**
The paper claims to be "the first that applies the GPT-style causal autoregressive model in novel view generation with camera control." While this is plausible, external literature verification was not possible in this review run (Retrieval-Disabled Mode). Additionally, the Related Work section does not provide a systematic head-to-head comparison table with decision-relevant axes (sequential generation, camera control, per-token 3D conditioning), making it hard for readers to verify the novelty claim from the paper alone.

*Required action (Nice-to-have):* Add a comparison table explicitly showing which capabilities each prior method supports vs. lacks, with direct column references to the paper's three contribution axes.

**W8. Resolution and domain limitations understated (Moderate).**
The method operates at 256×256 resolution, which is lower than many recent diffusion-based NVS methods (e.g., SEVA operates at higher resolution with large-scale pretraining). The limitation paragraph only mentions tokenizer quality, but the resolution cap, the reliance on predefined camera trajectories, and the limited domain coverage (indoor/outdoor real estate and aerial) are equally important boundaries that should be disclosed.

*Required action (Nice-to-have):* Expand the limitations section to cover resolution, trajectory dependence, and domain coverage explicitly.

## Score
**Final Score: 5.5/10**

**Rationale:** The paper addresses a timely and well-motivated research question with a technically clean design. The core idea of adapting causal AR models to NVS with per-token 3D positional conditioning is novel and interesting. However, the score is constrained by:
- **W1/W2 (Validity risk):** The experimental claims of "outperforming SOTA" are not supported by the paper's own mixed results, and the lack of statistical rigor prevents assessment of whether even the positive results are reliable.
- **W3 (Technical correctness):** Incomplete training objective (Eq. 7) and symbol errors in Eq. (5) reduce confidence in methodological precision.
- **W4 (Experimental rigor):** Inconsistent ablation metrics raise concerns about selective reporting.
- **Novelty verification is deferred** pending external literature comparison, which adds uncertainty.

The paper shows promise but requires substantial revisions to bring claims in line with evidence, fix mathematical formulations, and add statistical rigor before it meets the bar for publication.

---

### ASCII Diagrams

**ASCII Diagram A — Paper Structure & Evidence Map**
```text
[Claim: Causal AR models can generate multi-view sequences with camera control]
   │
   ├── C1: Video tokenizer enables temporally consistent discrete tokens
   │   └── Evidence: Table 3 (FVD 52.56 vs 137.68 for VQ tokenizer)
   │
   ├── C2: Camera autoencoder provides per-token 3D positional guidance
   │   └── Evidence: Eq. (5) camera loss formulation (λ weights unspecified)
   │   └── Gap: No ablation isolating camera token contribution
   │
   ├── C3: Spatial-only permutation enables bidirectional context in causal AR
   │   └── Evidence: Table 2 (PSNR 19.22 vs 16.29 for raster)
   │
   └── Overall: ARSS achieves competitive NVS quality
       └── Evidence: Table 1 (PSNR 19.02, LPIPS 0.269 on Re10K)
       └── Risk: No variance reported; SSIM/FID trail SEVA
       
[Key Gaps: Statistical testing missing | Eq. (7) incomplete | Overclaim in text]
```

**ASCII Diagram B — Revision Strategy Roadmap**
```text
Priority 0 (Must, before acceptance):
┌──────────────────────────────────────────────────────┐
│ W2: Reword all "outperforms SOTA" → metric-specific   │
│ W3: Fix Eq. (7) target argument, Eq. (5) symbol typo  │
│ W1: Add variance reporting + significance tests        │
│ W4: Unify ablation metrics (both FID+FVD in both)     │
└──────────────────────────────────────────────────────┘
         ↓
Priority 1 (Must, strengthens credibility):
┌──────────────────────────────────────────────────────┐
│ W5: Add data splits, baseline protocols, compute cost  │
│ W6: Quantify error accumulation rates per frame        │
└──────────────────────────────────────────────────────┘
         ↓
Priority 2 (Nice-to-have, improves completeness):
┌──────────────────────────────────────────────────────┐
│ W7: Add capability comparison table for novelty        │
│ W8: Expand limitations (resolution, trajectory, domain)│
│    Add camera token ablation to validate C2             │
└──────────────────────────────────────────────────────┘
```

**ASCII Diagram C — Related-Work Taxonomy Tree (Layered)**
```text
Novel View Synthesis Approaches (Root)
├── Branch 1: Diffusion-based Methods
│   ├── Leaf 1.1: Joint multi-view diffusion [SEVA, Genwarp]
│   │   - Generates all target views simultaneously
│   │   - Limitation: cannot incrementally extend
│   ├── Leaf 1.2: Video diffusion for 3D prior [ViewCrafter, MotionCtrl]
│   │   - Uses temporal consistency as inductive bias
│   │   - Limitation: requires full sequence at inference
│   └── Leaf 1.3: Warp-and-inpaint pipeline [Genwarp]
│       - Relies on depth accuracy
│       - Limitation: error accumulation from depth prediction
│
├── Branch 2: Feed-forward / Transformer Methods
│   ├── Leaf 2.1: Bidirectional transformer NVS [LVSM]
│   │   - Directly predicts visual tokens
│   │   - Limitation: no causal generation, blurry boundaries
│   └── Leaf 2.2: Explicit 3D representation [RayZer]
│       - Uses ray-based rendering
│       - Limitation: poor perceptual quality (LPIPS 0.639)
│
└── Branch 3: Autoregressive Visual Generation
    ├── Leaf 3.1: Single-image raster-scan AR [LlamaGen, VQGAN]
    │   - Generates images in fixed order
    │   - Limitation: no multi-view or camera control
    ├── Leaf 3.2: Permuted-order image AR [VAR, RAR, MAR]
    │   - Random spatial permutation + positional tokens
    │   - Limitation: single-image only, no 3D conditioning
    └── ★ ARSS (This paper) — Leaf 3.3: Multi-view AR with camera tokens
        - Spatial permutation + temporal order preservation
        - Per-token 3D Plücker conditioning
        - Novelty: first to combine causal AR + per-token camera control for NVS
```

---

The paper makes a solid contribution to an emerging direction (AR-based NVS), but the current evidentiary standards (no variance, overclaimed narrative, incomplete equations) prevent it from being a fully convincing publication. A focused revision addressing W1-W4 would substantially strengthen the paper.

**External literature verification not available in this run; novelty and comparison conclusions are marked as deferred manual verification.**