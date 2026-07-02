## Summary
This paper introduces a deletion-based probing framework to evaluate how faithfully LLMs depend on chain-of-thought (CoT) traces in physics problem solving. The authors intercept generated CoT scratchpads mid-generation, remove tokens under three strategies (end deletion, random deletion, and physics-aware deletion), and measure downstream effects on answer score, answer length, and lexical overlap between original and regenerated content. Evaluating three open-source models (Phi-4, Qwen-A3B, Magistral) on three physics benchmarks (UG Physics, PhysReason, PhyBench), they find that accuracy remains stable under moderate deletions (40–60%) while answer length increases — a compensatory pattern they term **cramming**. Lexical overlap analysis using Jaccard similarity and Manhattan distance shows that deleted content often reappears in final answers, but the pattern varies across deletion strategies, suggesting heuristic rather than systematic reasoning dependence.

The paper's core strength is the systematic, cross-strategy deletion methodology applied to a structured domain where quantitative overlap analysis is feasible. However, there are significant concerns about the reliability of the primary evaluation metric (LLM-as-judge scoring without human calibration), the construct validity of "faithfulness" as operationalized (external deletion sensitivity vs. internal reasoning faithfulness), and the conclusiveness of the evidence for cramming (lack of content analysis distinguishing physics reconstruction from generic hedging). The lexical overlap metrics capture surface-level token reuse rather than semantic reconstruction, weakening the central claim about "surface-level agreement without genuine reasoning dependence."

## Strengths
1. **Well-motivated research question.** The paper addresses a timely and important question: whether CoT traces are genuinely necessary for LLM reasoning or serve as post-hoc justifications. This question has direct implications for interpretability, evaluation, and system design in scientific AI applications.

2. **Systematic multi-strategy deletion framework.** Rather than a single manipulation, the paper compares three deletion strategies (end, random, physics-aware) across multiple deletion fractions (0–100%). This provides a richer characterization of model behavior than a binary intact/deleted comparison. The cross-strategy comparison reveals qualitatively different recovery patterns, strengthening the descriptive findings.

3. **Structured domain choice.** Using physics as a testbed is a principled methodological choice: the formal vocabulary (equations, units, constant names) enables quantitative overlap analysis that would be difficult in open-ended reasoning tasks. The domain specificity is leveraged for the physics-aware deletion condition and for interpreting the overlap metrics.

4. **Transparency about limitations.** Section 4.4 candidly acknowledges several limitations: the scope to physics and three models, the lack of latent representation analysis, and the need for broader robustness testing. This demonstrates methodological awareness and helps bound the claims appropriately.

5. **Empirical phenomenon discovery.** The identification and naming of "cramming" — increased answer length under CoT deletion — is a useful behavioral characterization that may inform future work on CoT compression, early stopping, and faithful reasoning evaluation. The X-shaped pattern (CoT length decreases while answer length increases) is visually clear and consistently observed across models and deletion strategies.

6. **Reproducibility-oriented design.** The use of open-source models and explicit sampling parameters (temperature, top-p) supports reproducibility. The paper commits to providing prompt templates in the appendix, which is good practice.

## Weaknesses
The following weaknesses are ordered by severity (highest impact first).

### W1. LLM-as-Judge scoring without human calibration undermines the primary evaluation metric (Major)

The paper's primary evaluation metric — **Score** (0–1 scalar) — is computed by Claude-4 Sonnet as an automated judge, assessing correctness, derivation accuracy, logic, formatting, and clarity. This introduces several unaddressed validity threats:

- **No reliability evidence:** No inter-rater agreement, test-retest reliability, or calibration against human expert judges is reported. It is unknown whether the judge's scoring is consistent or systematically favors certain answer styles.
- **Circularity risk with physics-aware deletion:** Claude-4 Sonnet is also used to identify physics-related tokens in the physics-aware deletion condition (Section 3.2). If Claude-4 has systematic biases in physics content identification, the results of the physics-aware deletion experiments could reflect those biases rather than genuine model behavior.
- **Conflated criteria:** The single Score combines correctness, derivation accuracy, logic, formatting, and clarity — conflating content quality with stylistic presentation. A model could receive a moderate score for poor formatting even when the physics is entirely correct.

**Required action:** Report a human-annotation calibration study on at least 100 samples. Separate correctness from formatting sub-scores. Use exact-match accuracy on final numerical answers as a primary metric, with the LLM-as-judge score as secondary. If expert human evaluation is unavailable, at minimum acknowledge this limitation explicitly and discuss potential bias directions.

