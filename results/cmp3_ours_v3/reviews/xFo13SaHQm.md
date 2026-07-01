Now I have a clear calibration picture. Let me produce the final review.

## Summary

This paper identifies "copy-paste artifacts" in identity-consistent image generation, where models replicate the reference image pixel-for-pixel rather than generating the identity under natural variation. The authors contribute (1) **MultiID-2M**, a large-scale paired dataset (500k multi-ID images with hundreds of references per identity across ~3k identities, plus 1.5M unpaired images); (2) **MultiID-Bench**, a benchmark with a novel copy-paste metric M_CP that quantifies the fidelity-copy trade-off; and (3) **WithAnyone**, a FLUX-based model using paired training and a contrastive identity loss. Experiments show WithAnyone achieves high identity similarity (Sim(GT)=0.460, within 0.004 of the best) while maintaining low copy-paste (CP=0.144, far below InstantID's 0.337), positioning it as the only method that deviates from the trade-off curve that all competitors follow.

---

## Strengths

1. **Problem identification (Sec. 1, Fig. 2).** The "copy-paste artifact" is a precise, underappreciated failure mode. The observation that real face similarity varies naturally (0.77, 0.46, 0.46, 0.30 for the same person) while models peak at 1.0 is a striking illustration. The reframing from "maximize similarity at any cost" to "maximize similarity within the natural range of variation" grounds the paper conceptually.

2. **Copy-Paste metric M_CP (Eq. 2, Sec. 4).** The metric normalizes bias toward reference vs. ground truth by the angular distance between them, producing an interpretable score in [-1,1]. The bounds check out: g=r gives M_CP=1, g=t gives M_CP=-1. This is a genuine methodological contribution to evaluation practice.

3. **Dataset contribution (MultiID-2M, Sec. 3).** 500k paired multi-ID images with hundreds of references per identity, constructed through a well-documented four-stage pipeline with responsible-sourcing choices (CC filters, anonymized identifiers, exclusion of restrictive licenses) detailed in the Ethics Statement.

4. **Breaking the fidelity-copy trade-off (Table 1, Fig. 5).** WithAnyone achieves Sim(GT)=0.460 (2nd best, within 0.004 of InstantID's 0.464) while maintaining CP=0.144 — far below InstantID's 0.337. Fig. 5 shows WithAnyone is the only method that deviates from the trade-off curve that all other methods follow. This is the paper's central empirical claim, and the evidence supports it.

5. **GT-aligned ID loss (Sec. 5.1, Fig. 7).** Using GT landmarks rather than predicted ones to align faces for ArcFace embedding computation across all noise levels is a clean engineering solution to a real problem (unreliable landmark detection on noisy diffusion outputs). The ablation (Table 3) shows measurable benefit.

---

## Weaknesses

### Major
- **Aesthetics gap is significant and under-discussed (Table 1).** WithAnyone achieves Aes=4.783 — the **lowest** among all 14 evaluated methods on MultiID-Bench. GPT-4o Native scores 5.344, InfU scores 5.389, and InstantID scores 5.255 — a gap of 0.5+ points. The paper claims "maintains strong perceptual quality" (Abstract) and "maintaining—and in many cases improving—identity similarity" (Conclusion), yet the quantitative aesthetic scores tell a different story. The paper does not acknowledge this gap or offer hypotheses about its cause (e.g., does the GT-aligned loss wash out textural detail? Does paired training reduce aesthetic quality?). This does not invalidate the core contribution (breaking the fidelity-copy trade-off), but it is a significant omission in the presentation that should be addressed candidly.

### Minor
- **Contrastive loss ablation shows an unacknowledged pattern (Table 3).** Removing extended negatives (w/o Ext. Neg.) improves CP from 0.161 to 0.074 (lower is better) while degrading Sim(G) from 0.405 to 0.368. The paper says only that "the effectiveness of ID contrastive loss is greatly reduced" based on the Sim(G) drop, without discussing why removing negatives improves copy-paste. The plausible explanation (lower identity similarity mechanically reduces copy-paste artifacts) should be explicitly addressed rather than framing the loss entirely positively.

- **User study lacks key rigor metrics (Sec. 6.3).** The paper states "the copy-paste metric exhibits a moderate positive correlation with human judgments" but does not report the correlation coefficient. No inter-rater reliability metric (Fleiss' κ, ICC) is reported. The bubble chart (Fig. 8) lacks error bars or significance testing. While the quantitative metrics (Tables 1-2) carry the primary evidence, the claimed correlation with human judgments is unsubstantiated.

- **Phase 4 (quality tuning) is not ablated (Table 3).** The ablation removes Phase 3 (paired tuning) but does not isolate Phase 4. Since Phase 4 is described as enhancing "perceptual fidelity" and aesthetics is the weakest metric, the absence of this ablation is a gap.

- **Contrastive loss implementation is underspecified (Sec. 5.1).** The paper states that 4096 negatives per sample are drawn from the reference bank but does not describe the mechanism (e.g., queue-based memory bank, sampling strategy, embedding update frequency). This matters for reproducibility.

- **Sim(GT) uses a single ground-truth image (Sec. 4).** The benchmark measures identity similarity against one GT image per test case, which is a noisy reference point for identity. The paper does not acknowledge this limitation.

### Trivial
- The aesthetic scoring model is cited as "discus0434, 2023" — an informal GitHub handle rather than a published paper — making the evaluation pipeline harder to reproduce.

---

## Nice-to-Haves
- A candid discussion of the aesthetics gap and whether it stems from the paired training strategy, the GT-aligned loss, or other design choices.
- Report the correlation coefficient between M_CP and human judgments, and inter-rater reliability for the user study.
- Ablate Phase 4 to quantify its contribution to perceptual quality.
- Specify the extended negative pool mechanism (memory bank, sampling strategy, update schedule).
- Acknowledge the single-GT limitation of Sim(GT) and discuss potential mitigations.

---

## Removed Points
These points are flagged to be removed; treat them with caution.
- **Aesthetic scoring model citation (discus0434).** The critic noted this is an informal handle. However, per the filtering rules, any cited reference is assumed to exist. The point is retained as Trivial since it concerns citation form rather than existence.
- **"MultiID-2M ethical sourcing concerns."** No reviewer raised this; not applicable.
- **Missing related work concerns.** Removed per rule: missing related works are not to be raised since external confirmation is unavailable.

---

## Novel Insights

The harsh critic contributes a precise observation about the contrastive loss ablation that goes beyond the paper's own analysis: the improvement in CP when removing extended negatives is not discussed, and the paper frames the loss entirely positively when the evidence is more nuanced. This is a genuinely useful diagnostic point. Otherwise, the review largely validates the paper's own framing.

---

## Suggestions
1. Add a candid discussion of the aesthetics gap — acknowledge it explicitly and offer hypotheses about its cause (paired training? GT-aligned loss?).
2. Address the counterintuitive CP improvement when removing extended negatives in the ablation discussion.
3. Report the correlation coefficient between M_CP and human judgments, and add inter-rater reliability for the user study.
4. Ablate Phase 4 to quantify its contribution to aesthetic quality.
5. Specify the extended negative pool mechanism for reproducibility.
6. Acknowledge the single-GT limitation of Sim(GT).

---

## Score and Decision

**Calibration anchors used (all from the human-review corpus):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `u1cQYxRI1H.md` (IC-Light) | 0.50 | Bracketing (strong reject) | Completely different domain, not comparable |
| `5lUdTogEL3.md` (L-ReID) | 1.00 | Bracketing | Unrelated task, far weaker |
| `NWvsm2VxAM.md` (ID-Booth) | 3.00 | Bracketing | Similar topic but rejected for overfitting issues |
| `12iSWNLDzj.md` (Adversarial Face) | 3.00 | Bracketing | Different task, weaker |
| `88Qm4fGWzX.md` (Event-Customized) | 5.00 | Bracketing | Similar domain; task-setting concerns, unconvincing evaluation → weaker than paper under review |
| `Bz9wjvToCS.md` (DiffDeID) | 4.40 | Bracketing | Face de-identification; missing baselines, weak novelty → clearly weaker |
| `WUibctXLT7.md` (DreamMakeup) | 4.75 | Bracketing | Makeup customization; limited evaluation → weaker |
| `oGYGjPsVWb.md` (Customize T2I) | 4.50 | Bracketing | Customization with overfitting issues → weaker |
| `riieAeQBJm.md` (UIFace) | 6.00 | Bracketing | Synthetic FR; single contribution, missing theoretical analysis → comparable but narrower scope |
| `ZkFMe3OPfw.md` (InstantPortrait) | 6.67 | Bracketing | Portrait editing with dataset; clearer weaknesses in methodology clarity → slightly weaker overall |
| `vQxqcVGrhR.md` (DisEnvisioner) | 6.00 | Bracketing | Customization method; missing ablations, unclear disentanglement → comparable |
| `jw7P4MHLWw.md` (Personalized Rep) | 5.60 | Bracketing | Personalized representations; missing baselines → weaker |
| `6O3Q6AFUTu.md` (NoiseDiffusion) | 8.00 | Bracketing | Foundational method paper; no notable weaknesses → stronger |
| `OlzB6LnXcS.md` (Shortcut Models) | 8.00 | Bracketing | Generative modeling advance; clean contribution → stronger |
| `zMoNrajk2X.md` (CADS) | 8.00 | Bracketing | Sampling strategy; clean single-contribution → stronger |
| `gU58d5QeGv.md` (Würstchen) | 8.00 | Bracketing | Architecture efficiency; clean contribution → stronger |

**Round 1 bracket:** 5.5 – 7.5

The paper makes multiple substantial contributions (dataset, benchmark, metric, method) with a well-supported central claim. The weaknesses are real (aesthetics gap is under-discussed, ablation analysis omits a nuance, user study lacks rigor metrics) but bounded and do not undermine the core thesis. Compared to anchors, the paper is clearly above the 4-5 range of single-contribution papers with significant gaps, and slightly above the 6.0-6.67 range of papers with narrower contributions. It does not reach the 8.0 level of papers with cleaner, more foundational contributions and no notable weaknesses.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>