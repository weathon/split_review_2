## Summary
# Final Review Report

## Summary

This paper introduces GUI-Spotlight, a visual grounding model for GUI agents that iteratively invokes specialized tools (crop, extract, find_color) to progressively narrow focus on target screen elements. The model is trained in three stages: (1) SFT warm-up on 2561 multi-turn teacher trajectories, (2) RL with a modified GSPO objective incorporating an auxiliary cross-entropy loss, and (3) further RL refinement on high-resolution data with bucketed tool sampling. On ScreenSpot-Pro, GUI-Spotlight achieves 52.8% accuracy using only 18.5K training samples, surpassing several prior 7B models that use millions of samples.

The paper has three stated contributions: (C1) a think-with-image iterative spotlighting model, (C2) a modified GSPO algorithm for multi-tool RL, and (C3) documentation of negative results. While the iterative tool-use approach is practically motivated and the empirical results on ScreenSpot-Pro are promising, the paper has several substantive weaknesses: the improvement margins are narrow and reported without variance or significance tests; the method underperforms prior 7B models on two of three evaluated benchmarks (UI-Vision and OSWorld-G) yet claims to "substantially outperform" comparable models; the critical Stage-1 accuracy collapse (39.3% to 17.8%) is not adequately analyzed; and inference cost (number of tool calls per query) is never reported. The GSPO modification is incremental (adding a filtered cross-entropy term) and its novelty boundary is unclear. External literature verification was unavailable in this run; novelty conclusions are deferred.

## Strengths
1. **Practically motivated approach.** The iterative spotlighting idea is intuitive and well-aligned with the problem of grounding on dense, high-resolution GUI screens. Using discrete tools (crop, extract, find_color) that mimic human visual search strategies makes the method interpretable at each step.

2. **Data efficiency on ScreenSpot-Pro.** GUI-Spotlight achieves competitive results with only 18.5K curated training samples, compared to millions used by prior methods such as UGround-V1-7B (10M) and V2P-7B (9.6M). This data efficiency is notable even when accounting for the 72B teacher-model cost.

3. **Structured training pipeline with transparency on negative results.** The three-stage training design (SFT → RL → refinement) is clearly described, and the paper documents several attempted modifications that did not work (e.g., uncertain-prompt selection, continuous reference policy update). This transparency is valuable for practitioners building similar systems.

4. **Comprehensive reward design analysis.** Section 4.2 provides a systematic comparison of sparse vs. dense answer rewards and crop/extract reward weighting, yielding the practical insight that sparse rewards with extract-favored weighting perform better. The observation that Extract is easier to learn than Crop is well-reasoned.

5. **Multi-benchmark evaluation.** The paper evaluates on three benchmarks (ScreenSpot-Pro, UI-Vision, OSWorld-G) covering high-resolution professional UIs, desktop applications, and general OS-level tasks, giving a reasonably broad view of method behavior.

## Weaknesses
### W1 (Critical): No variance reporting or statistical significance — core comparisons are unverifiable (Page 1 - Experiments, Tables 3-5)

All results in the paper are reported as point estimates without standard deviations, confidence intervals, or significance tests. This is a critical omission because the claimed improvements over prior 7B models are small (e.g., +2.2 points on ScreenSpot-Pro, -3.1 points on UI-Vision). Without variance estimates, readers cannot determine whether these differences are meaningful or within noise. The training dynamics plots (Figures 2-4) show single-run trajectories without error bands. **Required action:** Report mean ± std over ≥3 seeds for all GUI-Spotlight variants and add paired bootstrap significance tests against the strongest baseline on each benchmark.

### W2 (Major): Overstated and selectively reported comparative claims (Page 1 - Abstract, Contributions, Section 5.1)

The paper claims to "substantially outperform comparable 7B baselines" but this is not consistently supported across benchmarks:
- ScreenSpot-Pro: leads by +2.0 points (52.8% vs UI-Venus-7B 50.8%)
- UI-Vision: trails by -3.1 points (23.4% vs UI-Venus-Ground-7B 26.5%)
- OSWorld-G: trails by -5.0 points (62.7% vs GTA1-7B 67.7%)

