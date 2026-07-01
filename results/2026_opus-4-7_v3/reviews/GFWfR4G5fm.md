Now let me read the key sections more carefully to verify specific claims about the acceptance ratio, noise assumption, and AD metric.Now I have thoroughly read the paper. Let me draft the review based on my verification of each claim.Now let me proceed to calibration. Round 1 — Bracketing:Let me read some of the most relevant anchor papers for comparison.Now I have sufficient information to calibrate. Let me form my initial bracket and write the final review.

**Round 1 Bracket Assessment:**

- The paper is clearly above the strong reject (< 1.5) and reject (1.5–3.5) bands.
- The most closely related anchor is `lQYi2zeDyh` ("Demystifying amortized causal discovery", avg 5.0), which also diagnoses OOD challenges in supervised causal discovery but is limited to bivariate cases and offers no practical solution. The reviewed paper goes further with a concrete method and strong real-data results.
- Compared to `x3F8oPxKV2` ("Zero-Shot Learning of Causal Models", avg 6.25, rejected), which required known graphs and had its own scalability issues, the reviewed paper has stronger practical motivation and better real-data results but weaker technical rigor.
- The paper lacks the theoretical depth and rigor of the 8.0 band papers (e.g., `xByvdb3DCm`, `3cuJwmPxXj`).

**Initial bracket: 4.5–6.0**

Now let me write the final consolidated review.## Summary
This paper diagnoses three OOD generalization failures of Supervised Causal Learning (SCL)—fragility to distribution shifts, compositional generalization failure, and synthetic-to-real divergence—and proposes TTT-SCL, a framework that dynamically generates test-instance-aligned training data at test time. The concrete instantiation TACTIC uses a penalized-likelihood score to guide stochastic graph refinement, producing customized SCL training sets. Experiments on synthetic, pseudo-real, and real-world data show TACTIC significantly outperforms both pre-trained SCL models and traditional methods on the most challenging benchmarks.

## Strengths

- **Systematic diagnosis of SCL failure modes (Section 3, Figure 2, Table 1).** The controlled experiments cleanly isolate three distinct failure patterns. The compositional generalization finding (Issue 2) is the most novel: AUROC drops of 3–11 points when individually-seen components are combined in new ways (e.g., Component-mixed vs. i.i.d. across all six synthetic settings in Figure 2). This goes beyond the obvious observation that OOD hurts and identifies a more structural limitation of static pre-training.

- **Stage-wise analysis (Table 4) provides strong evidence for the core claim.** The progression from seed graph (61.8 on Sachs) → highest-score search graph (66.6) → SCL output (78.9) demonstrates that the supervised learning step adds substantial value beyond the search itself. The 12.3 AUROC jump from best-search-graph to SCL output on Sachs is the paper's strongest evidence that training on the search trajectory provides something a naive score-based approach cannot.

- **Convincing real/pseudo-real data results.** TACTIC (Notears) achieves 78.9 AUROC on Sachs and 80.1 on SynTREN, meaningfully outperforming both pre-trained AVICI (62.3/65.4) and the best traditional method (PC at 67.1/RESIT at 64.6). This is exactly the gap the paper motivates—the synthetic-to-real transfer problem—and the results directly support the claimed contribution.

- **The TTT-SCL framework itself is a genuinely novel paradigm.** Reframing test-time training for causal discovery by using score-guided search trajectories as SCL training data—rather than selecting a single best graph—is a creative contribution that distinguishes this work from both static SCL and classical score-based methods.

## Weaknesses

### Fatal
None

### Major

- **MCMC acceptance ratio is mathematically ill-specified.** Figure 3 gives α = min[1, score(G_{k+1}, D_test) / score(G_k, D_test)], where score(G) = AD(G, D_test) − λ · Sparsity(G) is a log-likelihood minus an L₀ penalty (Equations 3, 5). This score can be negative (log-densities for continuous variables are often negative, and the penalty makes it more so). The ratio of two negative numbers inverts the ordering: e.g., if score(G_{k+1})=−5 and score(G_k)=−3, the ratio is 5/3 > 1, meaning worse graphs are always accepted. A standard Metropolis-Hastings formulation would use α = min[1, exp(score(G_{k+1}) − score(G_k))]. Since the method works empirically, the implementation may use the correct formulation, but the paper's description does not allow readers to reproduce or assess the chain's behavior.

- **Gaussian noise default contradicts the paper's own motivation.** Section 3 demonstrates that noise distribution shifts degrade SCL performance (Issue 1, Figure 2: "Noise shift" drops AUROC by 4–21 points across settings). Yet Section 4.2, Stage 3 states: "We set the noise distribution to a standard Gaussian distribution N(0,1) by default." The paper does not acknowledge or justify this tension. For real-world data like Sachs, the true noise distribution is unknown and unlikely to be standard Gaussian. If the method's success depends on the noise being approximately Gaussian, its applicability is narrower than claimed. The fact that TACTIC still performs well on Sachs suggests the noise assumption may not be critical in practice, but the paper owes the reader a discussion of why.

