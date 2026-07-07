## Summary

Fed-MADS is a federated active learning (FAL) framework designed for explainable federated learning (XFL). It uses the Information Bottleneck (IB) principle to derive a minimax data selection objective: unlabeled samples are scored by summing the KL-divergence between local and global encoder outputs and the cross-entropy between local and global decoder predictions. The variational distributions in the IB objective are implemented by the global model, giving the method a natural fit to the FL setting. Experiments on four benchmark datasets using LR-XFL as the base XFL framework consistently show improvements over prior FAL methods in model accuracy, rule accuracy, and rule fidelity.

## Strengths

- **Clean theoretical derivation.** The step from IB objective (Eq. 1) → variational surrogate (Eq. 9) → minimax query score (Eq. 13) is logically coherent, and using the global model as the variational approximation is a motivated and novel design choice. It connects established IB theory to the FL setting in a principled way.
- **Consistent empirical gains.** Fed-MADS outperforms all six baselines on all four datasets across three metrics (model accuracy, rule accuracy, rule fidelity), without cherry-picking. The gains are particularly large on harder datasets (MIMIC-II, Credit-Card), which strengthens the argument that incorporating local–global divergence matters most when data is complex or imbalanced.
- **Computational efficiency.** The query score computation is O(|U_i|) per client and adds no communication overhead, making the approach practically deployable.

## Weaknesses

### Fatal
None.

### Major

- **Novelty of the final algorithm is modest.** The IB derivation ultimately yields a query criterion that selects samples where local and global models disagree most — in latent representations and predictions. Disagreement-based query strategies are long-established in AL, and KSAS (a direct competitor) already uses KL divergence between local and global model class-weighted predictions. The contribution is primarily in the IB-theoretic justification and in applying both encoder and decoder divergences simultaneously; but the resulting algorithm would likely be intuited without the IB machinery. The paper should do more to demonstrate that the IB lens reveals something that pure intuition would have missed.

- **The i.i.d. assumption substantially limits scope.** The paper explicitly assumes i.i.d. data across clients, which is the benign federated scenario. Non-i.i.d. (heterogeneous) data is the dominant practical concern in FL. Without experiments or analysis under heterogeneous data, it is unclear whether the method's reliance on the global model as a "good" variational approximation holds when data distributions diverge across clients.

- **Tested only on a single XFL framework.** All experiments use LR-XFL as the base model. The paper does not demonstrate that Fed-MADS generalizes to other XFL architectures or to standard FL models with interpretability add-ons. This limits the scope of the empirical claim.

### Minor

- **β=0 remains competitive.** Figure 3 shows that setting β=0 (using only the KL between encoder outputs, dropping the cross-entropy term) still yields competitive results. This weakens the argument that the full two-term score — and by extension the complete IB derivation — is necessary; the simpler encoder-divergence heuristic might suffice.

- **The bound in Eq. (8) is an upper bound, not a tight one.** Dropping the negative KL and cross-entropy terms to form a tractable surrogate is a common but lossy step. The paper does not discuss how loose this bound is or whether it is tightest in the high-divergence regime that the query strategy targets.

### Trivial
None significant.

## Nice-to-Haves

- Experiments under non-i.i.d. data partitioning (e.g., Dirichlet allocation) would make the results far more convincing for real-world federated settings.
- An ablation comparing the IB-derived score to a naive "encoder KL + decoder KL" baseline (without the IB framing) would clarify what theoretical insight the IB derivation actually adds beyond intuition.
- A second XFL architecture would support generalization claims.

## Novel Insights

The key genuinely novel idea is implementing both variational distributions in the IB objective with the global federated model — rather than with a fixed prior — so that the global model's accumulated cross-client knowledge directly guides local data selection. This is a simple but principled connection that had not been made before in the FAL literature and gives an information-theoretic rationale for why local–global model disagreement is a sound query criterion in XFL, as opposed to a heuristic choice.

## Suggestions

- Report results under a non-i.i.d. data setting with at least one Dirichlet partition to assess robustness.
- Include a baseline that uses only encoder KL divergence (β=0) as a named method in the main comparison table, to clarify the incremental value of the full score.
- Discuss the tightness of the bound in Eq. (8) and whether data points with highest query scores correspond to the tightest or loosest portion of the bound.

## Score and Decision

Fed-MADS offers a clean IB-theoretic derivation for an FAL query strategy and delivers consistent empirical improvements across three explainability metrics on four datasets. The global-model-as-variational-distribution design is a genuinely elegant fit to the FL setting. However, the resulting algorithm is close to known disagreement-based heuristics, the experiments are restricted to i.i.d. data and a single XFL framework, and the β=0 ablation partially undermines the necessity of the full derivation. The contribution is solid but incremental for ICLR.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Accept</decision>