## Summary

This paper introduces AetherCode, a new benchmark for evaluating LLMs on competitive programming tasks sourced exclusively from premier competitions (IOI, ICPC, and their regional/national variants). The key contributions are: (1) systematic collection and expert-curated categorization of 456 problems from top-tier contests with rigorous difficulty annotation, and (2) a hybrid test case construction pipeline combining automated generation with expert annotation, achieving 100% TPR and 100% TNR on a curated solution set of 30,000+ submissions. The authors evaluate 17 LLMs and demonstrate that even the best models (o4-mini-high) achieve only ~35% Pass@1, revealing a substantial gap between LLMs and elite human competitors.

## Strengths

- **High-quality test case construction methodology**: The paper proposes a novel quality metric (TPR and TNR on a curated solution set) rather than merely counting test cases. The hybrid approach of automated G-V agent generation followed by expert annotation and audit is well-motivated and rigorous. Achieving 100% TPR and 100% TNR on 30,000+ collected solutions is impressive.

- **Timely and well-motivated problem**: The paper correctly identifies two significant weaknesses in existing code reasoning benchmarks—insufficient difficulty and low-quality test cases—and provides concrete evidence for each. The distinction between using official contest judging services (with compliance and rate-limit issues) versus self-contained test cases is a practical problem that the paper directly addresses.

- **Comprehensive problem sourcing and expert curation**: Sourcing exclusively from premier competitions (IOI, ICPC regional/world finals) rather than online judges is a principled choice that ensures higher difficulty and avoids contamination concerns. The multi-dimensional categorization (difficulty, algorithmic domain, competition type, temporal metadata) enables fine-grained analysis.

- **Thorough evaluation across diverse models**: The paper evaluates 17 models (11 reasoning, 6 non-reasoning) with multiple sampling attempts and provides breakdowns by difficulty, year, algorithmic category, and failure type. The analysis of exploration potential (Pass@1 vs Pass@4) and the failure diagnosis section add meaningful insight beyond raw scores.

## Weaknesses

### Fatal

None.

### Major

- **Lack of direct comparison to human performance**: The paper argues that LLMs have a "significant gap compared to top human experts" and uses "Extreme" difficulty problems (unsolved by humans) as evidence, but never reports actual human baseline scores on the benchmark. What percentage of problems do top human competitors solve? How does Pass@1 for o4-mini-high compare to median ICPC contestant performance? Without human baselines, the claim about the gap is unsupported.

- **Limited novelty of the benchmark construction approach**: The G-V agent system and expert annotation pipeline closely follow established methodology from prior work (Wang et al., 2025b). While the scale and thoroughness are improved, the core technical contribution—collecting hard problems and constructing test cases—is incremental rather than novel. The paper would benefit from a clearer articulation of what specific methodological advances beyond prior work.

- **Absence of decontamination analysis**: The paper mentions metadata collection for decontamination purposes but provides no analysis of potential data leakage. Given that many of these competition problems may appear in LLM training data (especially for models like GPT-4.1, DeepSeek-R1, Gemini-2.5-Pro trained on public internet data), this is a critical concern. Were any contamination tests performed? How confident can we be that performance reflects reasoning rather than memorization?

### Minor

- **The benchmark size is moderate (456 problems)** and heavily skewed toward 2024 (400) versus 2025 (56). For a benchmark claiming to be "latest," the 2025 representation is small. The "v1 (2401-2505)" naming suggests ongoing updates, but the current version is predominantly single-year.

- **Difficulty distribution is uneven**: 20 Extreme problems and 132 Hard problems compared to 159 Easy and 145 Medium. This limits the statistical power of conclusions about Extreme-difficulty performance.

- **The Expert Annotation section lacks inter-annotator agreement statistics**. With 67 experts, it's unclear how much variability exists in test case construction or whether the elite audit team independently verified the same quality.

- **The paper claims AetherCode is the "first benchmark to systematically collect latest problems from premier programming competitions worldwide"**, but APPS (2021) and CodeContests (2022) already included problems from these competitions, albeit not exclusively. This claim should be qualified.

### Trivial

- The category "Basic" in Figure 2 has 225 problems, but "Algorithm Basics" in Table 4 is listed with performance; the paper could clarify whether these refer to the same category.
- "Claude-4-Sonnet-nothinking" appears to contain a typo ("nothinking").
- "Ssed-1.6-Thinking-0715" in Table 3 appears to be a typo (likely "Seed").

## Nice-to-Haves

- A human baseline on the exact benchmark would dramatically strengthen the paper's central claim about the gap between LLMs and human competitors.
- Contamination analysis (e.g., checking whether models output memorized solutions on problems released before training cutoff dates).
- Random split results or cross-validation style analysis for test case quality assessment.
- Comparison of AetherCode scores with existing benchmarks (e.g., LiveCodeBench, CodeContests) using the same models to directly show AetherCode is more discriminative.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

- Add human performance baselines (e.g., Pass@1 for top IOI/ICPC contestants) to support the gap claim.
- Conduct and report decontamination checks (e.g., n-gram overlap analysis, probing models with verbatim problem statements).
- Clarify how the difficulty classification ("Easy/Medium/Hard/Extreme") translates into concrete model performance expectations—what does "Easy" mean on AetherCode versus HumanEval?
- Include a comparison table showing how the same models perform on AetherCode versus existing benchmarks to quantify the increased difficulty/discrimination.

## Score and Decision

The paper makes a solid, well-executed contribution to LLM evaluation. The test case quality methodology is rigorous, the problem curation is principled, and the evaluation is thorough. However, the technical novelty is incremental (building on prior G-V agent work), the benchmark size is moderate, and the critical missing piece—human baselines—weakens the paper's main argument about the gap between LLMs and humans. The paper is clearly above the borderline but not at the "accept" tier of ICLR due to these limitations. I recommend a score of 6.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>