Now let me compile my final review after thorough analysis of both the paper and calibration anchors.

---

## Summary

This paper proposes ZNet, a deep learning architecture that learns instrumental variable (IV) representations directly from observed covariates without requiring pre-specified candidate instruments. The method decomposes the covariate space into confounder and instrument components by encoding the three IV conditions (relevance, exclusion restriction, unconfoundedness) into a multi-part loss function. The evaluation spans four dataset classes, linear/nonlinear settings, with/without unobserved confounding, using three downstream estimators and four baselines.

## Strengths

**1. Architecture and loss design explicitly encode IV structure (weight: 9.37).** Rather than relying on black-box variational inference, ZNet builds the three IV conditions directly into the objective via correlation and mutual information penalties. This transparency is a genuine advantage over VAE-based approaches (AutoIV, VIV, DVAE.CIV, GDIV) where the link between training objective and IV conditions is indirect (Section 5, Figure 3).

**2. Comprehensive evaluation across diverse data-generating scenarios (weight: 8.82).** The paper tests four dataset classes (disjoint candidate, mixed candidate, latent categorical, no candidate) × linear/nonlinear × with/without unobserved confounding, using three downstream estimators (TSLS, DeepIV, DFIV) and four baselines. This is the most thorough evaluation of IV generation methods I have seen (Section 6.1, Table 1).

**3. Ablation study validates loss design (weight: 9.71).** Figure 5c shows that each constraint (unconfoundedness, exclusion restriction, relevance) contributes to recovering existing instruments; removing any constraint deteriorates recovery. This confirms the loss design is not vacuous.

**4. Lemma 1 provides a theoretical bridge (weight: 8.74).** The connection between zero covariance with the observable residual \(Y-\mathbb{E}[Y|X,T]\) and zero covariance with the unobserved error \(e_Y\) (under normality of \(Z\)) offers principled justification for a loss term that would otherwise be purely heuristic (Section 3).

## Weaknesses

### Major

**1. Overclaimed framing regarding untestable assumptions.** The abstract claims ZNet works "regardless of whether the (untestable) assumption of unconfoundedness is satisfied." While Lemma 1 relaxes this assumption, the method does not eliminate untestable assumptions — it replaces the standard IV assumptions with a different set (well-specified \(\Phi\), soft normality constraint via KL penalty, covariance as a proxy for full conditional independence). No theorem bridges the gap between observable Constraints 1–3 and the true IV conditions involving unobservables. The paper's discussion (Section 7) partially acknowledges this limitation, but the abstract and introduction imply a solution that isn't fully delivered. [Verifiable in paper: lines 9, 23, 85, 394]

**2. "Superior performance" claim unsupported by Table 1.** The paper claims "superior" performance (abstract, line 386). Across the full table, ZNet is bolded (best) in roughly 11 out of 30 estimator-dataset cells. It is competitive, especially in the no-candidate setting where it frequently leads (e.g., Non-linear No Candidate DeepIV: 0.260, DFIV: 0.049), but several baselines — particularly VIV and AutoIV — match or beat ZNet in multiple settings (e.g., Linear Disjoint TSLS: TrueIV -0.002, VIV 0.147, ZNet 0.119; Linear Latent TSLS: VIV -0.082 vs ZNet -0.125). The evidence supports "competitive" or "strong on no-candidate settings," not blanket superiority. [Verifiable in paper: Table 1, lines 9, 23, 386]

### Minor

