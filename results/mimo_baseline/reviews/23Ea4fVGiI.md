## Summary

This paper proposes using the Task-Method-Knowledge (TMK) framework—a knowledge representation formalism from cognitive and educational science—as a structured prompting strategy to improve LLM performance on classical planning tasks. Evaluated on the PlanBench Blocksworld benchmark (Classic, Mystery, and Random variants), TMK prompting yields notable accuracy gains across several OpenAI models, with the most dramatic improvement being o1's jump from 31.5% to 97.3% on Random Blocksworld. The authors argue that TMK functions as a "symbolic steering mechanism" that shifts models from linguistic pattern-matching toward formal symbolic manipulation.

## Strengths

- **Novel cross-disciplinary idea.** Importing the TMK framework from cognitive/educational science into LLM prompting for planning is a genuinely interesting and underexplored direction. The explicit teleological ("why") component distinguishes TMK from existing hierarchical decomposition frameworks like HTN and BDI, and the paper articulates this distinction clearly.

- **Engagement with LLM reasoning critiques.** The paper thoughtfully addresses known criticisms of CoT and ReACT (Stechly et al., 2024; Bhambri et al., 2025) by structuring experiments to avoid pattern-matching confounds: using one-shot (not instance-matched) examples, evaluating full stepwise reasoning chains rather than just final answers, and testing on obfuscated domains (Mystery, Random) that resist semantic shortcutting. This positions the work well within the current discourse.

- **Compelling "performance inversion" observation.** The finding that o1 under TMK prompting achieves higher accuracy on Random (97.3%) than Mystery (83.3%)—reversing the typical pattern—is an intriguing empirical result that, if validated, would be genuinely informative about how structured prompts interact with reasoning model internals.

## Weaknesses

### Fatal

None.

### Major

- **Confounded comparison methodology.** The paper compares TMK one-shot results against zero-shot baseline values drawn from the PlanBench leaderboard, rather than running matched one-shot plain-text baselines under identical experimental conditions (same API, same extraction code, same time period). The authors' justification—that zero-shot often outperforms one-shot for plain text—is empirically acknowledged but does not eliminate the confound. Different API versions, temperature settings, extraction pipelines (the authors modified the extraction code for Random Blocksworld), and prompt formatting could all contribute to the observed differences. A rigorous comparison requires matched baselines.

- **Extremely narrow evaluation.** All experiments are confined to a single planning domain (Blocksworld) with only OpenAI model families. The paper does not test on other PlanBench domains (e.g., Logistics), other model families (Anthropic, Google, open-weight models), or other planning benchmarks. This severely limits the generalizability of the claims. The authors acknowledge this limitation but the claims in the abstract ("bridge the gap between semantic approximation and symbolic manipulation") are stated broadly.

- **No ablation study.** TMK bundles multiple structural elements: hierarchical task decomposition, explicit pre/post-conditions, teleological goal-mechanism linking, JSON serialization, and domain ontology. Without ablations isolating which components drive the improvements, it is impossible to determine whether TMK's teleological emphasis (its claimed differentiator from HTN/BDI) is actually responsible, or whether a simpler structured representation (e.g., PDDL-like JSON, or a well-structured bullet list of preconditions and effects) would achieve similar gains.

- **No statistical significance testing.** The paper reports accuracy percentages without confidence intervals, standard deviations, or significance tests. Given that some test sets may contain a limited number of instances, and LLM outputs can be stochastic, this omission makes it difficult to assess whether observed differences are robust.

### Minor

- **Speculative mechanistic claims.** The paper's central theoretical claim—that TMK "steers" models toward "code-execution pathways" and away from "linguistic approximation"—is presented as explanatory fact rather than hypothesis. No evidence is provided for this mechanism (e.g., no analysis of intermediate reasoning traces, attention patterns, or latent representations). The "performance inversion" is consistent with this hypothesis but also consistent with simpler explanations (e.g., TMK reduces formatting ambiguity for opaque tokens).

- **Modified extraction code as a potential bias source.** The authors modified the PlanBench extraction code for Random Blocksworld to tolerate formatting artifacts (extra words, symbols). While the rationale is reasonable, this modification was applied by the same team proposing the method, and it is not clear whether the same leniency was applied uniformly to baseline results from the leaderboard.

- **TMK design is hand-crafted for Blocksworld.** The TMK model used was authored by the paper's authors specifically for this domain. This introduces an implicit knowledge-engineering advantage—the prompt contains expert-designed problem decomposition that no baseline prompt has. The paper does not discuss how TMK would be generated for novel domains without expert authoring, which affects scalability claims.

### Trivial

- The paper mentions GPT-5 results, which may be anachronistic relative to the review timeline, but this is not a methodological issue.

## Nice-to-Haves

- A comparison against other structured prompting baselines (e.g., PDDL-style prompting, structured CoT, tree-of-thought) to isolate TMK's unique contribution.
- Analysis of the LLM's actual reasoning traces (for models that expose them, like o1) to see whether TMK genuinely changes the character of the reasoning.
- Evaluation on additional PlanBench domains (Logistics, Mystery-primed variants) and non-OpenAI models.

## Novel Insights

The "performance inversion" observation—that TMK prompting can make opaque symbolic tasks (Random) easier than semantically obfuscated tasks (Mystery) for reasoning models—is a genuinely novel empirical finding that, if replicated, would provide meaningful insight into how structured prompts interact with the internal reasoning modes of large reasoning models. The cross-disciplinary connection between TMK's teleological structure and LLM planning is also a fresh framing, even if the mechanistic explanation remains speculative.

## Suggestions

1. Run matched one-shot plain-text baselines under identical conditions (same API version, same extraction code, same evaluation pipeline) to replace the leaderboard comparison.
2. Conduct an ablation study comparing TMK against (a) PDDL-as-JSON prompting, (b) structured natural-language decomposition without teleological fields, and (c) just the JSON structure without TMK semantics.
3. Report confidence intervals and perform statistical significance tests, especially given the stochastic nature of LLM outputs.
4. Expand evaluation to at least one additional planning domain and one non-OpenAI model family.
5. Analyze reasoning trace content (where available) to provide direct evidence for the "code-execution pathway" hypothesis rather than inferring it from accuracy patterns alone.

## Score and Decision

The paper presents an interesting cross-disciplinary idea with promising initial results, but the experimental methodology has significant confounds (mismatched baselines, modified extraction code, no ablations, no statistical tests), and the evaluation is too narrow (single domain, single model family) to support the strong claims made. The dramatic improvement on o1 Random Blocksworld is noteworthy but needs much more rigorous validation before the theoretical claims about symbolic steering can be accepted. As it stands, this reads as a preliminary exploration rather than a thoroughly validated contribution.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>