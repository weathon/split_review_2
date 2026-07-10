Now let me produce the final consolidated review.

## Summary

This paper identifies and taxonomizes a blind spot in class-wise machine unlearning: prior work universally assumes the class label equals the target concept (all-matched setting). The authors systematically define three mismatch settings (target mismatch, model mismatch, data mismatch) where this assumption breaks, grounded in practical scenarios like a user requesting removal of a semantic subset within a class. They propose TARF (TARget-aware Forgetting), a three-phase framework using annealed gradient ascent on forgetting data and target-aware gradient descent on hard-to-affect retaining data, guided by an analysis of "gravity effects" in representation-level forgetting dynamics. Empirical results show TARF achieves qualitatively strong performance on target mismatch and data mismatch, with notable improvements (e.g., 1.23 vs. 20.80 Gap on CIFAR-10 target mismatch).

## Strengths

- **A genuinely novel problem formulation.** Prior class-wise unlearning work universally assumes L<sub>D</sub> = L<sub>T</sub> = L<sub>M</sub>. The paper identifies this blind spot and systematically taxonomizes three mismatch settings (target, model, data mismatch) that are well-motivated by practical scenarios. Figure 1 and the CIFAR-100 "boy"/"girl"/"people" running example make the taxonomy concrete. This reframing of the problem space is the paper's most significant contribution. [favorability=6.80]

- **Empirical results on target mismatch and data mismatch are decisive.** In Table 3, TARF achieves Gap values of 1.23 (CIFAR-10) and 0.21 (CIFAR-100) on target mismatch, compared to the next-best baseline (GA) at 20.80 and 8.86. On data mismatch, TARF's Gap is 0.96/1.17 versus the next-best (GA at 5.89/2.43). These are not incremental improvements — they represent a qualitative shift from "this task is basically not working" to "this task is working as well as the conventional all-matched setting." [favorability=10.42]

- **The three-phase design (identification → separation → approximation) is well-motivated by the analysis.** The "gravity effects" analysis in Section 3.2 provides an organizing principle: the representation distance between data subsets predicts how gradient ascent on one subset affects the other. Phase I exploits this to identify false retaining data; Phase II uses bidirectional gradient operations to disentangle entangled features; Phase III anneals to pure retraining. [favorability=9.28]

- **ImageNet-1k results (Table 4) extend the claims to a realistic scale.** TARF maintains its advantage (e.g., Gap 3.66 vs FT's 3.82 on all-matched, Gap 3.97 vs FT's 4.02 on target mismatch) while running in comparable time. Many unlearning methods that work on CIFAR fail to scale. [favorability=9.30]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Model mismatch scenario lacks a clear operational definition of what "forgetting" means.** The paper states (line 248) that UA in model mismatch is evaluated with superclass labels and the Retrained model still has UA ~88%, meaning the goal is not to suppress superclass predictions but to match a retrained model's behavior. This is a valid but subtle definition that needs more explicit statement. Additionally, the fine-grained evaluation in Table 2 introduces subclass-level metrics (UA-F, UA-R) but does not explain how these are computed from a model whose output space is the superclass level. This makes the model mismatch results harder to interpret than the other settings. [favorability=6.99]

- **The Gap metric can mask important tradeoffs.** Gap averages absolute deviations from Retrained across UA, RA, TA, and MIA. Since Retrained reference values differ substantially across metrics (e.g., UA=0 vs RA~99), a method with poor forgetting (UA=10) can get the same Gap as a method with destroyed utility (RA=89.51). The paper does report per-metric values in Table 3 alongside Gap, so the full picture is available to careful readers, but Gap is used as the headline comparison metric and bolded as the primary indicator of superiority, which may obscure which specific failures a method incurs. [favorability=4.09]

- **Theorem 3.2 is presented with formal weight that exceeds what it delivers.** The bound contains the term λ<sub>max</sub>(J<sub>θ</sub>(·)x<sub>1</sub>) which is not a well-formed matrix-vector product (the Jacobian J<sub>θ</sub> = ∂h(x)/∂θ is a matrix whose product with x<sub>1</sub> is dimensionally unclear), and the bound depends on an expectation E[d<sub>h</sub>] and a λ<sub>max</sub> term that depend on model parameters in ways not controlled by the analysis. The paper itself uses the theorem mainly as intuitive justification (Remark 3.1), which is reasonable, but the formal framing is somewhat misleading. [favorability=5.40]

- **Known-class-number assumption is strong and undiscussed.** The paper assumes "the number of classes in D<sub>un</sub> belonging to the target concept is known in target mismatch forgetting" (line 61). A user who reports a few "boy" images as problematic may not know that "girl," "man," "woman" also belong to the same target concept, yet the paper does not discuss sensitivity to incorrect specification of this number. [favorability=3.82]

### Trivial
None.

## Nice-to-Haves

