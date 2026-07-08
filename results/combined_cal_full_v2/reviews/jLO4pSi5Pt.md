Now I have all the data needed. Let me synthesize the final review.

## Summary

This paper introduces L-TTA, the first method for Test-Time Adaptation of Vision-Language Models under long-tailed test distributions. It combines three co-designed components — Synergistic Prototypes (SyPs), Rebalancing Shortcuts (RSs), and Balanced Entropy Minimization (BEM) — to address two identified failure modes: Text-induced Tail Erosion and Modality-bias Amplification. The method is evaluated across 15 datasets, 3 benchmarks, 3 imbalance ratios, 5 runs, and 4 additional backbones, showing consistent gains in both accuracy and macro-F1 while maintaining competitive efficiency.

## Strengths

- **Problem framing is genuine and well-motivated.** The paper identifies a clear gap: existing VLM TTA methods assume balanced test data, but real-world test streams can be long-tailed. The two identified failure modes (Text-induced Tail Erosion and Modality-bias Amplification) are plausible and supported by preliminary results. The observation that TTA's online (one-epoch) nature precludes standard LT remedies like up-sampling is a substantive constraint that justifies the need for a dedicated method. [weight=7.08]

- **Extremely thorough experimental evaluation.** The paper evaluates on 3 benchmarks (OOD, Cross-Domain, Corruption), 15 datasets, 3 imbalance ratios (10, 20, 50), with 5 runs per experiment, both accuracy and macro-F1 reported throughout, 4 additional backbones (ViT-L/14, ViT-H/14, SigLIP-L/16, MetaCLIP-BigG), and an efficiency analysis. This is substantially more comprehensive than most TTA papers. [weight=9.37]

- **Method is reasonably efficient.** L-TTA (1.45h, 1.89G on ImageNet) is much faster than heavyweight methods like RLCF (18.30h), WATT (27.70h), and SCAP (2.96h), while outperforming them. The design choice to keep prompts frozen and avoid gradient flow through the backbone is sensible. [weight=9.85]

- **Consistent empirical gains, especially in macro-F1.** Improvements are consistent across settings — e.g., +2.20% macro-F1 on the Cross-Domain benchmark, +2.64% on the Corruption benchmark over the next best method. Macro-F1 is the metric that matters most for long-tailed evaluation, and the gains here are not cherry-picked. [weight=10.53]

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Theoretical propositions are vaguely stated and overclaimed.** Propositions 1 and 2 (lines 132, 140) are presented as formal results with the phrase "certain measurements" to describe the head/tail split, without specifying what those measurements are, what distribution the expectation is taken over, or what assumptions are needed. Proposition 2's claim — that BEM reduces the gradient gap between head and tail classes — follows almost by construction from the penalty term that reduces gradients for confident classes. The paper claims these provide "theoretical capabilities" and "theoretical guarantees" (lines 44, 138), but the main-text formulations are closer to qualitative observations about gradient behavior. The empirical contribution does not depend on these being rigorous theorems, but the framing overstates what is established. [weight=2.86]

- **Ablation does not cleanly isolate BEM's contribution over standard EM.** Table 6 shows that the row "SyP(DP+EP)+RS" vs. "SyP+RS+BEM" differs by 0.36% accuracy and 0.66% macro-F1 on ViT-B/16. However, the paper does not specify what loss function "SyP(DP+EP)+RS" uses — whether it uses standard entropy minimization or no entropy loss at all. Without this clarity, the standalone contribution of BEM over standard EM cannot be assessed. The paper claims "BEM is an eligible advancement" (line 330) but the comparison conflates BEM's effect with the effect of any entropy-based objective. [weight=3.81]

- **MTA baseline entries show suspicious identical values across different imbalance ratios.** In Table 1, MTA shows exactly identical values (57.15 Acc. / 51.98 Mac.) for ImageNet-A across all three imbalance ratios (imb=10, 20, 50). Since the subsampled test distributions differ across imbalance ratios, the per-class accuracy and macro-F1 should vary. While this concerns a baseline rather than the proposed method, it raises questions about the experimental pipeline. The authors should verify and explain these entries. [weight=4.18]

- **No variance reported for 5 runs.** The paper reports running each experiment 5 times but never reports standard deviations or confidence intervals. With many baselines and small margins in some settings, this would strengthen confidence in the results. [weight=4.85]

### Trivial

- **K parameter inconsistency.** K is described as a count of hyper-class vectors (line 112: "$K$ hyper-class vectors $\mathbf{q} = \{\mathbf{q}_j\}_{j=1}^K$") but set to 0.3 in implementation details (line 208) with the best value found at 0.2 via ablation (line 334). K cannot be a fraction if it is a count; it presumably represents a fraction of the number of classes, but this is never clarified. The figure caption also refers to the variable as "b" rather than K (line 324). [weight=1.30]

- **Undefined notation and missing details.** (a) The BEM formulation (Eq. 9) uses $\tilde{\mathbb{P}}$ without defining it; from context it appears to be the softmax of $z'$, but this is never stated. (b) The class prior $\pi$ update mechanism is described as "continually updated based on the current predicted pseudo-labels" (line 138) without specifying how (EMA, direct count, momentum?). (c) The CRA loss (Eq. 7) uses notation that is hard to parse (same subscript $c$ for both averaging and indexing). [weight=-0.34]

