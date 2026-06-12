## Summary

The paper proposes HFPrune, which replaces the standard one-hot cross entropy criterion in Taylor-based neuron importance evaluation with information entropy of the model's output distribution. This label-free criterion considers all potential predictions across the vocabulary rather than just the ground-truth token, enabling more faithful preservation of model behavior during MLP pruning. Experiments across LLaMA and Qwen models at multiple sparsity levels demonstrate consistent improvements over existing methods.

## Strengths

- **Clear and well-motivated problem formulation.** The paper identifies a concrete limitation of existing Taylor-based pruning—the reliance on one-hot cross entropy only measures importance relative to the ground-truth token—and proposes an elegant, simple fix. Figure 1 effectively illustrates the conceptual difference.

- **Substantial practical advantages over the closest competitor.** Compared to SDMPPrune, which also aims to capture holistic predictions but uses self-distillation, HFPrune is ~3× faster and uses ~31% less GPU memory (Table 5), while avoiding the zero-gradient initialization problem of self-distillation methods.

- **Comprehensive and thorough experimental evaluation.** The paper evaluates across 5 different models (LLaMA2-7B, LLaMA3.2-3.2B, LLaMA3.2-1.2B, Qwen2.5-1.5B, Qwen2.5-7B, Qwen3-1.7B), multiple pruning ratios (20%-40%), 10 zero-shot benchmarks, and includes practical latency/throughput measurements (Table 4), output distribution fidelity analysis (Table 7), and component-level ablations (Tables 6, 8). This level of evaluation is commendable.

- **Method simplicity.** The method requires only changing the criterion in the Taylor expansion from cross entropy to information entropy—a minimal modification that is easy to implement and adopt.

## Weaknesses

### Fatal

None.

### Major

- **The improvement margins are modest.** The core empirical claims rest on differences of 0.5-1.0 average accuracy points over SDMPrune (e.g., 59.0 vs 58.2 at 20% on LLaMA2-7B, 56.3 vs 55.6 at 30%). While consistent, these margins are small enough to fall within typical variance across random seeds, calibration samples, or fine-tuning runs. The paper does not report standard deviations or confidence intervals, making it difficult to assess whether these differences are statistically significant.

- **The claim that HFPrune "recovers and even exceeds" the original dense model (59.0 vs 58.3) requires scrutiny.** The improvement over the dense model is only 0.7 points after pruning 20% of parameters plus fine-tuning. This could be an artifact of the LaMini fine-tuning dataset benefiting smaller models, rather than a genuine pruning benefit. The paper does not discuss this possibility or evaluate the dense model after the same fine-tuning.

- **Limited evaluation scope.** All results are on zero-shot accuracy benchmarks. There is no evaluation on generation quality (e.g., perplexity), downstream task fine-tuning performance, or longer-form generation. For a method targeting LLMs, understanding the impact on text generation capabilities is essential.

### Minor

- **Table 3 appears to contain a data anomaly.** The Qwen2.5-7B (30% ratio, SDMPrune) row and the Qwen2.5-1.5B (20% ratio, SDMPrune) row share identical values, and the Qwen2.5-1.5B (20% ratio, HFPrune) row appears identical to Qwen3-1.7B (20% ratio, HFPrune). This may be a parser artifact or a genuine error that should be verified.

- **Single calibration dataset.** All experiments use C4 for calibration and LaMini for fine-tuning. The sensitivity to calibration data is not explored, which limits understanding of robustness.

- **Uniform sparsity across layers.** The method uses a fixed pruning ratio per MLP layer. The paper acknowledges that layer-specific entropy could be explored (Conclusion), but does not demonstrate this, missing an opportunity to strengthen results further.

### Trivial

- Minor typos in the text (e.g., "brief" instead of "brevity").

## Nice-to-Haves

- A comparison to KL-divergence from the original model's distribution as the criterion, which is another natural way to preserve the full output distribution without requiring a teacher.
- Perplexity evaluation on standard language modeling benchmarks.
- Analysis of how the entropy criterion changes importance rankings compared to cross-entropy (e.g., rank correlation).

## Novel Insights

The core observation—that replacing the scalar cross-entropy loss with the information entropy of the full output distribution provides a richer, label-free signal for Taylor-based importance evaluation—is genuinely useful. The paper correctly identifies that this avoids both the narrowness of one-hot cross entropy and the complexity/zero-gradient problem of self-distillation. However, the idea of using entropy as a pruning criterion is not entirely novel (as acknowledged in Related Work), and the specific application to Taylor-based neuron pruning in LLMs, while technically sound, represents an incremental rather than fundamental advance.

## Suggestions

- Report confidence intervals or standard deviations over multiple runs/calibration seeds to establish statistical significance of the reported improvements.
- Evaluate the dense model after the same fine-tuning to properly contextualize the "exceeds original" claim.
- Add perplexity evaluation on WikiText-2 or C4 to assess language modeling quality beyond zero-shot accuracy.

## Score and Decision

The paper presents a simple, well-motivated modification to Taylor-based pruning that is clearly explained and thoroughly evaluated. The practical efficiency advantages over self-distillation are genuine. However, the core improvements are modest and may not be statistically significant given the lack of variance reporting. The evaluation is comprehensive but limited to zero-shot accuracy, and the "exceeds dense model" claim needs more careful baselining. This is a solid incremental contribution that would benefit from stronger empirical evidence.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>