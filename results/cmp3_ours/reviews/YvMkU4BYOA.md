Now I have a solid anchor comparison. Let me finalize.

## Summary

This paper proposes XBIC, a modification of the BIC score for score-based causal discovery in discrete Bayesian networks. The key idea is to use per-node XGBoost classifiers to compute Shapley attributions between variables, then soft-weight BIC's complexity penalty: edges with strong directional Shapley support are penalized less, while the score defaults to standard BIC when evidence is weak. The method is evaluated on ten benchmark discrete networks (6–76 nodes) across seven sample-size regimes, totaling 700 runs.

## Strengths

- **Genuinely novel and well-motivated core idea.** Using local Shapley attributions to inject directional information into a score-based causal discovery objective is a creative cross-pollination between XAI and causal discovery. The paper clearly distinguishes this from prior work that uses causal knowledge to *constrain* explanations (Frye et al. 2020; Heskes et al. 2020), establishing a clear and novel direction (Sections 2.2–2.3). The claim of being "the first to directly integrate local feature attributions as an edge-specific, directional modulation of a score-based objective" (line 58) is supported by the literature review.

- **Graceful degradation to BIC when evidence is weak.** When the Shapley signal is absent (w=0, or no confident predictions pass the threshold), XBIC reverts exactly to standard BIC. This safety property means the method cannot degrade arbitrarily below the baseline in low-signal regimes, and the paper's results on small samples confirm this behavior (Table 2, many near-zero entries on small networks).

- **Evaluation breadth.** The evaluation spans 10 networks (6–76 nodes), 7 sample-size regimes, and 700 runs — a solid scope for a causal discovery paper. Table 2's per-network, per-regime presentation allows readers to assess consistency rather than relying on a single aggregate number.

- **Honest discussion of limitations.** The paper openly acknowledges computational overhead (Table 5, 100–2000× slowdown over BIC on small networks), limited benefit in small-sample regimes, and scalability constraints. The limitations section (lines 313–317) is substantive and thoughtful.

## Weaknesses

### Fatal

None.

### Major

- **PDAG→DAG completion protocol inflates comparisons with PC and GES.** Lines 190–191 state: *"For baselines that return a PDAG, we complete it to a DAG by randomly orienting undirected edges (while preserving acyclicity) before computing directed-edge metrics."* This is a genuine evaluation concern. PC and GES output PDAGs/CPDAGs precisely because certain edge orientations are *not identifiable* from the data — the data do not distinguish between the two directions. Randomly orienting these edges guarantees that roughly half of the previously-undetermined orientations will be wrong by chance, artificially lowering precision, recall, and F₁ for PC and GES. XBIC (a score-based search producing a DAG) never suffers this penalty.

  The clean comparison — XBIC-HC vs BIC-HC, where both output DAGs — is unaffected and shows a 5.6% relative / 0.04 absolute F₁ improvement (Table 4). But the headline numbers in the abstract (+20.9% over PC, +9.6% over GES) mix comparisons contaminated by this protocol with the clean BIC-HC comparison. The actual improvement over the correct comparator (BIC-HC) is an absolute 0.04 F₁.

### Minor

- **The XBIC score (Eq. 2) is not strictly decomposable per family, making the claim that "rescoring is local" imprecise.** The penalty term's denominator depends on SHAP(G) = Σ_{(j→i)∈E(G)} |φ̄_{j→i}|, which sums over *all edges* in G. Changing one edge changes the penalty coefficient applied to *every* family's parameter count. The paper claims "Caching local families keeps rescoring cost low" (line 131) and "rescoring is local" (line 153), which is technically inaccurate in the strict sense. However, the practical impact is limited because the global term SHAP(G) is cheap to recompute (just a sum of absolute values and one exponentiation). The slowdown from 0.39s (BIC on Asia) to 74.78s (XBIC) is overwhelmingly driven by the front-loaded attribution phase, not the search-phase rescoring.

- **The GES comparison is reported over a non-representative subset without caveat in the abstract.** GES exceeded the 7-day time limit on most settings for larger/denser networks (Table 2 shows "—" for many entries, especially on Alarm, Insurance, Water, Hailfinder, Win95pts, Hepar2). The comparison covers only the subset where GES completed, which systematically excludes harder settings. The paper acknowledges this in Section 4.5, but the abstract reports "+9.6% over GES" without this caveat.

- **The confidence threshold τ used in the main experiments is not explicitly stated.** Algorithm 1 takes τ as input, and Section 4.1 mentions that varying it between 0.7 and 0.95 changed F₁ by <1%, but the actual value used for the Table 2 results is not stated. While the sensitivity analysis partially mitigates this, the exact value should be specified for reproducibility.

- **No diagnostic analysis of when the method works and when it doesn't.** Table 2 shows XBIC's advantage varies widely: consistent gains on Sachs, Insurance, Hailfinder; near-zero or negative on Water, Hepar2, Asia. The paper does not attempt to explain this variation in terms of network properties (e.g., Markov equivalence class size, degree of determinism in CPDs, average parameter count). Such analysis would strengthen the scientific contribution.

### Trivial

None.

## Nice-to-Haves

