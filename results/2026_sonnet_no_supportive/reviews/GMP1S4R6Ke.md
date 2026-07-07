Now I have enough to draft the review. Let me verify the RSL sign issue and the headline numbers more carefully.Now I have enough to write the final review. The calibration bracket puts this paper between 3.5 and 5.5 — let me read one anchor paper in each range.Based on my reading of the paper and calibration against anchor papers, here is the final consolidated review:

---

## Summary

LoRA-Mixer is a modular MoE framework that routes task-specific LoRA experts through the linear projection matrices of the attention module (Q/K/V layers) rather than replacing FFN/attention blocks or appending parallel branches. It proposes a Routing Specialization Balance Loss (RSL) that combines a load-balance auxiliary term with an entropy-shaping objective, and supports two regimes: joint training with hard/soft routing and plug-and-play reuse of pre-trained LoRAs from public repositories. Evaluation spans 15 benchmarks across three backbone models (LLaMA3-8B, Mistral-7B, Falcon-Mamba-7B).

---

## Strengths

- **Attention-layer placement is principled and generalization-capable.** Targeting linear projection layers (universal to Transformers and SSMs) is a concrete design advantage over FFN-only methods. The claim is validated empirically with Falcon-Mamba-7B (Table 2), where MixLoRA—which is Transformer-specific and targets FFN blocks—cannot be applied, yet LoRA-Mixer still delivers consistent improvements.

- **Plug-and-play regime is concretely exercised.** Table 3 (Flan-T5 with internet-sourced LoRAs, 2K routing data, frozen expert weights) and Table 6 (OOD generalization vs. PHATGOOSE) directly demonstrate data-efficient reuse, with results on 4/5 GLUE tasks beating single-LoRA performance.

- **RSL data-efficiency shown in Table 9.** The controlled ablation (same architecture, same LoRAs, only routing loss varies) shows RSL achieves comparable performance at 2K samples to the auxiliary loss at 6-8K—a concrete and well-isolated finding.

- **Domain-aware routing demonstrated in Figure 4.** Expert 1 activates at ~35% for Medical with RSL vs. ~18% w/o RSL; Expert 2 peaks at ~38% for GSM8K. This is mechanistic evidence that RSL produces differentiated routing, not just an outcome metric.

---

## Weaknesses

### Fatal
None that fully invalidate the empirical contribution.

### Major

**RSL loss sign contradicts the stated design principles (Equations 5–9 vs. Section 3.3).** Equation 5 defines:

$$\mathcal{L}_{\text{RSL}} = \alpha \cdot \sum_{i=1}^K \bar{p}_i \cdot \bar{f}_i - \lambda \cdot \mathbb{E}_{x \sim \mathcal{D}}[\mathcal{H}(p(x))]$$

When minimized, the second term minimizes $-\lambda\mathcal{H}$, which is equivalent to *maximizing* $\mathcal{H}(p(x))$ — producing flat, uniform routing distributions. Yet Section 3.3 design principle (1) states: "minimizing $\mathcal{H}(p(x))$ reduces token-conditional uncertainty... directly promoting specialization without disrupting the balance," and the text additionally states that RSL works by "suppressing overly flat distributions" and "encourages high variance and peaked distributions." The gradient in Equation 9 adds $+\lambda(\log p_i + 1 - \mu)$, whose fixed point is a uniform $p_i = e^{\mu-1}$—again, uniformity. Both terms in $\mathcal{L}_{\text{RSL}}$, when jointly minimized, push toward uniform routing. Figure 4 empirically shows that RSL *does* produce peaked distributions, which suggests the loss may work, but the theoretical account — the "information bottleneck" framing, the "curvature provider" language, the gradient intuition — cannot be reconciled with the sign as written. Either the sign in Equation 5 is wrong (should be $+\lambda\mathcal{H}$ for entropy minimization) or the verbal description of RSL's mechanism is inverted. This is not a presentation ambiguity — the reader cannot trust the stated mechanism until this is resolved.

