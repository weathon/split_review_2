Now I have all the information I need. Let me produce the final review.

## Summary

This paper studies single-node conditional-intervention causal bandits — a setting where the agent can intervene on one node at a time, setting its value based on observed context variables. The core contribution is a graphical characterization: the minimal set of intervention nodes guaranteed to contain the optimal intervention equals the LSCA (Lowest Strict Common Ancestor) closure of Pa(Y), the parents of the target variable. The paper also proposes the C4 algorithm (linear in |V|+|E|) to compute this set, provides search-space-reduction experiments on random and real-world graphs, and runs bandit experiments with a UCB-based conditional-intervention algorithm.

## Strengths

1. **Well-motivated and formally clean problem definition.** The paper correctly identifies that conditional interventions (where the intervention value depends on observed context) are more realistic than hard interventions for many applications, while most prior causal bandit work assumes hard interventions. The formalization in Section 2 (conditional interventions, observable conditioning sets, the conditional causal bandit problem) is clear and precise.

2. **The LSCA-closure characterization is elegant and fills a genuine gap.** The paper identifies why the simpler LCA (Lowest Common Ancestor) notion fails (Figure 1d) and introduces LSCAs to close it. The Λ-structure characterization (Theorem 12) provides an intuitive graphical interpretation. The C4 algorithm using connectors is a clever practical contribution — linear time in |V|+|E| is optimal for this task.

3. **Uniqueness of the mGISS (Proposition 6) is non-trivial and correctly established.** Without uniqueness, "the" minimal search space would be ill-defined, so this result is important for the framework.

4. **Search-space-reduction experiments are solid.** They measure a well-defined quantity (fraction of ancestor nodes retained in mGISS) across varying graph sizes and densities, and on real-world graphs from the bnlearn repository. The results convincingly demonstrate that mGISS can be dramatically smaller than the full ancestor set in sparse graphs, which matches real-world causal graphs.

## Weaknesses

### Fatal
None — the core theoretical contribution (the LSCA-closure characterization, Proposition 6, Theorems 12–13, and the C4 algorithm) does not depend on the bandit experiments and stands on its own.

### Major

1. **Unsound regret computation in the bandit experiments.** The paper states (footnote 11): *"For the computation of regret, we use the estimated best arm, defined as the arm that most runs concluded to be the best at the end of training."* Regret is standardly defined as Tμ\* − ΣE[Y_t], where μ\* is the *true* optimal mean reward. Defining μ\* based on the algorithm's own consensus across runs conflates the estimation of the best arm with the evaluation of regret. If the algorithm systematically converges to a suboptimal arm in many runs, that suboptimal arm becomes the "best" by this circular definition, and the resulting regret values are not interpretable as true regret. The gap between the mGISS and brute-force curves in Figure 3 could partly reflect that the two settings converge to different consensus arms, not that one converges to the true optimum faster. This compromises the paper's claim that pruning with mGISS "substantially accelerates convergence rates."

   *Why this is Major, not Fatal:* The search-space-reduction experiments (graph-only, measuring mGISS size relative to ancestor set) are not affected by this issue. The core theoretical contribution is independent of the bandit experiments. The claim about convergence speed is the only unsupported part.

### Minor

1. **SCM parameters for bandit experiments unspecified.** The paper does not describe how the SCM parameters (structural assignments, noise distributions) are set for the bnlearn graphs used in the bandit experiments. While code is submitted, the paper itself should state whether it uses the original CPTs from bnlearn, randomly generated parameters, or some other scheme. Without this, the bandit results are not self-contained.

2. **CondIntUCB algorithm underspecified.** The description (one paragraph) omits key implementation details: the UCB exploration parameter, the number of rounds, how the value ranges R_X are set, and how policies g are learned. These details matter for assessing whether the bandit results are robust or artifacts of a particular implementation.

3. **No proof sketch of Proposition 4 in the main text.** Proposition 4 (equivalence between conditional-intervention superiority over stochastic SCMs and deterministic atomic-intervention superiority over pointwise outcomes) is the linchpin connecting the paper's conditional-intervention problem to the deterministic setting used in the theory. The equivalence is genuinely non-obvious (the paper itself calls it "perhaps surprising"). While relegating proofs to the appendix is standard practice, a brief sketch of the proof's structure in the main text would significantly increase reader trust in this critical result.

4. **No comparison against simpler pruning baselines.** The paper compares mGISS only against "brute-force" (all ancestors of Y). Comparisons against simpler alternatives (e.g., Pa(Y) only, or Pa(Y) ∪ LCA(Pa(Y))) would clarify whether the full LSCA machinery adds value beyond simpler heuristics. Since the paper already computes these sets (LCA is a subset of LSCA), this comparison would not require additional experiments.

### Trivial
None.

## Nice-to-Haves

