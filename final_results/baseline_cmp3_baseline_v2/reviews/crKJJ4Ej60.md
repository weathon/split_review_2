## Summary

The paper proposes **Copy-Paste**, a generation paradigm that mitigates contextual unfaithfulness hallucinations in RAG by explicitly maximizing lexical copying from the provided context. The authors observe an inverse correlation between copying degree and hallucination density on RAGTruth, and instantiate Copy-Paste via a two-stage pipeline: (1) Copy-Paste-Prompting methods (CP-Order, CP-Link, CP-Refine) generate high-copying responses through hard/soft constraints, and (2) CopyPasteLLM is trained via DPO on preference data automatically constructed from those responses. The resulting model achieves strong performance on FaithEval, ConFiQA, and PubMedQA using only 365 query-context pairs, substantially outperforming baselines. The authors also propose a Context-Parameter Copying Capturing algorithm for token-level interpretability of knowledge source reliance.

## Strengths

- **Simple and intuitive approach**: The core idea—forcing the model to copy directly from context rather than paraphrase—is clean, well-motivated, and directly addresses the source of contextual faithfulness hallucinations. The observation of inverse correlation between copying degree and hallucination provides a solid empirical foundation.

- **Strong empirical performance with remarkable data efficiency**: CopyPasteLLM achieves 12.2%–24.5% accuracy improvements on FaithEval counterfactual subsets using only 365 training samples, which is 50× smaller than Context-DPO (18,000 samples). These gains are consistent across three backbones (LLaMA-3, Mistral, LLaMA-3.1) and multiple evaluation metrics.

- **Comprehensive evaluation across diverse scenarios**: The paper evaluates both counterfactual (FaithEval, ConFiQA) and non-counterfactual settings (PubMedQA, ConFiQA original), uses multiple faithfulness metrics (MiniCheck, AlignScore, hallucination density), and ablates the prompting strategies thoroughly. This provides a convincing picture of the method's general applicability.

- **Novel interpretability tool**: Context-Parameter Copying Capturing extends prior work (KTC) to full Chain-of-Thought trajectories, enabling position-aware analysis of contextual vs. parametric knowledge usage. The visualization of hidden state distributions and logit power patterns offers mechanistic insight into why CopyPasteLLM works—appearing to recalibrate parametric confidence rather than enhance contextual representations.

## Weaknesses

### Major

1. **Fairness of baseline comparison is questionable**: CopyPasteLLM's training data (365 query-context pairs) are drawn from the same distribution as the test sets (e.g., FaithEval), while strong baselines like Context-DPO are trained on different data (RAGTruth) with 18,000 samples. The in-distribution training advantage could inflate CopyPasteLLM's relative performance. The paper does not discuss domain shift or control for this. A fairer comparison would involve training Context-DPO on the same 365 FaithEval samples (or training CopyPasteLLM on RAGTruth) to isolate data efficiency claims.

2. **Data efficiency claim is overstated**: Although only 365 initial query-context pairs are used, each pair generates multiple preference pairs (approximately five per sample, per Section 3.2), meaning the DPO training set is substantially larger than 365. The effective number of training examples is not reported, making the "365" baseline requirement less impressive when compared to other methods that report total training samples (e.g., Context-DPO with 18,000 single responses). A clear breakdown of actual DPO training pairs used is needed.

3. **Comparison with GPT-4o is insufficiently documented**: The paper states that CopyPasteLLM "remarkably outperforms GPT-4o's reported 47.5%" on FaithEval, but the source of this number is deferred to Appendix Table 6 (not visible in the provided content). It is unclear whether the GPT-4o evaluation used the same test split, same prompting, or same metrics. Without transparent reporting, this claim lacks credibility and should be removed or properly contextualized.

4. **Context-Parameter Copying Capturing lacks validation**: The algorithm distinguishes "contextual" vs. "parametric" tokens by comparing with/without context runs, but this heuristic is not validated against ground-truth knowledge sources. There is no quantitative measure (e.g., precision/recall against human annotation or known fact conflicts) to confirm that "parametric tokens" actually reflect memorized knowledge. The mechanistic conclusions (recalibration of parametric confidence) are interesting but remain speculative without such validation.

### Minor

- The three prompting strategies (CP-Order, CP-Link, CP-Refine) are presented as complementary but their design rationale is heuristic. The paper does not provide principled guidelines for choosing among them; in practice CP-Refine appears best overall but this is only empirically determined.

- The hallucination tournament (Elo ranking) step in Stage 2 is described but not ablated. It is unclear how much of the final improvement comes from the prompting strategies vs. the preference ranking and stamping steps.

- The training data size of 365 is specific to this experimental setup; it is unclear how sensitive the method is to this number or whether it generalizes to other domains with more or fewer samples.

### Trivial

- In Table 1, the Hit Rate for CopyPasteLLM on FaithEval (37.2% on LLaMA-3-8B) is only marginally better than Context-DPO (36.7%) and worse than several baselines on ConFiQA subsets. The paper focuses on Accuracy but does not explain why Hit Rate (exact match) improvements are modest.

- The "contextual knowledge representations nearly co-distributed" observation (Figure 4) is based on UMAP, which is sensitive to hyperparameters. The paper does not discuss stability of this visualization.

## Nice-to-Haves

- A controlled experiment where both CopyPasteLLM and Context-DPO are trained on the same 365 samples from the same distribution would strengthen data efficiency claims.
- Validate Context-Parameter Copying Capturing against a known benchmark (e.g., using synthetic contexts with inserted false facts) to confirm that "parametric tokens" truly correspond to internal knowledge.
- Ablate the ELO hallucination tournament and stamping steps separately to understand their contribution.
- Report the actual number of DPO preference pairs generated from the 365 base samples.

## Novel Insights

The paper provides a clear demonstration that promoting lexical copying from context via preference optimization is an effective and data-efficient strategy for RAG faithfulness. More interestingly, the mechanistic analysis (logit power and hidden state distribution) suggests that the improvement comes from *suppressing* the model's confidence in its parametric knowledge rather than enhancing contextual feature extraction. This reframes the hallucination problem as one of over-reliance on internal priors, which could generalize to other alignment strategies. The positional analysis showing earlier contextual engagement in CopyPasteLLM is also a novel finding.

## Suggestions

1. Address the training data distribution issue explicitly: either run a controlled experiment with matched training data or provide a clear discussion of how distribution overlap might affect relative performance.
2. Report the effective number of DPO preference pairs (rather than just the seed query-context pairs) and compare with baseline methods on an apples-to-apples basis.
3. Provide validation of Context-Parameter Copying Capturing, perhaps by manually annotating a small set of tokens as contextual/parametric and measuring agreement.
4. Disentangle the contributions of prompting, ranking, and stamping through ablation.

## Score and Decision

Score: 5.0 / 10

This paper tackles an important problem with a simple and well-motivated approach, and it provides extensive empirical evidence of strong performance. However, concerns about the fairness of baseline comparisons, potential overstatement of data efficiency, and insufficient validation of the interpretability claims prevent me from recommending acceptance in its current form. The core idea has merit, but the experimental framing needs to be tightened to convincingly demonstrate that the gains are due to the proposed method rather than unaccounted distribution advantages.

MY FINAL SCORE: 5score</score>
MY FINAL DECISION: borderline reject</decision>