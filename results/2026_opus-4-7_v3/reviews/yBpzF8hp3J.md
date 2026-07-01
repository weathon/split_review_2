Now let me read the remaining sections to complete my verification.Now I have thoroughly read the paper. Let me draft the review before calibration.Now let me proceed with calibration. Round 1 — Bracketing:Let me read a few of the most relevant anchor papers for calibration.Now I have enough calibration data. Let me form my bracket and write the final review.

**Round 1 Bracket:**
- Score 1.0 papers: Clearly not comparable — those are fundamentally flawed.
- Score 2.5-3.0 DP papers: Limited novelty, weak utility analysis. Paper is clearly above.
- Score 4.6 (DP-OPH): Straightforward technique, missing utility bounds. Paper under review is significantly stronger.
- Score 5.0-5.25: Borderline reject DP papers with notable gaps. Paper is clearly above.
- Score 6.67-6.75 (DP hierarchical clustering, DP partially ordered counting): Focused DP theory papers with good algorithmic contributions but limited scope or some bound gaps. Similar tier, but paper under review has broader scope (three problems, conceptual reframing, experiments).
- Score 7.0 (Matrix Mechanism ℓ_p^p): Tight characterization of fundamental DP problem, heavily builds on prior work. Similar quality.
- Score 8.0 (DP ICL): Clean practical contribution with strong experiments. Different profile, somewhat higher bar.

**Initial bracket: 6.5–7.5**

The paper's conceptual reframing (missing mass), near-tight core bounds, elegant meta-algorithm, and honest/informative experiments place it solidly in this range. The downstream bound gaps and Zipfian assumption scope are real but bounded limitations. It compares favorably to the 6.67–7.0 accepted DP theory papers, with arguably broader impact from the metric reframing.

Now let me write the final review.

---

## Summary
This paper reframes differentially private (DP) domain discovery from cardinality-based evaluation to *missing mass* — the fraction of total item occurrences not recovered. It proves the first absolute utility guarantees for DP set union via the Weighted Gaussian Mechanism (WGM), showing near-optimal ℓ₁ missing mass on Zipfian data (Theorem 3.3) with a matching lower bound (Theorem 3.5), and a distribution-free ℓ∞ missing mass bound (Theorem 3.6). Using WGM as a domain-discovery precursor (Algorithm 2), it obtains new utility guarantees for unknown-domain top-k selection and k-hitting set, validated on six real-world datasets.

## Strengths

- **Conceptual reframing from cardinality to missing mass is the central contribution and is well-motivated.** Definition 2.2 introduces a natural metric; the singleton hardness example (Section 3, line 77) crisply demonstrates that no DP algorithm can achieve low missing mass without structural assumptions, motivating the Zipfian restriction. The ℓp generalization (Equation 1) cleanly unifies the new metric with prior cardinality-based work (p=0) and enables the ℓ∞ bridge to downstream applications.

- **First absolute utility guarantees for DP set union.** As verified against the literature survey (Section 1.1), prior work by Desfontaines et al. (2022) and Chen et al. (2025) proved only relative guarantees. Theorems 3.3 and 3.5 provide near-matching upper and lower bounds with tight dependence on ε and N, closing a real gap.

- **The meta-algorithm (Algorithm 2) is elegant and the distribution-free ℓ∞ bound (Theorem 3.6) enables downstream guarantees without Zipfian assumptions.** This is a clean design: half the privacy budget on domain discovery, half on a known-domain algorithm, with simple composition. The ℓ∞ bound removes the distributional assumption for top-k and k-hitting set results.

- **Experiments reveal a practically important insight: the conventional ranking of DP set union algorithms reverses under missing mass.** Figure 1 shows WGM achieves missing mass within 5% of sequential methods (Policy Gaussian, Policy Greedy), despite those methods recovering ~2× more unique items under cardinality (cf. Table 2 of Swanberg et al. 2023). This demonstrates that sequential methods spend budget on low-frequency items contributing little mass — a concrete, actionable finding for practitioners.

- **The k-hitting set result (Figure 3, Section 5.3) reveals that WGM-based domain discovery can outperform baselines with public domain knowledge**, because the WGM-discovered domain is smaller while retaining high-quality items, making the downstream peeling mechanism more effective. This non-obvious finding demonstrates domain discovery as beneficial dimensionality reduction.

