## Summary

EditBench introduces a benchmark for evaluating LLM capabilities on instructed code editing tasks, built from real-world user interactions collected via a VS Code extension. The benchmark comprises 540 problems spanning 5 natural languages and 2 programming languages, with diverse edit categories (feature addition, modification, bug fixing, optimization) and context-dependent inputs including highlighted code and cursor position. Evaluations across 40 LLMs show the benchmark is challenging (only one model exceeds 60% pass@1) and reveals that model performance varies significantly based on problem category and contextual information provided.

## Strengths

- **Real-world data collection methodology**: The paper develops a VS Code extension to collect genuine user instructions and code contexts from nearly 500 developers, avoiding the artificial, annotator-written problems that dominate existing benchmarks. This is a significant methodological contribution that grounds evaluation in actual developer workflows.

- **Comprehensive evaluation across diverse models**: Evaluating 40 models spanning multiple families (GPT, Claude, Gemini, DeepSeek, Qwen, Llama, Mistral, etc.) provides a thorough picture of current capabilities and reveals meaningful performance differences between open and closed models, as well as across problem categories.

- **Context-dependent problem design**: The inclusion of highlighted code and cursor position as additional inputs, and the ablation study showing these affect performance by up to 8%, is a novel contribution that captures the multi-modal nature of real code editing interactions.

- **Weak correlation with existing benchmarks**: The finding that EditBench has only weak correlation with Aider Polyglot (r=0.24) and Chatbot Arena coding (r=0.11) demonstrates that the benchmark captures a distinct and previously unmeasured dimension of code editing capability.

## Weaknesses

### Fatal
None.

### Major

- **Limited programming language coverage**: The benchmark only includes Python and Javascript, despite the authors noting that their collected data also contained PHP (18%) and HTML (7%). This significantly limits the benchmark's claim of representing "real-world" code editing, as many real-world developers work in other languages. The exclusion of TypeScript is particularly notable given it was grouped with Javascript in their data.

- **Test harness quality concerns**: The test harnesses were created by human annotators who "were instructed to create test harnesses that adhere to the user's intent" - but user intent in real-world edits is inherently ambiguous. The paper acknowledges that "the user instruction and code file... can often be too ambiguous" and that annotators were asked to remove such problems. This filtering process may systematically remove the most interesting and challenging real-world scenarios, potentially biasing the benchmark toward problems that are more easily specifiable.

- **Translation methodology**: The paper creates EditBench-complete by translating all 109 core problems into 5 languages using GPT-4o, then validates with "native speakers" on "a subset." This is a weak validation approach - machine translation of code comments and instructions may introduce subtle errors or unnatural phrasing that could affect model performance differently across languages, yet the paper provides no analysis of whether performance varies by natural language.

- **Unclear problem difficulty calibration**: The "easy" vs "hard" split is defined post-hoc based on how many models solve each problem (k=20). This is circular - it tells us that some problems are harder than others but provides no insight into what makes them hard. The observation that "hard" problems have shorter instructions but longer highlighted code is interesting but under-analyzed.

### Minor

- **Limited analysis of why models fail**: The paper reports aggregate pass@1 scores and category-level breakdowns, but provides little qualitative analysis of failure modes. For example, the observation that "gpt-5... struggles with simple tasks like formatting code indentation properly" is mentioned in passing but not systematically investigated.

- **No analysis of instruction language effects**: Despite including 5 natural languages, the paper never analyzes whether model performance varies by the language of the instruction. This is a missed opportunity given the claim of multilingual evaluation.

- **Cursor position ablation results are inconclusive**: The ablation study shows that adding cursor position helps some models and hurts others, with no clear pattern. The paper acknowledges this but does not explore why, leaving an important design question unanswered.

### Trivial
None.

## Nice-to-Haves

- Analysis of performance by natural language to validate the multilingual claims
- Qualitative examples of failure modes across different model families
- Investigation of whether the test harness creation process could be automated more reliably
- Analysis of how EditBench scores correlate with developer satisfaction (e.g., user acceptance rates from the extension)

## Novel Insights

The paper's most novel insight is that real-world code editing instructions are fundamentally different from existing benchmark problems - they are shorter, more ambiguous, and require integrating multiple contextual signals (highlighted code, cursor position, file context) to resolve. The weak correlation with existing benchmarks suggests that the code editing capability measured by current benchmarks may not transfer to real-world usage. The finding that different models excel at different edit categories (e.g., some are better at bug fixing while others excel at feature modification) suggests that "code editing ability" is not a monolithic capability but rather a collection of related skills that models develop unevenly.

## Suggestions

- Expand programming language coverage to include at least TypeScript and one additional language (e.g., Java or Go) to strengthen claims about real-world representativeness
- Provide per-language performance analysis to validate the multilingual claims and identify potential translation artifacts
- Include a qualitative analysis section examining specific failure cases to help the community understand what makes EditBench problems challenging
- Consider releasing the raw collected data (anonymized) alongside the benchmark to enable further research on the gap between real-world and synthetic edit problems

## Score and Decision

The paper makes a genuine contribution by creating a benchmark grounded in real-world data, which is a recognized gap in the code editing evaluation landscape. The methodology is sound, the evaluation is thorough, and the findings are informative. However, the limited programming language coverage and the potential biases introduced by the test harness creation process prevent this from being a definitive benchmark. The paper is a solid contribution that will be useful to the community, but it does not achieve the level of comprehensiveness or insight that would warrant the highest scores.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>