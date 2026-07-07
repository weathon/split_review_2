## Summary

This paper presents LSH-DBSCAN and LSH-HDBSCAN: locality-sensitive hashing-based algorithms that achieve the first provably subquadratic runtime for approximate DBSCAN and HDBSCAN on arbitrary high-dimensional datasets, with no assumptions on data distribution. The key improvement over the prior work of Okkels et al. (2025) is that the cluster formation step no longer requires the number of points within distance $c\varepsilon$ to be $O(\text{MinPts})$. The authors complement these upper bounds with SETH-based lower bounds showing that near-exact DBSCAN requires near-quadratic time.

## Strengths

- **First unconditional subquadratic approximation for high-dimensional DBSCAN.** The runtime $\tilde{O}(dn^{1+1/(2c^2-1)+o(1)})$ holds for all datasets, removing the critical density assumption of Okkels et al. (2025) that breaks in dense-cluster regimes. This is a clean and meaningful advance.
- **Tight algorithmic-complexity picture.** The SETH lower bound (Theorem 3.3) shows any algorithm achieving a $(1+\gamma)$-approximation for small $\gamma$ requires $\Omega(n^{2-\alpha})$ time, establishing near-quadratic lower bounds that match the behavior of the upper bound as $c\to 1$. Together these results give a nearly complete picture.
- **Clean reduction to HDBSCAN.** The extension via $O(\log \Delta)$ calls to LSH-DBSCAN with geometric scaling of $\varepsilon$ and intersection of clusterings is elegant and essentially "free" in terms of asymptotic runtime.
- **Empirical results demonstrate practical utility.** On most benchmarks, moderate values of $c$ (3–9) yield $10\times$–$120\times$ computation speedup with misalignment below 0.13, validating the theory.

## Weaknesses

### Fatal
None.

### Major
- **Sub-1x speedup for small $c$ on ALOI.** At $c=2$, LSH-DBSCAN is *slower* than exact DBSCAN on ALOI (0.78x speedup). This directly undermines the practical narrative for the smallest approximation factors, and is not adequately explained beyond a passing comment about ALOI's smaller $n$. It suggests the constant factors in the LSH approach can dominate for moderate dataset sizes.
- **Computation speedup metric obscures hash cost heterogeneity.** The paper counts distance and hash computations with equal weight, but hash computation cost for E2LSH (which involves random projections of high-dimensional vectors) is $O(d)$ per hash—comparable to a distance computation. The paper doesn't clearly quantify how this affects practical speedup relative to a baseline that also uses $O(d)$ operations. The wall-clock times are deferred to the appendix, leaving the main body with a potentially optimistic picture.

### Minor
- **Novel contribution is confined to the cluster formation phase.** The core point identification (Algorithm 2) is explicitly taken from Okkels et al. The main novelty is Algorithm 3's LSH-assisted BFS. The paper could more sharply highlight this distinction and justify why the prior cluster formation step was insufficient.
- **Small dataset scale for empirical validation.** With $n \leq 60{,}000$, the subquadratic advantage is modest. The theoretical speedup scales polynomially in $n$, so showing results at $n \sim 10^6$ would make a stronger empirical case.
- **Setting $\delta = 0.5$ in experiments.** Using a failure probability of 50% is non-standard and may give misleading impressions of robustness; the paper notes that scaling $K$ below theoretical values improved speedups but this deviates from the theoretical prescription without full justification.

### Trivial
None significant.

## Nice-to-Haves
- Experiments at larger scales ($n > 10^6$) would strengthen the empirical case considerably and better demonstrate the polynomial scaling advantage.
- A head-to-head comparison with the approach of Okkels et al. (2025) on dense datasets (where their assumption fails) would directly illustrate the improvement.
- A discussion of the practical range of $c$ that balances approximation quality and speedup, possibly as a practical guideline for users.

## Novel Insights
The key insight enabling the theoretical advance is in the cluster formation phase: rather than requiring explicit edges in the $\varepsilon$-neighborhood graph between all core point pairs, the LSH-assisted BFS guarantees connectivity within distance $\varepsilon/c$ while staying subquadratic even when clusters are dense. This decouples cluster correctness from the density of the point cloud, which is exactly what breaks the Okkels et al. assumption. The SETH lower bound argument, reducing from bichromatic closest pair, elegantly shows the approximation is not merely an algorithmic convenience but a computational necessity—this tight characterization of the hardness landscape is the paper's most insightful theoretical contribution.

## Suggestions
- Include a figure or table directly comparing against Okkels et al. (2025) on a synthetic dense-cluster dataset to empirically demonstrate when the assumption fails and your method succeeds.
- Provide a clear runtime analysis distinguishing hash computation cost from distance computation cost for the specific E2LSH family used in experiments.
- Discuss the empirical implications of using $\delta = 0.5$—e.g., how many independent trials were run, or why this is reasonable in practice despite the high theoretical failure probability.

## Score and Decision

The paper makes a genuine theoretical advance: the first assumption-free subquadratic algorithm for approximate DBSCAN/HDBSCAN in high dimensions, with matching lower bounds. The algorithmic idea is clean, the proofs appear sound, and the empirical evaluation is reasonable. The major weaknesses (sub-unity speedup at small $c$ and the limited scale of experiments) are real but do not invalidate the theoretical contribution. This is a solid algorithms/theory paper of clear value to the ICLR community.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>