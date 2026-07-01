Now I'll produce the final consolidated review.

## Summary

This paper identifies three fundamental limitations of static pre-training in Supervised Causal Learning (SCL)—fragility under distribution shifts, failure in compositional generalization, and a synthetic-to-real performance gap—and proposes Test-Time Training for SCL (TTT-SCL). The key idea is to dynamically generate training data aligned to each specific test instance. The authors introduce the Alignment of Distribution (AD) metric to quantify similarity between a candidate graph and test data, combine it with a sparsity constraint, and instantiate the framework as TACTIC, which performs stochastic graph refinement at test time to produce a customized training set. Experiments on synthetic, pseudo-real, and real-world data show TACTIC outperforming existing SCL methods and traditional causal discovery approaches.

## Strengths

1. **Well-designed diagnosis of SCL limitations (Section 3).** The paper systematically exposes that existing SCL methods fail under distribution shifts (graph, mechanism, noise), fail at compositional generalization (novel combinations of seen components), and fail to transfer from synthetic benchmarks to real data. The experimental setup in Figure 2 is well-constructed, and the results convincingly demonstrate these issues. This diagnosis is a valuable contribution independent of the proposed method.

2. **The core TTT-SCL idea is novel and principled.** Framing test-time training for SCL as a search over causal graphs guided by distributional alignment is a natural direction that prior SCL work has not pursued. The AD metric (Equation 3), connecting graph structure to observable data through likelihood, is a sensible operationalization. The sparsity constraint (Equation 4) correctly addresses the degeneracy of dense graph solutions.

3. **Strong empirical results on real and pseudo-real data.** TACTIC achieves substantial improvements on Sachs (78.9 AUROC vs. 67.1 for PC and 62.3 for AVICI) and Syntren (80.1 vs. 65.4 for AVICI). These are practically meaningful gains on the kind of data where existing SCL methods are weakest. The stage-wise analysis in Table 4 cleanly demonstrates that both the search phase and the SCL learning phase contribute to the final performance.

## Weaknesses

### Fatal
None.

### Major

1. **The score-based acceptance rule in the stochastic refinement is technically incorrect as specified (Section 4.2, Figure 3).** The paper defines the transition probability as `alpha = min[1, score(G_{k+1}, D_test) / score(G_k, D_test)]`. Since `AD(G, D_test) = (1/d) Σ_i log p(X_i | f_i^k)` (Equation 3), AD is an average log-likelihood and always ≤ 0. The combined score `AD − λ·Sparsity(G)` (Equation 5) is therefore also ≤ 0. When both scores are negative, the ratio is positive but the behavior is pathological: a better graph (less negative score) yields a ratio < 1, so it is accepted with probability less than 1, while a worse graph (more negative) yields a ratio > 1 and is always accepted. This is the opposite of the intended behavior. The standard Metropolis-Hastings correction would use `exp(score(G_{k+1}) − score(G_k))`. As written, readers cannot reproduce the search procedure correctly. — *Why it matters: this is the core optimization engine of the proposed method; a flawed acceptance rule undermines the method's description even if the empirical results are valid (the actual implementation may differ from the text).*

2. **Computational cost is enormous and its practicality is unclear.** TACTIC at test time must: run NOTEARS to obtain a seed graph, perform iterative stochastic graph refinement (with regressions and likelihood evaluations at each step), generate K=200 synthetic training datasets, and train an SCL neural network from scratch per test instance. The paper evaluates only on graphs with 10–20 variables and mentions complexity analysis in Appendix F (which is not accessible). For realistic causal discovery problems involving hundreds of variables, this pipeline would be computationally infeasible, and the paper provides no main-text discussion of wall-clock time, GPU hours, or scaling behavior. — *Why it matters: the paper claims TACTIC as a practical solution but provides no baseline for assessing whether the gains justify the cost.*

### Minor

3. **The comparison to static SCL baselines is asymmetric in an unacknowledged way.** AVICI (scm-v0) is a single fixed pre-trained model making one forward pass per instance. TACTIC invests substantial per-instance compute (seed estimation, search, data generation, and SCL training). The headline "TACTIC outperforms AVICI on real data" conflates the benefit of test-time adaptation with the massive additional compute budget. A compute-controlled comparison (e.g., fine-tuning AVICI on TACTIC-generated data, or using the same compute budget for baselines) would sharpen the contribution.

