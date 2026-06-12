## Summary

SWINGARENA introduces an adversarial evaluation framework for LLMs in software engineering that pairs models as *submitters* (generating patches) and *reviewers* (creating test cases) within real CI pipelines across C++, Python, Rust, and Go. The framework includes a Retrieval-Augmented Code Generation (RACG) module for long-context handling and a curated dataset of 2,300 GitHub issues with 400 evaluation instances. Experiments across proprietary and open-source models reveal behavioral differences in patch generation versus validation capabilities.

## Strengths

- **Novel adversarial evaluation paradigm**: The submitter-reviewer dual-role framework with CI-based verification is a meaningful step beyond static benchmarks like SWE-Bench, capturing the iterative, adversarial nature of real software development workflows. The role-switching design and scoring protocol are well-conceived.

- **Multi-language coverage with rigorous CI integration**: Supporting four languages (C++, Python, Rust, Go) with actual CI pipeline execution (not simulated tests) is a significant practical contribution. The use of repository-native CI configurations (GitHub Actions, Travis CI) with Docker isolation provides realistic validation.

- **Comprehensive ablation and analysis**: The paper includes thorough ablation studies on RACG components, retrieval granularity, Best@k scaling behavior, and failure pattern analysis. The ablation showing RACG improves Best@3 from 0.38 to 0.42 and Win Rate from 0.77 to 0.84 in C++ is concrete evidence of the module's value.

- **Careful variance control**: The paper explicitly addresses reproducibility concerns in adversarial settings through fixed prompts, temperature=0 decoding, pinned Docker images, and fixed random seeds. This methodological rigor is commendable for an interactive evaluation framework.

## Weaknesses

### Fatal
None.

### Major

- **Limited novelty of the core evaluation protocol**: The adversarial submitter-reviewer paradigm, while well-executed, is conceptually similar to existing work on adversarial testing and code review simulation. The paper's claim of being "the first" to model this interaction is overstated given prior work on adversarial code generation and test case generation. The RACG module is explicitly positioned as "not a standalone algorithmic contribution" (Section 1), which raises questions about what the primary technical contribution is beyond the dataset and evaluation framework.

- **Small evaluation set (400 instances) with potential selection bias**: The 400 evaluation instances (100 per language) are filtered through multiple stages including LLM-as-a-Judge and expert filtering. While quality filtering is reasonable, the aggressive filtering from 2,300 to 400 instances raises concerns about whether the remaining samples are representative of real-world GitHub issues or biased toward problems that are "solvable" by current LLMs. The paper does not analyze what types of issues were filtered out or how this affects generalization.

- **Win Rate metric interpretation issues**: The paper acknowledges that "higher values may also indicate weaker reviewer tests" (Section 4.1), yet Win Rate is used as a primary comparison metric. The self-play results (Claude vs Claude achieving 1.00 Win Rate) suggest that models may be generating weak tests for their own patches rather than demonstrating genuine robustness. The paper does not adequately disentangle patch quality from reviewer strictness.

- **Missing statistical significance analysis**: The main results (Table 1) show small differences between models (e.g., 0.55 vs 0.54 SPR) without any confidence intervals or statistical tests. Given the small sample size (400 instances) and the variance introduced by the adversarial protocol, it's unclear whether observed differences are meaningful or noise.

### Minor

- **RACG token budget limitation**: The fixed Top-5 file retrieval limit is acknowledged as a potential bottleneck, but the paper does not explore how varying this parameter affects results. Given that the RACG module is central to handling long contexts, this is a notable omission.

- **Open-source model evaluation is limited**: Table 4 (referenced but not shown in the main text) is relegated to the appendix. The paper would benefit from more prominent discussion of open-source model performance to demonstrate the framework's accessibility.

- **The "adversarial" nature is somewhat constrained**: The reviewer generates tests to challenge patches, but the paper does not explore more sophisticated adversarial strategies (e.g., multi-turn dialogue, targeted probing of specific failure modes). The current protocol is more "cooperative" than truly adversarial.

### Trivial
- The paper contains some redundancy in describing the battle protocol (appears in both Section 3.2 and Section 3.3).

## Nice-to-Haves

- A comparison with SWE-Bench on a shared subset of Python tasks would strengthen the claim that SWINGARENA surfaces different model behaviors than static benchmarks.
- Analysis of how reviewer test quality (e.g., code coverage, mutation score) correlates with Win Rate would help interpret the results.
- The paper could benefit from a discussion of the computational cost of running CI pipelines for evaluation, as this is a practical barrier to adoption.

## Novel Insights

The paper's most interesting finding is the asymmetry in model behavior between patch generation and test generation roles. GPT-4o's aggressive patching (high Win Rate but lower CI pass rates) versus DeepSeek/Gemini's reliability (lower Win Rate but higher CI pass rates) reveals that different models have fundamentally different "strategies" in software engineering tasks. This suggests that current benchmarks focusing solely on functional correctness may miss important dimensions of code quality and robustness. The finding that self-play (same model as submitter and reviewer) produces the highest Win Rates (Claude at 1.00) is particularly telling—it suggests models may be "gaming" the evaluation by generating tests that are aligned with their own patch generation patterns rather than genuinely challenging tests. This has implications for how we should design adversarial evaluation protocols.

## Suggestions

1. **Add confidence intervals or bootstrap estimates** to all main results (Tables 1, 2, 3) to help readers assess the reliability of observed differences between models.

2. **Include a "reviewer quality" metric** (e.g., how many reviewer-generated tests fail the golden patch, or code coverage of reviewer tests) to disentangle patch quality from reviewer strictness in Win Rate interpretation.

3. **Conduct a sensitivity analysis** on the Top-5 file retrieval limit in RACG, showing how performance changes with k=3, 5, 10, 20 to better understand the retrieval bottleneck.

4. **Add a comparison with SWE-Bench** on the Python subset to directly demonstrate what new insights SWINGARENA provides beyond existing benchmarks.

5. **Report the distribution of issue difficulty** in the final 400-instance set (e.g., how many required changes across multiple files, how many involved complex logic) to help readers assess task representativeness.

## Score and Decision

The paper presents a well-engineered evaluation framework with practical contributions in multi-language CI integration and adversarial testing. However, the core methodological novelty is incremental—the adversarial submitter-reviewer paradigm is a natural extension of existing work rather than a fundamentally new approach. The small evaluation set and lack of statistical rigor in comparing models weaken the empirical contributions. The paper is solid and useful to the community but does not rise to the level of a top-tier acceptance at ICLR.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>