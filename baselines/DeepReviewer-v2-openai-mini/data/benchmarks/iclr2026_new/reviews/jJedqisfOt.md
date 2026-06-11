## Summary
# Final Review Report

## Summary

This paper addresses two limitations of Spiking Self-Attention (SSA) in Spiking Transformer architectures: (1) a performance gap relative to ANN Transformers due to insufficient local modeling, and (2) high inference memory overhead from storing large attention matrices. The authors propose LRF-Dyn, a two-step approach. First, LRF-SSA augments SSA with depth-wise dilated convolutions to inject local receptive field bias. Second, LRF-Dyn reformulates the resulting attention computation through neuronal charge-fire-reset dynamics, eliminating the need to store explicit attention matrices and reducing memory to O(kd). Experiments on ImageNet-1k classification and ADE20K segmentation across three Spiking Transformer backbones (Spikformer, QKFormer, SDT-V3) show consistent accuracy improvements (0.41–1.24%) with LRF-SSA and comparable or slightly lower gains with LRF-Dyn, alongside claimed memory reductions. The paper's core conceptual contribution — bridging neuronal dynamics with attention to eliminate explicit attention storage — is interesting and timely for the neuromorphic computing community. However, the manuscript has significant gaps in mathematical clarity, experimental rigor (no statistical significance, missing variance), and claim substantiation (energy efficiency unmeasured, memory reduction unbroken).

## Strengths
**S1 — Clear problem identification and motivation.** The paper clearly identifies two concrete deficiencies in existing Spiking Transformers: lack of locality bias due to softmax removal (supported by histogram analysis in Fig. 2) and memory overhead from storing N×N or d×d attention matrices. The problem framing is accessible, well-illustrated, and practically relevant for edge deployment scenarios.

**S2 — Novel conceptual connection between attention and neuronal dynamics.** The core idea of reformulating attention aggregation as neuronal charge–fire–reset dynamics is conceptually interesting. Approximating the cumulative KV outer product accumulation (Σ kᵀv) as a membrane potential-like state variable and casting the local receptive field as dendritic input provides a fresh perspective on biologically plausible attention that goes beyond incremental improvements over SSA.

**S3 — Comprehensive architecture coverage in experiments.** The paper evaluates LRF-SSA and LRF-Dyn across three distinct Spiking Transformer backbones (Spikformer, QKFormer, SDT-V3) at multiple parameter scales, demonstrating general applicability of the proposed modules. The inclusion of both classification (ImageNet-1k) and segmentation (ADE20K) tasks strengthens the empirical scope.

**S4 — Clean modular design for integration.** Both LRF-SSA and LRF-Dyn are designed as drop-in replacements for the SSA module, requiring minimal modifications to existing architectures (as stated in Section 5.3). This modularity lowers the barrier for adoption by other researchers in the SNN community.

## Weaknesses
### W1 — Missing statistical rigor in all experimental results (Critical)

**Location:** Page 6—8, Section 6.1 (Image Classification & Semantic Segmentation)

No variance or significance measures are reported for any experiment. Accuracy improvements range from 0.41% to 1.24% — within typical single-run noise for ImageNet training. Without multi-seed standard deviations or confidence intervals, readers cannot distinguish genuine improvement from random seed variation. This is especially concerning for near-tie comparisons: Spikformer-8-768 baseline (74.81%) vs LRF-Dyn (75.58%, +0.77%) could be within one standard deviation. The same issue applies to the segmentation results (Table 2).

**Required fix (Must):** Report mean ± std over ≥3 seeds for all key results. At minimum, provide 3-run statistics for the smallest model (SDT-V3-S, 5.24M) and the primary Spikformer comparison. Add paired significance tests against baselines.

---

### W2 — Core theoretical claim insufficiently established (Major)

**Location:** Page 4—5, Section 5 (LRF-Dyn method)

