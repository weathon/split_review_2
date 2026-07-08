Here is the final consolidated review.

---

## Summary

VISTA is a model-agnostic framework for causal structure learning that decomposes the global graph into Markov Blanket subgraphs, applies any off-the-shelf base learner to each subgraph independently, then aggregates via an exponential-decay weighted voting scheme and enforces acyclicity with a Feedback Arc Set heuristic. The design is clean, modular, and parallelizable. Experiments across 6 base learners (NOTEARS, GOLEM, DAG-GNN, GraN-DAG, SCORE, CAM), two graph families, multiple sizes (n=30–300), and the Sachs real benchmark show consistent accuracy improvements and 2–10× runtime speedups.

## Strengths

- **Clean model-agnostic design.** VISTA's decomposition into MB identification, local learning, weighted voting, and FAS-based cycle breaking is genuinely modular. Any base learner that outputs directed edges can be plugged in without modifying the aggregation logic, distinguishing it from earlier fusion approaches like SADA (restricted to LiNGAM) or DCILP (NP-hard ILP formulation).

- **Extensive empirical scope.** The evaluation covers 6 base learners, 2 graph families (ER, SF), multiple sizes (n=30–300), and a real benchmark (Sachs). This breadth makes the robustness claims more credible than if only 1–2 methods were tested.

- **Coverage guarantee (Proposition 3.1).** The proof that every true edge appears in at least one MB subgraph is elementary but important — it cleanly justifies why the decomposition does not lose edges *in principle*, which is the foundation for the entire pipeline.

- **Substantive runtime improvements.** Table 3 shows 2–10× speedups across all methods, stemming from the divide-and-conquer strategy (smaller subproblems, parallelism). These gains are genuine and practically useful.

## Weaknesses

### Major

- **The MB solver used in all main experiments is never named.** The paper writes `MB_solver(v)` as a generic call and mentions implementing the DCILP solver only in the context of Appendix F.2, but the specific algorithm used for the reported MB accuracy (Figure 1) and as input to all base-learner experiments is not stated. Since the entire pipeline depends on MB quality, this significantly impedes reproducibility and prevents readers from assessing how MB errors propagate.

- **Internal inconsistency about the FAS vs. thresholding ordering.** Section 3.1 (line 114) states: *"In VISTA, cycles are first removed using GreedyFAS, after which edges with weights below a global threshold t are filtered out."* However, Figure 3's caption (line 118) states the opposite: *"The merged graph is filtered (if s < t, remove X → Y) and then GreedyFAS is applied to remove cycles."* The pseudocode's `post_prune()` call hides which ordering is actually implemented. This must be resolved as the ordering materially affects which edges are retained.

- **The theoretical guarantees (Theorems 3.2–3.5) assume independent vote trials across subgraphs, but this assumption is violated in the intended use case.** The paper acknowledges this at line 138: *"subgraphs learned from the same dataset can induce correlations among votes"* and downgrades the bounds to *"a qualitative guide."* However, the abstract and contributions section present *"finite-sample error bounds"* and *"asymptotic consistency"* as established guarantees without communicating that the formal proofs rely on an assumption the deployed method violates. The asymptotic consistency result (Theorem 3.5, with m = C log n) inherits this issue — the logarithmic dependence is derived under independence and has no proven analogue when votes are dependent.

- **The Naive Voting (NV) results reveal a structural signal-to-noise problem that is under-analyzed.** In Table 1, NV drives FDR above 0.84 and F1 below 0.28 for every base learner — far worse than the base learner alone. This tells us that the MB decomposition introduces a massive number of spurious edges into the candidate pool. The paper frames NV as validating that *"all true edges are included"* but does not quantify how many false edges are also included, or analyze how heavily the weighted voting + FAS pipeline must rely on filtering to recover. This gap makes it unclear whether VISTA's gains come from the divide step making the subproblems easier, or from the filtering heuristics overcoming noise introduced by the decomposition itself.

### Minor

- **The claim *"typically increasing precision without sacrificing recall"* (Conclusion, line 287) is slightly overstated.** For NOTEARS on ER5 (Table 1), TPR drops from 0.74 to 0.68 under WV — a non-trivial recall loss. The claim holds for most of the 5 methods, but NOTEARS is arguably the strongest baseline, and the drop is notable.

- **The SCORE runtime entry at n=300 (Table 3) is marked "—" for the standalone baseline while VISTA+SCORE reports 225s.** It is unclear whether SCORE failed to complete (memory error, timeout) or ran but took too long. If SCORE failed, the comparison is unfair to the baseline.

### Trivial

- **Theorem 3.4 uses a strict lower bound (-1/m ln(1-t) < λ) and a non-strict upper bound (λ ≤ -1/m ln ε) without explaining why the lower bound must be strict.** Also, ε appears in the theorem statement before it is defined in the surrounding text.

## Nice-to-Haves

