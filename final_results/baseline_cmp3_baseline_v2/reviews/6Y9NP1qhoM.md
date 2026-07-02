## Summary

This paper addresses the vulnerability of Large Language Model-based Multi-Agent Systems (MAS) to misinformation injection—covert, factually incorrect information that appears semantically benign. The authors introduce MISINFOTASK, a dataset of 108 realistic tasks with associated misinformation scenarios, and propose ARGUS, a two-stage training-free defense framework that combines adaptive localization of critical communication channels with goal-aware persuasive rectification. Experiments across multiple LLMs and attack methods show ARGUS reduces misinformation toxicity by approximately 28-36% and improves task success rates under attack by about 10%.

## Strengths

- **Timely and important problem**: The paper tackles a genuinely underexplored and practically significant vulnerability in MAS—misinformation that is covert rather than overtly malicious. This distinction is well-motivated and the paper correctly identifies that most prior work focuses on malicious/jailbreak content rather than subtle factual errors.

- **Novel dataset contribution**: MISINFOTASK fills a clear gap in the literature by providing a dataset specifically designed for misinformation injection testing in MAS, with 108 realistic tasks, potential injection points, and supporting/refuting argument sets. The dataset construction methodology (seed examples → guided sampling → manual filtering) is sound.

- **Well-designed defense framework**: ARGUS's two-stage approach (adaptive localization + goal-aware rectification) is principled and leverages the MAS graph structure effectively. The combination of topological importance, information relevance, and communication frequency for channel selection is sensible. The training-free nature is a practical advantage.

- **Comprehensive evaluation**: The paper evaluates across 4 different LLMs, 3 injection methods, 5 topological structures, and multiple defense baselines. The ablation studies (Tables 2 and 3) are thorough and help isolate the contribution of each component.

## Weaknesses

### Major

- **Limited dataset scale and diversity**: The dataset contains only 108 tasks. While the paper claims coverage of 5 categories (Conceptual Reasoning, Factual Verification, etc.), this is a small sample size for robust evaluation. The paper does not report per-category statistics or demonstrate that results are stable across categories. With only 108 samples, a few outlier tasks could significantly skew aggregate metrics.

- **Unclear evaluation methodology for MT and TSR**: The scoring function `Score(·,·)` is evaluated by an LLM judge (GPT-4o-2024-08-06), but the paper does not provide any validation of this judge's reliability. There is no human evaluation, no inter-annotator agreement, and no analysis of whether the LLM judge might be biased toward or against certain defense methods. The threshold θ_m for TSR is mentioned but never specified.

- **No comparison to state-of-the-art defense methods**: The baselines (Self-Check and G-Safeguard) are reasonable but limited. The paper does not compare against other relevant defense approaches such as multi-agent debate (Chern et al., 2024), graph pruning (AgentPrune), or hierarchical data management (AgentSafe), all of which are cited in the related work. This makes it difficult to assess whether ARGUS is truly state-of-the-art or merely competitive.

- **Computational cost not quantified**: The paper acknowledges efficiency concerns in the limitations section but provides no quantitative analysis of the overhead introduced by ARGUS. How many additional LLM calls does ARGUS require per round? What is the latency impact? Without this information, practitioners cannot assess the practical trade-off.

### Minor

- **The threat model is somewhat narrow**: The attacker compromises a single agent and injects misinformation at the initial round. Real-world scenarios might involve multiple compromised agents, staggered injection over time, or adaptive attackers who change their misinformation strategy in response to defense. The paper would benefit from discussing how ARGUS might handle these more complex scenarios.

- **Goal-aware intent inference accuracy is modest**: Figure 4 shows accuracy ranging from ~0.50 to ~0.80 depending on category and injection type. While the paper frames this positively, accuracy below 0.60 for some conditions (e.g., Tool Injection in the "star" category) suggests the inferred goals may be unreliable, which could undermine the adaptive re-localization.

- **The "persuasive rectification" mechanism is underspecified**: Section 4.2 describes the process at a high level (sentence-by-sentence deconstruction, internal knowledge resonance, heuristic persuasive reconstruction) but does not provide the actual prompts or detailed algorithmic steps. The appendix reference (B.4) is stripped, so the reader cannot assess the quality of the rectification logic.

### Trivial

- The paper uses "re-teaming" instead of "red-teaming" in the introduction (Section 1, paragraph 3).

## Nice-to-Haves

- A human evaluation study to validate the LLM judge's scoring would significantly strengthen the paper's claims.
- Analysis of which types of misinformation (by category) are most/least effectively defended would provide practical guidance.
- A cost-benefit analysis showing the trade-off between defense effectiveness and computational overhead would help practitioners.

## Novel Insights

None beyond the paper's own contributions. The key insight—that misinformation in MAS can be detected and rectified by combining graph-theoretic localization with goal-aware reasoning—is well-articulated within the paper itself.

## Suggestions

1. **Validate the LLM judge**: Conduct a human evaluation on a subset of outputs to establish inter-annotator agreement between the LLM judge and human raters. Report Cohen's kappa or similar metrics.

2. **Expand the dataset**: Either increase the dataset size or provide per-category breakdowns to demonstrate that results are robust across different types of misinformation.

3. **Add computational cost analysis**: Report the number of additional LLM calls, tokens processed, and wall-clock time overhead introduced by ARGUS relative to the attack-only baseline.

4. **Compare against more baselines**: Include comparisons to AgentPrune, AgentSafe, and multi-agent debate approaches to establish state-of-the-art positioning.

5. **Provide the actual prompts**: Include the CoT prompts used for detection and rectification in the main paper or a clearly accessible appendix.

## Score and Decision

The paper addresses a genuinely important and underexplored problem, makes a concrete contribution with the MISINFOTASK dataset, and proposes a well-designed defense framework. The evaluation is reasonably comprehensive across multiple dimensions. However, the small dataset size, lack of LLM judge validation, and absence of computational cost analysis are significant concerns that prevent a higher score. The paper is solid but not yet at the level of a top-tier acceptance.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>