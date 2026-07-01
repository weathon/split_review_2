## Summary

This paper presents a graphical characterization of distributional equivalence for linear non-Gaussian causal models that simultaneously contain both latent variables and cycles — a setting where no such characterization previously existed. The authors introduce *edge ranks* as a local, edge-level constraint tool (dual to the well-known path ranks), and show that equivalence reduces to checking two simple conditions involving "children bases" of the latent set and each observed singleton (Theorem 2). They further provide a transformational characterization of the equivalence class via admissible cycle reversals and edge additions/deletions (Theorem 3), analogous to covered edge reversals in Markov equivalence. An algorithm (glvLiNG) is given as a proof of concept that this equivalence class can be recovered from data.

## Strengths

- **A genuinely open gap, clearly identified and filled.** The paper correctly argues that distributional equivalence has been characterized for causally sufficient cyclic models and for acyclic latent-variable models separately, but the intersection of *both* cycles *and* latent variables has remained uncharacterized even in parametric settings. The paper's framing of this gap as the missing prerequisite for general discovery (lines 27–31) is compelling and well-motivated.

- **Edge ranks are a genuinely new tool with reach beyond this paper.** The duality between path ranks and edge ranks (Theorem 1, Equation 16) is elegant and principled. Edge ranks are local (operating on edges rather than paths) and admit a decomposition that path ranks do not (the "children bases" decomposition in Theorem 2). This is a genuine enrichment of the rank-based toolbox for causal discovery.

- **Clean, well-structured theoretical results.** Theorems 2 and 3 are stated with precision. Theorem 2's reduction — from checking exponentially many subset pairs to checking only the children bases of the latent set and each singleton observed variable — is a striking simplification. Theorem 3's transformational characterization (admissible cycle reversals + edge additions/deletions) provides a complete traversal mechanism for the equivalence class. The parallelism drawn to CPDAGs and Meek's conjecture (lines 260–302) helps orient readers.

- **The paper's honest cabining of its algorithm's role** (line 328: *"The glvLiNG algorithm serves more as a proof of concept"*) and its identification of OICA as a limitation (lines 328, 334) are commendable. However, as noted below, this honesty in one part of the paper is undercut by stronger claims in the abstract and introduction.

## Weaknesses

### Fatal

None.

### Major

- **The abstract's strong method claim is not supported by the evaluation presented in the main paper.** The abstract calls glvLiNG *"the first structural-assumption-free discovery method"* (line 9) and the introduction calls it *"an efficient algorithm to recover the equivalence class from data"* (line 40). Yet the main paper's evaluation section (lines 316–326) contains **zero numerical recovery metrics** — no precision, recall, SHD, F1, adjacency recovery rate, or orientation accuracy. The finite-sample evaluation (point 4, line 324) is described only qualitatively: *"glvLiNG performs particularly better than baselines on denser graphs… while baselines perform better on sparser graphs."* All numerical results (Tables 3–5) are deferred to the appendix, including the finite-sample comparisons to baselines. A single runtime number (n=10, under 5s) and one equivalence-class enumeration statistic (783 classes from 480,640 models) are insufficient to substantiate a claim of being *"the first structural-assumption-free discovery method"* when the actual recovery accuracy and comparison to existing methods are not reported in the main text. The paper partially acknowledges this gap at line 328 (*"proof of concept"*), but the mismatch between the abstract's strong claim and the evidence presented in the main body is significant. The authors should either present key numerical results (recovery rates under main simulation conditions) in the main paper, or substantially qualify the abstract's method claim to match what the evidence supports.

### Minor

- **OICA dependency undercuts the "method" claim.** The paper acknowledges OICA's limitations (lines 328, 334) and discusses future OICA-free directions (line 330). However, the abstract's *"first structural-assumption-free discovery method"* rests on a pipeline whose first step is OICA in the over-complete setting — a notoriously difficult estimation problem involving local minima, sensitivity to initialization, and hyperparameter tuning. The paper treats OICA essentially as a black box (line 308: *"access to an oracle OICA"*), meaning the practical "method" claim is contingent on a subproblem the paper does not address. This does not weaken the theoretical contribution, but it does mean the practical significance of the claimed "first method" is unclear until the OICA bottleneck is resolved.

