Here is my final consolidated review.

## Summary

This paper identifies three concrete failure modes of static supervised causal learning (SCL) — fragility to distribution shifts, failure in compositional generalization, and a synthetic-to-real generalization gap — and proposes Test-Time Training for SCL (TTT-SCL), a framework that dynamically generates training data distributionally aligned with each test instance. The authors instantiate this framework as TACTIC, which combines an alignment-of-distribution (AD) metric with sparsity constraints in a stochastic graph-refinement search, followed by SCL model training on the generated data. Experimental results on synthetic, pseudo-real (SynTReN), and real-world (Sachs) benchmarks show substantial improvements over both traditional causal discovery methods and the pre-trained SCL baseline AVICI.

## Strengths

- **Empirically grounded problem diagnosis (Section 3, Figure 2, Table 1).** The paper provides direct experimental evidence for all three claimed failure modes. The result that AVICI (scm-v0) drops from 97.8 AUROC on the in-distribution synthetic setting (RFF_G) to 62.3 on the real-world Sachs dataset is a striking demonstration of the synthetic-to-real generalization gap that the SCL community should take seriously. This diagnostic contribution has value independent of the proposed solution.

- **Well-motivated and coherent pipeline (Section 4, Table 4).** The TTT-SCL framing — dynamically generating customized training data at test time — is a natural response to the identified OOD failures. The three-stage pipeline (seed initialization → stochastic refinement → SCL training) is clearly described, and the stage-wise analysis in Table 4 convincingly separates the contribution of the graph search from that of the SCL training phase, showing that both stages add value.

- **Strong empirical results on challenging real-world data (Table 2).** On Sachs, TACTIC achieves 78.9 AUROC (vs. 67.1 for the best traditional method PC and 62.3 for AVICI); on SynTReN, it achieves 80.1 (vs. 65.4 for AVICI). These are substantial, practically meaningful improvements that cannot be dismissed as marginal.

- **Clean ablation validates the sparsity constraint (Table 3).** The consistent performance drop when removing the sparsity penalty (λ=0) across all five datasets confirms that AD alone is insufficient and that the L₀ constraint prevents degenerate dense solutions.

## Weaknesses

### Fatal
None.

### Major

1. **The SCL model training procedure at test time is critically underspecified in the main text.** The paper devotes a single sentence to Stage 3 (line 174): *"An SCL model is then trained on this set and applied to infer G_test."* This leaves fundamental questions unanswered: Is the SCL model trained from scratch on K=200 instances? If so, what architecture is used and how is it feasible given that AVICI was originally trained on millions of instances? Or is a pre-trained model fine-tuned — if so, which checkpoint serves as the starting point, and how is fine-tuning performed? The paper provides no optimization details (learning rate, batch size, number of training steps, loss function, hardware). Without this information, the reader cannot assess whether the method is computationally practical or even what the method *is* (training vs. fine-tuning are fundamentally different procedures). This gap directly affects reproducibility. *(Note: details may exist in the appendix, which is stripped by the parser; but the main text as presented is insufficient to understand the core method.)*

### Minor

2. **Missing standard deviations for real-world and pseudo-real results (Tables 2 and 3).** The table headers state "Results are presented as AUROC (standard deviation)," yet all entries for Sachs and SynTReN in Tables 2 and 3 are reported as bare numbers without variance estimates (e.g., TACTIC (Notears) at Sachs = 78.9, Syntren = 80.1; the ablation in Table 3 similarly lacks std for these columns). Since the synthetic columns include standard deviations, the inconsistency makes it impossible to assess the statistical significance of TACTIC's headline improvements on real-world data.

3. **The regression method for fitting mechanisms in the AD computation is not specified.** The paper states (line 146): *"given a candidate graph G_train^k, we regress the corresponding mechanisms from the observed D_test."* The choice of regressor (linear regression? Gaussian process? neural network?) directly determines the AD scores that drive the entire search procedure, yet it is not stated in the main text. (The paper references Appendix A for alternative AD implementations, but the specific regressor choice for the experiments is needed here.)

4. **The hyperparameter λ balancing AD and sparsity (Equation 5) is not discussed.** The paper defines λ as "a hyperparameter balancing the trade-off" (line 166) but provides no information about how it was chosen — was it tuned, cross-validated, or fixed across experiments? This matters because the sparsity constraint is critical to the method's success (Table 3), yet the strength of that constraint is controlled by an unexamined hyperparameter.

5. **The noise distribution mismatch between training data generation and test data is not discussed.** The paper states (line 174) that training data is forward-sampled with *"a standard Gaussian distribution N(0, 1) by default"* — even when the test data uses Uniform noise (e.g., Linear_U). The method achieves strong results despite this mismatch, which is interesting, but the paper neither discusses why the mismatch is tolerable nor analyzes the method's sensitivity to noise distribution misspecification.

