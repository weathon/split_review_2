## Summary
# Final Review Report

## Summary

This paper proposes TbLTA, a weakly-supervised framework for dense Long-Term Action Anticipation (LTA) that eliminates the need for frame-level annotations by relying solely on video transcripts — ordered action lists without timing or duration information. TbLTA uses a transformer encoder-decoder architecture with a temporal alignment module (ATBA) to generate dense pseudo-labels from transcripts, a CTC-based global supervisory signal, and cross-modal attention to semantically ground video features. The method is evaluated on Breakfast, 50Salads, and EGTEA Gaze+ benchmarks.

**Core contribution:** TbLTA is the first fully weakly-supervised approach for dense LTA that uses only transcript-level supervision, establishing a new baseline for annotation-efficient anticipation. On Breakfast, TbLTA achieves results competitive with fully supervised methods (29.03 Avg. MoC vs. ActFusion 28.45). However, on 50Salads, performance lags behind (20.92 vs. 28.39 for ActFusion), revealing limitations when action distributions are dense and transitions frequent.

**Strengths:** The problem is well-motivated — reducing annotation cost for LTA is practically important. The architecture is modular and thoughtfully combines existing components (ATBA, CTC, CRF, cross-modal attention) into a coherent weakly-supervised pipeline. The ablation study systematically evaluates each component's contribution.

**Weaknesses:** (1) Several mathematical inconsistencies exist in the loss formulations (CTC path length, duration loss indexing). (2) The "competitive" claim overstates results on 50Salads where the gap to supervised methods is large (~7.5 points). (3) Ablation studies lack statistical significance measures. (4) Key training details (L_vid definition, class token dynamics) are missing. (5) The conclusion over-generalizes without appropriate caveats. (6) The related-work comparison with language-based anticipation methods (Kim et al., 2024) is insufficiently differentiated.

**Novelty assessment (deferred — external literature search unavailable):** Due to the Retrieval-Disabled Mode (external paper search unavailable in this run), novelty and strongest-baseline comparisons are deferred for manual verification. The "first transcript-only LTA" claim appears plausible but requires verification against Kim et al. (2024) and other language-based anticipation works.

## Strengths
1. **Well-motivated problem.** Reducing annotation cost for dense LTA is a practically important direction. The paper correctly identifies that frame-level annotation is the primary scalability bottleneck for LTA, and transcript-level supervision offers a genuine cost-saving alternative. The motivation is clearly articulated in the Introduction.

2. **First transcript-only LTA framework.** To the best knowledge of the authors (and plausibly the field), TbLTA is the first fully weakly-supervised method for dense LTA that uses only transcripts — no frame-level labels, no boundary annotations. This establishes a new baseline and opens a promising research direction for annotation-efficient anticipation.

3. **Modular architecture with principled components.** The system design is methodical: it combines a temporal alignment module for pseudo-label generation (ATBA), a CTC-based global supervisory signal, a cross-modal attention layer for feature grounding, and a CRF-based coherence loss. Each component serves a clear purpose and is ablated in the experiments.

4. **Competitive results on Breakfast.** On the Breakfast dataset, TbLTA achieves 29.03 Avg. MoC in the deterministic setting, outperforming the best fully supervised method (ActFusion, 28.45). At 30% observation, especially with longer anticipation horizons, TbLTA shows pronounced gains (e.g., 31.67 vs. 29.64 at Obs30%/30% horizon). This demonstrates that transcript-level supervision can effectively capture procedural regularities for anticipation.

5. **Comprehensive ablation study.** The paper ablates CTC loss, cross-modal attention, CRF, and duration loss across two datasets, providing a clear picture of each component's contribution. The ablations reveal interesting dataset-dependent patterns (e.g., CRF is more beneficial on 50Salads than Breakfast).

6. **Good qualitative results.** The qualitative examples (Figure 3) show that TbLTA produces temporally coherent segmentations of observed portions and reasonable anticipation of future actions, with graceful degradation rather than complete failure in the future interval.

7. **Detailed experimental protocol.** The evaluation covers multiple observation/anticipation ratios (α = 20%, 30%; β = 10%-50%) and averages over standard data splits, providing a thorough assessment across difficulty levels.

## Weaknesses
### W1. Mathematical inconsistencies in loss formulations (Validity risk: High)

**CTC path length contradiction (Page 5, Section 3.2.2):** Equation (4) defines $\pi = [\pi_1, \dots, \pi_{\alpha T}]$ (observed-only length) but the CTC probability $P(\mathcal{Y}|X)$ sums over paths of length $T$ (full video), creating a direct contradiction. If CTC is computed over the full video, the definition of $\pi$ should use $T$, not $\alpha T$. If CTC uses only observed frames, the equation should sum to $\alpha T$. This inconsistency must be resolved before the method can be correctly reproduced.

