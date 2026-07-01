## Summary

This paper proposes XBIC, a score-based causal discovery method for discrete Bayesian networks that augments the standard BIC score with Shapley-value-based directional evidence. For each variable, a classifier is trained to predict it from all others; TreeSHAP attributions are aggregated across confident predictions to produce edge-specific signals $|\bar{\phi}_{j\to i}|$. These signals are used to softly down-weight BIC's complexity penalty for edges with strong directional support ($\text{XBIC}_w = \log P(D|G) - \frac{\log N}{2}\frac{\dim(G)}{\exp(w\cdot\text{SHAP}(G))}$). The method is evaluated on 10 benchmark networks (6–76 nodes) across 7 sample-size regimes.

## Strengths

- **Novel conceptual direction.** Using explanations (Shapley values) to inform causal structure learning, rather than the reverse, is a genuinely different framing. This cleanly distinguishes the paper from prior work such as Frye et al. (2020) and Heskes et al. (2020), which assume the causal graph is known.

- **Elegant integration with BIC.** The formulation in Equation 2 preserves BIC as a special case when $w=0$ or $\text{SHAP}(G)=0$, and maintains $O(\log N)$ penalty growth. The "drop-in upgrade" framing is accurate: a practitioner can substitute XBIC for BIC in an existing hill-climbing pipeline without changing the search algorithm.

- **Broad empirical evaluation.** 10 networks, 7 sample-size regimes, 700 total runs, with multiple baseline families (BIC-HC, PC, GES) covering major approaches to discrete causal discovery. Code and data splits are released.

## Weaknesses

### Fatal
None.

### Major

- **PC evaluation protocol inflates the headline +20.9% result.** As stated in the paper (line 190): "For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics." PC's undirected edges represent genuine ambiguity under the Markov equivalence class — randomly orienting them adds noise and systematically degrades PC's directed-edge metrics. This is not standard practice; the standard approach evaluates at the PDAG level or reports orientation F1 only on edges PC actually oriented. The largest headline number (+20.9% over PC) is therefore misleading, as it compares XBIC's fully-directed output against a deliberately degraded version of PC.

- **The core claim — that Shapley asymmetry encodes causal direction — is asserted without support, and the mechanism is not isolated from simple penalty softening.** Line 127 states: "Intuitively, if $|\bar{\phi}_{1 \rightarrow 2}| \gg |\bar{\phi}_{2 \rightarrow 1}|$, the edge $X_1 \rightarrow X_2$ has stronger directional support than $X_2 \rightarrow X_1$." This intuition is not theoretically justified (no analysis of when/why the asymmetry should track causal direction rather than general predictive relevance), and no controlled experiment isolates it. Meanwhile, the paper's own observation (line 237) that "larger $w$ tends to increase recall (more edges admitted) while sometimes reducing precision, as expected from a softer penalty" is fully consistent with the alternative explanation that XBIC's $F_1$ improvements come from uniformly reducing the complexity penalty (thereby favoring denser graphs) rather than from correct orientation. Without an ablation that compares XBIC against a version of BIC with a uniformly reduced penalty (e.g., $\text{BIC}_\lambda = \log P(D|G) - \lambda \cdot \frac{\log N}{2}\dim(G)$ for a constant $\lambda<1$), the specific role of the Shapley signal remains unclear.

- **GES comparison is on a selective, non-representative subset, yet presented as a headline result.** The paper acknowledges (line 278) that GES "exceeded the 7-day limit in many settings" and that comparisons were limited to the subset where GES completed. The +9.6% over GES in the abstract is computed on this non-representative subset (the easier, smaller cases where GES finishes). While the paper notes this filtering is "favorable for GES," presenting it as an aggregate improvement without prominently flagging the selection at the point of the claim weakens the evidence.

### Minor

- **No absolute baseline $F_1$ values are reported.** Table 4 reports only deltas (e.g., +0.04 absolute over BIC). Without knowing whether the BIC baseline $F_1$ is 0.50 or 0.90, the reader cannot assess the practical significance of the improvement. A supplementary table of absolute metrics should be included.

- **Consistency claim (lines 155–159) is hand-wavy.** Standard BIC consistency proofs rely on the penalty dominating spurious likelihood contributions as $N\to\infty$. Dividing the penalty by $\exp(w\cdot\text{SHAP}(G))$ weakens this dominance, and the paper provides no argument that $\text{SHAP}(G)$ decays appropriately with $N$ for incorrect graphs. The remark that this "preserves large-sample consistency under standard regularity conditions" is asserted without proof or citation.

