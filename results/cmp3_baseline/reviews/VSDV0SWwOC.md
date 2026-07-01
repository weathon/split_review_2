## Summary

This paper proposes LS-Merge, a framework that encodes LLM weights into a latent space using a transformer-based VAE, performs merging (interpolation, soup, etc.) in that latent space, and decodes back to weights. The key technical contributions are a two-stage curriculum for VAE training on heavy-tailed weight distributions, and optimal transport alignment that enables merging across heterogeneous architectures (different widths/depths and even across model families like Gemma \(\leftrightarrow\) LLaMA). Experiments on Gemma, LLaMA, and LoRA experts show that latent-space merging consistently outperforms weight-space baselines and is competitive with activation-based merging methods, while also enabling cross-architecture merging for the first time, albeit with modest gains.

## Strengths

- **Problem formulation is timely and well-motivated.** The paper correctly identifies that existing model merging methods are largely confined to shape-compatible models, and moving merging operations to a learned latent space is a natural avenue for overcoming this limitation.
- **The analysis of LLM weight statistics (Table 1) is concrete and informative.** The observation that weights exhibit high kurtosis (heavy tails) rather than a Gaussian distribution provides a principled justification for the design choices in the encoder, such as the two-stage curriculum and the choice of transformer architecture.
- **The OT-based alignment for heterogeneous merging is a technically sound and principled solution.** Treating cross-architecture merging as a manifold registration problem and using closed-form affine optimal transport under a Gaussian assumption is a clean approach that appears effective in the experiments.
- **The evaluation is reasonably comprehensive,** covering self-merging, expert merging, representation-merging baselines (Task Arithmetic, AIM), cross-architecture merging, and ablation studies on compression ratio and component contributions.

## Weaknesses

### Fatal
*(None.)*

### Major

- **Practical scalability is inadequately addressed.** The VAE must be trained on weight snapshots, but the paper does not specify the training data (how many checkpoints? from which training stages? what diversity?), the training cost (GPU-hours, model size), or the inference overhead of encoding/decoding. Without this information, it is impossible to assess whether the method is viable at the scale of modern LLMs (hundreds of billions of parameters). The claim of "scalable" in the title and conclusion is not supported by evidence.

- **Empirical improvements are modest and not always statistically significant.**  
  - In Table 2 (self-merging), the gain over the base model is \(< 3\%\) absolute on most benchmarks.  
  - In Table 3 (expert merging), LS-Merge(soup) is the top performer, but the margin over Greedy Soup or SLERP is small (e.g., MMLU: 56.0 vs 50.8; HellaSwag: 60.1 vs 54.6). Many numbers lack error bars, making it difficult to judge if improvements are meaningful.  
  - In Table 5 (cross-architecture), the improvement over the base model is \(+0.92\%\) on WinoGrande, \(+0.56\%\) on ARC-C, and \(+1.03\%\) on HellaSwag—these are very small.  
  - The paper would benefit from statistical significance testing or at least consistent reporting of standard deviations across all tables.

- **The "architecture-agnostic" claim is overstated.** The framework requires separate VAEs for each distinct architecture (or family), followed by OT alignment. This is not "architecture-agnostic" in the sense of a single encoder handling arbitrary architectures; rather, it is a two-stage procedure that still requires training multiple weight encoders. The OT alignment also assumes each layer’s latent distribution is Gaussian, which is a strong simplification not validated.

- **The role of the VAE's latent space is not clearly disentangled from simple post-hoc averaging of latent codes.** The paper describes "self-merging" as sampling multiple codes from the posterior and merging them. This could be seen as a stochastic ensemble effect rather than evidence that the latent space provides a fundamentally better structure for merging. The comparison to VAE reconstruction alone (Table 2) is helpful but does not isolate the merging operation from the VAE's denoising property.

### Minor

- **Algorithm 1 is poorly explained.** The "Proportional mapping to fixed \(d\)" step (line 4) is not defined: how exactly are the per-layer latents rescaled or projected to a common dimension when the architectures differ in depth/width? The description in Section 3.3 gives a formula for a scalar ratio \(r\) but does not specify how this translates to a concrete mapping of latent arrays.

- **The two-stage curriculum is presented without ablations.** The paper claims that training a deterministic autoencoder first then fine-tuning with KL helps stability and OOD generalization, but no experiment compares this curriculum to standard VAE training or other stabilisation techniques.

- **Figure 3 (latent embedding visualization) is low quality and provides limited insight.** The clusters appear noisy, and it is unclear whether the "overlap" between source and target is an artefact of the 2D projection or a genuine property of the OT-aligned latents.

### Trivial

- The paper references "Algorithm 2" in Section 3.3 but the only algorithm given is Algorithm 1.
- Table 8 (PCA vs VAE) has a formatting issue: the first row is labelled “Gemma-3-1b-it” but the “ratio” column says “1.0\(\times\)”.

## Nice-to-Haves

- It would be informative to see an experiment where the VAE is trained **jointly** on multiple architectures (e.g., using cross-architecture weight chunks) rather than training separate VAEs and then aligning latents. This would simplify the pipeline and test whether a single latent manifold can capture weight patterns across architectures.
- An analysis of the computational cost of OT alignment per layer (solving the closed-form Gaussian map) would help readers judge overhead for very deep models (e.g., 100+ layers).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report GPU-hours and VAE parameter counts for the largest experiment, and clarify the size and source of the weight-snapshot training set.
2. Provide error bars for all main tables (or a discussion of statistical significance).
3. Clarify the “proportional mapping” step in Algorithm 1 with a concrete equation or dimension diagram.
4. Add an ablation that replaces the two-stage curriculum with standard VAE training to justify its benefit.
5. Tone down the “architecture-agnostic” claim; it is more accurate to say “architecture-flexible via separate encoders plus alignment.”

## Score and Decision

The paper tackles a relevant problem with a technically sound approach, and the idea of using optimal transport to align latent representations for heterogeneous merging is novel. However, the empirical gains are modest, the practical scalability and training cost are left unclear, and key design choices (curriculum, Gaussian OT assumption) are not rigorously justified. These concerns weigh against acceptance at ICLR, which expects contributions of strong significance and thorough validation.

MY FINAL SCORE: <score>4.5</score>  
MY FINAL DECISION: <decision>Reject</decision>