## Summary
# Final Review Report

## Summary

This paper proposes **PI-CCA (Prompt-Invariant CCA Certificates)**, a replay-free continual learning framework for vision-language models (VLMs). The core idea is to preserve cross-modal alignment geometry (canonical correlations and subspaces from CCA) through a compact, sketch-based certificate that constrains training without storing past data. An additional prompt-invariance loss averages over randomized prompt perturbations to reduce sensitivity to phrasing variations.

The paper has three main contribution claims:
- **C1 (Insight)**: Reframing forgetting in VL-CL as alignment-geometry drift rather than proxy-signal degradation, offering a principled new perspective.
- **C2 (Capability)**: A replay-free, constant-memory consolidation mechanism using CCA certificates, compatible with LoRA-based efficient tuning, with explicit prompt-robustness.
- **C3 (Performance)**: State-of-the-art results among replay-free methods across four VL-CL benchmarks (MTIL, X-TAIL, VLCL, ConStruct-VL), with analyses linking geometry stability to retention.

The method is technically well-grounded in CCA theory, uses random sketching for memory efficiency, and provides a clean solution to a practically important problem. However, several concerns limit the confidence in the reported results: (1) suspiciously perfect correlation coefficients (Pearson r=1.00) in the geometry-performance analysis, (2) missing variance reporting in main classification results, (3) a likely formula error in the streaming estimation description, and (4) no explicit limitations discussion. Novelty and literature positioning cannot be fully verified in this run due to Retrieval-Disabled Mode.

## Strengths
**1. Principled problem formulation.** The paper's core insight — that forgetting in VL-CL should be understood as alignment-geometry drift rather than proxy-signal degradation — is conceptually sound and well-motivated. This reframing moves beyond ad-hoc regularization and provides a clear optimization target: preserving the canonical correlation structure of the whitened cross-modal covariance.

**2. Technically clean and elegant solution.** The CCA certificate mechanism is elegant: it captures both spectral (correlation strengths) and directional (subspace) invariants using random sketching to achieve constant memory. The prompt-invariance extension via projector averaging is a natural addition that avoids Procrustes alignment issues. The method is generator-free and replay-free, addressing practical privacy and storage concerns.

**3. Strong empirical scope.** The evaluation covers four distinct VL-CL tracks (classification, task-agnostic classification, retrieval, structured concepts) with multiple metrics per track. The ablation study (Table 3) systematically isolates each loss term's contribution, confirming that both spectral and subspace terms are necessary. The certificate capacity Pareto analysis (Figure 2) provides practical guidance for choosing k and h.

**4. Good diagnostic analysis.** The correlation analysis between geometry drift and performance drop (Figure 3), while raising statistical concerns, represents a commendable effort to go beyond "our method works" and explain *why* it works. The prompt invariance stress test (Figure 4) and task-order sensitivity (Figure 5) add robustness evidence.

**5. Reproducibility-oriented documentation.** The paper includes a detailed reproducibility statement, promises code release, and describes key implementation choices (EMA rates, power iteration steps, sketch types) that facilitate reproduction.

## Weaknesses
### W1. Suspiciously perfect correlation coefficients in geometry-performance analysis [Major, Validity]

**Location**: Page 8 - Figure 3 and surrounding text (Section 4.3)

**Evidence and Impact**: The paper reports Pearson r = 1.00 and Spearman ρ = 1.00 for multiple panels in Figure 3 showing the relationship between geometry drift and performance drop. Perfect linear correlations are essentially impossible for real empirical data collected from sweeps over "certificate size, EMAs, invariance strength, whitening, pairing, LoRA capacity/LR, sketch type" — each of which introduces independent stochastic variation from training. If these values arise from a small sample size (e.g., n ≤ 5), the uncertainty bounds would be extremely wide, making the reported values misleading. If they arise from a deterministic relationship where performance drop is defined as a function of drift by construction, this must be explicitly disclosed. As presented, the perfect correlations undermine the credibility of the paper's central diagnostic claim that "preserving CCA geometry predicts retention."

