## Summary

This paper challenges the prevailing Multi-Generator–Evaluator (MG-E) paradigm for ranking in recommender systems. It provides a theoretical argument that a sufficiently large single generator-only model can have lower approximation error than any finite MG-E system (Theorem 1). It then proposes **GoalRank**, a generator-only ranker trained via a group-relative optimization objective: using a learned reward model to construct a reference policy over groups of recommendation lists (Equation 4–5) and minimizing KL divergence. Offline experiments on ML-1M, Amazon-Book, and an industry dataset show large gains over baselines, and a 14-day online A/B test on a platform with 500M+ DAU shows consistent (though small) positive improvements across all business metrics.

## Strengths

1. **Well-motivated problem framing with empirical grounding.** The paper identifies that MG-E's gains saturate as the number of generators increases (Figure 1d) and uses this observation to motivate the central question — whether a single large generator could do better — rather than relying on pure speculation. This is a genuine, practically relevant problem.

2. **Large-scale online A/B test with consistent positive results.** The online evaluation (8 buckets, 14 days, tens of millions of users per bucket, Table 4) shows that GoalRank improves over the production MG-E baseline across all five business metrics (App Stay Time: +0.149%, Effective Views: +1.212%, etc.). The hybrid setting (GoalRank + MG-E) also shows gains, and the system has been deployed to full production traffic. This level of online validation is rare and constitutes the paper's strongest evidence.

3. **Ablations on group size and reward-model bias.** Tables 2 and 3 systematically explore the two key hyperparameters. Performance degrades gracefully rather than collapsing: moderate group sizes (8–20) are optimal, and even with substantial noise added to the reward model (λ=0.5, Table 3), GoalRank still outperforms all baselines. This suggests the method is not brittle.

4. **Honest limitations section.** The paper acknowledges that GoalRank is less flexible than MG-E in adapting to changing business objectives (line 323), a real practical limitation often glossed over in systems papers.

## Weaknesses

### Major

- **The contribution of the auxiliary policies ℳ versus the group-relative objective is not disentangled.** The training pipeline (Section 3.3) constructs each group ℬ₊ by taking the generator's output and combining it with outputs from auxiliary policies ℳ (heuristic methods and lightweight neural models). The reference policy π^ref and the training signal are therefore partly determined by the quality and diversity of ℳ. The paper does not ablate this: it does not compare GoalRank trained *without* ℳ (e.g., using only multiple lists sampled from the generator itself, or random perturbations). Without this control, the reader cannot tell how much of the reported gains come from the group-relative optimization principle versus simply having access to auxiliary policies' outputs during training. This is a genuine methodological gap in attribution.

