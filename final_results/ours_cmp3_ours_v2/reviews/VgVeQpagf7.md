## Summary

This paper proposes SPS and SPS+, algorithms for differentially private synthetic dataset generation by adapting the D3S dataset distillation framework to privatize intermediate activation statistics from a public pretrained model. SPS+ adds multistage clipping and grouped pseudo-classes to improve performance under high privacy. The core claim is that SPS+ is the first generation-based method to match DP-SGD accuracy on CIFAR-10/100 image classification, while also enabling downstream operations (ensembling, federated learning, continual learning) at zero additional privacy cost — advantages that DP-SGD cannot offer.

---

## Strengths

- **First generation-based method to match DP-SGD accuracy on image classification.** Prior DP synthetic data methods (Private Evolution at 89.1%, DP-KIP at 58.7% on CIFAR-10) fell well short. SPS+ closes this gap: at ε=1 with single WRN28-10, it achieves 95.1% vs DP-SGD's 94.8% on CIFAR-10 and 71.0% vs 70.3% on CIFAR-100 (Table 1). This is a meaningful advance for the private synthetic data community.

- **Genuine practical advantages from data-based privacy demonstrated experimentally.** Because SPS produces a DP dataset rather than a DP model, ensembling (5-model ensembles in Table 1), federated learning (Fig 5d-e, outperforming FedLAP-DP), and class-incremental continual learning (Fig 5c) incur zero additional privacy cost. These are validated experimentally and are advantages DP-SGD fundamentally cannot offer.

- **Well-motivated technical adaptations from D3S to the DP setting.** Removing the privately-trained teacher model, introducing class-conditional statistics with different random projection dimensionalities (D_G > D_C) to manage the C× noise multiplier on per-class statistics, and the noise-redistribution trick in §3.2.4 are non-trivial engineering choices grounded in analysis of how noise scales differently for global versus per-class statistics.

---

## Weaknesses

### Fatal
None.

### Major

- **The abstract's headline numbers conflate two orthogonal advantages.** The marquee result (96.2% on CIFAR-10, 76.6% on CIFAR-100 at ε=1) comes from SPS+ with **WRN34-10 ensembles of 5 models**, while the DP-SGD baseline is a single WRN28-10 model (Table 1). The fair single-model comparison (SPS+ WRN28-10 vs DP-SGD WRN28-10) shows 95.1% vs 94.8% on CIFAR-10 (within combined error bars) and 71.0% vs 70.3% on CIFAR-100. The ensemble advantage is a genuine benefit of the data-based approach, but presenting unqualified ensemble numbers as the headline — without clarifying the architecture and ensembling differences — conflates the privacy mechanism's contribution with orthogonal advantages. The abstract should present single-model, same-architecture results as the primary comparison and clearly qualify any ensemble/larger-model results.

- **The claim "SPS+ matches or exceeds DP-SGD in every setting" is not accurate.** On CIFAR-100 with single WRN28-10 models, SPS+ underperforms DP-SGD at ε=4 (76.2% vs 79.2%, a gap of 3 pp well outside error bars) and ε=8 (77.5% vs 81.8%, a gap of 4.3 pp) (Table 1). SPS+ is competitive mainly in the high-privacy regime (ε=1-2) where per-class noise reduction matters most, and DP-SGD pulls ahead at higher budgets. The paper should characterize this regime of advantage honestly.

### Minor

- **Dependence on a public pretrained model is under-discussed as a limitation.** SPS requires a high-quality model pretrained on relevant public data (here, 32×32 ImageNet). The CAMELYON17 experiment tests one binary classification task under domain shift, but there is no sensitivity analysis of how the method degrades with weaker or less relevant pretrained models. The limitations section (§6) mentions computational cost and class imbalance but does not address this dependency. While the paper acknowledges using a public pretrained model is "a common practice in the DP literature," the method's feasibility in scenarios where no such model exists (e.g., unusual medical imaging modalities, proprietary industrial data) should be scoped explicitly.

- **Grouped pseudo-classes (GPC), the most novel component of SPS+, lacks clear mechanistic explanation.** The paper states that generating P > C pseudo-classes via random grouping of real classes improves the noise rate from O(C/N) to O(C/(N·N_{c/p})), and that this "only works due to dynamics of optimizing the loss function, specifically the Σ inversion in the KL-divergence, and the eigenvalue clipping of Σ" (§4.2). However, it does not explain why random class groupings do not destroy class structure or how the optimization recovers meaningful class information. A concrete small-scale example or illustration would substantially clarify the mechanism.

- **The Rényi parameter α used for the reported ε values is not specified.** Theorem 4.1 states the RDP guarantee in terms of α, and the paper reports ε values, but never states what α range or conversion method (optimal α search) is used. This is standard reporting practice in DP papers.

- **Theorem 4.1 has a notational collision.** The theorem states ε = Mα/(2δ²), where the symbol δ appears to refer to the noise scale b₀ from §3.2.2 rather than the DP parameter δ. This makes the statement ambiguous as written.

### Trivial
None.

---

## Nice-to-Haves