4. **The ablation study is thin (Section 4.4).** Only the sparsity term is ablated (λ=0). There are no ablations of: the AD term (e.g., using only sparsity), the number of training graphs K, the search procedure itself, or a comparison against a simple graph ensembling baseline (e.g., aggregating predictions from the top-k graphs). For a paper whose novelty depends on two components plus a multi-stage pipeline, more thorough ablation is expected.

5. **The paper does not specify how the K=200 training graphs are selected from the refinement chain.** Are they the last 200 graphs of the Markov chain? Every k-th graph? The top-200 by score? Each choice has different implications for diversity and quality, and the paper provides no guidance.

6. **Real-world evaluation is limited.** The paper evaluates on only one real-world dataset (Sachs, 11 variables). While bnlearn datasets are mentioned in Appendix G (not accessible), the main-text claim about "good performance on real-world datasets" rests on thin evidence.

7. **The AD likelihood computation is underspecified (Equation 3).** The paper does not state what noise distribution is assumed when computing `log p(X_i | f_i^k)`. Is it Gaussian with variance estimated from residuals? The same N(0,1) used for forward-sampling? Without this, the AD metric cannot be independently implemented.

8. **The hyperparameter λ is not reported or analyzed.** The value of λ, whether it was tuned, and how sensitive results are to it, are all absent. Since λ controls the critical sparsity-accuracy trade-off, this is necessary for reproducibility.

9. **Standard deviations are not reported for Sachs and Syntren in Tables 2 and 3**, making it impossible to assess the reliability of the headline results on real-world data.

### Trivial

- The three "fundamental limitations" are presented as distinct issues but are all manifestations of distribution mismatch between training and test data. This does not harm the contribution but inflates the framing.

- The notation "AVICI (sem-v0)" appears as "sem-v0" once (line 122) and "scm-v0" elsewhere — likely a typo.

## Nice-to-Haves

- A compute-controlled variant where the SCL model is fine-tuned (rather than trained from scratch) on TACTIC-generated data would help isolate the benefit of better training data from the benefit of more compute.
- Standard deviations for all three stages in Table 4 across multiple runs, with a significance test on the 2→3 improvement, would strengthen the paper's central claim about the value of the supervised learning phase.
- Reporting λ and its sensitivity, and specifying how K graphs are selected from the chain, would improve reproducibility.

## Removed Points

- **Missing related work on test-time adaptation for causal discovery**: Removed per policy (cannot verify existence of external work).
- **"Computational cost is unaddressed in the main text"**: The paper explicitly references Appendix F for complexity analysis; the main text does address it by pointer. Downgraded to Minor.
- **"SCL training details not specified"**: The paper references Appendix B for detailed configurations. Downgraded to Minor.
- **"Only one real-world dataset" as a fatal weakness**: The paper references Appendix G with bnlearn datasets. Kept as Minor.
- **"The three limitations are overstated"**: Kept as Trivial — a framing observation, not a substantive weakness.
- **"NOTEARS seed borrows strength from compared-against method"**: The paper acknowledges this, and TACTIC(random) variant partially addresses it. Kept as Minor observation in item 3's spirit.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a novel framing or connection that the paper itself missed.

## Suggestions

1. **Fix the acceptance rule.** Replace the score ratio in Figure 3 with the standard form `exp(score(G_{k+1}) − score(G_k))` or clarify if AD is used as a likelihood (not log-likelihood) in the acceptance computation.
2. **Add a computational cost table.** Report wall-clock time, GPU hours, and scaling with node count (at least up to 50–100 variables) in the main text.
3. **Deepen the ablation.** Add ablations of AD alone (no sparsity), varying K, varying the search strategy, and a simple ensemble baseline.
4. **Add a compute-controlled baseline.** Fine-tune AVICI on TACTIC-generated data to separate the benefit of better data from more computation.
5. **Specify all procedural details.** How are the K=200 graphs selected? What noise model is used for AD likelihood? What is λ?
6. **Report standard deviations** for Sachs and Syntren across multiple runs or cross-validation folds.

## Score and Decision

The paper addresses a genuine problem (SCL's distribution-shift vulnerability) with a well-motivated framework (test-time training). The diagnosis of SCL limitations is strong, and the empirical results on real-world data are impressive. However, the method description has a technical flaw in the acceptance rule specification, the computational demands are unaddressed in a way that obscures practicality, and several procedural details needed for reproducibility are missing. These are fixable issues, but they prevent the paper from standing as a clean contribution in its current form.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>