- **The gap between offline and online improvements is large and unaddressed.** GoalRank's offline H@6 improvements over the best baseline are +17.12% (ML-1M) and +25.39% (Industry dataset, Table 1). Its online improvements over MG-E are 0.149% (App Stay Time) and 1.212% (Effective Views, Table 4). While it is expected that offline gains are larger than online gains, a factor of ~20× is unusual and warrants discussion. The paper presents the offline results as primary evidence of the method's effectiveness and the online results as confirmation, but does not acknowledge or explain this discrepancy. The most parsimonious interpretation a skeptical reader would reach is that the offline metric (predicting the user's last six historical interactions) is a weaker proxy for ranking quality than the paper implies, and the headline numbers in Table 1 substantially overstate the practical significance of the method.

### Minor

- **Theorem 1 and the training objective are narratively linked but formally disconnected.** Theorem 1 shows that *there exists* a sufficiently large generator-only model whose policy space has strictly smaller KL approximation error to π* than any k-mixture MG-E system. This is an existence result about function classes, not a guarantee that training with the group-relative loss (Equation 5) achieves this bound. The paper claims "we showed theoretically that GoalRank admits scaling laws" (line 274). Strictly speaking, Theorem 1 shows that a large *generator-only model* (not necessarily GoalRank, not necessarily trained with group-relative optimization) can achieve low error. The scaling laws are empirically validated (Figure 3), which is sufficient, but the theoretical framing slightly overstates the formal connection between the theorem and the method.

- **The group-relative normalization (Equation 4) is justified heuristically, not derived from the evidence bound.** The paper derives τ log Z = sup_π{ E[r] + τ H(π) } (line 138), which is the evidence bound, and notes the optimal policy is Boltzmann(r*/τ). It then replaces the inaccessible r* with biased r̂, and — under the condition that reward gaps dominate bias (Equation 3) — adopts a z-score normalization (subtract mean, divide by std) as the reference policy. The specific form of normalization is a sensible heuristic (z-scoring the rewards before softmax) but is not formally derived from the evidence bound nor from any optimality criterion under bias. The paper asserts the connection is "from" the evidence bound, but the actual step from bound → normalization is a pragmatic design choice, not a consequence.

### Trivial

- None that survived filtering.

## Nice-to-Haves

- **Ablation: train GoalRank without auxiliary policies ℳ.** Using only multiple lists sampled from the generator (or perturbed versions) would isolate the contribution of the group-relative objective itself.
- **Comparison: train a single large generator with the MG-E framework (generator + evaluator) at the same parameter scale.** This would test whether the bottleneck is the generator-only paradigm or just MG-E's inability to scale.
- **Discussion of the offline-online gap.** Even a short paragraph acknowledging the known limitations of offline metrics for ranking evaluation and explaining why the ~20× gap is expected would strengthen the paper.

## Removed Points

These points were flagged by a reviewer but are removed from the final review with justification:

1. **"Generator architecture is unspecified in the main text."** — The main paper describes the framework as model-agnostic, stating the generator "can be instantiated by any sequence generation model" (line 166). Architecture details are deferred to Appendix D.2, which is stripped by the parser. The main text provides enough information to understand the method's structure. *(Removed per rule: do not penalize missing appendix content.)*

2. **"Evidence upper bound is claimed but not shown."** — The paper derives τ log Z = sup_π{ E[r] + τ H(π) } (lines 134–140), which is the evidence bound. The derivation is present in the main text. The reviewer's claim to the contrary is factually incorrect. *(Removed per rule: remove factually wrong criticisms.)*

3. **"Offline evaluation is next-item prediction disguised as list ranking."** — Using the user's last L chronologically ordered interactions as ground truth with H@L, NDCG@L, MAP@L, and F1@L is a standard list-ranking evaluation protocol in recommender systems. The characterization as "disguised" is inaccurate. The valid concern about offline-online magnitude discrepancy is preserved above. *(Removed per rule: remove strawman weaknesses.)*

4. **"All baselines share same evaluator — ambiguous."** — The paper explicitly states "all baselines share exactly the same evaluator (reward model) as GoalRank" (line 236). This is unambiguous. *(Removed per rule: remove strawman weaknesses.)*

5. **"Scaling experiment could indicate baselines not designed to benefit from larger models."** — This is speculation about baseline design choices, not a specific identified flaw in the paper. *(Removed per rule: remove speculative criticisms.)*

6. **Various minor presentation nitpicks (the claim that "the theory and the method are narratively linked but formally disconnected" was raised in two forms and merged; the "connection missing" point was subsumed under the Minor weakness above).**

## Novel Insights

The most useful insight from the reviewer cross-examination is the recognition that the paper's evidence is structurally two-tiered: the offline results (Table 1, Figure 3) are consistent with the narrative of a scaling-amenable generator-only method but are substantially larger than what online deployment delivers. This pattern — large offline proxy numbers paired with small-but-positive online numbers — is common in production ML papers but is rarely discussed explicitly. The paper would benefit from acknowledging this directly and explaining why it is expected in list-ranking evaluation (e.g., the offline metric measures identity-prediction of past interactions, while online measures behavioral change, which is inherently harder to move). The auxiliary-policy ablation gap is the second genuinely novel observation: without it, the attribution of gains to the "group-relative principle" (the paper's claimed second contribution) is weaker than the paper suggests.

## Suggestions

1. **Add an ablation without auxiliary policies ℳ.** Train GoalRank using only the generator's own sampled lists (or random perturbations) to construct ℬ. If performance degrades significantly, the paper should honestly discuss what fraction of the gain comes from the group-relative objective versus the auxiliary signal.

2. **Add a paragraph discussing the offline-online gap.** Acknowledge that offline metrics (predicting historical interactions) and online metrics (improving user behavior) measure different things, and explain why the ~20× ratio is plausible given the production setting.

3. **Tone down the claimed connection between Theorem 1 and the training objective.** Replace "we showed theoretically that GoalRank admits scaling laws" (line 274) with "we showed theoretically that large generator-only models can in principle achieve lower approximation error; we then validate empirically that GoalRank exhibits scaling laws."

4. **Clarify the relationship between the evidence bound and the group-relative normalization.** State explicitly that the z-score normalization (Equation 4) is a heuristic choice motivated by the goal of preserving reward ordering under biased rewards, rather than a consequence of the evidence bound.

## Score and Decision

This paper presents a genuine practical contribution (a deployed generator-only ranker with positive online results) and a well-motivated problem framing. The online A/B test is the strongest evidence and cannot be dismissed. However, the paper suffers from (a) a missing ablation that entangles the claimed optimization principle from auxiliary data, and (b) a large, unaddressed gap between offline and online effect sizes that undermines the weight placed on the headline offline numbers. The core positive online result justifies the method's value, but the paper's current framing overstates the evidence for the group-relative principle specifically. A moderate revision adding the ablation and discussing the gap would substantially strengthen the paper.

MY FINAL SCORE: <score>7</score>
MY FINAL DECISION: <decision>Accept</decision>