## Summary

This paper introduces and formalizes Dual-level Noisy Correspondence (DNC), a new problem for Multi-modal Entity Alignment (MMEA) that accounts for noise in both intra-entity (entity-attribute) and inter-graph (entity-entity, attribute-attribute) correspondences. To address DNC, the authors propose RULE, a framework that: (1) estimates correspondence reliability via a two-fold principle combining uncertainty (Dempster-Shafer theory) and consensus; (2) uses these estimates for robust training through tailored loss strategies and reliability-weighted attribute fusion; and (3) incorporates a test-time reasoning module using a 72B MLLM (Qwen2.5-VL) with CoT prompting to uncover latent attribute-attribute connections. Experiments on five benchmarks show significant improvements over seven baselines across multiple noise levels.

## Strengths

- **A genuinely new and well-motivated problem formulation.** The Dual-level Noisy Correspondence (DNC) formulation — covering noise in both intra-entity (entity-attribute) and inter-graph (entity-entity, attribute-attribute) correspondences — is clearly distinct from prior MMEA work that assumes clean correspondences. The paper provides concrete motivation that this is a real issue (Appendix B statistics showing >50% noise in ICEWS benchmarks, Fig. 1(b) observations). [weight=7.56]

- **The two-fold reliability principle (uncertainty + consensus) is theoretically principled.** Theorem 1 correctly identifies that low uncertainty does not guarantee correct correspondence, and the consensus principle provides a necessary complement. The three-way pair division (S_U, S_I, S_C) maps naturally to different training strategies. [weight=8.61]

- **Consistently large empirical gains across five benchmarks.** At 50% DNC on ICEWS-WIKI (Non-name), RULE achieves H@1=58.2 vs. 42.4 for the best baseline MEAformer — a ~37% relative improvement. Gains are sustained across all five datasets, all noise levels (Inherent, 20%, 50%), and both evaluation protocols. [weight=11.20]

- **Comprehensive experimental design:** five benchmarks, seven baselines, three noise levels (including inherent real-world noise), two evaluation protocols, ablation studies (Table 3) cleanly separating training-time and test-time contributions, distributional analysis of reliability estimates (Fig. 3b, Fig. 4), and a noise-ratio sweep (Fig. 3a). [weight=9.28]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Test-time resource asymmetry in main comparisons.** Tables 1-2 present "Ours" results that include the Qwen2.5-VL-72B MLLM-based test-time reasoning (TTR) module, while none of the seven baselines have access to such a model. The paper states "For fair comparisons, we adopt the same backbone (i.e., CLIP) for all baselines and our method" — this is correct for the encoder backbone but does not address the asymmetry at test time. The ablation (Table 3) substantially mitigates this: w/o TTR still achieves 56.5 H@1 vs. the best baseline 42.4 on ICEWS-WIKI at 50% DNC, confirming the training-time modules carry the vast majority of the gain. However, the ablation is only reported on one dataset (ICEWS-WIKI), and the main comparison tables do not separate the MLLM contribution. The paper would benefit from either separating "with MLLM" and "without MLLM" results in the main tables or adding a clear caveat about this asymmetry. [weight=5.36]

- **Underspecified notation and strong assumption in the marginal-contribution-based estimation (Section 2.2.2).** The value function uses `s_i^j` which is not clearly defined — the earlier notation used `s_i` for entity-level similarity vectors, but here it appears to refer to attribute-level similarities. The max operator lacks an explicit argument. Assumption 1 (correctly associated attributes yield Δ ≥ 0; irrelevant attributes yield Δ < 0) is stated without justification and is strong: an irrelevant attribute could produce a positive marginal contribution by chance correlation, and a useful attribute could contribute negatively if it duplicates information already captured. The empirical impact is limited — the consensus-only variant (which relies on this estimation) underperforms uncertainty-only (48.3 vs 53.5 H@1) — but the notation should be cleaned up. [weight=6.68]

- **Missing limitations and cost analysis.** The paper does not discuss: (a) the computational cost of the 72B-parameter MLLM at test time (how many calls per query entity, total inference time, scalability to larger MMKGs); (b) the potential cold-start problem — early in training when entity representations are poor, even clean correspondences could yield high uncertainty and be incorrectly excluded from training; (c) failure cases or threshold sensitivity (though Appendix G.10 is mentioned for hyperparameter analysis). These gaps are notable given the test-time MLLM component is presented as a contribution. [weight=4.40]

### Trivial

- The evidence formulation e_ij = exp(tanh(s_ij/τ)) in Eq. 2 uses tanh clipping that introduces a soft upper bound on evidence. This design choice is not discussed or justified in the main text. [weight=3.11]

## Nice-to-Haves

- It would strengthen the paper to show the "w/o TTR" ablation results across all five datasets, not just ICEWS-WIKI, to confirm the training-time gains generalize.
- The noise injection strategy (random attribute replacement) could be supplemented with more subtle misattribution patterns to better simulate real-world DNC.

