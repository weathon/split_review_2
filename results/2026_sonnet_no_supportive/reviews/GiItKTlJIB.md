## Summary
This paper introduces a deletion-based probing framework for evaluating LLM dependence on chain-of-thought (CoT) scratchpads in physics problem-solving. Applied to Phi-4, Qwen-A3B, and Magistral across three physics benchmarks (UG Physics, PhyBench, PhysReason), it documents "cramming"—a compensatory behavior where models produce longer final answers as more of the scratchpad is deleted—and uses lexical overlap metrics to assess whether deleted content is reconstructed. The paper frames these findings as evidence of shallow and opportunistic CoT reliance with implications for AI-for-science evaluation.

## Strengths
- **Cramming is a concrete, replicable finding.** The X-shaped pattern in Figures 4, 5—final answer length rising as CoT scratchpad shrinks—holds consistently across all three models, three datasets, and all three deletion strategies. The different collapse thresholds (∼40% for end deletion, ∼60% for random, 70–80% for physics-aware) are a substantive result showing how structural position and domain salience interact with model reliance on the scratchpad.
- **The three-strategy deletion design is well-motivated.** End, random, and physics-aware deletion probe distinct structural properties, and their comparison yields a coherent and non-trivial story rather than a single parametric sweep.
- **Physics as a testbed is genuinely justified.** The paper's argument (§2.1) that physics' structured vocabulary—equations, units, constants—makes overlap metrics interpretable in ways that would not hold in free-form reasoning is a real methodological advantage, not a rhetorical one.

## Weaknesses

### Fatal
None.

### Major
- **Information-overlap analysis lacks a null baseline, undermining the faithfulness interpretation.** The paper measures Jaccard similarity and Manhattan distance between deleted CoT spans and regenerated final answers (§2.4, Figure 7), interpreting increasing overlap as evidence that models reconstruct deleted content. However, any two correct solutions to the same physics problem naturally use the same equations, constants, and units—not because one was copied from the other, but because those are the correct physics. No baseline is provided: e.g., overlap between two independently generated correct solutions, or between a no-scratchpad answer and the original CoT. Without this, the observed overlap increase could reflect shared domain vocabulary rather than specific reconstruction. The paper acknowledges "surface-level similarity rather than genuine fidelity" (§4.2)—but that acknowledgment also undermines the interpretation that meaningful recovery is happening at all. A null-baseline measurement is necessary before the faithfulness analysis in §4.2–§4.3 can be trusted.

- **"Cramming" vs. from-scratch solving is never distinguished.** The cramming framing implies that models specifically compensate by drawing on the deleted scratchpad. But an equally consistent—and simpler—explanation is that models solve the question de novo from the problem statement when the scratchpad is missing, naturally producing a longer standalone answer. The paper includes no zero-CoT control (model prompted to answer without any scratchpad) to compare answer length and content against the cramming condition. §4.1 notes "we do not probe internal mechanisms directly," but the alternative hypothesis is also not tested empirically. Without this control, "cramming" is a label on an observation that the simpler hypothesis also predicts.

- **The evaluation metric (Claude-4 Sonnet judge) is not validated against ground truth.** All main accuracy trends rest on 0–1 scores assigned by Claude-4 Sonnet (§2.4). The calibration study (§3.1) establishes statistical stability across re-runs, but stability ≠ validity. A consistently wrong judge is stable. No comparison against ground-truth labels (e.g., exact-match on multiple-choice PhysReason questions, verified numerical answers) is reported. LLM judges of physics derivations are known to accept plausible-sounding but numerically incorrect solutions, which matters directly for whether the accuracy-drop trends at high deletion fractions are trustworthy.

### Minor
- **Difficulty ordering inconsistent with Figure 2.** §2.1 states "UG Physics (easiest)... PhyBench (hardest)," but Figure 2's y-axis ranges are 0–0.5 for UG Physics and 0–0.8 for PhyBench. If axis ranges reflect actual score ranges, models score higher on the nominally "harder" benchmark, which is unexplained and conflicts with the stated ordering.

- **Manhattan distance normalization/inversion in Figure 7 is undescribed.** Manhattan distance is a distance (larger = less similar), yet it is plotted alongside Jaccard similarity on a common "Scaled Metric Value" axis in Figure 7. The normalization and inversion procedure is not specified in §2.4 or the figure caption, making Figure 7 difficult to interpret and hampering reproducibility.

- **Unresolved tension in practical recommendation.** §4.3 recommends early stopping of CoT generation as "a cost-effective way to save tokens without proportionally sacrificing accuracy." But the paper's own findings indicate that cramming produces heuristic reconstruction of uncertain faithfulness. For scientific applications—the stated motivation—advocating early stopping with cramming as the fallback is potentially counterproductive and conflicts with the cautionary framing in the rest of §4.3.

