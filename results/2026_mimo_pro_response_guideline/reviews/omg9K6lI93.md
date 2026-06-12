Now I have enough data to calibrate. Let me assess the paper against the anchors:

**Anchor analysis:**

| Anchor Paper | Avg Score | Decision | Relevance |
|---|---|---|---|
| "Evading Data Contamination Detection" | 4.25 | Reject | Very relevant - contamination evasion, similar methodological concerns |
| "Benchmark Inflation" | 4.25 | Reject | Relevant - contamination detection methodology, limited scope |
| "Elephants Never Forget" | 4.75 | Reject | Relevant - memorization/contamination testing |
| "How much can we Forget about Data Contamination?" | 6.75 | Reject | Very relevant - more rigorous, has theory + extensive experiments |
| "Detecting Pretraining Data" (Min-K% Prob) | 6.25 | Accept | Very relevant - foundational detection method, clean contribution |
| "To the Cutoff... and Beyond?" | 6.75 | Accept | Very relevant - longitudinal contamination analysis |
| "LiveBench" | 7.33 | Accept | Relevant - contamination-free benchmark |

**Round 1 Bracket: 3.5–5.0**

Our paper has genuine novelty (multilingual contamination angle, IDR extension, task-divergent findings) but suffers from a significant data volume confound, internal inconsistency between Section 4.2 and Table 2, and abstract overclaiming. It's comparable to the 4.25 "Evading" paper but with broader experiments; it's notably less rigorous than the 6.75 "How much can we Forget" paper (which had theory and controlled experiments) or the 6.25 "Min-K% Prob" paper (which had a clean methodology).

The data volume confound doesn't completely invalidate the TS-Guessing probe findings, but it fundamentally undermines the accuracy-based claims. I'll place this at **4.0**.

---

## Summary

This paper investigates whether translating LLM benchmarks into Arabic can mask data contamination signals. The authors fine-tune four open-weight LLMs on English benchmark data plus varying proportions (0%, 10%, 50%, 100%) of Arabic-translated benchmark data, evaluate on original English benchmarks (MMLU, XQuAD, MLQA), and extend TS-Guessing memorization probes with a choice-reordering strategy (Index-recall Rate, IDR). They propose a conceptual Translation-Aware Contamination Detection (TACD) framework.

## Strengths

- **Novel multilingual contamination angle:** The paper addresses a genuine gap — virtually all prior contamination detection work focuses exclusively on English. Table 2 shows MMLU accuracy increases monotonically with Arabic contamination level across all four models (e.g., Mistral: 0.577→0.690; LLaMA: 0.332→0.431), demonstrating that contamination through translation persists and benefits English benchmark performance.

- **Methodological extension of TS-Guessing via choice reordering (IDR):** The paper extends TS-Guessing (Deng et al., 2024) by shuffling MCQ answer choices and measuring Index-recall Rate. Table 3a shows meaningful IDR values for LLaMA (0.287 at 10%, 0.643 at 50%, 0.410 at 100%), providing a contamination signal that accuracy alone would not reveal.

- **Task-divergent contamination effects (MCQ vs. extractive QA):** The paper documents a systematic divergence — MMLU shows monotonic gains across all models (Table 2), while MLQA shows a frequent "peak-at-10% then decline" pattern (e.g., Qwen MLQA: 0.162→0.409→0.157→0.153). This characterizes how contamination operates through different mechanisms for surface-option memorization versus semantic alignment — a distinction not previously characterized.

- **Cross-architecture experimental breadth:** Four models from different families (Llama-3.2-1B, Mistral-7B, Gemma-3-1B, Qwen3-1.7B) spanning different sizes, providing evidence the phenomenon is not model-specific.

## Weaknesses

### Fatal

None.

### Major

- **No control for data volume vs. contamination confound.** The training setup (Section 3.1, line 130): `D_train^d(p) = D_EN^d ∪ D_AR^d(p)`. All conditions share the same English data; Arabic data is progressively added at p ∈ {0%, 10%, 50%, 100%}, so total training volume increases monotonically with p. Without a control condition using non-benchmark Arabic data of equivalent volume, the MMLU improvements (e.g., Mistral 0.577→0.690) could be attributed to seeing more QA-formatted training data rather than contaminated data specifically. This confound affects the central accuracy-based claims in Section 4.1. The TS-Guessing probes partially address this (flat memorization signals are independent of data volume), but the performance-based claims about "models benefiting from contaminated data" are undermined.

- **Internal inconsistency between Section 4.2 and Table 2.** Section 4.2 (line 201) claims "models exhibit approximately equal performance on all evaluated benchmarks" and describes a "near-flat trend," but Table 2 (lines 177–180) shows clear monotonic MMLU improvement across all models (e.g., Mistral: 0.577→0.690, ~20% relative increase). Section 4.1 (line 189) itself describes this as a "monotonic increase." This contradiction undermines the analytical framework — the "masking" interpretation partly relies on the claim that performance differences are small, which is not true for MMLU.

- **Abstract overclaims about Arabic capabilities.** The abstract (line 9) states models "still benefit from exposure to contaminated data, particularly those with stronger Arabic capabilities." But Table 2 contradicts this: Qwen (which has strong Arabic capabilities) shows the smallest MMLU improvement (0.553→0.581, ~5% relative), while Mistral (weaker Arabic) shows the largest (0.577→0.690, ~20% relative). The claim about Arabic capabilities is unsupported by the data.

