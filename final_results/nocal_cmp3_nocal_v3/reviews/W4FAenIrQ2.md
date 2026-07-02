## Summary

This paper presents RedSage, an open-source 8B cybersecurity LLM built through a three-stage pipeline: (1) large-scale continual pretraining on 11.7B tokens of cybersecurity-filtered web data (CyberFineWeb) plus curated seed documents (RedSage-Seed), (2) agentic augmentation of seed documents into 266K multi-turn conversation samples for SFT, and (3) DPO alignment. The authors also introduce RedSage-Bench, a 30K-item benchmark spanning cybersecurity knowledge, skills, and tools. RedSage shows improvements over Qwen3-8B and other baselines on established external benchmarks (CTI-Bench, CyberMetric, SECURE) and competitive results on general LLM benchmarks. Data, model, and code are to be released.

## Strengths

1. **Comprehensive three-stage pipeline that genuinely goes beyond prior work.** Tables 1 and 2 convincingly show that no prior cybersecurity LLM effort combines large-scale continual pretraining, agentic-augmented SFT, and preference alignment with full data/model release. The gap is real and the pipeline is the paper's strongest contribution.

2. **Agentic augmentation pipeline (Section 3.2) is the most novel methodological component.** The Planner + Augmenter framework that transforms static seed documents into multi-turn, role-based conversations is more sophisticated than simple Q&A generation. Table 3 shows meaningful expansion (9.2× sample count, 2.3× token count) while preserving technical depth.

3. **RedSage-Bench fills a genuine gap in benchmark coverage (Table 1).** Including tool proficiency and quality scoring for open-ended responses addresses a blind spot in prior benchmarks (which focus almost entirely on MCQ knowledge). The taxonomy in Figure 2 is well-structured.

4. **Results on independent external benchmarks are credible and meaningful.** RedSage shows consistent improvements over Qwen3-8B on CTI-Bench, CyberMetric, SECURE, MMLU-CSec, and SecBench (Table 5, +3.75 base, +5.59 instruct). These benchmarks are not derived from the same seed data, providing independent evidence of cybersecurity capability gains.

5. **Open release of data, model, and code** (project page and all artifacts) is a tangible contribution to the community that exceeds what most prior work provides.

## Weaknesses

### Fatal
None.

### Major

1. **Shared source between training data and RedSage-Bench undermines headline benchmark results.** Both the training data and the evaluation benchmark are derived from the same 28,637 seed documents (RedSage-Seed). Pre-training (Section 3.1) trains on these documents; SFT data (Section 3.2) is generated from them; and the benchmark MCQs and open-ended Q&A (Section 3.3) are generated from these same documents. The decontamination step (Section 3.3) only removes SFT instances with query similarity >0.9 to benchmark questions — it does **not** address the fact that the model was *pre-trained* on the seed documents whose factual content the benchmark tests. A model can score highly by having memorized facts from pre-training, even if the exact MCQ wording is novel. This means the RedSage-Bench results (Table 4, +2.98 to +3.88 vs Qwen3-8B) cannot be cleanly interpreted as independent evidence of cybersecurity competence. The external benchmarks (CTI-Bench, CyberMetric, etc.) remain valid, but the paper's strongest advertised numbers depend on this benchmark.

2. **Numerical inconsistency in open-ended QA results (Section 4.1).** The text at line 256 states: "RedSage-8B-DPO achieves the best performance (Fig. 6), surpassing the second-best model (Qwen3-8B) by +7% absolute mean correctness and +0.07 in mean quality score." However, the figure caption (line 290) reports mean quality scores as RedSage-8B-DPO=7.07, Qwen3-8B=7.50 — the difference is **−0.43**, not +0.07. For correctness, the figure shows 0.73 vs 0.40 (+33%, not +7%). Additionally, the text gives RedSage-8B-Ins quality as 6.43 while the figure reports 7.43. The text claim and the underlying data directly contradict each other on both metrics. This must be resolved before any open-ended QA claims can be taken at face value.

### Minor

