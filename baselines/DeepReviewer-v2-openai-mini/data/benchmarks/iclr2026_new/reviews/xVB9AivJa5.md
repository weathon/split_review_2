## Summary
# Final Review Report

## Summary

Blueprint-Bench introduces a benchmark for evaluating spatial reasoning in AI models through the task of converting apartment photographs into 2D floor plans. The authors evaluate 12 models across three families (LLMs, image generation models, and agent systems) on 50 apartments with ~20 photos each, using a scoring algorithm based on room connectivity graphs and size rankings. The main finding is that most models perform at or near a random baseline, while human performance is substantially higher.

**Strengths**: The benchmark addresses an interesting and under-explored evaluation gap — whether generalist AI models can perform spatial reasoning with in-distribution visual inputs. The cross-architecture comparison (LLMs vs. image models vs. agents) is a useful design choice. The scoring algorithm is transparent and rule-based. The paper identifies a genuine empirical finding (poor spatial reasoning performance across model types) that could inform safety evaluations.

**Core Weaknesses**: (1) The human baseline is evaluated on only 12 of 50 apartments, invalidating direct comparison. (2) The scoring function weights are arbitrary and lack validation against human judgments. (3) The benchmark conflates instruction-following with spatial reasoning, as demonstrated by the lowest-scoring models failing primarily on format compliance. (4) Statistical significance claims are unsubstantiated — no test details, p-values, or confidence intervals are reported. (5) The "first direct comparisons between image models and their underlying LLMs" claim is not supported by the experimental design, which lacks paired model variants. (6) Novelty claims are unverifiable due to unavailable literature search (retrieval-disabled mode). (7) The agent experiment tests only two scaffold-model combinations, likely with single runs, limiting generalizability.

**Recommendation**: The benchmark concept has merit for the community, but the current manuscript requires substantial methodological strengthening before it can serve as a reliable evaluation framework. Priority revisions include: re-evaluating the human baseline on the full dataset, validating the scoring function, reporting statistical methodology, and addressing the instruction-following confound.

## Strengths
**S1 — Important and underexplored evaluation direction.** The paper targets spatial reasoning — a capability that is increasingly relevant as AI systems are deployed in physical-world contexts. Most existing benchmarks test either language understanding or task-specific visual recognition; Blueprint-Bench's focus on reconstructing spatial layouts from photographs fills a gap in the evaluation landscape. The idea of testing models on a task where the input is in-distribution but the output format is novel is well-motivated and yields interpretable results.

**S2 — Cross-architecture comparison design.** By designing a model-agnostic task (generate an image from a sequence of images), the benchmark enables comparisons across LLMs (via SVG generation), image generation models (via direct image output), and agent systems (via iterative refinement in a containerized environment). This three-way comparison is rare in existing benchmarks and provides richer diagnostic information than single-model-type evaluations.

**S3 — Transparent and interpretable scoring.** The scoring algorithm decomposes similarity into six interpretable components (edge overlap, degree correlation, graph density, room count, door count, door orientation) with clearly stated weights. This is preferable to a black-box similarity metric and allows future work to analyze which specific spatial reasoning sub-capabilities models lack.

**S4 — Open-source evaluation framework.** The authors commit to open-sourcing the generation code and providing a dataset sample, and they welcome community submissions to a public leaderboard. This lowers the barrier for others to use and extend the benchmark, increasing its potential impact.

**S5 — Honest limitations discussion.** Section 2.4 acknowledges several limitations: room type labeling is absent, shape similarity is not measured, and strict formatting rules may penalize spatially correct but format-noncompliant outputs. The authors also discuss their experimentation with alternative scoring approaches (LLM-based extraction, nearest-neighbor distance) and explain why they chose the current design. This transparency is commendable.

**S6 — Qualitative agent trace analysis.** The analysis of Claude Code's iterative refinement process (Figure 8) provides valuable insight into why agents fail — they attempt self-correction but cannot reliably detect their own spatial errors. This goes beyond quantitative scoring and offers a diagnostic direction for future research.