- A synthetic diagnostic experiment (e.g., a simple 3-variable confounder and 3-variable chain with known discrete CPDs) directly validating that the Shapley asymmetry |φ̄_{j→i}| vs |φ̄_{i→j}| points in the correct causal direction would strengthen the paper's core assumption, which is currently untested in isolation.
- Decomposing runtime into search-phase cost vs. front-loaded attribution phase would clarify how much of the slowdown is due to the non-decomposability of XBIC vs. the attribution computation itself.

## Removed Points

These points are flagged to be removed, treat them with caution:

1. **"The absolute improvement over the correct baseline (BIC-HC) is very modest (0.04 absolute F₁)."** — This is a factual observation confirmed from Table 4. However, it is a judgment call that reasonable readers can disagree on; 0.04 F₁ is small but the improvement is consistent across many settings. This is better left as context for the significance evaluation rather than listed as a weakness per se.

2. **"The non-decomposability is an unacknowledged practical concern that further weakens the method's appeal as a 'drop-in upgrade'."** — Overstated. The global term SHAP(G) is cheap (just a sum of absolute values). The paper's phrasing is imprecise, but the practical impact on search cost is negligible compared to the front-loaded attribution phase. Demoted from the harsh critic's stronger framing to its current Minor tier.

3. **Various generic strengths (e.g., "the paper is well-written," "addresses an important problem")** — Removed for lacking specificity. The kept strengths are concrete and evidenced.

## Novel Insights

The input reviews do not surface genuinely novel observations that go beyond the paper's own contributions. The insight that the PDAG→DAG completion protocol is a known evaluation pitfall in causal discovery is useful but not novel; the observation about score non-decomposability is technically a correction of a minor imprecision rather than a novel insight.

## Suggestions

1. **Fix the PDAG evaluation protocol.** Instead of randomly orienting undirected edges, evaluate PC and GES on the directed-edge subset of their output (compute precision/recall only on edges they orient, with undirected edges excluded or counted separately). This is a post-processing change that would not require rerunning experiments. Alternatively, report both PDAG-level skeleton metrics and directed-edge metrics separately.

2. **Benchmark primarily against BIC-HC.** Acknowledge that PC and GES belong to different method families and that the PDAG output format makes direct DAG-level comparison problematic. Narrowing the focus to "XBIC-HC vs BIC-HC" as the central experiment would make the contribution cleaner and more defensible.

3. **State the confidence threshold τ explicitly** in the main text, and consider adding a diagnostic analysis of when XBIC helps (relating gains to network properties such as equivalence class size, parameter count, or CPD determinism).

4. **Caveat the GES comparison in the abstract.** The +9.6% figure should note that it is computed only on the subset where GES completed within 7 days.

---

## Score and Decision

### Calibration

Round 1 bracket estimate: **4.0 – 6.0**. The paper is well above the 1–3 range (genuinely novel idea, thorough evaluation, well-written). It is below the 6.5–8 range (evaluation flaw inflates some comparisons, and gains over the proper baseline are modest at 0.04 absolute F₁).

| Retrieval Anchor | Avg Score | Decision | Round | Comparison |
|---|---|---|---|---|
| DAG-SHAP (`ljZFM2mhbR.md`) | 5.00 | Reject | R1b3 | Shapley + DAG work, rejected due to known-graph assumption. Similar quality, thoroughness, and novelty level to XBIC. |
| ExDBN (`eqQFBnjjPP.md`) | 4.00 | Reject | R1b3 | Exact DBN learning. Less novel, less thorough evaluation than XBIC. |
| PIT (`orD5t7blqV.md`) | 4.25 | Reject | R1b3 | Improved PC algorithm. Less novel idea than XBIC. |
| Causal Graph Learning via Distributional Invariance (`Lxst78Rrwj.md`) | 5.00 | Reject | R2 | Novel invariance-based causal discovery. Had a fundamental theoretical concern about core method. Similar evaluation quality to XBIC. |
| Exact Distributed Structure-Learning (`DUfwD5yiN4.md`) | 5.25 | Reject | R2b3 | Distributed BN learning. Novel theory but limited comparison. |
| DrBO (`8muemqlnG3.md`) | 6.50 | Accept | R1b4 | Bayesian optimization for DAG learning. Stronger empirical results and cleaner evaluation than XBIC. |
| Causal Discovery via Bayesian Optimization (`8muemqlnG3.md`) | 6.50 | Accept | R2b4 | Strong method with dramatic improvements. XBIC has less impressive gains. |

The paper is closely comparable in quality to anchors scoring 5.0 (e.g., DAG-SHAP, Causal Graph Learning via Distributional Invariance). Both the DAG-SHAP paper and this one have genuinely novel ideas incorporating Shapley values into causal-graph-related tasks, thorough evaluations, and clear weaknesses that prevent acceptance in current form. The XBIC paper is arguably more practical (does not require a known graph), but the evaluation flaw (PDAG→DAG protocol) is more clearly fixable than DAG-SHAP's known-graph limitation. Overall, the paper is a **borderline case** — the core idea is novel and the evaluation is thorough, but the protocol inflates headline comparisons and the real gain over the proper baseline is modest.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>