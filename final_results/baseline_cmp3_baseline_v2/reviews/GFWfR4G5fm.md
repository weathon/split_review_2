## Summary

This paper identifies three fundamental limitations of static supervised causal learning (SCL)—fragility to distribution shifts, failure in compositional generalization, and a large gap between synthetic and real-world performance—and proposes a test-time training framework (TTT-SCL) to address them. The key idea is to dynamically generate a training set aligned with each test instance by searching over candidate graphs using an Alignment of Distribution (AD) metric combined with a sparsity constraint. The instantiation, TACTIC, performs stochastic graph refinement, generates synthetic training data from the refined graphs, and trains an SCL model at test time. Experiments on synthetic, pseudo-real, and real-world datasets show that TACTIC outperforms existing SCL and traditional causal discovery methods, especially under distribution shifts.

## Strengths

- **Well-motivated problem and clear diagnosis.** The paper convincingly demonstrates that static SCL pre-training suffers from severe out-of-distribution failures, including compositional generalization breakdown and poor transfer to real-world data. These experiments (Figure 2, Table 1) are systematic and expose a genuine limitation of the current SCL paradigm.
- **Novel framework and instantiation.** The TTT-SCL framework is a principled shift from static diversity to test-time concentration. The AD metric (likelihood-based) and sparsity constraint provide a tractable way to quantify graph–data alignment while enforcing causal minimality. TACTIC’s three-stage design (seed initialization, stochastic refinement, training data generation) is practical and well-justified.
- **Strong empirical results.** TACTIC achieves state-of-the-art or competitive AUROC on all tested datasets, including real-world Sachs and pseudo-real Syntren, where static SCL methods fail. The ablation study (Table 3) and stage-wise analysis (Table 4) cleanly isolate the contributions of sparsity and the supervised learning phase, respectively.
- **Reproducibility and thoroughness.** The paper uses open-source baselines (AVICI, PC, NOTEARS, etc.) and reports standard deviations. Additional metrics (AUPRC, F1, ACC) and backbone consistency (SiCL) are provided in the appendix, strengthening the claims.

## Weaknesses

### Major

- **Computational cost and scalability are not adequately addressed.** TACTIC requires training an SCL model from scratch at test time on 200 generated instances. The paper mentions complexity analysis in the appendix (not available in the main text) but does not report wall-clock time or discuss how the method scales to larger graphs (e.g., 50+ nodes). This is a critical practical concern for real-world adoption.
- **The AD metric’s ability to distinguish Markov equivalent graphs is unclear.** The likelihood-based AD may not differentiate between graphs in the same Markov equivalence class, yet the method aims to recover the full DAG. The sparsity constraint helps but does not guarantee identifiability beyond the assumptions (e.g., ANM, LiNGAM). The paper does not analyze how often TACTIC recovers the correct DAG versus a Markov equivalent one, nor does it report structural Hamming distance.
- **Dependence on the seed initialization.** TACTIC (Notears) consistently outperforms TACTIC (random), and on some datasets (e.g., Sachs) the random seed performs worse than several baselines. This suggests that the method’s success partly relies on a good initial graph from a traditional method, which may not always be available or reliable.

### Minor

- **Limited exploration of the AD metric design.** The paper uses a likelihood-based AD but mentions other possibilities in the appendix without empirical comparison. A study of alternative AD implementations would strengthen the framework’s generality.
- **Hyperparameter sensitivity is not discussed.** The balance parameter λ and the number of refinement iterations are fixed; no sensitivity analysis is provided. The choice of K=200 training graphs is also not justified.

### Trivial

- The paper occasionally uses “sem-v0” instead of “scm-v0” (Table 1), but this is a minor typo.

## Nice-to-Haves

- A runtime comparison with baselines (especially AVICI, which is a single forward pass) would help contextualize the trade-off between accuracy and computation.
- An analysis of how the quality of the seed graph (e.g., from PC vs. NOTEARS) affects TACTIC’s final performance would be informative.
- Discussion of potential failure cases (e.g., when the true graph is very dense or when the test data is high-dimensional) would improve the paper’s completeness.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Report wall-clock time for TACTIC on the tested datasets and discuss scalability to larger graphs (e.g., 50–100 nodes).
- Include structural Hamming distance or SHD in the evaluation to clarify whether TACTIC recovers the exact DAG or only the Markov equivalence class.
- Perform a sensitivity analysis on λ and the number of refinement iterations, and provide guidance for setting these hyperparameters.

## Score and Decision

The paper makes a significant contribution by identifying a critical weakness in static SCL and proposing a novel, well-executed test-time training framework. The empirical results are strong and the ablations are informative. However, concerns about computational cost, scalability, and the AD metric’s identifiability properties prevent the paper from being a clear top-tier contribution. The work is solid and deserves acceptance.

MY FINAL SCORE: 7.5</score>
MY FINAL DECISION: Accept</decision>