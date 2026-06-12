## Summary

The paper introduces LoRA-Mixer, a modular Mixture-of-Experts (MoE) framework that applies task-specific LoRA experts to the linear projection layers of attention (Q, K, V) and state-space model (SSM) modules, rather than to the feed-forward network (FFN) as in prior work. To train the router, the authors propose a **Routing Specialization Loss (RSL)** that adds an entropy regularization term to the standard auxiliary load–balancing loss, aiming to promote input-aware specialization while maintaining global expert balance. The framework is evaluated on 15 benchmarks across three base models (LLaMA3-8B, Mistral-7B, Falcon-Mamba-7B), and the authors also demonstrate plug-and-play reuse of publicly available LoRA modules and cross-model transfer.

## Strengths

- **Novel application of MoE to projection layers.** Instead of modifying the FFN or appending parallel branches, LoRA-Mixer inserts mixed LoRA experts into the core Q/K/V projections of the attention (or SSM) module. This placement is well-motivated because it directly influences the attention computation, enabling more fine-grained token-level specialization while preserving architectural compatibility.
- **Comprehensive empirical scope.** The experiments cover 15 diverse benchmarks (MedicalQA, GLUE, GSM8K, ARC, HumanEval, etc.), three base model families (LLaMA, Mistral, Falcon-Mamba), and comparisons against several recent LoRA-MoE and routing baselines (MoLE, MixLoRA, LoraHub, PHATGOOSE, LoRA-LEGO). The inclusion of an SSM (Falcon-Mamba) is a positive addition.
- **Data efficiency analysis.** The paper demonstrates that RSL achieves competitive or superior performance with significantly less training data for the router (e.g., 2K vs. 4K instances), which is practically important for low-resource scenarios. The ablation in Table 9 supports this claim.
- **Support for plug-and-play reuse.** The framework is validated with LoRA modules sourced from public repositories (LoRAHub) while freezing their parameters, showing that the router can be trained on a small independent dataset. This highlights practical value for modular model composition.

## Weaknesses

### Fatal
None.

### Major
- **Marginal empirical gains over strong baselines.** The improvements of LoRA-Mixer over the simple “LoRA” baseline (which likely trains independent or joint LoRAs without routing) are often small (e.g., +0.39% on GSM8K, +0.11% on SST-2 for LLaMA3-8B in Table 2). While some tasks show larger jumps (e.g., +1.71% on HumanEval, +1.78% on BoolQ), the overall advantage is modest. This weakens the claim that the method “significantly improves model performance across all evaluated tasks.”
- **Unclear baseline definition.** The label “LoRA” in Tables 2 and 4 is ambiguous. Is it a single LoRA trained on all tasks jointly, or separate LoRAs for each task? Without clarification, it is difficult to attribute the gains to the routing mechanism versus increased parameter count or training procedure. The paper should state the exact LoRA configuration used for this baseline.
- **Limited theoretical verification in main text.** The paper claims convergence analysis and generalization bounds for RSL (Appendix A.1, A.2), but the main text only provides a gradient derivation and heuristic arguments. Since the appendix is not available for review, the soundness of these theoretical claims cannot be evaluated. The core novelty of RSL (adding entropy regularization to the auxiliary loss) is a straightforward extension; the paper does not provide compelling evidence that this is a non-trivial advance beyond existing loss designs.
- **Cross-model transfer results are inconclusive.** In Table 5, transferring Mistral-7B trained experts to LLaMA3-8B yields improvement on GSM8K and ARC-C (max +1.21% and +0.49%), but degrades on ARC-E ( 3.3% relative drop). This mixed outcome reduces confidence in the robustness of the routing.

### Minor
- **Clarity of RSL motivation.** The paper frames the addition of entropy regularization as a “novel perspective” based on an information bottleneck, but the practical improvement is essentially a standard entropy penalty that sharpens the routing distribution. The connection to the information bottleneck is not fleshed out in the main text.
- **Lack of significance testing.** All results are reported as single averages over three runs, but no confidence intervals or statistical tests are provided. Given the small improvements, this omission makes it hard to assess whether gains are reliable.
- **Expert load analysis (Figure 3) is only weakly informative.** The load across six experts is very balanced (15%–18%), which is the target of load-balancing losses. The paper does not show that the routing is truly input-aware beyond a bar chart (Figure 4) that looks plausible but could benefit from quantitative metrics (e.g., expert–task mutual information).

### Trivial
- Some figure captions are repeated and the text formatting is slightly cluttered (likely due to the PDF extraction), but these do not affect technical assessment.
- The paper uses the term “CRL” in Figure 2 but never defines it in the main text.

## Nice-to-Haves

- A detailed parameter count comparison for each method in the experiments, to substantiate the claim of “48% of the parameters.”
- Results with confidence intervals or error bars to support the statistical significance of the reported improvements.
- An analysis of how often the top-K selection changes for the same input across tasks, to further demonstrate input-awareness.

## Novel Insights

Beyond the paper’s own contributions, the insight that applying MoE routing to the attention projection layers can yield token-level specialization with very few additional parameters is a useful observation for practitioners seeking modular fine-tuning. The idea of regularizing the router’s entropy to obtain sharper, data-efficient specialization is a reasonable design point, though it does not break new theoretical ground.

## Suggestions

- Clearly define the “LoRA” baseline (its training strategy, number of experts, and whether it is a single LoRA or weighted composition) to ensure fair comparison.
- Include a small number of error bars or confidence intervals for the key experiments (e.g., the main comparison in Table 2).
- Move the theoretical analysis (convergence and generalization bound) to the main text or provide a more accessible summary, as it is central to the claimed novelty of RSL.
- Add a discussion of why the cross-model transfer fails on ARC-E and whether this indicates a limitation of the routing.

## Score and Decision

The paper addresses an interesting problem and introduces a practical application of MoE to projection layers. However, the empirical gains over strong baselines are modest, the theoretical contribution of the routing loss is incremental, and several experimental details are ambiguous. The contributions are not sufficiently impactful or well-supported to warrant acceptance at a top venue.

**MY FINAL SCORE:** <score>4.5</score>  
**MY FINAL DECISION:** <decision>Reject</decision>