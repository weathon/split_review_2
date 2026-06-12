## Summary

The paper proposes LPFQA, a benchmark of ~505 questions across 20 professional domains, sourced from real technical forums, designed to evaluate LLMs on long-tail professional knowledge and complex reasoning. The pipeline involves crawling professional forums, generating QA pairs via MLLMs, expert verification, and difficulty calibration. The authors evaluate 12 state-of-the-art LLMs and conduct ablation studies on code interpreter and search tool augmentation.

## Strengths

- **Clear and well-motivated problem.** The paper articulates a genuine gap in existing benchmarks: most evaluate head knowledge or use artificial scenarios, while long-tail professional expertise remains under-tested. The positioning against MMLU, Chatbot Arena, Arena-Hard, and HLE is well argued and identifies a real niche.

- **Authentic sourcing from real forums.** Unlike benchmarks constructed from textbooks or crowd-sourced annotations, LPFQA derives questions from genuine professional discussions. This is a principled design choice that increases ecological validity for evaluating models in real-world professional contexts.

- **Comprehensive evaluation on modern models.** The paper evaluates 12 current frontier models (including GPT-5, o3-high, Gemini-2.5-Pro, DeepSeek-R1, Claude-4), providing timely and relevant results. The ablation studies on code interpreter and search tools (Tables 3–4) offer genuinely useful observations — that tool augmentation can *hurt* performance on long-tail knowledge tasks, which is a valuable empirical finding for the community.

## Weaknesses

### Fatal
None.

### Major

- **Severely insufficient scale and per-domain coverage.** The benchmark contains only ~505 questions across 20 domains, yielding an average of ~25 items per domain. Several domains have critically few items: Data Science (3), Aerospace (8), AI (8), ICE (7), EIS (10). With so few items per domain, the per-field analysis shown in Figures 3–4 has extremely high variance and the domain-level conclusions are statistically unreliable. A benchmark designed to evaluate cross-disciplinary capabilities needs substantially more items per domain to support its claims.

- **Evaluation methodology for short-answer questions is underspecified.** The paper mentions that short-answer items have "key knowledge points" as scoring criteria, but the actual scoring mechanism (how partial credit is awarded, how semantic matching is performed, whether LLM-as-judge is used, what prompts are used) is not described in the main text. For a benchmark whose value depends on reliable scoring, this is a significant omission. The reliability and inter-annotator agreement of the scoring process are not reported.

- **Figure 2 and Figure 5 present garbled data.** The CS field shows a count of "2121" in Figure 5's table, which is clearly a parsing or reporting error given the total dataset size is 505. Similarly, the bar heights in Figure 2 are inconsistent with the stated numbers (e.g., Math=61, Bio=61, Phys=68 would each represent ~12% of the dataset). These data integrity issues undermine confidence in the reported statistics.

### Minor

- **Inconsistency in total count.** The abstract states "502 tasks" while Section 3.3 and the caption state "505 questions." This minor discrepancy appears throughout the paper and should be corrected.

- **Filtered benchmark methodology is questionable.** LPFQA⁻ (removing items all models got wrong) and LPFQA⁼ (removing items all models got right) improve discrimination by construction, but this post-hoc filtering based on model performance raises concerns about benchmark validity. A benchmark should not be trimmed to maximize score separation on a specific set of models, as this risks overfitting the benchmark to current models.

- **Radar chart field coverage mismatch.** Figure 3 and 4 show only 12 fields in the radar charts, while the paper claims 20 fields. It is unclear why 8 fields are excluded from the visualization, and whether conclusions extend to the omitted domains.

- **Table 1 scores are low and lack context.** The best model (GPT-5) achieves only 47.28/100. Without understanding whether this is driven by impossible questions, ambiguous items, or genuinely hard content, the reader cannot calibrate what these scores mean. The observation that the range is "relatively narrow" (32–47) is noted but not deeply analyzed.

### Trivial
None.

## Nice-to-Haves

- A correlation analysis between benchmark difficulty and question characteristics (e.g., length, domain specificity, reasoning depth) would strengthen understanding of what LPFQA measures.
- Comparison with existing benchmarks on the same models to demonstrate complementary discriminative power.
- Analysis of failure modes — what types of errors do models make on LPFQA (knowledge gaps vs. reasoning failures vs. misinterpretation)?

## Novel Insights

The ablation finding that search tool integration *hurts* performance on long-tail knowledge tasks is genuinely insightful and practically important. It suggests that for specialized professional domains, retrieval-augmented approaches may introduce misleading information rather than helpful context — an observation that challenges the common assumption that "more tools = better performance." This finding, if validated at larger scale, would have meaningful implications for agentic LLM system design.

## Suggestions

1. **Scale up substantially.** The benchmark needs at least 50+ items per domain (ideally 100+) to support per-domain analysis. With current counts, the domain-level radar charts should be removed or caveated heavily.
2. **Fully describe the evaluation methodology.** Include the exact scoring prompts, LLM-as-judge setup (if used), and human agreement statistics in the main text.
3. **Fix the data inconsistencies** in Figures 2 and 5, and standardize the total item count throughout the paper.
4. **Report reliability metrics** — test-retest consistency across the 3 trials, scoring agreement rates, and item-level difficulty calibration statistics.

## Score and Decision

The paper addresses a legitimate and underexplored problem (long-tail professional knowledge evaluation) and offers some useful insights from ablation studies. However, the benchmark's scale (~25 items per domain on average, with several domains having only 3–8 items) is too small to support the cross-disciplinary claims being made. The evaluation methodology for short-answer questions is insufficiently described, and there are data integrity issues in the reported statistics. These limitations collectively mean the benchmark, in its current form, does not deliver the robust and discriminative evaluation tool the paper promises.

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>