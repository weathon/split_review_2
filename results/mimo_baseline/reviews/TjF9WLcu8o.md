## Summary

The paper proposes Contrastive-Online-Meta (COM), a framework for dynamic adaptation of instruction-tuned CodeLLMs that combines contrastive pre-training, online meta-learning, and a dynamic memory buffer. The authors claim this approach mitigates catastrophic forgetting and handles noisy feedback during deployment by separating task-invariant representation learning from fast adaptation.

## Strengths

- **Relevant problem**: The paper addresses a genuine and important challenge—adapting CodeLLMs to streaming instruction-feedback data at deployment without catastrophic forgetting. This is a practical concern for real-world programming assistance systems.
- **Clear architectural decomposition**: The framework cleanly separates frozen base model parameters, a contrastive instruction encoder, an online meta-learner, and a memory buffer, which is a sensible design philosophy for balancing stability and plasticity.
- **Modular design**: The frozen base CodeLLM with trainable lightweight components (~5% of parameters) is an appealing and practical design choice that could integrate with existing models.

## Weaknesses

### Fatal

- **No experimental results are presented.** Section 5 describes experimental setup in detail (datasets, baselines, metrics, implementation) but contains zero result tables, figures, or numerical comparisons. Section 1 explicitly states "Experimental results with several programming benchmarks are presented in Section 5," yet Section 5 only contains setup and no results. Section 6 jumps to discussion without any empirical findings to discuss. The specific quantitative claims made in the introduction—"3-5x fewer updates than conventional meta-learning approaches" and "outperforming instruction-tuned baselines by 12-18% on unseen programming languages"—are completely unsupported by any presented data. Without results, the paper cannot support any of its claims.

### Major

- **Insufficient novelty.** The proposed framework is a straightforward combination of three well-established techniques (contrastive learning, meta-learning, and memory replay) with no clear technical innovation that goes beyond prior work. The contrastive pre-training, online meta-learning with regularization, and FIFO memory buffers are all standard approaches. The paper does not demonstrate why this particular combination produces emergent benefits beyond what each component achieves independently.
- **Questionable claims about dataset novelty.** The paper introduces "StreamCode" as a sequential benchmark but provides no details on how it was constructed, how task boundaries are defined, or how it differs from existing continual learning benchmarks for code. Similarly, "CodeAlpaca-20k" and "CrossLang-Eval" are cited but their relationship to existing publicly available benchmarks is unclear.

### Minor

- **Missing ablation study.** Given the framework has multiple components (contrastive pre-training, meta-learner, memory buffer, spectral normalization, projection head), an ablation study is essential to understand each component's contribution. This is absent.
- **Limited baselines.** The baseline selection covers some but not all relevant approaches. For instance, there is no comparison to elastic weight consolidation (EWC) variants, LoRA-based continual learning, or other adapter-based approaches that are standard in this space.

### Trivial

- **Section 8 disclosure.** The paper acknowledges LLM-assisted writing polish. While transparent, this may partially explain some garbled sentences in the text.

## Nice-to-Haves

- A clear theoretical motivation or convergence analysis for why the combination of contrastive and meta-learning objectives is mutually beneficial (the paper claims this but provides no proof).
- Analysis of sensitivity to key hyperparameters (buffer size, regularization strength λ, temperature τ).
- Discussion of computational overhead compared to simpler baselines during deployment.

## Novel Insights

None beyond the paper's own contributions. The paper's central thesis—that contrastive objectives and meta-learning are complementary for CodeLLM adaptation—is stated repeatedly but neither theoretically justified nor empirically validated in the presented content.

## Suggestions

- The authors must present actual experimental results with quantitative comparisons to baselines on all claimed metrics. This is the single most critical issue.
- Add an ablation study isolating the contribution of each framework component.
- Provide clearer technical novelty beyond combining existing techniques—e.g., a novel contrastive objective specifically designed for code instruction spaces, or a theoretically grounded mechanism for how contrastive pre-training regularizes meta-learning updates.

## Score and Decision

The paper addresses a relevant problem and proposes a reasonable architectural design, but it fundamentally fails to present any experimental evidence for its claims. The specific quantitative results cited in the introduction are absent from the paper body. Without empirical validation, the paper cannot be considered a complete contribution.

MY FINAL SCORE: <score>1</score>
MY FINAL DECISION: <decision>Reject</decision>