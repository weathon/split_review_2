## Summary

This paper introduces LoRA-Mixer, a framework that routes LoRA experts through attention projection layers (Q/K/V linear projections) rather than through FFN blocks as in prior LoRA-MoE work. The authors also propose Routing Specialization Loss (RSL), an entropy-regularized auxiliary loss that balances global load balance with input-aware specialization. The framework supports both joint training of adapters and routers, and plug-and-play routing over frozen, pre-trained LoRA modules. Experiments span 15 benchmarks across Transformers (LLaMA3-8B, Mistral-7B) and an SSM (Falcon-Mamba-7B).

## Strengths

- **Well-motivated architectural choice.** Placing the MoE mechanism at attention projection layers (Q/K/V) rather than in FFN is a genuinely sensible design decision. The paper correctly identifies that existing works either replace entire FFN/attention blocks or use parallel LoRA branches (shallow output fusion), and treating projection matrices as the locus of composition is architecturally clean (Section 3.2, Figure 1).

- **Architecture-agnostic validation.** The inclusion of Falcon-Mamba-7B (a pure SSM) alongside LLaMA3-8B and Mistral-7B is a genuine strength. Most existing LoRA-MoE methods are Transformer-only, so demonstrating that projection-layer routing transfers to SSMs is a non-trivial verification of the paper's stated design goal (Table 2).

- **Internet-sourced LoRA experiments (Table 3).** Demonstrating plug-and-play composition of externally downloaded LoRA modules with only 2K additional routing-training data is practically relevant and supports the "modular reuse" framing.

- **RSL loss has principled motivation.** The entropy regularization perspective on routing (Section 3.3) is conceptually clear. The critique that standard auxiliary loss penalizes variance and forces uniform expert usage is well-taken, and the gradient analysis (Eqs. 7-9) shows that RSL introduces a token-level signal where the standard auxiliary loss only propagates global gradients.

- **Cross-model transfer experiment (Table 5).** Transferring routers trained on Mistral-7B to LLaMA3-8B without any fine-tuning and observing non-degraded performance on 2 out of 3 tasks is a noteworthy result, suggesting the routing learned by RSL captures task semantics that survive model-weight differences.

## Weaknesses

### Fatal
None.

### Major

- **The "LoRA" baseline in the main comparison table (Table 2) is never defined.** The row labeled "LoRA" often performs competitively with LoRA-Mixer (e.g., LLaMA3-8B: LoRA 81.09 vs LoRA-Mixer 81.55 on Medical; LoRA 65.14 vs LoRA-Mixer 65.53 on GSM8K; LoRA 95.30 vs LoRA-Mixer 95.41 on SST2). The paper does not specify whether this is a single LoRA trained on multi-task data, LoRA applied only to projection layers, or something else. The baseline section (line 134) names MoLE, MixLoRA, LoraHub, LoRA-LEGO, and PHATGOOSE but omits any description of "LoRA." This undermines interpretability of the main result table, as the strongest competitor is not identifiable.

- **No variance or statistical significance reporting despite three runs being conducted.** The paper states "all experiments are run three times and the average reported" (line 136). Many improvements over baselines are small (e.g., LLaMA3-8B: SST2 +0.11, Medical +0.46, GSM8K +0.39, ARC-E +0.29 — all under 0.5 points). Without standard deviations or confidence intervals, it is impossible to distinguish real improvements from noise, especially on benchmarks like HumanEval Pass@1 which has known high variance.

- **The RSL vs. GMoE/DS-MoE/AESL comparison (Table 8) shows large unexplained gains.** For example, HumanEval Pass@1 goes from 50.46 (AESL) to 57.32 (RSL) — a ~7 point gap from changing only the routing loss. SST-2 goes from 91.38 (GMoE) to 95.41 (RSL) — a ~4 point gap. The paper states "all experiments are conducted with the same training data (2k) and the only difference is the routing loss." If true, such large differences warrant analysis: do the baselines (GMoE, DS-MoE, AESL) use different MoE configurations that make them ill-suited here? Does RSL qualitatively route to different experts? The paper provides no discussion.

- **The LoRA-LEGO comparison (Table 4) has two problems.** First, results for LEGO are cited "from its paper" — not run under the same conditions, data splits, or hyperparameters. The paper states that "LoRA configuration uses r=6 and alpha=12" but does not confirm LEGO used the same. Second, LoRA-Mixer loses to LEGO on RTE by over 10 points (61.47 vs 71.85). The paper's text says "our method outperforms LoRA-LEGO on three of the four tasks" — technically true but omits this 10-point reverse gap. On a small 4-task comparison, a single 10-point loss is not a minor detail and suggests the advantage is task-dependent in ways not analyzed.

### Minor

- **The data efficiency claim (Table 9) is overstated.** The paper states RSL "achieves comparable or even superior performance using only 51.62% of the training data." However, at 4K data w/o RSL beats w/ RSL (79.14 vs 78.77). At 6K they are essentially tied (79.41 vs 79.37). At 8K and 10K the RSL advantage is 0.27 and 0.43 points respectively — negligible. The advantage concentrates at the 1K-2K range, which is a valid and useful finding (low-data regimes are important), but the broad framing as a data efficiency advantage is misleading.

- **The function $F_{\text{route}}$ in Eq. (4) is vaguely defined.** The text says it "represents the routing function output by the fusion expert" — this is circular. From the standard MoE definition (Eq. 2), it is clear that $F_{\text{route}}$ applies top-k selection and weighted summation, but the paper's own notation introduces ambiguity at a point that is central to the claimed novelty (serial vs. parallel routing). A precise definition would improve clarity.