**Duration loss indexing mismatch (Page 6, Section 3.2.3, Eq. 7):** The loss sums over $t=1$ to $T_{\text{pred}}$ (frame indices) while using $\hat{\delta}_i$ and $\hat{d}_{y_i}$ (segment-level quantities). If there are $N-k^*$ future segments (typically far fewer than $T_{\text{pred}}$ frames), this is a dimensional mismatch — the loss either uses wrong indices or implicitly broadcasts segment values across frames without explanation.

### W2. Over-claiming of "competitive" results (Objectivity risk: High)

**Page 7-8, Section 4.2:** The paper claims TbLTA "attains performance competitive with, and occasionally superior to, fully supervised approaches." On 50Salads, the deterministic TbLTA (20.92 Avg.) is **7.47 points below** the best supervised method ActFusion (28.39 Avg.) — a relative gap of ~26%. The "competitive" characterization is only accurate for Breakfast at 30% observation. On 50Salads, the results are substantially worse, and the paper should honestly acknowledge this gap rather than aggregating it into a blanket statement.

**Page 8, Conclusion:** The same unqualified claim is repeated, further reinforcing the overstatement. The conclusion should provide a balanced summary of where TbLTA works (Breakfast, especially at longer observation ratios) and where it struggles (50Salads with dense actions).

### W3. Ablation studies lack statistical reliability (Evidence sufficiency risk: Medium)

**Page 7-8, Section 4.3:** All ablation results are reported as single numbers without variance, confidence intervals, or significance tests. Several ablation deltas are small (e.g., CTC removal drops only 0.6 points on 50Salads; duration loss removal drops 0.2 points on 50Salads). Without multi-seed reporting, these small differences could be within run-to-run noise. The paper should either report mean±std over at least 3 seeds, or explicitly state that ablations use a single seed and caveat the conclusions accordingly.

### W4. Missing ℒ_vid definition (Reproducibility risk: Medium)

**Page 6, Training and Inference:** The progressive training scheme uses ℒ_vid (video-level classification loss) in the first 10 epochs, but this loss is never defined in Section 3.2 (TbLTA Objective). The three loss groups (ℒ_A, ℒ_TAS, ℒ_LTA) from Eq. (3) do not include ℒ_vid. A reader implementing TbLTA from the paper cannot determine what ℒ_vid is, how it is formulated, or how it relates to the other losses. This is a significant reproducibility gap.

### W5. Insufficient differentiation from language-based anticipation (Novelty risk: Medium)

**Page 2, Related Work — LTA paragraph:** Kim et al. (2024) "explored language-based anticipation without explicit time annotations," which appears closely related to TbLTA's transcript-only approach. The paper mentions this only in passing and does not provide a clear technical differentiation. If Kim et al. already removes time annotations for anticipation, what is the residual novelty of TbLTA? The paper should explicitly compare assumptions, output format (symbolic vs. dense frame-level), supervision requirements, and evaluation protocol to justify the "first transcript-only" claim.

### W6. EGTEA evaluation uses a substantially easier protocol (Evidence scope risk: Medium)

**Page 7, Section 4.1, Metrics:** EGTEA evaluation uses verb-only mAP (19 verbs) instead of full verb-noun action classes (106 classes), while Breakfast and 50Salads use the harder MoC metric. The verb-only setting is substantially easier, so the EGTEA results (TbLTA: 65.37 All vs. Anticipatr: 76.80, an 11-point gap) may not reflect performance on the full task. The paper does not explicitly caveat this, potentially misleading readers about the method's capability on egocentric video.

### W7. Duration normalization constraint may be inappropriate (Methodological risk: Medium)

**Page 3, Problem Definition:** Future durations are constrained to sum to 1 ($\sum d_j = 1$). In a weakly-supervised setting where the boundary index $k^*$ is unknown and no duration ground truth is available, this hard normalization may force the model to produce durations inconsistent with actual video length. The paper does not justify why this normalization is appropriate without ground truth.

### W8. Conclusion over-generalizes without specific limitations (Writing quality risk: Medium)

**Page 8, Conclusion:** The conclusion states TbLTA "opens a new paradigm for scalable and language-informed anticipation" without specifying what "scalable" means operationally. It also does not discuss the method's known failure modes (e.g., poor performance on dense action sequences, sensitivity to transcript quality, difficulty with unseen actions). The only stated limitation is duration prediction for unseen actions, which is too narrow given the empirical gaps on 50Salads.

### Minor Issues

