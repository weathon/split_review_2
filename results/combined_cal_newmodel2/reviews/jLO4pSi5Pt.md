Here is my final consolidated review:

## Summary

This paper proposes L-TTA, the first method specifically designed for Test-Time Adaptation (TTA) of Vision-Language Models (VLMs) under long-tailed test distributions. The method consists of three co-designed components: Synergistic Prototypes (SyPs) combining Deterministic and Exclusionary Prototypes to enrich tail-class representations, Rebalancing Shortcuts (RSs) for learnable prototype adaptation with a class re-allocation regularization, and Balanced Entropy Minimization (BEM) to counter head-class bias in entropy minimization. Experiments across 15 datasets, 3 imbalance ratios, 5 backbones, and 3 benchmarks consistently show L-TTA outperforming 11 baselines.

## Strengths

- **Novel problem framing with concrete failure mode analysis.** The paper is the first to systematically study TTA for VLMs under long-tailed test distributions. The identification of two specific failure modes — Text-induced Tail Erosion and Modality-bias Amplification — goes beyond noting that long-tailed data is hard and provides actionable guidance for the method design. The observation that unimodal LT-TTA methods applied to VLMs cause cross-modal mismatch is a genuinely useful diagnostic.

- **Consistent empirical superiority across a large evaluation landscape.** The method is evaluated on 15 datasets under 3 imbalance ratios (10, 20, 50), 5 backbones, and 3 benchmarks (OOD, cross-domain, corruption). L-TTA is the top performer in nearly every setting, with systematic gains (typically 1–3% over the best baseline in accuracy, 1–2% in macro-F1). Tables 1, 2, and 3 collectively present a convincing case.

- **Computational efficiency is genuinely competitive.** Table 4 shows L-TTA runs in 1.45h with 1.89GB memory on ImageNet, comparable to the fastest training-free methods and far cheaper than training-based methods like SCAP (2.96h), RLCF (18.30h), or WATT (27.70h), while achieving higher harmonic means on both benchmarks.

- **Ablation studies validate all three components.** Table 6 shows that removing any component (DPs, EPs, RSs, BEM) degrades performance, and the full SyP+RS+BEM setup is the best, providing clean evidence that the design is not over-fitted to a single dominant component.

## Weaknesses

### Fatal

None.

### Major

None.

### Minor

- **The hyper-class vector count K is inconsistently specified.** In the implementation details (Section 4), K = 0.3 is given, but in the methodology (Section 3.2), K is defined as the number of hyper-class vectors (an integer count). The ablation (Section 4.2) varies K from 0.1 to 1 and finds K = 0.2 best, while Figure 4(c) labels the axis as 'b' rather than K. This strongly suggests K is a fraction/ratio (likely relative to the number of classes), but this is never clarified, creating a reproducibility gap. The authors should provide an explicit formula mapping the fraction to the integer number of hyper-class vectors.

- **The theoretical propositions (Prop. 1 & 2) are lightweight.** Proposition 1 states that EM gradients are negative for head classes and positive for tail classes — this is essentially a mathematical restatement of the known intuition that EM amplifies head-class confidence under imbalance, rather than a non-trivial theoretical result. Proposition 2 claims that BEM reduces the gradient gap between head and tail classes, but is presented as an inequality (Eq. 10) without derivation or interpretable bounds in the main text. The paper would be equally strong (and more honest) presenting BEM as a well-motivated empirical contribution without claiming theoretical guarantees.

- **The head/tail accuracy breakdown — the most direct evidence for the paper's central claim — is deferred to Appendix C.** Table 1 and 2 captions refer readers to the appendix for head/tail class accuracy. While macro-F1 captures class balancing, a head-vs-tail breakdown is the most interpretable evidence for whether L-TTA's gains come from better tail accuracy, maintained head accuracy, or both. Including this in the main paper (e.g., as a supplementary figure) would strengthen the central claim.

- **No error bars, standard deviations, or significance tests are reported** despite stating "We conduct 5 runs for each experiment." In long-tailed settings constructed via random subsampling, different random seeds produce different test distributions even at the same imbalance ratio. Without variance estimates, readers cannot assess whether L-TTA's 1–3% improvements over baselines are statistically significant or within the noise of test-set construction.

- **The RSs mechanism (Eq. 6-7) is underspecified in key details.** The attention operation Attn([v_c, t_c], q_j) concatenates a D-dimensional prototype with a D_t-dimensional text embedding, but the attention mechanism's dimensionality and whether q_j serve as keys, values, or both are not defined. Additionally, the paper does not clearly state which parameters are optimized by the BEM loss vs. the CRA loss in the combined objective (Eq. 11).

- **No discussion of limitations or failure cases.** The paper does not discuss when L-TTA might underperform — e.g., when the class prior estimate is unreliable early in the stream (a bootstrapping problem for Exclusionary Prototypes, since tail-class predictions may be unreliable before sufficient tail samples have been seen), or how the method handles truly novel classes in open-world scenarios.

- **Ablation studies on hyperparameters (λ, η, K, β) are conducted on a single dataset (ImageNet) with a single imbalance ratio (10).** Results may differ at higher imbalance ratios or on different domains.

### Trivial

None.

## Nice-to-Haves

