## Summary
# Final Review Report

## Summary

This paper proposes Quantized Zeroth-order Optimization (QZO), a method that combines zeroth-order optimization (ZO) with model quantization to minimize GPU memory during LLM fine-tuning. The core technical idea is to perturb the continuous quantization scale (rather than the discrete quantized weights) for gradient estimation via a modified SPSA estimator (Q-SPSA), and to stabilize training with a Directional Derivative Clipping (DDC) mechanism. QZO eliminates gradient and optimizer state memory while compressing weights to 4-bit or 2-bit precision, achieving up to ~18x memory reduction compared to 16-bit AdamW fine-tuning. The method is validated on OPT-6.7B, Llama-2-7B, Llama-3.1-8B, and Llama-2-13B across five NLP benchmarks. Results show QZO significantly outperforms zero-shot baselines and achieves broadly competitive results with MeZO (ZO on 16-bit models) while using ~3x less memory. Under 2-bit extreme quantization, QZO also shows meaningful gains over the quantized zero-shot baseline. The paper includes both theoretical variance analysis for DDC and ablation studies demonstrating its stabilizing effect.

**Core contributions:**
- **C1:** A novel integration of ZO with post-training quantization (PTQ) that perturbs only the continuous quantization scale, avoiding de-quantization/re-quantization overhead.
- **C2:** Directional Derivative Clipping (DDC) with theoretical variance analysis for stabilizing ZO training on quantized models.
- **C3:** Empirical demonstration across multiple LLM families, quantization methods (GPTQ 4-bit, AQLM 2-bit), and five NLP tasks, showing practical memory savings with competitive performance.

## Strengths
1. **Technically clean and practical contribution.** The core idea of perturbing quantization scales rather than the discrete weights is conceptually elegant and directly addresses the precision-gap challenge that prevents naive ZO+quantization combination. The method is orthogonal to both scalar-based and codebook-based PTQ methods, enhancing its practical applicability.

2. **Significant memory savings.** QZO demonstrates a real and practically important reduction in GPU memory consumption. The 18x reduction versus 16-bit AdamW fine-tuning (enabling Llama-2-13B fine-tuning on a single 24GB GPU) is a tangible benefit for resource-constrained researchers. The elimination of both gradients and optimizer states while compressing weights to 4-bit represents a genuinely extreme memory-efficiency regime.

3. **Well-designed ablation for DDC.** The clipping threshold sensitivity analysis (Figure 3) provides practical guidance for choosing C and clearly demonstrates the training collapse that occurs without DDC. The empirical stabilization evidence is convincing and directly supports the practical value of DDC.

4. **Broad evaluation across model families and quantization methods.** Testing on OPT, Llama-2, and Llama-3.1 with both GPTQ (4-bit) and AQLM (2-bit) shows the method is not tied to a specific architecture or quantization scheme. Including 2-bit extreme quantization results is a useful stress test.

5. **Computation efficiency demonstration.** Table 2 shows QZO uses approximately 1% of the trainable parameters and substantially fewer FLOPs compared to MeZO, quantifying the computational advantage beyond just memory.

6. **Reproducibility considerations.** The paper provides a public GitHub repository and references to the specific quantization implementations (GPTQModel, AQLM) and the MeZO codebase, which supports reproducibility.

## Weaknesses
### W1. Theoretical analysis of DDC has gaps (Major)

The claim in Theorem 1 that the DDC-clipped gradient estimate is unbiased requires more careful justification. The standard SPSA estimator already has an $O(\epsilon^2)$ bias due to the finite-difference approximation. Adding clipping introduces further truncation bias unless $C \to \infty$ (which defeats the purpose). The variance derivation in Eq. 8 implicitly assumes the unclipped SPSA estimate is unbiased when substituting $\mathbb{E}[||\hat{\nabla}||]^2$ with $(\nabla_\Delta \mathcal{L})^2$, but this is not guaranteed. These gaps should be explicitly addressed: either clarify the asymptotic bias order or revise the claim to state that DDC reduces the second moment (rather than variance) under the stated inequality.

