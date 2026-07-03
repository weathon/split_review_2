## Summary

This paper proposes **Vision Filter (ViF)**, a backbone architecture that extends FNO by adding an input-dependent kernel through two mechanisms: (1) **selective activation** — gating between a frequency-domain global convolution branch (FNO-style) and a local convolution branch via a learned input-dependent Hadamard product, and (2) **adaptive modulation** — a power-law reweighting of frequency magnitudes. ViF is evaluated on ImageNet-1K classification, COCO object detection, and ADE20K semantic segmentation, achieving consistent improvements over Swin, ConvNeXt, NAT, and VMamba baselines at comparable or lower FLOPs.

---

## Strengths

1. **Consistent accuracy gains across all three model scales on ImageNet-1K (Table 2).** ViF-T (83.8%), ViF-S (84.5%), ViF-B (85.2%) each outperforms the corresponding VMamba (82.6%, 83.6%, 83.9%), Swin (81.3%, 83.0%, 83.5%), and NAT (83.2%, 83.0%, 84.3%) variants at comparable or lower FLOPs. The improvement is not a one-off spike at a single configuration.

2. **Parameter efficiency carries over to dense prediction tasks (Tables 3, 4).** In COCO Mask R-CNN 1×, ViF-S achieves 49.1 box AP with 64M params / 328G FLOPs vs. VMamba-S at 48.7 with 70M params / 349G FLOPs. In ADE20K segmentation, ViF-S (76M params / 1009G FLOPs) delivers comparable mIoU to VMamba-S (82M / 1028G). This shows the efficiency advantage is not limited to classification.

3. **Throughput reported under standardized conditions (Figure 1).** The paper measures throughput on H100 at batch 128, 224×224, directly comparing ViF against ConvNeXt, DeiT, Swin, VMamba, and LocalVMamba. ViF-T (~1600 img/s, 83.5% acc.) matches VMamba-T's throughput while surpassing its accuracy, providing practical evidence that the accuracy gains are not paid for by inference speed.

---

## Weaknesses

### Major

1. **Theoretical framing is substantially inflated (Propositions 1–2, Section 3.1).** Proposition 1 states that Fourier-series truncation creates an irreducible error—this is a restatement of the definition of truncation. Proposition 2 states that if spectral multipliers are bounded by ρ<1 on high frequencies, their product over L layers decays as ρ^L—this is a basic property of geometric sequences. Neither proposition says anything specific about *learned* FNO operators on vision data, nor do they provide any theoretical argument for why FNF's particular design resolves the identified issues. The paper claims it "theoretically and empirically demonstrates that our proposed FNF resolves the inherent over-smoothing effect and bandwidth bottleneck" (contribution 2), but the theory does not carry this weight. This over-framing is the paper's most significant weakness because it establishes expectations the rest of the paper cannot meet.

2. **Ablation does not test the core mechanistic claim (Table 5).** The paper's central novelty is an *input-dependent* kernel, yet the ablation removes entire components (LC-1, LC-2, AM, SA) without ever testing whether input-dependence specifically matters. A control that replaces the input-dependent gating signal G(v) with learned but input-independent parameters would isolate this. Similarly, there is no local-only baseline (removing the Global Conv / Fourier branch). The ablation differences are also small (0.2–0.7%), making clean attribution difficult.

3. **Experimental margins over the strongest baselines are thin, with no variance estimates.** On COCO 1×, ViF-T leads VMamba-T by 0.4 box AP; on COCO 3× MS, ViF-S leads VMamba-S by 0.2 box AP. On ADE20K single-scale, ViF-S (50.5) is *below* VMamba-S (50.6). Many margins fall in the 0.1–0.4 range. No confidence intervals, standard deviations, or statistical tests are reported anywhere. For a backbone claiming state-of-the-art status, margins this thin—especially without variance estimates—do not constitute strong evidence of superiority. The Limitations section (Section 6) itself concedes "marginal performance gains," which is consistent with this assessment.

### Minor

4. **Overstated claim in ADE20K results text (Section 5.3).** The text states: "ViF-S shows superior performance with 50.5 single-scale mIoU and 51.3 multi-scale mIoU, outperforming VMamba-S." On single-scale, ViF-S (50.5) is *below* VMamba-S (50.6). The multi-scale advantage is 0.1 (51.3 vs 51.2). While the parameter efficiency claim (76M vs 82M) is valid, the accuracy claim of "outperforming" is not correct for single-scale and is within noise for multi-scale.