The narrative throughout the abstract, contributions, and conclusion selectively highlights ScreenSpot-Pro results while de-emphasizing benchmarks where the method underperforms. **Required action:** Add explicit qualification about benchmark-dependent performance; restructure claims to match evidence scope.

### W3 (Major): Stage-1 accuracy collapse is unexplained (Page 1 - Figure 2, Section 3.2.2)

After Stage-1 SFT on 2561 teacher trajectories, accuracy drops catastrophically from 39.3% to 17.8% — less than half the base model's performance. The paper describes this as "under-aligned" but provides no analysis of why SFT degrades performance so severely. This is a fundamental issue: if SFT on expert tool-use trajectories makes the model worse at its core task, the three-stage design may be fighting symptoms rather than addressing root causes. **Required action:** Add diagnostic analysis: (a) decompose Stage-1 errors into format vs. grounding failures, (b) measure oracle accuracy with perfect tool selection, (c) compare against a simple baseline of skipping Stage 1 entirely.

### W4 (Major): Inference cost is never measured or reported (Page 1 - Sections 3-5)

The iterative tool invocation requires multiple forward passes per query, yet the paper reports zero inference-time metrics: average number of tool calls per query, total tokens generated, wall-clock time, or FLOPs. The claim that a 7B model with multi-step inference is "competitive with substantially larger models" cannot be evaluated without cost comparison. A 7B model requiring 5 forward passes may be more expensive than a single 72B forward pass. **Required action:** Report average steps per query, per-step token cost, and total inference time vs. single-pass baselines.

### W5 (Major): Data cleaning BA formula is mathematically asymmetric and insufficiently strict (Page 1 - Data Cleaning paragraph)

The Bounding Box Accuracy score S_BA = 5·|B_p∩B_gt|/|B_gt| + 5·|B_p∩B_gt|/|B_p| is an arithmetic mean of precision and recall scaled to 0-10. This allows a highly imprecise box (e.g., very large box containing the target) to score near threshold even when precision is poor. The threshold of 6/10 corresponds to average precision-recall of only 0.6, allowing noisy annotations through. **Required action:** Replace with IoU (Intersection over Union) at a conservative threshold (≥0.5), which is symmetric and more stringent.

### W6 (Major): GSPO modification novelty is incremental and notation is inconsistent (Page 1 - Section 3.2.2, Equations)

The claimed "modification" to GSPO consists of adding an auxiliary cross-entropy loss filtered to format-valid correct trajectories. Using a filtered supervised loss to stabilize RL is a known technique (used in DPO variants, rejection sampling, and earlier RL+LM loss combinations). The paper does not clearly delineate what is novel beyond this combination. Additionally, the notation uses undefined `s_{b,t}` in the auxiliary loss while the importance ratio uses explicit conditional notation `y_{i,t} | x, y_{i,<t}`. **Required action:** Clarify the novelty boundary of the GSPO modification relative to existing techniques. Fix notation inconsistency.

### W7 (Major): Data collection details are insufficient for reproducibility (Page 1 - Data Collection paragraph)

The Selenium-based collection pipeline is described at a high level but omits: webpage resolution used, list of crawled websites or domains, element detection criteria (CSS/heuristics/ARIA), and the exact size of the filtered UGround subset. The "18.5K" training sample count is the sum of an unknown UGround filtered subset plus 11.6K high-resolution samples, making the exact dataset composition opaque. **Required action:** Provide a data appendix with website categories, rendering resolution, detection methodology, and per-source dataset sizes.

### W8 (Minor): Contribution C3 is a meta-contribution rather than a technical contribution (Page 1 - Contributions)

Documenting negative results is commendable for transparency but is a reporting methodology choice, not a scientific contribution on par with C1 and C2. Listing it as a co-equal contribution may dilute the perceived technical contribution of the paper. **Suggestion:** Move C3 into the methodology section or supplement as a reproducibility statement.

### W9 (Minor): Attention mechanism citation (Shu et al., 2022) is decorative (Page 1 - Introduction P3)

The inspiration from "attention mechanisms that highlight discriminative regions" is cited but never connected to the actual tool design or model architecture in the method section. The iterative cropping and tool invocation do not implement or approximate any specific attention mechanism from Shu et al. **Suggestion:** Remove the decorative citation or integrate it meaningfully into the method section.

