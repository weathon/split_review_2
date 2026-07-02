Now I have verified all claims. Let me produce the final consolidated review.

## Summary

This paper identifies and formalizes a practical, under-explored problem in multi-modal entity alignment (MMEA) — Dual-level Noisy Correspondence (DNC), where misalignments exist in both intra-entity (entity-attribute) and inter-graph (entity-entity and attribute-attribute) correspondences. The authors propose RULE, which estimates correspondence reliability via a two-fold principle (uncertainty + consensus), divides pairs into three subsets, and applies tailored robust loss functions during training and an MLLM-based reasoning module at test time. Experiments on five benchmarks with seven baselines under three noise levels show consistent improvements.

## Strengths

- **Well-motivated problem identification.** The paper clearly identifies and formalizes DNC — a real problem in MMEA where real-world benchmarks contain substantial noise (e.g., over 50% in ICEWS). The concrete examples (e.g., "Elvis Tsui" image associated with "Jason Momoa") make the two noise types tangible, and the bar charts in Fig. 1(b) demonstrate that both intra-entity and inter-graph noise degrade existing methods.

- **Theoretically motivated two-fold principle.** Theorem 1 (low uncertainty does not imply correct alignment) is a genuine and non-trivial insight. The scatter plot in Fig. 4 validates that the three subsets ($S_U$, $S_I$, $S_C$) are empirically separable along uncertainty and consensus, supporting the design of separate loss strategies for each subset.

- **Strong and systematic empirical results, especially on the harder setting.** On the Non-name protocol (which excludes name attributes and cannot rely on string matching), RULE outperforms all 7 baselines by large margins: e.g., 64.2% vs. 52.5% H@1 (MEAformer) on ICEWS-WIKI under inherent DNC, and 58.2% vs. 43.9% (HHREA) under 50% injected noise. The evaluation spans 5 datasets, 3 noise levels (inherent, 20%, 50%), and two protocols.

- **Clean ablation isolating contributions.** Table 3 shows that training-time components (DRL + DRF) drive the bulk of improvement (w/o DRL: 31.6 → Default: 58.2 on Non-name), while the test-time TTR module adds a smaller but meaningful increment (w/o TTR: 56.5 → Default: 58.2). This correctly attributes credit to the core technical contributions.

## Weaknesses

### Fatal
None.

### Major

- **No variance or statistical significance reported for any result.** All numbers in Tables 1–3 are single points with no standard deviation, no mention of multiple seeds, and no statement about whether results are averaged across runs. This is especially problematic in two situations: (i) the All-attributes setting (Table 2), where many methods operate above 95% H@1 and margins between them are often 1–3 points (e.g., RULE 98.8% vs. MEAformer 97.0% under inherent DNC); (ii) the ablation (Table 3), where "MLLM Enhance" (97.6%) vs. "Default" (97.7%) is a 0.1 point difference. Given that training involves stochastic neural network optimization and the test-time module uses an MLLM (Qwen2.5-VL-72B) that may exhibit non-deterministic behavior, variance estimates are needed to assess whether reported gains are reliable. The large margins on the Non-name setting (11–14 points) mitigate this concern somewhat, but the complete absence of any variance reporting weakens the empirical case.

### Minor