- **Notation inconsistency in Definition 2.** The irreducibility definition (line 100) uses the notation $\mathcal{G} \stackrel{\mathcal{D}}{\sim} \mathcal{H}$ where $\stackrel{\mathcal{D}}{\sim}$ is not defined — Definition 1 (line 84) defines $\stackrel{X}{\sim}$. This appears to be a notational inconsistency; the symbol $\mathcal{D}$ may be a typographic variant of $X$ or a placeholder. It should be clarified.

- **Example 1's enumeration numbers lack methodological context.** The paper reports that for specific latent configurations there are "17 digraphs," "872," and "1,024" in equivalence classes (lines 186–187), but does not explain how these numbers were obtained (exhaustive enumeration? from the interactive demo?). A brief methodological note would help readers assess the claim.

### Trivial

- **"No structural assumptions" framing could be misread.** The paper carefully distinguishes parametric assumptions (linearity, non-Gaussianity) from structural/graph-pattern assumptions (lines 17, 23–24). However, the abstract's phrase *"structural-assumption-free"* (line 9) could be interpreted by a casual reader as "no assumptions at all." Adding a brief qualification in the abstract (e.g., "under linearity and non-Gaussianity") would prevent misreading.

## Nice-to-Haves

- A worked example showing how Equation (16) (the duality between path ranks and edge ranks) plays out for a concrete small graph would make Theorem 1 more accessible.
- The "maximal equivalent digraph" result (Theorem 4, Appendix C.3) — analogous to a CPDAG — sounds valuable and could be summarized in the main paper.
- A small-scale empirical validation that verifies Theorem 3's class traversal directly on random graphs (without OICA) would demonstrate that the theory works independently of OICA's practical difficulties.

## Removed Points

- **Claim that "the evaluation of glvLiNG is too thin for the strength of the claims made about it"** — This is kept as a **Major** weakness (see above), not removed. The reviewer's point about deferring all numbers to the appendix is valid and verifiable from the paper.
- **"The gap between theory and practice via OICA is understated"** — Kept as a **Minor** weakness (see above), weakened from the original framing because the paper does acknowledge this limitation.
- **Section-by-section notes about "Theorem 2's prose explanation is too brief"** — Removed. This is a subjective suggestion about exposition, not a weakness. The paper's explanation, while concise, is adequate for its purpose.

## Novel Insights

The harsh review insight that the paper would benefit most from **re-centering around its theoretical contribution** and treating the algorithm as a corollary rather than a co-equal contribution is the most useful framing observation. The paper's genuine and significant advance is the equivalence characterization; the algorithm is best understood as a proof of concept that the theory is actionable, not as a standalone SOTA method.

## Suggestions

1. **Reconcile the abstract with the evidence.** Either move key numerical recovery results (precision/recall/F1 for the main simulation settings) from the appendix into the main paper, or qualify the abstract's method claim (e.g., "first structural-assumption-free discovery procedure, demonstrated as a proof-of-concept") to match the evidence actually presented in the main body.
2. **Clarify the $\stackrel{\mathcal{D}}{\sim}$ notation** in Definition 2.
3. **Add a brief methodological note** in Example 1 explaining how the equivalence class sizes (17, 872, 1,024) were computed.
4. **Consider adding a small OICA-free validation** of Theorem 3's traversal procedure on randomly generated graphs, to demonstrate the theory in isolation from OICA's practical difficulties.

## Score and Decision

The theoretical contribution — the equivalence characterization, the edge rank tool, and the traversal procedure — is genuinely significant and well-supported. The paper fills a clear open gap, and the formal results (Theorems 1–3) are clean, principled, and accompanied by an interactive demo. The weakness is in the mismatch between the abstract's strong method claim and the thin evaluation of glvLiNG in the main paper. However, the paper itself honestly describes the algorithm as a proof of concept (line 328), and the theoretical contribution is substantial enough to warrant acceptance. The paper should either present key numerical results in the main text or calibrate its abstract claims accordingly.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>