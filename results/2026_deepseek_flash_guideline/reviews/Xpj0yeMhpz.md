Now I have a thorough understanding of the calibration landscape. Let me write the final review.

**Bracket reasoning:**
- Round 1 bracket: The same paper already appears in calibration (OHOmpkGiYK.md, avg 5.75, scores 6,6,3,8, decision: Reject). Anchors in the 5-6 range (unlearning papers) have avg scores 5.0-6.0. No papers in the >8.5 range for unlearning. This paper is clearly not in the 1-3.5 range (those are weak/unserious papers). The most comparable anchors sit between 5.0 and 6.0.
- The paper has a genuine conceptual contribution and strong empirical results, but also real limitations (Theorem 3.2 formal issues, β ablation missing, TOFU case study preliminary). None of the weaknesses are fatal. The human reviews of this same paper averaged 5.75 — consistent with my assessment.

**Final score: 6.0**, decision: Accept.

Here is my final review:

## Summary
2-3 sentence summary of the paper's contribution.

## Strengths
- strength 1 with evidence
- strength 2 with evidence

## Weaknesses
// List only reasonable points. Rank by severity.
// Not every paper has weaknesses at every tier. Leave a tier empty (or write "None") if nothing applies.

### Fatal
// Errors that invalidate the paper's core claims or results.
// Examples: fundamentally flawed methodology, unsupported central claim, incorrect proofs, data fabrication concerns.
// Most papers have none. Leave empty if none apply.

### Major
// Issues that a reviewer would weigh against acceptance, and that the authors should fully resolve in a rebuttal.
// Examples: missing critical baseline, overclaimed scope unsupported by experiments, significant methodological gap.
// Not every paper has major weaknesses. Do not invent them to fill this section.

- weakness 1 — why it matters
- weakness 2 — why it matters

### Minor
// Issues worth the authors' attention but unlikely to change an accept/reject decision.
// Examples: addressable in rebuttal, limited scope of one experiment, unclear phrasing of a claim, missing ablation that would strengthen but not invalidate.

- weakness 1 — why it matters

### Trivial
// Small issues the authors should fix but that carry no weight in evaluation.
// Examples: typos, minor notation inconsistencies, suboptimal figure choices, small presentation issues.

- weakness 1

## Nice-to-Haves
- suggestion that would improve but is not a core flaw

## Removed Points
Include something like this "These points are flagged to be removed, treat them with caution"
Weaknesses that are removed keep the details of the S/W just in case they are useful 

## Novel Insights
One paragraph synthesizing genuinely novel observations.
If no genuinely novel insight emerges from the reviews beyond the paper's own contributions, write
"None beyond the paper's own contributions."

## Suggestions
- specific actionable suggestion## Summary

This paper introduces a taxonomy of class-wise unlearning scenarios where the class label and target concept do not coincide — target mismatch, model mismatch, and data mismatch — formalizing three previously unstudied problems beyond conventional "all matched" forgetting. The paper analyzes representation-level forgetting dynamics ("representation gravity") and proposes TARF (TARget-aware Forgetting), a framework that couples annealed gradient ascent on forgetting data with selective gradient descent on hard-to-affect remaining data. Experiments on CIFAR-10/100 and ImageNet-1k show TARF dramatically outperforms existing baselines on mismatch scenarios while remaining competitive on conventional settings.

## Strengths

1. **Formal taxonomy of label-domain mismatch scenarios (Section 3.1, Figure 1, Table 1).** The paper systematically defines four distinct unlearning settings by defining relations among L_D (forgetting data domain), L_M (model output domain), and L_T (target concept domain). Prior work assumed all three coincide; this is the first work to name and categorize the three mismatch cases, giving the field a concrete vocabulary and evaluation framework for a class of practical unlearning problems that existing benchmarks ignore. The key insight — that the target concept may be a semantic group spanning multiple class labels, a subset of a class, or even a different granularity than the model was trained on — is genuinely novel.

2. **Substantial empirical gains on mismatch tasks (Table 3).** On CIFAR-100 target-mismatch forgetting, TARF achieves Gap=0.21 vs. the next best (GA) at 8.86 — a ~40× improvement. On data-mismatch (CIFAR-100), Gap=1.17 vs. GA at 2.43. On model mismatch (CIFAR-100), Gap=1.21 vs. SCRUB at 2.45. These are not incremental gains; they reflect qualitatively different outcomes — baselines largely fail on mismatch scenarios while TARF succeeds. The results are presented across 10 baselines, providing a comprehensive evaluation.

3. **Scalability to ImageNet-1k (Table 4).** TARF achieves the best overall Gap across all four settings on ImageNet-1k with a 1,000-class label space (e.g., Gap 3.97 on target mismatch vs. next best 5.05), demonstrating the approach works at scale with larger models and class spaces.

