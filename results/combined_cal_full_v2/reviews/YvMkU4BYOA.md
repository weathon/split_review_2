## Summary

This paper introduces XBIC, a score-based causal discovery method for discrete Bayesian networks that augments the Bayesian Information Criterion (BIC) with Shapley-value-based directional evidence. For each variable, a classifier (XGBoost) is trained to predict that variable from all others, and TreeExplainer computes Shapley values that are aggregated into an edge-specific signal. This signal soft-weights BIC's complexity penalty: edges with strong attribution support are penalized less, while the method reverts to standard BIC when signal is weak. The paper evaluates on ten benchmark networks across seven sample-size regimes (700 runs).

## Strengths

- **A genuinely novel idea linking explainability and structure learning.** Using local feature attributions (Shapley values from per-node classifiers) to modulate the BIC penalty during score-based search is an original direction. Most work at the causality–XAI interface injects known causal structure into explanations; this paper reverses the flow. (Lines 19–23, 97–113.)

- **Broad and honest empirical evaluation.** Ten benchmark networks (6–76 nodes), seven sample-size regimes, 700 total runs, with multiple baselines. The paper reports both gains and cases where XBIC does not improve, and it surfaces the runtime comparison transparently (Table 5). The acknowledgment that the method defaults to BIC when the Shapley signal is weak (line 159, line 206) is intellectually honest.

- **The method preserves BIC when no directional signal exists.** The property that XBIC = BIC when w = 0 or SHAP(G) = 0 (line 113) is practically important: the method does not introduce spurious bias in the absence of evidence.

## Weaknesses

### Major

1. **Unsubstantiated central premise — no justification that Shapley values from non-causal predictive models carry directional information aligned with causal orientation.** The method computes Shapley values from classifiers that predict each variable Xᵢ from all others X\_\i. These classifiers capture *any* statistical dependence (correlation via confounders, mediators, reverse causation), not causally meaningful directional signal. The paper asserts (line 127) "intuitively, if |φ̄₁→₂| ≫ |φ̄₂→₁|, the edge X₁→X₂ has stronger directional support than X₂→X₁" but provides no theoretical justification or per-edge empirical validation for why this asymmetry should align with causal direction. Consider a chain X₁→X₂→X₃: when predicting X₂, both X₁ (cause) and X₃ (effect) can be predictive, and when predicting X₃, X₂ is predictive while X₁ is not (due to Markov property). This yields bidirectional Shapley signal on X₂–X₃ without a clear asymmetry, illustrating that the directional information may not systematically favor the correct orientation. Missing analysis includes: (a) no theoretical justification, (b) no per-edge analysis validating that edges where |φ̄ᵢ→ⱼ| > |φ̄ⱼ→ᵢ| align with true causal direction, and (c) no controlled synthetic experiments varying the data-generating mechanism. Without such validation, it is unclear whether the method's gains come from genuine directional signal or from the reduced complexity penalty inflating recall at the cost of precision, yielding a small net F₁ increase.

2. **PDAG random-orientation evaluation protocol systematically disadvantages baselines.** The paper states (line 190): "For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics." PC and GES honestly leave unidentifiable edges undirected; random orientation means ~50% of truly unorientable edges will be counted as wrong. This conflates whether XBIC's directional signal is correct with whether committing to *any* direction (even random) is better than leaving edges undirected. The paper itself acknowledges (line 17) that mediator/confounder motifs "leave orientations unresolved" — i.e., these orientations are unidentifiable from observational data. The evaluation should report PDAG-level metrics (e.g., SHD on the skeleton, or F₁ computed only on edges the method orients) to provide an apples-to-apples comparison.

### Minor

3. **Modest absolute gains at extreme computational cost.** From Table 4, XBIC (w=2) achieves an absolute F₁ improvement of 0.04 over BIC-HC and 0.06 over GES. The 5.6% and 9.6% relative figures in the abstract sound larger than these absolute deltas. Table 2 shows many settings where improvement is 0.00–0.10 and some where it is negative (e.g., Water at 0.125M²: −0.01; Win95pts at 8M²: −0.09). Meanwhile, XBIC is 28–600× slower than BIC-HC (Table 5: e.g., Survey 0.09s vs 54.21s, 602×; Asia 0.39s vs 74.78s, 192×). An absolute F₁ gain of ~0.04 at a 50–200× computational premium raises questions about practical utility, especially given the authors' acknowledgment (line 206) that XBIC often does not improve for small networks and limited data.

4. **GES comparison may suffer from selection bias.** GES exceeded the 7-day limit on larger settings; the paper restricts to completed runs and asserts this is "favorable filtering for GES" (line 278). The alternative interpretation — that GES only finished on structurally easier settings where the advantage of any method is smaller — is not discussed or ruled out.

5. **SHD results not systematically reported for BIC and PC.** SHD is stated as a metric (line 200) but only reported for the GES comparison (Section 4.5, Figure 3). For a complete evaluation, SHD against all baselines should be reported.

6. **The consistency claim (lines 155–159) is not fully established.** The penalty scaling argument (O(log N) preserved) is valid in order, but the constant factor c(G) = 1/exp(w·SHAP(G)) can become arbitrarily small for dense graphs where many edges carry non-zero attribution, potentially weakening the penalty significantly. The paper acknowledges c(G) ∈ (0,1] but does not analyze the practical implications of this range.

### Trivial

7. **Individual F₁ numbers in Table 2 lack confidence intervals or standard deviations.** A Friedman test is reported (line 241), but given the variability across 10 repetitions per setting, readers cannot assess whether the 0.04 absolute gain is statistically reliable in each individual setting.

