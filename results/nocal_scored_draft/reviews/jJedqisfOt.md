Now let me synthesize the final review incorporating the favorability signals.

---

## Summary

This paper identifies two genuine limitations of spiking transformers — poor local attention modeling due to softmax removal and high memory overhead from storing attention matrices — and proposes LRF-SSA (adding local convolutions to SSA) and LRF-Dyn (a recurrent reformulation) to address them. Experiments on ImageNet classification and ADE20K segmentation show consistent accuracy improvements of 0.4–1.24% across three baseline architectures at negligible parameter cost.

## Strengths

- **Well-motivated problem identification with empirical evidence.** The paper diagnoses two genuine limitations of existing spiking transformers — the loss of local attention structure due to softmax removal and the memory overhead of attention matrices — and grounds this in empirical evidence (Figures 1–2 show SSA attention distributions are diffuse with entropy 0.5637 vs. VSA's 0.1777, and only 20.31% of SSA weight at short distances vs. 76.68% for VSA). This diagnostic analysis is the paper's strongest contribution.

- **Consistent empirical improvements across architectures and tasks.** Table 1 shows that substituting SSA with LRF-SSA improves ImageNet accuracy across three distinct baselines (Spikformer, QKFormer, SDT-V3) at multiple model scales, with gains of 0.44–1.24%, at negligible parameter overhead (<0.2M additional parameters). The pattern holds for LRF-Dyn as well (0.41–1.13%). The inclusion of ADE20K semantic segmentation (Table 2) further demonstrates generality.

- **The LRF-SSA method is simple and practical.** Adding two depthwise dilated convolutions to SSA to bias attention toward neighboring positions is a straightforward, low-cost modification that delivers consistent gains.

## Weaknesses

### Fatal

None.

### Major

- **Theorems 1 and 2 are overclaimed.** The paper presents Theorem 1 (VSA weights ∝ exp(-βΔ), SSA weights ∝ (α-βΔ)_+) and Theorem 2 (entropy ordering) as mathematical theorems, but these are assumed functional forms, not derivable properties of the attention mechanisms defined in Eqs. 5–6. There is no derivation connecting the actual attention computation to these forms. The entropy ordering claimed in Theorem 2 rests entirely on these unverified assumptions. The empirical observations in Figure 2 are legitimate, but labeling these as theorems is misleading and inflates the paper's theoretical contribution.

- **LRF-Dyn's claimed "neuronal dynamics" connection is rhetorical framing, not a technically accurate description.** The method in Eqs. 11–12 is standard causal linear attention using the associative property (q_n × Σ_{j<n} k_j^T v_j), reformulated as a recurrent state update. The paper asserts this "closely parallels the charge-fire-reset dynamics of spiking neurons" (line 146) and introduces a tridiagonal coupling matrix (Eq. 13) with biological terminology (membrane capacitance, dendrites), but no explicit derivation connects the KV accumulation to the recurrence, and the tridiagonal structure is not the LIF neuron dynamics defined in Section 3.1. The actual technique is a valid incremental engineering improvement — causal linear attention with local convolutions — but presenting it as a new paradigm of "neuronal-dynamics-based attention" substantially overclaims.

- **No actual measurements of memory, latency, or energy consumption.** The paper repeatedly motivates its contribution by citing deployment on resource-constrained devices (abstract, introduction, conclusion), yet every efficiency claim is supported only by asymptotic complexity notation (O(kd), O(d²)) and a single percentage (49.4% reduction in Section 6.2). There are no reported measurements of peak/average memory usage in MB/GB, inference latency, throughput, or energy. For a paper whose second core contribution is memory reduction, this is a significant evidential gap.

- **Missing comparison against linear-attention baselines.** LRF-Dyn's core mechanism (associative property + recurrent state accumulation) is the same technique that defines standard linear attention (Katharopoulos et al., 2020; Shen et al., 2021; Zhang et al., 2024b). The paper cites these in related work but includes none as experimental baselines. Since LRF-Dyn is effectively linear attention + local convolutions + spiking neurons, the experimental design cannot isolate how much of the improvement comes from the linear-attention reformulation itself versus the LRF convolutions versus the spiking components.

### Minor

- **The "Causal SSA" baseline in the ablation (Table 3) is undefined.** Its performance (74.30%) is substantially lower than LRF-SSA without LRF (77.86%), a gap larger than the improvement from adding LRF convolutions, making this baseline's setup unclear.

- **The Fourier transform in Eq. 15 is introduced without motivation.** The paper does not explain why a Fourier-domain convolution is needed to implement what is described as a first-order recurrence (Eq. 12).

### Trivial

- Table 2 (segmentation) has confusing formatting with duplicate model entries, and the citation "ResNet (Yu et al., 2022)" is non-standard (ResNet originates from He et al., 2016).

## Nice-to-Haves

- Drop or substantially soften the "neuronal dynamics" framing and present LRF-Dyn as causal linear attention with local convolutions. This would make the technical contribution clearer.
- Add a table reporting actual peak memory usage (in MB), latency, or MAC counts for each method in Table 1.
- Compare against at least one linear-attention baseline to isolate the effect of LRF convolutions and spiking components.
- Relabel Theorems 1 and 2 as empirical observations or propositions.

## Removed Points

- **Criticism about proofs being deferred to the appendix:** Removed — the parser strips appendix sections; they exist in the original submission.
- **Criticism about missing training hyperparameters:** Removed per hard rules (classified as a reproducibility nitpick).
- **Criticism that Eq. 8's global/local decomposition is "unusual":** Removed — the decomposition follows naturally from SSA's KV-aggregation form and the added LRF convolution.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

The paper's most productive revision path would be: (1) reframe LRF-Dyn honestly as causal linear attention with local convolutions (dropping the overstated neural-dynamics claims), (2) add actual memory/latency measurements, (3) include a linear-attention baseline, and (4) relabel Theorems 1–2 as empirical observations. These changes would bring the paper's framing in line with its actual technical contribution.

## Score and Decision

The paper has real empirical value — the diagnostic analysis of SSA's limitations and the consistent accuracy improvements across architectures are genuine contributions. However, the paper is undermined by four substantial issues that collectively make its current form unreliable: the theoretical apparatus is overclaimed (invalid theorems), the core method is rhetorically misrepresented (neuronal dynamics framing for standard linear-attention techniques), the claimed efficiency benefits are unmeasured (no actual memory/latency/energy numbers), and missing baselines prevent isolating contributions. These are not superficial presentation issues — they affect the paper's central claims and credibility. A substantially revised version addressing these concerns could be a solid incremental contribution.

**Score: 4.0**  

**Decision: Reject**

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>