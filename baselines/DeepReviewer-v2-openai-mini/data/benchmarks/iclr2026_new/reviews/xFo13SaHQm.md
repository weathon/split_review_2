## Summary
This paper addresses the problem of "copy-paste artifacts" in identity-consistent image generation, where models trained with reconstruction-based objectives over-replicate reference face appearance rather than generating natural variations in pose, expression, and lighting. The authors make three contributions: (1) MultiID-2M, a large-scale paired dataset of ~500K multi-person images with individual identity references; (2) MultiID-Bench, a benchmark that introduces a copy-paste metric ($\mathcal{M}_{CP}$) based on angular distances between reference, generated, and ground-truth face embeddings; and (3) WithAnyone, a FLUX-based diffusion model trained with a GT-aligned ID loss and an ID contrastive loss (InfoNCE with extended negatives) across four training phases. The paper demonstrates that WithAnyone achieves competitive identity similarity (Sim(GT)=0.460) while substantially reducing copy-paste artifacts (CP=0.144 on the single-person benchmark), outperforming dedicated face customization models on the OmniContext benchmark.

The paper is well-motivated, identifies a genuine failure mode in current ID-generation methods, and provides substantial data and benchmark resources to the community. The technical approach—particularly the GT-aligned landmark strategy and the contrastive loss with large-scale negative sampling—is thoughtful and grounded in a clear understanding of the limitations of reconstruction-based training.

However, several issues reduce confidence in the reported results. The quantitative evaluation lacks variance reporting and significance testing, making it unclear whether observed differences are statistically reliable. The "state-of-the-art" claim for identity similarity is contradicted by the paper's own Table 1 (InstantID achieves Sim(GT)=0.464 vs. Ours 0.460). The contrastive loss formula (Eq. 5) contains a formatting inconsistency that could affect implementation correctness. The user study is small (N=10) and lacks inter-rater reliability metrics. The conclusion overstates the contribution by claiming to "break the long-standing trade-off" when the evidence supports a more modest claim of achieving a better operating point. Novelty verification is deferred due to external literature search being unavailable in this run.

## Strengths
**S1 — Well-motivated problem identification.** The paper identifies a genuine and under-explored failure mode in ID-consistent generation: the copy-paste artifact where models over-replicate reference face features at the expense of controllability. The observation that standard similarity metrics (Sim(Ref)) implicitly reward direct copying is a valuable critique of current evaluation practices. Supporting evidence includes the natural face similarity variation analysis (Fig. 2, top) showing that real same-identity face pairs have similarity scores ranging from 0.30 to 0.77, while models like InstantID peak sharply at 1.0.

**S2 — Substantial data and benchmark contribution.** MultiID-2M is a large-scale resource (~500K identified multi-ID images, ~1.5M additional unpaired images, ~25K identities) that addresses the critical data bottleneck in multi-ID generation. The dataset construction pipeline (clustering ArcFace embeddings, multi-name web search, post-processing) is clearly described and publicly released. MultiID-Bench provides a standardized evaluation protocol with 435 test cases using rare, long-tail identities, which addresses the reproducibility issue of prior ad-hoc CelebA-based test sets.

**S3 — Clean copy-paste metric design.** The $\mathcal{M}_{CP}$ metric (Eq. 2) is a principled way to quantify the relative bias of generated embeddings toward the reference versus the ground truth. Using angular distance normalization by $\theta_{\mathbf{t}\mathbf{r}}$ makes the metric interpretable and comparable across different identity pairs. The decision to use Sim(GT) as the primary metric (rather than Sim(Ref)) is well-justified and corrects a methodological flaw in prior evaluation.

**S4 — Thoughtful training paradigm.** The four-phase training pipeline (reconstruction pre-training → caption alignment → paired tuning → quality tuning) is logically structured and addresses the copy-paste problem at its root cause (reconstruction-only training). The GT-aligned ID loss is a practical engineering contribution that avoids the computational cost of full denoising (PuLID) while enabling ID loss application across all noise levels. The contrastive loss with 4096 negative samples leverages the dataset's identity labels effectively.

