## Summary

This paper introduces BIRD-INTERACT, a benchmark that converts the single-turn BIRD/LIVESQLBENCH text-to-SQL tasks into dynamic, multi-turn interactive scenarios. It provides (1) a function-driven user simulator that maps model questions to constrained symbolic actions to prevent ground-truth leakage, (2) two evaluation settings—protocol-guided *c*-Interact and autonomous *a*-Interact, and (3) 600+300 tasks spanning CRUD operations with injected ambiguities, follow-up sub-tasks, and state dependencies. Experiments on 7 frontier LLMs show very low success rates (GPT-5 achieves 8.67% in *c*-Interact and 17% in *a*-Interact), and analyses including memory grafting and interaction test-time scaling reveal that communication strategy is as critical as SQL generation ability.

## Strengths

- **Timely and practically important problem**: Real-world database interaction is inherently multi-turn and ambiguous, but nearly all text-to-SQL benchmarks evaluate on single, perfectly-formed queries. This gap is significant and the paper convincingly motivates why dynamic interaction matters.

- **Function-driven user simulator is a technically sound solution**: The two-stage approach (LLM-as-parser mapping to AMB/LOC/UNA actions, then controlled response generation) directly addresses the ground-truth leakage and inconsistent behavior problems in prior simulators. The USERSIM-GUARD evaluation (Section 6) provides concrete evidence: baseline simulators fail on UNA questions up to 67.4% of the time, while the proposed approach reduces failure to 2.7%.

- **Comprehensive empirical evaluation with insightful analyses**: Testing 7 frontier models with multiple metrics (success rate, normalized reward, cost) is thorough. The memory grafting experiment (Figure 5) is a clever probe that cleanly separates communication ability from SQL generation ability. The action distribution analysis in *a*-Interact revealing a bias toward trial-and-error over systematic exploration is an actionable finding for the community.

- **Methodological rigor in annotation**: The ambiguity injection taxonomy (surface-level, knowledge chain breaking, environmental) with quality control ensuring unsolvability without clarification is well-specified. The use of 12 expert annotators with inter-agreement of 93.33% provides confidence in data quality.

## Weaknesses

### Fatal
None identified.

### Major

- **Limited novelty relative to prior work**: BIRD-INTERACT is built directly on LIVESQLBENCH (BIRD-Team, 2025), which is from the same group. While converting single-turn to multi-turn is a contribution, the core idea of dynamic interaction evaluation for text-to-SQL has precedent in the agent evaluation literature (MINT, Wang et al., 2024). The paper's novel contribution—the controlled user simulator and the specific annotation methodology—is incremental rather than paradigm-shifting for a top venue. The heavy reliance on an existing platform makes it unclear how much of the benchmark infrastructure is new versus inherited.

- **Single-run evaluation for all models**: The paper states it conducts "single runs due to cost" (Section 5). For a benchmark paper that reports performance comparisons across models, single runs introduce uncontrolled variance from stochastic model behavior, especially for non-deterministic LLMs with reasoning capabilities. Without quantifying variance (e.g., by running 3-5 seeds on a subset), the reported rankings and success rates have unknown reliability.

- **Moderate scale and narrow scope within the benchmark**: 900 tasks (600 full + 300 lite) with only 2 sub-tasks each is relatively modest compared to established benchmarks (Spider: 10k+, BIRD: 12k+, SParC: 4k+). The two-sub-task design limits the depth of multi-turn interaction tested. The paper does not provide a detailed breakdown of CRUD operation types (e.g., how many tasks involve INSERT vs. CREATE vs. DELETE), making it difficult to assess the claimed "full CRUD spectrum" coverage.

- **The ITS Law claim is oversupported by the data**: The paper claims "Interaction Test-time Scaling" where "performance improves monotonically with additional interaction opportunities across multiple models." However, Figure 4 shows mixed patterns—several models (especially in *a*-Interact) show flat or non-monotonic behavior. Only Claude-3.7-Sonnet in *c*-Interact shows clear scaling. This overclaiming weakens one of the paper's highlighted findings.

### Minor

- **"GPT-5" naming is confusing**: GPT-5 does not exist as a publicly known model. This appears to be either a placeholder name, a future model tested under NDA, or a mislabeling. The paper should clarify what model this actually refers to.

- **The interaction budget formulation is underspecified in the main text**: The budget formulas ($\tau_{\text{clar}} = m_{\text{amb}} + \lambda_{\text{pat}}$ and $B = B_{\text{base}} + 2m_{\text{amb}} + 2\lambda_{\text{pat}}$) are stated but not justified. Why base budget is 6, why the multiplier is 2 for *a*-Interact, and how these values were calibrated is deferred to appendices.

- **Online vs. offline evaluation discrepancy not fully explained**: The paper notes that normalized reward and success rate can diverge due to the 70/30 sub-task weighting, but doesn't reconcile cases where a model might have low SR but high reward (or vice versa), which would be informative for understanding the metrics' behavior.

### Trivial
- The user simulator accuracy of 90-95% on UNA questions (Figure 6) still means 5-10% of evaluation interactions may receive unfair feedback. A discussion of how this residual error affects benchmark conclusions would be helpful.

## Nice-to-Haves

- Release the function-driven user simulator as a standalone, reusable component for the community to use in other interactive benchmarks.
- Include human expert performance on a subset of tasks to establish a practical upper bound for the benchmark.
- Provide a breakdown of performance by ambiguity type (surface-level vs. knowledge chain breaking vs. environmental) to guide future research priorities.

## Novel Insights

The key insight emerging from this paper is that *interaction strategy* and *SQL generation capability* are partially dissociable skills in multi-turn text-to-SQL. The memory grafting experiment cleanly demonstrates this: GPT-5, a model that underperforms in *c*-Interact, achieves substantially higher success when given interaction histories from better-communicating models. This suggests that frontier LLMs may have sufficient SQL knowledge but lack effective communication schemas—a finding that redirects research attention from purely improving SQL accuracy to developing interaction policies. Additionally, the observation that models disproportionately favor costly trial-and-error actions (*submit*, *ask*) over cheaper systematic exploration (*retrieve schema*, *retrieve knowledge*) in the *a*-Interact setting reveals a specific behavioral pathology that may be addressable through prompt design or fine-tuning.

## Suggestions

- Run multi-seed evaluation on the Lite set (e.g., 3 seeds) to quantify variance and establish whether the reported rankings are statistically reliable.
- Tone down the "ITS Law" claim unless it holds more broadly than Figure 4 currently suggests—consider framing it as "some models exhibit scaling" rather than a general law.
- Clarify what "GPT-5" refers to—either rename it to the actual model identifier or provide a footnote explaining the naming convention.
- Add a table in the main paper showing the distribution of CRUD operation types across the benchmark to substantiate the "full CRUD spectrum" claim.

## Score and Decision

This paper addresses an important gap—dynamic interaction evaluation for text-to-SQL—with a methodologically sound benchmark construction and thorough experiments. The function-driven user simulator is a genuine improvement over existing approaches. However, the contribution is incremental given the heavy reuse of LIVESQLBENCH infrastructure and the existence of prior interactive evaluation frameworks (MINT). The single-run evaluation and modest scale also limit the benchmark's impact. The work has clear value for the community but does not represent a paradigm shift.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>