- A clean theoretical or empirical analysis of how the signal-to-noise ratio trades off with the hyperparameters D_G, D_C, L, and |L_C| would further strengthen the method's motivation.
- A small-scale synthetic experiment demonstrating that grouped pseudo-classes recover correct class structure during optimization would improve confidence in the most novel technical component.
- A sensitivity study showing how SPS performance depends on pretrained model quality (weaker architecture, less relevant pretraining data) would help practitioners assess when the method is applicable.

---

## Removed Points
These points are flagged to be removed, treat them with caution:

- "Proof deferred to appendix" criticism: removed per rules (the parser strips appendix content from all papers; proofs exist in the original submission).
- "Formatting error in the clipping norm equation": removed per rules (formatting artifacts are parser errors, not author errors).
- "CAMELYON17 δ values should be checked for consistency": this is raised as a question rather than a confirmed weakness; the critic acknowledges the ε=8 vs ε=10 comparison is valid, and no actual inconsistency is demonstrated.
- "Table 1 is informative but hard to parse": removed as a formatting/presentation nitpick that does not threaten any claim.
- "Per-class noise scaling analysis is incomplete": moved to Nice-to-Haves, as it asks for additional analysis beyond what the paper already provides (the paper already motivates and addresses this challenge with D_G > D_C and GPC).
- Several generic section-by-section observations that are commentary rather than verified weaknesses.

---

## Novel Insights

None beyond the paper's own contributions — the reviews largely validate the paper's claimed contributions while identifying concrete presentation issues and overclaims that need correction.

---

## Suggestions

1. **Restructure the headline results.** Present single-model, same-architecture comparisons (SPS+ WRN28-10 vs DP-SGD WRN28-10) as the primary result in the abstract and introduction, with ensemble/larger-model results framed as demonstrations of the flexibility advantage.
2. **Correct the overclaim.** Replace "SPS+ matches or exceeds DP-SGD in every setting" with a precise characterization: SPS+ is most competitive in the high-privacy regime (ε=1-2), where it matches or modestly exceeds DP-SGD, while DP-SGD pulls ahead at higher ε on many-class datasets like CIFAR-100.
3. **Add a limitations discussion of the pretrained model dependency.** Explicitly state that the method requires a high-quality pretrained model on relevant public data and may not be applicable when such a model is unavailable.
4. **Explain grouped pseudo-classes more clearly.** Provide a concrete worked example (e.g., C=5, P=10) showing how random grouping and KL-divergence optimization recover class structure.
5. **Fix the notational collision in Theorem 4.1** and specify the α range or conversion method used for reporting ε values.

---

## Score and Decision

**Calibration anchors used** (all rounds):

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| `ckabXglfiT.md` — "Privacy as a Free Lunch" (DD+DP) | 4.75 | 1 | Lower quality: had a fatal flaw in DP analysis; this paper is technically sounder |
| `kzePnQWUvC.md` — "Exploring Data Distillation for Tabular Data" | 3.33 | 1 | Lower quality: poor presentation, weaker experimental validation; this paper is stronger |
| `C8niXBHjfO.md` — "Does Training with Synthetic Data Truly Protect Privacy?" | 6.00 | 1,2 | Similar quality: solid empirical work with limited novelty; this paper has more novelty but more presentation issues |
| `YEhQs8POIo.md` — "DP Synthetic Data via Foundation Model APIs 1: Images" | 6.25 | 2 | Very similar domain and quality: both generate DP synthetic images, both have overclaims and under-discussed limitations; this paper is comparable |
| `rTBL8OhdhH.md` — "Towards Lossless Dataset Distillation" | 7.00 | 1 | Higher quality: cleaner story, stronger experiments; this paper has more overclaims |
| `oZtt0pRnOl.md` — "Privacy-Preserving ICL with DP Few-Shot Generation" | 8.00 | 1,2 | Higher quality: cleaner evaluation and framing; this paper is not as polished |

**Round 1 bracket:** 5.5–6.5 (above papers with fatal flaws like "Privacy as a Free Lunch" at 4.75, below cleanly-presented papers like the lossless distillation and DP-ICL papers at 7.0+)

**Round 2 narrowing:** Compared against the closely related "DP Synthetic Data via Foundation Model APIs" (6.25) — similar domain, similar types of overclaims, similar strength of contribution. The paper under review has a somewhat stronger core result (matching DP-SGD accuracy rather than just FID) but also has more significant presentation overclaims. Settling at 6.0 reflects a solid borderline-to-accept paper with genuine contributions that need presentation corrections.

This is a solid paper with a genuine contribution: it is the first generation-based method to match DP-SGD accuracy on image classification benchmarks. The technical adaptations from D3S are well-motivated, and the downstream flexibility experiments convincingly demonstrate practical advantages of data-based privacy. However, the paper's presentation inflates its results in two ways that need correction: the abstract uses unqualified ensemble/larger-model numbers as its headline, and the claim that SPS+ "matches or exceeds DP-SGD in every setting" is factually inaccurate on CIFAR-100 at higher ε. These issues are correctable and do not undermine the core technical contribution.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>