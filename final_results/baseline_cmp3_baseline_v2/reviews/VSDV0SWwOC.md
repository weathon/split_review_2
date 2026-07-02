## Summary

This paper proposes LS-Merge, a framework for merging LLMs by encoding their weights into a latent space using a transformer-based VAE, performing merging operations (interpolation, soup) in that space, and decoding back to weights. The key contributions are enabling heterogeneous merging across different architectures/sizes via optimal transport alignment of latent distributions, and demonstrating that latent-space merging is more robust than direct weight-space averaging. Experiments on Gemma and LLaMA models show improvements over weight-space baselines for expert merging and cross-architecture scenarios.

## Strengths

- **Novel and well-motivated approach**: Shifting model merging from weight space to a learned latent space is a conceptually clean way to handle heterogeneous architectures. The paper provides good motivation by analyzing LLM weight statistics (heavy tails, low-rank structure) and showing why non-linear encoding is necessary (PCA collapse in Table 8).

- **Comprehensive experimental validation**: The paper evaluates across multiple scenarios (self-merging, expert merging, cross-architecture, cross-family) with multiple benchmarks (MMLU, HellaSwag, GSM8k, etc.) and compares against several baselines (Uniform Soup, SLERP, Greedy Soup, DARE-TIES, Task Arithmetic, AIM). The ablation studies (component contributions, compression trade-off, linear vs. non-linear) are thorough and informative.

- **Principled handling of heterogeneity**: The optimal transport alignment for cross-architecture merging is a theoretically grounded solution to the latent distribution mismatch problem. The closed-form Gaussian OT map is computationally feasible and the empirical results (Table 5, Figure 4) demonstrate its necessity.

- **Strong empirical results**: LS-Merge consistently outperforms weight-space baselines in expert merging (Table 3) and achieves competitive results against activation-based methods (Table 4). The self-merging results (Table 2) show meaningful gains over the base model.

## Weaknesses

### Major

- **Scalability concerns are not adequately addressed**: The paper acknowledges that training VAEs on billions of parameters is computationally demanding, but provides no analysis of the actual training cost, inference overhead, or memory requirements. For a method that claims to be "scalable," the lack of any compute budget, training time, or parameter count for the VAE itself is a significant omission. The VAE must be trained on actual LLM weights, which requires access to those weights and substantial compute. How does this compare to the cost of the baselines?

- **The VAE training data and procedure are underspecified**: The paper states training data consists of "pretrained weight snapshots" but does not specify how many snapshots, from which training stages, or how they were obtained. The two-stage curriculum (deterministic AE then VAE fine-tuning) is mentioned but no details are given about convergence criteria, training duration, or validation. Without this information, reproducibility is limited and it's unclear how sensitive the method is to training details.

- **Limited evaluation of heterogeneous merging**: While cross-architecture merging is a key claimed contribution, the evaluation is limited to three benchmarks (WinoGrande, ARC-C, HellaSwag) in Table 5 and a single figure (Figure 4). The gains are modest (e.g., 56.83→57.75 on WinoGrande, 42.78→43.34 on ARC-C). More extensive evaluation across diverse tasks would strengthen the claim. Additionally, the cross-family experiment only merges LLaMA-3.2-1B into Gemma-3-1B; the reverse direction or other family pairs are not explored.

- **The "self-merging" concept is not clearly distinguished from standard VAE sampling**: The paper describes self-merging as "sampling multiple latent codes from one model's posterior distribution and merging them." This appears equivalent to drawing multiple samples from the VAE posterior and averaging them, which is a standard technique for improving VAE reconstructions. The paper should clarify whether there is a novel algorithmic contribution here beyond standard VAE inference.

### Minor

- **The theoretical compressibility argument (Section 3.1) is somewhat disconnected from the method**: The PCA analysis and manifold embedding theory motivate compression, but the actual VAE operates on chunked, flattened weight vectors rather than on the full weight matrices. The connection between the low-rank structure of individual weight matrices and the design of the chunking/encoding scheme could be made clearer.

- **The optimal transport alignment assumes Gaussian latent distributions**: The closed-form OT solution relies on approximating each layer's latent distribution as Gaussian. The paper does not validate this assumption empirically (e.g., by showing that latent distributions are approximately Gaussian) or discuss what happens when this assumption is violated.

- **Table 2 shows LS-Merge outperforming VAE reconstruction, but the mechanism is unclear**: The paper attributes this to "exploring the learned latent distribution" but doesn't explain why merging multiple posterior samples yields better performance than a single sample. Is this simply variance reduction, or is there a more interesting phenomenon?

### Trivial

- Algorithm 1 is labeled "Algorithm 2" in the text (Section 3.3: "summarized in algorithm 2").
- The notation in the heterogeneous mapping section is somewhat confusing (e.g., using both $n_s$ and $M$ for source dimensions).

## Nice-to-Haves

- An analysis of the computational cost of the VAE (training time, GPU hours, parameter count) relative to the baselines would greatly strengthen the scalability claims.
- A discussion of failure cases or settings where latent-space merging underperforms weight-space merging would provide a more balanced assessment.
- An investigation of whether the VAE latent space has interpretable structure (e.g., do different directions correspond to different capabilities?) would be interesting.

## Novel Insights

The key insight is that LLM weights, despite their high dimensionality, lie on a low-dimensional non-linear manifold that can be learned by a VAE, and that merging operations performed in this latent space are more robust than those in weight space because the latent space regularizes the merge to stay on the manifold of valid weights. The optimal transport alignment for heterogeneous merging is a natural extension: if two models' weight manifolds are disjoint, one must register them before interpolation. This perspective unifies homogeneous and heterogeneous merging under a single framework.

## Suggestions

- Provide training details for the VAE: number of weight snapshots used, training compute, convergence criteria, and validation procedure.
- Add more extensive evaluation of heterogeneous merging, including more tasks and additional architecture pairs (e.g., different model families in both directions).
- Clarify the distinction between "self-merging" and standard VAE posterior sampling, or reframe the contribution accordingly.
- Validate the Gaussian assumption for latent distributions used in the OT alignment, or discuss alternatives.

## Score and Decision

The paper presents a novel and well-motivated framework for model merging with strong empirical results. The main concerns are around scalability (lack of computational analysis) and the limited evaluation of the heterogeneous merging claim. However, the core idea is sound, the experiments are otherwise thorough, and the ablation studies are informative. The paper makes a clear contribution to the model merging literature.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>