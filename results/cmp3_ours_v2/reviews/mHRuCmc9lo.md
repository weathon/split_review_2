Now let me compile the final review.

## Summary

This paper develops a minimax decision-making framework for acting on forecasts that satisfy partial (ℋ-calibration) guarantees. The central theoretical result is a sharp phase transition: once the test class ℋ includes the |𝒜| indicator functions defining decision calibration, the minimax-optimal robust policy collapses to the plug-in best response—no robustness adjustment is needed. The authors provide a duality-based characterization (Theorem 3.1) that unifies regimes from no-information to full calibration, and derive practical ℋ-classes that arise from standard training pipelines (squared-loss regression) and post-hoc recalibration. The paper is primarily theoretical, with illustrative experiments on two regression datasets.

## Strengths

1. **A sharp, non-obvious theoretical finding (Section 4, Theorems 4.1–4.2).** The core result—that decision calibration (a tractable condition with only |𝒜| test functions) suffices for the plug-in best response to be minimax-optimal—is genuinely surprising. One would naturally expect a smooth trade-off where richer ℋ classes gradually reduce conservatism. Instead, the paper proves a phase transition: the robust policy collapses to best response precisely at the decision-calibration threshold, and adding further tests does not change it. This is a crisp theoretical contribution that cleanly answers the motivating question.

2. **Clean duality framework (Theorem 3.1).** The characterization of the optimal robust policy via a finite-dimensional dual problem is elegant. It provides a unified lens that subsumes the full-calibration case (ℋ = all functions, q* = v), the no-information case (ℋ = ∅, q* = constant minimax), and all intermediate cases. The pointwise computability claim—evaluation at a given v reduces to two low-dimensional optimizations—is a practically meaningful property.

3. **Clear connection to and differentiation from prior work (Section 1.2).** The discussion of how the minimax guarantee strengthens the swap-regret guarantees of Zhao et al. (2021) and Noarov et al. (2023) is precise. The contrast with Rothblum & Yona (2023), who study approximate full calibration in the binary-outcome setting, correctly identifies the different regime this paper addresses (qualitatively weaker guarantees in high dimensions).

4. **Practical secondary contributions (Section 4.2).** Propositions 4.4 and 4.5 give usable ℋ classes that arise naturally from standard training pipelines (squared-loss regression, bin-wise post-hoc calibration) without requiring explicit calibration interventions. These extend the framework's applicability beyond settings where one can enforce decision calibration.

## Weaknesses

### Fatal
None.

### Major

1. **Experiments test a different ℋ-class than the headline theoretical claim.** The paper's most important result (Theorems 4.1–4.2) is that under *decision calibration*, the plug-in best response is minimax-optimal. Yet the experiments in Section 5 test ℋ = {h(v) = v} (self-orthogonality from squared-loss training, Proposition 4.4), which is *not* decision calibration. The experiments therefore evaluate the regime *below* the decision-calibration threshold, telling us nothing about whether the central theoretical result holds in practice. The paper scopes this honestly in the abstract and Section 5, but the disconnect remains: the experiments are tangential to the headline claim. Adding an experiment that enforces decision calibration (e.g., via post-processing as in Noarov et al. 2023) and verifying that the robust policy and plug-in best response coincide would directly substantiate the paper's central practical recommendation.

### Minor

2. **No statistical uncertainty in any experimental result.** Table 1 reports six point estimates per dataset with no standard errors, confidence intervals, or number of independent trials. The differences between plug-in and robust policies are small (e.g., 0.474 vs. 0.463 under i.i.d. for Bike Sharing). Without any measure of variability, the reader cannot assess whether these differences are signal or noise. A single train/calibration/test split with no repetition is insufficient to draw empirical conclusions, even for an illustrative experiment.

3. **Gap between exact theory and approximate experiments.** The theory assumes exact ℋ-calibration, but the experiments use a finite-sample MLP trained to an (approximate) stationary point of squared loss. The paper notes that the forecaster "approximately satisfies" ℋ-calibration (line 293) but does not quantify how approximation error degrades the guarantees. The gap is acknowledged but not addressed.

4. **Construction of adversarial test distributions is not described.** Section 5 reports results under "adversarial" distributions that respect the ℋ-calibration constraints, but the procedure for constructing these worst-case distributions is not given. This matters for reproducibility: without knowing how the adversarial distributions are implemented, the reader cannot verify or replicate the adversarial evaluation.

5. **Linearity assumption (Assumption 2.1) restricts scope more than briefly noted.** The framework assumes utilities are linear in the outcome distribution v. While the paper acknowledges this in Section 6 ("risk averse utilities...fall outside our framework"), the restriction excludes many high-stakes decision problems involving risk aversion or threshold-based utilities. The limitation is more substantial than a single sentence suggests, though it is clearly stated as an assumption up front.

### Trivial
None.

