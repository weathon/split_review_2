## Summary
This paper introduces TTT-SCL (Test-Time Training for Supervised Causal Learning), a framework that addresses out-of-distribution generalization challenges in supervised causal learning by dynamically generating training data aligned to each test instance. The authors first demonstrate three fundamental limitations of static SCL pre-training—fragility to distribution shifts, failure in compositional generalization, and poor synthetic-to-real transfer—then propose TACTIC as a concrete instantiation using stochastic graph refinement with an Alignment of Distribution (AD) metric and sparsity constraints. Results on synthetic, pseudo-real (SynTREn), and real-world (Sachs) datasets show significant improvements over traditional causal discovery methods and the pre-trained AVICI SCL model.

## Strengths
- **Novel compositional generalization diagnosis (Issue 2)**: The "Component-mixed" training setup (Section 3.1) trains on all individual components but tests on unseen combinations. The data shows consistent AUROC drops from "i.i.d" to "Component-mixed" across all six test settings (e.g., RFF.G.97.8: 100→91, Chebyshev.G.62.3: 93→83). This finding—that SCL models memorize configurations rather than learning modular representations—is a genuinely distinct contribution beyond prior OOD analyses.
- **Two-stage improvement distinguishing TACTIC from score-based methods**: Table 4 demonstrates that the final SCL output (91.8 on RFF, 83.0 on Chebyshev, 78.9 on Sachs) consistently outperforms both the seed graph and the highest-score graph found during search, providing concrete evidence that supervised learning on generated training data adds value beyond score-based optimization.
- **Strong real-world and pseudo-real performance**: Table 2 shows TACTIC (Notears) achieves AUROC 78.9 on Sachs vs. 62.3 for AVICI (scm-v0) and 80.1 on SynTREn vs. 65.4 for AVICI—substantial gains on datasets where static pre-training collapses.
- **Both AD and sparsity validated as necessary**: Table 3 shows removing sparsity causes consistent drops (Chebyshev.G: 83.0→69.7, Sachs: 78.9→63.5), confirming both components are indispensable.
- **Robustness of framework even with random initialization**: TACTIC (random) outperforms AVICI on Linear_U (82.3 vs 75.6) and SynTREn (72.0 vs 65.4), suggesting the core approach is not merely dependent on a good seed graph.

## Weaknesses

### Fatal
None

### Major
- **Fixed Gaussian noise in forward sampling contradicts the paper's own framework**: Section 3 identifies noise distribution as one of three dimensions along which distribution shifts degrade SCL performance. Section 3.1 specifies that Linear_U uses Uniform noise for identifiability. Yet Section 4.2 Stage 3 states: *"We set the noise distribution to a standard Gaussian distribution N(0,1) by default."* This means TACTIC generates Gaussian-noise training data when the test data uses Uniform noise—a distribution mismatch the framework is explicitly designed to avoid. The paper provides no ablation comparing matched vs. mismatched noise distributions. This is an internal inconsistency that the authors should address, though it does not invalidate the empirical results which are strong even under this simplification.

### Minor
- **SIM regression function class underspecified in main text**: The entire TACTIC pipeline depends on the SIM procedure for mechanism regression (Eq. 3), but the main text does not specify what function class is used, deferring to Appendix A. For a load-bearing component—the bridge between graph hypotheses and data quality—the main text should at least name the function class and briefly discuss its implications for AD quality and computational cost.
- **Relationship to score-based causal discovery could be analyzed more deeply**: The AD metric (Eq. 3) resembles a marginal-likelihood score and the stochastic refinement is structurally similar to MCMC over DAG space. Table 4 shows the SCL model improves upon the highest-score graph (Sachs: 66.6→78.9), but the paper does not analyze *why*—whether the SCL model corrects systematic biases in AD, leverages transformer inductive biases, or learns something else entirely. This analysis would strengthen the core claim that TTT-SCL is a principled new framework.
- **λ hyperparameter sensitivity not reported**: The sparsity weight λ in Eq. 5 has no principled default, yet no sensitivity analysis is provided. For a test-time method without ground truth labels, this is a practical concern.
- **Computational cost not discussed in main text**: TACTIC trains an SCL model from scratch per test instance (K=200 generated graphs + model training), while baselines like AVICI need only a single forward pass. Complexity analysis is deferred to Appendix F, but a brief discussion in the main text would help assess practical viability.

### Trivial
None

## Nice-to-Haves
- An experiment at larger scale (d > 20) to confirm DAG search tractability at higher dimensions
- Analysis probing where the SCL model's predictions differ from the highest-score graph to illuminate *what* the model learns
- Report standard deviations for Sachs and SynTREn results

## Removed Points
These points are flagged to be removed, treat them with caution:
- **SIM underspecification as "fatal" or "structural" flaw**: The harsh critic framed this as a methodological gap that prevents assessing whether AD measures what it claims. However, the paper explicitly references Appendix A for implementation details, which exists in the original submission (parser strips appendices). Demoted to Minor.
- **Missing appendices concerns**: All appendix-related concerns (A through G) are parser artifacts—these sections exist in the original submission.