- **Page 1, Abstract:** Claims "very robust and less costly" but provides no quantitative cost comparison between transcript and frame-level annotation.
- **Page 1, Introduction:** Five contributions contain redundancy (C1 and C5 are essentially the same claim). Consolidating to 2-3 would improve clarity.
- **Page 1, Introduction P1:** The opening conflates TAS and LTA without establishing why LTA is fundamentally harder than segmentation.
- **Page 4, Cross-attention (Eqs. 1-2):** The construction of binary mask M from soft pseudo-labels needs clarification — is it hard-thresholded, and if so, is it differentiable?
- **Page 7, Table 1:** The deterministic TbLTA on 50Salads at Obs 30% shows 25.32 at 20% horizon — this is the only cell where TbLTA "wins" in the weakly-supervised row against supervised baselines, yet the narrative generalizes from this single data point.

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: Annotation burden for dense LTA]
    |
    v
[Proposed solution: TbLTA — transcript-only supervision]
    |
    +---> [Claim C1: First transcript-only LTA] 
    |         Evidence: Table 1 results on 3 benchmarks
    |         Weakness: Comparison with Kim et al. (2024) insufficient
    |
    +---> [Claim C2: TbLTA architecture enables weakly-supervised LTA]
    |         Evidence: Ablation studies (Tables 3-4)
    |         Weakness: ℒ_vid undefined; π length inconsistency
    |
    +---> [Claim C3: Competitive with fully supervised methods]
    |         Evidence: Table 1, Breakfast results
    |         Weakness: 50Salads gap ~7.5 points unacknowledged
    |
    v
[Core tension: Paper claims "competitive" but only Breakfast supports
 this; 50Salads shows large gap; EGTEA uses easier protocol]
    |
    v
[Recommended revision: Bound claims per dataset, add cost analysis,
 fix math errors, report ablation variances]
```

### ASCII Diagram — Revision Strategy Roadmap

```text
Priority 0 (Must fix — validity):
    π length inconsistency (Eq. 4) ——> Fix indexing to T or αT
    Duration loss dimension mismatch (Eq. 7) ——> Fix sum index
    Add ℒ_vid definition ——> Include in Section 3.2

Priority 1 (Must fix — objectivity):
    "Competitive" overclaim ——> Bound per dataset
    Conclusion over-generalization ——> Specific limitations
    EGTEA verb-only caveat ——> Explicit scope statement

Priority 2 (Should fix — reproducibility):
    Ablation variance ——> Add multi-seed or single-seed caveat
    Class token E details ——> Init, regularization, positional encoding
    Mask M construction ——> Clarify differentiable/neighborhood size

Priority 3 (Nice to have — clarity):
    Consolidate contributions (C1 + C5)
    Title refinement
    CRF short-term trade-off explanation
```

## Score
**Final Score: 6/10**

**Scoring rationale (evidence-grounded, prioritizing research value + novelty):**

- **Research value (7/10):** The problem is well-motivated and practically important. Reducing annotation cost for LTA is a genuine bottleneck. The paper demonstrates that transcript-only weak supervision is feasible for this task, which is a meaningful step. However, the value is partially undermined by (a) mathematical errors that cast doubt on implementation correctness, (b) overclaimed competitiveness on 50Salads where the gap to supervised methods is large, and (c) insufficient differentiation from related language-based anticipation work.

- **Novelty (6/10, deferred verification):** The claim of being the "first transcript-only LTA method" appears plausible but cannot be fully verified in this run (external retrieval unavailable). The technical novelty is moderate — the architecture assembles existing components (ATBA alignment, CTC loss, CRF decoder, cross-modal attention) rather than introducing fundamentally new mechanisms. The main novelty is in the *combination* of these components for the LTA task under weak supervision. Deeper comparison with Kim et al. (2024) (language-based anticipation without time annotations) is needed to establish the true novelty boundary.

- **Validity/Soundness (5/10):** The main weakness. Two mathematical inconsistencies (CTC path length, duration loss indexing) and one missing loss definition (ℒ_vid) reduce confidence in the method's correctness. The ablation studies lack statistical significance measures. The evaluation is inconsistent across datasets (MoC vs. verb-only mAP).

- **Reproducibility (5/10):** Below average. The missing ℒ_vid definition, unclear class token training dynamics, ambiguous mask construction, and unstated seed usage make reproduction difficult without the supplementary material or code.

- **Presentation (7/10):** Generally well-written with clear motivation. The related work is comprehensive but not always well-connected to the proposed method. The contribution list is somewhat redundant. The figures and tables are clear.

**Post-Revision Target:** [7, 8]/10 — If the mathematical inconsistencies are corrected, ℒ_vid is defined, ablation variances are reported, claims are properly bounded, and the EGTEA evaluation caveat is added, the paper could reach 7-8/10.

**Decision context:** The paper addresses a genuinely important problem and shows promising initial results on one benchmark. However, the two mathematical errors (CTC path length, duration loss indexing) must be resolved before the method can be considered reproducible, and the overclaiming must be corrected for scientific objectivity. I recommend major revision.