- **The PHATGOOSE comparison (Table 6) supports only a narrow claim.** Only 3 OOD datasets are shown with tiny improvements (QQP: +0.19, RTE: +1.44, MRPC: +0.20). The paper claims "excellent generalization ability" from this evidence. In-distribution results are deferred to the appendix. The margins are too small (especially without significance testing) to support the strong claim made.

### Trivial
None.

## Nice-to-Haves
- Include a proper parameter count comparison table substantiating the "48% of parameters" claim (referenced in the abstract but deferred to appendix).
- Add standard deviations to all main results.
- Analyze why RSL achieves such large gains over GMoE/DS-MoE/AESL — provide expert assignment analysis or clarify if these baselines are not designed for this setting.
- For the LoRA-LEGO comparison, either reproduce LEGO under identical conditions or acknowledge the comparison limitations and discuss the RTE failure case.
- Reframe the data efficiency claim to honestly state that RSL's main advantage is concentrated in low-data regimes (1K-2K).

## Removed Points
These points are flagged to be removed, treat them with caution:
1. **"48% of parameters claim is unsubstantiated"** — REMOVED because the paper explicitly references Appendix A.4-A.7 for parameter analysis. The appendix is stripped by the parser; it exists in the original submission. Per filtering rules, weaknesses about missing appendix content must be removed.
2. **Section-by-section nitpicks about the auxiliary loss definition in Eq. (3), notation issues, and related work style** — REMOVED as these are either appendix-deferred content (A.17) or style/preference observations that do not affect core contributions.
3. **"Narrow range of expert loads in Figure 3"** — REMOVED because the paper explicitly presents balanced activation (15-18%) as positive evidence against expert collapse, and separately shows task-level specialization in Figure 4. The criticism conflates aggregate balance (desired property) with lack of specialization (which Figure 4 addresses).

## Novel Insights
None beyond the paper's own contributions. The core observation that the harsh critic's most valuable critiques (undefined "LoRA" baseline, missing variance, unexplained RSL gains) are standard experimental rigor concerns rather than novel insights that would reshape the area.

## Suggestions
- Define the "LoRA" baseline in Table 2 explicitly — specify whether it is a single LoRA trained on all multi-task data jointly, LoRA applied only to projection layers, or another configuration.
- Report standard deviations for all main results since three runs were already performed.
- Analyze the large RSL gains over GMoE/DS-MoE/AESL: provide expert assignment analysis or clarify if these baselines use different MoE configurations.
- For the LoRA-LEGO comparison, reproduce under identical conditions or acknowledge limitations and discuss the RTE failure case.
- Reframe the data efficiency finding: RSL helps at low data (1K-2K) but does not consistently beat the auxiliary loss baseline at larger sizes. This is a meaningful finding on its own terms.
- Clarify $F_{\text{route}}$ in Eq. (4) — state explicitly that it applies top-k selection and weighted summation analogous to Eq. (2).

---

## Calibration Report

**Round 1 bracket (3.5–5.5).** The paper is clearly stronger than DLP-LoRA (avg 3.00, Reject) which had fundamental novelty issues, but weaker than HMoRA (avg 6.00, Accept) which had only minor weaknesses. Comparable papers in the LoRA-MoE space — MoLE (avg 5.00, Accept) and MoRE (avg 4.00, Reject) — provide the best anchors.

**All anchors retrieved:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| uWvKBCYh4S.md (MoLE) | 5.00 | 1,2 | Yes | Similar LoRA-MoE paper accepted despite marginal improvements and missing comparison variants. Our paper has more unique strengths (SSM validation, projection-layer routing) but also the additional undefined-baseline weakness. |
| LWvgajBmNH.md (MoRE) | 4.00 | 1,2 | Yes | Rejected LoRA-MoE paper with limited novelty and marginal improvement w/o significance. Our paper has better architectural novelty and broader evaluation. |
| lTkHiXeuDl.md (HMoRA) | 6.00 | 1 | Yes | Stronger paper with only minor weaknesses. Our paper has more severe experimental rigor issues. |
| yOOJwR15xg.md (MeteoRA) | 6.20 | 1 | Yes | Stronger paper with practical CUDA kernel contributions. Our paper lacks this practical engineering validation. |
| I1VCj1l1Zn.md (DLP-LoRA) | 3.00 | 1 | Yes | Weaker paper with fundamental novelty concerns. Our paper has clearer architectural novelty and broader evaluation. |
| 762u1p9dgg.md | 3.40 | 1 | No | MoE sparsification, different topic. |
| XVHXVdoV11.md | 3.40 | 1 | No | Model merging, different topic. |
| PPjpGTPG5K.md | 5.33 | 2 | No | MoE PEFT, different focus. |
| CRkoMdDlFh.md (I-LoRA) | 4.00 | 2 | Yes | Vision-language continual learning, different domain. |
| U3UtvOYMiw.md | 5.00 | 2 | No | Seeded LoRA, different approach. |

**Narrowing and final placement.** Comparing itemized impact scores: MoLE (5.00) had high-magnitude weaknesses about missing comparison variants (-9.69) and marginal improvements (-9.25), but the paper under review has the additional "undefined LoRA baseline" weakness (-10.00) that MoLE did not. Conversely, the paper under review has stronger unique strengths (+9.84 for SSM validation, +9.95 for internet-sourced LoRA) that MoLE lacked. The paper is thus weaker than MoLE on experimental rigor but stronger on architectural novelty and validation breadth, placing it between the two anchors. **Final score: 4.0** — the core ideas have clear merit but the experimental presentation has meaningful gaps (undefined baseline, no variance, unexplained large gains) that prevent acceptance in current form. These are fixable, making this a revision candidate rather than a rejection on principle.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>