**Required Action**: (a) Report the sample size n for each panel. (b) Provide p-values and 95% confidence intervals for each correlation coefficient using Fisher z-transformation or bootstrap. (c) If n is small, add more perturbation configurations to increase statistical power. (d) Show raw data points with jitter to allow visual inspection. (e) If the relationship is deterministic by construction, state this explicitly and rephrase from "correlation evidence" to "theoretical consistency check."

---

### W2. Missing variance reporting in main classification results [Major, Reproducibility]

**Location**: Page 6 - Table 1 (MTIL and X-TAIL results)

**Evidence and Impact**: Table 1 reports point estimates for all methods without any standard deviations, confidence intervals, or significance tests, while Table 2 (VLCL, ConStruct-VL) includes ± intervals. This inconsistency is problematic because several improvements are modest (e.g., PI-CCA vs C-CLIP on MTIL Avg: 76.8 vs 75.2 = +1.6 pts; vs RAIL on X-TAIL Avg: 68.1 vs 67.4 = +0.7 pts; vs DIKI on X-TAIL Last: 66.9 vs 65.8 = +1.1 pts). Without variance estimates, readers cannot determine whether these differences are statistically reliable or within run-to-run noise. The claim of "state-of-the-art performance" is therefore not properly supported for these tracks.

**Required Action**: Report mean ± std over at least 3 seeds for all entries in Table 1, or provide a supplementary table with per-seed values. Add significance tests (e.g., paired t-test or Mann-Whitney U) against the strongest baseline for each metric.

---

### W3. Likely formula error in streaming whitened cross-covariance [Major, Correctness]

**Location**: Page 5 - Section 3.4, text after Eq (12)

**Evidence and Impact**: The text states "We then form $\mathbf{M}^{(t)} = (\sum_{v=1}^t \mathbf{S}_v^{(t)})^{-1/2} (\sum_{v=1}^t \mathbf{S}_v^{(t)})^{-1/2}$". This contains two problems: (1) The notation $\mathbf{S}_v^{(t)}$ is used, but $\mathbf{S}_v$ was previously defined as the sketched canonical basis; the EMA-maintained quantities are $\Sigma_{vv}, \Sigma_{tt}, \Sigma_{vt}$, not $\mathbf{S}_v$. (2) The same term is repeated (both factors are $(\sum_{v=1}^t \mathbf{S}_v^{(t)})^{-1/2}$), which would yield a symmetric matrix rather than the whitened cross-covariance $\Sigma_{vv}^{-1/2} \Sigma_{vt} \Sigma_{tt}^{-1/2}$ from Eq (2). This appears to be a copy-paste error that would prevent correct implementation.

**Required Action**: Correct to $\mathbf{M}^{(t)} = (\Sigma_{vv}^{(t)})^{-1/2} \Sigma_{vt}^{(t)} (\Sigma_{tt}^{(t)})^{-1/2}$. Also verify that the pseudocode in Appendix A.1 (Algorithm 1) uses the correct formula.

---

### W4. Missing limitations and boundary discussion [Minor, Completeness]

**Location**: Page 9 - Conclusion (Section 5)

**Evidence and Impact**: The conclusion summarizes validated findings but does not discuss any limitations of the proposed approach. Important boundaries include: (1) reliance on the pre-continual model's alignment quality as the reference certificate — if the initial model's alignment is already suboptimal, the certificate may constrain adaptation unhelpfully; (2) sketch approximation error when h is too small relative to intrinsic subspace dimensionality; (3) the restriction to LoRA-based adaptation studied here. The ethical statement and reproducibility statement are present, but a dedicated limitations paragraph would improve scientific completeness.

**Required Action**: Add 3-4 sentences acknowledging the above limitations before the future work sentence.

---

### W5. Introduction narrative density [Minor, Clarity]

**Location**: Page 1 - Introduction (Section 1)

**Evidence and Impact**: The first introduction paragraph opens with eight inline citations before the reader understands the problem. This reduces readability and makes it harder for non-specialist readers to follow the motivation. The literature-review and gap-analysis functions are combined in the second paragraph, reducing the visibility of the key insight (proxy-signal limitation). The contribution list uses "Insight" before "Capability," which reverses the natural logical flow (describe what the method does before the conceptual reframing).

**Required Action**: Restructure the introduction to: (a) Open with 1-2 sentences of domain motivation without heavy citations, (b) state the VL-CL problem, (c) provide a compact gap analysis, (d) present the research question and method intuition, then (e) list contributions in a natural order (Capability → Insight → Empirical evidence).