- Compare against Pa(Y) ∪ LCA(Pa(Y)) as a baseline to quantify the additional pruning provided by the full LSCA closure.
- Provide a proof sketch of Proposition 4 in the main text (2–3 sentences explaining the reduction structure would suffice).
- Clarify the choice of Y (node with most ancestors) and discuss how alternative choices affect mGISS size.

## Removed Points

These points were raised by the harsh critic but are removed per the filtering rules:

- **"Proposition 4 proof is in the appendix and not visible"** — REMOVED: The parser strips appendices from all papers; the proof exists in the original submission. The softer point about wanting a proof sketch in the main text is retained as a Minor weakness above.
- **"Claim about single-node interventions being more challenging is stated without justification"** — REMOVED: The paper justifies this at line 98 (*"if one allows for interventions on arbitrary sets, one simply needs to intervene on all the parents of Y"*).
- **Formatting/parser artifact complaints** (e.g., garbled notation in Definition 1) — REMOVED: These are parser errors, not author errors.
- **Speculative concern that Proposition 4 might be incorrect** — REMOVED: The critic cannot verify the proof (appendix stripped), and a speculative concern about a proof one has not read is not a valid weakness.
- **"No discussion of why uniqueness holds"** — REMOVED: The proof is in the appendix (Proposition 6). The paper states the result and defers the proof, which is standard practice.

## Novel Insights

The harsh critic correctly identifies that the regret computation using "estimated best arm" is the paper's most significant weakness. This is a genuine problem because the paper's claim of "substantially accelerating convergence rates" depends on this analysis, and the methodology is not standard. However, the critic overstates the severity of some other concerns: the search-space-reduction experiments are independently valuable and methodologically sound, the theoretical contribution does not depend on the bandit experiments, and the demand for alternative baseline comparisons (while reasonable as a nice-to-have) does not threaten the paper's core claims. The critic's observation that the paper would be "a solid theory paper with weak experiments" captures the balance well — the theory is the main contribution, and the experiments need honest reframing.

## Suggestions for Authors

1. **Fix the regret computation** by replacing the "estimated best arm" definition with the true optimal arm (which can be identified given fully specified SCM parameters). This would make the regret curves in Figure 3 interpretable as evidence for faster convergence.
2. **Reframe the paper's applied claims.** If fixing the regret computation is not feasible, honestly state that the bandit experiments illustrate relative performance between mGISS and brute-force under the same bandit algorithm, and remove claims about "substantially accelerating convergence rates."
3. **Specify SCM parameters** for the bnlearn bandit experiments (original CPTs or randomly generated; the generation procedure).
4. **Add a brief proof sketch of Proposition 4** (2–3 sentences) in the main text explaining how the reduction from conditional-stochastic to deterministic-atomic works.

## Score and Decision

### Calibration Anchors

| Path | Avg Score | Round | Itemized? | Comparison to This Paper |
|------|-----------|-------|-----------|--------------------------|
| IPayPEGwdE.md (Causal Contextual Bandits with Adaptive Context) | 5.00 | R1 | Yes | Similar topic (causal bandits + theory + experiments). Weaker theory (simple chain graph vs full DAG). Poor baseline comparisons. My paper has richer theory but similar experimental issues. |
| YcW8i9VCf5.md (Adversarial Causal Bayesian Optimization) | 6.00 | R1 | Yes | Causal BO with external interventions. Mostly minor weaknesses (-1 weight items). My paper has one heavier weakness (flawed regret experiments), placing it slightly below. |
| MVpvyeVeyI.md (Causal BO with Unknown Graphs) | 6.50 | R1 | Yes | Strong writing, clear limitations. Some restrictive assumptions. My paper has cleaner theory but worse experimental support for convergence claims. |
| Various strong-reject anchors (GFlowNets, minimax paths, financial networks) | 1.00 | R1 | No | Completely different topics; not relevant for calibration. |

### Score Determination

**Round 1 bracket:** [5.0, 6.5] — the paper's theory is substantially richer than IPayPEGwdE (5.00) which used only a simple chain graph and had no baseline comparisons, but its experimental flaw pushes it below YcW8i9VCf5 (6.00) whose weaknesses were mostly minor notation/communication issues.

**Final placement:** The paper shares with IPayPEGwdE (5.00) the weakness of insufficiently rigorous experimental methodology (weight -4 for missing comparisons there; weight comparable for flawed regret computation here). It lacks the heavy-weight novelty concerns that pulled YcW8i9VCf5 down (weight -3 for "no fundamental difference") — this paper's LSCA-closure characterization is genuinely novel. The theory is solid, the C4 algorithm is clean, and the search-space-reduction experiments are convincing. The bandit-regret flaw is real but does not invalidate the theoretical contribution.

**Score: 5.5** — the paper makes a meaningful theoretical contribution that a rebuttal can salvage (by fixing or honestly reframing the regret experiments). The theory alone warrants borderline acceptance, but the overclaimed experimental support pulls the score below the clear-accept threshold.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>