- The CRA loss rationale borrows from MoE load balancing, but the connection to "discernable feature clustering" could be clarified. Load balancing encourages uniform assignment, while "discernable clustering" typically implies specialization — explaining why this tension is productive would strengthen the method description.
- Adding a brief limitations section would improve the paper's credibility.

## Removed Points

These points from the input review were removed with justification:

- **Criticism about appendix proofs being inaccessible** (Critical Issue 1: "The proof is deferred to Appx. A which was stripped by the parser, so I cannot assess its validity") — removed per hard rule: the parser strips appendices from all papers; they exist in the original submission.
- **Table 7 formatting complaint** — likely a parser artifact; the original table is probably well-formatted.
- **Generic section-by-section notes about abstract/intro verbosity** — parser artifact (repeated figure descriptions from PDF extraction).
- **Speculative-fatal claim about the propositions** (that they "overstate the rigor" beyond what is actually claimed in the paper) — the paper presents them as supporting justification, not as core theorems, so this criticism overstates the issue.
- **Strength conflicts with verified weaknesses** about "well-structured methodology" — the methodology description has real clarity gaps (K inconsistency, RS mechanism) that contradict an unqualified "well-structured" strength.

## Novel Insights

The reviews surface a subtle but genuine concern about the Exclusionary Prototypes: since EPs for each class are updated based on the model's current predictions, and those predictions are biased toward head classes early in the stream (due to the long-tailed distribution), tail-class EPs may be initialized with unreliable information. This bootstrapping problem — where the mechanism designed to help tail classes depends on having already seen enough tail-class data — is not discussed in the paper and represents a potential failure mode worth addressing in future work.

Additionally, there is an unresolved tension in the CRA loss: by forcing prototypes to distribute uniformly across hyper-class vectors (borrowed from MoE load balancing), the loss seems to encourage each hyper-class to cover all classes equally rather than specializing. The paper asserts this produces "discernable feature clustering" but does not explain why uniform assignment leads to discernable clusters rather than homogenized representations.

## Suggestions

1. Include the head/tail accuracy breakdown in the main paper (e.g., as a supplementary figure or sidebar table in the main body).
2. Clarify the K parameter: provide an explicit formula mapping the fraction value to the integer number of hyper-class vectors used in RSs.
3. Fully specify the attention operation in Eq. 6, including dimensionalities and whether q_j serve as keys, values, or both.
4. Add standard deviations or confidence intervals for the main results, especially given the stochastic test-set construction.
5. Add a brief limitations section discussing the EP bootstrapping problem and open-world scenarios.

## Score and Decision

**Calibration:**

*Round 1 bracket: [5.5, 7.5]*

*Anchors retrieved across rounds:*

| Anchor | Path | Avg Score | Round | Itemized? | Comparison |
|--------|------|-----------|-------|-----------|------------|
| DOTA | yD2JMeKumt.md | 6.00 (Reject) | R1 | Yes | TTA for VLMs but with weaker evaluation and a questionable human-feedback component; L-TTA has stronger empirical breadth |
| RLCF | kIP0duasBb.md | 6.67 (Accept) | R1 | Yes | TTA for VLMs across multiple tasks; cleaner method but less comprehensive evaluation within a single setting; L-TTA is slightly below |
| BLG | BUDxvMRkc4.md | 4.67 (Reject) | R1 | Yes | Long-tailed + VLMs (not TTA); criticized for incremental contribution and underperformance on head classes; L-TTA is clearly stronger |
| ROSITA | lF9QXpfNHm.md | 4.67 (Reject) | R1 | Yes | Open-world TTA for VLMs; shares similar weaknesses (no error bars, no limitations) but with more serious novelty concerns; L-TTA is clearly stronger |
| Multi-Label BEM | 75PhjtbBdr.md | 6.25 (Accept) | R2 | Yes | TTA with BEM for multi-label; similar presentation issues (unclear equations); L-TTA has broader evaluation (15 vs 3 datasets) |
| Noisy-TTA | iylpeTI0Ql.md | 6.00 (Accept) | R2 | Yes | Noisy TTA for VLMs; novel task framing with solid results; comparable evaluation rigor |
| PROGRAM | x5LvBK43wg.md | 6.20 (Accept) | R3 | Yes | Prototype-based TTA; shares "no limitations" weakness but has more negative-rated weakness items (-0.26, -1.67); L-TTA's weaknesses are all less negative |
| Concept Drift | b20VK2GnSs.md | 7.00 (Accept) | R1/R3 | No | Broader scope (concept drift from pre-training); higher score reflects tackling both gradual and sudden drift |

*Grounding:* L-TTA's highest-favorability strength (14.37 for novel problem framing) exceeds that of comparable anchors (PROGRAM's best strength at 14.49 for impressive results, DOTA at 13.70). All of L-TTA's weakness items have favorability in the 2.55–4.47 range, whereas PROGRAM and ROSITA have weakness items with negative favorability (-0.26, -1.67, -0.47, -5.57). The paper has no fatal or major flaws; every identified weakness is minor and fixable. The evaluation breadth (15 datasets, 3 imbalance ratios, 5 backbones) is among the most comprehensive in the TTA-for-VLM literature. Considering these comparisons, L-TTA sits above the 6.0–6.25 range of comparable anchors (PROGRAM, DOTA, Multi-Label BEM, Noisy-TTA) and slightly below the multi-task RLCF (6.67), yielding a final score of 6.5.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>