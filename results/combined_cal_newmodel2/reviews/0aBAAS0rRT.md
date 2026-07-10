Now I have all the data needed. Let me compile the final review.

## Summary

This paper proposes SigMap, a multimodal foundation model for wireless localization that introduces two innovations: (1) a cycle-adaptive masking strategy for self-supervised pre-training on CSI data that disrupts periodic shortcuts, and (2) a "map-as-prompt" framework that encodes 3D building geometry via a lightweight GNN as soft prompts for parameter-efficient cross-scenario fine-tuning. The parameter efficiency is compelling (0.085M parameters updated during fine-tuning, 30-minute training for 1000 epochs), and when map information is used, the method achieves substantial accuracy gains over CSI-only baselines on simulated data.

## Strengths

- **Well-motivated cycle-adaptive masking (Section 3.3).** The observation that standard random masking lets models exploit periodic shortcuts in CSI data, and the design of a mask that dynamically adapts to detected periodicity, is a genuinely domain-appropriate adaptation of masked autoencoding for wireless signals. This is a principled inductive bias rather than a generic SSL application.

- **Novel "map-as-prompt" framing (Section 3.4).** Encoding 3D building meshes via a lightweight GCN and prepending the result as soft prompts to a frozen Transformer's input is a creative and technically clean way to inject environmental geometry. Only 0.085M parameters (0.7%) are updated during fine-tuning (Table 5), with training taking 30 minutes for 1000 epochs — a practically meaningful advantage.

- **Honest 2D vs. 3D map ablation (Table 4).** The paper shows that 2D bird's-eye view retains most of the benefit (1.692m vs. 1.564m MAE), providing useful insight that most of the gain comes from topological/LoS cues rather than full 3D geometry.

## Weaknesses

### Major

- **NLoS-aware attention not described in the method section (Section 4.2 vs. Section 3).** Equation 11 introduces an "NLoS-aware attention mechanism" described as "the key advantage" that "explicitly models multi-path propagation," but this mechanism appears only in the Experiments section and is absent from the Methodology section (Section 3). The method section describes only standard Transformer self-attention (lines 201-205) and a multi-BS fusion mechanism (Eqs. 9-10). A reader cannot reconstruct the full architecture from the method description alone, which is a fundamental completeness requirement for a paper claiming an architectural contribution.

- **"Zero-shot generalization" claim contradicts the experimental protocol.** The abstract (line 9) and contribution list (line 43) claim "strong zero-shot generalization to unseen environments," but Section 4.5 (line 317) explicitly states that "only the downstream task heads are fine-tuned using limited target samples (approximately 100 instances per scenario)" and calls this a "few-shot learning setup." No experiment evaluates the model on an unseen environment without any fine-tuning of the task head. This is a direct contradiction between the stated claims and the actual evaluation.

- **Headline comparisons conflate map information benefit with method benefit.** The paper's headline result — "SigMap achieves 1.564m MAE vs. 2.382m for LWLM, a 34.4% improvement" (line 245) — compares SigMap (with map access) against LWLM (a CSI-only method without map access, as acknowledged indirectly in line 97). The actual method-level comparison on matched inputs (SigMap w/o map vs. LWLM) yields only 4.5% MAE improvement in single-BS and 4.7% in multi-BS. The abstract and headline framing present the 34.4% margin as a method-level achievement without disambiguating the role of the additional data modality.

### Minor

- **Numerical inconsistency: WAIR-D MAE.** The running text (line 340) reports SigMap's WAIR-D Scenario-2 MAE as 1.580m, but the corresponding table (line 336) shows 1.880m. It is unclear which value is correct.

- **Unexplained CDF@1m variation for LWLM.** LWLM achieves CDF@1m = 25.3% on O1_3p5 (Table 1) vs. 63.2% on DeepMIMO O2 (generalization table) at comparable MAE (2.382m vs. 2.213m), with RMSE jumping from 5.822 to 11.837. The paper offers no discussion of why this error distribution changes so dramatically across scenarios.

- **Cycle-adaptive masking implementation underspecified (Section 3.3).** The paper states that shift patterns are "comput[ed] using cross-correlation analysis" (line 133) but does not specify: which cross-correlation function, over which dimension (subcarrier, antenna, time), or how the dominant periodicity (d_final) and starting offset (j_0) in Eq. 6 are extracted. The core methodological innovation cannot be independently implemented from the description provided.

