## Summary

This paper re-evaluates claims that programmatic policies generalize better than neural policies in reinforcement learning, showing that much of the reported advantage stems from experimental confounds rather than representational differences. Through controlled experiments on TORCS, Karel, and Parking benchmarks, the authors demonstrate that neural policies with appropriate modifications (cautious reward functions, sparse observations) can match or exceed programmatic policy generalization. The paper then identifies classes of problems where programmatic representations provide a genuine advantage—those requiring working memory that grows with input size—and provides a proof-of-concept using FUNSEARCH to synthesize breadth-first search for a modified Karel task.

## Strengths

- **Careful re-evaluation with strong experimental design**: The paper systematically identifies and addresses confounds in prior work. The TORCS experiment is particularly compelling—showing that the original reward function incentivized speed over generalization, and that a simple modification to the intrinsic reward (β=0.5) allows neural policies to match programmatic ones. The authors trained 30 seeds for G-TRACK-1 and 15 for AALBORG, providing statistical robustness.

- **Clear conceptual framework**: The expressivity/discoverability distinction (Definitions 2 and 3) provides a principled way to analyze why different representations succeed or fail at OOD generalization. This framework is well-motivated by the experimental results and helps explain why prior work found advantages that were not fundamental.

- **Identifies a genuine limitation of neural architectures**: The paper correctly identifies that fixed-capacity neural networks cannot represent solutions requiring instance-scaling memory (e.g., breadth-first search for pathfinding, stack-based algorithms for nested subproblems). This is a theoretically sound argument grounded in computational complexity, and the proof-of-concept with FUNSEARCH demonstrates the practical relevance.

- **Honest treatment of challenging cases**: The Parking results are presented transparently—neither representation reliably generalizes, and the authors acknowledge this rather than overclaiming. This intellectual honesty strengthens the paper's credibility.

## Weaknesses

### Fatal
None.

### Major

- **The proof-of-concept experiment is underdeveloped**: The FUNSEARCH experiment (Section 5) is described in a single paragraph with no quantitative results. How many runs succeeded? What was the success rate? What were the computational costs? The paper claims "Three runs of FUNSEARCH returned a correct implementation of breadth-first search" but provides no details about the wall-sparse maze, the prompt engineering, or the evaluation protocol. This is the paper's central positive claim about programmatic advantages, yet it receives minimal empirical support.

- **The Karel "PPO with a_{t-1}" result may be less significant than claimed**: The paper shows that augmenting observations with the last action allows feedforward networks to match LEAPS on 100×100 grids for Stairclimber, Maze, TopOff, and FourCorner. However, these tasks can be solved by simple reactive strategies (e.g., wall-following) that don't require memory. The Harvester task, where PPO with a_{t-1} fails (0.04 success), is the one that might genuinely require memory, but the paper doesn't analyze why. The claim that "partial observability combined with a simpler model can generalize to larger grids" is true for these specific tasks but may not extend to tasks requiring genuine memory.

- **The paper conflates "neural networks" with specific architectures**: The claim that "commonly used neural architectures cannot encode a solution to this type of problem due to their fixed-capacity design" is true for feedforward and standard recurrent networks, but the paper acknowledges that memory-augmented neural models (stack-RNNs, neural Turing machines) could in principle address this. The paper dismisses these as "imperfect" without rigorous comparison. A stronger paper would either (a) show that these alternatives also fail empirically, or (b) acknowledge that the advantage is specific to certain neural architectures rather than neural representations broadly.

### Minor

- **The Parking analysis is incomplete**: The paper shows that PSM has better generalization gap (0.10 vs 0.68) but lower absolute test performance (0.16 vs 0.18). The authors don't resolve which metric is more meaningful or discuss the practical implications. The claim that Parking "points in the direction of benchmarks that could distinguish" representations is vague.

- **The discussion of related work (Section 6) is speculative**: The paper suggests that other works' results "may also be attributed to confounding factors" without providing evidence. This weakens the otherwise strong empirical contribution.

### Trivial
None.

## Nice-to-Haves

- A systematic comparison of different neural architectures (feedforward, LSTM, GRU, Transformer, memory-augmented) on a task requiring instance-scaling memory would strengthen the central claim.
- The paper could benefit from a formal definition of "working memory that grows with input size" in the context of POMDPs and policy classes.
- A discussion of how the expressivity/discoverability framework relates to the no-free-lunch theorems or PAC-learning theory would add theoretical depth.

## Novel Insights

The paper's key insight is that the reported OOD generalization advantages of programmatic policies in prior work are largely artifacts of uncontrolled experimental factors (reward design, observation sparsity) rather than fundamental representational differences. More importantly, the paper provides a principled framework for identifying when programmatic representations genuinely matter: when the solution requires working memory that scales with input size. This shifts the conversation from "programmatic vs. neural" to "what computational resources does the problem class require?"—a more productive framing for the field. The observation that simple modifications (adding last action to observations, cautious rewards) can close the generalization gap in standard benchmarks is practically valuable for practitioners.

## Suggestions

1. **Strengthen the proof-of-concept experiment**: Provide quantitative results for FUNSEARCH on the wall-sparse maze—number of successful runs, computational cost, comparison with neural baselines on the same task. Without this, the paper's positive claim about programmatic advantages remains unsubstantiated.

2. **Clarify the scope of the neural limitation claim**: Explicitly state which neural architectures are being compared (feedforward, LSTM, GRU) and acknowledge that memory-augmented neural models are a separate category that may address the limitation. Consider adding a small experiment with a stack-RNN or similar model on the wall-sparse maze.

3. **Add analysis of the Harvester task**: The PPO with a_{t-1} fails on Harvester (0.04 success on 100×100). Understanding why would strengthen the paper's analysis of when simple neural models succeed or fail.

4. **Resolve the Parking evaluation ambiguity**: Either argue for why the generalization gap metric is more meaningful than absolute test performance, or acknowledge that neither representation is satisfactory and discuss what this implies for benchmark design.

## Score and Decision

The paper makes a valuable contribution by carefully re-evaluating prior claims and providing a principled framework for understanding when programmatic representations offer genuine advantages. The experimental re-evaluation is thorough and convincing for the TORCS and Karel domains. However, the paper's central positive claim—that programmatic representations can solve problems requiring instance-scaling memory—is supported only by a minimal proof-of-concept with no quantitative results. This asymmetry between the strong negative results (showing neural policies can match programmatic ones) and the weak positive results (showing programmatic advantages) limits the paper's overall impact. The paper would be significantly stronger with a proper empirical evaluation of the wall-sparse maze task.

MY FINAL SCORE: 6.0</score>
MY FINAL DECISION: Accept</decision>