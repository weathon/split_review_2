## Summary

EditBench is a benchmark for evaluating LLMs on instructed code editing tasks, built from real-world user interactions collected via a VS Code extension. It comprises 540 problems across 5 natural languages and 2 programming languages, with diverse user instructions, code contexts, and contextual features (highlighted code, cursor position). The authors evaluate 40 LLMs and find that only one model exceeds 60% pass@1, revealing that the benchmark is challenging and captures unique aspects of real-world editing not covered by existing benchmarks.

## Strengths

- **Real-world grounding**: The benchmark is constructed from actual developer usage data collected via a VS Code extension, making it more realistic than existing benchmarks that rely on annotator-written or educational problems. This is a significant and timely contribution.
- **Diversity and richness**: EditBench spans 5 natural languages, 2 programming languages, 74 unique imports, and four functional edit categories (feature addition, modification, bug fixing, optimization). The variation in instruction and context lengths far exceeds prior edit benchmarks.
- **Context-dependent evaluation**: The inclusion of highlighted code and cursor position as contextual inputs is novel for code editing benchmarks. The ablation study (Table 3) shows that highlighted code improves performance for most models, validating the importance of this feature.
- **Comprehensive evaluation**: 40 models from diverse families (open and closed) are evaluated with careful experimental design (temperature 0, consistent prompts). The analysis across categories, difficulty levels, and context variants provides actionable insights.
- **Weak correlation with existing benchmarks**: The low correlation with Aider Polyglot and Chatbot Arena (coding subset) demonstrates that EditBench captures a distinct and more realistic distribution of editing tasks, justifying its value as a new benchmark.

## Weaknesses

### Fatal
None.

### Major
1. **Test harness creation is manual and potentially subjective**: The 109 core problems were curated by five annotators who wrote test cases based on their interpretation of user intent. While a second review was performed, no inter-annotator agreement metrics are reported. The filtering process (from 2672 responses to 109 problems) is aggressive and may introduce selection bias. The reliance on human judgment for test case quality is a limitation for reproducibility and scalability.
2. **Small core problem set**: The benchmark starts with only 109 unique problems (expanded to 540 via translation). This limits the statistical power of some analyses (e.g., per-category comparisons, per-language comparisons) and raises questions about how representative the set is of the full distribution of real-world edits.
3. **Translation quality is not fully validated**: Problems were translated to other natural languages using GPT-4o, with only a subset validated by native speakers. Translation artifacts could affect model performance on non-English problems, and the paper does not analyze whether performance varies by language.
4. **Limited context ablation**: The ablation study on highlighted code and cursor position (Table 3) includes only 7 models. A broader set of models would strengthen the conclusion that these contextual features matter.

### Minor
1. **Difficulty split is arbitrary**: The easy/hard split is based on a threshold of k=20 models solving a problem. While pragmatic, this choice is not justified and may not be stable across different model sets.
2. **Contamination not discussed**: Since the data is collected in the wild, some problems may have been seen by models during training. The paper does not address potential contamination or mitigation strategies (e.g., temporal holdout).
3. **Low conversion rate**: Only 109 core problems from 2672 accepted edits (4%). The paper acknowledges this but does not deeply analyze what types of edits were excluded and whether this biases the benchmark toward certain tasks.

### Trivial
None.

## Nice-to-Haves
- Report inter-annotator agreement for test case creation to quantify reliability.
- Include a larger set of models in the context ablation study.
- Provide a breakdown of model errors (e.g., formatting, logic, missing imports) to guide future improvements.
- Discuss potential data contamination and any steps taken to mitigate it (e.g., checking if problems appear in training data).

## Novel Insights

The paper’s core insight is that real-world instructed code editing is a distinct task from code generation or chat-based coding, and existing benchmarks fail to capture its challenges. The weak correlation with Aider Polyglot (r=0.24) and Chatbot Arena (r=0.11) quantitatively confirms this gap. The finding that highlighted code improves performance for most models (up to 3.5% absolute gain) while cursor position has mixed effects suggests that models are still learning to integrate multiple contextual signals. The observation that models perform best on bug fixing (52.2% average) and worst on optimization (44.6%) and feature addition (39.6%) indicates that real-world editing requires capabilities beyond those tested by prior benchmarks.

## Suggestions
- Release the raw collected data (with privacy safeguards) to enable the community to create additional test cases and validate the benchmark.
- Provide a more detailed analysis of the types of errors models make on EditBench (e.g., formatting, logic, missing imports) to guide future model development.
- Consider using a more principled method for difficulty stratification (e.g., item response theory) as the benchmark grows.

## Score and Decision

**Score**: 8

**Decision**: Accept

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>