- **AD metric novelty is overclaimed.** Equation 3 computes the average conditional log-likelihood of each variable given its regressed parents; Equation 5 adds an L₀ sparsity penalty. This is functionally a penalized likelihood score—the conceptual basis of score-based causal discovery (BIC, GES, Bayesian structure learning) for decades. The paper frames AD as a novel contribution ("we propose...the Alignment of Distribution (AD) metric," line 148) when the likelihood-based implementation is standard. The paper does acknowledge on line 154 that "likelihood inherently combines both structure and mechanism aspects," which is precisely the insight motivating classical score-based methods. The genuinely novel element—using the search trajectory as SCL training data rather than selecting the highest-scoring graph—is undersold relative to the scoring component.

### Minor

- **Seed method dependency limits practical value on real data.** Table 2 shows TACTIC (random) scores 58.6 AUROC on Sachs, underperforming PC (67.1) by 8.5 points. The framework's strong real-data performance is entirely contingent on using NOTEARS as a seed. The paper acknowledges this ("TACTIC (Notears) variant consistently outperforms TACTIC (random)"), but does not sufficiently discuss the implication: when no good seed method exists—precisely the scenario where a pre-trained SCL model would be most needed—TACTIC may not help.

- **Experimental scale limited to d ≤ 20.** All experiments use 10–20 variables; the single real-world dataset (Sachs) has d=11. Score-based causal discovery and SCL methods are commonly evaluated on graphs with 50–100+ nodes. Even one experiment at larger scale would strengthen the paper's practical applicability claims. (The paper defers runtime analysis to Appendix F, which is reasonable, but the absence of any main-text experiment beyond d=20 is a gap.)

- **Missing ablation: ensemble averaging vs. SCL training.** Table 4 compares only the single highest-score graph to the final SCL output. The paper's core differentiator from classical score-based methods is that training an SCL model on the search trajectory outperforms selecting the best graph. A more complete ablation would compare against majority voting or Bayesian model averaging over all K=200 search graphs, which would isolate whether the SCL training step provides value beyond simple model aggregation.

- **Compositional generalization claim ("fundamental failure") is overstated for some settings.** While Issue 2 is a genuine finding, the Component-mixed drops in Figure 2 range from 3 points (Linear_U_62.3: 92→89) to 11 points (Linear_U_97.8: 100→89). The smaller drops weaken the characterization as a "fundamental" limitation—this is more accurately a meaningful but modest degradation that varies by setting.

### Trivial
None

## Nice-to-Haves

- An experiment varying the noise assumption (e.g., fitting the noise distribution from residuals, or using non-Gaussian noise) would either demonstrate robustness to this choice or identify a concrete improvement opportunity.
- The paper should explicitly position its scoring and search components within the score-based Bayesian structure learning literature (e.g., Madigan & York 1995, Friedman & Koller 2003) and elevate the stage-wise analysis (Table 4) from an ablation to a central result with a principled explanation of why SCL on nearby graphs outperforms the single best graph (e.g., implicit model averaging, regularization from training-time variation).
- One scalability experiment at d=50 or d=100 would substantially address scope concerns.
- The "Strengthening" suggestion from the reviewer to provide ensemble-averaging baselines deserves attention as a minor nice-to-have ablation.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **"Theoretical results" claim unsupported in main text.** The reviewer noted the conclusion claims "theoretical and empirical results" but no theorems appear in the main body. Removed because theoretical results likely exist in the appendix (stripped by parser). The paper also references "theoretical results confirm that finding the exact G_test is essentially impossible" (line 170), which may point to appendix content.

- **Computational cost unaddressed.** The paper explicitly states "Complexity analysis and runtime variation with the number of nodes are detailed in Appendix F" (line 176). This is appropriately deferred appendix content, not a missing analysis.

- **MCMC convergence guarantees.** The further concern about the chain's theoretical convergence properties (beyond the specification error) demands analysis not standard for empirical methods papers. Demoted from the main review.

- **Component-mixed construction details unclear.** The reviewer wanted more detail on which combinations were excluded. The paper's description (line 94) is reasonably clear: training "contains all individual components seen in isolation during training, but crucially excludes the specific combinations present in the test instances."

## Novel Insights

The paper's central insight—that using a score-guided graph search trajectory as *training data for an SCL model* systematically outperforms both static pre-training and direct score-based selection—is genuinely novel and well-supported by Table 4. This reframes the search-learning interface: rather than using search to find the best graph, search generates a neighborhood of plausible graphs that, when used as training data, enables the SCL model to learn more accurate causal relationships than any individual graph in the trajectory. The compositional generalization failure diagnosis (Issue 2) is also a valuable contribution that advances understanding of SCL's limitations beyond the more obvious single-dimension OOD sensitivity.

## Suggestions

