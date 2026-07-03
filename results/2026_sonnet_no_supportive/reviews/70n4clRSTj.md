Now I have enough to draft the review. Let me prepare it.## Summary
SpookyBench is a synthetic video benchmark where content (words, object images, depth-map scenes) is encoded entirely through opposing-motion noise patterns, making individual frames appear as pure noise while the content becomes perceptible only during playback. The paper evaluates 27 VLMs ranging from 2B to 78B parameters alongside 6 human participants, finding a complete capability gap: humans achieve 98% accuracy while every model achieves 0%. A frame-rate ablation shows humans need ≥20 FPS and degrade predictably, while VLMs fail at all tested rates; a fine-tuning ablation shows direct training on SpookyBench data does not improve model accuracy above 0%.

---

## Strengths

- **Dramatic, consistent empirical result spanning 27 models.** Table 1 reports 0% accuracy for every model across parameter scales (2B–78B), architectures, access modes, and two prompting strategies. The uniformity eliminates architecture- or scale-specific explanations.
- **Fine-tuning ablation (Section 4.4) rules out distribution shift.** InternVL2.5-8B and Qwen2-VL-7B trained for 10 epochs on 400 SpookyBench videos still achieve 0% on the held-out test set, supporting an architectural rather than data-exposure explanation.
- **Frame-rate experiment (Section 4.3, Tables 4–5) is a well-designed control.** Human accuracy drops predictably from 95.6% at 30 FPS to 0% at 1 FPS; all four VLMs tested score 0% at every frame rate. This isolates the gap as independent of temporal sampling frequency.
- **Fully reproducible dataset generation.** Algorithms 1 and 2 are deterministic and completely specified with explicit noise density, speckle size, velocity, and resolution parameters; the dataset can be extended indefinitely.

---

## Weaknesses

### Fatal
None.

### Major

- **Section 3.3.2 is internally contradictory.** The section claims (a) word detection "jumped to 85.7% accuracy above [2.5 dB] threshold"; (b) "Prompts performed best (40% accuracy)"; and (c) Figure 4 shows accuracy at 100% for all SNR > 2.5 dB. These three numbers (85.7%, 40%, 100%) are mutually inconsistent and the referent for "Prompts" is never identified — it could be a model, a prompting strategy on a subset, or a human condition. If Figure 4 represents model performance, it directly contradicts Table 1 (0% for all models under all conditions), which is a factual inconsistency in the paper. If it represents human performance at synthetically varied SNR levels, it should be in the human evaluation section and labeled accordingly. As written, this section undermines the credibility of the SNR threshold analysis and makes a portion of the paper unreliable.

- **Framing substantially overgeneralizes what SpookyBench measures.** SpookyBench tests one specific perceptual mechanism: motion-defined figure-ground segregation, where opposing optical flow fields between foreground and background noise cause humans to group pixels by motion direction (described explicitly in Figure 2 and Algorithms 1–2). The paper diagnoses VLMs with "time blindness" and "inability to capture purely temporal patterns" as a general property. However, temporal reasoning in video encompasses event ordering, causal inference, duration estimation, and action recognition—none of which SpookyBench tests. The paper's architectural prescriptions ("dedicated temporal coherence pathways," "motion contrast analysis") and neuroscience framing (parietal cortex population clocks, interval timing) are mismatched with the specific mechanism demonstrated, which is optical flow–based figure-ground segmentation. This does not invalidate the empirical finding, but it substantially overstates what can be concluded from SpookyBench about VLM "temporal reasoning" broadly.

### Minor

- **Dynamic Scenes category uses a perceptually distinct encoding mechanism.** Algorithm 1 (words and images) uses opposing motion between foreground and background — a bilateral flow cue. Algorithm 2 (dynamic scenes from depth maps) uses threshold-based animation where pixels above a brightness threshold move while others stay static — a unilateral cue with no opposing flow. These are not the same perceptual task, yet both are presented as testing the same "purely temporal understanding" mechanism. The paper does not acknowledge or discuss this distinction.

- **Number of frames provided to VLMs is unspecified.** Section 4.1 states "We input sequences of multiple video frames simultaneously for models that do not directly support video input," but the exact frame count is never stated. Videos average 333.5 frames; standard VLM practice typically uses 8–16 frames, representing extremely sparse sampling. While Table 5 shows 0% at all tested FPS conditions, the correspondence between per-model frame count and the FPS sweep used in the human experiment is not established.

- **Small human baseline (n=6).** Six participants anchor the 98% figure that underpins the entire benchmark's claim. The qualitative gap is large enough (98% vs. 0%) that the conclusion is not overthrown, but the ±0.6% confidence interval in Table 1 is almost certainly underestimated at n=6. For a benchmark paper, the human baseline is the central comparator.

### Trivial
None.

---