**3. Missing uncertainty estimates in main results.** Table 1 reports mean ATE error across 50 bootstrap resamples but provides no standard deviations, confidence intervals, or any uncertainty measure. Without these, the reader cannot assess whether gaps between methods (e.g., ZNet 0.025 vs. AutoIV −0.028 on Linear No Candidate TSLS) are meaningful or noise. The asterisk notation (*/**) indicates significance rank across methods, not whether ATE estimates themselves differ significantly from the true ATE.

**4. "New SCM" framing is imprecise (line 69).** The paper claims learning \(f\) and \(g\) defines "a new SCM where the instrument \(Z\) is derived from the observed data \(X\)." An SCM is a model of the *data-generating process* with independent exogenous noise terms. ZNet learns deterministic functions without modeling exogenous variation. Calling this a "new SCM" overstates the theoretical status of the construction.

**5. Three-stage training procedure not ablated (Section 5.3).** Training occurs in three stages — train \(\Phi\) first, then pretrain \(f,g\) with a subset of losses, then full training with gradient surgery. No comparison against simpler alternatives (e.g., full end-to-end training) is provided, leaving open whether this complexity is necessary.

**6. Formal statement of Constraint 2 is imprecise (lines 100–103).** Constraint 2 states \(\text{Cov}(f(X),Y) > 0, \text{Cov}(g(X),f(X)) = 0\). The first part ensures \(C\) is correlated with \(Y\), but exclusion restriction requires that \(Z\) not directly affect \(Y\) — not that \(C\) is correlated with \(Y\). The actual implementation is more nuanced (F-test in Figure 6b), but the formal constraint statement is misleading as written.

**7. No hyperparameter sensitivity analysis.** The seven loss weights \((\alpha_1,\dots,\alpha_7)\) are tuned via Bayesian optimization per dataset (line 165). Without any sensitivity analysis, it is unclear whether ZNet's performance is robust to weight variation or depends critically on careful per-dataset tuning.

### Trivial

**8. Sloppy step in Lemma 1 proof (line 93).** The derivation writes \(\mathbb{E}[Z \cdot (e_Y - \mathbb{E}[e_Y|X,T])] = \mathbb{E}[Z \cdot e_Y] - \mathbb{E}[Z] \cdot \mathbb{E}[e_Y|X,T]\). Since \(\mathbb{E}[e_Y|X,T]\) is a random variable, \(\mathbb{E}[Z] \cdot \mathbb{E}[e_Y|X,T]\) is also random, not a scalar, and cannot be subtracted from \(\mathbb{E}[Z \cdot e_Y]\). The result is correct (since \(Z=g(X)\), the law of iterated expectations gives the intended simplification), but the derivation as written is not mathematically precise.

## Nice-to-Haves

- Report confidence intervals or standard deviations in Table 1.
- Ablate the three-stage training procedure against end-to-end training.
- Add a sensitivity analysis for loss hyperparameters.
- Include a clear statement of what ZNet guarantees and what it does not, with an honest discussion of the gap between observable constraints and true IV conditions.

## Removed Points

These points were raised by the harsh critic or strength finder but are removed after filtering:

- **Criticism about VAE methods claim (line 113):** The critic argued the paper's statement that VAEs "lack theory to guarantee learning the true causal model" is unfair because ZNet also lacks such guarantees. This is a reasonable observation but not a weakness of the paper's method — it's a comparative claim that is factually correct (VAEs do not have such guarantees) and the critic's counter-argument is about ZNet's own limitations, which is already captured in Weakness 1 above.
- **F-Statistic tuning criterion circularity:** The critic questioned whether tuning on the same metrics the loss enforces is circular. This is actually standard validation-based hyperparameter selection (choosing hyperparameters that make the loss work best on held-out data), not a circularity.
- **Several strengths from the strength finder**: Generic strengths about the problem being important or timely are removed.
- **Request for theoretical proof about loss landscape:** The critic's claim that the "gap between observable constraints and true IV conditions is unbridgeable by construction" is a strong claim that is ultimately an opinion about the entire sub-field, not a specific flaw in this paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Recalibrate the claims throughout the paper: replace "superior performance" with language that accurately reflects the method's strength in no-candidate settings while acknowledging it is competitive (not dominant) when candidate instruments exist.
2. Add a formal statement about the gap between Constraints 1–3 and the true IV conditions, and what would need to be true for one to imply the other.
3. Add uncertainty measures (standard deviations or confidence intervals) to Table 1.
4. Revise the "new SCM" language to more accurately describe what is learned (a representation satisfying moment conditions, not a full structural causal model).

## Score and Decision

### Calibration Summary

**Round 1 — Bracketing.** Six bands queried for papers on causal effect estimation / instrumental variables / representation learning with deep learning. Key anchors identified:

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| ADR (Decomposed Reps for ITE) | F7XPZnIUHh.md | 4.20 | R1 | Yes | Most similar structurally: both learn decomposed representations for causal inference without full theoretical guarantees. ADR had heavier negative weakness weights (-4.02, -6.68) due to derivation errors and novelty concerns; ZNet has no derivation errors and a more thorough evaluation. ZNet sits above ADR. |
| CFDiVAE (Front-Door + VAE) | wFf9m4v7oC.md | 5.75 | R2 | Yes | Both learn representations for causal inference with partial theoretical support. CFDiVAE has formal identifiability proofs that ZNet lacks, but ZNet has a broader evaluation. Comparable overall quality. |
| Causal Info Bottleneck | qac43AwuL9.md | 6.00 | R2 | Yes | Stronger theoretical framing but simpler experiments. Less directly comparable due to different problem setup (causal representation learning vs. IV generation). |
| CIV + Representation Learning | qDhq1icpO8.md | 6.75 | R1 | Yes | Addresses similar IV problem with theoretical guarantees ZNet lacks. Accepted paper. ZNet falls below this due to absent theoretical guarantees and overclaiming. |
| ShadowCatcher | Oc4ji1iCjQ.md | 6.75 | R1 | Yes | Automatically generates representations for collider bias. Similar spirit but different problem. Well-received but rejected. |
| No files in 8.5+ band | — | — | R1 | No | — |

**Round 1 Bracket:** The paper's weighted items show high strength weights (8.74–9.71) and moderately positive weakness weights (1.40–4.86, all > 0). Compared to ADR (4.20, which had negative weakness weights) and CFDiVAE (5.75, which also had positive weakness weights), the bracket is **4.5–6.0**.

**Round 2 — Narrowing.** Re-queried with more focused IV + representation learning query in the 3.5–7.5 range. The CIV paper (6.75) provides the upper bound: it has theoretical guarantees that ZNet lacks. The ADR paper (4.20) provides the lower bound: it has more severe weaknesses than ZNet. The CFDiVAE paper (5.75) is the closest comparator in overall quality: both have partial theoretical support and solid evaluations, with ZNet's evaluation being more comprehensive but its theoretical support weaker.

**Final placement:** The paper's weighted strengths (avg ~9.2) are comparable to the CIV and CFDiVAE papers' strengths, but its weaknesses are more significant than CFDiVAE's (which were mainly about limited novelty). The absence of any theoretical guarantee connecting the loss constraints to actual IV validity, combined with the overclaimed framing, places this paper below CFDiVAE (5.75). The comprehensive evaluation and clean architecture prevent it from falling to the ADR level (4.20). **Final score: 5.0.**

**MY FINAL SCORE:** <score>5.0</score>
**MY FINAL DECISION:** <decision>Reject</decision>