The paper's central claim is that LRF-Dyn "establishes an approximate correspondence between self-attention aggregation and the charge–fire–reset dynamics of spiking neurons." However, three critical gaps prevent verification of this claim:

(a) **Missing mapping between attention and dynamics (Page 5, Eqs. 11—12):** The transition from Eq. (11) (causal reformulation of LRF-SSA, which is a well-known linear attention trick) to Eq. (12) (neuronal dynamics with decay factor A and membrane capacitance Γ) is not derived. The term Token_n[t] is not linked to any specific Q/K/V variable. It is unclear whether the neuronal dynamics actually compute an approximation to attention or an entirely different function that happens to have low memory.

(b) **Dimension inconsistency in Eq. (13) (Page 5):** The decay factor A is defined as an ℝ^d vector but expressed as the product of a length-n vector and an n×n matrix (n=8 dendrites). For a feature dimension d=512, the mapping from 8 dendrites to 512 feature dimensions is unexplained. The notation C ∈ ℝ is also inconsistent with C being a length-n vector.

(c) **Undefined symbols in overall architecture (Page 6, Eq. 15):** Fourier transforms F and convolution kernel K(t) = Γ C Σ_{m=1}^{n-m} A are introduced without derivation from preceding equations. The notation α_k and H_{pk(t)} are undefined. This discontinuity makes Section 5.3 nearly incomprehensible as a standalone description.

**Required fix (Must):** Clarify the mapping between attention variables (q_n, k_j, v_j) and the dynamic variables (X_n, A, Γ, Token_n). Specify how the dendrite number (n=8) relates to feature dimension d. Derive or remove the Fourier formulation in Eq. (15). Without such clarification, the paper's central theoretical contribution cannot be evaluated.

---

### W3 — Memory reduction claim lacks breakdown and absolute quantification (Major)

**Location:** Page 8, Section 6.2 ("Enhanced Local Modeling Ability with Lower Memory Requirements")

The paper claims "reducing memory usage by 49.4%" (Fig. 5b) without specifying: (a) what memory is measured (total model, activation, or attention-specific), (b) the absolute memory values in MB, (c) the contribution breakdown between the causal reformulation (standard trick) and the neuronal-dynamic approximation (novel component). If most of the 49.4% comes from the causal reformulation (which is equivalent to existing linear attention methods applied to SNNs), then the novelty contribution of the neuronal dynamics to memory reduction is unclear.

The complexity notation in Table 1 is also inconsistent: Spikformer baseline is listed as O(d²), LRF-SSA as O(d²), and LRF-Dyn as O(kd). But LRF-SSA with the causal reformulation should also have lower memory than the baseline SSA — why is it still listed as O(d²)? This needs clarification.

**Required fix (Must):** Provide a memory breakdown table with absolute MB values, separating baseline SSA memory, causal-reformulation memory (without neuronal dynamics), and LRF-Dyn memory. Clarify whether LRF-SSA uses the causal reformulation or the original N×N attention.

---

### W4 — Parameter count inconsistency between classification and segmentation experiments (Major)

**Location:** Page 6—7, Tables 1 and 2

In Table 1 (ImageNet), SDT-V3-S has 5.11M params and SDT-V3-S + LRF-SSA has 5.24M params (+0.13M), consistent with the "fewer than 0.2M additional parameters" claim. However, in Table 2 (segmentation), SDT-V3-S baseline is 5.1M while SDT-V3 + LRF-SSA is 10.0M — a 4.9M increase, roughly 38× larger than expected. The paper does not explain this discrepancy. If the segmentation model uses a different configuration (e.g., larger convolutions), this must be stated. The comparison with SDT-V3 + LRF-Dyn at 5.24M suggests the 10.0M figure for LRF-SSA may contain an error.

**Required fix (Must):** Reconcile the parameter counts. Either correct the 10.0M figure or explain why the segmentation variant of LRF-SSA requires 4.9M extra parameters while the classification variant needs only 0.13M.

