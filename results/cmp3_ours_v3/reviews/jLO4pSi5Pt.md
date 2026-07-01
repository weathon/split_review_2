Now I have all the information needed. Let me compose the final review.

## Summary
This paper introduces L-TTA, a test-time adaptation method for vision-language models under long-tailed test distributions. It proposes three co-designed components: Synergistic Prototypes (SyPs) combining deterministic and exclusionary prototypes to enrich tail-class representations, Rebalancing Shortcuts (RSs) with a class re-allocation loss, and Balanced Entropy Minimization (BEM) as a tailored objective. Experiments span 15 datasets, multiple imbalance ratios (10, 20, 50), and several backbones.

## Strengths

- **Well-motivated problem framing with concrete failure modes.** The paper identifies two specific failure modes for VLM-based long-tailed TTA — text-induced tail erosion (pretraining biases in text embeddings) and modality-bias amplification (unimodal TTA methods applied to VLMs) — which go beyond the generic "long-tailed TTA is hard" claim. (Section 1, lines 33–38.)

- **Unusually broad experimental scope.** The method is evaluated across 15 datasets (OOD variants, cross-domain, corrupted), three imbalance ratios, four additional backbones beyond ViT-B/16, and five runs per setting. Tables 1–5 present a coherent and thorough picture that gives confidence the gains are not dataset-specific.

- **Informative efficiency comparison (Table 4).** Wall time and memory are reported alongside a harmonic mean of accuracy and macro-F1. L-TTA (1.45h, 1.89G) achieves higher HM than DPE (1.38h, 1.81G) and is far cheaper than SCAP (2.96h, 1.97G) or RLCF (18.30h, 19.84G), making a credible case for practical deployability.

- **Clean ablation study (Table 6).** Each component (DP alone, EP alone, DP+RS, EP+RS, SyP+RS, SyP+RS+BEM) is systematically isolated on two backbones. The incremental gains are consistent, confirming both prototype types contribute.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **CRA loss gradient flow is unspecified.** Eq. 7 defines `c_{c,j}(v) = 𝟙(j = Argmax_{j'}(Attn(...)))`. The Argmax+indicator is non-differentiable, yet the RS parameters `q_j` are optimized via this loss (Eq. 11). While this follows the standard MoE load-balancing convention where gradients flow through the differentiable attention term and the hard assignment is treated as a constant, the paper does not describe this mechanism. Authors should clarify the gradient pathway.

2. **Baselines lack controls combining standard TTA with simple long-tailed corrections.** The paper argues (line 134) that combining logit adjustment with entropy minimization may exacerbate bias, but provides no experiments testing this. Adding standard TTA methods (e.g., TPT, TDA) augmented with a simple class-weighting or logit-adjustment scheme would clarify whether L-TTA's specific design is necessary or whether any reasonable long-tailed correction accounts for the gains. The paper references "Appx. G" for comparisons of BEM and classic LT methods, but these are not available in the main text.

3. **Theoretical propositions are underspecified in the main text.** Propositions 1 and 2 use vague phrasing ("certain measurements" for splitting head/tail classes) without stating the assumptions about the logit distribution. While proofs are deferred to the appendix, the main-text formulation alone does not meaningfully constrain the method's design or provide testable predictions.

4. **Hyperparameter K is inconsistently reported and ambiguously defined.** K is set to 0.3 in implementation (line 208), but the ablation finds K=0.2 optimal (line 334). K is described as "the number of hyper-class vectors" but takes fractional values (0.1–1.0 in Figure 4c, labeled "b"), suggesting it is a proportion of classes — this is never clarified.

5. **`\tilde{\mathbb{P}}` in BEM (Eq. 9) is used before being defined.** The term `(1 - \tilde{\mathbb{P}})^\beta` appears in the definition of `z'`, but `\tilde{\mathbb{P}}` is not explicitly introduced. From context it appears to be `\mathbb{P}_{\text{LTTA}}` from Eq. 8; this should be stated.

6. **No standard deviations reported despite 5 runs.** Tables 1–3 claim 5 runs but show no variance. This makes it hard to assess whether improvements over the best baseline are statistically significant, especially for small margins (e.g., 0.97% gap over DPE in Table 1, imb=50).

7. **Class prior estimation via pseudo-labels may create a feedback loop.** BEM updates its class priors based on its own predicted pseudo-labels (line 138). Early errors in pseudo-labeling could corrupt the prior estimate and amplify bias. The paper does not discuss or evaluate this risk.

### Trivial

- **Scope novelty claim is slightly overstated.** Claiming "first attempt" (lines 9, 47) is defensible for VLM-specific long-tailed TTA, but existing non-i.i.d. TTA methods (SAR, DELTA, DA-TTA) address distribution shifts that subsume imbalance. Softening the claim to focus on VLM-specific challenges would be more precise.
- **Figure 4(c) label uses "b" instead of "K"** for the hyper-class vector count, inconsistent with the text.

## Nice-to-Haves