## Removed Points

These points were raised by the harsh reviewer but are flagged for removal after verification against the paper:

- "The noise injection strategy uses random attributes — a strong form of noise" — REMOVED: The paper follows standard practices from the noisy correspondence community (Natarajan et al., 2013; Huang et al., 2021) and also evaluates on inherent (real) DNC from real benchmarks, which already validates real-world robustness.
- "On DBP15K, RULE's gains are much smaller; on All-attributes, methods saturate" — REMOVED: These are observations about the data context, not weaknesses. Gains on DBP15K are still positive, and saturation on All-attributes is a characteristic of the setting, not a flaw.
- "The MLLM asymmetry is a fatal flaw" — DEMOTED from Fatal to Minor: The ablation (Table 3) clearly shows training-only performance (56.5 H@1) still dramatically exceeds baselines (42.4 H@1). The asymmetry is quantifiable and limited in impact.
- "Demand that baselines be augmented with the same MLLM" — REMOVED: This is a recommendation for additional experiments, not a verifiable weakness of the paper as written.
- "The joint noise modeling is very complex" — REMOVED: Stating a problem is complex is not a weakness.
- "The evidence formulation requires justification as a full weakness" — DEMOTED to Trivial as it is a design choice whose impact on final results is unclear.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Separate the MLLM-based (TTR) results from training-only results in the main comparison tables (e.g., an additional "Ours (w/o TTR)" row), or add a prominent footnote clarifying the test-time resource asymmetry.
2. Clean up the notation in Section 2.2.2: define `s_i^j` explicitly, specify the argument of the max operator, and discuss the limitations of Assumption 1.
3. Add a limitations paragraph covering computational cost of the 72B MLLM, cold-start concerns for early-training uncertainty estimation, and threshold sensitivity.
4. Consider justifying or discussing the tanh clipping in Eq. 2.

## Score and Decision

**Calibration Summary** (all anchors retrieved across rounds):

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| gwZ90hFSL2.md | 1.00 | R1 | No | Not comparable (robotics/NLP) |
| 5lUdTogEL3.md | 1.00 | R1 | No | Not comparable (person re-id) |
| u1cQYxRI1H.md | 0.50* | R1 | No | Outlier (scores 10,10,10,10) |
| P49gSPmrvN.md | 1.00 | R1 | No | Not comparable (discourse) |
| 5kMwiMnUip.md | 1.40 | R1 | No | Not comparable (jailbreaking) |
| a4O528mek9.md | 3.00 | R1 | No | Incomplete multi-modal data |
| NNUiUwQWx6.md | **5.75** | R1 | **Yes** | Neuro-symbolic EA — weaker than RULE; rejected despite good performance due to complexity/robustness concerns |
| ue1Tt3h1VC.md | **6.60** | R1 | **Yes** | MoMoK — MMKG representations; comparable method quality |
| z3dfuRcGAK.md | **6.67** | R1 | **Yes** | Generative EA — similar topic, slightly weaker empirical evidence |
| ftGnpZrW7P.md | 7.00 | R1 | No | Multimodal alignment — different focus |
| TPZRq4FALB.md | **8.00** | R1 | **Yes** | Multi-modal TTA with reliability — stronger uniformly; upper anchor |
| QQYpgReSRk.md | **6.25** | R2 | **Yes** | MOFI — noisy entity annotations; had major novelty concerns (-7.56 weight) |
| jJCeMiwHdH.md | 7.00 | R2 | No | Biomedical FMs + KGs |
| 5BXWhVbHAK.md | 6.33 | R2 | No | Synergistic modality training |

*Outlier: avg_score 0.50 but all scores 10 — likely a data error. Disregarded.

**Round 1 Bracket**: 5.5–7.5. The paper's strengths (empirical gains at 11.20, experiments at 9.28, two-fold reliability at 8.61) are comparable to or stronger than the top items of the 6.67 EA anchor (theory at 9.25, experiments at 8.34) and MoMoK at 6.60. The weaknesses are milder than those that led to rejection of the 5.75 NeuSymEA paper. The 8.00 TTA anchor is the upper bound — that paper has uniformly high scores with less significant weaknesses.

**Round 2 Narrowing**: Compared against the 6.67 EA anchor, RULE has stronger empirical evidence (11.20 vs. 8.34) and comparable theoretical foundation (8.61 vs. 9.25). Compared against the MOFI paper (6.25), RULE has no weakness as severe as MOFI's novelty concern (-7.56). The main weaknesses (TTR asymmetry at 5.36, notation at 6.68) are presentation issues that do not threaten the core claim that the training-time modules effectively handle DNC. Placed above the 6.67 EA anchor and below the 8.00 TTA anchor → **7.0**.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>