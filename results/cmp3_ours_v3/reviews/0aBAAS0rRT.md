Now let me compile the final review.

## Summary

SigMap proposes a wireless localization foundation model with two innovations: (1) cycle-adaptive masking that disrupts periodic shortcuts in CSI during masked autoencoding pre-training, and (2) a "map-as-prompt" framework that encodes 3D building geometry via GNN into soft prompts for parameter-efficient fine-tuning. Experiments on DeepMIMO and WAIR-D show improvements over OMP, CNN, SWiT, and LWLM baselines.

## Strengths

1. **The cycle-adaptive masking insight is well-motivated and domain-specific.** The observation that periodic patterns in CSI can serve as learning shortcuts for masked autoencoders (Section 3.3) is a genuine contribution that goes beyond applying generic SSL recipes to wireless data. This is the paper's most original idea.

2. **The map-as-prompt framework is architecturally clean and demonstrably parameter-efficient.** Encoding 3D building geometry via GNN into soft prompts that attach to a frozen backbone (Algorithm 1, Section 3.4) is a legitimate parameter-efficient strategy. Table 5 quantifies this clearly: 0.085M trainable parameters during fine-tuning vs. 11.73M total, with 30 min total fine-tuning time.

3. **The generalization experiments on held-out environments are the strongest evidence for the core claims.** Testing on DeepMIMO O2 and WAIR-D (100 city scenes, Section 4.5) with ~100 fine-tuning samples provides meaningful evidence for cross-scenario capability. The consistent improvement over LWLM on these unseen environments is the paper's most informative comparison.

## Weaknesses

### Major

1. **The "NLoS-aware attention mechanism" claimed as the key advantage is not described in the methodology.** Section 4.2 (lines 247-251) states: "The key advantage stems from our NLoS-aware attention mechanism that explicitly models multi-path propagation: α_i = exp(φ(o_s^(i) · W_NLoS)) / ..." However, this mechanism is completely absent from Section 3 (Methodology). The term **o_s** is never defined anywhere in the paper. Section 3.5 describes a different attention mechanism (Eq. 9) for multi-BS fusion using t_cls, which has a different functional form. Since the paper itself calls this the "key advantage" behind its SOTA results, its absence from the method description prevents proper evaluation of what drives the reported performance and whether the architecture is actually as described.

2. **Missing comparisons to the SSL-based localization methods discussed in related work.** The introduction (line 26) discusses CrowdBERT and signal-guided masked autoencoders as relevant SSL-based approaches whose limitations SigMap addresses. Yet the experimental comparison (line 243) includes only OMP (classical), CNN (supervised), SWiT (contrastive learning), and LWLM (foundation model). Without comparisons to the SSL methods the paper claims to advance beyond, it is unclear whether the reported advantages reflect a general improvement or are specific to the chosen comparison set.

### Minor

3. **Numerical inconsistency in a reported result.** The main text (line 340) states SigMap achieves "1.580 m on WAIR-D Scenario-2," but Table 4.5 (line 336) reports **1.880 m** for the same condition. The 0.3 m discrepancy (~19% relative error) needs correction.

4. **"Zero-shot" generalization claim is overstated.** The abstract (line 9) and contributions (line 43) claim "strong zero-shot generalization," but the generalization experiments (Section 4.5) fine-tune on ~100 samples per target scenario and provide 3D maps of target environments during inference. The paper itself calls this a "few-shot learning setup" (line 317). The term "zero-shot" is inconsistent with the experimental protocol, and the availability of target-environment 3D maps is a substantial source of environment-specific information that should be disclosed when describing the generalization setting.

5. **Periodicity detection procedure (d_final) is not specified.** The core cycle-adaptive masking innovation (Section 3.3, Eq. 6) depends on computing d_final, described only as "cross-correlation analysis" (line 133) with no algorithm, threshold, or procedure given. Without this, the core masking strategy cannot be reproduced.

6. **Fine-tuning protocol is ambiguous for cross-scenario experiments.** Section 3.4 (line 207) states that GNN parameters, projection MLP, and task head are all updated during fine-tuning. Section 4.5 (line 317) states that only task heads are fine-tuned during generalization experiments. The paper does not clarify whether the GNN and projection MLP are also updated in the generalization setting, or why the protocol differs.