## Nice-to-Haves
- **Include at least one external baseline** in the experiments (e.g., constant minimax strategy, bin-wise recalibration policy from Proposition 4.5) to provide an external reference point for the magnitudes in Table 1.
- **Discuss finite-sample computational cost** of computing a_robust: how much calibration data is needed for reliable estimation of λ*, and how sensitive are the results to finite-sample error?
- **Sharpen the practical significance of Corollary 4.3** (simultaneous plug-in optimality) with a comment on how large the union of decision-calibration tests can grow across diverse downstream problems.
- **Provide a concrete example** illustrating the gap between swap-regret guarantees and minimax optimality, to strengthen the comparison in lines 167–177.

## Removed Points
These points from the input review were removed with brief justification:

1. "The proof is in the appendix (not visible), so I cannot verify it" — REMOVED per hard rule: parser strips appendix sections; they exist in the original submission.
2. "The paper defers formal approximate-calibration analysis to Appendix B" — REMOVED as a standalone point about missing appendix content; the core observation (gap between exact theory and approximate experiments) is preserved as Minor weakness #3 above.
3. "No baselines against existing approaches" — REMOVED per hard rule about unfair comparison asymmetry: the experiments are an internal comparison between robust and plug-in policies, which is the natural comparison. Adding external baselines is a nice-to-have, not a weakness.
4. Various section-by-section subjective presentation notes — REMOVED.

## Novel Insights
None beyond the paper's own contributions. The reviews do not surface an insight about the work that the paper itself does not already articulate.

## Suggestions
1. Add an experiment that enforces decision calibration (e.g., via post-processing) and verifies that a_robust and a_BR coincide, to directly substantiate Theorems 4.1–4.2.
2. Report means and standard deviations over at least 10 random train/calibration/test splits for Table 1.
3. Describe the procedure for constructing the adversarial test distributions.
4. Quantify the gap between exact and approximate ℋ-calibration in the experiments—e.g., measure the empirical moment violations on the calibration split.

---

## Calibration

**Round 1 bracket:** 5.5–7.5

**Anchor papers retrieved across all rounds:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| bEgDEyy2Yk (minimax path implementation) | 1.00 | R1 | Unrelated; weak applied paper — current paper much stronger |
| Uj0h13lVrR (GFlowNets) | 1.00 | R1 | Unrelated |
| nSDOkm0SKo (financial news) | 1.00 | R1 | Unrelated |
| lvHHWDJCcr (calibrated metric) | 3.40 | R1 | Weak calibration paper — current paper significantly stronger |
| ZBL26FX0FT (Socrates loss) | 3.00 | R1 | Calibration paper, more applied — current paper stronger theoretically |
| BjZP3fTlVg (LLM risk control) | 3.00 | R1 | More applied — current paper stronger |
| XM7INBbvwT (calibration affects humans) | 4.67 | R1 | HCI study, different paradigm — not directly comparable |
| aIIYzzGKZp (LLM calibration) | 4.25 | R1 | Empirical — current paper stronger theoretically |
| 5HpZZbgdeK (binary top-vs-all calibration) | 5.00 | R1 | Applied calibration method — current paper stronger |
| **X0epAjg0hd (reassessing calibration)** | **5.67** | R1, R2 | Theory + weak experiments (1 dataset). Similar weakness profile, but current paper has more novel theory (sharp transition) |
| MUWkqH6e7d (human expertise + calibration) | 5.75 | R2 | Applied — current paper stronger theoretically |
| MxHgnYbxly (temp scaling + conformal) | 5.67 | R2 | Applied — less novel theory |
| dNunnVB4W6 (calibrating expressions) | 6.25 | R2 | Good applied paper — current paper's theory contribution is more fundamental |
| **uuPkll6i7m (certified calibration)** | **6.75** | R1, R2 | Strong theory + experiments validating theory. Current paper's experiments are weaker by comparison |
| **iOMnn1hSBO (decision-focused UQ)** | **6.80** | R1 | Good theory + experiments, bridges prediction and decisions. Current paper's theory is more novel |
| **dIkpHooa2D (MixMax, DRO)** | **6.75** | R2 | Minimax theory + experiments validating it. Similar minimax flavor. Current paper's sharp transition result is more distinctive |
| r5IXBlTCGc (LLM consistency checks) | 7.25 | R1 | Different domain, strong empirical work |
| **TId1SHe8JG (higher-order calibration)** | **7.50** | R1, R2 | Strong theory + experiments that validate theory. Current paper's experiments are substantially weaker |
| A3YUPeJTNR (prediction timing) | 8.00 | R1 | Strong theory + practical results, different topic |
| stUKwWBuBm (multi-agent RL) | 8.00 | R1 | Strong theory + experiments, different topic |
| rfdblE10qm (reward modeling) | 8.00 | R1 | Strong theory + experiments, different topic |

**Narrowing:** The paper's theory is stronger than the 5.67 anchor (X0epAjg0hd) but the experiments are substantially weaker than the 6.75–7.50 anchors (uuPkll6i7m, iOMnn1hSBO, TId1SHe8JG). In particular, the experiments in those papers directly validate their headline theoretical claims, whereas the current paper's experiments test a secondary case. The paper is a genuine theoretical contribution with weak illustrative experiments—positioning it above the 5.67 calibration paper but below the 6.75–7.50 papers where experiments substantiate the theory. Final score: **6.5**.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>