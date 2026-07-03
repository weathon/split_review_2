Now I have enough context for my final calibrated review.

**Bracket assessment**: Papers in the 5.5–7.5 range include TTA papers with new settings/methods (PROGRAM: 6.2, Multi-Label BEM TTA: 6.25, DeYO: 7.0). The 7.5–8.5 band includes READ (multi-modal TTA, new challenge) at 8.0. L-TTA sits between these bands: stronger evaluation breadth and more original problem formulation than most 6–7 papers, but with a resolvable Major concern about BEM prior initialization. I bracket the paper at **6.0–7.5**. Given its comprehensive empirical coverage (15 datasets, 3 imbalance ratios, 4 backbones), genuine theoretical contributions, and the BEM ambiguity being a clarification issue rather than a fatal flaw, I settle on **7.0**.

---

## Summary
This paper proposes L-TTA (Long-Tailed Test-Time Adaptation), the first TTA framework for VLMs under long-tailed test distributions. It identifies two specific failure modes of standard VLM-TTA in this setting (text-induced tail erosion; modality-bias amplification), then addresses them with three co-designed components: Synergistic Prototypes (Deterministic + Exclusionary), Rebalancing Shortcuts (learnable cross-attention with load-balancing-inspired class re-allocation loss), and Balanced Entropy Minimization (theoretically grounded to reduce the gradient gap between head and tail classes). Experiments span 15 datasets, three imbalance ratios, and four additional backbones.

---

## Strengths
- **Sharp problem motivation with concrete evidence**: The distinction between text-induced tail erosion and modality-bias amplification is non-trivial. Figure 1(b.2) demonstrates that applying the unimodal SAR method to a VLM backbone *hurts* performance — a clear negative result that motivates the need for bi-modal-aware solutions more credibly than citation-only motivation.
- **Breadth and consistency of evaluation**: L-TTA outperforms 12 baselines across 15 datasets (Tables 1–3), three imbalance ratios (10/20/50), and four additional VLM backbones including SigLIP and MetaCLIP-BigG (Table 5). The *consistency* of the advantage — rather than just its magnitude — is a strong evidential signal.
- **Macro-F1 as primary metric**: Reporting macro-F1 alongside accuracy is the correct choice for long-tail evaluation. The finding that macro-F1 advantage (+2.20%) significantly exceeds accuracy advantage (+1.02%) on the Cross-Domain Benchmark confirms L-TTA actually helps tail classes rather than marginally improving aggregate performance.
- **Efficiency profile (Table 4)**: L-TTA achieves the best HM on LT-CDB and LT-CB while running in 1.45h and 1.89G memory, outperforming methods that are 5–18× slower (RLCF: 18.3h, WATT: 27.7h). This practical efficiency is a concrete contribution.
- **Theoretical grounding**: Propositions 1 and 2 formally characterize why standard EM exacerbates head/tail gradient imbalance and prove BEM mitigates this gap. This provides interpretable motivation beyond purely empirical demonstration.

---

## Weaknesses

### Fatal
None.

### Major
- **BEM class prior initialization ambiguity (Section 3.2, Eq. 9)**: The paper states π is "set to the cardinality of all classes {|C_i|}_{i=1}^C in default" and "continually updated based on the current predicted pseudo-labels." It is unclear whether the *initial* π uses (a) ground-truth test-set cardinalities, (b) training-set cardinalities, or (c) online pseudo-label estimates. If (a), BEM receives oracle distributional information — knowledge of which classes are head vs. tail — that no baseline in the comparison receives. This would be a structural advantage that biases the reported gains for BEM. If (b) or (c), the concern dissolves, but the paper should state this explicitly. As written, the sentence "set to the cardinality of all classes" reads most naturally as the true test cardinalities, and no ablation exists to test sensitivity to initialization choice. An ablation comparing π initialized from true cardinalities vs. uniform vs. online pseudo-labels would resolve this and would itself be a meaningful finding.

### Minor
- **EP mechanism: stated rationale vs. actual behavior (Eq. 5)**: The paper claims EPs "enrich tail class representations" because they "can always be updated along the datastream." The EP update (Eq. 5) accumulates visual embeddings of *every* class from *every* sample, weighted by (1 − P(c|x̃)/max P). In a long-tailed stream, most updates to tail-class EPs use head-class images, contributing embeddings semantically far from the tail class. The ablation (Table 6) confirms EPs matter empirically (−3.22% macro-F1 without EPs), but the stated mechanism — that accumulating "improbable features" enriches tail representations — is not convincingly established. A visualization comparing DP-only vs. DP+EP tail-class representations (e.g., nearest-neighbor retrieval or T-SNE) would ground the claimed mechanism in observable evidence.
- **K notation under-specified**: K is described as "the number of hyper-class vectors" in Section 3.2, set to K=0.3 in implementation details, and swept as variable "b" in Figure 4c over {0.2, 0.4, 0.6, 0.8, 1.0}. The paper does not explicitly state that K is a fraction of C (total number of classes), leaving the parameter definition inconsistent across sections.

### Trivial
- **Food101 accuracy anomaly (Table 2)**: L-TTA's Food101 accuracy (85.55%) is slightly below TDA (85.94%), the only exception to near-universal wins. This is not discussed; a brief acknowledgment would strengthen credibility.
- **Table 7 column count**: The text describes ε ∈ {0, 1/3, 2/3} but Table 7 has four value columns per dataset. This may be a parsing artifact, but if genuine, the table and text disagree.

