## Summary
This paper proposes *conformalized survival counterfactual prediction*, a calibration method for constructing lower predictive bounds (LPBs) on counterfactual survival times under different treatments for general right-censored data. The central contribution is a reweighting scheme (equation 1) that bounds the full-population miscoverage probability via a reweighted expectation over uncensored observations, transforming the problem into a weighted conformal inference problem (Lei & Candès, 2021) with exact—rather than PAC-type—marginal coverage guarantees. The method also provides a doubly-robust property (Theorem 4.2) and is validated on synthetic data across six simulation settings and a real-world lung cancer dataset.

---

## Strengths

- **Genuine and consequential gap addressed.** Prior work (Gui et al. 2024; Davidov et al. 2025) produces only PAC-type guarantees, which fail under outlier contamination. This is concretely demonstrated in Figure 3: when survival outliers are injected, Focus and Fused lose coverage while the proposed method maintains it. The distinction between exact and PAC-type marginal coverage is not merely theoretical—it matters precisely in the high-stakes clinical settings the paper targets.

- **Technically sound core argument.** The inequality chain in equation (1)—particularly step (iii), which bounds full-population miscoverage by a reweighted expectation over the uncensored subpopulation using the conditional independence T(w) ⊥ C | X from Assumption 3.1—is the paper's main technical advance. The reduction to weighted conformal prediction is clean and correctly inherits exact finite-sample guarantees.

- **Less conservative and valid empirically.** Figures 1 and 2 show that the proposed method achieves *higher* relative LPBs than Focus and Fused in most settings while maintaining valid coverage, demonstrating it is simultaneously more informative and more correct. This is a stronger empirical result than merely restoring validity.

---

## Weaknesses

### Fatal
None.

### Major

- **Theorem 4.1 establishes coverage for the uncensored subpopulation (e=1), not the full population stated as the goal.** The paper's objective (Section 3, eq. on p.3) is marginal coverage over P_X × P_{T(w)|X}. Theorem 4.1 (eq. 4), however, establishes coverage with respect to P_X × P_{T(w)|X, e=1}—the uncensored subpopulation. While the body text acknowledges this ("it is sufficient for the LPB to satisfy the coverage guarantee for P_X × P_{T̃|W=w,e=1,X}"), the connection from this sufficient condition back to the full-population goal is carried by the inequality at step (iii) of eq.(1) and is *not stated within Theorem 4.1*. As written, the theorem is a weaker statement than the paper's main claim requires. This is very likely a presentation gap rather than a fundamental error—the argument in eq.(1) supports the stronger claim—but the theorem must either be restated in terms of the full marginal distribution, or a corollary explicitly connecting the two must be added.

- **No formal guarantee that data-dependent τ* selection preserves exact coverage.** Theorem 4.1 holds for any *fixed* τ. Section 4.1 then defines τ*(x) = argmax_τ (q̃_τ(x) − c_{1−α}(τ, x)), where c_{1−α}(τ) is computed from the same calibration set as the nonconformity scores. Using calibration data for both score computation and τ selection introduces coupling. The paper asserts "our procedure yields a prediction set that satisfies the coverage guarantee for any τ ∈ (0,1)" but does not prove simultaneous (uniform over τ) coverage, which is what data-dependent selection requires. Without this, the claim of "exact" coverage under the optimized LPB is formally unsubstantiated. Table 1 shows empirical coverage remains valid in practice, but a formal argument is absent.

### Minor

- **Setting 6 coverage falls below 1−α with insufficient explanation.** The paper notes: "the average coverage rate of our method slightly falls below 1−α in setting 6, it remains remarkably close to the target level." Given the paper's central claim of exact coverage, this deviation warrants explicit explanation—whether due to small calibration set size, MLP underfitting in that setting, or a structural limitation of the bound—rather than dismissal in one sentence.

- **"Naive" calibration baseline is undefined in the main text.** It is compared in Figures 1, 2, and 3 but defined only in the appendix. A one-sentence definition in the main text would aid interpretation.

