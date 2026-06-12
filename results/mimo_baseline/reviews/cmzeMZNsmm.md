## Summary
This paper presents the first systematic study of whether Large Reasoning Models (LRMs) like DeepSeek-R1 and OpenAI o1 still benefit from prompt optimization and whether they serve as better prompt optimizers compared to general-purpose LLMs (GPT-4o, GPT-4.5). Using an MCTS-based prompt optimization framework on event extraction (ACE05), the authors find that LRMs gain substantially more from prompt optimization than LLMs and that LRMs, particularly DeepSeek-R1, serve as more effective and stable prompt optimizers. These findings generalize to symbolic reasoning (Geometric Shapes) and biomedical NER (NCBI Disease) tasks.

## Strengths
- **Timely and well-motivated research question**: The question of whether the advent of LRMs diminishes the need for prompt optimization is practically important and underexplored. The paper addresses this gap with a systematic experimental design spanning 4 models in dual roles (task model and optimizer), 2 training set sizes, and multiple MCTS depths.
- **Comprehensive cross-model evaluation**: The 4×4 matrix of task model × optimizer configurations (Table 1) provides a thorough comparison. The consistent pattern that DeepSeek-R1 as optimizer yields the best results across all task models, and that LRMs consistently gain more from optimization, provides robust evidence for the core claims.
- **Generalization experiments**: Extending beyond event extraction to Geometric Shapes and NCBI Disease NER (Table 3) strengthens the generalizability of the findings significantly, showing consistent patterns across structurally different tasks.
- **Informative qualitative and quantitative analysis**: Table 2's comparison of optimized prompts across models reveals meaningful qualitative differences—LRMs generate actionable extraction rules and exception handling while LLMs focus on output formatting. The convergence analysis (Fig. 4), survival plots (Fig. 5a), and error categorization (Fig. 5c) add useful dimensions of analysis beyond raw scores.

## Weaknesses
### Fatal
None.

### Major
- **No statistical significance testing or variance reporting**: The main results (Table 1) report single-run numbers without confidence intervals, standard deviations, or significance tests. Given that MCTS is stochastic and some differences between models are modest (e.g., o1 vs. DeepSeek-R1 as optimizers in several settings), it is difficult to assess whether these gaps are statistically meaningful. This is particularly important since the dev set has only 100 examples.
- **Quantization of DeepSeek-R1**: The paper quantizes DeepSeek-R1 to 2.5 bits due to compute constraints, which could meaningfully affect both its performance as a task model and its quality as a prompt optimizer. While the authors cite minimal degradation benchmarks, this is a confounding variable that makes it difficult to compare DeepSeek-R1 fairly against the other models accessed at full precision.
- **Single optimization framework**: Only MCTS from PromptAgent is used. The paper does not compare against other prompt optimization approaches (e.g., OPRO, evolutionary methods), so the observed advantages of LRMs could be specific to MCTS rather than general properties of prompt optimization.

### Minor
- **Downsampled event types**: Reducing from 33 to 10 event types limits the ecological validity of the event extraction results. The authors acknowledge this, but the gap between 10 and 33 types could significantly alter the difficulty profile and model behavior.
- **Batch prompting interaction**: Batch prompting is used during inference and is reported to improve performance, but its interaction with different model types and prompt optimization is not analyzed. This adds an unexamined confound.
- **Single dev/test split**: Results are reported on a single random split of 100 dev / 250 test examples. Multiple splits would provide more robust estimates.

### Trivial
- The paper notes "our preliminary exploration found that including all 33 event types... could lead to overly long prompts, which both LLMs and LRMs cannot properly handle" — the repetition of "LLMs" appears to be a minor textual issue.

## Nice-to-Haves
- Analysis of whether the optimized prompts transfer across task models (i.e., can a prompt optimized for GPT-4o by DeepSeek-R1 work well for o1?)
- An ablation on the number of event types to show how the gap between LRMs and LLMs scales with task complexity.
- Cost analysis comparing the token/API costs of using LRMs vs. LLMs as optimizers, given the large output token counts for LRMs (e.g., o1 averages ~500+ output tokens per query).

## Novel Insights
The paper provides a genuinely novel empirical finding: LRMs are not self-sufficient for complex structured prediction tasks like event extraction—they benefit *more* from prompt optimization than LLMs do, despite their stronger reasoning capabilities. This challenges the emerging narrative that LRMs may render prompt engineering obsolete. Additionally, the finding that DeepSeek-R1 achieves its best performance with the *shortest* prompts (~1750 tokens) while other models require much longer prompts is counterintuitive and practically valuable, suggesting that model-specific prompt style preferences exist and are not merely a function of prompt length.

## Suggestions
- Add error bars or run multiple MCTS seeds to establish statistical robustness of the reported numbers.
- Include at least one alternative prompt optimization method (e.g., OPRO) as a baseline to demonstrate that the LRM advantage holds across optimization frameworks, not just MCTS.
- Report results for the full 33-event-type setting, even if only for a subset of model configurations, to validate that the findings hold at realistic task complexity.

## Score and Decision
The paper addresses a timely and practically important question with a systematic experimental design across multiple models, training sizes, and tasks. The findings are consistent and informative, and the qualitative analysis of prompt differences is valuable. However, the reliance on single runs without statistical testing, the quantization confound for DeepSeek-R1, and the use of only one optimization framework limit the strength of the conclusions. The contribution is more of a well-executed empirical study than a methodological advance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept