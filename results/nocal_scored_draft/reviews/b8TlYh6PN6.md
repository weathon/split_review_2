Now I have all the signals I need. Let me produce the final review.

## Summary

This paper provides the first characterization of distributional equivalence for linear non-Gaussian causal models with arbitrary latent structure and cycles. The core theoretical contributions are the introduction of *edge rank* constraints (a new graphical tool with a duality to path ranks, Theorem 1), a graphical criterion for equivalence (Theorem 2, reducing exponentially many rank checks to singleton checks), and a transformational characterization (Theorem 3, analogous to the Meek conjecture, enabling traversal of the equivalence class via cycle reversals and edge additions/deletions). The paper also presents glvLiNG, a proof-of-concept algorithm that uses these results for latent-variable causal discovery from data.

## Strengths

- **The paper addresses a genuine and well-motivated gap.** The introduction clearly traces the problem: FCI is maximally informative under CI constraints but uninformative about latent structure, existing latent-variable methods rely on restrictive structural assumptions (measurement models, acyclicity, triangle-freeness, etc.), and a core obstacle to a general method has been the lack of an equivalence characterization. The historical parallel to how CPDAGs enabled PC and MAGs enabled FCI is compelling.

- **The edge rank concept (Section 3.3) is a genuinely novel theoretical contribution.** Theorem 1 (duality between path ranks and edge ranks) is elegant and non-trivial, drawing on matroid-theoretic foundations (König, Perfect, Ingleton & Piff — acknowledged by the authors) but applying them to causal discovery for the first time. The paper demonstrates concretely why edge ranks are easier to manipulate than path ranks and lead to cleaner local conditions, which is the key enabler for the main results.

- **Theorem 2 (graphical criterion) and Theorem 3 (transformational characterization) are substantive results.** The reduction from checking all subsets x ⊆ X to checking each singleton X_i independently (plus the latent set) is a genuine theoretical advance over the path-rank formulation. The cycle-reversal + edge-addition/deletion operations provide a clean traversal mechanism, and the analogy with the Meek conjecture is apt and illuminating.

- **The framing is strong and historically informed.** The paper correctly identifies that the lack of an equivalence characterization has been a bottleneck (echoing how PC followed CPDAGs and FCI followed MAGs), and sets clear expectations about what the theory delivers and what it does not.

## Weaknesses

### Major

- **Mismatch between the strength of the algorithmic claims and the evidence provided.** The abstract and introduction claim "the first structural-assumption-free discovery method" (line 9) and "an efficient algorithm" (line 40), yet the paper later acknowledges that "the glvLiNG algorithm serves more as a proof of concept" (line 328) and that OICA has "known inefficiency in practice" (line 328). The empirical evaluation is too thin to support strong algorithmic claims: the runtime comparison (Table 4) is against a linear programming baseline for a specific subproblem rather than against alternative causal discovery methods; the real-data application is described in two sentences (lines 325-327) with no quantitative validation; finite-sample results are deferred to the appendix and the main text already signals mixed performance ("baselines perform better on sparser graphs," line 324); and while evaluating baselines under structural misspecification (Table 5) is informative, the paper does not also compare methods on models where baselines' own assumptions hold. This creates a clear tension between front-loaded confidence and back-loaded caveats that needs resolution — either the evaluation must be strengthened or the claims must be recalibrated.

### Minor

- **The irreducibility condition (Proposition 1, line 104) requires checking all non-empty subsets l ⊆ L**, which is exponential in the number of latent variables (2^|L| − 1 checks). The paper notes that in the acyclic case it suffices to check each single L_i, but in the general cyclic case no polynomial-time algorithm or complexity analysis is provided. This could be a practical bottleneck when the number of latent variables is not very small.

- **The practical significance of the equivalence characterization is not fully explored.** The paper enumerates equivalence class sizes for tiny graphs (up to 6 vertices) and mentions specific classes of size 17, 872, and 1,024 (Example 1, line 186), but does not analyze what determines class size, which edges are invariant across the class, or how to summarize the class informatively for practitioners. Theorem 4 (deferred to appendix) apparently addresses invariant edges; bringing it into the main text would substantially strengthen the paper.

- **The glvLiNG algorithm relies on an oracle assumption for OICA** to recover mixing matrix ranks, and OICA is known to be sensitive to initialization, local optima, and sample size. While this is acceptable for a theory paper (and the paper acknowledges the limitation and suggests alternatives in lines 329-330), it further widens the gap between the claimed practical contribution and what is actually delivered.

### Trivial

None.

## Nice-to-Haves

- A complexity analysis for the key operations (checking irreducibility, computing bases for Theorem 2, checking edge-addability in Lemma 7) would strengthen the theoretical framing.
- An analysis of what determines equivalence class size and which edge features are invariant across the class would increase practical relevance.
- An explicit discussion of when OICA can be replaced by alternative rank-estimation methods (briefly mentioned in line 329) would be helpful.

## Removed Points

These points from the harsh critic input are flagged to be removed; treat them with caution:

1. "Baseline comparison is staged to make glvLiNG look better" — REMOVED. The paper transparently frames this as evaluating methods "under structural misspecification" (line 322). Evaluating assumption-requiring methods on models that violate their assumptions is a legitimate experiment that supports the paper's claim about being assumption-free. The concern about missing comparisons on models where baselines' assumptions hold is retained within the Major weakness above.

2. "Runtime comparison against a linear programming baseline is a strawman" — REMOVED. The paper clearly states the baseline is a linear programming approach for the same subproblem (line 320). This is a legitimate efficiency benchmark for the algorithm's core step.

3. "Finite-sample results deferred to appendix" — REMOVED as a standalone point; the appendix is stripped by the parser but exists in the original submission. The concern is absorbed into the overall thinness-of-evaluation point.

## Novel Insights

None beyond the paper's own contributions. The harsh critic's analysis validates the paper's own framing rather than adding new insights.

## Suggestions

1. **Recalibrate the algorithmic claims to match the evidence.** The theory is strong enough to warrant acceptance on its own. Either substantially strengthen the evaluation (proper finite-sample comparisons in the main text, comparisons on models within baselines' own assumptions, multiple real-data examples with quantitative validation) or downgrade the language around contribution 4 from "the first structural-assumption-free discovery method" to "a proof-of-concept algorithm demonstrating that the equivalence characterization enables discovery in principle."

2. **Bring Theorem 4 (characterization of invariant edges, analogous to CPDAG arrows) into the main text.** This directly addresses the practical question of what can be learned from the equivalence class and would substantially strengthen the paper's practical relevance.

3. **Add a complexity note for the irreducibility check** and, if possible, discuss when the exponential check can be avoided or whether the number of latents is typically small enough in practice that this is not a bottleneck.

## Score and Decision

MY FINAL SCORE: <score>8</score>
MY FINAL DECISION: <decision>Accept</decision>