---

### W5 — Related Work is a shallow list, missing explicit positioning (Moderate)

**Location:** Page 2, Section 2 (Related Work)

The Related Work section reads as two disconnected mini-surveys without connecting to the paper's own contributions. The Vision Transformer paragraph describes linear attention methods but does not explain how LRF-Dyn differs from or improves upon them. The Spiking Transformer paragraph lists models (Spikformer, QKFormer, SDT-V3) but does not state which specific limitations of each are addressed by LRF-SSA/LRF-Dyn. Without this positioning, the novelty boundary is unclear.

**Required fix (Must):** Restructure around explicit comparison axes (e.g., softmax-free attention locality, memory-efficient attention for SNNs, bio-inspired dynamics for attention). For each listed method, state one concrete limitation that this paper addresses.

---

### W6 — Ablation conflates factors and misses causal separation (Moderate)

**Location:** Page 8, Section 6.3 (Ablation Experiment)

The ablation Table 3 varies LRF kernel count but does not separately measure the effect of the causal reformulation vs. the LRF convolutions. The "Causal SSA" baseline (74.30%) is unexplained: it is ~3.5% lower than LRF-Dyn w/o LRF (77.78%), yet LRF-Dyn is supposed to approximate LRF-SSA. The large gap suggests the causal reformulation and the LRF-Dyn neuronal dynamics are not equivalent. A 2×2 design (LRF on/off × Causal reform on/off) would cleanly separate the contributions.

**Required fix (Nice-to-have):** Add an ablation row "SSA + Causal reformulation (no LRF)" to isolate the effect of the memory-reduction trick alone. Measure the difference between SSA + causal reformulation and LRF-Dyn (which adds dendritic dynamics and LRF convolutions) to quantify what each component contributes.

---

### W7 — No energy efficiency measurements despite strong deployment claims (Moderate)

**Location:** Page 0, Abstract; Page 1, Introduction; Page 9, Conclusion

The abstract states the method "establish[es] it as a key unit for achieving energy-efficient Spiking Transformers," the introduction frames the work around "low-power computing" and "deployment on resource-constrained devices," and the conclusion claims "practical potential for deploying high-performance SNN models in resource-constrained edge environments." However, no actual energy measurements, hardware benchmarks, or latency results are reported. Memory reduction does not guarantee energy efficiency (the method adds two depthwise convolutions per head, which increase per-step compute). Without energy quantification, these deployment claims are speculative.

**Required fix (Must):** Either (a) provide measured energy consumption (e.g., using a hardware energy model or on-device measurement), or (b) replace all energy-efficiency claims with bounded statements about memory reduction. The abstract's "energy-efficient" should be replaced with "memory-efficient" unless energy data is provided.

---

### W8 — Causal analysis of locality loss conflates binary spike quantization with softmax removal (Minor)

**Location:** Page 3, Section 4.1 (Limited Local Modeling Capability)

The paper attributes SSA's uniform attention distribution solely to softmax removal, but SSA also applies LIF neurons to Q, K, V activations (Eq. 4: Q = SN{BN(Conv_Q(X))}), producing binary {0,1} spike trains. The dot product of binary vectors produces a fundamentally different distribution than the dot product of real-valued vectors, regardless of softmax. The paper's analysis does not disentangle these two factors. The Manhattan distance histogram (Fig. 2) compares VSA (real-valued Q,K with softmax) to SSA (binary Q,K without softmax), conflating two differences.

**Required fix (Nice-to-have):** Add an ablation comparing entropy for: (1) real-valued Q,K without softmax, (2) binary Q,K with softmax, (3) binary Q,K without softmax. This would isolate the contribution of each factor to the locality loss.

## Score
**Final Score: 5.5/10**

### Scoring rationale

The score prioritizes research value, novelty strength, and validity — weighted conservatively due to the identified weaknesses.

