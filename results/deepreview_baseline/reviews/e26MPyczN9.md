## Summary

This paper re-evaluates claims that programmatic policies generalize better than neural policies in reinforcement learning, showing that much of the reported advantage stems from experimental confounds (e.g., reward function design, observation sparsity) rather than representational differences. The authors introduce a framework distinguishing *expressivity* (whether a policy class contains a generalizing solution) from *discoverability* (whether the search algorithm can find it), and argue that for problems requiring instance-scaling working memory (e.g., pathfinding, nested subproblems), programmatic representations provide a genuine advantage because fixed-capacity neural architectures cannot represent the required solutions. A proof-of-concept using FUNSEARCH synthesizes a BFS program that provably generalizes OOD.

## Strengths

- **Clear conceptual framework**: The expressivity/discoverability distinction provides a principled lens for understanding when representational differences matter for OOD generalization, moving beyond anecdotal comparisons.
- **Rigorous re-evaluation**: The paper systematically revisits three influential benchmarks (TORCS, KAREL, PARKING) and identifies specific confounds (reward shaping, observation sparsity) that explain prior reported gaps, with careful experimental controls.
- **Novel insight about memory scaling**: The identification of problems requiring instance-growing working memory as a fundamental limitation of fixed-capacity neural architectures is well-motivated and connects to theoretical results about neural network limitations.
- **Proof-of-concept demonstration**: The FUNSEARCH experiment showing synthesis of BFS for a wall-sparse maze provides concrete evidence that programmatic representations can provably generalize where neural policies cannot.

## Weaknesses

### Fatal
None.

### Major
- **Limited scope of the positive claim**: The paper convincingly shows that programmatic representations can express solutions requiring instance-scaling memory, but the proof-of-concept uses FUNSEARCH with a large language model (Qwen 3-Coder 30B) rather than the program synthesis methods (NDPS, LEAPS, PSM) studied in the re-evaluation. It remains unclear whether the specific programmatic policy search methods from prior work can reliably discover such solutions in practice.
- **PARKING results are inconclusive**: The PARKING experiments show that neither representation generalizes reliably, which undermines the paper's ability to draw strong conclusions about when programmatic representations help. The authors acknowledge this but then use it to motivate their theoretical analysis, creating a gap between the empirical re-evaluation and the positive contribution.
- **Theoretical claims about neural limitations need qualification**: The paper states that feedforward and recurrent policies "cannot encode a solution" to problems requiring instance-scaling memory, but this conflates practical failure with theoretical impossibility. Recurrent networks are Turing-complete in principle, and the paper's own discussion acknowledges that LSTMs can approximate finite-state machines. The argument would be stronger if it explicitly addressed the distinction between theoretical expressivity and practical discoverability for neural architectures.

### Minor
- **The KAREL experiments with $a_{t-1}$ augmentation are interesting but the mechanism is not fully explained**: Why does adding the last action to the observation enable generalization? The paper suggests it helps with partial observability, but a more detailed analysis of what information this provides would strengthen the contribution.
- **The TORCS reward modification changes the learning problem**: While the authors argue this is an "intrinsic reward" that doesn't change the evaluation problem, modifying the reward function during training does change what the agent optimizes, and it's not obvious that this is a fair comparison to the original NDPS results.

### Trivial
- The paper could benefit from a table summarizing which experimental confounds were identified for each benchmark.

## Nice-to-Haves

- An analysis of whether the specific program synthesis methods (NDPS, LEAPS, PSM) could discover the BFS solution for the wall-sparse maze, not just FUNSEARCH.
- A discussion of how the expressivity/discoverability framework relates to other known challenges in OOD generalization, such as distribution shift in observations or reward misspecification.
- Empirical evaluation on a domain with nested subproblems (e.g., a simplified NetHack variant) to directly test the claim about stack-like memory requirements.

## Novel Insights

The paper's key insight is that the OOD generalization advantage of programmatic policies in prior work was largely an artifact of experimental design rather than representation, but that there exists a genuine class of problems—those requiring instance-scaling working memory—where programmatic representations have a fundamental advantage. This reframes the debate from "which representation is better?" to "which problems require which representational capacity?" The expressivity/discoverability distinction is a useful conceptual tool for this reframing, though the paper's empirical support for the positive claim (programmatic advantage) is weaker than its support for the negative claim (prior results were confounded).

## Suggestions

- Strengthen the positive contribution by either (a) demonstrating that the specific program synthesis methods from prior work can discover the BFS solution for the wall-sparse maze, or (b) providing a more thorough theoretical characterization of when neural architectures provably cannot represent solutions requiring instance-scaling memory.
- Consider adding a simple domain with nested subproblems (e.g., a two-level subtask environment) where the memory limitation can be empirically demonstrated for neural policies and overcome by programmatic ones.

## Score and Decision

The paper makes a valuable contribution by carefully re-evaluating prior claims and providing a clear conceptual framework for understanding OOD generalization in RL. The re-evaluation experiments are well-designed and convincingly demonstrate that prior results were confounded. However, the positive contribution—showing when programmatic representations genuinely help—is less empirically supported, relying on a proof-of-concept with a different synthesis method than those studied. The paper is a solid contribution that advances understanding, but the gap between the negative and positive claims prevents it from being a definitive work.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>