1. **Fix the MCMC acceptance ratio specification** to use exp(score difference) or clarify the actual implementation if it differs from Figure 3. This is the most straightforward fix and addresses a core reproducibility concern.
2. **Explicitly discuss the tension** between diagnosing noise shift as a problem (Section 3) and defaulting to Gaussian noise in training data generation (Section 4.2). Even a brief argument for why mechanism alignment dominates noise alignment would suffice.
3. **Reposition the AD metric** within the score-based causal discovery literature and sharpen the novelty claim around the TTT-SCL framework and the trajectory-as-training-data insight rather than the scoring metric itself.
4. **Add an ensemble-averaging ablation** (majority voting or averaging over search trajectory) to isolate the SCL training step's contribution more cleanly.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Demystifying amortized causal discovery | lQYi2zeDyh | 5.00 | R1 | Most closely related: also diagnoses OOD challenges in supervised causal discovery, but limited to bivariate and offers no solution—reviewed paper is stronger. |
| Zero-Shot Learning of Causal Models | x3F8oPxKV2 | 6.25 | R1 | Also amortized causal learning; requires known graphs (stronger assumptions), methodologically cleaner but less practical—reviewed paper has stronger real-data contribution but weaker technical rigor. |
| Causal Structure Learning Supervised by LLM | JzFLBOFMZ2 | 3.20 | R1 | Informal math, poor organization, unclear contributions—reviewed paper is substantially stronger. |
| Best of both worlds: causal structure learning | AvXrppAS2o | 3.00 | R1 | Marginal improvements, weak baselines, confusing contributions—reviewed paper clearly stronger. |
| Predicting perturbation targets | cbFqqtJGtA | 4.25 | R1 | Different problem; limited practical contribution—reviewed paper has clearer impact. |
| Efficient differentiable causal order | G19piTjVYA | 4.00 | R1 | Score-based causal order; limited novelty—reviewed paper more novel. |
| Learning Latent SCMs | 0sO2euxhUQ | 4.00 | R1 | Different scope (latent variables); both limited in scale—reviewed paper has stronger empirical contribution. |
| Selection meets Intervention | xByvdb3DCm | 8.00 | R1 | Strong theoretical contribution with broad impact—reviewed paper falls well short of this quality level. |
| Identifying Representations for Intervention Extrapolation | 3cuJwmPxXj | 8.00 | R1 | Strong identifiability theory—reviewed paper doesn't approach this rigor. |
| Cross-Entropy Inverts Data Generating Process | hrqNOxpItr | 8.00 | R1 | Deep theoretical insight—reviewed paper is primarily empirical and less rigorous. |
| Root Cause Analysis via Granger Causal Discovery | k38Th3x4d9 | 8.00 | R1 | Comprehensive method with strong evaluation—reviewed paper is more limited. |
| D³PM Diffusion for Causal Discovery | TRHyAnInUC | 3.25 | R1 | Novel idea but execution issues; similar quality tier to lower end—reviewed paper stronger. |
| Causal Bayesian Optimization | MVpvyeVeyI | 3.40 | R1 | Different problem; mixed reviews—reviewed paper has clearer contribution. |
| Neural Causal Graph | nmvmPIi185 | 6.25 | R1 | Interpretable classification with causal reasoning; different scope—similar quality tier. |
| Robust causal/anticausal detection | Q0s6kgrUMr | 6.67 | R1 | Robust method with theoretical backing—reviewed paper is weaker theoretically. |
| Robust agents learn causal models | pOoKI3ouv1 | 5.75 | R1 | Theoretical contribution about causal models and robustness; different scope—similar quality tier. |
| KL Divergence for Stochastic GFlowNets | Uj0h13lVrR | 1.00 | R1 | Fundamentally flawed—reviewed paper far stronger. |
| Financial Markets Neural Network | nSDOkm0SKo | 1.00 | R1 | Toy/hypothetical work—reviewed paper far stronger. |
| IC-Light | u1cQYxRI1H | 0.50 | R1 | Score anomaly (actual score 10); unrelated topic. |
| Lifelong Person Re-ID | 5lUdTogEL3 | 1.00 | R1 | Unrelated; fundamentally flawed—reviewed paper far stronger. |

**Round 1 bracket: 4.5–6.0**

The paper sits above the clear reject band (papers like JzFLBOFMZ2 at 3.2 and AvXrppAS2o at 3.0 that have confused contributions and weak evaluation). It is stronger than lQYi2zeDyh (5.0), which diagnoses similar problems but is bivariate-only with no solution. However, it falls below x3F8oPxKV2 (6.25) in technical rigor, and well below the 8.0 papers which have strong theoretical grounding.

**Final calibration:** The paper has a genuine novel framework (TTT-SCL) with strong real-data results that directly support its claims. This pushes it above 5.0. However, the accumulation of methodological issues—mathematically ill-specified MCMC ratio, internal contradiction on noise assumptions, overclaimed novelty of AD—keeps it from reaching a confident borderline accept. The seed dependency and limited scale (d≤20) are additional concerns. The paper lands between the 5.0 anchor (lQYi2zeDyh, which offered diagnosis without solution) and the 6.25 anchor (x3F8oPxKV2, which had cleaner methodology). I place it at **5.5**: a paper with genuine contributions that would benefit from a revision addressing the methodological specification issues and framing before acceptance.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>