### Trivial
- Physics-aware deletion tags physics tokens via Claude-4 Sonnet with no inter-rater validation. Given this strategy produces the noisiest results, some characterization of tagging quality would be useful.

## Nice-to-Haves
- Add a zero-CoT control (model prompted to answer with no scratchpad at all) to distinguish cramming from from-scratch solving; compare answer length and content to the deletion-sweep results.
- Report null-baseline overlap: Jaccard between two independently generated correct solutions to the same question, to calibrate whether observed overlap increases are meaningful.
- For benchmarks with available ground-truth (e.g., multiple-choice PhysReason), compare Claude judge scores against exact-match accuracy to validate the judge.
- Clarify the normalization/inversion of Manhattan distance in §2.4 and Figure 7 caption.
- Reconcile the difficulty ordering in §2.1 with Figure 2's y-axis ranges.

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Novelty framing critique**: The harsh critic argues the introduction overstates novelty by implying the faithfulness gap is "largely unaddressed." §1 in fact says "while prior work has examined CoT faithfulness in general settings, its implications for AI-for-Science remain underexplored"—this is accurate scoping, not overclaiming. **REMOVED.**
- **Sample size instability across k∈[0,100]**: The critic questions whether each data point in the deletion sweep is stable. The paper's calibration effort (§3.1) shows 5 runs over 50 questions are sufficient, and Figure 7 shows standard error bands. This is a reasonable effort that addresses the concern; absent specific evidence of instability at particular k values, this is speculative. **REMOVED.**
- **Strength "choice of physics is justified"**: Retained in strengths above as it is concrete and paper-specific.
- **Strength "evaluation has not kept pace" (generic importance claim)**: REMOVED as generic; the specific technical strengths are retained instead.

## Novel Insights
The cramming phenomenon—where deleted CoT triggers longer, more elaborated final answers—is a genuinely novel and cleanly documented behavioral observation. The systematic comparison of three deletion strategies with different collapse thresholds reveals that structural position (truncation vs. random scatter) and domain salience (physics-specific vs. general tokens) interact differently with CoT dependence, which is a nuanced and useful finding. However, the inability to distinguish cramming from from-scratch solving means the mechanism remains open: whether cramming is reconstruction or re-solving is itself an important scientific question that this paper raises but cannot yet answer.

## Suggestions
1. Add a zero-CoT baseline condition to directly test whether cramming behavior differs from unaided from-scratch answering.
2. Report a null-baseline overlap (e.g., between two independent correct solutions) to calibrate the information-overlap analysis.
3. For benchmarks with deterministic answers, validate Claude judge scores against exact-match ground truth.
4. Clarify the Manhattan distance normalization/inversion procedure in §2.4.
5. Reconcile the difficulty ordering claim in §2.1 with Figure 2.

---

## Score and Decision

**Anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `1OyE9IK0kx.md` (Hardness of Faithful CoT) | 5.00 | R1 | Most directly comparable topic; broader theoretical framing, also rejected |
| `w6nlcS8Kkn.md` (To CoT or not to CoT) | 6.67 | R1 | Accepted; far more comprehensive (100+ papers, 20 datasets, 14 models) than the paper under review |
| `asGQQc7gNo.md` (Factuality vs. faithfulness) | 6.67 | R1 | Accepted; well-validated metrics and comprehensive analysis |
| `rpbzBXdo4x.md` (Mind Your Step) | 5.00 | R1 | Rejected; similar CoT behavioral characterization, comparable scope |
| `FP77VtEuaT.md` (LLM Reasoning via 3-SAT) | 5.25 | R1 | Rejected; principled LLM reasoning characterization, similar empirical scope |
| `awtd0XhzKQ.md` (FLARE) | 5.75 | R1 | Rejected; proposes faithful CoT method, more actionable |
| `pXIbcRPxWR.md` (Supervised CoT) | 2.50 | R1 | Rejected; much weaker paper |
| `Q6a9W6kzv5.md` (PhysBench) | 8.00 | R1 | Accepted; well-engineered, comprehensive physics benchmark—far stronger than the paper under review |
| `9OevMUdods.md` (Factual Knowledge of LLMs) | 6.75 | R1 | Accepted; rigorous factual benchmark study, better validated |

**Round 1 bracket: 4–5.**

The paper has a concrete and novel empirical finding (cramming), a sensible multi-strategy design, and genuine motivation in the AI-for-science context. However, three major methodological gaps—no zero-CoT control, no null overlap baseline, and an unvalidated judge—prevent the paper from fully supporting its primary interpretive claims about cramming and faithfulness. The closest topical anchors (hardness of faithful CoT, Mind Your Step) both scored around 5 and were rejected. The accepted papers in the 6.5–7 range (To CoT or not to CoT; factuality/faithfulness trade-off) are substantially more comprehensive and methodologically tighter. The paper under review sits below those thresholds. Given the genuine novelty of the cramming observation but the significant evidential gaps in the faithfulness analysis, I score this at **4.0** (borderline reject).

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>