## Weaknesses

### Fatal
None

### Major
- **Upper-lower bound gaps for top-k and k-hitting set are substantial and their tightness is undiscussed.** For top-k: the upper bound (Theorem 4.3) includes terms max_i|W_i|/(ε√q*) and √k·log(M)/ε that are absent from the lower bound Ω̃(k/(εN)) in Corollary 4.4. For k-hitting set: Theorem 4.5's additive error has a gap of at least √k in the k-dependence versus the lower bound Ω̃(k/ε) in Corollary 4.6. While the paper acknowledges these gaps in Section 6, it provides no discussion of whether the upper or lower bound is likely to be loose. This matters for assessing whether the WGM-based approach is near-optimal for these downstream problems or whether substantially better algorithms exist. The equal 50/50 privacy budget split in Algorithm 2 is one plausible source of looseness in the upper bounds that could be explored.

### Minor
- **The 1/(s−1) factor in the ℓ₁ bound (Theorem 3.3, Corollary 3.4) makes the bound vacuously large for practically important Zipfian exponents near 1.** Many real-world frequency distributions have s ∈ [1.0, 1.2]. The lower bound (Theorem 3.5) also contains 1/(s−1), confirming this dependence is inherent rather than an artifact of loose analysis. However, the paper does not discuss what the bound concretely implies in the regime s ∈ (1, 1.2] — even a brief numerical example would help practitioners assess the theory's relevance to their datasets.

### Trivial
None

## Nice-to-Haves
- An explicit table of the hidden logarithmic factors in the main theorems (Theorems 3.3, 3.6, 4.3, 4.5) would ease cross-theorem comparison and practical parameter selection. Currently, different subscripts are suppressed in different theorems, making it hard to compare bounds without chasing through appendix lemmas.
- Instance-dependent bounds that leverage the actual frequency distribution beyond the Zipfian envelope could show that WGM performs better than the worst-case bound suggests in the s ∈ (1, 1.5] regime, aligning theory with the experimental evidence.
- Reporting variance or confidence intervals for the set union experiments (Section 5.1) would match the standard set by the top-k and k-hitting set experiments, which report standard errors.
- A brief empirical investigation of how well real datasets conform to the Zipfian assumption (e.g., fitting s and C) would connect the theory to practice.
- A joint analysis for the meta-algorithm (Algorithm 2) that accounts for correlation between the discovered domain and the downstream mechanism's performance, rather than taking a worst-case union bound, could tighten the downstream guarantees.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **"The (1−1/ε) approximation factor in Theorem 4.5 appears incorrect"**: This is a parser artifact. The standard greedy approximation for submodular maximization yields (1−1/e) where e is Euler's number, and the paper references Mitrovic et al. (2017). Per rules, parser/formatting artifacts are not author errors.
- **"Main-text experiments only use (1, 10⁻⁵)-DP"**: The paper explicitly states (Section 5, line 273) that (0.1, 10⁻⁵)-DP results appear in the appendix and are "not significantly qualitatively different." The appendix was stripped by the parser. Cannot criticize its absence.
- **"The ℓ₀ missing mass connection (Section 2.3) could be stated more precisely"**: A minor precision nitpick about Definition 2.2 that doesn't affect any result. The paper correctly notes that minimizing missed unique items is equivalent to maximizing output cardinality under Assumption 1.
- **"The tilde-O notation suppresses different dependencies across theorems"**: While true, this is standard practice in theoretical CS. The actionable version has been moved to Nice-to-Haves.

## Novel Insights
The paper's key novel insight is that the conventional ranking of DP set union algorithms reverses when evaluated under missing mass rather than cardinality: the simple WGM, which recovers far fewer unique items than sequential methods, captures nearly the same total mass. This happens because sequential methods spend privacy budget discovering low-frequency items that contribute negligible mass. Combined with the formal near-optimality guarantee, this provides both theoretical and practical justification for using the simpler, more scalable WGM in production DP systems — a conclusion that prior cardinality-based evaluations would not have reached.

