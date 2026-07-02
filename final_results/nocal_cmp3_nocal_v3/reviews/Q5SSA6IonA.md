## Summary

This paper proposes Vision Filter (ViF), a vision backbone that extends Fourier Neural Operator (FNO) with two novel components: selective activation (gated fusion of time-domain local convolution and frequency-domain global convolution) and adaptive modulation (power-law weighting of frequency components). The authors identify two limitations of standard FNO for vision — bandwidth bottleneck (hard truncation of high-frequency modes) and over-smoothing (exponential decay of high-frequency content with depth) — and design FNF (Fourier Neural Filter) to address them. ViF achieves competitive results on ImageNet classification, COCO detection, and ADE20K segmentation, with a favorable throughput-accuracy tradeoff.

## Strengths

1. **Clear architectural motivation tied to specific problems.** The paper identifies two genuine limitations of FNO for vision (bandwidth bottleneck and over-smoothing, formalized in Propositions 1–2) and designs components selectively aimed at these: selective activation (Hadamard gating between local time-domain and frequency-domain branches) and adaptive modulation (power-law weighting to rebalance frequency components). This problem→design story is coherent and well-articulated in Section 3.

2. **Consistently competitive results across three major tasks.** Results in Tables 2–4 show real advantages: ViF-T reaches 83.8% on ImageNet-1K (29M/5.1G), outperforming VMamba-T (82.6%), Swin-T (81.3%), and NAT-T (83.2%). On COCO detection (Table 3), ViF-T achieves 47.7 AP^b vs. VMamba-T at 47.3. On ADE20K segmentation (Table 4), ViF-T reaches 48.7 SS mIoU vs. VMamba-T at 48.0. These advantages are small but consistent across model sizes and tasks, which is the paper's strongest evidence.

3. **Favorable throughput-accuracy tradeoff.** Figure 1 reports real throughput on an H100: ViF-B achieves ~800 img/s at 84.5% accuracy vs. VMamba-B at ~800 img/s at 83.5%. ViF-T runs ~1600 img/s at 83.8% vs. VMamba-T at ~1600 img/s at 82.5%. The accuracy-at-equal-throughput advantage is practically meaningful, leveraging well-optimized FFT kernels on GPU.

## Weaknesses

### Fatal

None.

### Major

1. **Claimed theoretical resolution of FNO limitations is not demonstrated.** Contribution (2) states: "We theoretically and empirically demonstrate that our proposed FNF resolves the inherent over-smoothing effect and bandwidth bottleneck of the original FNO." However, the paper never bridges the propositions to the proposed components with any formal analysis. Propositions 1–2 in Section 3.1 identify the problems (truncation error from fixed bandwidth; multiplicative decay of high-frequency content). Section 3.2 then describes FNF components, but the Remarks (3 and 5) are qualitative and informal — they assert that selective activation "enhances informative mid/high-frequency components" and that adaptive modulation "attenuates dominant low-frequency components" without any proof, bound, or even informal argument connecting these operations back to the error bounds in Propositions 1–2. No analysis is provided showing that the gated global convolution reduces the truncation error lower bound, or that adaptive modulation changes the contraction rate from Proposition 2. The paper presents a problem statement followed by an architectural description, not a theoretical demonstration. This claim should be downgraded to "empirically motivated design" unless genuine analysis is added. (Source: Contribution list line 47; Remarks 3 and 5 lines 143, 161.)

2. **Missing the single most informative ablation: vanilla FNO backbone.** The paper builds on the premise that FNO has limitations that FNF overcomes. Yet no experiment compares ViF against a version where FNF is replaced by a standard FNO operator (at comparable parameter count and FLOPs). The existing comparison against GFNet/GFNetV2 (Section 5.1) is not a substitute — those are ViT-style architectures with DFT replacing attention, not FNO-style integral kernel operators. Without this ablation, it is impossible to determine whether ViF's performance comes from the specific FNF innovations (selective activation + adaptive modulation) or from the overall architectural scaffolding (hierarchical stages, local convolutions, LPU, FFN modules, etc.) that could work equally well with a plain FNO kernel. Given that ablation differences in Table 5 are 0.3–0.7%, and overall margins over strong baselines are 0.4–1.3%, this missing comparison is consequential. (Source: Table 5 ablation study lines 333–342; Table 2 comparison lines 201–245.)

3. **Overclaimed novelty and factual inconsistency about computational complexity.** (a) The abstract claims "ViF demonstrates lower computational complexity than Transformer-based models." Table 2 shows ViF-T at 5.1G FLOPs vs. Swin-T at 4.5G and NAT-T at 4.3G — the opposite. ViF-B at 16.7G vs. Swin-B at 15.4G. This claim is contradicted by the paper's own data. (b) Contribution (1) claims "the first unified backbone that couples time-domain and frequency-domain analysis." Prior Fourier-based vision models (GFNet, AFNO) also operate in both domains (FFT→filter→IFFT→spatial MLP). The paper's specific gated parallel-branch design is a genuine architectural contribution, but the "first" framing is overstated. (c) Contribution (3) claims "state-of-the-art performance on three mainstream visual tasks," yet the limitations section (line 346) acknowledges "significant performance gap against ViT variants on downstream tasks." (Sources: Abstract line 9; Contribution list line 47; Table 2 lines 201–245; Limitations line 346.)