## Weaknesses
**W1 — Human baseline evaluated on a different subset invalidates direct comparison.** [severity=critical]
The human performance data (Figure 7, score 0.547) is based on only 12 of 50 apartments, while all AI models are evaluated on the full set of 50. The paper notes this discrepancy in a caption but does not adjust the comparison. Since the random baseline also differs between the two figures (0.279 for full set vs. 0.322 for the 12-apartment subset), the 12 apartments are clearly not a random subset with equivalent difficulty. Without evaluating humans on the full 50 apartments or reporting AI scores on the same 12-apartment subset, the central claim that "human performance remains substantially superior" is not rigorously supported. This is the paper's headline result and it rests on an invalid comparison.
- *Required action* (Must): Either evaluate human participants on all 50 apartments, or report AI model scores on the same 12-apartment subset alongside human scores. Report the subset selection criteria and demonstrate representativeness.

**W2 — Scoring function weights are arbitrary and unvalidated.** [severity=major]
The composite score uses a weighted average (50% edge overlap, 20% degree correlation, 10% density, 10% room count, 5% door count, 5% door orientation) with no justification for the specific allocation. The 50% weight on edge overlap means that connectivity errors dominate the score, while room shape is not considered at all. More critically, the paper does not report whether this weighted combination correlates with human judgments of floor plan similarity — the most basic validity check for any similarity metric. Different weight choices could produce different model rankings, and without sensitivity analysis, the scores lack scientific foundation.
- *Required action* (Must): (a) Conduct a weight sensitivity analysis showing rank stability across reasonable variations. (b) Validate the composite score against human similarity ratings. (c) Report all six sub-scores separately alongside the composite.

**W3 — Core confound: instruction-following vs. spatial reasoning are not separated.** [severity=major]
The nine formatting rules are strict and complex. Models that produce spatially correct but format-noncompliant outputs receive low scores, while models with better instruction-following but mediocre spatial reasoning may score higher. The paper acknowledges this trade-off in Section 2.4 but does not resolve it. Empirical evidence shows that the two lowest-scoring models (GPT-4o, NanoBanana) failed primarily due to poor instruction following, not spatial reasoning deficits. This means the benchmark cannot cleanly attribute low scores to spatial reasoning failures. The bias is systematic: LLMs generating SVG code have structured output by construction, while image generation models must infer the 9-rule format from a text prompt, facing a harder instruction-following problem.
- *Required action* (Must): (a) Discuss this confound explicitly and bound claims accordingly. (b) Consider reporting spatial accuracy conditional on format compliance. (c) Explore alternative output formats that equalize the instruction-following burden across model types.

**W4 — Statistical significance claims are unsubstantiated.** [severity=major]
The paper states that "some models statistically perform better than the random baseline" without reporting any statistical test details. Missing information includes: the specific test used (t-test? Wilcoxon? permutation?), the significance threshold, whether multiple-testing correction was applied across 12 models, whether the 50 apartments are treated as independent samples, and the effective sample size given multiple epochs. Similarly, the claim that agent results are "not statistically better than the random baseline" is unsupported. Error bars in Figure 5 show standard deviation, but the caption does not specify whether this is across apartments, epochs, or both.
- *Required action* (Must): Report exact p-values or 95% confidence intervals for each model vs. random baseline comparison. Specify the test, sample size, multiple-testing correction, and effect sizes.

**W5 — Claimed comparison between image models and their underlying LLMs is not implemented.** [severity=major]
The paper states that Blueprint-Bench "can be used to compare how the intelligence of an image generation model compares to the LLM it is based on" and claims this as a contribution. However, the experimental design does not include paired model variants (e.g., GPT-5 Image vs. GPT-5 text-only). The comparison between GPT-5 and GPT Image is between different model generations, not between an image model and its base LLM. To substantiate this claim, the authors need to test image generation models alongside their exact text-only backbones, which is not done for any of the evaluated models.
- *Required action* (Must): Either remove this claim or provide the paired comparisons. If the necessary model variants are not publicly available, explicitly state this limitation.

**W6 — Novelty claims are unverifiable (retrieval-disabled mode).** [severity=major]
The abstract claims "first numerical framework for comparing spatial intelligence across different model architectures" and the introduction claims "first benchmark to make such comparisons [between image generation models and their base LLMs]." Due to retrieval-disabled mode in this review, these novelty claims could not be verified against the existing literature. The paper's own references include LayoutGPT (Feng et al., 2023) and PosterLLaVA (Yang et al., 2024), which evaluate floor plan generation — raising the possibility that related benchmarks exist. These claims should be bounded with explicit qualifiers.
- *Required action* (Must): Add qualifiers such as "to our knowledge" and explicitly discuss how Blueprint-Bench differs from existing floor plan evaluation benchmarks. External literature verification is needed before publication.