**Impact:** Reduces confidence in the theoretical justification of DDC. The empirical evidence for DDC (Section 4.3) remains valid, but the paper's theoretical contribution needs tightening.

**Recommendation:** Revise Theorem 1 to state bias is bounded by $O(\epsilon^2)$, matching the base SPSA estimator. Correct Eq. 8 to avoid the unjustified substitution, and instead directly argue that $\mathbb{E}[||\hat{\nabla}'||^2] \leq \mathbb{E}[||\hat{\nabla}||^2]$ is sufficient for the practical claim that DDC does not increase the gradient magnitude.

### W2. Baseline comparison is asymmetrical and incomplete (Major)

The paper's central empirical claim is that QZO achieves performance "on par with MeZO." However, several issues weaken this comparison:

**(a) SGD as upper-bound:** The fine-tuning baseline uses SGD rather than AdamW (footnote 2), due to compute constraints. This is a significant limitation because AdamW is the standard optimizer for LLM fine-tuning and uses 2x the memory of SGD (due to momentum buffers). The memory reduction factor of 18x is computed against the AdamW memory (Figure 1), but the performance upper-bound is only measured against SGD. This creates an apples-to-oranges situation where the memory claim and the performance claim use different baselines.

**(b) No comparison with ZO-signSGD-based methods:** The Related Work section states that prior work (Feng et al., 2024; Zhou et al., 2025; Bar & Giryes, 2025) addresses ZO fine-tuning of quantized models, but no experimental comparison is provided. Without this, the claimed advantage ("inherently more efficient and flexible") is unverified.

**(c) Manipulation of three variables simultaneously:** QZO vs MeZO comparisons conflate weight precision (4-bit vs 16-bit), parameter count (1% vs 100%), and optimization details (scale-only vs full-weight). A matched-parameter ablation is needed to isolate individual effects.

**Recommendation:** Add AdamW fine-tuning results for at least one model (e.g., OPT-6.7B) as a stronger upper-bound. Include a comparison with at least one ZO-signSGD-based method under matched conditions. Add an ablation where QZO fine-tunes both the scales and a matched subset of weights.

### W3. 2-bit results lack meaningful baselines (Major)

Table 3 compares QZO at 2-bit only against Zero-Shot-Q (a 2-bit quantized model without fine-tuning). Missing baselines include: (i) the 16-bit zero-shot model (to quantify quantization damage), (ii) MeZO on the 16-bit model (to contextualize QZO's recovery), and (iii) QZO at 4-bit on the same model (to isolate the effect of 2-bit vs 4-bit). Without these, the reader cannot assess whether the performance improvement is practically meaningful or how much is sacrificed for the extreme memory savings.

**Recommendation:** Add 16-bit zero-shot and MeZO results for Llama-2-13B to Table 3, or explicitly cite published results for these baselines. Include a column showing the 4-bit QZO performance for the same model (even if the 4-bit version is not directly comparable due to different quantization methods).

### W4. Introduction overclaims in comparative framing (Moderate)

The introduction states QZO "significantly outperforms" zero-shot models while "performing on par with MeZO." However, Table 1 shows cases where QZO substantially underperforms MeZO (e.g., CB: 69.6 vs 91.1 for Llama-3-8B, a 21.5-point gap). The "on par" characterization is too optimistic. A more nuanced framing that acknowledges task-dependent gaps would improve credibility.

**Recommendation:** Replace "on par" with more precise language that explicitly notes the range of performance gaps and acknowledges the variability across tasks.

### W5. Conclusion introduces unsupported new information (Moderate)

The conclusion paragraph about Stable Diffusion 3.5 Large introduces a significant new experiment (text-to-image generation) that is not discussed with quantitative metrics in the main text. The claim "visually closer to the ground truth" is subjective without FID or CLIP scores reported in the main body. Conclusions should consolidate validated findings, not announce new experimental domains.

**Recommendation:** Either (a) include quantitative metrics (FID/CLIP) in the main results section, (b) move this discussion to future work, or (c) provide at least one summary metric in the conclusion with a clear reference to Appendix F.

### W6. Missing statistical significance and variance reporting (Minor)

All results in Tables 1 and 3 are reported as single-point estimates without variance, confidence intervals, or significance tests. Given that ZO methods are known to have high gradient variance, and the reported differences between QZO and baselines are sometimes small (~1-3 points), the lack of multi-seed reporting makes it impossible to assess whether observed differences are statistically reliable.

**Recommendation:** Report mean and standard deviation over at least 3 random seeds for the main results. For the headline comparisons, add a paired significance test against MeZO.

### W7. Notation inconsistency between Method and Algorithm (Minor)

The quantized weights are denoted $\bar{\theta}$ in Definition 3.3 and Eq. 5, but switch to $\tilde{\theta}$ in Algorithm 1 without explanation. This can cause confusion for readers implementing the method from the text.

**Recommendation:** Harmonize notation: use $\bar{\theta}$ consistently throughout.

### W8. Related Work section is catalog-style rather than comparative (Minor)

The Related Work subsection on LLM Quantization presents a sequential list of methods (Dettmers et al., Frantar et al., Lin et al., etc.) without comparing their assumptions or limitations. This makes it harder for readers to understand where QZO fits in the landscape.

**Recommendation:** Reorganize by comparison axes (e.g., bit-width, quantization granularity, fine-tuning compatibility) rather than chronologically. Add explicit sentences stating how QZO differs from each family.

### W9. Activation memory oversimplification (Minor)

The paper states activations are "mostly affected by the size of mini-batch" — this is an oversimplification. In transformers, activation memory scales with sequence length, hidden dimension, and number of layers, and can be reduced via gradient checkpointing. A more accurate characterization would strengthen technical rigor.

**Recommendation:** Revise to: "Activation memory is primarily determined by batch size, sequence length, and model depth; techniques like gradient checkpointing can further reduce it."

---

**ASCII Diagram — Paper Structure & Evidence Map**

```text
[Problem: LLM fine-tuning memory bottleneck]
    |
    v
[Idea: Combine ZO (eliminate gradients/states) + Quantization (compress weights)]
    |
    v
[Challenge: ZO gradients are continuous; quantized weights are discrete]
    |
    v
[Q-SPSA: Perturb quantization scale Δ instead of discrete weights θ̄]
    |                                   [DDC: Clip directional derivative d to [-C, C]]
    |                                   [Theorem: 2nd moment does not increase]
    v
[Empirical Evaluation]
    ├── 4-bit (GPTQ): OPT-6.7B, Llama-2/3-7/8B  →  5 datasets  →  competitive with MeZO
    ├── 2-bit (AQLM): Llama-2-13B  →  meaningful gains over Zero-Shot-Q
    └── Ablation: DDC prevents NaN, C≥75 yields stable training
    |
[Gap: No comparison vs ZO-signSGD baselines; SGD upper-bound; single-seed results]
```

**ASCII Diagram — Revision Strategy Roadmap**

```text
[Priority 1: Theoretical fix]
  Theorem 1 bias claim → revise to O(ε²) bias bound
  Eq. 8 derivation → replace unjustified substitution with 2nd-moment argument
  → Expected impact: Sound theoretical foundation for DDC

[Priority 2: Baseline strengthening]
  Add AdamW fine-tuning for ≥1 model
  Add ZO-signSGD comparison or justify omission
  → Expected impact: Fairer and more complete empirical evaluation

[Priority 3: 2-bit table expansion]
  Add 16-bit zero-shot and MeZO baselines
  → Expected impact: Contextualize extreme quantization trade-offs

[Priority 4: Statistical rigor]
  Multi-seed variance reporting + significance tests
  → Expected impact: Confidence in result reliability

[Priority 5: Writing polish]
  Fix "on par" overclaim, notation inconsistency, activation description
  Move/buffer Stable Diffusion conclusion
  → Expected impact: Improved credibility and narrative clarity
```

## Score
**Final Score: 6/10**

**Scoring rationale:** This score reflects a methodologically interesting paper with a clean technical idea (Q-SPSA + DDC) and practically relevant memory savings, but held back by (i) gaps in the theoretical justification of DDC, (ii) an asymmetrical baseline comparison that weakens the central empirical claim, (iii) missing comparisons with prior ZO+quantization methods, (iv) absence of statistical significance reporting, and (v) several overclaims in the narrative framing. The core contribution — perturbing quantization scales rather than discrete weights for ZO fine-tuning — is novel and well-motivated, but the paper's current evidence package does not fully support its strongest claims. The research value is moderate: the method is practical and reproducible, but the theoretical depth is limited and the empirical validation would benefit from more rigorous baselines.

**Scoring breakdown (research value prioritized):**
- **Novelty (7/10):** Q-SPSA's scale-perturbation trick is genuinely new and non-obvious. DDC is a standard clipping technique applied in a novel context. However, the overall idea of combining ZO with quantization has been explored in prior work (ZO-signSGD line).
- **Validity/Soundness (5/10):** The theoretical variance analysis has gaps. The empirical comparison is weakened by using SGD as the upper-bound and missing direct comparisons with prior ZO+quant methods. Single-seed reporting limits reliability assessment.
- **Research value / significance (6/10):** The practical memory savings are real and important for resource-constrained researchers. The 2-bit results suggest potential for on-device learning. However, the limited baseline comparisons and absence of significance testing reduce the actionable knowledge contribution.
- **Reproducibility (7/10):** Code is provided, implementation details are mostly sufficient, and the algorithm description is clear. Notation inconsistency is a minor obstacle. Data and quantization tool references are given.
- **Presentation (6/10):** The paper is well-structured and mostly clearly written. However, narrative overclaims ("on par," "maximum reduction") reduce credibility. The conclusion introduces unsupported new results. Related work is catalog-style rather than analytical.

**Post-Revision Target: [7, 8]/10** — With strengthened theoretical claims (correcting the bias/variance derivation), addition of AdamW and ZO-signSGD baselines, multi-seed variance reporting, corrected narrative overclaims, and proper handling of the Stable Diffusion results, this paper could reach a score of 7-8.

---

**ASCII Diagram — Related-Work Taxonomy Tree (Layered)**

```text
Related Work: Memory-Efficient LLM Fine-Tuning (Root)
├── Branch 1: Gradient/Optimizer State Reduction
│   ├── Leaf 1.1: Low-rank gradient projection (GaLore)
│   ├── Leaf 1.2: Zeroth-order optimization (MeZO, SPSA)
│   └── Leaf 1.3: Mini-batch gradient matching (CoLM)
│
├── Branch 2: Weight Compression
│   ├── Leaf 2.1: Scalar-based PTQ (GPTQ, Quarot, LLM.int8)
│   └── Leaf 2.2: Codebook-based PTQ (AQLM, VPTQ)
│
├── Branch 3: Combined ZO + Quantization
│   ├── Leaf 3.1: Sign-based ZO on quantized weights (ZO-signSGD, ZOQO, Feng et al.)
│   └── Leaf 3.2: Scale-perturbation ZO (QZO — THIS PAPER)
│
└── Branch 4: Parameter-Efficient Fine-Tuning
    └── Leaf 4.1: Adapter-based methods (LoRA, QLoRA)
```

**Value Contribution Mapping:**
- QZO sits at the intersection of Branch 1.2 (ZO eliminates gradients/states) and Branch 2.1/2.2 (PTQ compresses weights).
- The primary value-add over Branch 3.1 (prior ZO+quant) is avoiding per-step re-quantization and noise quantization.
- The primary value-add over Branch 4.1 (LoRA/QLoRA) is eliminating both gradient storage and optimizer states entirely, while also compressing weights.
- **Novelty position:** Genuinely new mechanism for ZO+quantization (scale perturbation), but the broader problem setting is explored in prior literature. External literature verification is deferred due to Retrieval-Disabled Mode.

---

**Novelty & Retrieval Note:** External literature verification (paper_search) was unavailable in this run (Retrieval-Disabled Mode due to missing API token). All novelty/comparison conclusions above are based on manuscript-internal evidence and the paper's self-cited references. A full novelty audit against ZO-signSGD-based methods and the broader ZO+quantization literature is deferred for manual verification by the authors or future review.