- Supplement the Gap metric with per-metric spider/radar plots or a table of individual absolute deviations from Retrained so readers can directly see which dimensions drive the Gap.
- Clarify what gradient operation (if any) is applied to the identified false retaining data D<sub>fr</sub> during Phase II (the ablation in Figure 7 right panel addresses this for an ablation variant, but the main method's behavior is not fully specified).
- Discuss sensitivity of TARF to incorrect specification of the number of target-concept classes in D<sub>un</sub>.
- Clarify the notation in Theorem 3.2 and state more directly that the bound serves as a qualitative justification.

## Removed Points

These points were flagged for removal from the input review. Treat them with caution if referenced:

- *Model mismatch evaluation confusion about subclass labels:* REMOVED. The main evaluation (Table 3) uses superclass labels consistent with the model's output space. The paper explicitly states at line 248 that UA in model mismatch is evaluated with superclass label.
- *"Missing appendix" complaints:* REMOVED per policy — appendix sections are stripped by the parser but exist in the original submission.
- *Terminology nitpick about "under-entangled":* REMOVED as a style preference, not a substantive issue.
- *MIA interpretation concern:* REMOVED — the paper reports Retrained reference MIA alongside, so the interpretation as a consistency check (not absolute privacy guarantee) is accessible to readers.
- *Speculation about proof quality in inaccessible appendix:* REMOVED per policy.
- *β threshold phrasing critique:* REMOVED as a minor phrasing artifact that does not affect understanding.

## Novel Insights

Beyond the paper's own contributions, the most valuable observation from the reviews is the Gap metric's potential aggregation bias: averaging absolute deviations against a Retrained reference with heterogeneous scales (UA~0, RA~99, TA~95, MIA~100) means that two methods with radically different failure modes — one failing to forget (UA=10, everything else perfect) and one destroying utility (RA=89.51, everything else perfect) — can receive identical Gap scores. This is a methodological note applicable beyond this specific paper: any aggregate metric that averages deviations against a reference with heterogeneous scales should be complemented by per-component reporting.

## Suggestions

- Add a paragraph explicitly stating the operational goal for each of the four settings, especially model mismatch, where "forgetting" means matching the Retrained model's behavior at the superclass level (not suppressing superclass predictions).
- Fix the notation in Theorem 3.2 (λ<sub>max</sub>(J<sub>θ</sub>(·)x<sub>1</sub>) is dimensionally unclear) and position it more honestly as a qualitative justification.
- Discuss sensitivity of TARF to the known-class-number assumption.

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OHOmpkGiYK.md | 5.75 | R1, R2 | Yes | **This exact paper** — human avg 5.75 (scores 6,6,3,8). My review retains its strongest strengths and filters noise from the lower-scoring review. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/pUOesbrlw4.md | 5.25 | R1 | Yes | "Deep Unlearning" — SVD-based class unlearning. Weaker problem novelty; this paper is stronger. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/TLBPjECC5D.md | 5.25 | R1 | Yes | "Unlearning via Sparse Representations" — bottleneck-based unlearning. Incremental novelty; this paper has a more original contribution. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/CGfWyU28Pd.md | 4.50 | R1 | Yes | "Why FT Struggles" — theoretical analysis of fine-tuning. Narrower scope, weaker empirical validation. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/SIZWiya7FE.md | 6.00 | R2 | Yes | "Label-Agnostic Forgetting" — accepted. Similar mixed-review pattern (8,8,3,5). Novel problem (supervision-free). Comparable empirical scope. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/HVFMooKrHX.md | 6.60 | R2 | Yes | "Utility and Complexity of Unlearning" — accepted. More rigorous theory; minimal experiments. Different paper type. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Xagys9QD3T.md | 3.00 | R1 | No | "Pseudo-Probability Unlearning" — clearly weaker in both formulation and results. |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/hwXUmwJAq5.md | 3.00 | R1 | No | "UGradSL" — standard class unlearning with label smoothing. Less novel. |

**Bracketing and Narrowing:**

- **Round 1 bracket:** The paper sits clearly above the 3.0–4.5 range (where papers have incremental or weaker contributions) and below the 7.5+ range (papers with exceptional theoretical or empirical contributions). Initial bracket: [4.5, 7.5].
- **Round 2 narrowing:** Within [4.5, 7.5], the paper clusters near 5.75–6.0. Its own human-averaged score is 5.75. Compared to "Label-Agnostic Forgetting" (6.00, accepted), this paper has a similarly novel problem formulation but somewhat stronger empirical results on its core settings. The weaknesses I retain are all Minor (no fatal or major issues).
- **Final placement:** The paper's strengths (novel problem taxonomy, decisive results on two of three settings, ImageNet-1k validation) outweigh its weaknesses (model mismatch clarity, Gap metric aggregation, Theorem 3.2 framing, known-class-number assumption). The human reviews show a split (6, 6, 3, 8), and my filtering removes the noise from the lowest-scoring review while keeping the substantive concerns from the 6–8 reviewers.

**Final score:** 6.0 — borderline accept. The paper presents a genuinely novel problem formulation and strong empirical evidence for two of its three proposed settings. The weaknesses are real but addressable and do not undermine the core contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>