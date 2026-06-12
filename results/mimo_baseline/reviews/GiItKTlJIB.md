## Summary

This paper introduces a systematic deletion framework to probe how much LLMs actually depend on their chain-of-thought (CoT) traces for physics problem solving. By intercepting CoT mid-generation and deleting varying fractions of tokens, the authors test three open-source models (Phi-4, Qwen-A3B, Magistral) across three physics benchmarks, finding that models remain accurate under moderate deletions (40–60%) by "cramming" reconstructed reasoning into final answers, suggesting shallow rather than faithful reliance on CoT.

## Strengths

- **Important research question**: Whether LLMs genuinely depend on their CoT traces is a fundamental question for AI-for-science, and physics provides a natural structured testbed where reasoning faithfulness should matter most.
- **Systematic experimental design**: The paper evaluates three deletion strategies (end, random, physics-aware) across three models and three datasets, providing a reasonably comprehensive sweep. The consistent "X-shaped" pattern of decreasing CoT length paired with increasing answer length is a compelling empirical observation.
- **Clear presentation**: The paper is well-organized with informative figures, and the three-stage experimental pipeline (baseline → deletion sweeps → overlap analysis) is logical and easy to follow.

## Weaknesses

### Fatal
None.

### Major

- **Crude overlap metrics for faithfulness claims**: The paper's central faithfulness analysis relies on Jaccard similarity and Manhattan distance over bag-of-words representations. These metrics capture lexical overlap but not semantic or mathematical equivalence. A model could produce a correct but differently-expressed equation or derivation that scores near zero on these metrics, or could reproduce surface tokens without genuine reasoning. The paper acknowledges "surface-level similarity" but does not provide or validate any more meaningful faithfulness metric, yet draws strong conclusions about CoT faithfulness from these measurements.

- **Lack of statistical rigor**: The paper reports accuracy trends and "slight upticks" in scores (e.g., panels b), c), f) of Figure 6) without any statistical significance testing. Confidence intervals or error bars are mentioned only for the calibration study. Key claims—such as the 40% deletion threshold where accuracy begins to drop—are not supported by formal hypothesis tests. Without this, it is difficult to distinguish genuine effects from noise, especially given stochastic sampling (T=0.6–0.7).

- **Using Claude-4 Sonnet as judge is suboptimal for structured physics**: Physics problems with expected numerical answers or equations can be evaluated programmatically (exact match, symbolic equivalence via CAS). Using an LLM judge introduces unnecessary opacity and potential bias, especially since the paper claims to be critiquing evaluation methodology. This choice is never justified.

- **The "cramming" mechanism remains opaque**: The paper observes longer final answers under deletion but does not analyze *what* is being crammed. Are the reconstructed equations correct? Do they match the original CoT semantically, or are they hallucinated boilerplate? Is the increased length actually useful reasoning or just verbosity? Without this analysis, the central finding (models "reconstruct missing reasoning") is speculative. Alternative explanations—such as increased uncertainty leading to more hedging text—are not ruled out.

### Minor

- **Novelty relative to prior work is modest**: Lanham et al. (2023), which is cited, already performed CoT faithfulness experiments via truncation and paraphrasing. The specific variant of deleting k% of tokens is a straightforward extension, and the paper does not clearly articulate what new insight the deletion framework provides beyond prior interventions. The contribution is incremental.

- **Fixed sampling parameters without sensitivity analysis**: Temperature and top-p are held fixed throughout. Since the models are sampled stochastically, variance across runs could substantially affect the deletion sensitivity curves. A sensitivity analysis on sampling parameters would strengthen the claims.

- **Model size confounds**: The three models differ substantially in architecture, size, and training procedure (14B Phi-4 vs. 30.5B MoE Qwen vs. 24B Magistral), making it difficult to attribute behavioral differences to any specific factor. The paper does not control for this.

### Trivial
None.

## Nice-to-Haves

- Analyze the *content* of crammed answers—are the reconstructed equations and facts actually correct, and do they match the deleted CoT semantically (not just lexically)?
- Replace the LLM judge with programmatic evaluation for structured physics answers.
- Include statistical significance tests for the key deletion thresholds and accuracy trends.

## Novel Insights

The "cramming" observation—that models systematically produce longer final answers to compensate for deleted CoT, following a consistent X-shaped pattern across models and datasets—is a genuinely novel and interesting empirical finding. However, the paper does not go deep enough into the mechanism to fully capitalize on this observation. The insight that physics-aware deletion degrades accuracy more gradually than random deletion (70-80% vs 60% threshold) is also informative, suggesting models have partially internalized domain-specific reasoning patterns. These findings are valuable but would be substantially strengthened by mechanistic analysis.

## Suggestions

- Add semantic-level overlap analysis (e.g., using a math-aware NLI model or symbolic matching for equations) to distinguish genuine recovery from lexical echoing.
- Conduct a qualitative analysis of crammed answers—sample and manually evaluate what content is reconstructed and whether it is correct.
- Add error bars and statistical tests to all main results (not just the calibration study).
- Justify the LLM-judge choice or replace it with programmatic evaluation for equations/numerical answers.

## Score and Decision

The paper addresses an important question with a systematic experimental approach and produces interesting empirical observations (especially the cramming pattern). However, the faithfulness analysis rests on inadequate metrics, statistical testing is absent from the main results, the central "cramming" mechanism is left unanalyzed, and the novelty is modest relative to existing CoT faithfulness work. These issues collectively limit the paper's ability to support its stronger claims about CoT faithfulness in scientific domains.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>