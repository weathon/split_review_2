## Summary

This paper decouples the class label from the target concept in class-wise machine unlearning, introducing a taxonomy of label-domain mismatch scenarios (target mismatch, model mismatch, data mismatch) that extend beyond the conventional all-matched setting. The authors identify the specific failure modes of existing methods on these new tasks and propose TARF, a framework combining annealed gradient ascent on the forgetting data with selective gradient descent on hard-to-affect retaining data, driven by a "representation gravity" identification mechanism. The paper's main contributions are the problem framing and strong empirical results demonstrating that TARF substantially outperforms existing baselines on the mismatch settings.

---

## Strengths

1. **Problem formulation (Section 3.1, Figure 1).** The paper correctly identifies a blind spot in prior unlearning work: the label domains of the forgetting data, model output, and target concept can all disagree. The four scenarios (all matched, target mismatch, model mismatch, data mismatch) are clearly defined via the relations $\mathcal{L}_D = \mathcal{L}_T = \mathcal{L}_M$ and its variants. This is a genuine conceptual contribution that cleanly carves out space previously assumed away.

2. **Empirical results on mismatch tasks (Table 3).** On target mismatch and data mismatch—the two settings where existing methods collapse—TARF produces results dramatically closer to the Retrained reference. On CIFAR-10 target mismatch: TARF Gap = 1.23 vs. next best (GA) at 20.80. On CIFAR-100 data mismatch: TARF Gap = 1.17 vs. next best (GA) at 2.43. These are differences of kind, not degree, and justify the method if the motivating problem is accepted.

3. **Scalability evidence (Table 4).** The ImageNet-1k results show TARF maintaining its advantage across all four settings at scale, with Gap values consistently lowest or tied for lowest. This strengthens the generality claim—many unlearning methods that work on CIFAR degrade on ImageNet.

---

## Weaknesses

### Fatal
None.

### Major
1. **Theorem 3.2 is imprecisely stated and its connection to the method is loose.** The term $\lambda_{\max}(J_\theta)$ is described as "the largest eigenvalue of the Jacobian matrix $J_\theta = \frac{\partial h(x)}{\partial \theta}$" (line 106). However, $J_\theta$ is a $(\dim h) \times (\dim \theta)$ matrix and is typically non-square; eigenvalues are not defined for such matrices—one would need singular values. The expression $\lambda_{\max}(J_\theta(\cdot) x_1)$ in Eq. (2) is similarly unclear in how the Jacobian is evaluated and what $x_1$ multiplies. More importantly, the method's concrete identification criterion $I_{\text{con}}(x,y,\theta) = |\ell(f_\theta(x),y) - \ell(f_{\theta^t}(x),y)|$ (Definition 3.3) is not derived from Eq. (2); it is a heuristic loss-change measure. The theory–method gap does not invalidate the paper—the empirical results and problem framing stand on their own—but the theoretical section claims a tighter link than it delivers.

### Minor
1. **The Gap metric aggregates four differently-scaled quantities without normalization (Section 4.1).** The Gap is defined as $\frac{1}{4}\sum|\mathcal{R}_{\text{Retrain}} - \mathcal{R}_{\text{Opt}}|$ over UA, RA, TA, and MIA. UA and MIA span 0–100, while RA and TA typically vary within narrower bands for a given setting, so the aggregate can be dominated by whichever metric deviates most in absolute terms. This does not affect the paper's main conclusions—TARF's advantage on mismatch settings is large on any individual metric—but the per-metric breakdown in the table is more informative than the aggregated Gap.

2. **Limited tuning guidance for hyperparameters.** TARF has three hyperparameters ($k$, $t_0$, $t_1$) plus the threshold $\beta$. The paper provides some guidance ($k \approx 0.05$, $\beta$ from the top-10% ordering) and includes an ablation, but the sensitivity analysis beyond all-matched is deferred to the appendix (Figure 17). The paper acknowledges this as an "open challenge" (line 359) but offers limited practical guidance for deploying TARF on a new dataset without a retrained reference for validation.

3. **The three-phase framing overclaims conceptual unification (Remark 3.3, line 186).** The paper states the phases form "a unified framework rather than an ad-hoc pipeline," but the process is sequential by design (controlled by $t_0$ and $t_1$), which is by definition a pipeline. This is not a substantive flaw—pipelines are entirely reasonable—but the framing is unnecessary and invites skepticism.

4. **The RL baseline (Toneva et al., 2018) is listed in all result tables but its relevance to unlearning is never explained.** Toneva et al. studies which examples are forgotten during standard training; the paper should clarify why this serves as a comparative unlearning baseline.

### Trivial
None.

---

## Nice-to-Haves

- Tighten the theory–method link: either derive $I_{\text{con}}$ from Eq. (2) or present the gravity effect as an empirical observation (Figure 3 already supports it well without a theorem).
- The ablation on gradient cleaning (setting gradient to 0) for $D_U$ (Figure 7, right) suggests it may be a better choice than gradient ascent for the identified false retaining data. This algorithmic insight could be explored further or incorporated into the main procedure.
- Adding an illustrative failure case where the gravity signal is weak would strengthen the paper's characterization and credibility.

---

## Removed Points

- **TOFU/LLM results appear garbled (Table 5).** The text-extracted table shows repeated row headers and duplicated method rows. This is a parser artifact—the original PDF submission does not have this issue. Per the review guidelines, formatting/parsing artifacts are not weaknesses.
- **"No failure case analysis"** was raised as a missing component. The paper's conclusion (line 359) explicitly discusses regimes where the gravity signal weakens and frames this as an open challenge, partially addressing the concern. Remaining detail is a nice-to-have, not a weakness.
- **"Baseline RL not properly cited"** — the paper does cite RL (Toneva et al., 2018) in all tables. The issue is lack of explanation of its relevance (kept as Minor weakness 4 above), not lack of citation.

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. Clean up the statement of Theorem 3.2: replace $\lambda_{\max}(J_\theta)$ with a well-defined quantity (e.g., the largest singular value of the Jacobian or a Lipschitz constant of the representation map) and clarify the matrix-vector product notation.
2. Consider reporting per-metric gaps (e.g., Gap_UA, Gap_RA, Gap_TA, Gap_MIA) alongside the aggregate Gap in the main table, or equivalently normalizing each deviation by the Retrained reference range.
3. Add a brief sentence explaining why Toneva et al.'s forgetting events are relevant as an unlearning baseline.

---

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>