---

## Nice-to-Haves
- An explicit ablation of BEM with π initialized from (a) true cardinalities, (b) training-set priors, and (c) uniform priors — would demonstrate whether BEM is robust to the initialization and validate real-world applicability.
- A "BEM-only" ablation row in Table 6 (SyPs and RSs without BEM's special weighting) would isolate BEM's standalone contribution from joint optimization with prototypes.
- A failure-case analysis (settings or datasets where L-TTA does not improve) would demarcate boundary conditions and further support the paper's credibility.
- An explicit quantification of the correlation between class "richness" (zero-shot baseline per-class accuracy) and class cardinality would sharpen the text-induced tail erosion motivation from qualitative to quantitative.

---

## Removed Points
*These points are flagged to be removed, treat them with caution.*

- **Dataset protocol heterogeneous subsampling**: The harsh critic noted that some datasets retain unchanged classes when cardinality falls below the target size, potentially violating a clean exponential distribution. The paper acknowledges this design choice ("if the calculated cardinality is less than the class cardinality itself, we simply keep that class unchanged"). This is a reasonable protocol decision, not a flaw. **Removed.**
- **Ablation design: missing "BEM-only" row**: Moved to Nice-to-Haves because the SyP+RS+BEM vs. SyP+RS comparison does isolate BEM's marginal contribution, making this a refinement rather than a gap.
- **BEM "further exacerbates bias" theoretical argument (Section 3.2)**: The paper argues that applying logit adjustment to EM may further exacerbate head-class bias. This claim is stated but not proven in the main text. However, since it is deferred to appendices (which are stripped by the parser), it is not a genuine gap. **Removed.**

---

## Novel Insights
The EP design — accumulating prediction-weighted visual embeddings from *all classes* at *every sample* — sidesteps the fundamental tail-prototype update problem (tail prototypes don't update if tail samples rarely appear) by ensuring constant updates regardless of sample identity. This is architecturally novel relative to standard negative-cache TDA-style designs. Additionally, Proposition 1's formalization that standard EM disproportionately sharpens head-class predictions (because head classes dominate the maximal term in the softmax gradient) provides a clean theoretical explanation for a practically observed phenomenon, and the BEM penalty term's connection to confidence-weighted gradient rebalancing is conceptually generalizable beyond the long-tail setting.

---

## Suggestions
1. **State BEM initialization explicitly** in the main text: whether π starts from ground-truth test cardinalities, training cardinalities, or pseudo-label counts. Add a single ablation row comparing all three initializations to demonstrate robustness.
2. **Unify K notation** across the paper: define K = ⌊b·C⌋ in Section 3.2 and maintain this definition throughout implementation details and ablation figures.
3. **Add a brief sentence on the Food101 accuracy exception** in Section 4.1 to show awareness of boundary conditions.

---

## Score and Decision

**Anchor papers:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `lF9QXpfNHm.md` (ROSITA, open-set TTA for VLMs) | 4.67 | R1 | Weaker coverage, narrower problem than L-TTA |
| `A78MiKnGrL.md` (Search4Prompt, attribute-guided TTA) | 4.50 | R1 | Single idea, narrower scope |
| `Rc3RP9OoEJ.md` (InCPL, in-context prompt learning TTA) | 5.00 | R1 | Narrower scope, less evaluation breadth |
| `NeVbEYW4tp.md` (Self-TPT, efficient prompt tuning) | 5.00 | R1 | Less comprehensive than L-TTA |
| `75PhjtbBdr.md` (Multi-Label TTA with BEM) | 6.25 | R1 | Structurally similar: extends TTA to non-standard setting; L-TTA has more components and broader evaluation |
| `x5LvBK43wg.md` (PROGRAM, prototype-graph TTA) | 6.20 | R1 | Similar prototype TTA, but less comprehensive setting |
| `yD2JMeKumt.md` (DOTA, distributional VLM TTA) | 6.00 | R1 | VLM TTA, less comprehensive, rejected |
| `9w3iw8wDuE.md` (DeYO, disentangled TTA) | 7.00 | R1 | TTA with new insight and method; L-TTA is more comprehensive |
| `TPZRq4FALB.md` (READ, multi-modal reliability bias TTA) | 8.00 | R1 | Multi-modal TTA new challenge, comparable depth to L-TTA |
| `uAFHCZRmXk.md` (Modality Gap analysis VLM) | 8.00 | R1 | Analysis paper, different type |
| `WyEdX2R4er.md` (Visual Data-Type VLM) | 8.00 | R1 | Dataset/evaluation paper, different type |

**Round 1 Bracket**: 6.0 – 8.0. L-TTA clearly outperforms the 4.5–5.0 papers in scope and evaluation. It is comparable to the 6–7 range papers (Multi-Label BEM TTA: 6.25, DeYO: 7.0). The READ paper (8.0) is a close topical match: both address multi-modal TTA with a newly defined challenge and multi-component solution. L-TTA has broader empirical coverage than READ but carries the BEM prior initialization ambiguity as a resolvable Major concern.

**Narrowing**: Given the paper's genuine novelty (new problem, three co-designed components, theoretical propositions), breadth of evaluation (15 datasets, 4 backbones), and the fact that the Major concern is a clarification/ablation gap rather than a fatal flaw, I place L-TTA above the 6.25 Multi-Label BEM TTA and closer to DeYO/READ. Final score: **7.0**.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>