## Summary

This paper characterizes distributional equivalence for linear non-Gaussian causal models with both latent variables and cycles — a setting for which no equivalence characterization previously existed. The authors introduce *edge rank* constraints as a new graphical tool, prove a duality between edge ranks and path ranks (Theorem 1), derive a local graphical criterion for equivalence that reduces checking from all subsets to singletons (Theorem 2), and provide a transformational characterization for traversing equivalence classes (Theorem 3). They further present glvLiNG, a proof-of-concept algorithm that recovers models up to equivalence from data.

## Strengths

- **Edge ranks are a genuinely novel technical contribution to causal discovery.** The duality between path ranks and edge ranks (Theorem 1) is well explained, and the connection to König's theorem / bipartite matching provides a clean, local alternative to path-based reasoning. While the duality is known in matroid theory, its application to causal equivalence is new and Section 3.3 is the clearest part of the paper.

- **Theorem 2 (graphical criterion) is the paper's theoretical centerpiece and is striking.** Reducing equivalence checking from iterating over all subsets of observed variables to checking each singleton independently, via the "children bases" condition, is a nontrivial simplification. The analogy to moving from "all d-separations" to "adjacencies and v-structures" in the causally sufficient acyclic case is apt.

- **Theorem 3 (transformational characterization) rounds out the theory.** Providing both a static criterion (Theorem 2) and an operational traversal mechanism (admissible cycle reversals + edge additions/deletions) mirrors the classic Meek conjecture / covered edge reversals structure. The claim that at most one cycle reversal suffices is a strong result that, if correct, simplifies traversal considerably.

## Weaknesses

### Fatal

None.

### Major

- **The algorithmic contribution (glvLiNG) is claimed but unsupported by experimental evidence in the main text.** The paper lists "develop an algorithm to recover models from data up to such equivalence" as a key contribution (Point 4 in §1). Section 5 is labeled "Algorithm and Evaluation," yet the evaluation subsection contains no tables, figures, or concrete numerical results — only text assertions such as "[glvLiNG] solves cases with n=10 vertices in under 5s" and "Both methods tend to produce overly sparse graphs and misidentify over half of the edges." All results are deferred to the appendix (Tables 3–5, Appendix D). While page limits may necessitate some deferral, a reader evaluating the main paper cannot assess any of these empirical claims. The paper acknowledges that glvLiNG "serves more as a proof of concept" (§6), but then presents it as a first-class contribution in the abstract and introduction. This mismatch between claimed significance and provided evidence is a significant weakness. The paper would be stronger if it either (a) substantially reduced the prominence of the algorithm as a contribution or (b) brought representative experimental evidence into the main body.

### Minor

- **The evaluation of baseline methods (item 3 in §5) tests LaHiCaSi and PO-LiNGAM exclusively on models outside their assumptions and declares them inferior.** The paper states this is examining "structural misspecification," which is legitimate, but the framing would be more informative if accompanied by a scenario where these baselines' assumptions *are* satisfied, to calibrate what "good" performance looks like. The finite-sample comparison (item 4) partially addresses this, but the oracle comparison (item 3) lacks a within-domain reference point.

- **The term "structural-assumption-free" could mislead readers about the retained assumptions.** The paper correctly defines "structural assumptions" narrowly (measurement models, pure children requirements, triangle-freeness, etc.) and works within the LiNG setting (linearity, non-Gaussianity, faithfulness, I−B invertibility). However, a reader may infer from "without any structural assumptions" (abstract, line 9) that the method makes no assumptions at all. An explicit summary of retained assumptions (as in the Strengthening the Paper suggestions) would improve clarity without detracting from the genuine contribution of removing *graph-structural* assumptions.

- **The reliance on path rank constraints holding generically in cyclic digraphs (Lemma 2 → Lemma 3 chain) is referenced but not discussed in the main text.** The paper cites Talaska (2012) for the cyclic generalization, which is a published result and thus valid. However, the main text (lines 146–147) dismisses the denominator issue ("this does not affect our results") with a forward reference to the proof. Given that the entire equivalence characterization rests on this step, a brief intuitive explanation of why the cyclic path rank constraints remain generic would strengthen reader confidence without requiring full technical details in the main body.

- **The paper does not discuss the computational complexity of equivalence-class traversal.** Theorem 3 enables BFS/DFS traversal, but equivalence class size can be exponential in the number of vertices. The paper mentions a maximal-digraph representation (Theorem 4, deferred to appendix) as a compact alternative, but the main text gives no sense of whether the output is practically representable for graphs beyond small examples. A brief comment on this would help.

- **The practical estimation of the number of latent variables via OICA receives limited discussion.** The paper notes that OICA identifies the number of latents (lines 106, 132) but does not address the circularity concern that OICA itself typically requires knowing (or jointly estimating) the number of sources. Since the algorithm depends critically on an OICA oracle, more clarity on this point would benefit practitioners.

### Trivial

None.

## Nice-to-Haves

- A worked example of Theorem 2's bases conditions for a nontrivial case (not just the L=∅ causally sufficient case) would substantially improve accessibility.
- A brief summary table of retained assumptions (linearity, non-Gaussianity, faithfulness, I−B invertibility, OICA identifiability) would prevent overclaiming concerns.

## Removed Points

**(Critical Issue 4, original framing — "path rank constraints for cyclic graphs is a heavy lift")** — The reviewer characterized this as a potentially fatal weakness. In fact, the paper cites Talaska (2012), a published result that generalizes path rank constraints to cyclic digraphs. The denominator issue is addressed in the proof (appendix), and the claim that rank constraints suffice is established there. This is standard practice for theory papers: citing existing results and deferring technical details. The criticism as originally framed overstated the concern. Removed as not a genuine weakness; the softened version above (Minor item 4) captures the reasonable presentation-level suggestion.

**(Critical Issue 2, original framing — "misleading at worst")** — The reviewer's claim that the baseline comparison is "uninformative at best, and misleading at worst" is not supported by the paper. The paper explicitly states it is testing "under structural misspecification" (line 322), and the finite-sample comparison (item 4) does evaluate all methods on common ground. A method being tested where its assumptions are violated is a standard stress test, not a misleading comparison. Removed the "misleading" characterization; the softened Minor item 1 above retains the reasonable suggestion to add a within-domain reference point.

**(Original reviewer strength: "The problem is well-chosen and clearly motivated")** — This strength is partly about problem importance and is somewhat generic. Retained in the summary's implicit motivation but not listed as a standalone strength since the paper's substantive technical strengths are more informative.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Either reduce the prominence of glvLiNG as a claimed contribution (e.g., relegate it to a proof-of-concept in the main text) or bring at least one representative experimental figure/table into the main paper so readers can assess the empirical claims.
2. Add a short paragraph or table explicitly listing the assumptions the method retains (linearity, non-Gaussianity, faithfulness, I−B invertibility, OICA identifiability).
3. Add a computational complexity note about the worst-case size of the equivalence class and whether the maximal-digraph representation (Theorem 4) always compresses it compactly.

## Score and Decision

**Score:** The theoretical contribution — edge ranks, the equivalence criterion (Theorem 2), and the transformational characterization (Theorem 3) — is novel, technically sound, and addresses an important open gap. These results alone constitute a meaningful publication. However, the paper's decision to present glvLiNG as a first-class contribution (§1, Point 4; §5) without supporting experimental evidence in the main text creates a significant mismatch between claimed contribution and provided evidence. The paper would be stronger by either reducing the prominence of the algorithm or substantiating it with data.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>