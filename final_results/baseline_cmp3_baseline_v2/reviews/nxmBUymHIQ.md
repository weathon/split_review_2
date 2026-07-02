## Summary

The paper proposes *LoLoRA*, a method that augments Low-Rank Adaptation (LoRA) by replacing gradient-based updates of the adapter matrix $A$ with local, forward-pass unsupervised updates (e.g., Hebbian PCA or autoencoder loss). The aim is to reduce activation memory during fine-tuning while allowing $A$ to adapt to input distributions, in contrast to the fully frozen $A$ in LoRA-FA. Theoretical analysis identifies the optimal $A$ as any non-singular transformation of the top principal components of the input covariance matrix. Experiments on GLUE, mathematical reasoning, and multimodal fine-tuning show that *LoLoRA* matches or slightly improves upon LoRA-FA, but does not convincingly outperform the simpler LoRA-FA with EVA initialization.

## Strengths

- **Addresses an important problem**: Reducing activation memory during fine-tuning of large models is practically relevant, and exploring local (backprop-free) updates for LoRA adapters is a worthwhile research direction.
- **Theoretical grounding**: Theorem 4.4 provides a formal characterization of optimal $A$ under a random regression model, linking good initializations to the principal subspace of layer inputs. This offers insight beyond the purely empirical EVA work.
- **Diverse empirical evaluation**: Experiments span NLU (RoBERTa-large), mathematical reasoning (LLaMA-3.1-8B), and multimodal fine-tuning (LLaVA-7B), with multiple runs and standard deviations reported.
- **Thorough ablations**: The paper compares several local update rules (HPCA, AE, SoftHebb) and initialization strategies (uniform, orthogonal, PiSSA, EVA), giving a clear picture of which components matter.

## Weaknesses

### Fatal
None.

### Major

1. **Limited improvement over the simpler LoRA‑FA baseline**  
   The core practical claim is that *LoLoRA* “consistently outperforms standard LoRA-FA in two out of three experimental setups.” However, a close inspection of Tables 1–4 shows that *LoLoRA* HPCA often performs **on par with or worse than LoRA‑FA (uniform)**. In GLUE, *LoLoRA* is below LoRA‑FA (uniform) on CoLA, MRPC, STS‑B, MNLI, QQP; it ties or is slightly better only on RTE, QNLI, SST‑2. In the math reasoning task, both LoRA‑FA (EVA) and *LoLoRA* HPCA achieve 0.829—identical. In LLaVA, *LoLoRA* HPCA (1.075 loss) is better than LoRA‑FA (uniform) (1.087) but worse than LoRA‑FA (EVA) (1.070). The advantage over an already memory‑efficient baseline is marginal at best and often absent. The claimed “consistent” improvement is not supported.

2. **Misleading claim about memory reduction**  
   The paper states that *LoLoRA* “further reduc[es] the memory required for fine‑tuning” relative to standard LoRA. The proper baseline for memory‑saving is LoRA‑FA, which already avoids storing activations for $A$. In the provided numbers, *LoLoRA* does **not** reduce memory below LoRA‑FA: for LLaMA‑8B both use 26 GB extra; for LLaVA, *LoLoRA* uses 24.1 GB vs. LoRA‑FA’s 23.9 GB (i.e., slightly more). The memory benefit over standard LoRA is inherited from freezing $A$, not from the local updates. The paper should clarify that *LoLoRA* aims to improve *performance* over LoRA‑FA while maintaining comparable memory, not further reduce it.

3. **Lack of comparison to widely‑used memory‑efficient methods**  
   The paper compares only to LoRA and LoRA‑FA. In practice, many practitioners use QLoRA (Dettmers et al., 2023) or gradient checkpointing to cut activation memory. QLoRA combines 4‑bit quantization with LoRA and achieves much larger memory savings than the ∼13% reported here. The absence of such comparisons makes it hard to gauge the practical relevance of the proposed savings.

4. **Computational overhead is under‑analyzed**  
   The local updates require extra forward‑pass computation and a separate optimizer state for $A$. Run‑time data from LLaVA (Table 4) shows *LoLoRA* HPCA (2h52m) is slightly slower than LoRA‑FA uniform (2h46m) and LoRA uniform (2h45m). The paper does not discuss the FLOPs or training time overhead relative to LoRA‑FA, nor does it provide a breakdown of where memory is saved vs. added.

5. **Theoretical analysis has limited direct connection to the empirical scheme**  
   Theorem 4.4 is derived under strong assumptions (i.i.d. Gaussian random $\Delta W_0$, isolated submodule, stationary targets) that do not hold in practice. The theorem justifies PCA‑based *initialization*, but the method uses *online* updates (HPCA) whose dynamics during joint training with $B$ are not analyzed. The paper acknowledges the stationarity limitation but does not bridge the gap between the static optimal‑initialization result and the claimed benefit of iterative local adaptation.

### Minor

- The paper repeatedly states that *LoLoRA* reduces memory compared to standard LoRA (which is true) but fails to emphasize that the reduction comes from *freezing* $A$ rather than from the local update mechanism. LoRA‑FA already achieves the same memory profile.
- Tables 1 and 2 use bold only for the overall best; this sometimes hides that *LoLoRA* is not significantly different from LoRA‑FA (e.g., RTE). More statistical testing (e.g., confidence intervals, paired tests) would strengthen the empirical claims.
- The summary of GLUE results says “LoRA remains strongest overall” but then argues that *LoLoRA* improves over LoRA‑FA; this is somewhat contradictory given the results.
- Notation inconsistencies: In Definition 3.1, “$W_o$” is listed twice.

### Trivial

- Some references in the main text (e.g., Vaswani et al., 2023) are not in the provided reference list (likely a formatting artifact).
- The paper uses both “LoLoRA” and “*LoLoRA*”; capitalization is inconsistent in a few places.

## Nice-to-Haves

- A comparison to QLoRA or gradient‑checkpointed LoRA would give the reader a more complete picture of where *LoLoRA* sits in the memory‑performance trade‑off landscape.
- An analysis of how well the subspace learned by HPCA matches the true principal components during training (e.g., subspace distance) would strengthen the connection to theory.
- A discussion of the effect of the extra optimizer state for $A$ on total memory (even if small) would be helpful.

## Novel Insights

None beyond the paper’s own contributions.

## Suggestions

- Reframe the paper’s contribution: instead of claiming “further memory reduction,” position *LoLoRA* as a method to *adapt* the frozen‑$A$ baseline (LoRA‑FA) via cheap local updates, with the goal of closing the performance gap to full LoRA while keeping memory nearly as low as LoRA‑FA.
- Include a comparison to QLoRA (and maybe LoRA+ or DoRA) to demonstrate the practical significance of the memory savings.
- Provide a more nuanced summary of experimental results: acknowledge that *LoLoRA* usually performs similarly to LoRA‑FA (EVA), and that the improvement over LoRA‑FA (uniform) is modest and task‑dependent.
- Add a brief ablation on the computational cost (FLOPs per forward pass) of the local update rules.

## Score and Decision

**Score**: 4 – borderline reject  
**Decision**: Reject

**Rationale**: The paper tackles a relevant problem and offers a clean theoretical insight, but the experimental evidence does not convincingly demonstrate that the proposed method improves over the simpler LoRA‑FA baseline in either performance or memory. The claimed memory reduction is already achieved by LoRA‑FA, and the performance gains are marginal, inconsistent, and often absent. The lack of comparison to widely adopted memory‑saving techniques (e.g., QLoRA) further limits the contribution. Overall, the incremental nature of the results and the overstated claims make the paper unsuitable for acceptance at ICLR in its current form.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>