7. **No variance estimates reported despite 5 independent runs.** Line 239 states results are averaged over 5 runs, but no standard deviations, confidence intervals, or error bars appear in the main tables. This makes it impossible to assess the statistical significance of the reported improvements.

8. **GPU type not specified in Table 5.** Training time (36 h pre-training, 30 min fine-tuning) is reported without specifying the GPU hardware.

### Trivial

None.

## Nice-to-Haves

- Clarify whether spatial pruning is applied to the Delaunay triangulation graph (Section 3.4), since Delaunay triangulation in 3D over building vertices and BS positions would create many edges that cross through free space without physical meaning.
- Discuss why strip-masking achieves better RMSE (0.972 m) than adaptive masking (1.099 m) in Table 3, even though adaptive masking improves MAE and CDF@1m.

## Removed Points

These points were considered but removed with justification:

- **Backbone under-specification**: Critic faulted missing backbone architecture details. The paper states "Detailed configuration parameters are provided in Appendix B.3" (line 237). The appendix was stripped by the parser; this is not an author omission. **REMOVED** per rule about parser-stripped appendix content.
- **Section 1.1 claim about periodicity asserted "without evidence"**: This criticizes a standard research-gap framing statement. Too generic to constitute a specific weakness. **REMOVED**.
- **Strip-masking RMSE trade-off in Table 3**: The critic noted strip-masking has better RMSE but worse MAE and CDF@1m. This is an observation about an ablation result, not a weakness of the paper. **REMOVED**.
- **2-D vs 3-D map showing modest 8% degradation**: Critic framed this as undermining the paper's emphasis on 3D prompts. The paper directly acknowledges and discusses this (lines 299-303), interpreting it as evidence that "most gain comes from topological/LoS cues." The paper's own interpretation is reasonable. **REMOVED**.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Move the NLoS-aware attention mechanism (Eq. 11) into the methodology section with proper definitions of all variables, and clarify how it relates to or differs from the multi-BS attention already described in Section 3.5.
2. Correct the numerical inconsistency (1.580 vs 1.880) in the WAIR-D result.
3. Add comparisons to CrowdBERT and signal-guided masked autoencoders, or temper the claims about advancing beyond SSL approaches.
4. Replace "zero-shot" with "few-shot" or "cross-scenario" throughout, and explicitly disclose that target-environment maps are used during inference.
5. Add standard deviations or confidence intervals to the main experimental tables.
6. Specify the GPU hardware in Table 5.
7. Provide the algorithm for computing d_final from cross-correlation.
8. Clarify whether the GNN and projection MLP are updated during cross-scenario fine-tuning in Section 4.5.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| NormWear (wearable sensing foundation model) | 3.00 | R1 | Weaker than SigMap — less novel methodology, more unclear components |
| WiMTR (WiFi human mesh) | 4.00 | R1 | Comparable core quality but SigMap has more novel methodological contributions |
| Big Learning (position paper) | 5.25 | R2 | Similar score tier but different paper type, not directly comparable |
| ECCT Foundation Model | 6.25 | R1/R2 | Stronger than SigMap — more complete architectural description, clearer presentation |
| Wi-GATr (wireless simulation) | 7.00 | R1 | Stronger — solid experiments, clear contribution, minor weaknesses only |
| CrossMPT (error correction) | 6.40 | R2 | Stronger — complete architectural description, clear evaluation |

**Round 1 bracket:** 4.5–5.5

**Final score rationale:** SigMap introduces genuinely novel domain-specific ideas (cycle-adaptive masking, map-as-prompt) with informative generalization experiments. However, the paper has a significant coherence problem: the mechanism it calls the "key advantage" (NLoS-aware attention, Eq. 11) appears only in the experimental section with undefined notation and is absent from the methodology. This is compounded by missing comparisons to the very SSL baselines the paper claims to improve upon. These issues prevent the paper from being a clear accept, but the core contributions are substantive enough to place it above reject-level work. Score: **5.0**.

<score>5.0</score>
<decision>Reject</decision>