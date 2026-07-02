## Summary

This paper proposes **Direct Optimal Action Learning (DOAL)**, a framework for efficient policy extraction from Q-value functions in offline RL. The key idea is to avoid backpropagation through iterative sampling chains (as required for diffusion/flow policies) by first computing a target action via a batch-normalized gradient step on the Q-function and then training the policy to imitate that target using a simple native behavior-cloning loss. The method is tested with Gaussian, flow, and diffusion policies across IQL, Q-learning, and regularized Q-learning value functions on OGBench and D4RL benchmarks, showing aggregated improvements over strong baselines while simplifying hyperparameter search.

## Strengths

- **Clean, insightful reinterpretation of BRAC gradients** – Proposition 1 shows that the BRAC policy gradient can be viewed as minimizing distance to a target action that combines the data action and a Q gradient term. This perspective elegantly motivates the DOAL framework and decouples target computation from the policy being trained.
- **Practical computational efficiency** – DOAL avoids costly backpropagation through iterative generative sampling chains. The runtime analysis (Figure 2) clearly shows that DOAL requires significantly fewer neural network calls than full BPTT alternatives, with memory usage also lower. This makes the method attractive for scaling generative policies.
- **Comprehensive empirical evaluation** – The paper tests DOAL with three different value functions (IQL, Q-learning, regularized Q-learning) and three policy classes (Gaussian, flow, diffusion) across 15 tasks from two benchmarks. This breadth strengthens the claim of versatility and provides controlled comparisons.
- **Addresses an important practical bottleneck** – The computational difficulty of training generative policies with Q-value gradients is a known issue in offline RL. DOAL offers a simple, principled solution that can be dropped into existing methods with minimal overhead.

## Weaknesses

### Fatal
None.

### Major

1. **Empirical gains are modest and task-dependent** – While aggregated totals on OGBench improve, many individual tasks show small or no improvement, and some (e.g., antmaze-large-navigate with IQL) even degrade. On D4RL with IQL, DOAL models perform no better than baselines; improvement only emerges with regularized Q-learning. This suggests that DOAL’s effectiveness depends heavily on the quality of the Q-function, and the claimed “effective and versatile” characterization is weaker than the paper implies.

2. **The “batch-normalizing optimizer” contribution is not convincingly distinguished from a simple scaling factor** – The paper shows that gradient norms are stable during training (Figure 3), which means one could equivalently use a fixed scalar multiplier instead of the batch-normalized form. The practical benefit of the batch-normalized formulation over a tuned linear scale is therefore unclear; both require per-environment tuning (δ still varies across tasks). The claim that it “facilitates hyperparameter search” is only partially supported (δ range is narrower than α, but not zero-shot).

3. **The analysis of MaxQ sampling hyperparameter (n_sample) is claimed as a key contribution but lacks direct empirical support in the main paper** – Proposition 3 (informal) argues that large n_sample leads to maximization bias. The paper states that tuning n_sample is crucial for strong baselines, yet no ablation or sensitivity plot for n_sample appears in the main text. Without such evidence, the claim remains an intuition rather than a verified result, and the strength of the baseline improvements cannot be fully attributed to this tuning.

### Minor

- The paper introduces many algorithmic variants (DIOL, DIFQL, DTrigFlow, ETrigFlow, MFQL, DMFQL, MFReBRAC, DMFReBRAC) without a clear summary table of their components. This makes it difficult to track the exact difference between methods.
- The “Importance of Tanh” discussion (Section 5.1) correctly notes that ReBRAC with tanh outperforms flow-based policies on D4RL, but this point is not followed up with any analysis or future work suggestion beyond a one-sentence remark.

### Trivial

- None.

## Nice-to-Haves

- Include an ablation study on the effect of n_sample for MaxQ sampling (even for a subset of tasks) to substantiate Proposition 3 and justify the hyperparameter tuning.
- Provide an ablation comparing DOAL with and without the batch-normalized gradient (i.e., using a fixed scalar step) to isolate the contribution of the normalization.
- Add a comparison with more recent methods that use gradient-based policy extraction for diffusion models (e.g., QGPO, DAC, FAC) to better contextualize DOAL’s performance.

## Novel Insights

Beyond its own contributions, the paper offers a perspective that reinterprets the BRAC policy gradient as a target-matching problem. This sheds light on why behavior-regularized actor-critic methods work and suggests that the gradient evaluated at the data point (DOAL) is a natural alternative to the gradient at the policy output (BRAC). The connection to target-propagation and related non-end-to-end training methods is a nice conceptual link that may inspire further work on decoupling policy optimization from generative model training.

## Suggestions

- Strengthen the empirical case for the MaxQ sampling analysis by including, at minimum, a table or plot showing how performance varies with n_sample for a few representative tasks.
- Consider adding a schematic or algorithm box that clearly specifies the actor loss for each combination of value function and policy type, to improve readability.
- Discuss potential failure modes: when the Q-gradient at data points is unreliable (e.g., due to sparse rewards or poor critic training), DOAL may distort the target action. The paper could offer guidance on detecting such cases.

## Score and Decision

**Score**: 6  
**Decision**: Borderline Accept

The paper introduces a practical and well-motivated idea that addresses a real bottleneck in offline RL with generative policies. The experimental evaluation is broad and the analysis is generally sound. However, the empirical gains are incremental and depend on critic quality, and some of the claimed contributions (batch-normalizing optimizer, MaxQ sampling importance) are not fully validated in the main paper. A score of 6 reflects a solid, above-average submission that would benefit the community but has room for improvement.

MY FINAL SCORE: <score>6.0</score>  
MY FINAL DECISION: <decision>Accept</decision>