- **Masking ablation tested only on multi-BS (Table 3).** Since cycle-adaptive masking is claimed as a general SSL improvement, the ablation should also be validated for single-BS localization and generalization tasks. As presented, the benefit could be specific to the multi-BS setup.

- **No standard deviations reported despite claiming 5 independent runs** (line 239). Without variance information, the statistical significance of the modest method-level improvements (4-5%) cannot be assessed.

### Trivial

- **Speculation about "street-level photograph" as alternative to 2D polygon** (line 301) is unsupported by any experiment and reads as filler.

## Nice-to-Haves

- Evaluating on a real-world (measured, not ray-traced) dataset would substantially strengthen the generalization claims, since the gap between simulated and real wireless data is well-known to be large.
- Reporting full CDF curves (rather than just the single CDF@1m point) would help resolve ambiguity about error distributions.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

- **"No real-world data"** — This is a genuine limitation but is a scope-acknowledged issue; moved to Nice-to-Haves rather than a weakness, since the paper is upfront about using simulations.
- **"GCN only 2 layers provides limited receptive field"** — Speculative; not demonstrated as a problem by any experiment in the paper.
- **"2D vs 3D ablation suggests simpler encoding would work"** — Overinterpretation; the ablation shows 3D outperforms 2D, consistent with the paper's claims.
- **"Missing related works from robotics/CV literature"** — Removed per policy (cannot confirm existence of un-cited works from other fields).
- **Generic reproducibility nitpicks about baselines** — Partially valid but the paper cites original baseline papers; removed to avoid duplication with already-listed underspecification issues.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Move the NLoS-aware attention mechanism (Eq. 11) into Section 3 with a clear description of which representations it operates on and how it differs from the standard self-attention and multi-BS fusion.
2. Replace "zero-shot" with "few-shot" (or "few-shot generalization") in the abstract and contributions, or add a proper zero-shot experiment with no fine-tuning.
3. Restructure results presentation to clearly separate: (i) method-level comparison without map (SigMap w/o map vs. baselines), and (ii) the additive benefit of map information (SigMap w/ map vs. w/o map).
4. Fix the WAIR-D numerical inconsistency and report standard deviations for all metrics.
5. Provide the cross-correlation details for cycle-adaptive masking (function, dimension, periodicity extraction) to enable reproducibility.

## Score and Decision

**Round 1 bracket (3.5–5.5).** All retrieved calibration anchors within this range (4.40–5.33) share domain-specific SSL methodology and have similar weakness profiles: incomplete baselines, limited evaluation scope, or underspecified method details. The paper under review has stronger novelty (cycle-adaptive masking and map-as-prompt are both genuinely domain-specific innovations) than the SSL-masking anchors (MLO-MAE at 4.40, NAS-MAE at 4.00) and the domain-transfer anchors (Presto at 4.75). However, its structural issues (incomplete method description, claims contradiction) are more significant than any single weakness in the higher-scoring anchors (MW-MAE at 5.25, MRT at 5.75, prompt-tuning papers at 6.50–6.67), which had issues of marginal improvement or limited novelty rather than incomplete methodology.

**Narrowing rounds (targeted 4.0–6.0).** The Presto anchor (4.75, Reject) and the speech-separation anchor (5.00, Reject) provide the closest comparison: both are domain-specific SSL papers rejected due to a combination of incomplete evaluation and methodology gaps. SigMap surpasses both in novelty and is better structured, but the method-section omission and claims inflation are more severe than Presto's weakness of "applying an existing framework without significant modifications" (favorability -2.29). The MW-MAE anchor (5.25, Accept) shows that a paper with modest per-task gains can be accepted — but MW-MAE's method description was complete, whereas SigMap's method section is incomplete.

**Final score and decision: 5.0, Reject.** The core ideas (cycle-adaptive masking, map-as-prompt) are genuinely novel and well-motivated, and the parameter efficiency demonstration is strong. However, three issues collectively prevent acceptance: (1) the method section does not describe the full architecture as evaluated (NLoS-aware attention missing from Section 3), (2) the "zero-shot" claim is directly contradicted by the paper's own experimental protocol, and (3) the headline results conflate the benefit of an additional data modality with the benefit of the algorithmic contribution. These are fixable through rewriting and re-framing, and a carefully revised version could be a clean borderline accept (6). In its current form, the gap between what the paper claims and what it demonstrates is too wide.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>