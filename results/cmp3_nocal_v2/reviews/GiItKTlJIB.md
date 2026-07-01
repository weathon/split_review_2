Now let me produce the final consolidated review.

## Summary

This paper introduces a deletion-based probing framework to evaluate how much LLMs depend on their chain-of-thought (CoT) scratchpads for physics problem solving. By intercepting CoT mid-generation, deleting tokens via three strategies (end, random, physics-aware), and measuring downstream effects on accuracy, answer length, and information overlap, the authors find that models maintain accuracy under heavy deletion (40–60%) and exhibit "cramming"—reconstructing missing reasoning in final answers. The study covers three open-source LLMs (Phi-4, Qwen-A3B, Magistral) and three physics benchmarks.

## Strengths

- **Creative and well-executed experimental paradigm.** The deletion-based probing framework (intercepting CoT mid-generation, removing tokens, then measuring downstream effects) is a natural and effective way to study CoT dependence. The sweep over three deletion strategies (end, random, physics-aware) provides useful breadth that goes beyond any single manipulation approach.

- **The "cramming" observation is a genuinely interesting and robust empirical finding.** The finding that final answer length increases sharply under CoT deletion, with an "X-shaped" pattern (Section 3.2, Figures 5–6), is documented across all three models, all three datasets, and all three deletion strategies. The cross-strategy consistency (end deletion at ~40%, random at ~60%, physics-aware at 70–80%) gives this behavioral observation real empirical weight.

- **Good breadth of models and benchmarks.** Testing across Phi-4 (14B), Qwen-A3B (30.5B MoE), and Magistral (24B) on three benchmarks of varying difficulty (UG Physics, PhysReason, PhyBench) provides reasonable evidence that the observed trends are not idiosyncratic to one architecture or dataset.

## Weaknesses

### Fatal

None.

### Major

- **Core confound: the experimental design cannot distinguish robustness from unfaithfulness, yet the paper consistently frames results as evidence of the latter.** A model that has internalized physics knowledge should be expected to maintain accuracy under partial deletion of its scratchpad—this is robustness, not necessarily bypassing. The paper defines faithfulness (Section 1) as whether the scratchpad "faithfully represents the computations that yield the final answer" — a causal claim. But the deletion experiments test functional dependence (does the model need the CoT?), not causal faithfulness. Section 4.1 acknowledges that models "may draw on internalized physics knowledge," yet the abstract ("shallow and opportunistic reliance"), Section 4.3 ("CoT scratchpads...can be bypassed"), and conclusion all frame the results as evidence of unfaithfulness. This mismatch between evidence and framing is the paper's most significant weakness. The empirical observations are valuable; the over-interpretation is not.

- **The LLM-as-judge (Claude-4 Sonnet) is used without any validation against ground-truth correctness.** For physics problems with objectively checkable answers (especially numerical problems with tolerance-based answers on PhyBench and PhysReason), relying entirely on a single LLM judge without human validation, inter-annotator agreement, or comparison against exact-match metrics is a significant methodological gap. Section 2.4 states the judge produces a single 0–1 score rolling together "correctness, derivation accuracy, logic, formatting, and clarity." If deletion manipulations affect formatting or clarity in ways that influence Claude-4 but not actual correctness, the accuracy curves (Figures 3–4) could partially reflect style changes rather than reasoning degradation. This paper makes quantitative claims about accuracy under deletion; the evaluation instrument for those claims is uncalibrated.

### Minor

- **The information overlap metrics (Jaccard similarity, Manhattan distance on bag-of-words) are too crude to support the faithfulness claims drawn from them.** Two mathematically equivalent physics derivations can express the same reasoning with different vocabulary, while high token-level overlap can arise from standard physics terminology ("F = ma," "Newton's second law") regardless of reasoning recovery. The paper acknowledges this as "surface-level similarity" (Section 4.2) but then uses the overlap results to support claims that "reconstruction is heuristic and opportunistic rather than systematic" (Section 4.2) and that CoT reliance is "shallow and opportunistic" (abstract). The gap between what token-overlap metrics measure (lexical reuse) and what the paper claims they measure (reasoning recovery fidelity) is substantial and unbridged.

