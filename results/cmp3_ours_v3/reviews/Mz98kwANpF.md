Now I have enough calibration data. Let me produce the final review.

## Summary

This paper challenges the multi-component LoRA paradigm for multi-task learning. It first shows that M-LoRA (a simplified multi-head LoRA without routing) outperforms complex diversity-enforcing variants despite high inter-head similarity (Section 3). It then demonstrates that a single high-rank LoRA matches multi-component architectures at equivalent parameter budgets (Section 4). Building on these findings, the paper proposes Align-LoRA, which adds a KL-divergence-based representation alignment loss to encourage task-shared representations in a single LoRA adapter, evaluated on BBH generalization and an 8-task benchmark (Section 5).

## Strengths

1. **The M-LoRA finding is counterintuitive and well-demonstrated (Section 3, Table 1, Figure 2).** Removing the dynamic router from a multi-head LoRA and simply summing the heads (M-LoRA) outperforms diversity-enforcing variants like R-LoRA (75.45 vs. 74.67 avg). The inter-head similarity analysis in Figure 2 corroborates the mechanism claim — high redundancy, not diversity, correlates with better performance. This is a clean empirical result that challenges a real assumption in the literature.

2. **The rank-scaling experiment (Section 4, Tables 2–3) is the paper's most conceptually important finding.** Showing that a single LoRA adapter with sufficient rank matches multi-component architectures at equivalent parameter budgets (e.g., LoRA rank 10 at 0.25% params ties R-LoRA at 49.51 on Qwen2.5-7B; LoRA† rank 30 at 0.34% params essentially ties R-LoRA at 42.21 vs. 42.24 on LLaMA2-7B) directly questions whether multi-component designs are necessary. The breadth across LLaMA2 7B/13B and Qwen2.5 7B/14B strengthens this result.

3. **Align-LoRA is simple, well-motivated, and practical.** Applying representation alignment in LoRA's low-rank space follows naturally from the paper's thesis. The zero-inference-overhead property is a genuine practical advantage over routing-based methods like HydraLoRA and R-LoRA, which cannot merge their weights.

4. **The evaluation is reasonably broad** — multiple model families (Qwen2.5, LLaMA2, LLaMA3), multiple scales (3B–14B), and both in-domain (8-task) and out-of-domain (BBH) generalization.

## Weaknesses

### Fatal
None.

### Major

1. **Rank mismatch in Table 4 conflates the effect of the alignment loss with higher rank.** A-LoRA-K uses rank 8 while the multi-head baselines (HydraLoRA, R-LoRA, M-LoRA) use rank 4. Since Section 4 demonstrates that increasing rank substantially improves LoRA's performance, the improvement of A-LoRA-K over rank-4 baselines cannot be cleanly attributed to the alignment loss. The paper lacks a same-rank control (LoRA at rank 8 vs. A-LoRA-K at rank 8) within Table 4's experimental setup.

   *Mitigating factor:* LoRA at rank 10 (more parameters than A-LoRA-K at rank 8) scores 48.36 vs. A-LoRA-K's 50.28 on Qwen2.5-7B, suggesting rank alone does not fully explain the improvement. But a direct same-rank comparison is still the necessary control and is absent.

2. **No statistical significance or variance reporting across any experiment.** Not a single standard deviation, confidence interval, or indication of multiple runs is reported. This matters because several key comparisons involve small margins (e.g., M-LoRA 75.45 vs. R-LoRA 74.67 in Table 1 — a 0.78% gap; A-LoRA-K 80.06 vs. M-LoRA 78.51 in Table 5 on Qwen2.5-3B — a 1.55% gap). In LLM fine-tuning, single-run results at these margins are within the range of optimization noise. The reader cannot assess whether the reported improvements are systematic.

### Minor

3. **A-LoRA-M (MMD variant) performs worse than M-LoRA in several cases, undercutting the robustness claim.** In Table 4, A-LoRA-M scores below M-LoRA on Qwen2.5-7B (47.53 vs. 48.44) and Qwen2.5-14B (52.24 vs. 53.78), and essentially ties on LLaMA3-8B (45.42 vs. 45.35). The paper's claim that "both A-LoRA-K and A-LoRA-M significantly outperform the baselines" is inaccurate for A-LoRA-M. This suggests sensitivity to the choice of alignment metric, which the paper should acknowledge and discuss.

4. **The theoretical bound (Section 5.3) is a standard domain-adaptation-style bound applied to the LoRA setting, not a novel theoretical contribution.** The structure — empirical risk + distribution discrepancy + complexity term — follows a textbook form (cf. Ben-David et al., 2006; Mansour et al., 2009). The paper calls it "a novel generalization bound for MTL" without distinguishing it from prior bounds. The derivation is deferred to the appendix (stripped by the parser), but the presented form does not support a strong novelty claim. The paper should reframe this as an application of existing theory to motivate the alignment loss, not as a separate contribution.

5. **The "w/o Router" ablation in Table 1 is under-described.** The paper removes the router from HydraLoRA but does not specify how the heads are aggregated (summation? averaging?). This matters for understanding the comparison to M-LoRA, which uses explicit summation.