**Research value (6/10):** The conceptual connection between neuronal dynamics and attention is a worthwhile direction that could inspire future work. However, the current manuscript does not fully substantiate this connection (W2), and the empirical validation lacks the statistical rigor needed to demonstrate reliable gains (W1). The practical value for edge deployment is claimed but not measured (W7).

**Novelty (6/10):** The idea of casting attention as neuronal charge-fire-reset dynamics has conceptual novelty. However, two caveats apply: (a) the causal reformulation (Eq. 11) is a direct application of existing linear attention tricks to SNNs — the novelty lies specifically in the dendritic dynamics formulation (Eqs. 12-13), which is currently under-specified; (b) the LRF convolutional bias (dilated depthwise convs) is a straightforward engineering addition. Given that external literature verification was unavailable (Retrieval-Disabled Mode), the definitive novelty assessment is deferred. A cautious mid-range score reflects the fact that the core idea is interesting but its novelty boundary relative to softmax-free attention and prior SNN-dynamic works cannot be fully verified here.

**Validity/Soundness (5/10):** This is the weakest dimension. The absence of standard deviation and significance testing (W1), the parameter count inconsistency in Table 2 (W4), the circular notation in LIF equations (minor) and the ambiguous method formulation (W2) collectively reduce confidence in the core conclusions. The ablation design does not isolate the key components (W6), and the memory reduction claim lacks breakdown (W3).

**Presentation (5/10):** The paper is well-structured and the problem motivation is clear. However, the Related Work lacks positioning (W5), several equations have ambiguous notation (Eqs. 7, 8, 11-13), and the energy-efficiency claims in Abstract and Conclusion overstate what is actually measured (W7).

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: SSA lacks locality + high memory]
    |
    v
[Analysis: Sec 4 — Manhattan distance histograms,
 entropy comparison VSA vs SSA]
    |
    v
[LRF-SSA (Sec 5.1): SSA + dilated depthwise convs
 to restore locality bias]
    |
    v
[LRF-Dyn (Sec 5.2-5.3): Reformulate attention as
 neuronal charge-fire-reset dynamics (Eqs 11-13)]
    |
    v
[Experiments (Sec 6): ImageNet-1k + ADE20K
 across 3 backbones]
    |
    v
[Claimed gains: +0.4–1.24% accuracy, up to 49.4%
 memory reduction]
    |
    v
[GAPS: No variance (W1), ambiguous dynamics mapping
 (W2), unmeasured energy (W7), inconsistent params (W4)]
```

### Top Defect Board

| Rank | Defect | Severity | Validity Risk | Fixability |
|------|--------|----------|---------------|------------|
| 1 | Missing statistical significance (W1) | Critical | High — cannot assess if gains are real | Fixable — add multi-seed runs |
| 2 | Core dynamics mapping unclear (W2) | Major | High — central claim unverifiable | Fixable — clarify derivation |
| 3 | Memory reduction unbroken (W3) | Major | Medium — overclaim risk | Fixable — add breakdown table |
| 4 | Parameter count inconsistency (W4) | Major | Medium — possible error | Fixable — correct numbers |
| 5 | No energy measurement (W7) | Major | Medium — claim-evidence gap | Must retract claims or add data |

### Verdict

The paper presents a genuinely interesting conceptual direction — linking neuronal dynamics to attention computation in order to eliminate explicit attention matrices. This idea could become a solid contribution if the method formulation is significantly clarified, the empirical evaluation is hardened with proper statistics, and the scope of claims is aligned with what is actually measured. In its current form, the manuscript is not yet ready for publication. The required minimal revision includes: (1) adding multi-seed variance and significance tests, (2) clarifying the mathematical mapping between attention and neuronal dynamics with consistent notation, (3) providing a detailed memory breakdown with absolute numbers, and (4) correcting the parameter count inconsistency. A major revision with these fixes could elevate the score to approximately 7.0/10.