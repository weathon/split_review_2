Now I have enough to draft the review. Let me write it up and call `draft_review`.Now I have enough calibration context. Let me write the final review.

---

## Summary
Medix is a novel OOD detection framework for the unlabeled in-the-wild setting. Its core contribution is a greedy, leave-one-out element-wise median (EWM) filtering algorithm that identifies OOD samples from a mixed unlabeled wild set by measuring each sample's contribution to the L2 distance between the EWM gradient of the wild set and the mean gradient of labeled InD data. The identified outliers are then used to train a binary OOD detector following Du et al. (2024a)'s protocol. Theoretical bounds on inlier and outlier misclassification rates are derived under sub-Gaussian gradient assumptions, and empirical evaluation covers CIFAR-10/100 against 20 baselines.

---

## Strengths

- **Large empirical gains on CIFAR-10 (Table 1):** Medix achieves average FPR95 of 0.80% vs. WOODS's 3.40% — a 4× reduction. Per-dataset improvements (PLACES365: 10.19 → 2.98; TEXTURES: 6.21 → 0.96) are too large to be explained by hyperparameter tuning alone, providing credible evidence that EWM-based filtering works substantially better than WOODS's approach in this setting.
- **Concrete motivating experiment (Figure 1):** The monotonic increase in EWM gradient deviation as OOD samples are added to the wild set is a clear, reproducible motivation for the method and directly inspires both the algorithm and the stopping criterion.
- **Two-sided theoretical framing:** Theorems 4.1 and 4.2 bound inlier misclassification (contamination + concentration) and outlier misclassification (separation + contamination + concentration) separately, covering both error directions; the paper also validates the sub-Gaussian assumption empirically via histogram and Q-Q plot (Figures 4a, 4b).
- **Breadth of baselines:** Twenty baselines spanning InD-only and wild-data methods (including the two most recent, CONJ and DRL), with performance averaged over five runs with standard deviations reported.

---

## Weaknesses

### Fatal
None.

### Major

- **Algorithm 1 has a logical error in the stopping condition (line 2):** The while-condition reads `t ≤ T or |δ_max| > ε`. With `or`, the loop continues as long as *either* condition holds — so even when convergence is achieved (|δ_max| ≤ ε), the algorithm runs until T iterations are exhausted. The intended semantics — stop when the iteration limit is reached *or* convergence is achieved — requires `and`. As written, the convergence criterion is dead code: the algorithm always runs T iterations regardless of gradient deviation. This is reproducibility-relevant because the choice of T, ε, and the interaction between them as described in text differs from what the pseudocode actually implements.

- **Ambiguous hyperparameter selection potentially inflating CIFAR-100 results:** Section 5.2 states ε and k are "selected… with the objective of maximizing OOD performance" over a 4×4 = 16-combination grid. The paper does not describe a held-out validation OOD set or any mechanism preventing the use of test OOD performance for selection. On CIFAR-100, Medix's improvement over WOODS averages 1.32% FPR95 (from 6.74 → 5.42), with per-dataset margins ranging from 0.01% to 5.88% — well within what grid-search bias across 16 combinations could produce. The paper reports in Section 5.3 that Appendix A.2 shows "Medix's strong robustness to hyperparameters," but this does not address whether the *reported optimal configuration* was selected using test OOD performance. A clear statement of the selection protocol is needed for the CIFAR-100 results to be accepted at face value.

### Minor

- **Theoretical bounds are vacuous at the experimental setting (π = 0.5):** At the default contamination ratio π = 0.5, Theorem 4.1's contamination term is π/[2(1−π)] = 0.5, and Theorem 4.2's corresponding term is (1−π)/(2π) = 0.5. Both bounds thus guarantee only ERR ≤ ~0.5 (plus small concentration terms), no better than random guessing. The empirical error rate of 12.5% (Figure 2) is 4× better than what the theory proves. The paper frames the theory as "validating empirical findings" and providing "rigorous theoretical assurance," but this framing is inaccurate when the bound is uninformative at the operating point. The theory is correct, but the paper should honestly present the bounds as qualitative characterization rather than quantitative validation of the observed 12.5%.

- **CONJ and DRL absent from the main comparison tables (Tables 1 and 2):** Section 5.1 explicitly positions CONJ and DRL as baselines "to provide a more thorough evaluation," but they appear only in Appendix A.3. The claim in the conclusion that "Medix outperforms all the baselines" cannot be verified from the main tables alone. If CONJ or DRL are competitive with WOODS, their omission from Tables 1 and 2 inflates the impression of Medix's advantage over the state of the art visible to the reader.

- **Training data asymmetry:** Medix trains the InD classifier on 25,000 samples (first half of CIFAR) while all InD-only baselines use the full 50,000. This is acknowledged, but the effect on the reference gradient $\bar{\nabla}_\text{in}$ quality — which anchors all filtering decisions — is not analyzed. Given that the reference gradient is the core signal of the method, a brief sensitivity check (e.g., using 50k vs 25k InD samples for gradient computation) would strengthen the claim that the filtering quality is not confounded by this asymmetry.

### Trivial
None.

---

## Nice-to-Haves

