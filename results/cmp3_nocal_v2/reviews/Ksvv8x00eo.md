## Summary

CaTS-Bench is a large-scale, multimodal benchmark for context-aware time series captioning, built from 11 real-world datasets (health, climate, border crossing, safety, agriculture, sales, demography) yielding 20k samples. Each sample pairs a numeric series segment with contextual metadata, a line-plot image, and a validated caption. The paper introduces a scalable pipeline for generating semi-synthetic references (oracle LLM + factual verification + human indistinguishability study + diversity analysis), a human-revisited subset of 579 captions, 460 multiple-choice Q&A items, and tailored evaluation metrics (Numeric Score, Statistical Inference Accuracy). A comprehensive evaluation of proprietary and open-source VLMs reveals that finetuning substantially improves open-source models, but VLMs largely fail to leverage visual inputs, exposing a genuine gap in multimodal alignment.

## Strengths

- **Scale and diversity of the benchmark.** CaTS-Bench spans 11 real-world datasets across 7 domains with numeric + text + visual modalities, rich metadata, expressive captions, and Q&A tasks. Table 1 clearly shows that existing TSC benchmarks (TADACap, TRUCE, TACO) are narrower in domain coverage and modality; CaTS-Bench is the only one that simultaneously offers all three modalities with both captioning and Q&A.

- **Rigorous quality validation of semi-synthetic captions.** Three complementary verification studies (Section 3.2) — manual factual checking of 72.5% of test captions (98.6% accuracy), a 35-participant blind detectability study (41.1% detection rate, near random), and diversity/bias analysis across nine embedding models — substantially address the legitimate concern about LLM-generated references. This is notably more thorough than typical synthetic-benchmark verification.

- **Tailored evaluation metrics that capture what matters for TSC.** The Numeric Score (recall-weighted with λ_R=0.7, penalizing omissions more than imprecision) and Statistical Inference Accuracy (treating wrong values as errors, ignoring omissions — a sensible hallucination detector) are genuinely motivated by the limitations of generic NLP metrics for time series. The metric design choices are clearly justified.

- **Visual modality ablation revealing a genuine VLM limitation.** The experiment in Section 4.3 (Figure 4) cleanly shows that removing the line-plot image produces marginal performance changes and often improvements across multiple VLMs. This finding — that current models default to textual priors — is important and correctly framed by the paper as a limitation of VLM architectures rather than a benchmark flaw.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Oracle-as-reference and oracle-as-baseline creates a methodological tension that is documented but not fully resolved.** Gemini 2.0 Flash generates the primary semi-synthetic reference captions AND is evaluated as a baseline. The paper's defenses are substantive — the oracle receives privileged metadata unavailable at evaluation time (line 69), the paraphrasing robustness check yields ρ=0.9266 (lines 213-240), and the human-revisited (HR) evaluation in Table 3 provides a direct comparison. Crucially, Table 3 shows that Gemini 2.0 Flash does not dominate rankings under either reference: finetuned LLaVA (0.712 HR / 0.758 SS) and finetuned Idefics 2 (0.711 HR / 0.759 SS) surpass it on DeBERTa F1 against both SS and HR ground truths. These data partially resolve the concern. However, the remaining risk — that stylistic overlap between Gemini-generated references and Gemini evaluation outputs could inflate surface-level metrics (BLEU, ROUGE-L) — is not directly tested, e.g., by computing whether Gemini's rank against HR captions is statistically distinguishable from its rank against SS captions. The human-revisited subset covers only 4 of 11 domains with 579 samples, limiting the power of this comparison.

2. **The Q&A task filtering by a single model's performance introduces unvalidated selection bias.** Section 3.4 (line 144): "an initial pool of 4k questions per type was filtered by removing those correctly answered by Qwen 2.5 Omni." The paper references Appendix J.2 claiming this produces "genuinely harder questions, rather than reflecting Qwen-specific weaknesses only." However, single-model filtering is a known pitfall in benchmark construction — if Qwen 2.5 Omni has systematic blind spots (e.g., certain types of trend reasoning or statistical comparisons), the remaining questions will disproportionately exploit those blind spots, creating a test set that is hard-for-Qwen but not necessarily hard-in-general. The paper should demonstrate filtering robustness across architecturally diverse models, or at minimum acknowledge this limitation explicitly in the main text.

3. **The claim that models "largely ignore visual inputs" is stronger than the evidence cleanly supports.** The visual ablation (Section 4.3) shows marginal changes when the plot is removed. The paper interprets this as models "largely [disregarding] visual cues in favor of textual priors" (line 283). An equally plausible alternative is that the serialized numeric values provided as text (e.g., `[25.3, 26.1, 26.8, ...]`) already encode all trend information present in the plot, making the visual channel redundant rather than ignored. The visual attention analysis (line 283) supports the paper's interpretation but is described only qualitatively ("minimal visual grounding," "sporadic, weak, and inconsistent"). Quantitative attention metrics (e.g., fraction of attention weights on plot lines vs. axis text) would substantially strengthen the case. The paper's conclusion is likely correct given the supporting Q&A result that all models perform near-random on plot matching (Section 4.2), but the ablation itself does not cleanly distinguish "ignored" from "redundant."