**W7 — Agent experiment design limits generalizability.** [severity=major]
Only two agent scaffolds (Codex CLI, Claude Code) are tested, each paired with a single underlying model. This confounds scaffold effects with model effects. The observation that the Codex-based agent did not use iterative refinement is a behavioral finding about one specific agent-model pair, not a general conclusion about agent approaches. The paper likely uses single runs per condition, making it impossible to distinguish systematic effects from stochastic variation. The conclusion that "agent-based approaches with iterative refinement capabilities show no meaningful improvement over single-pass generation" overstates the evidence.
- *Required action* (Must): (a) Test multiple underlying models per scaffold and multiple scaffolds per model to disentangle confounds. (b) Report multiple runs with variance. (c) Qualify conclusions to reflect the limited N.

**W8 — Dataset curation details are insufficient.** [severity=major]
The 50 apartments are sourced from "apartment listing's official floor plan images," but the paper does not specify: the data source (platform, region), apartment selection criteria, diversity characteristics (size range, architectural style), or the ground truth adaptation process (who performed the conversion, inter-annotator agreement, verification against actual layouts). Without this information, readers cannot assess dataset representativeness or potential biases. The private nature of the majority of the data (stated in the reproducibility section) further limits independent verification.
- *Required action* (Must): Document the data source, selection criteria, diversity statistics, and ground truth adaptation protocol. Release a public development set alongside the private evaluation set.

**W9 — Conclusion restates without synthesizing.** [severity=minor]
The conclusion largely repeats the abstract's findings rather than synthesizing deeper insights. The qualitative agent trace analysis (Figure 8) offers potentially rich diagnostic information about why models fail, but this is not incorporated into the conclusion. The final sentence making claims about "a fundamental aspect of intelligence" is too broad for a benchmark that tests one specific task.
- *Required action* (Nice-to-have): Integrate insights from the agent traces. Bound the scope of claims to the specific task evaluated.

**W10 — Writing and presentation issues.** [severity=minor]
The paper has several writing quality issues: (a) a sentence fragment occurs across a page break ("it is possible for them to do it by, for example, generating SVG code" with a comma before "by" that creates awkward syntax); (b) informal language such as "ARC is brilliant" reduces scholarly tone; (c) the evaluation section uses numbered line markers (216-269) that appear to be artifacts; (d) figure captions are triplicated in the text (likely a PDF extraction artifact). While some of these are extraction artifacts, the informal register should be revised for a conference submission.
- *Required action* (Nice-to-have): Revise informal language. Fix comma splices and sentence flow. Ensure figure captions appear once.

## Score
**Final Score: 5/10**

**Scoring rationale**: The score prioritizes research value and validity as primary dimensions, consistent with the review policy.

- **Research Value (5/10)**: The benchmark concept addresses an important evaluation gap — spatial reasoning with in-distribution visual inputs — and the cross-architecture design is innovative. However, the current implementation has significant methodological weaknesses that prevent the results from being scientifically reliable. The benchmark framework, once validated, has potential to become a useful community resource.

- **Validity/Soundness (4/10)**: The paper's headline finding (humans outperform AI, and most models are at random baseline) is undermined by the invalid human baseline comparison (12 vs. 50 apartments), unsubstantiated statistical claims, and unvalidated scoring weights. The confound between instruction-following and spatial reasoning means the benchmark may not measure what it claims to measure. These issues require major revision before the findings can be trusted.

- **Novelty (unclear, deferred)**: Due to retrieval-disabled mode in this review, novelty claims could not be verified against the external literature. The paper claims "first numerical framework" and "first benchmark to make such comparisons," but these could not be confirmed. Manual literature verification is required before publication.

- **Reproducibility (5/10)**: The generation code and a dataset sample are open-sourced, which is positive. However, the majority of the dataset is private, the scoring code availability is not clearly stated, and critical experimental details (statistical methodology, agent run configurations, dataset selection criteria) are missing.

- **Presentation (6/10)**: The paper is generally well-structured and readable. The limitations section is commendably honest. However, informal language ("ARC is brilliant"), sentence fragments, and some unclear transitions reduce the scholarly quality.

**Post-Revision Target**: [6, 7]/10 — achievable if the authors: (a) fix the human baseline comparison, (b) validate the scoring function, (c) report statistical methodology, (d) address the instruction-following confound, and (e) substantiate or qualify novelty claims.