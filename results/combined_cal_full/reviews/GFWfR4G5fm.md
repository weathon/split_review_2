Now I have all the calibration data I need. Let me produce the final consolidated review.

## Summary

This paper identifies three fundamental limitations of static supervised causal learning (SCL) — fragility to distribution shifts, failure in compositional generalization, and synthetic-to-real transfer gap — and proposes Test-Time Training for Supervised Causal Learning (TTT-SCL), a framework that dynamically generates training data distributionally aligned with each test instance. The paper instantiates this framework as TACTIC, which uses a novel Alignment of Distribution (AD) metric with sparsity constraints to guide stochastic graph refinement, generating targeted training data for each test instance. Experiments on synthetic (d=10), pseudo-real (Syntren, d=20), and real-world (Sachs, d=11) benchmarks show that TACTIC outperforms existing SCL and traditional causal discovery methods, particularly in out-of-distribution settings.

## Strengths

- **Clear problem diagnosis (Section 3).** The paper's systematic identification of three failure modes of static SCL pre-training — distribution shift fragility, compositional generalization failure, and synthetic-to-real transfer gap — is well-supported by controlled experiments. The separation of shifts by dimension (graph, mechanism, noise) in Figure 2 provides an actionable decomposition. This is the paper's most robust contribution, with weight +5.11 from the trained scoring model, indicating it strongly supports acceptance.

- **Stage-wise analysis (Table 4) cleanly demonstrates the pipeline's value.** The decomposition into seed → highest-scoring search graph → final SCL output shows that the SCL training phase adds significant value beyond what score-based search alone achieves, directly answering the question of why one would not simply stop at the best-scoring graph (weight +4.57).

- **Ablation of sparsity (Table 3) provides clear evidence of necessity.** The consistent performance drop when λ=0 confirms that the sparsity constraint prevents degenerate dense solutions and is not merely decorative (weight +4.15).

- **Evaluation includes real-world and pseudo-real data.** Going beyond purely synthetic evaluation (common in prior SCL work), the paper tests on the Sachs protein-signaling dataset and SynTReN-generated gene regulatory data. This strengthens the practical relevance of the claims (weight +3.89).

- **The core TTT-SCL idea is well-motivated and coherent.** While test-time adaptation is not new in ML broadly, its application to SCL is novel, and the motivation follows naturally from the OOD diagnosis in Section 3.

## Weaknesses

### Fatal
None.

### Major
- **Narrow evaluation scale limits evidence for practical utility.** TACTIC is evaluated only on d=10 (synthetic), d=11 (Sachs), and d=20 (Syntren). AVICI (the SCL backbone) was trained on graphs with "up to 100 nodes," and many real causal discovery problems involve dozens or hundreds of variables. The stochastic graph refinement over a d×d adjacency space and the cost of training an SCL model per test instance both raise scalability concerns that are not addressed experimentally. The absence of at least a moderate-scale experiment (e.g., d=50 on synthetic data) is the single biggest gap for demonstrating practical applicability (weight -1.42).

- **The Gaussian noise assumption for training data generation is an unexamined design choice.** Section 4.2 states: "We set the noise distribution to a standard Gaussian distribution N(0,1) by default." This means that even when the test data has uniform noise (Linear_U), the generated training data uses Gaussian noise, creating a distribution mismatch within the TACTIC pipeline itself. The paper provides no ablation, sensitivity analysis, or justification for this choice. Given the paper's emphasis on distributional alignment, this blind spot is significant (weight -2.86).

### Minor
- **The compositional generalization claim (Issue 2) is somewhat overstated.** The paper describes SCL models as failing to "generalize compositionally" and "memorizing specific (G, f, ε) configurations." However, the AUROC drops in Figure 2 for the Component-mixed condition are modest in several cases (RFF_G_62.3: 90→86, Linear_U_62.3: 92→89, Linear_U_97.8: 100→89). The largest drops occur on Chebyshev_G (93→83, 100→90). This pattern is more consistent with partial compositional generalization that degrades for unfamiliar function classes, rather than a wholesale failure of compositionality. Tightening the language would improve accuracy.