4. **No human baseline for the primary captioning task.** The paper provides a human baseline for Q&A tasks (Section 4.2; humans achieve near-perfect on plot matching) but not for time series captioning. This makes it difficult to calibrate the reported scores — e.g., is a DeBERTa F1 of 0.688 good? Is a BLEU of 0.137 meaningful? While the subjective nature of captioning (no single ground truth) makes a human baseline harder to construct, even a small-scale human captioning study (50–100 samples) would provide an interpretability anchor for the benchmark.

5. **Confidence intervals / significance tests are missing for close model comparisons.** The paper reports variance from three runs as "vanishingly small (often 10⁻⁶)" but does not report confidence intervals or significance tests. Some top-performing models are separated by tiny margins (e.g., 0.712 vs. 0.711 DeBERTa F1 on HR, Table 3). Without significance information, readers cannot determine whether these differences are meaningful.

### Trivial

- **"Timestamps" vs. "samples" in abstract.** The abstract states "465k training and 105k test timestamps" while Section 3.1 describes "20k triplet samples" and Table 2 shows 16k train + 4k test samples. These refer to different quantities (total time steps vs. window crops), but the relationship is unclear on first reading and should be stated explicitly.

## Nice-to-Haves

- **Per-domain results would make the benchmark more diagnostic.** Given the dramatic variation in sample lengths across domains (Crime avg. 76.8 steps vs. Injury avg. 5.9 steps), reporting per-domain performance would reveal whether certain model families excel on short series while failing on long ones, and would increase the benchmark's utility as a diagnostic tool. (The paper notes full results are in Appendix G.)

- **A control experiment where numeric values are removed and only the plot + metadata are provided** would cleanly separate "visual ignored" from "visual redundant." If models collapse under this condition, it would confirm genuine visual-reasoning capability in current models; if they already collapse, it would strengthen the paper's claim.

## Removed Points

These points were removed from the main review for the following reasons:

- **"Window length ranges per dataset not specified"** — Removed. The paper states these are in Appendix C ("see Appendix C for our range calculation"), and the parser strips appendices. The information exists in the original submission.
- **"Gramian Angular Fields and recurrence plots receive only one sentence"** — Removed. The paper references Appendix I.3 for the full discussion; the main text is a summary by design.
- **"Domain-level results not shown"** — Removed as a weakness; moved to Nice-to-Haves. The paper notes "complete results in Appendix G."
- **"Statistical significance for model comparisons" from the Strengthening section** — Retained as a Minor weakness (see #5 above), but the reviewer's framing as a "missing part" was correct; it's already in Minor.
- **"The paper does not test whether the oracle model has an unfair advantage by comparing rankings against HR vs. SS"** — Removed. The paper already does this in Table 3 (both HR and SS columns for all models), and the data show Gemini does not dominate rankings in either setting.

## Novel Insights

The reviews surface one genuinely novel observation beyond the paper's own contributions: the visual modality finding (Section 4.3) and the plot-matching near-random performance (Section 4.2) together form a convergent picture that current VLMs have a fundamental, not just incremental, gap in time series visual reasoning. The paper demonstrates this through two independent channels (captioning ablation + multiple-choice plot matching), and the reviews correctly emphasize that this convergence strengthens the claim more than either channel alone. The reviews also highlight that the ablation alone leaves the "ignored vs. redundant" ambiguity, which the plot-matching result helps resolve — a synthesis the paper could make more explicit.

## Suggestions

1. **Clarify the visual modality interpretation.** Add a sentence explicitly acknowledging that the numeric text input may render the visual redundant, and note that the near-random plot-matching performance (Section 4.2) resolves the ambiguity by showing models fail even when the visual is the *only* way to answer.
2. **Run a cross-model filtering robustness check for the Q&A task.** Re-filter the question pool using 2–3 architecturally diverse models (e.g., a GPT model and a different open-weight model) and report what fraction of questions survive all filters. If the surviving set is largely the same, the bias concern is addressed.
3. **Compute confidence intervals for the top-model comparisons in Tables 3 and 4.** Even bootstrapped 95% CIs over the 4k test samples would let readers judge whether margins like 0.712 vs. 0.711 are meaningful.
4. **Explicitly state in the abstract** that the 465k/105k "timestamps" refer to total time steps across all window crops, while the benchmark comprises 20k samples (16k train + 4k test).

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>