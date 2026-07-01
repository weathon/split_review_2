## Summary

This paper investigates the problem of output length volatility in long-form generation from Large Language Models (LLMs). The authors introduce VOLTBench, a heterogeneous-task benchmark to quantify length volatility across multiple generations, probe internal attention mechanisms to identify patterns like Attention Collapse and Attention Instability, and propose SELB (Structural Enforcement via Logits Boosting), a lightweight, training-free decoding strategy that improves mean output length by 148% and reduces length volatility by 69%.

## Strengths

- **Novel problem framing**: The paper identifies and systematically studies an important and overlooked issue—output volatility across multiple generations rather than single-generation quality—which has practical implications for reliability and computational cost in real LLM applications.
- **Comprehensive benchmark design**: VOLTBench covers multiple dimensions (language, instruction complexity, output format) and includes both unstructured and structured tasks with explicit length constraints, enabling fine-grained analysis of model behavior.
- **Attention-based mechanistic analysis**: The probing of attention traces to identify internal patterns of volatility (Attention Collapse and Attention Instability) provides a plausible causal link between model internals and observed output instability, going beyond purely phenomenological observation.
- **Practical mitigation**: SELB is lightweight, training-free, and demonstrably effective across multiple base models (Qwen2.5-7B, Qwen3-8B, Llama3.1-8B), with results showing large improvements in length accuracy and volatility reduction while maintaining quality.
- **Strong experimental scope**: The evaluation includes multiple mainstream models (GPT-4o-mini, Claude-3.5-Sonnet, Deepseek-R1, etc.) and compares against several training-free decoding strategies, lending credibility to the findings.

## Weaknesses

### Major

- **Limited number of repeated queries**: The volatility evaluation uses only N=5 runs per instruction (stated in Section 3.2). With such a small sample size, the LSD and LVC metrics may have high variance and may not reliably capture true output volatility. This is a significant methodological concern for a benchmark claiming to measure stability.
- **Incomplete comparison with existing methods**: The paper compares SELB against simple baselines (Repetition Penalty, Entropy-Based Stopping, Length Constraint, Lookahead Decoding) but does not compare with more sophisticated training-free methods (e.g., contrastive decoding, typical sampling, or methods that adaptively control generation length). The claim that SELB is superior would be stronger with a more comprehensive comparison.
- **Lack of formal definitions for key patterns**: The identified patterns (Attention Collapse, Attention Instability) are described qualitatively and only shown in two model examples. There is no formal definition, detection threshold, or automated identification procedure for these patterns, making it difficult to verify their generality or reproduce the analysis.

### Minor

- **The quality evaluation on unstructured tasks relies on LLM-as-a-Judge**, which is known to have biases and limited reproducibility. The paper acknowledges this but does not discuss potential confounding effects or provide evidence of judge reliability.
- **The generalization to free-form generation (Section 6.4) is mentioned but detailed experimental results are relegated to the appendix**, which is stripped. The reader cannot verify these claims based on the main text alone.

### Trivial

- Some figure descriptions in captions are repeated verbatim.

## Nice-to-Haves

- A formal definition and automated detection method for Attention Collapse and Attention Instability would strengthen the probing contribution.
- An ablation study showing which component of SELB (structural enforcement vs. proactive failure prevention) contributes more to the observed improvements.
- Analysis of how the choice of the number of repeated runs (N) affects the stability of the benchmark metrics.

## Novel Insights

Beyond the paper's own contributions, the key insight is that LLMs exhibit systematic and predictable failure modes in long-form generation (accelerating attention to irrelevant tokens and collapsing attention to constraints) and that these failures can be mitigated through simple logit manipulation at decoding time, without retraining or fine-tuning. The finding that structured tasks naturally induce lower volatility (due to stronger format constraints) is a useful practical observation for practitioners.

## Suggestions

1. **Increase the number of repeated runs** for volatility evaluation to at least N=10-20, or provide a justification (with empirical evidence) that N=5 is sufficient for reliable estimation.
2. **Add comparisons with more recent training-free decoding control methods** such as contrastive decoding, typical sampling, or classifier-free guidance approaches.
3. **Provide a formal definition** of the identified attention patterns (e.g., a threshold-based detector for Attention Collapse) to enable reproduction and broader analysis by the community.

## Score and Decision

The paper tackles a genuinely important and understudied problem, provides a comprehensive benchmark and insightful mechanistic analysis, and proposes a simple but effective practical solution. The main weaknesses are the small sample size for volatility measurement and the incomplete comparison with existing decoding control methods. These are substantial but not fatal; the paper's core contributions (benchmark, attention analysis, mitigation strategy) are sound and valuable.

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>