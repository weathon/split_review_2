## Summary

REPL proposes a semi-supervised learning framework for LiDAR semantic segmentation that refines pseudo-labels through error detection (confidence-based agreement between teacher and student) followed by masked reconstruction (inspired by MAE), rather than discarding or reweighting unreliable labels as prior work does. The method is evaluated on nuScenes-lidarseg and SemanticKITTI, achieving strong results particularly on nuScenes.

## Strengths

- **Novel and well-motivated core idea.** The paper correctly identifies that existing SSL methods for LiDAR segmentation are "post-hoc" — they filter or reweight pseudo-labels after generation rather than improving their quality. The proposal to *correct* unreliable pseudo-labels via masked reconstruction is a genuine departure from the dominant filtering/reweighting paradigm (Section 1, Section 3).

- **Strong results on nuScenes-lidarseg.** REPL achieves the best mIoU at 10%, 20%, and 50% label ratios and ties for best at 1%, with an average gain of +2.0 mIoU over the second-best method (IT2). The improvements are non-trivial and consistent across all four label ratios (Table 1).

- **Informative oracle error mask analysis (Table 4).** Showing that an oracle error mask would yield 67.3 mIoU (vs. 60.0 with REPL's heuristic) both validates the refinement direction and honestly indicates room for improvement in error detection. This is a clean experiment that strengthens the paper's thesis.

- **Reasonably thorough ablations on loss components.** Tables 2 and 3 systematically ablate the contributions of individual loss terms for both the refiner and segmentation network, showing consistent improvement as each component is added.

## Weaknesses

### Fatal

None.

### Major

- **Factual error in reported results.** The paper states (line 166): *"On SemanticKITTI, REPL also showed strong results, achieving the best performance at 1% and 50%."* However, Table 1 shows that at 1% on SemanticKITTI, REPL achieves 54.7 mIoU, while FrustrumMix achieves 55.7 and LaserMix++ achieves 56.2 — making REPL **third-best** at this setting. This is contradicted by the paper's own data. While the overall average (61.6) and nuScenes results are strong, this specific claim is factually wrong and appears in a passage reporting the main results. The authors should correct this and honestly characterize REPL's performance on SemanticKITTI at the 1% label ratio.

- **Citation inconsistencies across text and tables.** Three cases where the body text and Table 1 disagree on method identity:
  - Text (line 166): *"AIScene (Liu et al., 2025)"* — Table (line 185): *"AScene (Xu et al., 2023)"* (different name, different author, different year)
  - Text (line 166): *"FrustumMix (Xu et al., 2025)"* — Table (line 186): *"FrustrumMix (Kong et al., 2023)"* (different spelling, different author, different year)
  - Text (line 167): *"SLiDR (Sautier et al., 2022)"* — Table (line 178): *"SLiDR (Santner et al., 2022)"* (different author spelling)
  
  These inconsistencies make it difficult for a reader to verify which baselines were actually compared, undermining trust in the experimental comparison.

- **No clean ablation isolating the refiner's marginal contribution.** The paper's central claim is that refinement is better than filtering/reweighting. Yet Tables 2 and 3 start from the supervised-only baseline (50.9) and incrementally add loss components — they never show a "teacher-student without refiner" control point within the REPL framework. The closest baseline is Mean Teacher in Table 1 (51.6 at 1% on nuScenes), but this is a separate implementation. Without ablating the refiner itself (i.e., REPL minus the refiner, keeping the symmetric CE and mixing), the marginal contribution of the refiner cannot be cleanly attributed.

### Minor

- **Theoretical analysis (Section 3.5) is too elementary to constitute a meaningful contribution.** Proposition 1 ($H(Y|X,T) \leq H(Y|X)$) is a direct consequence of the basic information-theoretic fact that conditioning on additional information cannot increase entropy — it requires no proof specific to this setting and provides no actionable design insight. Proposition 2 derives $\zeta = \pi - r/(q+r) > 0$, which algebraically restates a precision-recall tradeoff. The empirical analysis then shows the condition is extremely easy to satisfy (e.g., $r < 11.05 \cdot q$ for $\pi=0.917$). The theoretical section does not guide any design choice in REPL. The paper would lose nothing if this section were removed.

- **No variance or statistical significance reporting.** All results in Table 1 are reported as single numbers without standard deviation or confidence intervals. Given that semi-supervised learning is inherently stochastic (different label subsets, different training trajectories), it is impossible to know whether margins such as the 0.1 mIoU advantage over AScene on SemanticKITTI (61.6 vs. 61.5 on average) are meaningful.

- **No per-class results.** LiDAR point clouds exhibit extreme class imbalance. mIoU averages over classes, but a per-class breakdown would reveal whether REPL helps uniformly or primarily on frequent classes.

- **Error detection mechanism is heuristic and not compared against alternatives.** The three-condition agreement strategy (Section 3.3) is described as "simple" and "even with a simple error estimation strategy" — but the paper never compares it against even basic alternatives such as entropy-based uncertainty or ensemble disagreement, which would be straightforward to implement.

### Trivial

- The relationship between the refiner's concatenated input $(X, \tilde{Q})$ and the Cylinder3D architecture's channel dimensions is not explicitly specified (the refiner uses Cylinder3D, so the first-layer channel count would be $C + K$, but this is stated nowhere).

## Nice-to-Haves

- An analysis of why REPL benefits more from higher label ratios (Figure 5 shows the refiner providing larger improvements at 20% and 50% than at 1%) — this is somewhat counterintuitive and deserves discussion.
- A comparison of the error detection heuristic against simple alternatives (entropy, ensemble disagreement).
- Per-class IoU results to show whether the benefit is concentrated on frequent classes.

## Removed Points

- **Computational cost concern ("refiner nearly doubles the model footprint"):** The paper transparently quantifies the cost (+0.25s, +396 MB, +9.1 mIoU) and characterizes it as "moderate." The critic's framing is essentially the same observation rephrased as a criticism. The paper's characterization is fair.
- **Concern about negative learning potentially misleading when the true class is outside top-k:** The paper acknowledges this implicitly, and the concern applies to any negative learning approach. Not specific enough to this paper to warrant retention.
- **Formatting, style, and presentation nitpicks.**
- **Speculation about missing appendix content** (the parser strips those sections).
- **Generic "the evaluation lacks rigor" framing** without a specific anchor — removed for lack of concrete referent.
- **Strengths about "important problem" or "addressing an interesting question"** — removed because they are generic; only specific, evidence-backed strengths are retained.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's review surfaces two verified problems (factual error in results, citation inconsistencies) that the authors must address, but does not generate a novel scientific insight about the method that the paper itself does not already contain.

## Suggestions

1. **Correct the factual error.** Reword line 166 to honestly state REPL's ranking at 1% on SemanticKITTI (third-best, behind LaserMix++ and FrustrumMix). The overall average (61.6) is still the best, so the paper's broader claims remain defensible.

2. **Resolve all citation inconsistencies.** Ensure the text and Table 1 agree on method names, author names, and publication years for every baseline.

3. **Add a clean ablation isolating the refiner.** Add a row to Table 3 showing "teacher-student with refiner removed" (or equivalently, REPL minus the refiner while keeping symmetric CE and mixed-scene training). This directly tests the paper's central thesis.

4. **Remove or substantially rework the theoretical section (Section 3.5).** As it stands, Propositions 1 and 2 do not constrain or inform any design choice in REPL. Either replace them with analysis that actually guides the method, or drop the section and let the empirical results speak.

5. **Add variance estimates** (standard deviations over multiple runs or label subsets) to the main results table.

6. **Report per-class IoU** to establish where the improvements come from.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Human Score | Round | Comparison |
|------|----------------|-------|------------|
| GtnNhtuVrc (Semi-Supervised Seg via Marginal Context) | 5.25 | Bracket | Pseudo-label refinement for segmentation; rejected due to inconsistent numbers and unclear ablations. REPL has a more novel core idea and stronger results but also has a verified factual error. |
| PBq8uOjGso (Semi-Supervised Active Learning 3D Detection) | 4.50 | Narrow | Label-efficient 3D detection; rejected. Comparable in score range but REPL has stronger empirical results. |
| Q1vkAhdI6j (MixSup: Label-efficient LiDAR Detection) | 6.67 | Bracket | Cleaner paper with clearer claims; accepted. REPL has more issues (factual error, citations) that prevent reaching this tier. |
| Ylk98vWQuQ (Learning 3D Perception from Others) | 5.80 | Bracket | Label-efficient 3D detection; accepted despite some baseline concerns. REPL has more verification issues. |
| MHQMZ8FOL5 (Novel Class Discovery in Point Clouds) | 5.50 | Narrow | Point cloud segmentation; rejected. Comparable in score. |
| XT2yAa6Bbp (Sinkhorn Output Perturbations) | 5.50 | Narrow | Pseudo-label noise in semi-supervised segmentation; rejected. Comparable. |

**Round-1 bracket:** 4.0–6.0 (determined by comparing against semi-supervised segmentation papers scoring 4.5–5.5 and LiDAR label-efficient papers scoring 5.5–6.67).

**Round-2 narrowing:** The factual error and citation inconsistencies are more severe than the issues in papers scoring 5.5+ (e.g., GtnNhtuVrc at 5.25 had inconsistent numbers too, but the citations were clean). Comparing to PBq8uOjGso (4.50) and MHQMZ8FOL5 (5.50), REPL's core idea is stronger and the nuScenes results are more convincing than either, but the verification issues lower confidence. The 4.5–5.0 range best reflects a paper with a genuinely novel core idea and strong partial results, marred by a factual error and sloppy citation work that must be fixed before the claims are trustworthy.

The core contribution — pseudo-label refinement as an alternative to filtering — is sound and well-motivated. The nuScenes results are strong and the oracle error mask experiment is informative. However, the factual error in the main results text ("best at 1%" when the table shows third-best) and the three citation inconsistencies between text and tables are serious presentation issues that undermine trust in the experimental comparison. Additionally, the paper lacks a clean ablation that isolates the refiner's marginal contribution, making it impossible to attribute gains to the refinement mechanism versus the other training additions (symmetric CE, mixed-scene training). These issues are fixable, but as presented the paper does not meet the bar for acceptance.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>