**S5 — Comprehensive evaluation against diverse baselines.** The paper evaluates against 14 methods spanning general customization models (OmniGen, GPT-4o, FLUX.1 Kontext) and dedicated face customization models (PuLID, InstantID, UniPortrait, ID-Patch), on both single-person and multi-person subsets. The inclusion of both quantitative metrics and qualitative comparisons (Fig. 6) provides a reasonably complete picture of relative performance. The ablation study (Table 3) isolates the effects of the three key components.

## Weaknesses
**W1 — Factual inconsistency: "state-of-the-art identity similarity" claim is contradicted by reported numbers.** [Severity: Major]
The Introduction claims WithAnyone "maintains state-of-the-art identity similarity (with regard to target image)." However, Table 1 shows InstantID achieves Sim(GT)=0.464 while Ours achieves 0.460. WithAnyone is second-best, not state-of-the-art. This is a clear text-table inconsistency (F2). The same overstatement appears in the conclusion ("in many cases improving identity similarity"). The paper's own data shows Ours is comparable to but not exceeding the top similarity methods. **Fix:** Replace "state-of-the-art identity similarity" with "competitive identity similarity among dedicated face customization models" and explicitly acknowledge InstantID's higher Sim(GT) in the discussion.

**W2 — Missing variance and statistical significance in all main results.** [Severity: Major]
Tables 1, 2, and 3 report all metrics as point estimates without standard deviations, confidence intervals, or significance tests. Many comparisons are close: Sim(GT) differences of 0.004-0.006 between top methods, CP differences of 0.002 (Ours 0.144 vs OmniGen2 0.142 on the single-person subset). Without multi-seed variance (minimum 3 seeds), the reader cannot assess whether these differences are within noise. The claim "WithAnyone deviates substantially from this curve" (Section 6.1) cannot be evaluated without knowing the spread of measurements. **Fix:** Report mean±std over ≥3 seeds for all main metrics. Add a paired significance test (e.g., Wilcoxon signed-rank) comparing WithAnyone against top-3 baselines on Sim(GT) and CP. Explicitly address the OmniGen2 CP comparison where the baseline has a numerically better score.

**W3 — Contrastive loss formula (Eq. 5) has an ambiguous parentheses placement.** [Severity: Major]
The ID Contrastive Loss denominator is written as `\sum_{j=1}^M \exp(\cos(\mathbf{g}, \mathbf{n}_j))/\tau`, where the division by temperature $\tau$ is outside the exponential. Standard InfoNCE places $\tau$ inside the exponential: `\exp(\cos(\mathbf{g}, \mathbf{n}_j)/\tau)`. The numerator clearly uses the `\cos(...)/\tau` form. If implemented as written (division outside exp), the temperature scaling would not properly control distribution sharpness, potentially degrading contrastive learning. This is a critical implementation detail that must be clarified. **Fix:** Correct Eq. (5) to the standard InfoNCE form and verify the implementation in the code release matches.

**W4 — Copy-Paste metric (Eq. 2) has numerical stability issues when $\mathbf{r} \approx \mathbf{t}$.** [Severity: Major]
When the reference and ground-truth embeddings are very similar ($\theta_{\mathbf{t}\mathbf{r}}$ near zero), the denominator is clamped to $\varepsilon$, potentially producing large or unstable metric values. The paper does not discuss this corner case, report how many evaluation instances were affected, or validate the claimed $[-1, 1]$ range empirically. Since the benchmark samples rare identities and uses different images as reference and GT, $\mathbf{r} \approx \mathbf{t}$ scenarios may occur when the reference and GT happen to capture similar pose/expression. **Fix:** Report the number of test cases where $\theta_{\mathbf{t}\mathbf{r}} < \varepsilon$, analyze the metric's behavior in this regime, and add an exclusion criterion or alternative formulation for near-duplicate pairs.