6. **The compositional generalization failure claim (Issue 2) is slightly overstated relative to the evidence.** The drops from i.i.d. to Component-mixed in Figure 2 range from 3–11 AUROC points (e.g., Linear_U_97.8: 100→89, RFF_G_97.8: 100→91). While these are meaningful degradations, they are substantially less severe than the mechanism-shift drops (e.g., RFF_G_97.8: 100→42, Chebyshev_G_97.8: 100→57). The paper's narrative frames compositional generalization failure as a "fundamental limitation" on par with distribution shifts, but the evidence shows it is a secondary issue. This overclaiming inflates the perceived crisis that TTT-SCL is meant to solve.

7. **The graph-type dimension (ER vs. SF) is collapsed without explanation when reporting results.** The experiment setup in Section 3.1 defines six settings with explicit graph-type suffixes (RFF_G_ER, RFF_G_SF, etc.), but Figure 2 and Tables 1–2 use only mechanism+noise labels (RFF_G, Linear_U, Chebyshev_G) without clarifying whether results are averaged across ER and SF, and if so, how.

8. **The search sometimes degrades the seed before SCL recovers (Table 4).** On Linear_U, the seed graph achieves 82.0 AUROC but the highest-score graph drops to 80.1 — the score-based search made things worse before the SCL training rescued performance (86.3). This is an interesting phenomenon that the paper does not discuss or explain.

### Trivial
None.

## Nice-to-Haves

- A comparison against a baseline that trains an SCL model on K=200 *random* training instances (without AD alignment) would more sharply isolate the value of the AD-based data generation, rather than just the effect of having more training iterations at test time.
- A brief discussion of why the SCL training phase improves over the highest-scoring graph (i.e., the mechanism by which learning from imperfect graphs yields better results than the graphs themselves) would strengthen the paper's scientific contribution.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **Asymmetric comparison re: AVICI as a single fixed model (Issue 2b from harsh critic).** The criticism that comparing a per-instance customized model against a one-size-fits-all baseline inflates improvement is not a valid weakness: this comparison is the natural and appropriate baseline for evaluating the paper's core claim that per-instance customization helps. Removed.
- **Stage-wise analysis already acknowledged (Issue 2c).** The paper explicitly provides the stage-wise analysis in Table 4 and discusses it. The reviewer's concern that the headline comparisons embed the search advantage is already addressed by the paper's own ablation. Removed.
- **Diversity vs. concentration dichotomy oversimplified (Section 1 note).** This is a framing preference, not a substantive weakness. Removed.
- **Only PC and AVICI in Table 1.** Table 2 provides comprehensive baselines for the same datasets. The purpose of Table 1 is narrowly to illustrate the divergent generalization pattern, which it does. Removed.
- **Relationship between AD+sparsity search and score-based discovery (Issue 4).** The paper already provides Table 4 and explicitly discusses the two-stage distinction. The request for deeper analysis of *why* SCL helps is a reasonable nice-to-have but not a weakness. Removed.
- **Computational budget asymmetry (Issue 2a).** While TACTIC uses more computation, comparing methods with different computational profiles is standard in ML; the stage-wise analysis in Table 4 already separates the contribution of SCL training from the search. The concern about conflating "more computation" with "better method" is partially addressed by the paper's design. Removed (downgraded from original framing).
- **TACTIC vs. TTT-SCL conflation.** A minor framing issue without substantive consequence. Removed.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's review surfaced a useful framing concern about the compositional generalization claim being overstated relative to mechanism shift, and the practical specification gaps around the test-time training procedure. Neither reveals a fundamentally novel insight about the method or the problem that the paper itself does not already contain.

## Suggestions

- Specify in the main text whether the SCL model at test time is trained from scratch or fine-tuned from a pre-trained checkpoint. If fine-tuned, state which checkpoint is used and provide the fine-tuning protocol (learning rate, steps, batch size). If trained from scratch, explain how training on K=200 instances is sufficient and provide architecture details and training hyperparameters.
- Report standard deviations for all dataset columns in Tables 2 and 3, especially for Sachs and SynTReN where they are currently absent.
- Specify the regression method used to fit mechanisms for the AD computation, and describe how λ is set.
- Discuss the noise distribution mismatch (Gaussian training noise vs. potentially non-Gaussian test noise) and its implications.
- Tone down the claim that compositional generalization failure is a "fundamental limitation" of equal severity to distribution shifts, or clarify that the evidence primarily identifies mechanism shift as the dominant failure mode.

## Score and Decision

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>