## Summary

The paper introduces **Thoughtbubbles**, a transformer variant that learns to dynamically fork and delete residual streams during pretraining using only a language modeling loss. This enables parallel adaptive computation in latent space without requiring explicit chain-of-thought tokens or supervised reasoning traces. Experiments across 150M–772M parameter scales on OpenWebText and peS2o show consistent perplexity improvements and gains on zero-shot tasks (LAMBADA, HellaSwag) over both parameter-matched and computation-matched baselines. The method also allocates more computation to tokens with higher uncertainty, providing interpretable behavior.

## Strengths

- **Novel and well-motivated architecture.** The idea of learning to fork/delete residual streams as a budget-constrained allocation problem is original and addresses a clear limitation of fixed-computation transformers. The design of cumulative scores, top‑k selection, and score-attenuated attention/residual updates is technically sound and internally consistent.
- **Consistent empirical gains across scales and datasets.** Thoughtbubbles outperforms both the standard transformer and the “copy” baselines (which add non‑adaptive parallel computation) on validation perplexity in all settings, and on most zero‑shot evaluations. The improvement is often substantial (e.g., 772M model on OpenWebText: 19.74 vs. 21.22 perplexity). The scaling plot (Figure 3) shows that the advantage holds across model sizes.
- **Interpretable computation allocation.** The analysis in Section 5 demonstrates that the model allocates more forks to tokens with higher output entropy (uncertainty), and that forked tokens are strongly attended to by their parent token. This provides evidence that the learned forking behavior is meaningful and not just a random artifact.
- **Unsupervised training.** The method requires no additional supervision beyond standard language modeling loss, making it directly applicable during pretraining. This is a significant practical advantage over methods that need explicit chain‑of‑thought data or special training stages.

## Weaknesses

### Major

1. **Baseline comparison is not fully fair.** The “copy‑3” and “copy‑5” baselines add extra residual streams by simply duplicating the input, but they do not have any mechanism to *selectively* allocate computation. They also do not use score attenuation or output averaging. While the paper claims these are “computation‑matched,” the comparison conflates the effect of *adaptive* allocation with the effect of simply having more parallel streams. A stronger baseline would be a model that also uses a learned gating mechanism to weight multiple copies, or a model that inserts a fixed number of “pause tokens” at every position (as in Goyal et al., 2024). Without such a control, it is unclear how much of the gain comes from adaptivity versus from the increased representational capacity of multiple residual streams.

2. **Limited scale and training budget.** All models are trained for only 2.5 billion tokens, which is relatively small by modern standards. The zero‑shot results on BLiMP and PIQA are often close to or below the copy baselines, and the paper acknowledges that harder reasoning tasks (e.g., GSM8K) are not evaluated due to scale limitations. This makes it difficult to assess whether the method will maintain its advantage when scaled to the regime where adaptive computation is most needed (e.g., multi‑step reasoning). The claim that “our approach at a smaller 319M scale outperformed baselines at 772M scale” is interesting but based on a single metric (perplexity) and may not hold for downstream tasks.

3. **No wall‑clock or efficiency comparison.** The paper mentions that the implementation is in raw PyTorch and that hardware‑adaptive kernels would improve efficiency, but it does not report actual training or inference time. Since the method increases the effective sequence length (up to 4× the input block size), the computational overhead is non‑trivial. Without a comparison of FLOPs or wall‑clock time, it is hard to judge the practical trade‑off between the perplexity gain and the added cost.

4. **Potential training instability and gradient issues.** The top‑k selection is non‑differentiable, and the paper notes in the Limitations that too much forking leads to no further improvement because early high‑scoring tokens may be dropped later, causing gradient starvation. The paper does not provide any analysis of training stability (e.g., variance of scores across runs, sensitivity to the placement of forking layers, or the effect of the log‑space implementation). This is a concern for reproducibility and for scaling to deeper models.

### Minor

- The paper claims “first‑known architecture to enable unsupervised dynamic allocation of latent parallel computation.” While the specific mechanism is novel, related work on pause tokens (Goyal et al., 2024; Herel & Mikolov, 2024) also adds extra residual streams, albeit not adaptively. The claim should be softened or more precisely qualified.
- The analysis of forking behavior (Figure 5) shows a concave relationship between entropy and number of forks, but the explanation is speculative. The paper could provide more quantitative evidence (e.g., by comparing the entropy of tokens that are forked vs. not forked, or by showing examples).
- The autoregression results (Figure 6) show that naive fixed forking causes a distribution shift, but the proposed dynamic forking mitigation is only briefly described in the appendix. The main text would benefit from a clearer explanation of how the budget is scaled.

### Trivial

- The notation in Section 2.2 is somewhat heavy and could be simplified. For example, the distinction between $x_j^{(k)}$ and $x_{i,j}^{(k)}$ is clear but the text occasionally uses them inconsistently.
- Figure 1 and Figure 2 are dense and the captions are long; a cleaner schematic would improve readability.

## Nice-to-Haves

- An ablation study that removes the score attenuation (i.e., uses forking but without modulating attention/residual updates) would help isolate the contribution of the scoring mechanism.
- A comparison with a model that inserts a fixed number of learnable “thinking tokens” at every position (similar to Goyal et al., 2024) would strengthen the claim that adaptivity is beneficial.
- Reporting the actual number of forks per layer on average (e.g., what fraction of the budget is used) would give insight into how aggressively the model prunes streams.

## Novel Insights

Beyond the paper’s own contributions, the observation that the model learns to allocate more computation to tokens with moderate (rather than extreme) entropy is interesting and aligns with the intuition that the most uncertain tokens (e.g., at clause boundaries) may not benefit from additional parallel computation. This suggests that adaptive computation methods may need to target a specific “zone” of difficulty rather than simply the hardest tokens. The attention analysis (Figure 4) also provides a clear mechanistic view of how forked streams are used: the parent token attends strongly to its children, indicating that the forks serve as a form of local memory.

## Suggestions

- Add a baseline that uses a fixed number of learnable “pause tokens” inserted at every position (as in Goyal et al., 2024) to better isolate the benefit of adaptivity.
- Report the actual FLOPs or wall‑clock time for training and inference, so readers can assess the efficiency trade‑off.
- Provide an analysis of training stability (e.g., score variance across random seeds, sensitivity to the placement of forking layers).
- Include results on a more challenging reasoning task (e.g., GSM8K) at a larger scale, or at least discuss the expected behavior.

## Score and Decision

The paper presents a novel and well‑engineered architecture for adaptive parallel computation in transformers, with consistent empirical improvements over reasonable baselines. The main weaknesses are the lack of a fully fair baseline (non‑adaptive parallel streams with learned gating) and the limited scale of experiments, which make it unclear whether the method will translate to the large‑scale, multi‑step reasoning regime where adaptive computation is most valuable. The contribution is solid but not yet transformative. I recommend borderline accept.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>