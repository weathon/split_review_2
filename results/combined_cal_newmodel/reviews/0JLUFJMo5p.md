## Summary

This paper proposes DTERM (Dynamic Task-Embedded Reward Machine), a framework that conditions reward-component weights on task embeddings via a hypernetwork for RL-based code generation. The high-level idea (dynamic reward weighting for different coding tasks like translation, repair, and completion) is well-motivated and the three-module architecture is clearly structured. However, the paper has fatal presentation flaws (a garbled conclusion containing hallucinated text from a different paper, placeholder citations) and severe experimental deficiencies (no specified base policy model, no reported variance, insufficient baselines, uninterpretable cross-task experiments, unevaluated components). These issues collectively prevent the paper from supporting its central claims.

## Strengths

- **The problem is well-motivated (Section 1, Section 3.2):** Fixed reward weighting in RL for code generation is a genuine limitation — different coding tasks (translation, repair, completion) place different relative importance on compilation correctness, functional correctness, style, and efficiency. The paper correctly identifies this gap.

- **The high-level architecture is sensibly structured (Section 4):** The three-module design (task embedding generator, hypernetwork weight generator, modular reward decomposer) is clearly laid out in Figure 1. The pipeline from task description to dynamic weights to reward computation is intuitive.

- **The paper attempts a specific design that goes beyond a simple learned linear combination (Sections 4.2–4.3):** While the core weighting in Equation 5 is a linear projection with softmax, the framework also includes FiLM modulation of sub-reward network features (Section 4.2) and prototype-based cross-attention (Section 4.3), showing some architectural ambition.

## Weaknesses

### Fatal

- **The conclusion section (lines 299–301) contains completely garbled, hallucinated text from a different paper:** "The Dual Selfular-Acting Machine (DSAM.Mouth Rachel) A new method for analyzing the dual selfular acting machine (DSAM), a generative text model architecture akin to one employed by ChatGPT." This is not a parser artifact but content from another context pasted into the conclusion. Combined with multiple "(?)" placeholder citations in the paper (lines 39, 47, 197), this indicates the paper was not finalized before submission, fundamentally undermining its readiness for peer review.

### Major

- **The base policy model being fine-tuned is never specified.** The paper mentions "CodeLLM pipelines" and PPO (line 201) but never identifies which language model serves as the policy. Without knowing whether the base model is a 125M-parameter CodeGPT or a 7B-parameter CodeLlama, the experimental setup is unreproducible and the numerical results cannot be contextualized.

- **No variance or uncertainty is reported anywhere in the experimental results.** The paper states "3 random seeds" (line 201), yet Table 1, Table 2, and Figure 2 all present only point estimates with no standard deviations, confidence intervals, or error bars. The claimed gains (e.g., 2.7 BLEU on summarization, 22.7 vs. 18.4 Pass@1) cannot be assessed for statistical significance.

- **The baseline comparison is insufficient to support the paper's claims.** (a) The Expert-Tuned baseline cites Rame et al. (2023) — Rewarded Soups — which studies interpolating weights fine-tuned on different reward models for RLHF alignment, not manually optimized code generation reward weights. The actual weights used are never specified. (b) No comparison is made to any actual RL-based code generation method such as CodeRL (Le et al., 2022), which the paper itself cites. (c) There is no baseline that learns separate per-task static weights, which would be needed to isolate whether the *dynamic* aspect specifically contributes versus simply having learned weights at all.

- **The cross-task generalization experiment (Figure 2) is uninterpretable.** Tasks are labeled "Task 1" through "Task 10" with zero description. The metric is "normalized reward values" with no statement of what normalization was applied or across what range. DTERM starts at 0.70 while Uniform starts at 0.28, suggesting the normalization is not anchored to an absolute scale. Without task definitions and metric clarity, this experiment provides no scientific evidence.

- **The multi-modal task embedding fusion mechanism (Section 4.4) is presented as part of DTERM but is never evaluated.** No experiment involves multi-modal tasks. This inflates the claimed contribution without evidence.

- **The meta-training procedure for prototypes (Section 4.3) is never described.** The paper states prototypes are "learned during meta-training on many different types of tasks" but never specifies how tasks are sampled, how prototypes are initialized, what the meta-training objective is, or how many prototypes are used (what is *m*?). The "meta-training loss" in Figure 4 is never defined mathematically.

### Minor

- **The "Reward Machine" framing is misleading.** The paper acknowledges (Section 3.5) that reward machines are finite state automata and that DTERM "differs in implementation," yet the name suggests a connection that does not exist — DTERM has no automaton structure, states, or transitions. This could mislead readers about the relationship to prior work.