4. **Empirical demonstration of representation gravity and systematic ablations (Figures 3, 7).** The t-SNE visualizations and loss dynamics in Figure 3 make the core intuition about representation-level forgetting dynamics tangible. The ablations in Figure 7 validate key design choices (annealed vs. constant gradient ascent, initialization strength k, model architecture effects, operations on identified false-retaining data), providing insight into why TARF works.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Theorem 3.2 has formal/notational issues that undercut the "systematic analysis" framing.** The equation (2) contains the notation "λ_max(J_θ(·) x₁)" where J_θ = ∂h(x)/∂θ is a matrix of size |h|×|θ| and x₁ is a data input from s₁; multiplying a Jacobian by an input vector in this way is dimensionally suspect (J_θ expects a forward-pass activation or parameter-space argument, not a raw input). The proof is relegated to Appendix C (not available in the extracted text). While the core intuition — that representation proximity correlates with co-movement during gradient ascent — is plausible, well-supported by Figure 3, and not necessary for the method's validity, the paper presents this as a formal theorem with a mathematical bound that is not correctly stated. **This is a weakness in presentation/rigor, not a structural flaw.** The empirical evidence (Figure 3, Figure 9) independently validates the representation gravity concept.

2. **The Gap metric averages across quantities with different interpretations.** Gap = (1/4)∑|R_Retained−R_Opt| across UA, RA, TA, and MIA. In model mismatch, for example, the Retrained reference itself has UA=87.76 (since evaluated on superclass labels) while MIA=20.57, so the four components sit on fundamentally different scales. A method could match the Retrained well on UA/RA/TA but differ on MIA and receive a misleadingly large or small Gap. **However**, the individual metric values in Table 3 corroborate TARF's superiority — the dramatic Gap differences (e.g., 0.21 vs. 8.86) reflect real improvements, not artifacts. Still, the paper should either justify the composite more rigorously or present a disaggregated analysis as the primary result.

3. **The target identification phase assumes knowledge of how many classes in D_un belong to the target concept** (Section 2, "Dataset partition in mismatched setting"). The paper states: "we assume that the number of classes in D_un belonging to the target concept is known in target mismatch forgetting." It then uses the representation gravity signal (Figure 5a) to identify affected classes in practice. However, there is no systematic study of what happens when the target concept is fragmented across many classes, when the gravity signal is weak (few forgetting examples, high intra-class variance), or when the assumption is violated. The "Open challenge" section briefly acknowledges this, but empirical characterization would strengthen the paper.

4. **The β threshold (top-10%) is heuristic and not ablated.** The paper selects the top-10% most-affected data based on loss/accuracy change (Section 3.3). No ablation is provided showing how performance varies with different percentile choices (5%, 15%, 20%), which would strengthen the method's credibility.

5. **TOFU/LLaMA case study (Table 5) is preliminary and the table is difficult to interpret.** The table formatting is garbled with duplicated column headers, and TARF(GA) and TARF(NPO) produce identical numerical values in several blocks (e.g., 0.0762/0.0824 across all settings in the first block for LLaMA3.2-1B-Instruct). This requires clarification — either the two variants genuinely produce the same results (indicating the NPO component has no effect in these settings) or there is a reporting issue. The stable diffusion demo (Figure 6) shows only qualitative examples without quantitative metrics (e.g., CLIP score, FID). These case studies suggest generality but do not provide rigorous evidence on their own.

6. **Gradient cleaning vs. gradient ascent inconsistency.** The ablation on operations for D_U (Figure 7, right panel) shows that gradient cleaning (zeroing out the gradient) on false retaining data may outperform gradient ascent for retaining accuracy, yet TARF uses gradient ascent by default for this component. The paper does not resolve this tension.

### Trivial
None.

## Nice-to-Haves
- A systematic study of how TARF's Gap degrades when only 1-2 examples per class are provided for the forgetting set.
- Quantitative metrics for the stable diffusion concept removal experiments.
- Clarifying whether Theorem 3.2 could be stated as an empirical observation rather than a theorem, given the notational issues.

## Removed Points
These points are flagged as having been filtered out; treat them with caution.
- "The paper attributes the user's unlearning request to 'the model users' but requests may come from data subjects/copyright holders/regulators" — Minor framing nitpick. The paper's central point about misalignment between target concepts and class labels is unaffected.
- "The 'Different focus from prior methods' paragraph is too brief to be useful" — A presentation preference, not a substantive weakness. The paper's contribution is the new taxonomy and method, not a tutorial on existing methods.
- "The connection from practical trustworthiness concerns to mismatch scenarios is asserted rather than argued" — Generic criticism; the paper provides concrete examples in Figure 1 and Appendix D that instantiate the scenarios.
- "Standard deviations and significance tests not shown in main text" — The paper states these are in Appendix F.7 (removed by parser); not verifiable as missing.
- "CRITICAL ISSUE: Theorem 3.2 ... but this does not damage the paper's main empirical contribution" from the Harsh Critic — Already included as a minor weakness above; the framing as a "critical issue" is disproportionate given the critic's own acknowledgment that the empirical contributions stand independently.
- Strength Finder claim about "Cross-domain generalization beyond image classification" — Downgraded because the TOFU table is garbled and the stable diffusion demo lacks quantitative metrics. The contribution of these case studies is preliminary.