---

### W6. Insufficient main-text hyperparameter disclosure [Minor, Reproducibility]

**Location**: Page 5-6 - Experiment setup and method sections

**Evidence and Impact**: Key experimental details (backbone model variant, LoRA rank, hyperparameter values for λ₁, λ₂, λ₃, ξ, η, α, β, k, h) are deferred to the appendix with no summary in the main text. While the reproducibility statement promises full details, the main text should at minimum state the backbone, LoRA rank, and primary certificate dimensions to give readers an immediate sense of the experimental configuration.

**Required Action**: Add a short paragraph at the end of Section 4.1 summarizing: "All experiments use [backbone] with LoRA rank r=[?]. Certificate size (k=? , h=?) with λ₁=?, λ₂=?, λ₃=?, α=?, β=?. Results averaged over X seeds."

---

### W7. Novelty and literature comparison unverifiable in this run [Verification, Deferred]

**Location**: Throughout

**Evidence and Impact**: Due to Retrieval-Disabled Mode (paper_search unavailable), external literature verification could not be performed. The paper's novelty claims — particularly the geometry-first reframing of forgetting and the CCA certificate approach — cannot be independently verified against the prior work cited in the paper or potentially missing baselines. All novelty and comparison conclusions in this review are deferred for manual verification. Readers should consult the cited literature (ZSCL, Mod-X, C-CLIP, CTP, DKR, etc.) to assess whether the CCA-based alignment certificate is genuinely novel or overlaps with existing geometry-regularization approaches.

## Score
**Final Score: 6/10**

**Score Rationale**: The paper presents a conceptually interesting idea (geometry-first alignment preservation via CCA certificates) with strong practical motivation (replay-free, constant-memory VL-CL). The method is technically sound and the evaluation covers multiple benchmarks. However, the score is constrained by three significant concerns: (1) the suspiciously perfect correlation coefficients (Pearson r=1.00) in the central diagnostic analysis undermine confidence in the paper's main explanatory claim; (2) missing variance estimates in the primary classification results (Table 1) leave key performance claims unverifiable; (3) a likely formula error in the streaming estimation section suggests incomplete proofreading. These issues are fixable but currently prevent a higher score. Novelty assessment is deferred due to retrieval unavailability.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: Replay-free VL-CL requires preserving zero-shot]
    |
    v
[Claim C1 - Insight: Forgetting = alignment-geometry drift]
    |-- Evidence: Conceptual argument + ablation (Table 3)
    |-- Gap: No counterfactual test separating drift from other causes
    |
    v
[Claim C2 - Capability: CCA certificate + prompt invariance]
    |-- Evidence: Ablation (Table 3), certificate sweep (Fig 2)
    |-- Gap: Formula error in Sec 3.4 may affect streaming implementation
    |
    v
[Claim C3 - Performance: SOTA among replay-free methods]
    |-- Evidence: Tables 1-2, Figs 3-5
    |-- Gap W1: Perfect correlations (r=1.00) in Fig 3 unreliable
    |-- Gap W2: No variance in Table 1 -> significance uncertain
    |-- Gap W3: Modest margins (+0.6 to +1.6 pts) vs strong baselines
    |
    v
[Core Conclusion: Alignment-invariant preservation improves retention]
    |-- Support: Ablations + Pareto analysis + task-order robustness
    |-- Risk: Without fixable correlation evidence, "reliably predicts"
    |          claim is over-stated
```

---

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority | Problem                    | Fix                              | Expected Gain
---------|----------------------------|----------------------------------|----------------------
P0 (Must)| W1: Perfect correlations   | Report n, CI, p-values;          | Core evidence credibility
         |    in Fig 3                | add more configs if n small      |
P0 (Must)| W2: Missing variance in    | Add mean±std over ≥3 seeds       | Statistical reliability
         |    Table 1                 | to Table 1; add significance     | for SOTA claim
P0 (Must)| W3: Formula error in       | Correct M^(t) formula;           | Correctness & reproducibility
         |    Sec 3.4                 | verify Algorithm 1               |
P1 (Must)| W4: Missing limitations    | Add 3-4 sentence limitations     | Scientific completeness
         |    in Conclusion           | paragraph                        |
P1 (Nice)| W5: Intro narrative        | Restructure for clarity;         | Readability
         |    density                 | reduce citation overload         |
P2 (Nice)| W6: Hyperparameter         | Add backbone/LoRA/lambda summary | Reproducibility
         |    disclosure              | in main text                     |
```