## Suggestions
- Discuss (even speculatively) whether the upper or lower bounds for top-k and k-hitting set are likely to be loose, to guide future work on closing the gaps.
- Add a brief numerical example showing what the ℓ₁ bound concretely implies for a dataset with s = 1.1 and realistic N, to help practitioners assess the theory's relevance.
- Consider whether optimizing the privacy budget split in Algorithm 2 (rather than fixed 50/50) could tighten downstream bounds, and if so, note this explicitly as a source of potential improvement.
- Fit the Zipfian parameters (C, s) on the experimental datasets and compare the theoretical bounds to actual performance, even if just qualitatively.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Cloth-Irrelevant Lifelong Person Re-ID | 5lUdTogEL3 | 1.0 | 1 | Fundamentally flawed; not comparable |
| Efficient All Pairs Minimax Path | bEgDEyy2Yk | 1.0 | 1 | Code implementation only; not comparable |
| KL Divergence for Stochastic GFlowNets | Uj0h13lVrR | 1.0 | 1 | Not a complete paper; not comparable |
| Time-dependent Development of Discourse | P49gSPmrvN | 1.0 | 1 | Visualization method; not comparable |
| Nonlinear Inference for DP Massive Data | uxFme785fq | 2.5 | 1 | DP paper with limited novelty; paper under review is significantly stronger in theory and experiments |
| MAAD Private | FNCFiXKYoq | 3.0 | 1 | DP fairness paper with limited technical depth; paper under review is stronger |
| DP Synthetic Dataset Alignment | TbOcySs6g8 | 2.5 | 1 | DP paper with weak utility analysis; clearly below |
| DP One Permutation Hashing | S6Dn3uyM2p | 4.6 | 1 | Straightforward DP technique with missing utility bounds; paper under review has much deeper theory |
| Maximum Coverage in Turnstile Streams | yfZJdCijo6 | 5.25 | 1 | Related coverage/selection problem but rejected for limited novelty; paper under review has stronger contributions |
| Avoiding Pitfalls for DP Accounting | fj5SqqXfn1 | 5.0 | 1 | Important but narrow DP accounting contribution; paper under review has broader scope and impact |
| Data Value Estimation on Private Gradients | mkXi7O0fun | 5.25 | 1 | DP utility analysis but rejected; paper under review is stronger |
| Privately Counting Partially Ordered Data | hVTaXJ0I5M | 6.75 | 1 | Focused DP theory with good algorithmic contribution; similar quality but paper under review has broader scope (three problems, conceptual reframing) |
| Optimality of Matrix Mechanism on ℓ_p^p | fbqOEOqurU | 7.0 | 1 | Tight DP theory characterization but heavily follows prior work; similar quality to paper under review |
| Guaranteed Error for Learned DB Operations | 6tqgL8VluV | 6.0 | 1 | Theory for learned methods with some gaps; paper under review is somewhat stronger |
| Price of DP for Hierarchical Clustering | yLhJYvkKA0 | 6.67 | 1 | DP theory with upper/lower bounds and bound gaps; very comparable, paper under review has slightly broader contributions |
| Hidden Cost of Waiting for Predictions | A3YUPeJTNR | 8.0 | 1 | Different domain; strong accept reflects completeness and novelty; paper under review doesn't quite reach this bar |
| DP Few-Shot Generation for ICL | oZtt0pRnOl | 8.0 | 1 | Clean DP practical contribution with thorough experiments; higher novelty/impact profile |
| Quantitative Data Usage Inference | EUSkm2sVJ6 | 7.6 | 1 | Strong contribution but different domain; paper under review is slightly below |
| Submodular File Selection for LLMs | f4gF6AIHRy | 8.0 | 1 | Different domain (LLM pretraining); not directly comparable |

**Round 1 bracket: 6.5–7.5**

The paper sits comfortably among accepted DP theory papers in the 6.67–7.0 range. It matches the "Privately Counting Partially Ordered Data" (6.75) in theoretical quality while offering broader scope, and compares favorably to "Optimality of Matrix Mechanism" (7.0) by adding a genuine conceptual reframing and experimental validation. The downstream bound gaps prevent it from reaching the 8.0 tier. The paper makes a clear positive contribution: the missing mass reframing is a genuine insight, the core bounds are near-tight, and the experiments are honest and informative.

**Final score: 7.0** — A solid accept. The paper introduces a well-motivated metric that changes the evaluation landscape for DP domain discovery, proves near-tight bounds for its core contribution, and provides informative experiments. The gaps in downstream bounds are real but explicitly acknowledged and do not undermine the central contribution.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>