### W10 (Minor): Conclusion lacks limitations discussion (Page 1 - Conclusion)

The conclusion does not acknowledge the UI-Vision/OSWorld-G underperformance, missing inference cost analysis, or failure modes of the approach. A transparent limitations paragraph would improve the paper's scientific integrity. **Suggestion:** Add limitations covering benchmark-conditional performance, inference cost, and known failure patterns.

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: GUI visual grounding accuracy on high-resolution screens]
   │
   ├── Claim C1: Iterative spotlighting with tools improves accuracy
   │   ├── Evidence: ScreenSpot-Pro 52.8% (↑ from 38.7% baseline)
   │   ├── Gap: No variance reported; inconsistent on UI-Vision/OSWorld-G
   │   └── Risk: Overclaimed as "substantially outperforming"
   │
   ├── Claim C2: Modified GSPO improves training stability
   │   ├── Evidence: Training reward curves (Fig 3 right)
   │   ├── Gap: Incremental modification; notation inconsistency
   │   └── Risk: Novelty boundary unclear vs. existing methods
   │
   └── Claim C3: Negative results documentation provides guidance
       ├── Evidence: Ablation on RL variants and reward designs
       ├── Gap: Meta-contribution rather than technical advance
       └── Risk: Dilutes perceived contribution depth
```

### ASCII Diagram — Revision Strategy Roadmap

```text
[Stage 1: Pre-submission fixes]
  ├── Add variance/std to all results (W1) → enables significance assessment
  ├── Fix BA formula to IoU (W5) → improves data quality guarantee
  ├── Clarify notation s_{b,t} in GSPO (W6) → resolves reproducibility risk
  └── Qualify comparative claims (W2) → aligns narrative with evidence
       │
[Stage 2: Medium-effort improvements]
  ├── Analyze Stage-1 accuracy collapse (W3) → strengthens scientific rigor
  ├── Report inference cost (W4) → enables fair cost-benefit comparison
  ├── Add data appendix (W7) → satisfies reproducibility standard
  └── Add limitations paragraph (W10) → improves scientific integrity
       │
[Stage 3: Substantial extensions]
  ├── Multi-seed experiments (W1) → enables statistical claims
  ├── Failure mode analysis → deepens contribution understanding
  └── Comparison on matched-compute budget → validates efficiency claims
```

## Score
**Final Score: 5/10**

**Rationale:** The paper addresses a practically important problem (GUI visual grounding on high-resolution screens) with a well-motivated approach (iterative tool-based spotlighting). The data efficiency on ScreenSpot-Pro is promising, and the documentation of negative results is transparent. However, the score is constrained by several critical weaknesses that affect the core claims:

- **Research value and novelty are moderate (primary scoring dimension).** The iterative tool-use approach is intuitive but the technical novelty is incremental — the GSPO modification adds a filtered cross-entropy term, which is a known technique. The paper does not establish clear superiority over prior 7B models on two of three benchmarks. Without external literature verification (unavailable in this run), novelty conclusions are deferred, but the within-paper evidence suggests the contributions are solidly incremental rather than transformative.

- **Validity and evidence sufficiency are the main concerns (secondary scoring dimension).** The complete absence of variance reporting or significance testing means the core comparative claims cannot be verified. The narrow margins (+2.0 points on ScreenSpot-Pro) may not be statistically significant. The unexplained Stage-1 accuracy collapse (39.3% → 17.8%) indicates a potential instability in the training pipeline that is not analyzed. The inference cost is never measured, making the "competitive with larger models" claim unsubstantiated.

- **Reproducibility is limited (tertiary scoring dimension).** Data collection details are insufficient, notation inconsistencies exist in the GSPO equations, and the BA filtering formula has mathematical flaws. While the three-stage training is clearly described, these gaps reduce confidence in exact reproducibility.

- **Presentation quality is good.** The paper is clearly written with appropriate figures and tables. The reward design analysis is well-structured. The main weakness in presentation is selective reporting emphasis and overstated claims.

**Summary justification:** The paper has a solid practical motivation and promising directional results on one benchmark, but the missing variance analysis, selective result reporting, unmeasured inference cost, and incremental technical novelty place it in the "borderline but with significant fixable issues" range.