**W5 — User study is underpowered and lacks statistical rigor.** [Severity: Major]
The user study uses only 10 participants. While 230 groups × 4 criteria produce many judgments, the effective statistical unit is the participant. Inter-rater reliability is not reported (Fleiss' kappa or Kendall's W). The bubble chart (Fig. 8) shows only average rankings without confidence intervals or significance tests. Participant demographics, screening criteria, and fatigue mitigation are not described. **Fix:** Report inter-rater reliability metrics, add confidence intervals to Fig. 8, include a Friedman test with post-hoc Nemenyi comparisons, and acknowledge the sample size limitation.

**W6 — "Breaking the long-standing trade-off" claim is overstated.** [Severity: Minor]
The Conclusion and Introduction claim WithAnyone "breaks the long-standing trade-off between fidelity and copying." The evidence shows WithAnyone achieves a better operating point (high Sim(GT), low CP) in the evaluated setting, but this does not demonstrate that the trade-off is fundamentally eliminated. The trade-off might reappear under different capacity, compute, or data regimes. A more defensible claim is that WithAnyone "substantially shifts the Pareto frontier" or "achieves a more favorable trade-off." This is a wording issue but appears in the paper's central narrative.

**W7 — Phase 3 paired sample ratio (50%) is not justified or ablated.** [Severity: Minor]
The paired tuning phase replaces 50% of samples with paired instances. This hyperparameter is central to the copy-paste reduction claim but no ablation study explores its sensitivity. The choice of 50% appears arbitrary. **Fix:** Add a sensitivity analysis varying the paired ratio (e.g., 25%, 50%, 75%, 100%) and report the CP/Sim(GT) trade-off for each.

**W8 — Related Work is a citation list rather than structured comparison.** [Severity: Minor]
The Single-ID Preservation paragraph contains ~20 citations without grouping by approach type or comparison axis. The reader cannot extract a clear methodological landscape. The section lacks an explicit statement of how WithAnyone differs from the strongest prior methods. **Fix:** Restructure by approach families (adapter-based, embedding injection, fine-tuning) and add a paragraph explicitly contrasting WithAnyone's approach with PuLID, InstantID, and UMO.

**W9 — GT-aligned ID loss dependency on GT landmarks is not discussed as a limitation.** [Severity: Minor]
The loss requires ground-truth landmarks during training, which limits applicability to settings without paired data. The paper claims "implicitly supervises generated landmarks" but provides no direct evidence (landmark accuracy metrics). No compute comparison with PuLID's full-denoising strategy is given.

**W10 — Conclusion lacks limitations and future work.** [Severity: Minor]
The Conclusion does not discuss any limitations (e.g., FLUX backbone dependency, potential failure cases, dataset skew toward public figures). No future work directions are suggested.

**W11 — (Deferred) Novelty verification.** External literature search was unavailable in this run. The novelty claims for MultiID-2M, MultiID-Bench, and the WithAnyone training paradigm relative to existing methods (e.g., PuLID, InstantID, XVerse, UMO, DynamicID) should be verified manually against the full body of literature. The paper's internal citations suggest partial overlap with existing multi-ID methods; the extent of residual novelty cannot be assessed without external verification.

## Score
**Final Score: 6/10**

**Score Rationale:** The paper addresses a well-motivated problem (copy-paste artifacts in ID generation) and provides substantial data/benchmark resources (MultiID-2M, MultiID-Bench) that will benefit the community. The technical approach—particularly the GT-aligned ID loss and contrastive training with extended negatives—is thoughtful and grounded.

However, the score is limited by several significant issues: (1) a factual inconsistency in the "state-of-the-art" identity similarity claim contradicted by the paper's own data (InstantID 0.464 > Ours 0.460); (2) complete absence of variance reporting and statistical significance across all quantitative results, making the reported rankings unreliable; (3) a formatting inconsistency in the contrastive loss formula (Eq. 5) that affects reproducibility; (4) an underpowered user study (N=10) without inter-rater reliability metrics; (5) overclaimed narrative about "breaking the trade-off" that exceeds what the evidence supports.

The paper's core contributions—the dataset, benchmark, and modeling framework—have clear value, but the empirical evidence is presented with insufficient rigor to fully substantiate the claimed advances. With major revisions addressing the reproducibility and statistical issues, the paper could become a solid contribution.