---

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
VL-CL Methods (Root)
├── Branch 1: Regularization / Distillation
│   ├── Leaf 1.1: Similarity-distribution alignment
│   │   └── ZSCL, Mod-X, CTP, DKR, ZAF
│   ├── Leaf 1.2: Contrastive knowledge consolidation
│   │   └── C-CLIP
│   └── Leaf 1.3: Neighborhood / proxy preservation
│       └── Proxy-FDA
│
├── Branch 2: Architectural / Parameter-Efficient
│   ├── Leaf 2.1: MoE/Adapter routing
│   │   └── DDAS, DIKI, RAIL, LADA
│   ├── Leaf 2.2: Prompt learning (single-task)
│   │   └── CoOp, MaPLe
│   └── Leaf 2.3: Analytic adapters
│       └── RAIL (X-TAIL variant)
│
├── Branch 3: Replay / Data-Free Consolidation
│   ├── Leaf 3.1: Synthetic replay (diffusion)
│   │   └── GIFT, CLAP4CLIP
│   ├── Leaf 3.2: Pseudo-replay / symbolic replay
│   │   └── Smith et al., Lei et al., Zhang et al.
│   └── Leaf 3.3: Time-continual pretraining
│       └── Garg et al.
│
└── Branch 4: [This Paper] Geometry-First Alignment Invariant
    └── Leaf 4.1: CCA certificate (spectral + subspace)
        └── PI-CCA (ours): Replay-free, constant-memory,
            prompt-invariant via projector averaging

Value Gap: Prior branches optimize proxy signals (similarities,
logits, weights, routes). Leaf 4.1 directly constrains the
whitened cross-modal covariance geometry — a structurally
different objective. Novelty magnitude depends on whether
overlap exists with Leaf 1.3 (Mod-X is "geometry-inspired"
but targets off-diagonals, not canonical spectra/subspaces).
External verification deferred.
```

---

### Page Coverage Audit

| Page | Annotation Count | Coverage Status | Notes |
|------|-----------------|-----------------|-------|
| 1 (Title+Abstract+Intro+Related+Method+Experiments+Conclusion) | 14 | Covered | All substantive paragraphs annotated. One page contains the entire paper content. No appendix pages available. |

**Skipped Paragraph Records**: None. All substantive paragraphs in the provided manuscript (Abstract, Introduction paragraphs 1-4, Related Work paragraphs 1-3, Method subsections 3.1-3.4, Experiments 4.1-4.3, Conclusion, Ethics/Reproducibility statements) have received at least one annotation. Non-substantive boilerplate (author affiliations, figure captions, references list) intentionally skipped.

---

### Contribution-Level Novelty Conclusion (Deferred)

Due to Retrieval-Disabled Mode, external literature verification could not be performed. Based on internal manuscript evidence alone:

- **C1 (Insight)**: *Unclear* (deferred). The geometry-drift reframing is conceptually novel relative to the proxy-signal approaches described in the paper, but whether similar ideas exist in the CCA-for-CL literature or in concurrent work cannot be verified.
- **C2 (Capability)**: *Unclear* (deferred). The specific combination of CCA certificates, random sketching, and prompt-invariant projector averaging appears technically novel in the VL-CL context, but overlap with sketching-based CCA methods or continual CCA approaches in other domains cannot be assessed without retrieval.
- **C3 (Performance)**: *Partially supported* (pending variance reporting). The reported numerical results are competitive, but the lack of variance in Table 1 and the perfect-correlation concern in Figure 3 weaken the empirical evidence strength.

**Manual verification required**: A reviewer with paper_search access should compare PI-CCA against (1) Mod-X's off-diagonal geometry matching, (2) C-CLIP's contrastive knowledge consolidation, (3) DCCAE / deep CCA methods, and (4) other sketch-based subspace tracking approaches to determine genuine novelty overlap.