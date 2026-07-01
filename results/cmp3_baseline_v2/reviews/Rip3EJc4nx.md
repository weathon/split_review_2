## Summary

This paper introduces HFPrune, a structured pruning method for LLMs that replaces the standard one-hot cross-entropy (CE) loss criterion in Taylor-based neuron importance scoring with the information entropy of the model's output distribution. The key claim is that entropy provides a more holistic, label-free measure of a neuron's contribution by considering all potential next-token predictions rather than only the ground-truth token, thereby better preserving the model's global predictive distribution after pruning. Experiments on LLaMA-2, LLaMA-3, and Qwen series models across ten zero-shot benchmarks show consistent improvements over baselines like SDMPrune, LLM-pruner, and LoRAPrune.

## Strengths

- **Clean and well-motivated idea**: Replacing CE with entropy as the Taylor-pruning criterion is a simple yet sensible departure from standard practice. The paper provides clear intuition (Figure 1) for why entropy can capture more information about the model's output distribution than a one-hot target.

- **Label-free and efficient**: The entropy criterion requires no ground-truth labels during importance scoring, which avoids the "zero initial gradient" problem of self-distillation methods and reduces computational overhead (Table 5 shows ~3× speedup over SDMPrune with 31% less peak memory on LLaMA2-7B).

- **Consistent empirical gains**: HFPrune outperforms baselines across multiple model families (LLaMA-2, LLaMA-3.2, Qwen2.5, Qwen3) at various pruning ratios (20%–40%), with Table 1 showing that at 20% sparsity on LLaMA2-7B, HFPrune (59.0%) actually exceeds the original dense model (58.3%) after fine-tuning.

- **Useful ablations**: Table 6 isolates the effect of the entropy criterion without fine-tuning, showing it outperforms CE and SD criteria. Table 7 provides distribution-level metrics (JS distance, Top-15 Jaccard) supporting the claim that entropy pruning better preserves the output distribution.

## Weaknesses

### Major

- **Mischaracterization of cross-entropy in the motivation**: The paper repeatedly claims that CE "ignores all other potential predictions" and "only considers the single ground-truth next token" (Section 1, Figure 1). This is inaccurate. The gradient of CE w.r.t. hidden states involves the full softmax denominator and all logits via ∂L/∂z_j = p_j - y_j. While the one-hot target weights the gradient, the entire vocabulary contributes to the gradient signal through the softmax normalization. The paper builds its motivation on a straw-man depiction of CE, which weakens the theoretical justification for the proposed criterion.

- **Data integrity concerns in Table 3**: The numbers reported for Qwen2.5-1.5B at 20% pruning (SDMPrune) are identical to Qwen2.5-7B at 40% pruning (SDMPrune). Similarly, Qwen3-1.7B at 20% (SDMPrune) duplicates the same row. This pattern strongly suggests a copy-paste or formatting error that undermines confidence in the Qwen experimental results. The paper does not acknowledge or explain these duplications.

- **Limited comparison scope**: The paper compares against only four baselines (LLM-pruner, LoRAPrune, LoRAP, SDMPrune), none of which are state-of-the-art methods like SparseGPT or Wanda. The authors state they focus on "structural pruning methods," but many LLM pruning papers provide results under similar structured settings. The absence of key recent baselines makes it difficult to assess where HFPrune stands in the broader LLM compression landscape.

### Minor

- **Modest absolute gains**: While statistically consistent, the improvements over the best baseline (SDMPrune) are often small — e.g., +0.8% at 20% and +0.7% at 30% on LLaMA2-7B (Table 1). At 30% pruning on smaller LLaMA3.2-1.2B, HFPrune is still 2.88% below the original model, raising questions about how much of the gain is from the entropy criterion versus the post-pruning fine-tuning protocol.

- **MLP-only pruning is a significant restriction**: The method only prunes MLP modules. While the authors justify this with parameter counts and ablation (Table 8), many practical deployment scenarios require simultaneous reduction of both attention and MLP. The paper does not address whether the entropy criterion extends well to attention head pruning, which limits the method's applicability.

- **No perplexity or generation-quality evaluation**: All experiments use zero-shot classification benchmarks. There is no evaluation of perplexity, text generation quality, or task-specific downstream performance, which are standard metrics for assessing LLM compression quality. The claim of "preserving intrinsic knowledge" is not directly validated.

- **Calibration set size not investigated**: The method uses 43,128 sequences from C4 for importance scoring. There is no analysis of sensitivity to calibration data size or composition, which is important for practical adoption where compute may be limited.

### Trivial

- The paper uses "self distillation" and "SDMPrune" interchangeably but cites Zhu & Shen (2025) without providing full details of how the self-distillation loss differs architecturally from the proposed entropy loss.

## Nice-to-Haves

- Evaluate on perplexity (e.g., WikiText-2, PTB) to directly measure distribution preservation.
- Analyze the relationship between pruning ratio and the resulting per-layer entropy changes — would adaptive, entropy-aware per-layer ratios improve performance further?
- Compare against a version that uses KL divergence between the original and pruned model's output distribution as the importance criterion, which is a more direct "distribution preservation" objective than entropy.
- Include a discussion of how the entropy criterion behaves on out-of-distribution calibration data.

## Novel Insights

The paper's key insight is that the importance scoring function in Taylor pruning does not need to be a supervised loss — an unsupervised, label-free information-theoretic quantity (entropy of the model's own predictions) can serve as a more faithful criterion for identifying which neurons contribute to the overall output distribution. This reframes pruning from "maintaining task-specific accuracy" to "maintaining distributional fidelity," which is a conceptually interesting shift. However, the practical novelty is somewhat limited because the only change from standard Taylor pruning is swapping the loss function, and the empirical gains are incremental.

## Suggestions

1. **Fix the data reporting in Table 3**: The duplicated rows for Qwen2.5-1.5B and Qwen3-1.7B SDMPrune need to be corrected and clearly explained.
2. **Correct the CE motivation**: Acknowledge that CE gradients do involve all vocabulary logits through softmax, and restate the motivation more precisely (e.g., "CE weights distributional changes by the one-hot target, while entropy weights all tokens equally").
3. **Add perplexity results**: Report perplexity on a held-out validation set (e.g., WikiText-2) for all pruned models to strengthen the claim of distribution preservation.
4. **Include additional baselines**: At minimum, compare against SparseGPT and Wanda in the no-fine-tuning setting (Table 6) to contextualize the method's relative effectiveness.

## Score and Decision

Score: 6  
Decision: Borderline Accept

The paper presents a clean, well-motivated idea with consistent empirical results. However, the contribution is incremental (swapping the criterion in an existing Taylor-pruning framework), the theoretical motivation contains an overstatement about cross-entropy, and there are data integrity concerns in Table 3 that need resolution. The paper would benefit from broader baseline comparisons and additional evaluation metrics (e.g., perplexity) to fully substantiate its claims.

MY FINAL SCORE: 6<score>6</score>
MY FINAL DECISION: Borderline Accept