### Minor

- **No statistical rigor.** All results are single-point estimates with no variance, standard deviations, confidence intervals, or multiple random seeds. Given that LoRA fine-tuning is sensitive to initialization and some differences are small (e.g., Qwen MMLU: 0.553→0.581, a 0.028 absolute difference), reported differences may be within run-to-run variance.

- **Missing MLQA TS-Guessing results.** Section 3.3 (line 158) states TS-Guessing is applied "for d ∈ {MMLU, XQuAD, MLQA}" but Table 3 only reports MMLU and XQuAD results. MLQA TS-Guessing results are absent without explanation.

- **Underdeveloped embedding analysis.** Section 4.3 (line 224) references "The embedding figure shows that Arabic→English translations remain close to their English originals" with a cosine similarity formula, but this is mentioned in passing as a brief remark rather than presented as systematic quantitative analysis.

- **No unfine-tuned baseline.** While the 0% condition serves as an English-only fine-tuning reference, reporting the pre-fine-tuning model performance would help establish the starting point and assess improvement magnitude relative to baseline capabilities.

## Nice-to-Haves
- Dataset statistics (number of examples per condition, token counts) should be at least summarized in the main text, given their importance to experimental design interpretation.
- The TACD framework (Section 5) adds limited substance — its components (cross-translation benchmarking, TS-Guessing across variants, back-translation consistency) are straightforward extensions with no empirical validation. The authors acknowledge this, but the section could be compressed.
- Adding a non-benchmark Arabic data control would transform the central claim from speculative to testable.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Criticisms about missing appendix content (parser strips appendix; the paper does reference Appendix B for dataset statistics).
- Style/formatting nitpicks.
- The claim that XQuAD EM scores are "uniformly <0.02" — this is factually wrong; Mistral's EM is 0.103, 0.093, 0.074 in Table 3b, which are substantially above 0.02.
- Strength Finder claim about "TS-Guessing for extractive QA confirming masking" — this conflates low EM scores with masking; the paper's framing is more nuanced.
- Strength Finder claim about "honest framing of TACD" — acknowledging limitations is a basic expectation, not a notable strength.

## Novel Insights

The paper's most genuinely novel observation is the task-divergent contamination response: MCQ tasks (MMLU) show monotonic improvement with contamination while extractive QA tasks (XQuAD, MLQA) show non-monotonic, model-specific patterns including "peak-at-10% then decline" behavior. This suggests contamination operates through fundamentally different mechanisms for surface-option memorization versus semantic alignment — a distinction not previously characterized in the contamination literature and potentially important for understanding how memorization effects propagate across task types.

## Suggestions

1. **Add a control condition with non-benchmark Arabic data** (e.g., Arabic Wikipedia QA or unrelated Arabic MCQ data) at equivalent volumes to each contamination level. This single addition would isolate contamination from data-volume effects and would significantly strengthen the central claim.
2. **Report multiple seeds with variance** (even 3 seeds per condition) to establish whether observed differences, especially the small Qwen MMLU changes, are statistically meaningful.
3. **Reconcile Section 4.2 with Table 2** — either qualify the "approximately equal" claim or restructure the analysis to acknowledge that MMLU shows clear trends while TS-Guessing shows flat signals (which is actually the more interesting finding).
4. **Report MLQA TS-Guessing results** as promised in Section 3.3, or explicitly state why they were omitted.
5. **Correct the abstract's claim about Arabic capabilities** — the data shows the opposite pattern from what is claimed.

## Score and Decision

**Calibration anchors (all retrieved in Round 1):**

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| "Evading Data Contamination Detection" | 4.25 | R1 | Very similar topic (contamination evasion); similar methodological weaknesses but our paper has broader experiments |
| "Benchmark Inflation" | 4.25 | R1 | Contamination detection methodology; our paper has more models/datasets but a more fundamental confound |
| "Elephants Never Forget" | 4.75 | R1 | Memorization/contamination testing; our paper has more focused research question and experiments |
| "How much can we Forget?" | 6.75 | R1 | Much more rigorous with theory and controlled experiments; our paper is notably weaker |
| "Detecting Pretraining Data" | 6.25 | R1 | Clean methodology, foundational contribution; our paper has more significant issues |
| "To the Cutoff... and Beyond?" | 6.75 | R1 | Novel longitudinal methodology; our paper has less clean execution |
| "LiveBench" | 7.33 | R1 | Contamination-free benchmark; not directly comparable but shows what a strong contamination paper looks like |
| "Linguini" | 4.75 | R1 | Benchmark paper with limited scope; our paper has similar mixed-reception pattern |
| "Systematic Review of LLMs" | 1.00 | R1 | Very weak survey; incomparable to our paper |
| "NEMESIS Jailbreaking" | 1.40 | R1 | Weak jailbreaking paper; incomparable |
| "DataSciBench" | 3.20 | R1 | Benchmark paper with methodological issues; our paper is stronger |

**Round 1 bracket: 3.5–5.0**

Our paper sits above the 3.0–3.5 range (papers with limited novelty or fundamental incompleteness) and below the 5.5+ range (papers with cleaner methodology and stronger claims). It's most comparable to the 4.25 "Evading" paper — both have interesting contamination angles and concrete experiments but suffer from methodological issues that undermine core claims. Our paper has broader experiments (4 models, 3 datasets) which slightly elevates it, but the data volume confound and internal inconsistency are significant. I place it at **4.0**.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>