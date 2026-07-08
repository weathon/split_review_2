## Summary

This paper introduces **SpookyBench**, a synthetic benchmark where information is encoded solely through motion patterns in noise-like frames (individual frames contain no spatial structure). The benchmark uses opposing-noise motion to reveal text, object silhouettes, and depth-mapped dynamic scenes. Human participants achieve >98% accuracy, while all 23 evaluated VLM variants (2B–78B, including GPT-4o and Gemini 2.0 Flash) score 0% — including after fine-tuning on 400 training videos. The paper argues this reveals a fundamental "time blindness" in current VLMs' inability to extract meaning from temporal patterns when spatial cues are removed.

## Strengths

- **Creative and clean benchmark design (Section 3, Algorithms 1–2).** The opposing-noise motion encoding is genuinely novel. Individual frames contain no spatial information; content is revealed only through coherent pixel motion across frames. The two generation algorithms are fully specified and deterministic. The dataset can be expanded indefinitely via the generator.

- **Comprehensive model coverage (Table 1).** Evaluation spans 23 model variants across 15+ families and sizes from 2B–78B, including GPT-4o, Gemini 1.5 Pro, and Gemini 2.0 Flash. The consistent 0% result across this entire sweep is the paper's strongest empirical finding.

- **Fine-tuning negative result (Section 4.4).** Training InternVL2.5-8B and Qwen2-VL-7B on 400 SpookyBench videos for 10 epochs yields 0% test accuracy. This rules out domain mismatch / distribution shift and meaningfully strengthens the claim that the limitation is architectural rather than data-driven.

- **Frame-rate ablation (Section 4.3, Tables 4–5).** Human accuracy degrades from 95.6% at 30 FPS to 0% at 1 FPS, while all VLMs remain at 0% across all frame rates. This cleanly decouples the human limitation (insufficient temporal resolution) from the model limitation (zero capability at any resolution).

## Weaknesses

### Fatal
None.

### Major

- **Framing inflation — the paper overstates its findings by describing SpookyBench as a test of "purely temporal understanding" and labeling VLMs as "time-blind."** The task is **motion-based figure-ground segregation** to reveal static spatial shapes (text glyphs, object silhouettes). The motivating examples (firefly bioluminescence rhythms, Morse code intervals) involve temporal *interval* and *sequence* processing — categorically different from the motion-revealed spatial shapes in SpookyBench. The core finding — that VLMs cannot extract content from motion patterns when individual frames lack spatial structure — is real and interesting. But the "temporal reasoning / time-blind" framing inflates the contribution by at least one level of abstraction. The paper's own architectural recommendations (Section 5: "dedicated temporal coherence pathways") would be more precisely aimed if the task were described as motion-based spatial content recovery rather than temporal understanding. *(Verified: Abstract calls it "purely temporal patterns"; Introduction says "purely temporal reasoning" and "temporal pattern recognition"; Section 3 says "all meaningful information is encoded exclusively in the temporal domain"; Section 6 calls models "time-blind". The actual task is recognizing static shapes revealed through opposing-noise motion, per Algorithm 1 and Figure 2.)*

### Minor

- **Missing diagnostic baselines.** The paper does not test whether VLMs can recognize content from pre-computed optical flow or frame-difference maps. This would diagnose whether the failure is in low-level motion detection (fixable with preprocessing) or in higher-level recognition from motion signals (a deeper architectural gap). Without this decomposition, the paper's architectural recommendations ("dedicated temporal coherence pathways," Section 5) are premature.

- **Insufficient analysis of model outputs.** The paper reports 0% accuracy but provides only a brief qualitative description of model outputs ("attempts to extract information from individual frames," Section 5). A systematic analysis — how often models output "noise," describe random objects, remain silent, or produce off-target text — would strengthen the claims and help future work.

- **SNR threshold analysis disconnected from main results (Section 3.3.2).** The binary threshold discussion (0% below 2.5 dB, ~85.7% above) describes human text detection but is never connected to model performance. There is also a numeric discrepancy: the text reports "jumped to 85.7% accuracy," while Figure 4's table shows 1.00 (100% accuracy) at SNR ≥ 3 dB, and the figure caption contains a likely parser artifact ("near 1.0%"). The authors should clarify what the 85.7% figure refers to and reconcile it with the table.

- **Limited integration of neuroscience discussion (Section 2.2).** The cited literature on interval timing and duration perception (Mauk & Buonomano 2004, Paton & Buonomano 2018) concerns how the brain encodes *when* events occur and *how long* they last — tangential to the motion-based figure-ground segregation mechanism in SpookyBench. The section reads as background padding rather than a genuine connection to the paper's methodology.

- **Insufficient fine-tuning details.** The paper does not report the train/test split size (51 test videos if total is 451) or whether models achieved non-zero accuracy on the *training set*. These details would help assess the adequacy of the fine-tuning setup and the strength of the negative result.