- **Subsampling limitation unacknowledged.** The paper states that when constructing long-tailed test sets, "if the calculated cardinality is less than the class cardinality itself, we simply keep that class unchanged" (line 206). This means that for some classes the effective imbalance ratio may be lower than the stated value, but this limitation is not discussed. [weight=1.90]

## Nice-to-Haves

- Add a row to the ablation (Table 6) that replaces BEM with standard EM, so the standalone contribution of BEM can be cleanly assessed.
- Either clarify the definitions in Propositions 1/2 (head/tail split criterion, expectation distribution, assumptions) or reframe them as observations about gradient behavior rather than formal propositions.
- Resolve the K parameter inconsistency: clarify whether K is a fraction of classes or an absolute count, and explain why the default (0.3) differs from the ablated optimum (0.2).
- Report standard deviations for the 5 runs.

## Removed Points
*These points are flagged to be removed, treat them with caution*

- **"HM is never defined"** — Factually wrong; line 286 explicitly states "Here HM is the harmonic mean of Accuracy and Macro-f1." Removed.
- **"Missing related works"** — Cannot be verified without external sources; removed per protocol.
- **"Table 7 formatting errors"** — Likely parser artifacts (extra numerical entries for 3 ε conditions); removed per protocol on formatting artifacts.
- **"No limitations section"** — May be in the appendix (stripped by parser); removed.
- **"SAR/DELTA not included in comparison"** — The paper mentions unimodal LT-TTA methods (SAR, DELTA) to motivate the modality-bias problem, not as baselines; this is scope-appropriate.
- **"Modality-bias amplification claim not proven with controlled experiment"** — The claim references Figure 1(b.2) which is described as demonstrating the phenomenon; the figure is a schematic but the behavior is quantitatively shown in Figure 2 results.

## Novel Insights

The harsh critic usefully identifies that the theoretical propositions (Propositions 1 and 2) are essentially descriptions of gradient behavior presented as formal results — the paper would be stronger without the pretense of formal theory. The critic also correctly observes that the ablation design lacks a simple row (full method minus BEM using standard EM instead) that would cleanly isolate BEM's contribution, which is the most directly informative comparison given the paper's narrative about BEM's advantages over standard EM. The MTA baseline anomaly (identical ImageNet-A values across three different imbalance ratios) is a genuine concern about evaluation pipeline quality, though it affects a baseline rather than the proposed method.

## Suggestions

1. In the ablation (Table 6), replace or supplement the "SyP(DP+EP)+RS" row with a row that clearly uses standard EM instead of BEM, so the standalone contribution of BEM can be cleanly assessed.
2. Reframe Propositions 1 and 2 as observations about gradient behavior rather than formal theoretical propositions, or specify the head/tail split criterion and the distribution over which expectations are taken.
3. Resolve the K parameter inconsistency: clarify whether K is a fraction of the number of classes or an absolute count, and explain why the default (0.3) differs from the ablated optimum (0.2).
4. Verify and explain the MTA entries in Table 1 where ImageNet-A values are identical across imbalance ratios.
5. Report standard deviations for the 5-run experiments.

## Score and Decision

**Calibration.** Round 1 bracket (5.5–7.5) based on topical similarity to anchors. The closest anchors and how they compare:

| Anchor Path | Avg Score | Round | Itemized? | Comparison |
|---|---|---|---|---|
| `/home/.../lF9QXpfNHm.md` (ROSITA) | 4.67 | R1 | Yes | Less thorough evaluation; rejected due to incremental contribution; this paper is stronger |
| `/home/.../yD2JMeKumt.md` (DOTA) | 6.00 | R1, R2 | Yes | Similar topic but major methodological weaknesses (human feedback, distribution estimation); this paper's weaknesses are milder |
| `/home/.../75PhjtbBdr.md` (ML-TTA BEM) | 6.25 | R2 | Yes | Most similar profile — also proposes a BEM variant for a new TTA setting; accepted with clarity-related weaknesses; this paper has more extensive evaluation |
| `/home/.../kIP0duasBb.md` (RLCF) | 6.67 | R1 | Yes | Novel RL-based TTA for VLMs; accepted; this paper's evaluation is more thorough but theoretical framing is weaker |
| `/home/.../b20VK2GnSs.md` (Concept Drift) | 7.00 | R2 | Yes | Addresses long-tailed data in VL pre-training; accepted with substantial weaknesses; this paper has cleaner evaluation but less theoretical depth |
| `/home/.../TPZRq4FALB.md` (READ) | 8.00 | R1 | Yes | Strong multi-modal TTA paper; clearly superior motivation, theory, and benchmarks |

Round 2 narrowing: The paper sits between the 75PhjtbBdr.md (6.25) and kIP0duasBb.md (6.67) anchors. Its strongest weighted items (efficiency: 9.85, empirical gains: 10.53) match or exceed those anchors' strongest items. Its weaknesses all land in the minor/trivial range (highest: 4.85 for no variance reported), which is milder than DOTA's major methodological concerns. The MTA data anomaly (weight 4.18) is the most notable weakness but concerns a baseline, not the proposed method.

**Final score: 6.5. Decision: Accept.**

The paper makes a genuine contribution by identifying and addressing a previously unstudied problem (LT-TTA for VLMs). The experimental evaluation is unusually thorough. The weaknesses are real but minor — theoretical overclaiming, an incomplete ablation condition, and some clarity issues — and none threaten the core empirical finding that L-TTA consistently outperforms existing methods on this new task. All identified weaknesses are addressable in revision.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>