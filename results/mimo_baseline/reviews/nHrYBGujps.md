## Summary

The paper introduces BIRD-INTERACT, a benchmark for evaluating LLMs in dynamic, multi-turn text-to-SQL interactions that goes beyond static conversation transcripts and SELECT-only queries. It features a function-driven user simulator that avoids ground-truth leakage, two evaluation paradigms (protocol-guided *c*-Interact and agentic *a*-Interact), full CRUD task coverage, and budget-constrained awareness testing, comprising 900 tasks that unfold up to ~11,800 dynamic interactions. Even frontier models like GPT-5 achieve only 8.67% (c-Interact) and 17.00% (a-Interact) end-to-end success rates on the full suite.

## Strengths

- **Well-motivated gap identification.** The paper convincingly demonstrates that existing multi-turn benchmarks (COSQL, LEARN-TO-CLARIFY) rely on static conversation transcripts, forcing all models to follow predetermined trajectories regardless of their natural interaction strategy. This is a genuine and important limitation that the paper directly addresses through dynamic evaluation.

- **Function-driven user simulator with strong empirical validation.** The two-stage approach (mapping model questions to constrained symbolic actions before generating responses) is technically sound. The USERSIM-GUARD evaluation shows dramatic improvements in reliability (failure rates reduced from 67.4% to 2.7% on unanswerable queries), and human alignment experiments show significantly higher correlation (0.84 vs. 0.61 Pearson) between simulator and human success rates across models.

- **Comprehensive ambiguity taxonomy and injection methodology.** The paper defines a principled categorization of ambiguities (superficial, knowledge chain-breaking, environmental) paired with executable test cases ensuring that ambiguous queries are unsolvable without clarification yet fully reconstructable once provided. This creates a controlled experimental framework.

- **Novel analysis dimensions.** The memory grafting experiment reveals that GPT-5's poor c-Interact performance stems from communication deficiency rather than SQL generation weakness—a genuine insight. The Interaction Test-time Scaling (ITS) analysis demonstrates monotonic performance improvement with additional interaction turns across models, establishing an interesting empirical finding.

- **Dual evaluation settings testing complementary capabilities.** The divergence in model rankings across settings (e.g., GPT-5 ranks worst in c-Interact but best in a-Interact) provides meaningful evidence that interaction paradigm design critically affects measured performance.

## Weaknesses

### Fatal

None.

### Major

- **Single experimental runs with no variance reporting.** The authors acknowledge conducting "single runs due to cost." For a benchmark that will be used to compare systems, the lack of any variance estimation or confidence intervals makes it difficult to assess whether observed differences between models (e.g., Claude-Sonnet-4 at 22.33% vs. O3-Mini at 24.00% in c-Interact) are meaningful or within noise. At minimum, variance estimates on the LITE subset would substantially strengthen the results.

- **Only two sub-tasks per task (n=2).** While practical for annotation, this limits the ability to evaluate longer-horizon planning and state management. Real interactive database sessions may involve 5-10+ dependent steps. The paper claims to capture "evolving user requirements" but each task sequence is quite short, which somewhat undercuts the "long-horizon" positioning.

### Minor

- **Human alignment evaluation scope.** The correlation analysis in Table 3 uses only 100 tasks and 7 system models, yielding relatively few data points for correlation computation. The p-values (0.02, 0.03) are significant but modest, and wider task sampling would increase confidence in the simulator's general alignment.

- **ITS "law" lacks formal characterization.** The paper introduces an "ITS Law" stating that performance with enough interaction turns can match idealized single-turn performance, but this is stated informally without derivation of conditions under which it holds or fails. The term "law" suggests a stronger theoretical claim than the empirical observations support.

- **Budget constraint analysis is incomplete.** The paper introduces budget-constrained awareness as a key feature but the main experiments use a single default patience setting (λ_pat=3). More systematic analysis of how models degrade under tighter budgets would better motivate this design choice.

### Trivial

- The cost analysis in Table 2 reports user simulator cost (0.03 USD) separately but doesn't provide end-to-end per-task cost including both system and simulator, which would be more informative for practitioners.

## Nice-to-Haves

- Include at least 3-5 runs on the LITE subset with standard deviations reported for key metrics.
- Extend task depth beyond 2 sub-tasks for a subset of tasks to evaluate longer-horizon interaction.
- Provide ablation on the ambiguity types to identify which categories are most challenging for current models.

## Novel Insights

The memory grafting experiment provides a genuinely novel insight: GPT-5's underperformance on protocol-guided interaction is not due to insufficient SQL generation capability but rather to poor communication strategy. When provided with interaction histories from better-communicating models (Qwen-3-Coder, O3-Mini), GPT-5's performance jumps significantly, demonstrating that the interaction modality and model capability can be decoupled. Combined with the finding that models universally prefer trial-and-error over systematic resource exploration in agentic mode, this suggests that current LLM training heavily biases toward execution-based problem solving at the expense of strategic information gathering—a finding with broader implications beyond text-to-SQL.

## Suggestions

- Run at least 3 seeds on the LITE subset to establish variance; this is critical for a benchmark paper where downstream comparisons depend on measured differences being reliable.
- Consider adding a "free-mode" a-Interact variant (acknowledged in Future Work) even in this submission, as the stress-mode-only evaluation may not reveal natural interaction patterns.
- Add per-ambiguity-type breakdown in the main results table to help diagnose which interaction challenges are most acute.

## Score and Decision

This is a well-executed benchmark paper that addresses a genuine and important gap in text-to-SQL evaluation. The function-driven simulator design is a meaningful methodological contribution with strong empirical backing. The dual evaluation settings, CRUD coverage, and budget constraints create a comprehensive evaluation framework. The experimental analysis—particularly memory grafting and ITS—yields actionable insights. The main weakness is the lack of variance reporting in a benchmark that aspires to become a standard evaluation suite, plus the relatively shallow task depth (n=2). These are addressable but non-trivial limitations for a benchmark paper.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: Accept