- Add an ablation replacing estimated MBs with ground-truth MBs to bound how much room for improvement exists in the MB step vs. the aggregation step.
- Directly measure the signal-to-noise gap: what fraction of edges in the aggregated subgraph union are true vs. spurious, and how does weighted voting change that ratio?
- Include a statistical significance analysis for key results where error bars overlap substantially.
- Report what "—" means for SCORE at n=300 in Table 3.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **DCILP comparison relegated to appendix:** The critic notes DCILP is discussed as a key baseline but compared only in Appendix F.2. This is a scope choice about placement rather than a substantive flaw; the comparison exists in the supplementary material. *Removed: scope creep — the paper cannot include every comparison in the main text.*
- **Missing statistical significance tests:** Not standard practice in this subfield for large-scale benchmarks with multiple base learners. *Removed: not a required methodological standard.*
- **Strengths removed from input:** Generic/superficial praise (e.g., "important problem," "interesting question") was removed per filtering rules. Only concrete, evidence-grounded strengths were retained.
- **The question about SCORE possibly failing:** This was kept as a Minor weakness, not removed.

## Novel Insights

The input reviews surface two observations not made in the paper: (1) that the NV results effectively quantify the signal-to-noise ratio introduced by the MB decomposition (a property the paper treats primarily as a validation of coverage rather than as a diagnostic for how much filtering the pipeline must do); and (2) that the theoretical framework's independence assumption is not merely a simplifying convenience but creates a gap between what the abstract claims ("finite-sample error bounds," "asymptotic consistency") and what the theorems actually guarantee for the deployed method. These observations sharpen the distinction between what VISTA demonstrates empirically and what it proves theoretically.

## Suggestions

1. **Name the MB solver** used in all experiments and report its F1 or SHD per graph size/setting as a sensitivity analysis. This is the single most impactful fix for reproducibility.
2. **Resolve the FAS/threshold ordering inconsistency** between the text (FAS first, then filtering) and Figure 3 (filtering first, then FAS), and expose the ordering explicitly in the pseudocode.
3. **Tone down the high-level theoretical claims** in the abstract and contributions: describe the error bounds as derived under an idealized independence assumption, with the understanding that correlation may alter the required sample size.
4. **Add a ground-truth MB ablation** to bound the improvement potential of the MB step vs. the aggregation step.
5. **Clarify the "—" for SCORE at n=300** and, if SCORE failed, note this explicitly and discuss the fairness of the comparison.

## Score and Decision

### Calibration Anchors

**Round 1 — Bracket identification:**
| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|---|---|---|---|---|---|
| Exact Distributed Structure-Learning for BNs | DUfwD5yiN4 | 5.25 | R1 | Yes | Most similar topic (distributed/divide-conquer structure learning). VISTA has stronger experiments (6 base learners vs just PC) but similar theoretical gaps. VISTA is slightly stronger overall. |
| Two Time-Slices Help Topological Ordering | mGmx41FTTy | 6.33 | R1 | Yes | Causal structure learning. More focused contribution but mixed reviews. VISTA has less novelty but cleaner evaluation. |
| Extendable/Iterative Structure Learning for BNs | 3n6DYH3cIP | 5.60 | R1 | Yes | Similar-level paper. VISTA is comparable in quality with better experiments but weaker theory. |
| Causal Graph Learning via Distributional Invariance | Lxst78Rrwj | 5.00 | R1/R2 | No | Causal graph learning. Similar score band, slightly below VISTA in experimental breadth. |
| Recovery of Causal Graph via Homologous Surrogates | fGhr39bqZa | 6.00 | R2 | Yes | Solid causal discovery paper with strong theory but smaller experiments. VISTA has better empirical breadth but weaker theoretical guarantees. |
| Causal Structure Learning Supervised by LLM | JzFLBOFMZ2 | 3.20 | R1/R2 | No | Lower-scored causal discovery paper. Significantly weaker evaluation. |

**Round 1 bracket:** 4.5–6.5. The paper shares heavy-weight strengths (extensive experiments, clean design) and damaging low-weight weaknesses (theoretical overclaiming, missing specification) with the ~5.5 anchor papers. It is stronger than the 3–4 papers but not as focused as the 6+ papers.

**Final calibration:** The closest anchor is DUfwD5yiN4 (avg 5.25, distributed structure learning). VISTA has:
- Shared heavy-weight strengths: clean modular design, theoretical foundation for decomposition
- Stronger heavy-weight strengths: more extensive empirical evaluation, measurable runtime gains
- Shared damaging weaknesses: theory-practice gap, limited analysis of decomposition's noise
- VISTA-specific damaging weaknesses: MB solver not specified (missing from DUfwD5yiN4), internal inconsistency

VISTA is slightly above DUfwD5yiN4 due to superior experiments and runtime evidence, but below fGhr39bqZa (6.00) due to the theoretical independence gap not being fully resolved. The weighted-item comparison places VISTA firmly in the 5–6 range.

### Final Score and Decision

The paper makes a genuine contribution — a clean, well-engineered modular framework with extensive empirical validation and practically useful speedups. The weaknesses (unnamed MB solver, FAS/threshold inconsistency, theoretical overclaiming, under-analyzed signal-to-noise) are real but addressable. The paper does not achieve the theoretical rigor it claims, but the empirical contribution stands on its own.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>