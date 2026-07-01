## Summary

This paper proposes ChaosNexus, a foundation model for forecasting chaotic systems. Its core architectural contribution is the ScaleFormer, a U-Net-inspired Transformer with hierarchical patch merging/expansion that encodes multi-scale temporal representations, augmented with MoE layers, a wavelet-based frequency fingerprint, and MMD regularization. The model is pretrained on 20K synthetic chaotic ODEs and evaluated zero-shot on 9.3K held-out systems and on real-world weather forecasting.

## Strengths

1. **Well-motivated architectural gap.** The paper correctly identifies that existing chaotic-system foundation models (Panda, DynaMix) operate at a single temporal resolution, which is a genuine limitation for systems with multi-scale dynamics. The U-Net-inspired hierarchical encoder-decoder (Section 3.2) is a sensible architectural response to this problem, and the motivation is clearly articulated in Sections 1 and 2.

2. **Large-scale evaluation.** The synthetic benchmark covering 9.3K held-out systems (Section 4.1) is genuinely large-scale. The evaluation uses both point-wise metrics (sMAPE) and attractor statistics (D_frac, D_step, D_lyap, ME_LRW), which is appropriate for chaotic systems. The Wilcoxon signed-rank test for statistical significance is good practice.

3. **Practically useful scaling analysis.** Figure 4 cleanly separates parameter scaling, per-system data scaling, and system-diversity scaling. The finding that adding more trajectories per system yields negligible gain while adding more systems yields substantial improvement (Section 4.3) is a concrete, actionable result for practitioners building scientific foundation models.

## Weaknesses

### Fatal

None.

### Major

1. **Attractor-metric claims are not supported by the data shown in the main paper.** The abstract claims "notable improvements in the fidelity of long-term attractor statistics," and Section 4.1 argues that attractor preservation is more important than point-wise accuracy for chaotic systems. Yet on the two attractor metrics displayed in Figure 2, ChaosNexus and Panda are essentially tied: D_step is ~1.2 for both, and on D_frac, ChaosNexus (mean ~0.225) is marginally *worse* than Panda (mean ~0.200). The actual improvement is on sMAPE (point-wise accuracy, ~70 vs ~75 at 128 steps, ~7% relative). This creates a disconnect between the paper's motivation (attractor statistics matter most) and its primary empirical finding (improvement is on point-wise accuracy, not attractor metrics). While the paper mentions additional attractor metrics (D_lyap, ME_LRW) in the appendix, the two main attractor metrics in the central figure do not support the "notable improvements" claim. The authors should reconcile this gap or adjust their claims.

2. **Weather evaluation conflates pretraining with architectural innovation.** The headline weather result (Section 4.2, Figure 3, abstract) shows ChaosNexus zero-shot achieving MAE ~0.8°C while baselines trained from scratch achieve ~3°C. However, the main Figure 3 does *not* include the relevant comparison against other chaotic-system foundation models (Panda, Chronos-S-SFT) that share the same pretraining corpus. That comparison is deferred to Appendix A.6 and mentioned only briefly in text. Since the 4× gap over scratch-trained baselines is overwhelmingly attributable to large-scale pretraining on 20K chaotic systems (a benefit shared by any model pretrained on this corpus), the reader cannot assess from the main paper how much of the weather improvement comes from the multi-scale architecture versus pretraining itself. The authors acknowledge the pretraining advantage in the text, but the visual presentation gives an inflated impression of the architectural contribution. The fair baseline comparison should be prominent in the main paper.

3. **Multiple architectural differences confound attribution to the multi-scale component.** ChaosNexus differs from Panda (the key baseline) in several ways: (i) U-Net hierarchical multi-scale encoder-decoder, (ii) dual axial attention instead of standard attention, (iii) MoE layers instead of standard FFNs, (iv) wavelet-scattering frequency fingerprint conditioning, and (v) MMD regularization in the training objective. The paper states that ablation studies are in Appendix A, but the main text does not isolate the multi-scale component from these other changes. Without an ablation that controls for the other four differences (e.g., a variant without patch merging/expansion but with axial attention, MoE, wavelet fingerprint, and MMD), the central claim that multi-scale structure drives the observed improvements is not directly supported by evidence in the main paper.

### Minor

1. **"Key insight" about diversity-driven scaling is framed as more novel than it is.** The paper presents the finding that generalization is driven by system diversity (not per-system data volume) as a "guiding principle" and "key insight," but explicitly acknowledges that "prior work, such as (Lai et al., 2025), establishes the scaling law for system diversity, which our Figure 4(c) corroborates" (Section 4.3). The genuinely new contribution is the complementary finding that per-system trajectory volume does not help (Figure 4b), which is a useful refinement. The framing in the abstract and conclusion overstates the novelty.

2. **No limitations or failure-case discussion.** The paper has no section discussing what types of chaotic systems the model handles well or poorly, conditions under which it might underperform, or scope boundaries (e.g., only ODE-based systems, limited variable count). Given the strong claims, this is a notable gap.

