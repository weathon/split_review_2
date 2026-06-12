## Summary

BIRD-INTERACT is a benchmark for evaluating text-to-SQL systems in dynamic, multi-turn interaction settings. It introduces a function-driven user simulator with safeguards against ground-truth leakage, two evaluation settings (protocol-guided c-Interact and agentic a-Interact), and 900 tasks spanning the full CRUD spectrum with ambiguous initial sub-tasks and state-dependent follow-ups. Empirical results show that even frontier models like GPT-5 achieve only 8.67-17.00% success rates, highlighting a critical gap between SQL generation and strategic interaction capabilities.

## Strengths

- **Well-motivated and addresses a genuine gap:** The paper correctly identifies that existing multi-turn text-to-SQL benchmarks rely on static conversation histories and narrow SELECT-only operations, failing to capture real-world ambiguities, execution errors, and database state changes. The benchmark design directly targets these limitations.

- **Methodologically sound user simulator:** The two-stage function-driven approach (semantic parsing into AMB/LOC/UNA actions followed by controlled response generation) is a principled solution to the well-known problems of ground-truth leakage and inconsistent behavior in LLM-based user simulators. The quantitative evaluation on USERSIM-GUARD (reducing UNA failure rates from up to 67.4% to 2.7%) convincingly demonstrates this improvement.

- **Rich evaluation design:** The dual settings (c-Interact and a-Interact) provide complementary views of model capabilities, and the budget-constrained mechanism adds practical relevance. The memory grafting and Interaction Test-time Scaling experiments offer meaningful diagnostic insights beyond simple leaderboard comparisons.

- **High-quality data collection:** 12 expert annotators, high inter-annotator agreement (93.33-93.50%), and principled ambiguity injection strategies (superficial, knowledge chain breaking, environmental) indicate careful benchmark construction.

## Weaknesses

### Fatal
None.

### Major

- **Unclear novelty relative to LIVESQLBENCH:** The paper builds directly on LIVESQLBENCH (BIRD-Team, 2025), using its databases, HKB structure, metadata files, and sandbox. The core contribution is converting single-turn tasks into interactive ones. However, the paper never clarifies how BIRD-INTERACT differs from simply running LIVESQLBENCH tasks with a user simulator wrapped around them. Is the ambiguity injection and follow-up annotation the only delta? If LIVESQLBENCH already contains the databases, knowledge bases, and executable environment, the marginal contribution is the interaction layer—which is valuable, but the paper should be explicit about what is inherited versus what is newly created.

- **Limited evaluation of the user simulator's limitations:** The simulator is evaluated on USERSIM-GUARD (static classification accuracy) and correlation with human users (100 tasks). However, the paper does not analyze whether the simulator introduces systematic biases (e.g., being overly cooperative, missing subtle human conversational patterns, favoring certain interaction strategies). The significant correlation drop from GPT-4o (0.84) to Gemini-2.0-Flash (0.79) suggests backbone model choice matters, yet this is not explored.

- **No analysis of when the simulator itself fails during actual evaluation:** The USERSIM-GUARD evaluation is on static classification, but during dynamic interaction, the simulator's responses influence the system's subsequent actions, creating compounding errors. An analysis of evaluation failures attributable to simulator errors versus model limitations is missing.

- **Cost asymmetry across models not properly accounted for:** Table 2 shows Avg. Cost varies by up to 15x across models (e.g., Claude-Sonnet-3.7 at $0.60 vs O3-Mini at $0.07 in a-Interact). Higher-cost models like Claude-Sonnet-4 achieve better performance, raising the question of whether performance differences are partly driven by the ability to spend more budget on trial-and-error rather than genuine interaction skill. Differences in cost due to different output lengths and action choices should be controlled for or analyzed.

- **Missing analysis of sub-task dependencies and error propagation:** The paper notes that subsequent sub-tasks are released only after the first is completed, and that failure in the priority sub-task terminates the session. This creates a strong path-dependency, yet there is no analysis of where models fail (is it the ambiguity resolution sub-task or the follow-up?) and whether failure patterns are consistent across models. "Follow Ups (Success Rate)" is reported cumulatively, which conflates prior sub-task failures.

### Minor

- **Budget constraint formulation appears hand-designed:** The budget formulas B = B_base + 2*m_amb + 2*λ_pat and τ_clar = m_amb + λ_pat for c-Interact are not justified. Why base 6? Why coefficient 2? The paper should clarify whether results are sensitive to these choices.

- **The c-Interact setting seems under-defined versus a-Interact:** Section 4.1 explains that the user drives the conversation in c-Interact, but the system can still ask clarification questions. The distinction between a system "following a structured conversation" (c-Interact) versus "autonomous planning" (a-Interact) is intuitive but the exact action space overlap (both can ask questions, both have debugging opportunities) makes the boundary fuzzy, which could affect reproducibility.

- **Ambiguity injection metrics not reported:** How many queries became unsolvable after ambiguity injection? The paper claims "quality control ensures that ambiguous queries are unsolvable without clarification," but no verification metric (e.g., what percentage of original LIVESQLBENCH queries were solvable vs unsolvable after injection) is reported.

### Trivial
None.

## Nice-to-Haves

- Release the annotated USERSIM-GUARD dataset (2,100 questions with reference actions) to the community for user simulator research
- Analyze whether model rankings in single-turn text-to-SQL (e.g., on BIRD or Spider) correlate with rankings on BIRD-INTERACT
- Provide an analysis of the budget sensitivity on the Full set (currently only Lite set is analyzed in Figure 4)

## Novel Insights

Beyond its contributions, the paper reveals that "interaction skill" is a distinct capability from SQL generation skill, as shown by the memory grafting experiment where GPT-5's SQL generation excels when given interaction histories from weaker models. This dissociation between communication ability and code generation ability suggests that interactive text-to-SQL requires separate optimization of dialogue management, not just better SQL generation. The finding that models prefer trial-and-error execution (submit/ask actions) over systematic knowledge/schema exploration, even when the latter is cheaper, points to pre-training biases that may be suboptimal for interactive database tasks.

## Suggestions

1. Clearly delineate the benchmark's novel contributions from LIVESQLBENCH by providing a table mapping what was inherited versus newly created (databases, queries, annotations, user simulator, evaluation framework, etc.)
2. Conduct a failure analysis where evaluation outcomes are attributed to (a) user simulator errors, (b) model reasoning/planning errors, (c) SQL generation errors, to better understand which component is the bottleneck
3. Add an experiment controlling for interaction budget to separate the effect of "being able to spend more" from "interacting more effectively"

## Score and Decision

The paper presents a well-motivated, carefully constructed benchmark that addresses a clear gap in text-to-SQL evaluation. The function-driven user simulator is a methodological improvement over prior work, and the comprehensive evaluation across 7 models reveals meaningful insights. However, the strong dependence on LIVESQLBENCH without clear delineation of novel contributions, limited analysis of simulator failures in dynamic settings, and lack of cost-controlled experiments are notable weaknesses.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>