6. **The O(M²) cost of the pairwise KL alignment loss (Equation 5) is not discussed.** With M=5 or M=10 this is fine, but the paper does not address scaling to larger task sets, which would be a practical concern for broader adoption.

### Trivial
None.

## Nice-to-Haves
- Report results over multiple random seeds (≥3) with means and standard deviations for Tables 1, 4, and 5.
- Add a same-rank comparison: LoRA at rank 8 vs. A-LoRA-K at rank 8 in Table 4's setup.
- Clarify how the "w/o Router" variant aggregates its heads in Table 1.
- Tone down the novelty claim for the theoretical bound.
- Consider adding full fine-tuning as an upper-bound reference.

## Removed Points
These points are flagged to be removed; treat them with caution:

1. **Criticism about code availability** ("The paper states code is available anonymously, but this cannot be verified.") — Removed per rule: cannot question the existence of cited resources.

2. **Criticism about Figure 3 showing flat lines for LoRA/R-LoRA** ("Including them as baselines on a λ-axis plot adds no information and visually exaggerates Align-LoRA's superiority.") — Removed: flat lines for baselines on a hyperparameter sensitivity plot is standard visualization practice; the corresponding table is also provided. This does not misrepresent the data.

3. **Criticism about missing comparison to full fine-tuning** — Removed: requesting an upper bound outside the paper's stated scope (PEFT methods) is scope creep. The paper's comparisons are within the PEFT family.

## Novel Insights

The reviews reveal a clear structural tension in the paper: the two strongest empirical findings (M-LoRA's surprising effectiveness with redundant heads; high-rank single LoRA matching multi-component architectures) are compelling precisely because their experimental designs are clean and well-controlled. The Align-LoRA contribution, by contrast, suffers from a confound between the alignment loss and increased rank that weakens the causal claim. This suggests the paper could be strongest if it repositioned to feature the diagnostic findings from Sections 3–4 as the primary contributions and presented Align-LoRA as an initial validation of the shared-representation hypothesis, rather than making it the headline result. The paper's best evidence supports the claim that "multi-component architectures are unnecessary" — not that "representation alignment in a shared adapter is the reason for improvement."

## Suggestions
1. **Highest priority:** Add a same-rank controlled experiment: LoRA at rank 8 vs. A-LoRA-K at rank 8 in the Table 4 setup (5-task → BBH). This directly isolates whether the alignment loss provides benefit beyond higher rank.
2. Report all main results over ≥3 random seeds with means and standard deviations.
3. Reframe the theoretical bound (Section 5.3) as an application of existing MTL/domain adaptation theory to the LoRA setting, not as a novel generalization bound.
4. Clarify the "w/o Router" aggregation mechanism in Table 1.
5. Acknowledge and discuss why A-LoRA-M (MMD) underperforms M-LoRA in several settings.

## Score and Decision

**Calibration anchors (all from /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/):**

| Paper | Avg Score | Round | Comparison |
|---|---|---|---|
| UnoLoRA (49ti6LOUw5) | 3.00 | R1 low | Similar topic (shared LoRA for MTL) but much weaker: only T5 models, narrower eval, no rank-scaling analysis. Current paper is clearly stronger. |
| MORE (LWvgajBmNH) | 4.00 | R1 mid-low | MoE LoRA for MTL, only GLUE eval. Current paper has broader evaluation and more interesting conceptual findings. |
| MoRA (SxOrhLuuVz) | 4.75 | R2 narrow | Comparable: both have interesting ideas about LoRA limitations but experimental confounds. Current paper's evaluation is broader. |
| PaLoRA (icDoYdUhRa) | 5.50 | R2 narrow | Pareto-front multi-task LoRA. Better controlled experiments. Current paper has more surprising findings but weaker Align-LoRA evidence. |
| C-Poly (G1Hlubz1fR) | 6.00 | R1 mid-high | Multi-task LoRA with shared + specialized modules. Stronger evaluation and methodology. Current paper has more provocative findings but weaker central contribution. |
| Multi-Task Fusion (iynRvVVAmH) | 7.00 | R1 high | Better experimental design across modalities. Current paper is below this level due to confound and missing variance. |

**Round 1 bracket:** [4.5, 6.0] — The paper is clearly stronger than UnoLoRA (3.0) and MORE (4.0) due to broader evaluation and more interesting findings, but below C-Poly (6.0) and Multi-Task Fusion (7.0) due to the rank confound and missing variance.

**Round 2 narrow:** The MoRA (4.75) and PaLoRA (5.50) anchors help pin the score. The current paper has more conceptually interesting findings than MoRA but suffers from a similar experimental confound issue. It is somewhat weaker than PaLoRA, which has cleaner experimental design. Final score: **5.0**.

This paper makes two genuinely interesting empirical findings (M-LoRA, rank scaling) that are worth publishing. However, the central claimed contribution (Align-LoRA) has an experimental confound that prevents clean attribution of the improvement to the alignment loss, and the absence of any variance reporting makes the reliability of all comparative claims uncertain. The paper sits at a borderline score: the findings justify interest from the community, but the experimental methodology needs tightening before the paper's strongest claims can be accepted at face value.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>