## Nice-to-Haves

- Report PDAG-level metrics (e.g., SHD on skeleton, edge-orientation accuracy) for PC and GES as a sensitivity check alongside the random-orientation protocol.
- Add a per-edge analysis on small networks (e.g., Asia, Survey) showing whether |φ̄ᵢ→ⱼ| > |φ̄ⱼ→ᵢ| aligns with ground-truth causal direction — this is the most direct test of the core mechanism.
- Include controlled synthetic experiments varying data-generating mechanisms (linear vs. nonlinear, additive vs. non-additive noise) to characterize *when* the Shapley directional signal works and when it fails.
- Discuss the practical implications of the c(G) constant factor in the consistency argument.

## Removed Points

These points were considered and removed for the reasons stated:

- **Missing comparison with methods that break Markov equivalence (LiNGAM, CAM, NOTEARS variants):** These methods target continuous data; the paper focuses on discrete causal discovery. Demanding their adaptation is scope expansion beyond the paper's stated contribution. **Removed.**
- **Exclusion of MMHC:** The paper explains (line 190) that MMHC "targets large sparse graphs and is not the focus here." This is a reasonable scope choice. **Removed.**
- **Equation 2 global vs. local modulation:** The reviewer notes the penalty modulation is global rather than edge-specific. However, SHAP(G) in Equation 3 sums per-edge |φ| values, so edges with different |φ| contribute differentially to the modulation. This is a valid design choice, not a flaw. **Removed.**
- **Confidence threshold selection bias:** The paper addresses this directly (line 194): varying τ between 0.7 and 0.95 changed downstream F₁ by <1%. **Removed.**
- **Hyperparameter w selection on test data:** The paper reports results for all w ∈ {1,2,3} (Table 4), enabling the reader to assess sensitivity directly. No claim of test-set tuning is made. **Removed.**
- **ReX baseline comparison:** ReX is cited as working in continuous settings with constraint pruning (line 56), positioning XBIC differently (discrete, score-based). The baseline set is standard for discrete causal discovery. **Removed.**
- **PC runtime on Hailfinder (Table 5):** The reviewer notes PC takes 15,923s on Hailfinder, exceeding XBIC's 1,904s. This is a surprising observation about a baseline implementation that does not directly affect evaluation of the proposed method. **Removed.**

## Novel Insights

The harsh critic correctly identifies an important gap: the paper asserts that Shapley asymmetry from non-causal predictive classifiers should align with causal direction, but this claim is neither theoretically justified nor empirically validated at the per-edge level. The PDAG random-orientation issue is also a useful methodological critique — it means the reported F₁ improvements over PC and GES may partially reflect the advantage of committing to any direction (even possibly random) rather than correctly identifying causal direction. These points are well-taken but do not constitute novel meta-insights beyond the paper's own framing.

## Suggestions

1. Provide a per-edge analysis on small networks (e.g., Asia, Survey) showing whether |φ̄ᵢ→ⱼ| > |φ̄ⱼ→ᵢ| aligns with ground-truth causal direction.
2. Report PDAG-level metrics for PC and GES as a sensitivity check alongside the random-orientation protocol.
3. Add controlled synthetic experiments where the ground-truth mechanism is known and varied to characterize when the Shapley signal is directionally informative and when it fails.
4. Report confidence intervals or standard deviations for the F₁ numbers in Table 2.
5. Report SHD for all baselines (not just GES).
6. Discuss the practical range and implications of the c(G) constant factor in the consistency argument.

## Summary of Calibration

**Calibration anchors used:**

| Anchor | Avg Score | Round | Itemized | Comparison |
|--------|-----------|-------|----------|------------|
| DAG-SHAP (ljZFM2mhbR) | 5.00 (Reject) | R1 (3.5–5.5) | Yes | Similar Shapley+causal theme; XBIC has a more severe theoretical gap (−1.54 vs 0.46) but stronger empirical breadth (10.47 vs 9.12) |
| DrBO: Causal Discovery via BO (8muemqlnG3) | 6.50 (Accept) | R1 (5.5–7.5) | Yes | Stronger paper; XBIC's worst weakness (−1.54) is more severe than any in DrBO's review |
| Extendable BN Structure Learning (3n6DYH3cIP) | 5.60 (Accept) | R1 (3.5–5.5) / R2 | Yes | Comparable structure-learning paper; XBIC has more novel idea but weaker empirical deltas and a deeper theoretical gap |
| ExDBN (eqQFBnjjPP) | 4.00 (Reject) | R2 (3.5–6.0) | Yes | XBIC's weaknesses are less severe (−1.54 vs −4.17) and strengths stronger |
| DiffIntersort (G19piTjVYA) | 4.00 (Reject) | R2 (3.5–6.0) | Yes | XBIC's weaknesses are less severe (−1.54 vs −3.25, −2.84) |

**Bracketing:** Round 1 placed XBIC between 3.5 and 5.5. Round 2 narrowed to 4.0–5.0 based on comparison with ExDBN (4.00, weaker paper) and DAG-SHAP (5.00, comparable paper with less severe theoretical gap). Within this bracket, XBIC's weighted items place it above ExDBN (whose worst weakness weights −4.17 and −1.76 are more negative than XBIC's −1.54) but below DAG-SHAP (whose weakest items have positive weights 0.46–0.61, while XBIC's central premise weakness at −1.54 is genuinely more concerning). The final score of **4.5** reflects a paper with a creative idea and extensive evaluation but with two major methodological issues (unsubstantiated premise and unfair evaluation protocol) that collectively prevent acceptance in the current form.

## Score and Decision

**Score:** 4.5

**Decision:** Reject

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>