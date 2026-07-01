## Summary

This paper systematically compares Transformers and modern recurrent models (SSMs like Mamba, Hyena) on associative recall and copying tasks, revealing that SSMs suffer from critical optimization instabilities—their success is confined to a narrow learning rate window, unlike Transformers which are robust across a wide range. The authors show that this brittleness can confound prior expressivity comparisons, and further uncover contrasting scaling behaviors (SSMs favor width, Transformers favor depth) and divergent single-layer dynamics. Through ablations, they identify the 1D convolution as a key driver of Mamba’s single-layer expressivity and demonstrate that newer architectures like DeltaNet can improve optimization stability.

## Strengths

- **Thorough empirical investigation**: The paper conducts over 3,000 runs and ~20,000 GPU hours, systematically sweeping learning rates and model configurations. This provides strong evidence for the optimization instability claim and convincingly shows that prior work may have drawn misleading conclusions due to insufficient tuning.
- **Clear and actionable findings**: The demonstration that SSMs require extremely narrow learning rate windows (Fig. 1) and that scaling strategies differ fundamentally (width vs. depth) gives practitioners concrete guidance for fair comparisons and model design.
- **Novel insights into single-layer dynamics**: The observation that 1-layer Transformers exhibit induction-head-like loss bumps without accuracy gains, while 1-layer Mamba can solve the task, is interesting and well-analyzed. The ablation identifying the convolution as the critical component for Mamba’s single-layer success is a clean mechanistic finding.
- **Relevance to ongoing debates**: The paper directly addresses the conflicting views on SSMs vs. Transformers, providing a learnability-focused perspective that re-contextualizes prior expressivity analyses. This is timely and important for the community.

## Weaknesses

### Fatal
None.

### Major
- **Limited to synthetic benchmarks**: The study is conducted entirely on MQAR and copying tasks. While these are well-motivated as proxies for in-context learning, the paper’s central claim about optimization stability being the key differentiator between SSMs and Transformers would be significantly strengthened by validation on downstream language modeling tasks. The authors acknowledge this limitation but it remains a gap.
- **Lack of theoretical analysis for optimization instability**: The paper empirically documents the narrow learning rate window but offers only a brief hypothesis (vanishing gradients from the decay rate in Mamba’s A matrices) without formal analysis or proof. A deeper theoretical understanding of why this instability occurs would elevate the contribution.
- **Overstatement of the central thesis**: The paper states “Transformers differ from SSMs not in terms of expressive power but mainly because of their optimization dynamics.” However, the results also show expressivity differences (e.g., 1-layer Transformer cannot solve MQAR while Mamba can, even with optimal tuning). The authors later show that adding a convolution to the Transformer closes this gap, but the claim as stated is too strong—there are known theoretical expressivity limitations of SSMs (finite state) that are not fully addressed.

### Minor
- The paper could more clearly separate the effects of optimization instability from expressivity limitations when comparing models at different widths. For example, Hyena still underperforms at low widths even with optimal learning rates, suggesting a genuine expressivity gap that is not purely optimization-driven.
- The analysis of DeltaNet’s stability (Fig. 7) is promising but limited to model dimensions up to 256 due to implementation constraints. It would be helpful to see if the stability holds at larger scales.

### Trivial
None.

## Nice-to-Haves

- Extend the analysis to include training dynamics on real language modeling tasks (e.g., perplexity on a small LM dataset) to validate whether the optimization instability observed on synthetic tasks transfers.
- Provide a theoretical characterization of the loss landscape for SSMs, perhaps linking the narrow learning rate window to the spectral properties of the recurrence or the gradient flow.
- Investigate whether adaptive learning rate methods beyond Adam (e.g., AdamW with different schedules) can mitigate the instability.

## Novel Insights

Beyond the paper’s own contributions, a genuinely novel insight is the demonstration that the 1D convolution in Mamba is the key architectural component enabling single-layer associative recall, and that adding a similar convolution to a Transformer makes it equally capable. This suggests that the convolution provides a form of local pattern matching that compensates for the lack of depth, and that the core difference between these architectures may be more about inductive biases for local vs. global processing than about fundamental expressivity. The finding that single-layer Transformers exhibit induction-head-like dynamics without solving the task also provides a new perspective on the role of depth: depth is not just for forming induction heads, but for actually leveraging them effectively.

## Suggestions

- Consider adding a small-scale language modeling experiment (e.g., on WikiText-2) with matched parameter counts and learning rate sweeps to directly test whether the optimization instability observed on synthetic tasks translates to real data.
- Provide a more nuanced statement of the central thesis, acknowledging that both expressivity and learnability differences exist, but that optimization has been underappreciated as a confounder.

## Score and Decision

**Score**: 8  
**Decision**: Accept

MY FINAL SCORE: <score>8</score>  
MY FINAL DECISION: <decision>Accept</decision>