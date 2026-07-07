## Summary
DiskHIVF is a hybrid memory-disk approximate nearest neighbor search (ANNS) algorithm that achieves O(√N·d + N) memory complexity by combining a two-level k-means clustering scheme (storing only n+m ≈ 2√N centers in memory) with disk-resident inverted lists. The method adds a greedy centroid reordering algorithm to improve disk locality and a query-aware dynamic pruning strategy based on polynomial fitting. Experiments on four datasets (SIFT1M, GIST, BIGANN, DEEP) show 10–30× memory reduction over prior SOTA and 1.2–2.3× latency improvement at 90% recall@1.

---

## Strengths

- **Practically important memory reduction**: The O(√N·d + N) memory footprint is a genuine asymptotic improvement over DiskANN/Starling's O(Nd/k) and SPANN's O(0.16·N·d). The billion-scale results (1.2 GB memory for BIGANN/DEEP vs. ~32 GB for competitors) demonstrate this concretely and are relevant to real deployment constraints.

- **Comprehensive evaluation**: Four datasets spanning 1M to 1B vectors, different dimensionalities (96–960d), and different data types (float, uint8) are tested. The paper also includes full recall-latency Pareto curves (Figure 3) rather than just a single operating point, allowing fair comparison across methods.

- **Starling limitation exposed**: The paper identifies a concrete failure mode of Starling (4096-byte disk page limit) that prevents it from handling high-dimensional vectors (GIST at 960d), which is a genuine and insightful empirical contribution.

- **Ablation studies validate each component**: Table 3 and Figures 4–5 quantitatively demonstrate that both the merge-read optimization and query-aware dynamic pruning contribute meaningfully (2–4× disk access reduction from merge-read alone).

---

## Weaknesses

### Fatal
None.

### Major

- **Novelty is incremental relative to GNO-IMI**: The core hierarchical two-level k-means with shared second-level codebooks applied to billion-scale data is essentially the GNO-IMI structure (Babenko & Lempitsky, 2016), which the paper cites. The paper's contributions are the specific memory-disk adaptation, disk layout, and pruning strategy—all individually well-motivated but modest in novelty. The paper should more explicitly delineate what is new beyond applying GNO-IMI in a memory-disk context.

- **Index build time absent**: For billion-scale systems, index construction time and cost are critical practical concerns. Neither Table 2 nor any figure reports build time or disk space usage, making it impossible to assess total system cost. Disk replication (SPANN duplicates vectors 8×) is mentioned for competitors but DiskHIVF's disk footprint is never quantified.

- **Throughput (QPS) not reported**: Only average latency for single queries is measured. In production systems, batch/concurrent query throughput (queries per second) is the primary metric. It is unclear whether DiskHIVF's sequential disk access pattern scales well under multi-threaded load.

### Minor

- **Dynamic pruning transferability**: The polynomial coefficients (a, b, c in Eq. 5) are fitted per dataset on training query distributions. There is no analysis of how sensitive these coefficients are to query distribution shift, which matters for out-of-distribution queries in practice.

- **Comparison fairness under memory constraints**: Baselines (DiskANN, Starling, SPANN) are run with their recommended configurations which may use far more memory than necessary. A fairer comparison would tune competitors to operate with the same memory budget as DiskHIVF and report best achievable recall.

- **Algorithm 2 is O(n²)**: The centroid reordering is a greedy nearest-neighbor path traversal with O(n²) complexity. For large n (√N for billion-scale, ~31,623), this is ≈10⁹ operations. Scalability of this step is not discussed.

### Trivial

- The paper inconsistently uses "DiskHIVE" and "DiskHIVF" (e.g., Section 1 introduces "DiskHIVE" before switching to "DiskHIVF"). This appears to be a revision artifact.

---

## Nice-to-Haves

- Report index build time and disk storage footprint alongside memory.
- Multi-threaded QPS experiments.
- Analysis of recall degradation on out-of-distribution queries under dynamic pruning.
- Evaluation on cosine similarity / inner product datasets (e.g., text embeddings relevant to the RAG motivation).

---

## Novel Insights

The paper's core insight—that sharing second-level cluster centers across all first-level clusters reduces the in-memory centroid count from O(N) (as in SPANN) to O(√N), while retaining fine-grained spatial partitioning into O(N) cells on disk—is a clean and effective design principle for memory-constrained ANNS. The empirical confirmation that this sub-linear memory footprint does not substantially harm search quality (and can even improve speed due to better I/O patterns) is a practically valuable finding for billion-scale retrieval systems.

---

## Suggestions

- Add a table or section comparing index construction time and disk usage across methods.
- Provide multi-threaded throughput experiments to validate production readiness.
- More clearly delineate the contributions beyond GNO-IMI in the introduction.
- Discuss the scalability of Algorithm 2 (centroid reordering) for very large n.

---

## Score and Decision

The paper addresses an important practical problem with solid empirical results on billion-scale datasets. The memory savings are concrete, substantial, and practically relevant. The main limitation is that the core algorithmic idea builds on GNO-IMI and the novelty, while real, is evolutionary. The missing index build time and throughput data are notable gaps. On balance, the practical significance and clean experimental validation outweigh the incremental nature of individual components.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>