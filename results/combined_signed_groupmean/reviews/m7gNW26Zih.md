Now I have sufficient anchor data. Let me compile and write the final review.

## Summary

This paper addresses language-based audio retrieval on the CLOTHO dataset using a dual-encoder architecture enhanced with three techniques: (i) soft-label distillation from an ensemble of retrieval teachers, (ii) LLM-driven caption augmentation (back-translation and audio mixing), and (iii) cluster-guided auxiliary classification. The best single model achieves mAP@16 of 46.6 and a weighted ensemble reaches 48.8 on the development test split. However, the paper has a fundamental structural problem: the evidence does not support the claimed contributions.

## Strengths

- **Clear problem motivation.** The paper correctly identifies that CLOTHO's annotation structure — multiple captions per audio with potential semantic overlap across recordings — creates a non-binary correspondence problem that standard contrastive loss cannot handle. This framing is well-articulated in the introduction and Section 2.2.

- **Honest acknowledgment of limitations.** The abstract and limitations section concede that "cluster guidance yields mixed gains across backbones" and that single-model gains are inconsistent. This candor about the technique's limitations is refreshing (though it conflicts with the conclusion, as discussed below).

- **Reproducible system specification.** The three-stage training protocol (pretraining, finetuning with distillation, re-finetuning with classification) is described with concrete hyperparameters, optimizers, schedulers, and dataset splits. Tables 1 and 3 provide clear configuration specifications.

## Weaknesses

### Major

1. **Claimed novel contributions (ii) and (iii) are not supported by the evidence.** The paper presents LLM-based augmentation and cluster-guided classification as equal contributions alongside distillation. For the best model (PaSST) on the primary metric (mAP@16), adding augmentation *decreases* performance (46.62 → 46.41), and adding cluster guidance provides no recovery (S4: 46.39, S5: 46.50). For EAT and BEATs, cluster guidance consistently hurts or provides negligible gains. The abstract claims these techniques "jointly improve robustness," but the evidence does not support this for the paper's own proposed components.

2. **The main performance driver (distillation loss) is directly adopted from prior work without modification.** Section 2.2 states: "we adopted a distillation loss approach from the top-ranked DCASE 2024 Task 8 system (Primus et al., 2024)." This method was published for the *same task* (language-based audio retrieval) on the *same dataset* (CLOTHO). The paper does not identify any adaptation or modification. Combined with weakness #1, this leaves the paper with no clearly novel contribution that demonstrably works.

3. **No comparison to prior published results on CLOTHO.** The paper evaluates on the CLOTHO development test split but provides no comparison to any published state-of-the-art results (e.g., prior DCASE challenge submissions, Koepke et al. 2022, or any other method). The only baseline is System 1 (their own implementation without proposed components). Without situating results against prior work, the reader cannot assess whether mAP@16 of 46.6 is competitive or not.

4. **Inconsistency between the conclusion and the experimental data.** The conclusion states that clustering "contributed to additional performance gains," but the limitations section acknowledges "mixed single-model gains from cluster supervision," and the data in Table 2 shows cluster guidance does not help (and often hurts) across backbones and metrics. These statements are contradictory, and the data supports the limitations section, not the conclusion.

5. **Promised ablations are absent.** The introduction claims "thorough ablations on topic granularity and teacher softness" as a contribution. The paper contains no such ablations — no sweeps over number of clusters, distillation temperature, loss weights (λ₁/λ₂), or any other parameter that would constitute an ablation of these design choices. This promised analysis is missing entirely.

### Minor

6. **Unsubstantiated claim in the abstract.** The abstract states "ablations indicate consistent improvements under high correspondence ambiguity," but no experiment in the paper tests varying levels of correspondence ambiguity. This claim has no supporting evidence.

7. **No statistical significance or variance estimates.** Several critical comparisons hinge on differences as small as 0.01–0.12 mAP@16 (e.g., S2 vs. S3 for PaSST: 46.62 vs. 46.41). Without standard deviations or results over multiple seeds, it is impossible to determine whether any of the reported differences are meaningful.

### Trivial

None.

## Nice-to-Haves

- Report results on AudioCaps (used for pretraining) as a cross-dataset evaluation to demonstrate generalization.
- Analyze why augmentation and cluster guidance fail to improve PaSST, the best-performing model. Is there an interaction with model capacity or pretraining data?
- Provide qualitative examples of the LLM-mix augmented data to give insight into whether the mixed audio is acoustically coherent.

## Removed Points

These points were raised in the input review but are removed for the following reasons:

- **LLM mix acoustic coherence critique** (Section 2.4): Speculative criticism about whether mixed audio is "acoustically coherent" — no evidence is presented that this harms results, and the paper already shows the metric impact. REMOVED as speculative.
- **"We propose a novel approach" overstatement** (Section 2.3): While a fair observation, this is subsumed by the broader weakness (#1) about claimed contributions not being supported. REMOVED as redundant.
- **Ensemble validates ensembling rather than proposed components**: This is an observation about a standard technique, not a weakness of the paper. Ensembling diverse models is well-known to improve results. REMOVED.
- **Cross-dataset evaluation on AudioCaps**: Scope creep. The paper focuses on CLOTHO; reporting AudioCaps results is a nice-to-have, not a weakness. MOVED to Nice-to-Haves.
- **Section-by-section formatting/presentation notes**: Not actionable weaknesses; parser artifacts. REMOVED.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the paper honestly.** Acknowledge that soft-label distillation (adopted from Primus et al.) provides the primary gains, and that LLM augmentation and cluster guidance yield mixed/inconclusive results. The current framing is incompatible with the data.

2. **Add comparisons to published results on CLOTHO.** Without situating results against prior work, the contribution cannot be assessed.

3. **Deliver the promised ablations or remove the claim.** The introduction promises "thorough ablations on topic granularity and teacher softness" — these must either be provided or the claim must be removed.

4. **Run experiments with multiple seeds** to establish statistical significance, especially for comparisons with sub-0.1 mAP differences where noise could dominate the signal.

## Score and Decision

**Calibration analysis.** I retrieved and itemized several anchor papers from the human-review corpus. The closest anchor in methodology and outcome is **DM-Codec** (avg 3.00, reject), an incremental distillation paper where the novel components were functional but the contribution was deemed insufficient for ICLR. DM-Codec at least had working novel components, comparisons to prior work, and thorough ablations — all of which our paper lacks. **RetFormer** (avg 3.00, reject) similarly had SOTA results despite novelty concerns. Higher-scored anchors (CompA at 6.50, Doppelgänger at 6.25) had clearly identifiable and working novel contributions with rigorous evaluations. Our paper lacks these characteristics. The round-1 bracket of plausible scores was [1.5, 3.5], and round-2 narrowing confirms the paper sits at the lower end of this bracket due to (a) its novel components not working, (b) lack of prior-work comparisons, and (c) internal claim-data contradictions — all absent from the 3.0 anchors but present here.

**Final score: 3.0. Decision: Reject.**

The paper has a well-specified system and clear problem motivation, but the structural mismatch between its claims and its evidence is decisive for ICLR. The two components presented as novel contributions do not improve results, the primary working component is adopted from prior work, promised ablations are missing, and no comparisons to prior published results are provided.

MY FINAL SCORE: <score>3</score>
MY FINAL DECISION: <decision>Reject</decision>