- Analysis of failure cases: datasets or class splits where L-TTA does NOT improve relative to baselines.
- Discussion of error accumulation in prototype updates when early samples are misclassified.
- Explicit computational cost of the EP update (updating all C classes for each of Q views per image).

## Removed Points
These points were flagged during review but are removed for the following reasons:
- *"Eq. 4 has a formatting error in the denominator"* — parser artifact, not an author error.
- *"The CRA loss is non-differentiable — structural flaw"* — follows standard MoE load-balancing convention; gradients flow through the differentiable attention term. The paper should clarify but this is not a structural flaw.
- *"Baseline comparison is fundamentally unfair"* — the paper compares against 12 published baselines designed for the (balanced) setting; the absence of TTA+logit-adjustment controls is a valid weakness but does not make the comparison "fundamentally unfair."
- *"Missing appendix/proofs"* — these are stripped by the parser.
- *Various formatting/style observations* — parser artifacts.
- *"No limitations discussed in conclusion"* — standard for conference papers.

## Novel Insights
The input review's key insight is that the paper's evaluation conflates two factors: L-TTA's specific design vs. the mere presence of *any* long-tailed mitigation mechanism. This is a legitimate concern that the authors should address with controlled experiments. However, this does not invalidate the paper's contribution — the problem framing, the specific bi-modal design (SyPs, RSs, BEM), and the extensive evaluation still constitute a meaningful advance. The harsh critic's observation about the CRA gradient is nuanced: while the paper should clarify the mechanism, the approach follows standard MoE practice and is not a structural flaw.

## Suggestions

1. **Clarify the CRA loss gradient mechanism.** Describe whether `c_{c,j}` is treated as a stop-gradient constant (as in standard MoE load balancing) or whether a relaxation (straight-through, Gumbel-Softmax) is used.
2. **Add controlled experiments** comparing TPT/TDA augmented with simple logit adjustment or class-weighted entropy against L-TTA. This directly tests whether the specific SyPs+RSs+BEM design is necessary.
3. **Define `\tilde{\mathbb{P}}` explicitly in Eq. 9** and reconcile the K inconsistency (K=0.2 vs. 0.3, integer vs. fraction).
4. **Add standard deviations or confidence intervals** to Tables 1–3 given the claim of 5 runs.
5. **State the assumptions** underlying Propositions 1 and 2 more explicitly in the main text, or recast them as motivational observations rather than formal propositions.

## Score and Decision

### Calibration Anchors

Round 1 (bracketing) retrieved the following anchors:

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| Active TPT VLM (pdzHpQbGrn.md) | 2.50 | R1 | Reject-level VLM TTA paper; substantially less experimental rigor than the reviewed paper. |
| LVLM-CL (JIlIYIHMuv.md) | 2.50 | R1 | Reject-level continual learning paper; less scope and weaker method. |
| Efficient TPT (NeVbEYW4tp.md) | 5.00 | R1 | Similar TTA-for-VLMs topic; major methodological concerns; weaker experimental breadth. |
| CTTA prototypes (eXrUdcxfCw.md) | 4.80 | R1 | Prototype-based TTA; narrower evaluation, more significant weaknesses. |
| **Multi-label BEM (75PhjtbBdr.md)** | **6.25** | **R1** | Similar novel-TTA-setting paper; weaker experimental scope (3 datasets vs. 15). |
| **DOTA (yD2JMeKumt.md)** | **6.00** | **R2** | VLM TTA paper; comparable contribution level but had several significant methodology concerns. |
| **Noisy TTA (iylpeTI0Ql.md)** | **6.00** | **R2** | Novel task (noisy TTA); similar evaluation scale, accepted. |
| **DeYO (9w3iw8wDuE.md)** | **7.00** | **R1** | Stronger empirical TTA paper; cleaner single-idea method with better theoretical grounding. |
| Multi-modal TTA (TPZRq4FALB.md) | 8.00 | R1 | Significantly stronger: new benchmarks, cleaner method, excellent presentation. |

**Round 1 bracket:** 5.5 – 7.0 (excluding the 8.0 anchor as clearly stronger, and excluding sub-5.0 anchors as clearly weaker).

**Final calibration:** The reviewed paper's experimental breadth (15 datasets, multiple backbones, multiple imbalance ratios) is substantially wider than the 5.0–6.25 anchors. Its weaknesses (gradient clarity, missing controls, K inconsistency, underspecified theory) are all addressable and none threaten the core claim. However, it does not reach the 7.0–8.0 level where papers typically combine a clean single-idea method with excellent presentation and theoretical grounding. The most natural comparison is the Multi-label BEM paper (6.25) — both tackle a novel TTA setting and have similar presentation issues — but the reviewed paper's much broader evaluation warrants a slightly higher score. The DOTA paper (6.0) was rejected primarily due to methodological concerns about the online distribution estimation with single-image batches; the reviewed paper does not have comparable issues.

**Final score: 6.5** — a solid borderlineto-accept paper with a genuinely novel problem, unusually broad experiments, and several addressable minor weaknesses.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>