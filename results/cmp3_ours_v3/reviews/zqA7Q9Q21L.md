## Summary

This paper addresses real-time pursuit under partial observability in graph-based pursuit-evasion games (PEGs). It makes three contributions: (1) proving that a dynamic programming (DP) algorithm's distance table yields strictly optimal strategies under asynchronous evader moves (Theorems 2–3); (2) proposing a computationally efficient belief-preservation mechanism (O(|V|) per timestep) that extends DP policies to partial observability by maintaining a set of possible evader positions and a weighted belief over them; and (3) embedding this mechanism into an EPG-based cross-graph RL pipeline (R2PS) that trains a GNN pursuer policy capable of zero-shot generalization to unseen graphs. Experiments on 10 real-world and synthetic graphs show the policy consistently outperforms a PSRO baseline and achieves sub-0.01s GPU inference vs. minutes for DP recomputation.

## Strengths

- **Theoretically clean extension to asynchronous moves (Section 3.1, Theorems 2–3, Lemma 1).** The paper proves that the distance table D produced by Algorithm 1 yields strictly optimal strategies for both pursuer and evader under asynchronous moves, where the evader observes the pursuers' action before moving. This is a genuine theoretical contribution that extends the DP framework beyond the synchronous-move setting assumed by prior work.

- **Computationally efficient belief preservation mechanism (Section 3.2, Eqs. 4–7).** The Pos-update rule and belief propagation cost O(|V|) per timestep. The ablation in Table 4 shows that reducing belief-update frequency from every step to every 2 or 3 steps degrades success rates substantially (e.g., Downtown Map: 0.92 → 0.61 → 0.39), providing empirical evidence that the mechanism is doing useful work.

- **Inference time advantage is substantial (Section 5.3, Table 3).** The paper reports sub-0.01s GPU inference (0.007–0.010s per step) vs. minutes (6–139s) for DP recomputation on graphs with 744–2065 nodes. This directly supports the "real-time" applicability claim and is the paper's clearest practical contribution.

- **Cross-graph zero-shot generalization demonstrated against a meaningful baseline (Section 5.2, Table 2).** The R2PS policy, trained only on a separate set of 300 graphs (150 synthetic + 150 random urban Google Maps graphs), consistently outperforms a PSRO policy trained directly on the 10 test graphs, across multiple evader types (Stay, DP_sync, DP_async). This is a nontrivial result suggesting the training procedure extracts transferable structure.

## Weaknesses

### Major

- **Missing ablation that isolates the belief mechanism's contribution within the RL training pipeline.** The paper repeatedly states that it "embeds the belief preservation into the state-of-the-art EPG framework" (abstract, line 9; Section 4.1). However, the evaluation never compares against an RL policy trained *without* the belief mechanism under the same EPG-style framework — for example, using only the Pos set without belief averaging, or using a recurrent network on observations. The sole baseline (PSRO) differs in the entire RL framework (training paradigm, objective, guidance structure), not just the belief component. Without such an ablation, it is impossible to determine whether the reported generalization gains come from the EPG training framework, the belief mechanism, or their combination. This is the most significant evidential gap relative to the paper's claimed contribution.

### Minor

- **"Worst-case robust" claim is not well calibrated to the evidence.** The title and abstract claim "worst-case robust" strategies, but against the BR_async evader (a best-responding opponent trained specifically to counter the learned policy), success rates are as low as 10% (Hollywood Walk of Fame), 20% (Sagrada Familia), and 23% (The Bund) in Table 2. The paper defines "robust" relative to PSRO (line 268: "clearly better than the PSRO policy"), which is a defensible but substantially weaker interpretation than the absolute "worst-case robust" framing in the title and abstract suggests. The claims should be calibrated to what is actually demonstrated.

- **No variance or confidence intervals reported.** All success rates in Tables 1–4 are point estimates averaged over 500 tests, but no standard deviations, confidence intervals, or multi-seed results are provided. This makes it impossible to assess the stability of the reported numbers or the statistical significance of the comparisons, particularly when PSRO rates are near zero on several graphs (e.g., 0.00 on Hollywood Walk of Fame, Sagrada Familia against DP_async in Table 2), where small random fluctuations could produce meaningfully different results.

- **Potential training/test overlap for Google Maps data needs explicit clarification.** The training set includes "150 random urban locations from Google Maps" (line 238), and the test set includes "Downtown Map (a real-world location from Google Maps)" (line 211). The Downtown Map has 206 nodes (≤ the 500-node maximum for training graphs). The paper asserts that "our training process never comes across the test graphs" (line 261) but does not explicitly confirm that the Downtown Map and the 7 real-world spots were excluded from the 150 random urban Google Maps samples. This should be clearly stated.

- **The belief mechanism is a heuristic, not a principled POMDP belief.** The belief update (Eq. 7) defaults to a uniform evader policy (line 157: "set to be a uniform distribution over Neighbor(v) by default"). This means the "belief" is not an actual posterior over evader positions unless the evader's policy is uniformly random. The paper acknowledges this implicitly but frames it as a minor default assumption; it is actually a significant limitation that makes the belief a heuristic reachability weighting scheme rather than a principled belief-state representation.