5. **Discrepancy between ablation table and text (Table 5 vs. line 342).** Table 5 shows "w/o SA" achieves 83.1% top-1, but the text says "accuracy dropping to 83.3%." One of these is incorrect.

6. **"Frequency Normalization (FN)" appears in the architecture diagram (Fig. 3) but is never defined or described in the text.** The text also leaves several details unspecified: the kernel sizes/strides of the local convolutions in the FNF module, initialization and constraints for the learnable parameters α and β in adaptive modulation (Eq. 12), and whether there are numerical stability safeguards when α<0 and ‖z‖≈0 (since ‖z‖^α could diverge).

7. **GFNet comparison at different resolutions (Table 2).** ViF is compared at 224² against GFNetV2 at 384² (e.g., "ViF-T surpasses GFNetV2-B by 1.7%"). GFNetV2-B uses 23.3G FLOPs vs. ViF-T's 5.1G. The data is reported but the text does not note this resolution/compute asymmetry, making the comparison less informative than it appears.

8. **ViF-B is larger than VMamba-B in COCO (Table 3, Mask R-CNN 1×).** ViF-B uses 120M params / 517G FLOPs vs. VMamba-B's 108M / 485G, weakening efficiency claims at this scale.

### Trivial

- Text says "accuracy dropping to 83.3%" for w/o SA (line 342); Table 5 shows 83.1%.
- "Frequency Normalization (FN)" in Figure 3 is never defined in the main paper text.

---

## Nice-to-Haves

- An ablation replacing the input-dependent gating G(v) with input-independent learned parameters to isolate whether input-dependence specifically drives performance.
- A local-only baseline (removing the Global Conv / Fourier branch entirely) to measure the Fourier branch's contribution alone.
- Frequency-domain visualizations or spectral analysis demonstrating that ViF preserves more high-frequency information than FNO — a natural experiment given the paper's central narrative.
- Throughput comparison with GFNet/GFNetV2 in Figure 1, as these are the most directly related Fourier-based competitors.

---

## Removed Points

*These points were raised in the input reviews but are removed from the main assessment for the following reasons:*

- **"FNF is just FNO with a standard gating mechanism; novelty is overstated."** — The paper transparently describes the mechanism (Eq. 4–6, Fig. 2). Combining FFT-based global convolution with local-convolution gating is a novel architectural design even if both component types are individually known. Removed as a matter of opinion rather than a verifiable flaw.
- **"Limitations section contradicts the paper's narrative."** — The Limitations section is actually a positive feature demonstrating honesty. The paper's SOTA claims are scoped to the baselines it compares against; acknowledging limitations is not a contradiction. Removed.
- **"Missing baselines (ConvNeXt V2, MaxViT, etc.)."** — The baseline set already includes 12+ architectures across 4 categories (CNN, Transformer, Mamba, Fourier). Requesting more is generic scope creep. Removed.
- **"No comparison with models that outperform ViF."** — The Limitations section references Fan et al. (2024) and Shi (2024) but does not name specific models. This is imprecise but not a critical flaw. Removed.
- **Strength Finder's "principled theoretical diagnosis"** — As noted in Weakness #1, the propositions are too thin to merit this characterization. Overclaimed as a strength.
- **"Claim about being 'first unified backbone that couples time-domain and frequency-domain analysis' overlooks GFNet/AFNO."** — GFNet and AFNO operate purely in the frequency domain without an explicit time-domain branch, so the claim is accurate. Removed.

---

## Novel Insights

None beyond the paper's own contributions. The reviews largely recapitulate the paper's stated results and limitations without uncovering unstated implications or connections to broader trends.

---

## Suggestions

1. **Reframe the theoretical section** (Propositions 1–2) as intuitive motivation rather than formal proof. Add an ablation that tests input-dependent vs. fixed (learned, input-independent) gating to substantiate the claimed mechanism.
2. **Correct the ADE20K single-scale claim** for ViF-S vs. VMamba-S and fix the text/table discrepancy for the w/o SA ablation accuracy (83.1 vs. 83.3).
3. **Report confidence intervals or standard deviations** for at least the key ImageNet and COCO comparisons, or run multiple seeds for the ablation study.
4. **Add frequency-domain visualizations** (e.g., power spectra of feature maps) that empirically demonstrate ViF preserves more high-frequency information than FNO — directly supporting the paper's central narrative.
5. **Define all components** that appear in the architecture diagram, especially "Frequency Normalization (FN)" and specify local convolution kernel sizes, numerical stability for adaptive modulation (Eq. 12), and block-diagonal structure details.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Borderline</decision>