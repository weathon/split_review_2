## Summary

This paper introduces Ambig-SWE, an underspecified variant of SWE-Bench Verified designed to evaluate how LLM agents handle incomplete instructions in interactive code generation settings. The authors systematically evaluate proprietary and open-weight models across three key capacities: detecting underspecificity, asking targeted clarification questions, and leveraging interaction to improve performance. Their experiments reveal that while interaction can recover up to 74% of performance lost to underspecificity, most models default to non-interactive behavior, struggle to distinguish well-specified from underspecified inputs, and show brittle sensitivity to prompt engineering.

## Strengths

- **Well-motivated and practically important problem**: The paper addresses a critical real-world issue—how AI agents handle underspecified instructions—that has direct implications for safety, resource efficiency, and task alignment in deployed systems. The motivation is clearly articulated with concrete examples.

- **Carefully designed evaluation framework**: The decomposition of underspecificity handling into three distinct capacities (detection, questioning, integration) is thoughtful and enables targeted analysis. The three experimental settings (Full, Hidden, Interaction) provide clean ablations to isolate the effects of underspecificity and interaction.

- **Comprehensive model coverage and insightful comparisons**: The paper evaluates six models spanning proprietary (Claude family) and open-weight (Llama, Deepseek, Qwen) categories, with meaningful comparisons across model scales and families. The analysis of navigational vs. informational details (Table 1) and question-asking strategies (§5.3) provides nuanced insights beyond simple accuracy numbers.

- **Actionable empirical findings**: The paper identifies specific failure modes (e.g., Qwen 3 Coder's complete non-responsiveness to interaction prompts, Llama's poor question quality) and provides concrete guidance for future model and agent design, such as the importance of exploration-first strategies and answerability in clarification questions.

## Weaknesses

### Fatal
None.

### Major
- **Synthetic underspecification generation may not reflect real-world patterns**: The paper generates underspecified issues by having GPT-4o remove details from fully specified SWE-Bench Verified issues. While the authors acknowledge this limitation and provide distributional analysis, the synthetic nature raises concerns about ecological validity. Real-world underspecification often involves ambiguous phrasing, implicit assumptions, and conversational fragments that may differ qualitatively from "aggressive information removal." The paper's own analysis shows that natural underspecified issues have more concrete technical details and conversational fragments, suggesting the synthetic data may not capture the full challenge.

- **User proxy limitations are under-explored**: The use of GPT-4o as a simulated user proxy is a significant design choice that could substantially affect results. The proxy is described as "conservative" and only responds with information explicitly in the full issue, but the paper does not validate whether this proxy behavior is realistic or whether different proxy behaviors would change conclusions. Real users may be less cooperative, provide irrelevant information, or have incomplete knowledge themselves. The paper acknowledges this briefly in limitations but does not discuss how it might affect the key findings.

- **Detection experiment conflates multiple factors**: In RQ2, the detection accuracy metric combines the model's ability to detect underspecificity with its willingness to act on that detection through interaction. A model might correctly identify missing information but choose not to ask (e.g., due to training biases toward self-sufficiency), which would be counted as a detection failure. The paper's framing of "detection" conflates perceptual and behavioral aspects, making it unclear whether failures are due to inability to recognize underspecificity or inability to overcome default non-interactive behavior.

### Minor
- **Limited analysis of interaction efficiency**: The paper notes that interaction improves effectiveness but not efficiency, but does not deeply analyze why. Understanding whether inefficiency stems from redundant questions, poor information integration, or other factors would strengthen the practical recommendations.

- **Statistical significance reporting is incomplete**: While the paper mentions Wilcoxon Signed-Rank tests, the results are only referenced in an appendix table. The main text would benefit from explicit p-values or effect sizes to support claims about significance.

- **The 30 vs. 100 turn allocation difference across models is not fully justified**: Claude Sonnet 4 and Qwen 3 Coder receive more interaction turns, which could confound comparisons. The paper mentions this is due to "greater reasoning and planning capacity," but this introduces a confound between model capability and experimental resources.

### Trivial
- Figure 2 is difficult to parse due to dense text in the figure panels; the key information could be more clearly presented in a table.

## Nice-to-Haves

- A human evaluation study comparing the synthetic underspecified issues to real underspecified GitHub issues would strengthen ecological validity.
- Analysis of how different user proxy behaviors (e.g., less cooperative, more verbose) affect agent performance would be valuable.
- A breakdown of which types of missing information (file locations, expected behavior, error context) are most impactful for task completion.

## Novel Insights

Beyond the paper's own contributions, a genuinely novel insight emerges from the comparison of Qwen 3 Coder and Claude Sonnet 4: high task capability does not automatically translate to effective interaction. Qwen 3 Coder achieves strong SWE-Bench performance but shows rigid, non-adaptive behavior—it fails to interact even when explicitly prompted, and when it does receive navigational information, it redundantly re-explores the codebase. This suggests a fundamental tension between training for autonomous task completion and training for effective human-AI collaboration. Current training paradigms that optimize for end-to-end task success may inadvertently suppress interactive behaviors, as models learn to rely on their own knowledge and exploration rather than seeking external information. This has important implications for how we should train future agents: interaction skills may need to be explicitly incentivized rather than expected to emerge from general capability improvements.

## Suggestions

- Conduct a validation study comparing agent behavior on synthetic vs. naturally occurring underspecified issues to assess ecological validity of the Ambig-SWE dataset.
- Disentangle detection from action in RQ2 by adding a control condition where models are explicitly told to output a "detection" judgment before being allowed to interact, separating perceptual from behavioral aspects.
- Include a more detailed analysis of interaction efficiency, such as measuring the number of wasted turns (questions that yield no new information or information already available in the codebase).

## Score and Decision

The paper makes a solid contribution to an important and under-studied problem. The evaluation framework is well-designed, the experiments are thorough, and the findings provide actionable insights for the community. However, the synthetic nature of the underspecification data and the reliance on a simulated user proxy introduce uncertainties about real-world applicability that prevent a higher score. The paper is clearly above the acceptance threshold but not at the level of a top-tier contribution that would warrant a 10.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>