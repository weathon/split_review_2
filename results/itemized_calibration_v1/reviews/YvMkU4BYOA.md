Now writing the final consolidated review.

## Summary

XBIC augments the Bayesian Information Criterion (BIC) with Shapley values from per-node predictive classifiers to inform score-based causal discovery in discrete Bayesian networks. The method reduces BIC's complexity penalty in proportion to the aggregate directional Shapley evidence across edges in a candidate graph, aiming to guide hill-climbing toward better orientations within Markov equivalence classes. The paper reports oriented-edge F₁ improvements of +5.6% over BIC, +9.6% over GES, and +20.9% over PC across 10 benchmark networks (6–76 nodes) and 7 sample-size regimes (700 runs).

## Strengths

1. **Novel cross-domain connection.** The idea of using Shapley values from predictive classifiers to inform score-based structure search is genuinely creative. The paper correctly positions this against prior work (Frye et al., Heskes et al., Janzing et al.) that assumes a known causal graph and uses it to constrain explanations, rather than the reverse direction (§2.2–2.3). This is, to my knowledge, a novel direction.

2. **Extensive and systematic benchmarking.** The evaluation covers 10 networks across diverse domains (medical, insurance, weather, software) with varying structure (sparse to dense) and CPT sizes, at 7 sample-size regimes (§4.1). Using consistent data splits across methods is good practice. The paper honestly reports where its method does not help.

3. **Graceful degradation and honest reporting.** XBIC reverts to standard BIC when Shapley signals are weak (§3, Eq. 2, property (i)), and the paper transparently reports that small-sample regimes yield no improvement (§4.3) and that XBIC is 100–600× slower (§4.4, Table 5). The confidence threshold (§3.1) provides a principled mechanism for this default behavior.

## Weaknesses

### Fatal
None.

### Major

**1. The core mechanism — that Shapley value asymmetry from predictive classifiers tracks causal direction — is asserted but not validated.**

The paper states: "Intuitively, if $|\bar{\phi}_{1 \rightarrow 2}| \gg |\bar{\phi}_{2 \rightarrow 1}|$, the edge $X_1 \rightarrow X_2$ has stronger directional support than $X_2 \rightarrow X_1$" (§3.2). This intuition is not justified. Predictive relevance in a model that conditions on *all other variables* is not equivalent to causal direction. In chains ($X \to Y \to Z$), confounders ($X \leftarrow Z \to Y$), and colliders ($X \to Z \leftarrow Y$), Shapley asymmetry depends on the specific conditional distributions, not solely on causal structure. The paper provides no theoretical analysis, controlled synthetic experiment, or ablation to verify that $|\bar{\phi}_{j\to i}| - |\bar{\phi}_{i\to j}|$ consistently aligns with the true causal direction. Without this, the mechanism by which XBIC improves orientation is opaque, and the reported improvements could arise from a global penalty-reduction effect (adding more edges, increasing recall) rather than from correctly resolving directions — consistent with Figure 2 showing larger $w$ increases recall but sometimes reduces precision. This gap directly undermines the paper's central explanatory narrative.

**2. The evaluation protocol for PDAG-returning baselines biases directed-edge metrics against them.**

The paper states: "For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics" (§4.1). This systematically disadvantages PC and GES, which honestly mark edges whose direction cannot be resolved from observational data as undirected. Randomly orienting these unresolved edges turns the baseline's correct expression of uncertainty into random guesses, artificially lowering their directed-edge F₁. XBIC, which always outputs a direction for every edge, faces no similar penalty. The headline improvement over PC (+20.9% relative) is almost certainly inflated by this protocol. A fair comparison would evaluate all methods at the CPDAG level or use metrics that separate skeleton accuracy from orientation accuracy (e.g., Tsamardinos et al. 2006).

### Minor

**3. The "edge-specific" framing is overstated relative to the actual mechanism.**

The paper repeatedly describes XBIC as providing "edge-specific" penalty weighting (abstract, §1, §3, contributions). However, Equations 2–3 show the penalty modulation is global: $\exp(w \cdot \text{SHAP}(G))$ is a single scalar applied to the entire penalty term. The Shapley evidence is computed per edge, but its *application* is aggregate — two graphs with the same total SHAP sum but different edge compositions receive the same penalty reduction. This does not invalidate the method but creates a misleading impression of how the penalty modulation operates.

**4. Absolute F₁ gains are small, and statistical significance does not imply practical significance.**

