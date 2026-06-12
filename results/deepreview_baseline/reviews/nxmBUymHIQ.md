## Summary
This paper introduces LoLoRA, a memory-efficient fine-tuning method for LLMs that combines local unsupervised updates of the LoRA adapter matrix A with gradient-based updates of matrix B. The authors provide theoretical justification showing that optimal initialization of A should approximate the dominant eigenspace of the input covariance matrix, and propose using Hebbian PCA or autoencoder-based local learning rules to update A during the forward pass without storing activations for backpropagation. Experiments on GLUE, mathematical reasoning, and multimodal tasks show that LoLoRA achieves comparable performance to standard LoRA while reducing memory consumption.

## Strengths
- **Theoretical contribution**: The paper provides a rigorous theoretical analysis (Theorems 4.4, 4.5, 4.6) characterizing the optimal initialization for matrix A under random regression assumptions, which is a valuable addition to the LoRA literature. The proof that optimal A should span the top-r principal components of the input covariance matrix is clean and well-motivated.
- **Novel hybrid approach**: Combining local unsupervised updates for A with gradient-based updates for B is a creative solution that addresses the memory bottleneck of standard LoRA while avoiding the performance degradation of simply freezing A. The method is well-motivated by the observed asymmetry between A and B matrices.
- **Comprehensive experimental evaluation**: The paper evaluates on multiple diverse tasks (NLU, mathematical reasoning, multimodal) with multiple model sizes (RoBERTa-large, LLaMA-3.1-8B, LLaVA-v1.5-7B, TinyLlama-1.1B), providing a thorough assessment of the method's capabilities.

## Weaknesses
### Major
- **Incremental performance gains**: The experimental results show that LoLoRA does not consistently outperform the simpler LoRA-FA (frozen A) baseline. On GLUE (Tables 1-2), LoLoRA is often worse than LoRA-FA (uniform). On mathematical reasoning (Table 3), LoLoRA matches LoRA-FA (EVA) but does not exceed it. The claimed advantage of "adapting to input distribution shifts" is not empirically demonstrated to translate into better performance over a well-initialized frozen A.
- **Memory savings are modest and inconsistent**: The reported memory savings (20% on GLUE, 13% on LLaMA-3.1-8B, ~2% on LLaVA) are relatively small and vary significantly across tasks. The paper does not provide a clear analysis of when the memory savings are meaningful versus when the overhead of local updates (extra optimizer state, forward-pass computation) negates the benefits. The LLaVA experiment shows only 0.5-0.7 GB savings, which is marginal.
- **Missing comparison to other memory-efficient PEFT methods**: The paper only compares against LoRA and LoRA-FA variants. There is no comparison to other memory-efficient PEFT methods like VeRA, DoRA, or QLoRA, which also address activation memory. This limits the ability to assess where LoLoRA stands in the broader landscape.

### Minor
- **Computational overhead not fully characterized**: While the paper reports run time for LLaVA experiments, there is no systematic analysis of the computational cost of the local update rules (HPCA, AE) versus standard backpropagation. The ablation on TinyLlama (Table 6) does not report training time, making it difficult to assess the efficiency trade-off.
- **Limited analysis of non-stationarity**: The paper acknowledges that the theoretical analysis assumes stationary targets, which is not the case in multilayer architectures. However, there is no empirical investigation of how the local updates behave under non-stationary conditions or whether they might interfere with the gradient-based updates of B.

### Trivial
- The paper uses "LoLoRA" as the method name but also uses "LoLoRA HPCA" and "LoLoRA AE" inconsistently in tables and text.

## Nice-to-Haves
- An analysis of how the local update rules interact with different learning rates and optimizer settings for A versus B would be valuable for practitioners.
- A study on the convergence behavior of the HPCA updates during fine-tuning (e.g., how quickly does A converge to the dominant eigenspace, and does it track distribution shifts?)
- Discussion of potential applications beyond standard fine-tuning, such as continual learning or domain adaptation where input distribution shifts are more pronounced.

## Novel Insights
The paper's key insight is that the asymmetry between LoRA matrices A and B can be exploited: A primarily needs to capture the input covariance structure (which can be learned locally without backpropagation), while B handles task-specific adaptation (which requires gradient information). This is supported by theoretical analysis showing that optimal A depends only on input statistics, not on task targets. The connection between this theoretical result and the practical observation that freezing A (LoRA-FA) works reasonably well provides a principled explanation for an empirical phenomenon.

## Suggestions
- Add a comparison to at least one other memory-efficient PEFT method (e.g., VeRA or QLoRA) to contextualize the memory-performance trade-off.
- Provide a more detailed analysis of when the memory savings are practically meaningful (e.g., for different model sizes, batch sizes, sequence lengths).
- Consider adding an experiment where the input distribution shifts significantly during fine-tuning (e.g., multi-task or continual learning setting) to demonstrate the advantage of adaptive A over frozen A.

## Score and Decision
The paper presents a theoretically grounded and well-motivated method, but the empirical results do not convincingly demonstrate that LoLoRA outperforms the simpler LoRA-FA baseline. The memory savings are modest and inconsistent across tasks, and the performance is often comparable to or worse than LoRA-FA with good initialization. While the theoretical contribution is valuable, the practical impact is limited by the incremental nature of the improvements.

MY FINAL SCORE: 5.0</score>
MY FINAL DECISION: Reject</decision>