**Headline improvements in the abstract are not traceable to any main-text table.** The abstract and introduction both claim "+3.79%, +2.90%, and +3.95% on GSM8K, CoLA, and ARC-C, respectively." In Table 2 (LLaMA3-8B), LoRA-Mixer vs. the strongest competitor MixLoRA yields +1.09 on GSM8K, +1.55 on CoLA, +0.34 on ARC-C. In Table 8 (routing loss comparison), RSL vs. AESL on ARC-C gives +3.36, not +3.95, and Table 8 does not include GSM8K. No single table yields all three claimed improvements against any identifiable baseline. These numbers are the first quantitative claim readers encounter and are load-bearing for the abstract's conclusions; they must be sourced to a specific table and baseline.

### Minor

**Non-monotonic RSL performance at 4K in Table 9, deferred without main-text explanation.** At 4K training samples, w/ RSL = 78.77 vs. w/o RSL = 79.14 (RSL is *worse*), recovering only at 6K–10K. The paper acknowledges this in a single sentence: "We explain the suboptimal RSL results at 4k in A.16." Given that data efficiency is a central contribution claim, this non-monotonicity warrants at least a qualitative explanation in the main text—e.g., whether this reflects $\lambda$ sensitivity, optimization instability, or batch-sampling variance.

**Non-standard evaluation for Medical QA.** Section 4.1 states: "we use DeepSeek-R1 for evaluation" for MedQA. MedQA is a multiple-choice benchmark with determinate correct answers and standard exact-match scoring. Using an LLM judge introduces variance and potential positional/format biases, and makes the Medical column incomparable across methods if baselines were evaluated under exact match. The given justification ("domain-specific freedom and rigor") is not appropriate for a benchmark with unambiguous ground-truth labels.

**No ablation isolating attention-layer placement from RSL.** The paper's two architectural contributions—routing inside attention projection layers (rather than FFN layers) and the RSL loss—are always evaluated together. Without a condition that applies RSL to FFN-layer LoRA experts (as MixLoRA does), it is impossible to determine whether performance gains stem from the attention placement specifically or from RSL alone. Both contributions are interesting; the lack of isolation weakens the attribution.

### Trivial

- The "48% of trainable parameters" claim appears only in the appendix (A.4, A.7) without specifying which baseline serves as the 100% reference. Since multiple baselines exist (LoRAHub, MoLE, MixLoRA, GMoE), this figure is difficult to evaluate as written.

---

## Nice-to-Haves

- Quantify per-domain routing entropy (bits) for RSL vs. auxiliary loss conditions to formally validate the mechanism beyond Figure 4's visual comparison.
- Provide a sensitivity analysis for the $\lambda$ hyperparameter in RSL, which would clarify whether the 4K non-monotonicity is $\lambda$-dependent and guide practitioners in choosing this parameter.
- Show a brief ablation comparing attention-layer LoRA routing vs. FFN-layer LoRA routing under the same RSL objective to isolate the architectural contribution.

---

## Removed Points

*These points are flagged to be removed — treat them with caution.*

- **Table 2 baseline completeness**: The reviewer criticizes that LoRA-LEGO, PHATGOOSE, GMoE, AESL, DS-MoE do not appear in Table 2. These are compared in separate tables (4, 5, 6, 8) under clearly specified conditions. The experimental setups are distinct and the paper is transparent about this separation. Removed as a style preference, not a methodological gap.

- **LoRAHub not shown on Flan-T5 in Table 3**: LoRAHub is a gradient-free composition approach; Table 3 uses frozen LoRAs with router-only training, which is a different regime. LoRAHub is compared in Table 2. Removed as scope creep.

- **Figure 4 routing visualization not quantified**: The reviewer prefers routing entropy numbers over bar charts. Figure 4 is visually clear and informative; the absence of entropy values is a presentation choice moved to nice-to-have, not a methodological flaw.

- **Reproducibility/hyperparameter exposure**: The paper states hyperparameter exploration is in Appendix A.8. Removed per hard rule on appendix-deferred content.

---

## Novel Insights

The attention-layer placement of LoRA-MoE routing — operating in serial within the attention computation path rather than replacing FFN blocks or adding parallel branches — is an underexplored architectural choice with genuine benefits for SSM compatibility, since linear projection layers are ubiquitous across architectures. The data-efficiency angle in Table 9 (RSL matches auxiliary loss performance at ~50% of training data in the low-data regime) points to a real phenomenon in routing loss landscape geometry. If the RSL sign inconsistency is a typo and the intended formulation uses entropy *minimization*, the information-bottleneck framing becomes coherent: entropy regularization acts as a curvature provider on the routing simplex, and the generalization bound argument (Appendix A.2) would correctly explain the observed data efficiency. This would constitute a genuinely novel and principled contribution to routing loss design.