- **Asymmetric comparison created by the MLLM test-time module.** RULE's test-time component uses Qwen2.5-VL-72B, a 72-billion-parameter vision-language model, to re-rank candidates. None of the 7 baselines have access to an equivalent module. The paper states "For fair comparisons, we adopt the same backbone (i.e., CLIP) for all baselines and our method" — but this refers only to the feature extraction backbone, not the test-time reasoning. The ablation (Table 3) partially addresses this: w/o TTR achieves 56.5 H@1 on Non-name vs. Default's 58.2, showing training-time components are the main driver. However, adding an "MLLM-enhanced baseline" (applying the same TTR pipeline to the best baseline's outputs) would substantially strengthen the comparative claims. The gap between "Baseline + MLLM" and "RULE (Default)" would cleanly separate the training-time contribution from the MLLM's contribution.

- **Greedy correspondence estimation has unresolved theoretical gaps.** The greedy attribute selection (Section 2.2.2, Eqs. 6–7) estimates the correct correspondence $y_i$ by computing similarity scores and selecting attributes with positive marginal contribution. Three issues arise: (1) The value function $v(\pi) = \max(\frac{1}{|\pi|} \sum_{j \in \pi} s_i^j)$ is notationally ambiguous — the max is implicitly over candidate entities but this is not stated. (2) The initial subset size $\lfloor M/2 + 1 \rfloor$ (when $M \geq 3$) is presented without justification, and the paper does not specify the behavior when $M < 3$ (which matters since MMEA datasets typically have 2–3 modalities). (3) The similarity scores $s_i^m$ come from encoders trained on data that may contain entity-attribute noise, creating a potential bootstrapping problem. The paper acknowledges the estimation is needed because $y_i$ is unavailable during inference, but does not discuss when the estimation could fail (e.g., at high noise levels where all attributes are corrupted). The empirical results suggest the strategy works in practice, but the paper's reasoning is incomplete.

- **Missing standard reproducibility details in the main text.** The paper reports hyperparameters $\lambda=10^{-4}$, $\beta=0.3$, $\tau=0.07$, $\gamma=0.5$, but does not mention the optimizer, learning rate, learning rate schedule, weight decay, batch size, number of training epochs, or hardware used. Some of these may appear in the (stripped) appendix, but the main text should at minimum specify these basic training details or provide a clear cross-reference to where they appear.

### Trivial

- **Hard boundary in pair exclusion.** The indicator function $\mathbb{I}(i \notin S_U)$ in Eq. 11 applies a hard threshold: pairs on either side of $\beta_u$ are treated completely differently (one excluded, the other included). This is a standard design choice, but a brief discussion of why a soft weighting scheme was not used would strengthen the presentation.

## Nice-to-Haves

- Add an "MLLM-enhanced baseline" to the comparison tables (e.g., apply the TTR procedure using the same Qwen2.5-VL-72B to PMF's or MEAformer's outputs) to separate the MLLM contribution from the training-time design.
- Compare the DST-based uncertainty estimate against a simpler alternative (e.g., entropy over similarity scores) to justify the added complexity.
- Validate the greedy correspondence estimation (Section 2.2.2) with a controlled experiment reporting precision/recall of estimated $\hat{y}_i$ vs. ground-truth $y_i$ across noise levels.
- Conduct an ablation injecting each noise type (entity-entity, entity-attribute, attribute-attribute) independently to reveal which noise type is most damaging and which RULE component helps for each.
- Include the CoT prompt template used for Qwen2.5-VL-72B and report per-query latency and total test-time cost.

## Removed Points

These points from the input review were removed with justification:

1. **"Over 50% in ICEWS benchmarks belongs in the main text"** — the statistic already appears in the main text (line 34: "According to the statistics in Appendix B, real-world benchmarks always contain numerous NC (e.g., over 50% in ICEWS benchmarks)"). The criticism is factually wrong. **Removed.**

2. **"Fig. 1(b) source unclear (which dataset and noise level)"** — Fig. 1(b) is a conceptual illustration to build intuition, not a formal experiment. The paper's caption describes the qualitative comparison ("Ours vs. Concat under four conditions"). **Removed as misreading of figure purpose.**

3. **"DBP15K_GEN rendering artifact"** — the reviewer correctly identifies this as a parser artifact (the underlying paper uses ZH-EN, JA-EN, FR-EN). Since it is a parser issue, not an author error, it is removed. **Removed per hard rule on formatting artifacts.**

4. **"DST uncertainty is heavy / should compare with simpler alternatives"** — this is a design choice and a potential ablation, not a weakness. Moved to Nice-to-Haves.

5. **"Hard thresholding should be soft weighting"** — this is a design preference. The paper's choice is standard and reasonable. Moved to Trivial/Nice-to-Haves.

6. **"Why some baselines robust in All-attributes but not Non-name"** — this is a discussion point, not a weakness. The paper implicitly addresses it (name attributes are a strong signal). **Removed.**

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report all main results (Tables 1–3) as mean ± std over at least 3 random seeds. This is the single most impactful addition the authors can make.
2. Add an MLLM-enhanced baseline: apply the same TTR module (with the same Qwen2.5-VL-72B) to the outputs of the strongest baseline (e.g., PMF or MEAformer) and report results.
3. Clarify the notation in Section 2.2.2: state explicitly that the max in $v(\pi)$ is taken over candidate entities. Specify the handling of $M < 3$ cases.
4. Add a short discussion of potential failure cases for the greedy estimation strategy and/or provide empirical precision/recall of estimated $\hat{y}_i$ against ground truth.

## Score and Decision

The paper identifies a genuine, practically important problem (DNC) and proposes a well-motivated, multi-component solution (RULE). The empirical evaluation is broad and the results on the harder Non-name setting are consistently strong. The main weaknesses are the complete absence of variance reporting and the asymmetric MLLM comparison, which weaken but do not invalidate the paper's claims. The core technical ideas — the two-fold reliability principle, the pair division, and the tailored robust losses — are novel, sound, and supported by ablation. With variance reporting and an MLLM-enhanced baseline added, the paper would be substantially strengthened.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>