### Trivial

None.

## Nice-to-Haves

- Comparing against learning fixed per-task weights separately to test whether the dynamic aspect adds anything beyond having learned weights.
- Reporting what the hypernetwork actually learns (e.g., do repair tasks weight compilation success more, as one would expect?).
- Hyperparameter sensitivity analysis (learning rate, hidden dimension, etc.).

## Removed Points

These points are flagged to be removed, treat them with caution:

- The harsh critic's claim that "Equation 5 reduces to a single learned linear layer with softmax" is overly narrow — the implementation details state the hypernetwork is a 3-layer MLP with hidden dimension 256 (line 201), and Sections 4.2–4.3 describe prototype-based cross-attention and FiLM modulation. The criticism is partially valid (Eq. 5 itself is a simple linear projection) but the paper describes a more complex architecture.
- Criticism about GradNorm being a "category error" is removed as speculative — balancing reward components in single-task RL is a plausible application of gradient normalization.
- Missing related works mentions: removed per instructions (cannot confirm from external sources).
- Formatting/style nitpicks and "unreleased" concerns: removed per instructions.
- Reproducibility nitpicks about code release: removed as not a standard acceptance criterion.
- Reviewer praise about the problem "being well-motivated" and having "sensible structure" — kept because they are specific and verifiable. Removed generic praise ("the paper targets an interesting question") as superficial.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Fix the garbled conclusion and all placeholder "(?)" citations before resubmission.
2. Specify the base policy model being fine-tuned.
3. Report standard deviations or confidence intervals from the claimed 3 random seeds.
4. Compare against at least one actual RL-for-code method (e.g., CodeRL) and against learning separate per-task static weights.
5. Define the cross-task generalization tasks concretely, specify the normalization, and report task-specific metrics.
6. Either evaluate the multi-modal fusion component or remove Section 4.4.
7. Describe the meta-training procedure explicitly (task sampling, prototype initialization and count, objective function).

## Score and Decision

**Calibration Anchors (all rounds):**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Uj0h13lVrR.md | 1.00 | R1 | No | Essentially incomprehensible; current paper has more structure |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/gwZ90hFSL2.md | 1.00 | R1 | No | Cross-lingual robots paper; different topic |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/5kMwiMnUip.md | 1.40 | R1 | No | LLM jailbreaking paper; different topic |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/OXIIFZqiiN.md | 1.50 | R2 | No | Patch analysis; incomplete presentation, similar tier |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/N581Nje6fH.md | 1.50 | R2 | No | Robotics; incomplete, similar tier |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/dsALpkd1OU.md | 1.67 | R2 | Yes | D2Coder; coherent writing, complete experiments; current paper is worse |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/N18Z2MkMEa.md | 3.00 | R1 | Yes | FALCON; similar topic (RL+code), specifies base models, coherent; current paper is notably worse |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/Q6HYM1EMu8.md | 3.00 | R1 | No | LARG2; language-based reward generation; better executed |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/CscKx97jBi.md | 3.00 | R1 | No | Code generation with feedback; coherent paper |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/zPPy79qKWe.md | 4.50 | R1 | Yes | RLEF; specifies models (Llama 3 8B/70B), open-source code; far more complete |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/vLqkCvjHRD.md | 4.75 | R1 | No | Coarse-tuning code models with RL; solid paper |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/lvDHfy169r.md | 5.75 | R1 | Yes | ProgressCounts; well-organized, thorough experiments |
| /home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/tUM39YTRxH.md | 7.00 | R1 | Yes | Text2Reward; polished, comprehensive evaluation |

**Bracket:** Round 1 placed the paper between 1.0 and 2.0, below FALCON (3.0). The paper's fatal flaw (garbled conclusion from another paper) and placeholder citations show it was not finalized. Compared to D2Coder (1.67), which has coherent writing and clear experimental framing, the current paper is weaker — it does not specify its base model, has an uninterpretable generalization experiment, and includes unevaluated components. The draft's most negative favorability items (fatal garbled conclusion at -1.13, uninterpretable cross-task experiment at -1.37, baseline citation issue at -0.56) collectively place the paper below the 1.67 anchor. However, it retains some coherent structure, keeping it above pure-gibberish papers (1.0).

**Final Score: 1.5, Decision: Reject.**

MY FINAL SCORE: <score>1.5</score>
MY FINAL DECISION: <decision>Reject</decision>