---

## Suggestions

1. **Resolve the RSL sign discrepancy.** If the intent is to penalize flat distributions (peaked routing, specialization), change $-\lambda\mathbb{E}[\mathcal{H}]$ to $+\lambda\mathbb{E}[\mathcal{H}]$ in Equation 5 and update Equation 9's gradient accordingly. If the sign is intentional (entropy maximization for exploration), rewrite Section 3.3 to describe entropy maximization rather than minimization.
2. **Trace headline numbers to a specific table and baseline.** Add a footnote in the abstract or a cross-reference sentence identifying which table and which comparison yields +3.79%, +2.90%, +3.95%.
3. **Add one or two sentences in the main text explaining the 4K anomaly** in Table 9 — even a qualitative account (e.g., $\lambda$ mismatch at intermediate data regimes) would suffice and would strengthen the data-efficiency claim.

---

## Score and Decision

**Calibration anchors retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `I1VCj1l1Zn.md` (DLP-LoRA) | 3.00 | R1 | Similar LoRA routing paper, weaker scope, rejected |
| `49ti6LOUw5.md` (UnoLoRA) | 3.00 | R1 | Single-LoRA multi-task, simpler, rejected |
| `XVHXVdoV11.md` (Collective Model Intelligence) | 3.40 | R1 | Model merging/routing, rejected |
| `762u1p9dgg.md` (MOEfication by Masks) | 3.40 | R1 | MoE sparsification, wider quality spread |
| `LWvgajBmNH.md` (MoRE) | 4.00 | R1 | LoRA-MoE multi-task, soundness concerns, rejected |
| `uWvKBCYh4S.md` (Mixture of LoRA Experts) | 5.00 | R1 | Basic LoRA mixture, accepted borderline |
| `uHTmx0nRfX.md` (MoTE) | 4.75 | R1 | LoRA-MoE for embeddings, borderline reject |
| `PPjpGTPG5K.md` (PERFT) | 5.33 | R1 | PEFT for MoE LLMs, mixed reviews |
| `IDJUscOjM3.md` (Self-MoE) | 6.00 | R1 | Self-specialized MoE, clean contribution, accepted |
| `lTkHiXeuDl.md` (HMoRA) | 6.00 | R1 | Hierarchical LoRA-MoE, accepted uniformly at 6 |
| `QHzzAU7Qf9.md` (SMEAR) | 6.00 | R1 | Soft MoE routing, accepted |
| `Pu3c0209cx.md` (Tight Clusters) | 7.00 | R1 | MoE routing theory, strong theoretical grounding |
| `t7P5BUKcYv.md` (MoE++) | 8.00 | R1 | MoE efficiency, strong accepted |
| `WbWtOYIzIK.md` (Knowledge Card) | 8.00 | R1 | Modular LLM plug-in, strong |
| `TwJrTz9cRS.md` (HiRA) | 8.00 | R1 | PEFT with strong ablations, clean |

**Round 1 bracket: 4.0 – 5.5**

LoRA-Mixer is clearly above the 3.0 papers (DLP-LoRA, UnoLoRA) in terms of scope, breadth (15 benchmarks, 3 backbone models), and the architectural novelty of attention-layer routing with SSM compatibility. It is comparable to MoRE (4.0) and MoTE (4.75) in ambition but shares their soundness concerns.

The RSL sign inconsistency is a serious flaw: it means the paper's stated theoretical mechanism (Section 3.3) contradicts the loss equation. Unlike MoRE's limitations (which were about novelty), this is a correctness problem in the central methodological contribution. The unverifiable headline numbers compound the concern. Compared to HMoRA (6.0) — which has a consistent hierarchical routing design, clear auxiliary loss formulation, and a uniform 6/6/6/6 reviewer reception — LoRA-Mixer falls short in theoretical rigor and presentation clarity.

**Final score: 4.5 (borderline reject).** The empirical contribution is real and the attention-layer placement is a useful idea, but the core loss formulation has a sign inconsistency that undermines the theoretical justification, and the abstract's headline numbers cannot be verified from any main-body table. These two issues together prevent acceptance without significant revision.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>