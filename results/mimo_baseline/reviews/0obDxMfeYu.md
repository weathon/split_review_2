## Summary
The paper introduces Medix, a two-stage framework for out-of-distribution detection that first identifies candidate OOD samples from unlabeled wild data using an element-wise median (EWM) of gradients, then trains a binary OOD detector on these extracted outliers and labeled InD data. The core contribution is the filtering stage: a greedy leave-one-out procedure that iteratively removes samples whose gradient removal most reduces the L2 distance between the EWM of remaining wild gradients and the mean InD gradient. The paper provides theoretical misclassification bounds decomposed into contamination, concentration, and separation effects, and demonstrates strong empirical results across 11 InD-OOD pairs against 20 baselines.

## Strengths
- **Novel filtering mechanism with theoretical backing:** The use of element-wise median of gradients as a robust statistic for separating InD/OOD samples in unlabeled mixtures is well-motivated by median's 50% breakdown point. The theoretical analysis (Theorems 4.1 and 4.2) cleanly decomposes error bounds into contamination, concentration, and separation terms, providing interpretable guarantees. The contamination term π/[2(1−π)] explicitly shows robustness up to π < 0.5, which is a satisfying and intuitive result.

- **Consistent empirical improvements across diverse settings:** On CIFAR-10, Medix achieves 0.80% average FPR95 versus WOODS's 3.40% (a 76% relative reduction). On CIFAR-100, it achieves 5.42% versus 6.74%. The improvements are consistent across all five OOD test sets, not just cherry-picked pairs, and the method outperforms both InD-only methods and wild-data methods comprehensively.

- **Good experimental rigor:** The paper follows the established WOODS protocol for fair comparison, uses standard benchmarks (CIFAR-10/100 with PLACES365, SVHN, TEXTURES, LSUN), reports mean and standard deviation over 5 runs, and provides empirical validation of the sub-Gaussian assumption (histogram and Q-Q plots). The 2D synthetic visualization (Figure 2) effectively illustrates the filtering mechanism with a quantified 12.5% error rate.

## Weaknesses
### Fatal
None.

### Major
- **Scalability of the greedy algorithm:** Algorithm 1 requires computing EWM for the leave-one-out set $\mathcal{S} \setminus \{i\}$ for every remaining sample $i \in \mathcal{S}$ at each iteration, yielding O(|S| × T × d) complexity where d is the gradient dimensionality (often 512+ for penultimate layers of WRN-40-2). For large wild datasets, this could become prohibitive. The paper defers computation analysis to Appendix A.6, but given that this is the core algorithmic contribution, the main text should discuss complexity trade-offs more directly and whether approximations (e.g., mini-batch EWM, random subsampling of candidates) could be employed.

- **Hyperparameter selection lacks practical guidance:** The method introduces hyperparameters ε (convergence threshold), k (number of samples removed per iteration), and T (maximum iterations), selected from {5e-5, 5e-4, 5e-3, 5e-2} and {4k, 7k, 10k, 20k}. The paper claims robustness to hyperparameters (Appendix A.2), but in the main text, there is no practical guidance for practitioners on how to choose these in novel settings—particularly k, which implicitly determines how many OOD samples are extracted and directly affects the false positive rate of the filtering stage.

### Minor
- **The CIFAR-100 improvements over WOODS are modest:** While the CIFAR-10 results are dramatic (0.80% vs. 3.40%), the CIFAR-100 improvements over WOODS average only 1.32% FPR95, and on PLACES365 specifically, it's 15.99% vs. 21.87%—still good but with high variance (±0.66). The narrative of "outperforms all baselines across the board" is technically true but somewhat overstated for CIFAR-100.

- **Limited InD diversity:** Only CIFAR-10 and CIFAR-100 are used as InD datasets. These are relatively low-resolution (32×32) with 10/100 classes. Evaluating on higher-resolution or more diverse InD distributions (e.g., TinyImageNet, domain-specific datasets) would strengthen generalizability claims.

- **Pseudo-label dependence:** The algorithm uses predicted labels $\hat{y}$ from the InD model for gradient computation on wild data. While Appendix A.5 claims resilience to label noise, the main paper should explicitly discuss how pseudo-label quality affects the gradient-based filtering, since misclassified InD samples could have misleading gradients.

## Nice-to-Haves
- A comparison of computational cost (wall-clock time, memory) of Medix versus WOODS and other baselines in the main paper.
- Analysis of performance across varying contamination ratios π (not just π=0.5) to validate the theoretical bounds empirically.
- Discussion of whether the element-wise median could be replaced by a coordinate-wise trimmed mean or other robust estimators, and sensitivity to this choice.

## Novel Insights
The paper's genuinely novel insight is that element-wise median filtering on gradients provides a theoretically grounded mechanism for separating InD and OOD samples from unlabeled mixtures, with a clean decomposition of the error into contamination and concentration effects. The empirical observation that gradient deviations increase monotonically with OOD contamination (Figure 1) provides a simple but effective diagnostic. The sub-Gaussian empirical validation (histogram + Q-Q plot) is a useful contribution for the broader community, as it gives concrete evidence that gradient-space analysis benefits from concentration-of-measure arguments.

## Suggestions
- Provide a complexity analysis of Algorithm 1 in the main text with concrete wall-clock timing comparisons against WOODS and other methods.
- Include a sensitivity analysis across varying π values (e.g., π ∈ {0.1, 0.3, 0.5, 0.7}) to empirically validate the theoretical bounds, especially the 0.5 threshold.
- Consider discussing approximation strategies for the leave-one-out computation to make the method more practical for large-scale deployment.

## Score and Decision
The paper makes a genuine and well-executed contribution: a novel median-based filtering mechanism for OOD detection from unlabeled wild data, backed by clean theoretical analysis and strong empirical results. The theoretical framework is elegant and the results are convincing. The main concerns—scalability and modest CIFAR-100 improvements—do not invalidate the contribution but limit enthusiasm for a strong accept. This is a solid borderline-accept paper that would benefit the community.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: Accept