3. **General benchmark comparison is against a degraded instruct baseline (Table 6).** Qwen3-8B (instruct) shows substantial degradation vs Qwen3-8B-Base across multiple tasks (MMLU: 78.73→73.59; ARC-C: 68.09→62.54; HellaSwag: 79.62→56.70). The paper's framing ("surpassing... by +5.05 points on Open LLM Leaderboard tasks," abstract) implies a net improvement, but RedSage's real achievement is *avoiding* post-tuning degradation while adding cybersecurity expertise — a finding that is strong in its own right. The data is fully transparent in Table 6 (both base and instruct results shown), but the framing could be clearer.

4. **No ablation studies for key design choices.** The 30% FineWeb-Edu replay ratio (Section 3.1), the effect of agentic augmentation vs. naive Q&A generation from seed documents, and the contribution of the Planner Agent vs. directly prompting the Augmenter are never ablated. These are the paper's distinctive methodological choices, and their individual effect sizes are unknown. The paper compares CFW-only, Seed-only, and combined pre-training variants, but this is only one of several relevant ablations.

5. **LLM-as-Judge for open-ended evaluation lacks human calibration.** The open-ended QA evaluation uses Llama-3.3-70B and Qwen2.5-72B as judges — the same model families used to generate the benchmark data. The paper reports human verification of the benchmark items but no human evaluation of model outputs, no inter-rater agreement statistics, and no reported correlation between LLM-based quality scores and human judgments.

### Trivial

6. **Minor numerical inconsistency between abstract and conclusion.** Abstract reports "+5.59 points on cybersecurity benchmarks," while the conclusion states "+5.9 points on cybersecurity tasks." This small discrepancy should be reconciled.

## Nice-to-Haves

- Constructing a held-out portion of RedSage-Bench from documents not used anywhere in training would significantly strengthen the benchmark's independence and the credibility of headline claims.
- A small-scale human evaluation or human-LLM agreement study for the open-ended QA quality scores would strengthen the LLM-as-Judge methodology.

## Removed Points

These points were raised in the input review but are removed with justification:

- **"No variance or replication information"**: REMOVED. The paper explicitly states it uses normalized log-likelihood accuracy for MCQs and greedy decoding at temperature=0 for instruction-tuned evaluations (line 246), both of which are deterministic. Variance estimates would be zero across runs. This is not a meaningful critique for this evaluation protocol.
- **"Most works also do not release their data or pipelines" overstated**: REMOVED (factually accurate as a general claim; the paper's central contributions do not depend on this being perfectly precise).
- **"The claim about full openness being unique" overstated**: REMOVED. Several prior works in Table 2 also release data and models. This is a minor overstatement unrelated to core contributions.
- **Pure formatting and grammar nitpicks**: REMOVED per policy (parser artifacts, not author errors).
- **Criticisms about missing appendix content or references**: REMOVED per policy (appendix was stripped by parser; references exist in the original submission).
- **"30% replay ratio never ablated or justified"** as a standalone fatal point: Downgraded to Minor (#4 above). It is a reasonable design choice grounded in prior replay-based continual learning work (Ibrahim et al., 2024; Guo et al., 2025), though the lack of ablation is noted.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the shared-source methodological concern but do not generate genuinely novel observations beyond what the paper already presents.

## Suggestions

1. **Clarify the numerical inconsistency in open-ended QA.** Confirm whether the text claims or the figure numbers are correct, and fix whichever is wrong.
2. **Acknowledge and discuss the shared-seed-data issue explicitly** in the Limitations section (which currently omits it). Consider constructing a held-out subset of RedSage-Bench from documents not used in pre-training or SFT.
3. **Reframe general benchmark comparisons** to emphasize the finding that RedSage avoids post-tuning degradation (vs. Qwen3-8B-Base) rather than claiming net improvement over the base model.
4. **Add ablation experiments** for at least the 30% replay ratio and the agentic augmentation vs. a simpler Q&A generation baseline to substantiate the claimed benefits of these design choices.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>