- **Confidence threshold $\tau$ sensitivity analysis is too narrow.** The paper reports (line 194) that varying $\tau$ between 0.7 and 0.95 changes downstream $F_1$ by $<1\%$, but this does not test whether the *directional signal itself* ($\bar{\phi}_{j\to i}$ values) changes qualitatively, or what happens at lower thresholds (e.g., $\tau=0.5$). The excluded low-confidence instances could be those where causal relationships are weakest, and filtering them might overstate directional evidence.

- **Use of absolute Shapley values is not motivated.** Equation 3 uses $|\bar{\phi}_{j\to i}|$, discarding the sign of Shapley values. If $\bar{\phi}_{j\to i}$ is large and negative (indicating $X_j$ suppresses $X_i$), the paper's formulation treats it identically to a large positive attribution. This design choice is not discussed.

- **No ablation with permuted/randomized Shapley values.** A straightforward sanity check — comparing XBIC against a version where $\bar{\phi}_{j\to i}$ values are randomly permuted across edges — would test whether the specific directional pattern of attributions is responsible for the improvement, or whether any edge-specific weighting would suffice.

### Trivial
None.

## Nice-to-Haves

- **Controlled synthetic test of directional Shapley asymmetry.** Generate data from a simple two-variable causal model ($X\to Y$) with known ground truth and show that $|\bar{\phi}_{X\to Y}| - |\bar{\phi}_{Y\to X}|$ correlates with true direction across varying noise levels, nonlinearities, and cardinalities.
- **Orientation accuracy conditioned on correct skeleton.** Restrict evaluation to edges whose skeleton is correctly identified by all methods, and compare only whether the *direction* is correct — directly testing the orientation-within-Markov-equivalence-classes claim.
- **Guidance on selecting $w$ in practice.** Without a validation set with known ground truth, how should a practitioner choose $w$? Cross-validated log-likelihood or stability across bootstrap samples could be discussed.
- **Parallelized wall-clock times.** The paper claims the method "parallelizes naturally" but reports only single-machine runtimes.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"The 50–200× runtime overhead further limits practical significance"** — Removed because the paper explicitly acknowledges this limitation (line 313, "Runtime" under Limitations) and frames XBIC as suitable for "offline discovery." Retaining this as a main weakness would double-count a self-acknowledged trade-off. It is moved to Nice-to-Haves as a parallelization suggestion.

- **"The +9.6% over GES should not be presented as a headline result without clear caveat"** — Partially removed because the paper *does* include the caveat (lines 278–279), though it could be more prominently placed. The point is retained in weakened form under Major weaknesses (selective subset issue), but the phrasing about "should not be presented" is removed as overly strong given the paper's own qualification.

- **"No ablation with permuted Shapley values"** — This is a legitimate suggestion but falls under "strengthening the paper on its own terms" rather than a structural flaw. Demoted to Minor weakness.

- **"The weight $w$ selection is unresolved"** — Moved to Nice-to-Haves, since this is a practical deployment concern, not a flaw in the paper's own evaluation (which sweeps $w$ and reports results).

- **"The paper's Limitations section omits the most fundamental one: the lack of causal grounding for the Shapley asymmetry"** — This is a framing observation, not a separate weakness; it is subsumed under the second Major weakness above.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's key insight — that the observed $F_1$ gains could equally arise from a simple penalty-softening effect rather than from the Shapley directional signal — is well-taken but represents a critique of the evidence rather than a novel positive insight. The merging of the generality of the PC evaluation problem with the mechanism-ambiguity problem into a unified assessment of the paper's evidential strength is the main synthetic observation.

## Suggestions

1. **Fix the PC evaluation protocol.** Report PC's performance at the PDAG/CPDAG level (using SHD on CPDAGs or orientation F1 only on oriented edges), or use a principled method to complete the PDAG (e.g., assign directions by optimizing BIC on the restricted space). Without this, the +20.9% claim is unreliable.
2. **Add an ablation that isolates the Shapley signal from penalty softening.** Compare XBIC against BIC with a uniformly reduced penalty (constant scalar $\lambda<1$). If the uniform reduction matches XBIC's $F_1$, the Shapley signal is epiphenomenal.
3. **Report absolute $F_1$ values for all baselines** alongside the deltas, and include standard deviations or confidence intervals.
4. **Add a controlled two-variable synthetic experiment** showing that $|\bar{\phi}_{j\to i}| - |\bar{\phi}_{i\to j}|$ correlates with true causal direction across different noise levels and cardinalities.

## Score and Decision

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>