## Novel Insights

The reviews surface an interesting tension: the paper's "representation gravity" concept is intuitively compelling and empirically validated (Figure 3), but the attempt to formalize it as Theorem 3.2 introduces a mathematical gap that does not affect the paper's main contributions. This suggests a broader question for the unlearning community: can representation-level intuitions about forgetting dynamics be rigorously formalized, or are they inherently heuristic? The paper's strongest contribution — the mismatch taxonomy — does not depend on resolving this question, but future work building on this paper would benefit from a cleaner theoretical treatment. Additionally, the reviewers' divergent assessments (scores of 3, 6, 6, 8 in the calibration set) reveal that the paper's reliance on an extensive appendix and its somewhat dense notation create an accessibility problem that may cause readers to underestimate a genuinely novel contribution.

## Suggestions

1. Fix the notational issues in Theorem 3.2 (the J_θ(·) x₁ term is dimensionally suspect), or re-frame it from a theorem to an empirical observation/heuristic supported by Figure 3.
2. Either expand the TOFU/stable diffusion case studies with rigorous quantitative evaluation or present them more modestly as preliminary explorations.
3. Ablate the β threshold choice (5%, 10%, 15%, 20%) to justify the heuristic.
4. Resolve the gradient cleaning vs. gradient ascent finding from Figure 7 (right panel) — if cleaning is better, the method should be updated or the discrepancy explained.
5. Present individual metric comparisons (UA, RA, TA, MIA) alongside the composite Gap in a supplementary analysis to address concerns about the composite metric.
6. Improve the presentation of the TOFU table and ensure TARF(GA)/TARF(NPO) identical values are explained.

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| OHOmpkGiYK.md (same paper) | 5.75 | R1 bracket (5.5–7.5) | Same paper; human avg 5.75 (scores 6,6,3,8). My synthesis finds the taxonomy contribution stronger than Reviewer 3 (score 3) suggests, but acknowledges the weaknesses identified across reviewers. |
| pUOesbrlw4.md (Deep Unlearning) | 5.25 | R1 (3.5–5.5) | Training-free unlearning with SVD; strong method but incremental novelty. Current paper has stronger conceptual contribution. |
| TLBPjECC5D.md (Sparse Representations) | 5.25 | R1 (3.5–5.5) | Zero-shot unlearning via DKVB; model-specific. Current paper is more general and has broader empirical validation. |
| lgnAEBE1Xq.md (Contrastive Unlearning) | 5.00 | R1 (3.5–5.5) | Contrastive approach to standard unlearning. Current paper tackles a fundamentally different (broader) problem space. |
| SIZWiya7FE.md (Label-Agnostic Forgetting) | 6.00 | R1 (5.5–7.5) | Supervision-free unlearning; accepted. Current paper has comparable empirical rigor but a stronger conceptual contribution (new problem taxonomy). |
| 9hjVoPWPnh.md (Image-to-Image Gen) | 6.00 | R1 (5.5–7.5) | Unlearning for generative models. Different domain, comparable scope. |
| Xagys9QD3T.md (Pseudo-Probability) | 3.00 | R1 (1.5–3.5) | Standard unlearning method paper with limited novelty. Current paper is clearly stronger. |
| hwXUmwJAq5.md (UGradSL) | 3.00 | R1 (1.5–3.5) | Gradient-based unlearning with smoothed labels. Current paper addresses a fundamentally broader problem. |
| 5lUdTogEL3.md | 1.00 | R1 (<1.5) | Unrelated topic (person re-ID). Not comparable. |
| gwZ90hFSL2.md | 1.00 | R1 (<1.5) | Unrelated topic (robots, Chinese NLP). Not comparable. |

**Round-1 bracket:** 5.0–7.0. The paper sits above the method-focused unlearning papers (3–5 range) due to its conceptual contribution, but below the 7.5+ range (papers with flawless execution on well-defined problems) due to the formal issues and presentation gaps. The human review average of 5.75 (same paper) anchors this assessment.

**Final score:** 6.0 — borderline accept. The paper makes a genuine conceptual contribution (mismatch taxonomy) that opens a new evaluation dimension for the unlearning community, and TARF convincingly addresses the identified failure modes. The weaknesses are real but bounded and addressable.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>