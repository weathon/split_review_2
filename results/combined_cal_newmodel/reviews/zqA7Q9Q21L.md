Now I have sufficient calibration data to finalize my score. Let me compose the final review.

**Calibration anchors used (all rounds):**

| Paper | Avg Score | Decision | Round | Itemized? | Comparison |
|---|---|---|---|---|---|
| Urban Network Security (DjHnxxlqwl) | 4.75 | Reject | 1 | Yes | Weaker paper; our theoretical contributions and experiments are stronger |
| ACCES Games (7YKV7zkNpX) | 6.50 | Accept | 1 | Yes | Similar strength magnitude; our major weaknesses are worse than their worst (-2.25 lit gap) but our core contributions are empirical rather than theoretical |
| Tractable MARL (stUKwWBuBm) | 8.00 | Accept | 1 | Yes | Much stronger theoretical foundation; our paper's weaknesses are significantly more severe |
| DRDA POSGs (KD5nJUgeW4) | 7.00 | Accept | 2 | Yes | Similar strength magnitude; their low-favorability items (-1.48, -0.40) are similar to our 0.09-1.52 but they have stronger convergence theory |
| GXMFG (zwU9scoU4A) | 6.67 | Accept | 2 | Yes | Similar strengths; their worst weakness (-1.71) is comparable to ours |
| Proto Succ. Measure (s9SVlWOcLt) | 6.75 | Reject | 3 | Yes | Similar strength range but rejected despite high score; had severe experimental limitations (-3.03, -2.85) that are worse than our issues |