- **The faithfulness concept shifts between causal and functional definitions.** Section 1 defines faithfulness causally (whether the scratchpad "represents the computations that yield the final answer"). Section 4.3 echoes this. But the experiments test functional dependence (whether the model needs the CoT to produce correct answers). These are different concepts: a model could faithfully use its CoT (causally) while being robust to deletion due to redundancy or internal knowledge. This conflation weakens the paper's conceptual precision.

- **No objective correctness numbers are reported.** For physics benchmarks with verifiable answers—especially PhyBench's Olympiad-style problems and PhysReason's reasoning-based questions—the paper relies entirely on Claude-4 scores. Even a supplementary table showing exact-match or tolerance-based numerical accuracy would substantially strengthen the evidence that the qualitative patterns hold under objective evaluation.

### Trivial

- **The number of test questions used in the main deletion sweeps is not clearly stated.** The calibration study (Section 3.1) uses 50 UG Physics questions with 5 re-runs, but the sweep experiments do not transparently report how many questions per benchmark were used, making it hard to assess statistical power.

## Nice-to-Haves

- **Add a zero-CoT direct-answer baseline** to calibrate whether maintained accuracy under 40% deletion is impressive or expected. Section 3.1 compares prompting styles (high/medium/low reasoning) but does not clearly report the accuracy of direct answer without any scratchpad.
- **Statistical significance tests** for differences between deletion strategies, models, and datasets would strengthen claims that currently rely on visual inspection.
- The **physics-aware deletion** strategy uses Claude-4 Sonnet both to identify physics-related tokens for deletion and to evaluate the final answer, introducing a potential correlated-bias concern. Since the main findings replicate across all three deletion strategies, this is not a fundamental issue, but acknowledging it would improve transparency.

## Removed Points

These points are flagged to be removed; treat them with caution:

- "The question is genuine and well-motivated" — Generic strength without specific evidence anchored to this paper's content. Removed.
- "Physics-aware deletion circularity is a critical/evidential issue" — Demoted to nice-to-have because the main findings (cramming, stable accuracy under deletion) replicate across end and random deletion, which do not use Claude-4 for tagging. Only one of three strategies is affected.
- "No zero-CoT baseline is an evidential issue" — Demoted to nice-to-have because the paper's experiments study partial deletion; the relevant comparison is against full CoT, which is reported.
- Section-by-section commentary on abstract, introduction, etc. — These are category-driven commentary rather than specific, anchored weaknesses. The substantive concerns they raised are already captured in the weaknesses above.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the contribution** from "CoT is unfaithful" to "CoT exhibits redundancy and models show robustness to deletion." The cramming observation, the differential effects of annotated vs. non-annotated deletion, and the X-shaped length pattern are genuinely interesting empirical findings that do not require the faithfulness framing. Reframing would align the paper's claims with what the evidence supports.

2. **Add objective correctness metrics** (exact-match or tolerance-based accuracy) to complement and validate the LLM-as-judge scores. For physics problems with verifiable answers, this would substantially strengthen the evaluation and address the most significant methodological gap.

3. **Explicitly address the robustness/unfaithfulness confound** in the limitations section and adjust the strongest claims in the abstract and conclusion to match what the experimental design can actually establish.

4. **Clearly state the number of test questions** used in each deletion experiment to improve transparency.

## Score and Decision

The paper introduces a creative experimental paradigm and documents a genuinely interesting behavioral pattern (cramming) across three models and three benchmarks. However, the paper's central claims about CoT unfaithfulness go beyond what the experimental design can establish, and the evaluation relies on an unvalidated LLM-as-judge for physics problems with objectively checkable answers. These are structural rather than cosmetic issues. With a reframed interpretation and additional evaluation metrics, this work could make a solid contribution. In its current form, the gap between the evidence and the strongest claims is too wide.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>