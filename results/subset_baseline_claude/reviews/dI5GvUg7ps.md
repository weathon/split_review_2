## Summary

RewardRank is a two-stage learning-to-rank framework for counterfactual utility maximization. It (1) trains a permutation-aware transformer reward model on logged user interactions to predict list-level utility, and (2) optimizes a ranker end-to-end by differentiating through a SoftSort operator. Alongside the method, the paper proposes two automated evaluation protocols—PO-Eval (parametric click model oracle on Baidu-ULTR) and LAU-Eval (LLM-simulated users on Amazon-KDD-Cup)—and demonstrates that optimizing NDCG is sub-optimal for maximizing true user utility.

---

## Strengths

- **Well-motivated problem.** The paper clearly identifies a gap: classical LTR losses optimize proxy metrics (NDCG) that assume position-independent relevance, whereas real user utility is list-level and influenced by cognitive biases. The empirical results in Table 1 confirm this gap—high offline NDCG does not correlate with high counterfactual utility.
- **Novel, reproducible evaluation protocols.** PO-Eval and LAU-Eval fill a real void in counterfactual LTR research, where standard offline evaluation is impossible without access to the true utility function. Both protocols are automated and applicable to public datasets, which is a concrete service to the community.
- **Strong empirical results across three testbeds.** RewardRank outperforms all baselines on PO-Eval, LAU-Eval, and—notably—also achieves the highest DCG_rel on Baidu-ULTR with real click data (Table 2), providing consistent evidence across settings rather than cherry-picking one favorable benchmark.
- **Reward misspecification correction.** The sample reweighting scheme (Eq. 13) is a practically motivated addition that acknowledges the inherent unreliability of learned rewards on out-of-distribution permutations, and ablations confirm it improves counterfactual performance.

---

## Weaknesses

### Fatal
None.

### Major

1. **Distribution shift in counterfactual space is not adequately addressed.** The reward model is trained only on the small set of permutations actually observed in the logged data (the factual space). During ranker training, the reward model is queried on permutations it was never trained on. The misspecification correction (Eq. 13) reweights training *samples* based on how well the reward model fit those observed permutations, but it does not address extrapolation quality on *unseen* permutations—which is precisely where the ranker operates during optimization. There is no analysis of reward model accuracy on held-out permutations or evidence that the soft reward (Eq. 11) generalizes beyond the factual space.

2. **Potential circularity in PO-Eval.** The oracle used in PO-Eval is itself a parametric IPS model trained on the same Baidu-ULTR dataset. RewardRank's reward model (a transformer encoder with positional embeddings, Eq. 4) has a similar architecture and training signal. There is a risk that RewardRank succeeds on PO-Eval primarily because it approximates the oracle's functional form rather than because it learns genuinely better user preferences. An ablation showing performance when the oracle is replaced with a structurally different model (e.g., a simple cascade click model) would help rule this out.

3. **LAU-Eval's validity as a proxy for real user behavior is unverified.** The paper claims LLM simulation captures "realistic user behavior," but there is no validation against real user data. The biases injected into the LLM prompt (position bias, brand bias, etc.) are manually specified rather than inferred from data, making LAU-Eval's fidelity as a counterfactual proxy uncertain.

### Minor

1. **Contradiction between Tables 1 and 2 is unexplained.** In Table 1 (PO-Eval), RewardRank achieves the lowest offline NDCG_click (0.370) among competitive methods, yet in Table 2 (Baidu-ULTR with real clicks), it achieves the highest DCG_rel. If NDCG and true utility are misaligned, why does maximizing true utility also yield the best NDCG with real clicks? This apparent paradox warrants discussion.

2. **Amazon-KDD-Cup permutation sampling is synthetic.** The 400K training query groups are constructed by sampling permutations from annotation data rather than from real logged interactions. This means the factual space is artificially expanded, which may artificially simplify the counterfactual evaluation setting.

### Trivial
None significant.

---

## Nice-to-Haves

- An analysis of reward model generalization to out-of-distribution permutations (e.g., measuring reward model calibration on held-out orderings).
- A comparison where PO-Eval uses a different oracle family to test robustness of the evaluation benchmark itself.
- Ablation on transformer size to assess sensitivity to model capacity.

---

## Novel Insights

RewardRank's key insight—that permutation-level utility can be learned end-to-end from sparse logged interaction data and used to directly supervise a differentiable ranker—is a meaningful reframing of the LTR problem. More practically novel is the empirical demonstration that NDCG-optimizing rankers systematically fail to maximize counterfactual utility (Table 1), and the dual-protocol evaluation infrastructure that makes this claim testable. The combination of soft permutation gradients with a misspecification-aware reweighting scheme is technically clean. The LLM-as-User evaluation paradigm, while currently unvalidated against real users, points toward a scalable methodology for offline counterfactual ranking evaluation that the broader community can iterate on.

---

## Suggestions

- Provide an empirical analysis of how well the reward model generalizes to permutations not observed during training, to directly address the distribution shift concern.
- Validate LAU-Eval's fidelity by comparing simulated purchase rates to real user behavior on a held-out test split (even partially).
- Discuss the Table 1 vs. Table 2 NDCG discrepancy explicitly—understanding why maximizing counterfactual utility leads to better NDCG on real clicks would strengthen the paper's thesis.

---

## Score and Decision

RewardRank addresses a well-identified problem with a technically sound framework, proposes two reproducible evaluation protocols that the community needs, and delivers consistent empirical improvements. The major weaknesses—distribution shift in the reward model and unverified evaluation fidelity—are real but do not invalidate the core results. The real-click results in Table 2 provide independent empirical grounding. This is a solid paper with contributions worth sharing.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>