- A controlled ablation isolating the filtering stage: Du et al. (2024a) filtering + Du et al. training vs. Medix filtering + Du et al. training. Since Stage 2 directly follows Du et al., this experiment would be the cleanest demonstration of Medix's filtering advantage.
- Tighter theoretical analysis at high π (e.g., exploiting gradient separability of neural networks) to bridge the gap between the bound (~0.5) and the observed performance (~12.5% error).
- Running time comparison in the main text (currently deferred to Appendix A.6).

---

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **Separation condition in Theorem 4.2 (√d scaling in high dimensions)**: Critic argued the condition ‖μ_out − ∇̄_in‖₂ ≥ Δ√d is hard to satisfy for high-dimensional gradients. This is speculative — Figure 1 provides empirical evidence of separability, and the condition's scaling is standard for sub-Gaussian concentration arguments. Removed as speculative, not anchored in a concrete failure in the paper.
- **O(n²×d) computational complexity concern**: Without concrete timing evidence that the complexity is prohibitive, and given the paper defers to Appendix A.6 for efficiency analysis, this is speculative. Removed.
- **Greedy algorithm gap from exact optimization (Eq. 4)**: The paper acknowledges Algorithm 1 is a greedy approximation; the absence of optimality gap analysis is standard for empirical OOD papers. Removed as not a meaningful weakness for this setting.

---

## Novel Insights
The paper cleanly demonstrates that element-wise median gradient deviation is a principled and practically effective signal for separating InD from OOD samples in unlabeled wild mixtures. The identified logical error in Algorithm 1 (OR vs AND) is a specific, verifiable bug that, if taken literally, would make the convergence criterion moot — correcting this should be straightforward but is an important fix. The hyperparameter selection ambiguity is a real methodological gap that particularly affects CIFAR-100: the CIFAR-10 improvements are convincingly large, but the CIFAR-100 story rests on margins that require a clean selection protocol to be credible.

---

## Suggestions
1. **Fix Algorithm 1 line 2**: replace `or` with `and` to correctly implement the intended "stop when converged or budget exhausted" rule.
2. **Clarify hyperparameter selection**: add an explicit statement in Section 5.2 of whether test OOD datasets were used for selection. If not, say so. If yes, redo using a held-out validation OOD set or select by a proxy (e.g., InD validation accuracy).
3. **Move CONJ and DRL results** (at minimum summary rows) to Tables 1 and 2 to allow direct verification of the "outperforms all baselines" claim.
4. **Recalibrate the framing of Theorems 4.1 and 4.2** at π = 0.5: acknowledge the bound is loose at the experimental operating point and reposition the theorems as qualitative robustness characterization rather than quantitative validation of the 12.5% error rate.

---

## Score and Decision

**Calibration anchors:**

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| `jlEjB8MVGa` — SAL (Du et al. 2024a, direct predecessor to Medix) | 6.50 | 1 | Most comparable: same setting (unlabeled wild OOD), theory + experiments; Medix builds on SAL's training stage with a new filtering approach |
| `iriEqxFB4y` — DOS (diverse outlier sampling) | 7.33 | 1 | Clean contribution, strong CIFAR-100 results, simpler methodology, no algorithmic errors |
| `voVjW1PT2c` — ProMix (guaranteed OOD, diverse aux set) | 6.00 | 1 | Similar provable-OOD framing, rejected; weaker overall than Medix on CIFAR-10 |
| `nUBLhhVM1l` — Tight rates in supervised outlier transfer | 6.33 | 1 | Theoretical OOD paper, similar tier |
| `Cdhxv0Oz1v` — GradRect | 4.20 | 1 | Gradient-based OOD, borderline reject; weaker experiments and contribution |
| `RWZzGkFh3S` — Outlier gradient analysis | 4.50 | 1 | Gradient outlier detection, less comprehensive evaluation |

**Round 1 bracket:** 5.0–6.5. The direct predecessor (SAL, which introduced the problem setting and provided theory+experiments) scored 6.5. Medix contributes a new filtering mechanism with substantially larger CIFAR-10 gains but has a real algorithm bug, hyperparameter selection ambiguity on CIFAR-100, and vacuous theory at π = 0.5. DOS (7.33) is a comparably strong empirical OOD paper but has cleaner methodology.

**Round 2 narrowing:** Medix's CIFAR-10 results are convincingly strong (well beyond what selection bias could explain), and the paper covers the same setting as SAL at a similar depth. However, relative to SAL: (a) Medix's contribution is narrower (filtering only, Stage 2 directly adopted from SAL), (b) the algorithm has a verifiable logic error, and (c) the theoretical claims are oversold at the operating point. These lower it slightly below SAL's 6.5. The hyperparameter leakage concern specifically undermines the CIFAR-100 claims but not the CIFAR-10 claims. On balance: the paper is between borderline reject and borderline accept.

**Final score: 5.0** — borderline reject. The core idea is sound and CIFAR-10 results are impressive, but the verifiable algorithm error, the ambiguous hyperparameter selection protocol for CIFAR-100 (where margins are small), and the misleading framing of theoretical bounds at π = 0.5 collectively require revision before acceptance.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>