## Nice-to-Haves
- An analysis of fine-tuned model output distributions — do fine-tuned models output random labels, a constant label, or labels that pattern-match training examples? The paper notes they "mimicked training examples without correctly identifying test patterns" (Section 5), but a quantitative breakdown would sharpen the architectural diagnosis.
- Testing a VLM augmented with explicit optical flow features (e.g., RAFT-computed flow maps supplied alongside frames) would directly test whether the failure is architectural (flow cannot be computed from per-frame features) vs. representational (flow information is not in training distribution).
- The binary SNR threshold finding — if properly measured and attributed — parallels detection threshold phenomena in medical imaging and adversarial robustness and would be worth presenting cleanly as a standalone human psychophysics result.

---

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Missing psychophysics citations (Julesz random dot kinematograms, Johansson biological motion).** Removed per the rule prohibiting criticism based on missing related work; reviewer does not have external sources to confirm these citations' precise relevance.
- **Claim that the "0% model finding is already established."** TemporalBench and TVBench do not show complete 0% failure — they show significant but partial performance. SpookyBench's complete elimination of spatial cues and the resulting 0% is a genuinely distinct contribution.
- **Criticism about the claim that GPT-4o, Gemini 2.0 Flash, etc. exist and are available.** Removed per hard rule; the paper cites these models, they exist.
- **Reproducibility complaint about missing hyperparameters.** Algorithms 1–2 and the Reproducibility Statement are explicit; removed per the rule on trivial reproducibility nitpicks.
- **Demand for larger dataset.** 451 videos generating 0% accuracy across 27 models is sufficient for the benchmark's central claim; requesting more videos is not substantive.

---

## Novel Insights
The most genuinely novel observation in this paper is that fine-tuning directly on SpookyBench training samples — same distribution, same task, 10 epochs — yields 0% test accuracy. This is a stronger claim than distributional mismatch accounts for and points to the absence of a learnable signal in per-frame features, not merely a generalization failure. This null fine-tuning result is underanalyzed in the paper but is arguably the most compelling evidence that the limitation is architectural rather than a training data gap.

---

## Suggestions
1. **Rewrite Section 3.3.2 as two distinct analyses**: a human psychophysics experiment (accuracy vs. synthetically varied SNR) and a separate model analysis (if any). Reconcile all reported accuracy values (85.7%, 40%, 100%) with Table 1.
2. **Narrow the framing** from "temporal reasoning broadly" to "motion-defined figure-ground segregation" — this makes the architectural prescription (integrating optical flow computation) concrete and falsifiable.
3. **Specify the exact frame count given to each VLM**, and if it differs substantially from 30 FPS-equivalent sampling, discuss the implication.
4. **Expand human baseline** to ≥20 participants for a benchmark intended as a community reference point.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| Wto5U7q6I2 (TemporalBench) | 4.20 | R1 | Video temporal benchmark, ~10K QA pairs, partial model failure (~38% best); rejected |
| fCi4o83Mfs (TVBench) | 6.75 | R1 | Temporal reasoning VLM benchmark, 1484 annotated QA, principled methodology, cleaner presentation; accepted |
| liuqDwmbQJ (ViLMA) | 6.00 | R1 | Video-language benchmark with counterfactuals, task-agnostic; accepted |
| a1P5kh2oo8 (Vinoground) | 5.75 | R1 | Temporal counterfactual benchmark, 1000 pairs, partial model failure; rejected |
| BTr3PSlT0T | 3.75 | R1 | Video reasoning evaluation suite, heterogeneous quality; rejected |
| tEei1bolt3 | 5.00 | R1 | Motion-grounded video reasoning benchmark, more elaborate but limited; rejected |
| bEvI30Hb2W | 3.00 | R1 | Long-form video reasoning model, no benchmark contribution; rejected |
| YGWxpOI6Y0 | 3.40 | R1 | VideoGPT+ method paper, not primarily a benchmark; rejected |

**Round 1 bracket: 4.5–6.0.**

SpookyBench is stronger than TemporalBench (4.2) in the drama of its finding (0% vs. partial failure) and the quality of its ablations. It is weaker than TVBench (6.75) due to the confusing SNR section (an internal contradiction), the limited scope (451 videos, single perceptual mechanism), the overgeneralized framing, and the very small human study. Vinoground (5.75, rejected) is a reasonable comparator: clean design, limited scope, strong empirical finding but insufficient to carry the paper to acceptance at a strong venue.

The Section 3.3.2 contradiction is a genuine major flaw — it is not speculative, it is demonstrably present in the paper as written: three mutually inconsistent accuracy numbers with no clear referent, and the figure potentially contradicting Table 1. Combined with the scope-claim mismatch, the paper needs significant revision. However, the core empirical contribution (0%/98% gap, fine-tuning ablation, frame-rate control) is real and will be useful to the community. 

**Final score: 5.0 (borderline reject).**

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>