3. **Patch size D is never specified numerically.** Section 3.1 defines S = floor(T/D) + 1 patches of length D, but D is never given a concrete value. Since D determines the temporal resolution of "fine-grained" modeling and affects the hierarchy depth, this parameter should be stated explicitly.

4. **Computational cost not discussed.** The model has 52M parameters with MoE layers and dual axial attention, but no training/inference cost comparison to Panda or other baselines is provided. Given the modest performance improvements, cost differences matter for practical adoption.

### Trivial

None that survive the filtering criteria.

## Nice-to-Haves

- **Ablation isolating the multi-scale component** (e.g., a variant without patch merging/expansion but retaining all other design choices) should be prominent in the main paper, not deferred to the appendix.
- **Weather evaluation in the main paper should include foundation model baselines** (Panda, Chronos-S-SFT) alongside the scratch-trained baselines, so the reader can directly assess the architectural contribution versus the shared benefit of chaotic-system pretraining.
- A dedicated **limitations section** discussing scope conditions (ODE vs PDE systems, variable count scalability, noisy observational data) would improve the paper.

## Removed Points

These points from the input review were removed with justification:

- **Speculation about appendix content** (Issue 3: "If the appendix does not include such ablations, then the paper's core architectural claim is unsubstantiated"): The parser strips appendix sections from all papers; they exist in the original submission. The substantive point about ablations not being in the main paper is retained and weakened to a Major weakness above. The speculative conditional about what the appendix might lack is removed per the hard rules.
- **Claim about "different patch embedding strategies"** being a confounding factor: The paper states its embedding approach is "adopted from recent work (Lai et al., 2025)" (Section 3.1), so this is the same as Panda. Removed as factually incorrect.
- **Criticism about MMD regularization being conceptually odd**: The reviewer's concern about applying MMD to finite-horizon trajectories is a reasonable technical question, but the paper uses a batch-based formulation that partially addresses it, and the justification is deferred to the appendix. This is a technical curiosity, not a verified weakness. Removed.
- **Generic criticisms** about the weather comparison being "fundamentally unfair": The paper discloses the asymmetry. The weakness is reframed above as a presentational issue rather than a fairness violation.
- **Several section-by-section notes** that are redundant with the major weaknesses above (e.g., rehashing the same weather concern multiple times).
- **"No asterisks are described for D_frac or D_step"**: The figure caption mentions asterisks are present in the figure; whether they appear for every subplot cannot be determined from the text description alone. Removed as unverifiable from the text.

## Novel Insights

The most incisive observation from the reviews concerns the disconnect between the paper's stated motivation (attractor preservation is paramount for chaotic systems) and its main empirical finding (improvement is on point-wise sMAPE, while attractor metrics are essentially tied with Panda). This is not a minor inconsistency — it cuts to whether the paper's central framing matches its actual contribution. The scaling analysis confound (multiple architectural changes not isolated) is a standard but well-articulated concern. The weather framing critique is sharp but primarily about presentation rather than scientific validity. None of these observations exceed what a careful reader of the paper would notice.

## Suggestions

1. **Reconcile the attractor-metric disconnect.** Either present evidence that ChaosNexus improves attractor statistics over Panda (on D_lyap, ME_LRW, or other metrics) in the main paper, or acknowledge that the improvement is primarily on point-wise accuracy and adjust the abstract/claims accordingly.

2. **Restructure the weather evaluation.** Include Panda and Chronos-S-SFT in the main Figure 3 alongside the scratch-trained baselines. The current figure is informative for demonstrating sample efficiency but not for assessing the architectural contribution.

3. **Add a clean ablation in the main paper** that holds axial attention, MoE, wavelet fingerprint, and MMD constant while varying only the multi-scale U-Net structure (patch merging/expansion). This would directly test the paper's core thesis.

4. **Specify the patch size D** and discuss its relationship to the temporal scales the model can capture.

## Score and Decision

<score>6</score>
<decision>Borderline Accept</decision>

**Reasoning**: The paper addresses a well-motivated problem with a sensible architecture, and the synthetic benchmark evaluation is large-scale and informative. The scaling analysis provides a practically useful finding. However, the evidence for the paper's strongest claims has notable gaps: (1) the claimed "notable improvements" in attractor statistics are not visible on the two attractor metrics shown in the main figure, where ChaosNexus and Panda are essentially tied; (2) the weather evaluation's headline comparison conflates pretraining with architecture, and the fair baselines are deferred to the appendix; (3) the multi-scale architecture's contribution is not isolated from other simultaneous design changes in the main paper. These weaknesses prevent the paper from reaching "Accept" (8) but do not warrant rejection because the core idea is well-motivated, the evaluation scale is substantial, and the scaling analysis is genuinely useful. The paper would benefit from the suggested revisions but has real contributions in its current form.