### Trivial
- Table 5 caption contains an unclear parenthetical ("rather than temporal FPS") that appears to be an editing artifact.

## Nice-to-Haves
- An optical-flow or frame-differencing preprocessing baseline to diagnose the failure point.
- A frame-averaging baseline (since averaging moving noise frames would reveal the static content mask).
- Reporting whether fine-tuned models memorized the training set (0% on training data too would be even more revealing).
- Per-category breakdown of model results (Table 1 aggregates over categories).

## Removed Points
These points were raised in the input reviews but are removed with justification:

- *"The benchmark does not test whether the failure is specific to end-to-end VLMs or stems from lack of motion preprocessing"* — Retained as a Minor weakness above (optical flow baseline). The critic framed this as a "Critical Issue," but it is a helpful diagnostic experiment that would strengthen the paper, not a flaw that undermines existing claims. The paper's core result (0% on raw video) is valid regardless.

- *"The framing of isolating temporal from spatial understanding is imprecise"* — Merged into the Major framing weakness above. The core point (motion-based spatial recovery vs. temporal reasoning) is the same concern expressed differently.

- *"The Dynamic Scenes category is very small (12.6%)"* — The paper acknowledges the distribution and notes the generator can produce unlimited additional data. This is a reasonable scope choice, not a weakness.

- *"SNR metrics never connected to model performance"* — Covered by the SNR threshold disconnect weakness above.

- *Missing appendix content, reproduction details, hyperparameters* — The parser strips appendix/reference sections from all papers; they exist in the original submission.

## Novel Insights
None beyond the paper's own contributions. The reviews surface an important framing concern (the gap between "motion-based spatial content recovery" and "temporal understanding") but this is a corrective to the paper's framing rather than a novel insight about the results.

## Suggestions
1. **Reframe the central claims.** Replace "temporal understanding / temporal reasoning / time blindness" with more precise language describing motion-based figure-ground segregation and motion-to-content decoding. This would make the paper *less* sensational but *more* scientifically useful.
2. **Add an optical-flow preprocessing baseline** to diagnose the failure point (motion detection vs. content recognition from motion).
3. **Provide a systematic analysis of model outputs** — what do models say instead of correct answers?
4. **Resolve the numeric discrepancy** in Section 3.3.2 (85.7% vs. 1.00/100% in Figure 4) and clarify which population the analysis describes (humans? models?).
5. **Report fine-tuning details** (train/test split, training-set accuracy).

## Score and Decision

**Calibration anchors retrieved:**
| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|-----------|
| TemporalBench (Wto5U7q6I2) | 4.20 | R1 | Yes | Weaker benchmark novelty, more evaluation issues. SpookyBench is stronger. |
| MCTBench (BVACdtrPsh) | 3.00 | R1 | No | Different task; less relevant. |
| LVBench (uHgVrGF2Wn) | 4.50 | R1 | No | Long video benchmark; less relevant. |
| TC-Bench (xSOl0s1u77) | 4.75 | R1 | No | Video generation benchmark; less relevant. |
| Motion-Grounded (tEei1bolt3) | 5.00 | R1, R2 | No | Motion reasoning dataset. Similar relevance. |
| Vinoground (a1P5kh2oo8) | 5.75 | R1, R2 | Yes | Similar rejection reason (limited novelty/scope concerns). SpookyBench has higher benchmark novelty. |
| ViLMA (liuqDwmbQJ) | 6.00 | R1, R2 | Yes | Accepted. Similar overall quality, but no framing inflation issue. |
| TVBench (fCi4o83Mfs) | 6.75 | R1, R2 | Yes | Accepted. Stronger conceptual framework (three principles), better analysis. SpookyBench's benchmark design is more creative but less rigorous in framing. |
| T3 (sHAvMp5J4R) | 6.80 | R2 | Yes | Accepted. Strong diagnostic analysis, clear contribution. Different paper type. |
| Dynamic Social Vision (wAXsx2MYgV) | 7.00 | R2 | Yes | Accepted. Broader model evaluation but limited technical novelty. |

**Bracket:** Round 1 → [5.5, 7.0]. Round 2 (itemized comparison with TVBench 6.75, ViLMA 6.00, Vinoground 5.75) → narrowed to **5.5**.

**Reasoning:** The paper's strengths (benchmark novelty, comprehensive evaluation, fine-tuning control, frame-rate ablation) are competitive with TVBench (6.75) and ViLMA (6.00) — all four strengths received high model weights (8.02–10.60). However, the framing inflation weakness (weight 2.72) is a structural issue that no accepted anchor paper in this comparison exhibited to the same degree. The core finding is real and significant, but the paper's claims about "temporal understanding" misrepresent what the task actually tests by at least one level of abstraction. This places the paper below ViLMA (6.00) and Vinoground (5.75-equivalent for rejection) — strong enough to warrant revision but not accept in current form.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>