- **Inconsistency in the search acceptance rule description.** The text (Section 4.2) says candidates are "accepted with probability proportional to its score," while Figure 3 shows a ratio-based rule: min[1, score(G_{k+1})/score(G_k)]. These are different descriptions. Moreover, using a ratio of scores directly requires scores to be positive, which is not guaranteed for log-likelihood-based scores with a subtracted sparsity penalty. The description needs clarification.

- **No standard deviations reported for TACTIC on Sachs and Syntren** in Table 2, unlike the synthetic results where standard deviations over multiple runs are provided. The paper should report variance over different random seeds of the TACTIC pipeline itself.

### Trivial
None.

## Nice-to-Haves
- Ablate the noise distribution choice (compare default Gaussian to test-matched noise distributions for Linear_U and other settings).
- Include runtime analysis (wall-clock time per test instance, broken down by pipeline component: initialization, search, data generation, SCL training).
- Compare against fine-tuned AVICI (starting from scm-v0 weights and adapting to TACTIC-generated data) to isolate whether the benefit comes from the data generation or the training protocol.
- Discuss how λ (the sparsity penalty weight) was selected and whether it is fixed across datasets or tuned per dataset.

## Removed Points
These points are flagged to be removed; treat them with caution.
- "AD metric and SCL training loop underspecified" (Critical Issue 1 from harsh input): Concerns about the regression function class used for AD and missing training hyperparameters. These details are deferred to the appendix (Appendix A for AD, training details in appendix), which was stripped by the parser. Per the hard rule, criticisms about content that the paper explicitly assigns to appendices are removed.
- "Computational cost not addressed" (critical issue framing): The paper explicitly states "Complexity analysis and runtime variation with the number of nodes are detailed in Appendix F" (stripped by parser). The remaining concern about no runtime in the main text is minor and subsumed by the Nice-to-Haves section.
- "Abstract/Introduction framing conflates issues": A subjective organizational preference with no substance.
- "Component-mixed composition details should be in main text": Deferred to Appendix B (stripped).
- "L0 norm vs BIC/MDL discussion missing": Interesting suggestion but not a core requirement for the paper's contribution.
- "No fine-tuned AVICI comparison": A useful extension but not a missing baseline; standard comparison is against the pre-trained model as-is.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add at least one experiment at a larger scale (d=50 on synthetic data) to demonstrate that TACTIC scales beyond d=20.
2. Add an ablation comparing the default Gaussian noise to noise distributions matched to the test data.
3. Clarify the acceptance rule — reconcile the text description with Figure 3, and address the sign/positivity issue for the score ratio.
4. Report per-instance wall-clock time with a breakdown by pipeline component.
5. Report standard deviations for all TACTIC results, including Sachs and Syntren, over multiple random seeds.

## Score and Decision

**Bracket analysis.** My draft's weighted items show heavy positive weights (+5.11, +4.57, +4.15, +3.89) from the problem diagnosis, stage-wise analysis, sparsity ablation, and real-world data evaluation. The negative weights are moderate (−2.86, −1.42) for the Gaussian noise design choice and narrow evaluation scale. The closest calibration anchor is **ZXs3pkmrRG.md** (5.50, TTT + SCL in interventional setting), which had a heavy −10.04 "limited novelty" negative that this paper does not share. The anchor **lQYi2zeDyh.md** (5.00, amortized causal discovery) had −4.40 to −6.30 negatives from incomplete validation. The anchors **x3F8oPxKV2.md** (6.25) and **eeJz7eDWKO.md** (6.00) — both with strong problem framing and empirical work but real limitations in evaluation scope — are the closest qualitative matches. This paper's weighted item profile is more positive than the 5.00–5.50 anchors (lacking their severe novelty or validation negatives) but has weaker scalability evidence than the 6.25 anchor. I therefore place it at **6.0** (borderline accept).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>