### Trivial
None that belong to the authors (the Figure 2 caption inconsistency is a parser artifact in the image alt-text, not the authors' caption).

---

## Nice-to-Haves

- A small simulation characterizing method behavior under sparse calibration sets (small |I_cal^(w)| due to imbalanced treatment or high censoring) would help practitioners identify the method's operational range. This is acknowledged in the Discussion but not empirically characterized.
- A brief discussion of whether the doubly-robust conditions in Assumption A2 (bounded conditional density, joint convergence of E_N(X)/γ̂(x)) are plausibly satisfied by the MLP quantile regressor and Random Forest classifier used experimentally would strengthen the theoretical section.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Assumption 3.1 is "stronger than typically assumed."** The harsh reviewer notes that {T(1),T(0)} ⊥⊥ (W,C)|X bundles treatment ignorability with independent censoring. The paper cites Kalbfleisch & Prentice (2002) and Remark 3.2 explicitly acknowledges this. This is standard in causal survival analysis; criticizing its absence is scope creep. Removed.

- **Doubly robustness conditions "difficult to verify and restrictive."** This is a general limitation of doubly-robust methods, not a specific flaw of this paper. Demoted to nice-to-have.

- **Figure 2 alt-text inconsistency ("lower relative LPB closer to 1.0").** This is a parser artifact from image auto-captioning, not an author error. Removed per hard rules.

- **Strength: "well-placed in the literature / addresses important problem."** Generic. Removed; retained only the specific, grounded strengths above.

---

## Novel Insights
The paper's cleanest contribution is showing that the right-censored counterfactual coverage problem reduces to a *covariate-shift* problem: the shift is from the full marginal X distribution to the conditional X|W=w, e=1 distribution, and the likelihood ratio ω(x) = p(W=w, e=1)/γ(x) is the bridge. This framing connects disparate threads—causal inference, survival analysis, and weighted conformal prediction—in a way that is both principled and computationally tractable, and the outlier experiment cleanly illustrates why the PAC-type approximation is genuinely inferior in the high-stakes regime where rare extreme cases matter.

---

## Suggestions

1. **Fix Theorem 4.1:** Restate it with P_X × P_{T(w)|X} (full population) as the target distribution, using eq.(1) as the proof structure, with the e=1 subpopulation appearing as an intermediate step. This brings the theorem into alignment with the paper's stated goal.
2. **Address τ-selection formally:** Either prove simultaneous coverage over all τ (which would validate data-dependent τ* selection), or add a separate held-out set for τ selection and adjust the algorithm accordingly. If the empirical evidence (Table 1) is used to argue robustness, frame it explicitly as an empirical robustness claim, not a theoretical guarantee.
3. **Explain Setting 6 deviation:** Add one or two sentences characterizing why coverage falls below target in Setting 6 (e.g., censoring rate × treatment imbalance leading to very small |I_cal^(w)|).
4. **Define "naive calibration" in main text:** One sentence suffices.

---

## Score and Decision

**Calibration anchors retrieved across rounds:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `AKAz88zYLB.md` | 5.80 | R1 | Most topically similar: conformal prediction for causal dose-response with covariate shift; only synthetic data, no censoring, less rigorous than this paper |
| `Nfd7z9d6Bb.md` | 6.00 | R1 | Conformal prediction with approximate conditional coverage; clean theory but narrower scope than this paper |
| `33XGfHLtZg.md` | 7.00 | R1 | Conformal Risk Control — more general and cleaner extension of conformal prediction; serves as upper anchor |
| `rulxyXjf46.md` | 6.25 | R1 | Conformal prediction via regression-as-classification; solid but narrower contribution |
| `XgYPzNtz0s.md` | 4.60 | R1 | Survival analysis via density estimation — borderline, weaker contribution |
| `Dtxc7mlKRg.md` | 4.60 | R1 | Conformal prediction for imbalanced classification — narrower, borderline |
| `y2ch7iQSJu.md` | 2.00 | R1 | Survival data active learning — rejected, less rigorous |
| `v8RDgaEtE2.md` | 2.50 | R1 | Conformal prediction under bias — rejected, narrower |

**Round 1 bracket: 5.5 – 7.0**

The paper is clearly above the 4.6 borderline papers (XgYPzNtz0s, Dtxc7mlKRg) in novelty and rigor, and below the cleaner/more general Conformal Risk Control (7.00). The most similar paper, `AKAz88zYLB.md` (5.80, rejected), is weaker than this paper in that it lacks real data, lacks a doubly-robust theorem, and addresses a less technically demanding setting (no censoring). This paper fills a more specific and harder gap (general right-censored + counterfactual + exact coverage) with both stronger theory and stronger experiments.

**Narrowing:** The two major weaknesses—Theorem 4.1 distribution mismatch and τ-optimization coverage gap—are real but correctable. The empirical results are credibly positive across 6 simulation settings + a real clinical dataset with 541 patients. The outlier robustness experiment is particularly compelling. A revised version with a corrected theorem and a formal τ-selection argument would be a solid accept. As written, the theoretical gaps are notable but do not invalidate the core contribution.

**Final score: 6.0**

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>