## Novel Insights
The paper's identification of compositional generalization failure in SCL (Issue 2) is a genuinely novel finding. Prior work (Montagna et al., 2024) attributed SCL failures to unseen individual components; this paper shows models fail even on novel *combinations* of seen components, revealing that SCL memorizes (G, f, ε) configurations rather than learning modular causal representations. This insight motivates the shift from diversity-seeking pre-training to test-time concentration, and represents a meaningful conceptual advance. The stage-wise analysis (Table 4) also provides an important empirical insight: score-based search and supervised learning are complementary, with the SCL model consistently adding value beyond the highest-score graph.

## Suggestions
- Add an ablation comparing matched vs. mismatched noise distributions in forward sampling (Stage 3) to directly address the Gaussian noise simplification
- Specify the SIM regression function class in the main text and briefly discuss its properties
- Include a brief sensitivity analysis for λ in the main text
- Discuss computational cost implications in the main text, even briefly
- Analyze what the SCL model learns beyond the highest-score graph (e.g., probing where predictions differ)

## Calibration Anchors
**All anchors retrieved across rounds:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Uj0h13lVrR.md | 1.00 | 1 | GFlowNets paper, irrelevant topic, strong reject |
| nSDOkm0SKo.md | 1.00 | 1 | Financial analysis, irrelevant |
| 5lUdTogEL3.md | 1.00 | 1 | Person re-identification, irrelevant |
| AvXrppAS2o.md | 3.00 | 1 | Causal structure for outcome prediction; weaker methodology, marginal improvements |
| MVpvyeVeyI.md | 3.40 | 1 | Causal Bayesian Optimization; high reviewer variance |
| JzFLBOFMZ2.md | 3.20 | 1 | Causal Structure Learning with LLMs; weak contribution |
| 4LiegvCeQD.md | 2.50 | 1 | Test-time adaptation IEL; limited scope |
| lQYi2zeDyh.md | 5.00 | 1 | Demystifying amortized causal discovery; similar topic but limited to bivariate |
| 8GhwePP7vA.md | 4.25 | 1 | Feature Matching Intervention; strong assumptions, unclear experiments |
| 7f5hNhzVAe.md | 4.00 | 1 | Causal Invariant BNNs; limited experiments |
| Gp6VU0oJX3.md | 3.67 | 1 | Causal framework for OSDA; theoretical only |
| 22ywev7zMt.md | 5.67 | 1 | OOD of SSL; limited to SSL setting |
| zwMfg9PfPs.md | 6.75 | 1 | Out-of-Variable Generalisation; novel OOV problem, good theory, Accept |
| x3F8oPxKV2.md | 6.25 | 1 | Zero-Shot Learning of Causal Models; strong assumptions, Reject |
| tlH4vDii0E.md | 5.60 | 1 | Fine-Tuning PLMs for Causal RL; different focus |
| xByvdb3DCm.md | 8.00 | 1 | Selection meets Intervention; very strong theoretical contribution |
| 3cuJwmPxXj.md | 8.00 | 1 | Identifying Representations for Intervention Extrapolation; strong theory |
| TPZRq4FALB.md | 8.00 | 1 | Test-time Adaptation multi-modal; very strong |
| hrqNOxpItr.md | 8.00 | 1 | Cross-Entropy Invert DGP; very strong theory |
| iad1yyyGme.md | 6.75 | 2 | CausalTime benchmarking; Accept |
| wmV4cIbgl6.md | 7.33 | 2 | CausalRivers benchmarking; Accept |
| eeJz7eDWKO.md | 6.00 | 2 | Meta-Learning Bayesian Causal Discovery; solid but less novel, Accept |
| xqxG5WogN6.md | 5.67 | 2 | Distribution Shift-Aware Prediction Refinement; Reject |
| 5sU32OCxgZ.md | 6.00 | 2 | TTVD geometric TTA; Accept |
| 4wk2eOKGvh.md | 6.50 | 2 | Test-Time Ensemble; Accept |
| 9w3iw8wDuE.md | 7.00 | 2 | Entropy not Enough for TTA; Accept |

**Round 1 bracket: 5.5–7.5.** The paper is clearly above the 3.0–5.0 rejected papers (weak methodology, marginal contributions) and comparable to accepted papers at 6.0–7.0. It is below the 8.0 papers which had stronger theoretical depth.

**Round 2 narrowed bracket: 6.0–7.0.** The paper has more novelty than "Meta-Learning Bayesian Causal Discovery" (6.00) and "Zero-Shot Learning of Causal Models" (6.25, rejected). It's comparable to "Out-of-Variable Generalisation" (6.75) and "Entropy is not Enough for TTA" (7.00) in novelty and practical impact.

**Final score: 6.5.** The paper is above 6.0 due to its genuinely novel framework, strong real-world results, and compelling compositional generalization diagnosis. It is below 7.0 due to the noise inconsistency, SIM underspecification, and incomplete score-based method analysis. The contribution is solid and the weaknesses are fixable rather than fundamental.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>