4. **No frequency-domain evidence despite frequency-domain framing.** The paper's entire narrative is about frequency-domain properties: bandwidth bottleneck, over-smoothing, high-frequency preservation. Selective activation is claimed to "enhance informative mid/high-frequency components while suppressing redundant low-frequency ones" (Remark 3). Adaptive modulation is said to "attenuate dominant low-frequency components while relatively enhancing weak high-frequency components" (Remark 5). Yet the paper provides zero frequency-domain analysis — no spectral visualization of feature maps, no effective bandwidth comparison between ViF and baselines, no Fourier power spectrum plots, no measurement of whether high-frequency content is actually better preserved. For a paper whose central motivation is about frequency-domain limitations, this omission is striking. (Sources: Remarks 3 and 5 lines 143, 161; ablation Table 5 lines 333–342.)

### Minor

5. **Key implementation details underspecified.** The core FNF module is defined via G(v), H(v), and T(v), described only as "linear transforms used for expansion or compression" (line 113). The main text does not specify whether these are 1×1 convolutions, linear projections, or channel mixing layers. Figure 2's elements ("Local Conv," "Global Conv," "Complex Transformer," "Adaptive Modulator") are described in the block diagram but not explicitly connected to the mathematical formulation. The model description in Table 1 provides only stage-level macro configuration (blocks, channels, heads). While implementation details are likely in the (parsed-away) appendix, the main text should be self-contained enough for a reader to understand the architecture without it.

6. **No variance reporting with small margins.** Results in Tables 2–5 are reported as single numbers without error bars, standard deviations, or confidence intervals. The performance margins are small (0.3–0.7% on ImageNet, 0.2–0.4 mAP on COCO), and ablation differences are 0.3–0.7%. While single-run reporting is standard practice in this subfield, the small margins make it difficult to assess reliability. Weakened because this is the field convention.

### Trivial

7. **Minor internal contradiction.** The Ethics Statement (Section 7) claims the work "does not raise concerns regarding... bias, fairness," while the Broader Impact (Section 6) states "potential risks include... possible perpetuation of biases present in training data." These are contradictory.

## Nice-to-Haves

- **Original FNO backbone ablation:** The single highest-value addition would be a controlled experiment comparing ViF against a version where FNF is replaced by a standard FNO operator at comparable parameters and FLOPs. This directly tests whether the claimed innovations contribute beyond the overall architecture.
- **Frequency-domain analysis:** Spectral density visualization of ViF feature maps vs. an FNO baseline, to empirically substantiate the paper's narrative about high-frequency preservation.
- **Ablation isolating input-dependence:** Compare (a) input-dependent kernel, (b) fixed learned kernel (FNO-style), (c) random kernel to test whether input-dependence per se is beneficial, beyond what the ablation study currently tests.
- **Reframing theoretical claims:** Replace the "theoretically demonstrates" framing with "empirically motivated by two identified limitations and validated through experiments."

## Removed Points

These points are flagged to be removed; treat them with caution.

- Critic's claim that "convolution does not create new frequency content outside the existing bandwidth" in the context of selective activation: this specific technical argument is debatable (convolution of bandlimited signals can produce content up to 2× the original bandwidth) and is not needed for the core weakness (the paper does not provide the claimed theoretical demonstration). Removed because the technical sub-argument may be incorrect.
- Critic's mentions of "the stripped appendix presumably contains more detail": removed per instructions — the appendix exists in the original submission but was stripped by the parser.
- Critic's claim that Contributions (2) statements about "theoretical proofs and derivations are included in Section 3" proves the paper lacks content: the reproducibility statement (line 358) says proofs are "included in Section 3" — the actual content of Section 3 is observable and correctly critiqued above; the reproducibility statement itself is not a weakness.
- Critic's claim that "Figure 2's description mentions 'Local Conv,' 'Global Conv,' and 'Complex Transformer,' but the text never connects the equations to these diagram elements explicitly": the Block Design paragraph (line 175) does describe the two-branch structure and maps it to Figure 3. The connection could be clearer but is present.
- Critic's "Section-by-Section Notes" section (abstract overstatement claim, Swin-T being from 2021, etc.): the abstract overstatement is already covered in Major weakness 3. The "Swin-T is from 2021" point is a normative claim about what baselines are acceptable, not a verifiable weakness of the paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add a direct FNO-baseline ablation experiment to empirically validate that the FNF-specific components (selective activation, adaptive modulation) improve over a vanilla FNO kernel at comparable scale.
2. Include frequency-domain visualizations (e.g., spectral power of feature maps at different layers for ViF vs. baselines) to substantiate the paper's central narrative about preserving high-frequency content.
3. Reframe Contribution (2) from "theoretically demonstrate" to "empirically motivated by and designed to address," and either provide genuine theoretical analysis or drop the theoretical claim.
4. Correct the "lower computational complexity" claim in the abstract, which is contradicted by Table 2.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>