**Post-Revision Target: 7/10** (conditional on fixing W1-W5, adding variance reporting, correcting the contrastive loss formula, and toning down overclaims)

---

```text
ASCII Diagram — Paper Structure & Evidence Map

[Problem: ID generation models over-copy reference faces]
    |
    ├── Evidence: Fig. 2 shows InstantID peaks at Sim=1.0, 
    |             real pairs vary 0.30-0.77
    |
    ├── Root Cause: Reconstruction training with same
    |   reference and target image
    |
    └── Solution: WithAnyone (4-phase training)
        |
        ├── C1: MultiID-2M dataset (500K multi-ID + 1.5M unpaired)
        │   └── Evidence: Dataset statistics in Section 3
        |
        ├── C2: MultiID-Bench with M_CP metric
        │   └── Evidence: Eq. (1)-(2), Tables 1-2
        |
        └── C3: WithAnyone model
            ├── GT-aligned ID loss → Evidence: Table 3 (w/o GT-Align: 0.385→0.368)
            ├── ID Contrastive loss → Evidence: Table 3 (w/o Ext. Neg.: 0.368→CP 0.074)
            └── Paired tuning Phase 3 → Evidence: Table 3 (w/o Phase 3: CP 0.239→0.161)
                    |
                    └── GAPS: Missing variance, significance tests, 
                        Eq. 5 parentheses, user study N=10
```

```text
ASCII Diagram — Revision Strategy Roadmap

[W1: SOTA claim contradicted by data]
    → Fix: Replace "state-of-the-art" → "competitive"
    → Expected impact: Removes factual error

[W2: No variance/significance reporting]
    → Fix: Add 3-seed std dev + Wilcoxon tests
    → Expected impact: Enables reliable ranking assessment

[W3: Eq. (5) parentheses inconsistency]
    → Fix: Correct InfoNCE formulation
    → Expected impact: Ensures reproducibility

[W4: M_CP denominator instability]
    → Fix: Add exclusion criterion + empirical bound validation
    → Expected impact: Increases metric reliability

[W5: Underpowered user study]
    → Fix: Report inter-rater reliability + confidence intervals
    → Expected impact: Strengthens perceptual evidence

[W6: "Breaking trade-off" overclaim]
    → Fix: Replace with "substantially more favorable trade-off"
    → Expected impact: Accurate claim-evidence alignment
```

```text
ASCII Diagram — Related-Work Taxonomy Tree (Layered)

Identity-Consistent Image Generation (Root)
│
├── Branch 1: Single-ID Preservation
│   ├── Leaf 1.1: UNet/SD-era embedding injection
│   │   [e.g., DreamBooth, Textual Inversion, IP-Adapter]
│   ├── Leaf 1.2: ArcFace/CLIP cross-attention methods
│   │   [e.g., InstantID, PuLID, UniPortrait]
│   └── Leaf 1.3: DiT/FLUX-based ID preservation
│       [e.g., PuLID-FLUX, ***WithAnyone (this work)***]
│
├── Branch 2: Multi-ID Preservation
│   ├── Leaf 2.1: VAE-concatenation methods
│   │   [e.g., XVerse, UMO → prone to copy-paste]
│   ├── Leaf 2.2: Decoupled attention methods
│   │   [e.g., DynamicID → improved control, limited data]
│   └── Leaf 2.3: Paired-training with contrastive loss
│       [***WithAnyone (this work)*** → mitigates copy-paste]
│
└── Branch 3: Datasets & Benchmarks
    ├── Leaf 3.1: Single-ID datasets
    │   [e.g., CelebA, FFHQ, FaceID-6M]
    ├── Leaf 3.2: Multi-ID datasets without paired refs
    │   [e.g., IMdB, M3ID]
    └── Leaf 3.3: Multi-ID with paired references
        [***MultiID-2M (this work)***, MultiID-Bench]

Note: Novelty verification is deferred to manual literature 
search (external search unavailable in this run). The 
positioning above is based solely on manuscript claims.
```