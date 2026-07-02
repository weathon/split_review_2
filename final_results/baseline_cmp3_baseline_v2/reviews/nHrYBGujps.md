## Summary

This paper introduces BIRD-INTERACT, a benchmark for evaluating LLMs on dynamic, multi-turn text-to-SQL tasks that better reflect real-world database interactions. The benchmark contributes: (1) a high-fidelity interactive environment with a function-driven user simulator that prevents ground-truth leakage, (2) two evaluation settings (*c*-Interact for protocol-guided conversation and *a*-Interact for autonomous agentic planning), and (3) a task suite of 900 tasks covering the full CRUD spectrum with ambiguous initial queries, follow-up sub-tasks, and state dependencies. Empirical results show SOTA models struggle significantly, with GPT-5 achieving only 8.67% success in *c*-Interact and 17.00% in *a*-Interact.

## Strengths

- **Addresses a critical real-world gap**: The paper correctly identifies that existing text-to-SQL benchmarks evaluate models on static, perfectly-formed queries that fail to capture the ambiguous, iterative nature of real-world database interactions. The shift toward dynamic interaction evaluation is timely and important for the community.

- **Novel function-driven user simulator**: The two-stage approach (semantic parsing into constrained actions - AMB/LOC/UNA, then controlled response generation) is a principled solution to the ground-truth leakage and behavior inconsistency problems that plague naïve LLM-based simulators. The USERSIM-GUARD evaluation showing reduction in failure rate from 67.4% to 2.7% for unanswerable queries is compelling.

- **Thoughtful evaluation design**: The dual evaluation settings (*c*-Interact vs. *a*-Interact) reveal meaningful model differences that single-turn benchmarks miss—e.g., GPT-5 being worst in *c*-Interact but best in *a*-Interact, suggesting interaction mode matching matters. The budget-constrained awareness mechanism adds practical realism.

- **Comprehensive and rigorous empirical analysis**: The memory grafting experiment provides strong causal evidence that communication deficiencies (not SQL generation ability) limit performance in interactive settings. The Interaction Test-time Scaling (ITS) analysis and action distribution analysis offer concrete directions for future research.

## Weaknesses

### Major

- **Limited analysis of state-dependency across sub-tasks**: While the paper claims state-dependency between sub-tasks is a key contribution (p.3: "system models must reason over modified database states"), there is no experiment isolating this factor. The 17.00% *a*-Interact success on follow-up sub-tasks could be due to state-dependency, longer context, or both. An ablation study that evaluates models on the same tasks without state modification would strengthen the claim.

- **Reliance on a single interaction roll-out per model**: The paper states "conducting single runs due to cost" (Section 5). Given that LLM outputs are stochastic even at temperature=0 (due to implementation-level nondeterminism), reporting results without variance estimates weakens confidence in the relative model rankings. This is particularly concerning for edges of 1-2% differences between models.

- **Missing detailed ablation of ambiguity injection quality**: The paper describes injecting three types of ambiguities but does not provide a human evaluation verifying that the injected ambiguities are natural, that they truly require interaction to resolve, and that there is no latent leakage in the formulation that could shortcut the intended interaction requirement.

### Minor

- **The "comprehensive interaction environment" claim is overstated relative to dependencies on LIVESQLBENCH**: While BIRD-INTERACT contributes the interaction layer, the underlying databases, knowledge bases, and metadata files are inherited. The novelty is predominantly in the interaction wrapper and simulator rather than the environment itself.

- **User simulator analysis uses a proprietary evaluator**: The USERSIM-GUARD evaluation uses `Qwen3-235B-A22B-Instruct-2507` as judge (p.8). Without analysis of evaluator bias or calibration against human judgments for the classification task, there is risk that the evaluation itself favors the proposed approach.

### Trivial

- The paper alternates between table numbers (Table 2 uses numeric format, Table 1 uses standard format) in the main text references—this is cosmetic but could be unified.

## Nice-to-Haves

- Release of the actual interaction logs or a small-scale human annotation of "effective communication patterns" (as mentioned in Appendix P reference) would significantly strengthen the qualitative analysis.
- A breakdown of failure modes per ambiguity type (superficial vs. knowledge vs. environmental) would help the community prioritize which interaction scenarios to address first.

## Novel Insights

The interaction test-time scaling (ITS) observation—that performance correlates monotonically with increased interaction turns—is a practical extension of the test-time compute scaling narrative to the interactive domain. The GPT-5 memory grafting experiment provides a particularly clean demonstration that communication strategy (not just reasoning ability) is the binding constraint for interactive text-to-SQL, a finding that generalizes beyond the specific benchmark. The counterintuitive result that models favor costly submit/ask actions over cheaper exploration actions in *a*-Interact suggests that pre-training biases (from standard single-turn SQL benchmarks) may actively harm interactive performance, which is a testable hypothesis for future work.

## Suggestions

- Add variance/confidence intervals to main results (Table 2) through multiple seeds with reduced evaluation subsets, or provide evidence that single-run results are stable.
- Design an ablation experiment that compares follow-up sub-task performance with and without database state modification to isolate the effect of state-dependency.
- Include a human evaluation on a small sample of the injected ambiguities to validate their naturalness and the necessity of interaction for resolution.

## Score and Decision

The paper tackles a genuine gap in text-to-SQL evaluation, provides a well-engineered benchmark with thoughtful design choices (especially the function-driven simulator), and produces actionable empirical insights. The benchmark is likely to be adopted by the community. The weaknesses are real but not fatal—they suggest directions for future work rather than invalidating the core contribution.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>