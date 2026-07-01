## Summary

This paper re-evaluates claims that programmatic policies generalize better than neural policies in RL. Through controlled experiments on TORCS, KAREL, and PARKING, the authors show that much of the reported advantage disappears when confounds (reward shaping, observation design) are addressed. They then propose a framework based on *expressivity* (the policy space contains a generalizing solution) and *discoverability* (the search algorithm can find it). They argue that the genuine advantage of programmatic representations arises only when tasks require working memory that grows with input size—something fixed-capacity neural architectures cannot satisfy. A proof-of-concept using FUNSEARCH to synthesize breadth-first search for a maze domain supports this claim.

## Strengths

- **Important re-evaluation of influential claims:** The paper systematically revisits three prominent prior works and demonstrates that previously reported generalization gaps are largely due to experimental confounds rather than representational differences. This is a valuable service to the community.
- **Clear conceptual framework:** The decomposition into *expressivity* and *discoverability* provides a principled lens for analyzing when and why a representation might (or might not) enable OOD generalization. This framing is useful for future research.
- **Thorough and reproducible experiments:** The authors extend the original experimental setups, provide multiple seeds, and carefully document their modifications. The results convincingly show that neural policies can match programmatic ones under proper training conditions.
- **Identification of a theoretically sound differentiator:** The insight that tasks requiring memory scaling with input size (e.g., general pathfinding, nested subproblems) are inherently beyond fixed-capacity neural models is well-motivated and theoretically rigorous.

## Weaknesses

### Fatal
None.

### Major
- **The main positive claim (memory-scaling advantage) lacks strong experimental support.** The proof-of-concept uses FUNSEARCH with a large language model to synthesize BFS for a single modified Karel task. This does not demonstrate that *any* programmatic RL method can reliably learn such solutions, nor does it compare against neural baselines on the same task (the authors assert neural models would fail but do not train them). The paper would be stronger if it showed a programmatic RL algorithm (e.g., LEAPS, NDPS) succeeding on tasks where neural networks demonstrably fail.
- **The expressivity/discoverability framework is not formalized.** Definitions 2 and 3 are intuitive but vague—e.g., “within a bounded time limit” is not specified. The paper uses the framework conceptually but does not provide operational criteria or testable conditions. This limits its utility beyond post-hoc explanation.

### Minor
- **PARKING results are ambiguous.** DQN achieves higher test success rate (0.18 vs. 0.16), while PSM shows a smaller generalization gap. The paper does not resolve which representation is genuinely better, and the discussion acknowledges the domain is challenging for both. This weakens the narrative that confound resolution uniformly explains the gap.
- **The proof-of-concept is not integrated with standard RL.** FUNSEARCH with an LLM is far from typical RL training loops. It is unclear whether the approach can be scaled or generalized to other domains. The paper would benefit from a discussion of how programmatic RL could leverage this capability in practice.

### Trivial
None.

## Nice-to-Haves

- The paper could include a small experiment training a neural policy (e.g., LSTM, Transformer) on a task that requires memory scaling (e.g., a larger maze with no wall-following shortcut) to explicitly demonstrate failure, strengthening the positive claim.
- A discussion of how the proposed framework relates to VC-dimension, Rademacher complexity, or other formal measures of generalization would add depth.

## Novel Insights

- The paper offers a clean reconciliation of seemingly conflicting results in the programmatic RL literature: programmatic policies do not inherently generalize better, but they can when neural networks lack the expressive capacity for instance-scaled working memory. The key insight is that much of the prior empirical advantage was an artifact of poorly tuned neural training, not a representational superiority. The formal separation of expressivity and discoverability as independent bottlenecks is a useful conceptual contribution, even if not fully operationalized.

## Suggestions

- Explicitly test neural baselines (feedforward, LSTM, Transformer) on a problem where wall-following is impossible (e.g., the proposed SparseMaze) to empirically show that they cannot generalize OOD due to fixed memory. The paper currently relies on theoretical reasoning, but an experiment would greatly strengthen the main claim.
- Discuss how programmatic RL methods (e.g., LEAPS, NDPS) might be extended to learn memory-scalable policies more generally, rather than relying on an external LLM-based synthesizer.

## Score and Decision

The paper provides a valuable re-evaluation that clarifies important confounds in the literature and offers a theoretically sound framework for when programmatic representations have a genuine advantage. However, the main positive contribution—the memory-scaling advantage—is supported only by a narrow proof-of-concept rather than a full empirical demonstration within standard programmatic RL pipelines. This limits the paper’s impact and leaves its central positive claim incompletely validated. I recommend borderline acceptance; the re-evaluation alone is strong, but the evidence for the new insight is too thin to warrant a higher score.

MY FINAL SCORE: <score>6</score>  
MY FINAL DECISION: <decision>Accept</decision>