The headline absolute improvements are +0.04 (BIC), +0.06 (GES), and +0.12 (PC) on a [0,1] scale (Table 4). With 700 runs, the adjusted Friedman and Wilcoxon tests ($p<0.05$) will detect trivially small effects. The paper does not report standardized effect sizes (e.g., Cohen's d). Table 2 further shows several (network, sample-size) combinations where XBIC's F₁ delta relative to BIC is zero or negative (e.g., Asia at $2M^2$: −0.12; Win95pts at $8M^2$: −0.09), indicating the improvements are inconsistent across settings.

**5. No ablation isolating the Shapley contribution from the broader score formulation.**

The paper compares XBIC to BIC-HC, PC, and GES but does not ablate whether the specific XBIC score formulation matters. A natural baseline would be using Shapley values as a post-processing step (e.g., re-ranking edges of a BIC-HC output by $|\bar{\phi}|$ asymmetry) or as a pruning criterion. Without this, it is unclear whether the gains derive from the specific XBIC score integration or from any method that somehow incorporates predictive Shapley information.

### Trivial
None.

## Nice-to-Haves
- A controlled synthetic experiment (e.g., small discrete DAGs with known ground-truth direction) to verify that $|\bar{\phi}_{j\to i}| - |\bar{\phi}_{i\to j}|$ consistently has the same sign as the true causal direction under varying noise levels, sample sizes, and distribution types.
- Reporting skeleton-level metrics (undirected edge F₁) alongside directed-edge metrics to separate orientation improvement from recall improvement.
- CPDAG-level comparison metrics for all methods instead of the PDAG random-orientation protocol.
- Reporting standardized effect sizes alongside p-values for headline comparisons.
- Analysis of how the confidence threshold $\tau$ alters the Shapley values themselves (sign, ranking, magnitude) rather than only downstream F₁.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *GES comparison is selectively filtered (Critic Issue 5):* The paper explicitly acknowledges that filtering is "favorable for GES" (§4.5) and conducts the comparison only on the subset where GES completed. The paper addresses this concern transparently on its own terms. **Removed** because the paper acknowledges and mitigates this issue.

- *Consistency argument is superficial (§3.3):* The paper presents this as a remark, not a formal proof, and lists formal theory as future work in the limitations. The critic demands a level of rigor the paper never claims. **Removed.**

- *No analysis of confidence threshold's effect on Shapley values (§4.1):* The paper does examine $\tau$'s effect on downstream F₁ (<1% variation). The request to analyze its effect on Shapley values themselves is reasonable but not a standard expectation. **Demoted to Nice-to-Have.**

- *No discussion of XGBoost's inductive biases:* Reasonable but minor and speculative. **Demoted to Nice-to-Have.**

## Novel Insights

The critic's analysis of why Shapley asymmetry from a fully-conditional predictor may not track causal direction — specifically the chain ($X \to Y \to Z$), confounder ($X \leftarrow Z \to Y$), and collider ($X \to Z \leftarrow Y$) cases — is a genuinely insightful formalization of the gap between predictive relevance and causal direction in the XBIC context. The observation that XBIC's signal might be strongest precisely for colliders (where standard methods already resolve direction) reframes the paper's contribution challenge usefully. This goes beyond the generic "correlation ≠ causation" observation and specifically targets the XBIC mechanism.

## Suggestions
1. Add a controlled synthetic experiment on small discrete DAGs with known ground truth to directly test whether $|\bar{\phi}_{j\to i}| - |\bar{\phi}_{i\to j}|$ consistently aligns with causal direction.
2. Replace the PDAG random-orientation evaluation protocol with CPDAG-level metrics (e.g., SHD on equivalence classes) that do not penalize baselines for honestly marking unresolvable edges.
3. Report skeleton F₁ alongside directed-edge F₁ and, within correctly-identified edges, the fraction with correct direction — to isolate orientation improvement from recall improvement.
4. Report standardized effect sizes alongside p-values for the headline comparisons.
5. Add an ablation using Shapley values as a post-processing step (e.g., re-rank edges of a BIC-HC output by Shapley asymmetry) to isolate the contribution of the specific XBIC score formulation.

## Calibration Anchors

| File | Avg Score | Round | Itemized | Comparison to This Paper |
|------|-----------|-------|----------|--------------------------|
| AvXrppAS2o.md | 3.00 | 1 | Yes | Similar: novel combination of two ideas, marginal improvements, no theoretical guarantees. XBIC has more extensive evaluation but also the PDAG bias problem. |
| JzFLBOFMZ2.md | 3.20 | 1 | Yes | Similar: external knowledge integrated into causal discovery without theoretical justification. XBIC is methodologically cleaner and better evaluated. |
| Idygh9MX0N.md | 3.40 | 1 | No | Similar: LLM + causal discovery, but different methodology space. |
| Z756zcjNcC.md | 4.50 | 1 | Yes | Comparable: novel methodology for causal discovery, limited theory. XBIC has broader evaluation but DDCD has clearer motivation for its diffusion approach. |
| l3Q0scRuT9.md | 5.00 | 1 | Yes | Somewhat weaker: incremental contribution over NOTEARS with diffusion. XBIC is more novel in idea but has execution flaws the diffusion paper does not. |
| DUfwD5yiN4.md | 5.25 | 1 | No | Stronger: exact distributed algorithm with theoretical guarantees, cleaner evaluation. |

**Round-1 bracket:** I identified 3.0–5.0 as the plausible range, with the most comparable papers sitting at 3.00, 3.20, and 4.50. XBIC has a more novel core idea than the 3.0–3.2 papers but shares their fundamental problem (unvalidated mechanism for the claimed benefit). It has more extensive evaluation than the 4.50 paper but also has a clearer evaluation bias (PDAG protocol). The weighted-item comparison places it between these anchors. **Narrowing:** the two major weaknesses (unvalidated mechanism + biased evaluation) are each severe enough to prevent acceptance, pushing the score below 4.0, while the genuine novelty and benchmarking scope prevent a strong reject, setting the floor above 3.0. Final score: **3.5**.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>