**Round 1 bracket:** 5.5–7.0 (paper's strengths are strong but two major weaknesses drag it below the 7+ papers).

**Narrowing:** Comparing itemized favorability, this paper's two major weaknesses (1.52, 0.09) are notably lower than any item in the 7.0+ accepted papers. However, the paper's strengths (12.03–13.74) equal or exceed the 6.5–7.0 papers. The framing overclaim is real but fixable; missing variance is a methodological gap but does not invalidate the results. The paper is a clear step above the 4.75 rejected anchor but below the 7.00–8.00 anchors.

**Final score: 6.0** — borderline accept, consistent with comparable papers that had non-fatal but significant weaknesses.

Now let me write the review.

---

Actually, I realize I should present the calibration anchors in a table in my response. Let me compile the review now.

Let me also make sure my review accounts for the hard rules properly.

Actually, looking at the weaknesses more carefully, I want to re-verify the "worst-case robust" criticism. Let me check what exactly the paper claims.

The paper title: "R2PS: WORST-CASE ROBUST REAL-TIME PURSUIT STRATEGIES UNDER PARTIAL OBSERVABILITY"

Abstract: "This paper introduces the first approach to worst-case robust real-time pursuit strategies (R2PS) under partial observability."

Contributions: "deriving the first worst-case robust real-time pursuit strategies (R2PS) applicable to dynamically changing PEGs with partial observations."

Line 268: "Since our worst-case zero-shot performance is clearly better than the PSRO policy directly trained on the test graphs, we can say that our real-time strategies are worst-case robust even under varying graph structures, which implies that our approach achieves R2PS under partial observability."

Line 311 (Conclusion): "our cross-graph policy manages to generate real-time pursuit strategies with worst-case robustness"

The paper does have Theorem 2 which gives worst-case guarantees for the DP policy. The RL policy is trained with the DP policy as reference. But the RL policy itself has no formal worst-case guarantee.

However, line 268 says "worst-case zero-shot performance" which could be read as "performance in the worst-case scenario we tested" rather than "formally worst-case robust." But the title and abstract use the term unconditionally.

I think this is a genuine weakness but not fatal. The paper should qualify the claim more carefully.

OK, finalizing now.## Summary

This paper addresses the problem of real-time pursuit-evasion in graph-based environments under partial observability. It makes three contributions: (1) a theoretical proof that a DP algorithm for Markov PEGs remains optimal under asynchronous moves by the evader (Theorems 2–3, Corollary 1); (2) a lightweight belief preservation mechanism (Eqs. 4–7) that maintains possible evader positions without exponential explosion; and (3) an RL pipeline that embeds this belief mechanism into the EPG framework to train GNN pursuit policies via cross-graph reinforcement learning against optimal DP evaders, achieving zero-shot generalization to unseen graphs. Experiments on 10 real-world maps show the RL policy matches or outperforms a PSRO baseline trained directly on the test graphs while offering orders-of-magnitude inference speedups over DP recomputation.

---

## Strengths

- **Theoretical extension to asynchronous moves is correct and non-trivial.** The paper proves (Theorems 2–3, Corollary 1) that the DP algorithm from Lu et al. (2025a) — originally analyzed only under synchronous moves — also yields strictly optimal pursuit and evasion strategies when the evader can observe the pursuers' action and react asynchronously. Lemma 1 captures the recursive structure cleanly. This is a genuine theoretical addition to the theory of graph-based PEGs.

- **Belief preservation mechanism is computationally sensible and effective.** Equations (4)–(7) define a lightweight tracking mechanism (Õ(|V|) per step) that maintains possible evader positions and a belief distribution over them. The improvement of DP\_belief over DP\_Pos in Table 1 (e.g., 0.78 vs 0.59 on Grid Map, 0.90 vs 0.73 on Downtown Map) is consistent across all 10 test graphs, showing the belief averaging genuinely helps.

- **Cross-graph RL pipeline delivers impressive zero-shot generalization.** The R2PS policy, trained on 300 graphs it has never seen, outperforms a PSRO policy trained directly on the test graphs (Table 2). Against the strongest opponent (DP\_async), R2PS achieves success rates of 0.76–1.00 on most graphs while PSRO drops to 0.00–0.52. This cleanly demonstrates real generalization value — note that the comparison is intentionally asymmetric *in favor of PSRO* (PSRO trains on the test graphs while R2PS never sees them), making the result stronger.

- **Scalability results are dramatic.** Table 3 shows RL inference times of ~0.008–0.01 seconds on a GPU vs 6–139 seconds for DP recomputation on large graphs (744–2065 nodes). The paper also provides a fair CPU-to-CPU comparison (line 201: <1 second RL vs >2 minutes DP on i9-13900HX for n=1000), validating the real-time claim on equal hardware.

---

## Weaknesses

### Fatal
None.

### Major

- **The "worst-case robust" label for the RL policy overreaches, and the central framing needs correction.** The paper uses "worst-case robust" in the title, abstract, contributions list, and conclusion to describe the RL policy (R2PS). However, only the DP strategies (μ* and ν*) carry formal worst-case guarantees (Theorem 2). The RL policy inherits no such guarantee — it is trained via imitation learning + RL against specific DP opponents on training graphs. The paper's own Table 2 shows that against a best-responding evader (BR\_async) trained adversarially against the RL policy, success rates drop sharply — from 0.95 to 0.27 on Times Square, from 0.38 to 0.10 on Hollywood Walk of Fame, from 0.99 to 0.92 on Downtown Map. The paper then claims (line 268) that "our real-time strategies are worst-case robust even under varying graph structures," conflating empirical strength against tested opponents with a formal guarantee against any opponent. The RL policy is empirically strong but *exploitable* — calling it "worst-case robust" in the title sets an expectation the evidence does not meet. This is not a minor terminological issue; it is the paper's headline claim. The fix is straightforward: reserve "worst-case robust" for the DP component and describe the RL policy as "empirically robust" or "strong across diverse graphs."

- **No statistical uncertainty is reported for any result.** All success rates in Tables 1–4 are point estimates. Table 1 says "averaged over 500 tests" but no standard deviation, confidence interval, or error bar is provided anywhere in the paper. Given the stochastic processes (initial position randomization, RL policy stochasticity, belief updates), it is impossible to assess whether reported differences (e.g., the consistent improvement of DP\_belief over DP\_Pos in Table 1) are meaningful or within noise.

### Minor

- **The belief update (Eq. 7) uses a uniform-random evader by default** (ν(v) set to uniform over Neighbor(v), line 157) rather than the actual opponent policy. This means the belief is not a true Bayesian posterior about the evader's position. The improvement of DP\_belief over DP\_Pos in Table 1 may partially come from replacing the hard max in Eq. (5) with a weighted average in Eq. (6) (softening the pessimism) rather than from belief tracking per se. An ablation comparing Eq. (6) using uniform belief vs. using the correct evader policy ν* for the DP mechanism itself would disentangle these effects. (Table 4 partially addresses this for the RL policy by comparing "Known Opponent" vs "Original," but the DP mechanism is not ablated.)

- **The transitive policy space argument (Section 4.1, line 195) is hand-wavy**, not technically grounded. The claim that "the cross-graph policy will be improved at an exponential level across a diverse training corpus" is supported only by an intuitive sketch ("Imagine that a half space is excluded…") rather than a formal argument. This over-promises relative to what is delivered.

- **No comparison against the EPG baseline itself.** Since the paper builds directly on EPG (Lu et al., 2025a), a natural baseline is EPG under perfect information (to measure the partial-observability degradation) or an EPG variant retrofitted with the belief preservation mechanism. Without this, the marginal benefit of the belief mechanism over prior work is unclear.

- **No analysis of failure cases.** When the RL policy fails (e.g., 0.20 success rate on Sagrada Familia against DP\_async, Table 2), the paper does not analyze why. Understanding whether the evader exploits a specific graph substructure or the belief set explodes would inform assessment of the method's limitations and guide future work.

### Trivial
None.

---

## Nice-to-Haves

- Include failure case analysis (e.g., what causes the 0.20 success rate on Sagrada Familia — is it graph structure, belief collapse, or policy limitations?).
- Add an EPG-based baseline to isolate the value of the belief mechanism.
- Provide an ablation for the DP belief mechanism that compares uniform belief vs. the correct evader policy ν* to separate the effect of belief tracking from the effect of softening the max operator.

---

## Removed Points

These points from the input review were removed per filtering rules:

1. **PSRO training budget inequality criticism** — REMOVED. Per hard rule: asymmetry favors the baseline (PSRO is trained directly on the test graphs while R2PS never sees them). The comparison is already stacked against R2PS, strengthening the result.

2. **CPU vs GPU timing asymmetry in Table 3** — DEMOTED to trivial then removed. The paper provides a fair CPU-to-CPU comparison (line 201: <1 second RL vs >2 minutes DP on i9-13900HX). The GPU times in Table 3 are supplemental and the text explicitly states the hardware used.

3. **Remove() operator underspecification for multi-pursuer** — REMOVED. The paper's description ("all currently observed positions") is sufficiently clear for the intended purpose; union of overlapping ranges is a straightforward inference.

4. **Section 2.1 formalism criticism** — REMOVED. The definitions are adequate for the paper's scope; the game-theoretic foundation for asynchronous moves is sufficiently connected via Theorem 2.

5. **SAC vs MAPPO choice not justified** — REMOVED. Implementation detail; the algorithm choice is not central to the paper's contribution.

6. **RL policy stochastic/deterministic at test time** — REMOVED. Minor implementation detail.

7. **"Directly applicable" overstatement about observation range (line 290-291)** — REMOVED. The claim is modest (performance monotonically increases with range, which is expected behavior).

---

## Novel Insights

The most striking finding from the review is the tension between the paper's two components: the DP component genuinely achieves worst-case robustness (Theorem 2), while the RL component — which is the paper's main deliverable — demonstrably does not, as evidenced by the sharp drop against BR\_async. This suggests a potential research direction: could the DP policy's worst-case guarantees be distilled more faithfully into the RL policy, or is the gap inherent to function approximation under partial observability? The paper does not engage with this question, but the data it provides makes it salient.

---

## Suggestions

1. **Reframe the RL policy claims.** Remove "worst-case robust" from the RL policy description in the title, abstract, and conclusion. Reserve it for the DP component. Describe the RL policy as "empirically robust" or "practically strong across diverse unseen graphs." This would bring the paper's claims into alignment with its evidence and strengthen its credibility.

2. **Add variance estimates** (standard deviations or confidence intervals) to all reported success rates in Tables 1–4. With 500 tests in Table 1, bootstrapped confidence intervals would be straightforward to compute.

3. **Add an EPG baseline** under perfect information (or EPG + belief) to quantify the marginal benefit of the belief mechanism over prior work.

4. **Add failure case analysis** for the low-success-rate graphs (especially Sagrada Familia at 0.20).

---

## Score and Decision

**Round 1 bracket (explicit):** 5.5–7.0. The paper's strengths (favorability 12.03–13.74) match or exceed accepted 6.5–7.0 papers (ACCES Games 6.50, GXMFG 6.67). However, its two major weaknesses (favorability 1.52 and 0.09) are notably lower than any weakness item in the 7.0+ accepted anchors. Round 2 narrowed by comparing against the 6.50–6.75 anchors: the overclaim and missing variance issues are fixable but push the paper below the 7.0 anchors (DRDA POSGs, Tractable MARL) which had stronger theoretical foundations. The paper is clearly above the 4.75 rejected anchor (Urban Network Security).

**Final score: 6.0** — The core contributions are genuine and significant: a clean proof of DP optimality under asynchronous moves, a practical belief mechanism, and strong cross-graph RL results with real-time inference. However, the title-level "worst-case robust" claim for the RL policy is unsupported by the evidence and requires reframing. The absence of any statistical uncertainty estimates weakens the experimental rigor. These are fixable in revision.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>