- **Partial observability extension is heuristic with no optimality guarantees (Section 3.2).** Lemma 2 only guarantees reduction to optimality when Pos is a singleton (unlimited observation). Beyond this trivial case, the paper acknowledges (line 234) that "D(·) becomes an optimistic estimator under partial observability." The theoretical contribution of Section 3 is limited to the asynchronous-move setting (Theorems 2–3, which are properly proved); the partial observability extension is empirically motivated. The paper's framing in the introduction and contributions occasionally blurs this distinction, potentially misleading readers about what is proved vs. what is heuristic.

### Trivial

None.

## Nice-to-Haves

- A comparison against the original EPG framework under full observability would help quantify the cost of partial observability.
- An analysis of the training corpus's structural diversity (e.g., degree distribution, treewidth, diameter range) would strengthen the generalization claims.
- A discussion of failure cases — particularly on graphs where success rates against BR_async are ≤20% — would be informative for future work.

## Removed Points

These points were raised by the harsh critic and removed for the stated reasons:

- **"No comparison against EPG"** — Reframed and kept as the Major weakness above (missing ablation isolating belief vs. EPG contribution), but the framing as a direct "comparison against EPG" was softened because EPG requires full observability, so a direct comparison would need a different setting.
- **"Criticism about 'first' claim needing contextualization"** — Removed as a minor framing point that cannot be fully verified without comprehensive literature audit; the paper's claim is bounded to graph-based PEGs with the specific DP+RL combination.
- **"Section 2.1: asynchronous moves deserves more formal treatment"** — Removed as a presentation nitpick.
- **"Section 2.2: pure-strategy NE condition is nontrivial"** — Removed because this concerns an assumption inherited from prior work (EPG), not the paper's own contribution.
- **"Section 5.1: shortest-path baseline is too weak"** — Removed; the paper presents this as an intuitive reference, not a competitive baseline.
- **"Section 5.3: known opponent condition is unrealistic"** — Removed; Table 4's "known opponent" condition is an informative upper-bound ablation, not a claimed contribution.
- **"No evaluation with different pursuer numbers"** — Removed; the paper justifies the m=2 setting and a full evaluation at m={1,3} is scope expansion.
- **"No analysis of training corpus diversity"** — Moved to Nice-to-Haves.
- **"No discussion of failure cases"** — Moved to Nice-to-Haves.
- **"Code link is missing"** — Removed; this is a parser artifact (stripped from submission format).

## Novel Insights

None beyond the paper's own contributions. The harsh critic's review and strengths/weaknesses analysis do not surface any observation about the paper that goes substantially beyond what the paper itself claims or discusses.

## Suggestions

The single highest-leverage improvement would be an ablation experiment comparing R2PS (trained with belief-averaged guidance) against an otherwise-identical RL policy trained with position-only guidance (using μ(s_p, Pos) from Eq. 5 as the reference policy instead of μ(s_p, belief) from Eq. 6, with all other training parameters held constant). This would directly isolate the value added by the belief-averaging component within the RL pipeline and address the most significant evidential gap. Second, clarifying the definition of "worst-case robust" (e.g., "outperforms the PSRO baseline under the strongest evader across unseen graphs") and adjusting the title accordingly would make the claims match the evidence.

## Score and Decision

**Calibration Procedure:**

*Round 1 (Bracketing):* Retrieved anchors across score bands. The closest topically relevant anchors were:
- "Solving Urban Network Security Games" (4.75, Reject) — benchmark/platform paper in a related domain; our paper has stronger theoretical and algorithmic contributions → our paper clearly above this.
- "Learning Mean Field Games on Sparse Graphs" (6.67, Accept) — theory + algorithm + experiments on real-world graphs; similar structure and similar type of weakness (missing baseline comparison noted by reviewer). Our paper is comparable or slightly below.
- "Can RL Solve Asymmetric Combinatorial-Continuous Zero-Sum Games?" (6.50, Accept) — theory + algorithm + experiments; similar structure. Our paper has broader experiments but similar evaluation gaps. Comparable.
- "NfgTransformer" (6.00, Accept) — mixed reviews (3,8,5,8); game representation learning. Our paper has cleaner contributions but some evaluation gaps. Comparable or slightly above.
- "Regularization is Enough for Last-Iterate Convergence" (5.60, Reject) — despite mixed reviews; theoretical paper. Our paper has more applied contributions.

*Initial bracket:* The paper sits between 5.5 and 6.5. It is clearly stronger than the 4.75 anchor and comparable to the 6.0–6.67 anchors.

*Narrowing:* Within the 5.5–6.5 bracket, the paper's genuine theoretical contribution (async-move optimality proof) and practical inference-time advantage are offset by the incomplete evaluation (missing ablation, overclaimed title, no variance). This places it at 6.0.

**Final Score and Decision:**

**MY FINAL SCORE: <score>6.0</score>**
**MY FINAL DECISION: <decision>Accept</decision>**