### W2. Construct validity gap: "Faithfulness" operationalized as deletion sensitivity rather than internal computation faithfulness (Major)

The paper defines faithfulness as "the extent to which the scratchpad explicitly reflects the internal computations that lead to the model's final prediction" (Section 1), but the deletion experiments measure something different: the sensitivity of the final answer to *previously generated text being removed from the context*. This is closer to **input sensitivity** or **context dependence** than to faithfulness of internal computation.

The distinction matters: a model could be highly dependent on its own CoT text (high deletion sensitivity) while that text is still unfaithful to internal reasoning (e.g., the model produces a plausible-looking derivation that doesn't match its actual decision process). Conversely, a model could have low deletion sensitivity because it stores reasoning in its internal representations, not because its CoT is unfaithful.

**Required action:** Explicitly reframe the paper's contribution as measuring "functional dependence of answers on externally recorded CoT traces" rather than "faithfulness of internal reasoning." Alternatively, add a mechanistic analysis (e.g., probing hidden states during CoT generation) to connect deletion sensitivity to internal computation.

### W3. Cramming evidence lacks content analysis confirming physics reconstruction (Major)

The paper identifies cramming as increased final answer length under CoT deletion, interpreted as attempted reconstruction of missing reasoning. However:

- **No content analysis:** The extra length could consist of hedging ("I'm not sure but..."), repetition of preserved tokens, or generic filler rather than genuine physics reconstruction. The paper does not analyze what fraction of added characters are physics-relevant.
- **No statistical significance testing:** The thresholds at which cramming "emerges" (40%, 60%, 70-80% across strategies) are read from figures without statistical tests (e.g., comparing length at each deletion level to the full-CoT baseline via paired test with multiple-testing correction).
- **Multiple mechanisms possible:** Increased length could arise from template filling, self-correction loops, or increased uncertainty behavior, not necessarily from domain-specific reconstruction of deleted physics content.

**Required action:** Perform content analysis on at least 100 answer pairs (full CoT vs. deletion condition), categorizing additional characters into physics-relevant (equations, values, units), hedging, repetition, and other. Report a significance test for length increase at each deletion threshold (e.g., Wilcoxon signed-rank test, Bonferroni-corrected).

### W4. Information overlap metrics capture lexical not semantic recovery (Major)

The paper uses Jaccard similarity and Manhattan distance on bag-of-words token sets to measure whether deleted content reappears in final answers. These metrics have fundamental limitations for the intended inference:

- **High lexical overlap ≠ faithful reconstruction:** Common physics vocabulary (e.g., "force," "mass," "equation," "calculate") will co-occur regardless of whether the model faithfully reproduces deleted reasoning or generates an alternative solution path.
- **No baseline calibration:** The paper does not report overlap scores for *unrelated* CoT-answer pairs, so the reader cannot calibrate whether the observed overlap values are high or low relative to chance.
- **Missed opportunity for semantic matching:** Given the structured nature of physics, the paper could have used equation-level matching (parsing "F = ma" as a semantic triple), numerical value tracking, or step-order alignment — all of which would provide stronger evidence for or against faithful recovery.

**Required action:** Add equation-level semantic overlap as a third metric. Report baseline overlap values for random CoT-answer pairs to calibrate the metrics. Acknowledge the lexical/semantic gap explicitly as a limitation.

### W5. Calibration study underspecified and potentially insufficient for deletion conditions (Moderate)

The calibration study (Section 3.1) claims that "approximately 5 prompts are sufficient to reduce the relative error bar below 10%" based on bootstrapped results over 50 UG-Physics questions. Several issues:

- **Figure 8 missing:** The calibration results reference Figure 8, which is not present in the available manuscript. The reader cannot verify the convergence claim.
- **Bootstrap methodology not specified:** The resampling scheme (number of iterations, CI type, what "relative error bar" means operationally) is not described.
- **Applicability to deletion conditions:** Calibration was performed under full-reasoning prompting, but the deletion experiments introduce additional variance (especially at high deletion fractions). There is no evidence that 5 prompts suffice when 60-80% of CoT is deleted, where output variance is likely higher.

**Required action:** Show the calibration figure, specify the bootstrap methodology precisely, and validate that 5 prompts remain sufficient under deletion conditions (at minimum, report CI widths at 0%, 40%, and 80% deletion for one model-dataset pair).

### W6. Practical implications overreach the experimental evidence (Moderate)

Section 4.3 suggests "early stopping of CoT generation may provide a cost-effective way to save tokens" and that prompts "could be redesigned to elicit more concise yet effective reasoning traces." These recommendations:

- **Are not tested:** The paper tested deletion of *existing* tokens, not prevention of generation. Early stopping involves different dynamics (model may plan ahead differently, may not generate the content at all).
- **Lack cost evidence:** No compute, latency, or token savings measurements are reported to support the "cost-effective" claim.
- **Contradiction risk:** If models cram (reconstruct content in the answer), early stopping could simply shift tokens from CoT to answer, potentially increasing rather than decreasing total length.

**Required action:** Qualify all practical recommendations as speculative and requiring dedicated validation. Remove or weaken the "cost-effective" claim unless supported by direct measurements.

### W7. AI-for-Science framing is inflated relative to the actual study scope (Minor)

The paper repeatedly invokes "AI for science" (abstract, introduction, conclusion, limitations) as the broader context, claiming the findings have "direct implications for AI-for-Science." However:

- The study evaluates three general-purpose LLMs on exam-style physics benchmarks — not on scientific discovery, hypothesis generation, experimental design, or any real scientific workflow.
- No domain-specialized scientific foundation model is tested.
- The evaluation metrics (answer accuracy, lexical overlap) are standard NLP benchmarks, not scientific reasoning metrics.

**Required action:** Narrow the framing to "evaluation of reasoning faithfulness in structured scientific domains" or "physics problem solving." Reserve "AI for science" claims for studies that actually test scientific workflows or domain-specialized models.

### W8. Related Work is descriptive rather than argumentative (Minor)

The Related Work section (Section 6) lists models and prior faithfulness work without organizing them along comparison axes relevant to the paper's contribution. It does not explicitly state how the paper's deletion-based probing differs from or improves upon prior faithfulness evaluation methods (e.g., Lanham et al., Turpin et al.). The section ends with the generic statement that "systematic evaluation of faithfulness remains an open challenge" without positioning the paper's framework as a specific response to an identifiable gap.

**Required action:** Restructure the Related Work to compare prior faithfulness methods along explicit dimensions (e.g., what is manipulated, what is measured, whether metrics are quantitative or qualitative) and state clearly what the present paper adds.

### W9. Missing benchmark statistics and difficulty validation (Minor)

The benchmark descriptions (Section 2.1) are qualitative ("easiest," "intermediate," "hardest") without key statistics: problem counts for UG Physics and PhyBench, topic distributions, answer format specifications, or difficulty validation (e.g., baseline model scores or human performance). The UG Physics reference (Xu et al., 2025) is not included in the reference list, making it untraceable.

**Required action:** Provide full dataset statistics, validate the difficulty ordering with baseline results, and ensure all benchmark references are complete.

### Novelty and Comparison Assessment (Deferred)

Due to Retrieval-Disabled Mode (external literature search unavailable in this run), novelty and comparison judgments are explicitly deferred. The paper's claim of introducing "a systematic deletion framework" as a new methodology merits cautious qualification, as prior faithfulness evaluation work (Lanham et al., 2023; Turpin et al., 2023) already manipulates CoT traces. The specific contribution of applying deletion probing to physics with structured overlap metrics is plausibly novel, but a definitive verdict requires manual literature verification.

## Score
**Final Score: 5/10**

**Rationale:** The paper addresses a timely and well-motivated research question — whether LLMs genuinely depend on CoT traces for physics reasoning — with a systematic multi-strategy deletion framework applied to a structured domain. The identification of the "cramming" pattern (increased answer length under CoT deletion) is an interesting empirical observation. However, three major weaknesses substantially reduce confidence in the core claims: (1) the primary evaluation metric (LLM-as-judge Score) lacks any human calibration or reliability evidence; (2) the central construct of "faithfulness" is operationalized as external deletion sensitivity rather than internal reasoning faithfulness, creating a gap between claims and evidence; and (3) the cramming phenomenon is not supported by content analysis that would distinguish genuine physics reconstruction from generic hedging or repetition. Additionally, the lexical overlap metrics (Jaccard, Manhattan) capture surface-level token co-occurrence rather than semantic reconstruction, weakening the analysis of reasoning faithfulness. These issues are fixable with additional experiments and more cautious framing, but in their current form they limit the paper's contribution to a suggestive behavioral characterization rather than a conclusive evaluation of reasoning faithfulness.