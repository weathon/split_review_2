## Summary
This paper proposes **Steady Thought (ST)**, a thought-level preference optimization framework to mitigate "under-thinking" in Large Reasoning Models (LRMs)—the tendency of models to abandon promising reasoning thoughts prematurely. ST operates in three stages: (1) **Thought Segmentation**, which partitions model responses into thought units using entropy-based detection; (2) **Thought Completion**, which generates forced completions of each thought under logit suppression of switch-trigger words (e.g., "wait", "alternatively"); and (3) **Fine-Grained Preference Optimization (STPO)**, which treats the forced correct completion as preferred and the original switch-heavy continuation as dispreferred, using a SimPO-inspired length-normalized objective.

Experiments across three model families (DeepSeek-R1-Distill-Qwen 1.5B/14B, Qwen3-8B) and four benchmarks (MATH500, AIME2024, GSM8K, LiveCode) show that ST reduces output length by 17.3–25.5% while maintaining or slightly improving accuracy (overall gains of +1.9% to +3.12%). On the out-of-distribution LiveCode benchmark, ST shows positive transfer with accuracy improvements of 4.2–5.3%.

The paper addresses a timely problem in efficient LLM reasoning and proposes a clean, well-motivated framework. However, the empirical validation has notable gaps: no statistical significance testing, missing variance estimates, unverified central claims about preserved exploration ability, and a distribution mismatch between training (logit-suppressed completions) and inference (unsuppressed decoding). These issues limit the strength of the conclusions currently drawn.

## Strengths
1. **Well-motivated problem framing.** The paper identifies a genuine and practically important limitation of current LRMs: excessive thought switching that wastes computation without commensurate accuracy gains. The "under-thinking" concept is clearly defined and supported by preliminary evidence (Figures 1a/1b showing early correct thoughts being abandoned).

2. **Clean, principled method design.** The three-stage pipeline (Segmentation → Completion → Preference Optimization) is logically coherent and each stage addresses a specific sub-problem. The use of SimPO's length-normalized objective at the thought level is a natural adaptation that addresses the known length-bias issue in DPO, which is particularly relevant given the asymmetric lengths of chosen (short forced completions) vs. rejected (long switch-heavy trajectories).

3. **Consistent and meaningful empirical trends.** Across three model families and four datasets, ST consistently reduces output length (17.3–25.5%) while maintaining or slightly improving accuracy. The positive transfer to the out-of-distribution LiveCode benchmark (accuracy improvements of 4.2–5.3%) is particularly noteworthy, as it suggests the method learns a generalizable pattern of thought management rather than simple task-specific memorization.

4. **Comprehensive ablation studies.** The paper includes thoughtful ablation analyses on entropy threshold sensitivity (Section 4.4.3), comparison of training methods (SFT vs. DPO vs. STPO, Section 4.4.4), and analysis of in-depth exploration and switching ability (Sections 4.4.1-4.4.2). These provide useful insights into the method's behavior and design choices.

5. **Reproducibility-oriented details.** The paper specifies training data source (omni-math), baseline methods, evaluation datasets, and averaging procedures (8 runs for AIME, 2 for LiveCode), providing a reasonable starting point for reproducing the main results.

## Weaknesses
### Major Weaknesses

**W1. Unsubstantiated causal claim about commitment vs. recognition (Page 1 - Introduction, Paragraph 2).**
The paper states that under-thinking "roots from the lack of ability to recognize and commit to promising reasoning trajectories," but does not distinguish between two distinct deficits: (a) failure to recognize a promising thought, and (b) failure to commit to it once recognized. The entire ST framework assumes the deficit is in commitment (Stage 3 trains commitment), but the "promising thought" is identified externally via forced completion + answer checking, not by the model's own recognition. If the model cannot reliably recognize promising thoughts during online generation, training it to commit to externally-selected thoughts may not transfer to inference. This conflation weakens the foundational motivation. **Fix:** Acknowledge the recognition-commitment distinction explicitly. Add a controlled experiment that measures whether ST improves commitment when the model can be verified to have recognized a promising thought (e.g., by measuring switching behavior after thoughts with high model confidence).

**W2. Missing statistical significance and variance reporting (Page 5 - Main Results, Table 1).**
Accuracy improvements are modest (1.9–3.12% overall) and reported without confidence intervals, standard deviations, or significance tests. For the 1.5B model on MATH500, the gain is 2.4 percentage points (82.0 → 84.4), which could easily be within noise range. The "average of eight test runs for AIME" is mentioned but the variance across those runs is not reported. Without statistical rigor, readers cannot assess whether ST's accuracy improvements are reliable. **Fix:** Report mean ± std for all metrics across all runs. Include a paired significance test (e.g., bootstrap or Wilcoxon) comparing ST against the vanilla baseline for each dataset-model combination.

**W3. Central claim of "preserved exploration ability" is unverified (Page 2 - Introduction, last paragraph; Page 1 - Method, Section 3.3).**
The paper's key differentiator from prior suppression methods is that ST "preserves the ability to explore necessary alternatives." However, no experiment tests whether the ST-trained model can still switch thoughts when the current trajectory is genuinely unpromising. The experiments only show overall accuracy and efficiency, which could be achieved by a model that simply commits to the first thought on every problem (including incorrect ones). **Fix:** Design a targeted "unpromising-start" experiment: force the model to begin with an incorrect reasoning prefix (by prompting or by inserting an incorrect thought), then measure whether the ST model switches to a correct path more or less frequently than the baseline. This directly tests the claimed preservation of exploration.

**W4. Distribution mismatch in preference optimization (Page 3 - Thought Completion; Page 4 - STPO Loss).**
The chosen trajectory $T_i'$ is generated under logit suppression of switch-trigger words, while the rejected trajectory $(T_{i+1},...,T_n)$ is the model's natural output. The STPO loss then optimizes $\pi_\theta$ to prefer the suppressed-decoding completion over the natural one, conditioned on a context $T_i$ that was itself generated by the base model (not the current policy). This creates a distribution mismatch: the model is trained to favor outputs from a different decoding distribution than what it will use at inference time. **Fix:** At minimum, acknowledge this mismatch explicitly and quantify its magnitude (e.g., KL divergence between suppressed and unsuppressed output distributions on a held-out set). Ideally, explore on-policy generation of completions or iterative DPO-style refinement to close the gap.

**W5. Counter-intuitive increase in thought count on hard problems contradicts narrative (Page 6 - Figure 2, Section 4.4.1).**
On AIME2024 with the 1.5B model, ST increases the average number of thoughts from 12.87 to 18.21 (a 41.5% increase) while decreasing the proportion of the last thought. The paper acknowledges this but frames it positively ("this increase led to improved accuracy"). However, this directly contradicts the narrative that ST "mitigates under-thinking by reducing unnecessary switches." If under-thinking is defined as excessive switching, and ST increases switching on hard problems, then on those problems ST is exacerbating under-thinking, not mitigating it. **Fix:** Provide a more nuanced characterization: on easy problems ST reduces switching (genuine under-thinking mitigation), while on hard problems it restructures reasoning into shorter, more numerous thoughts (perhaps a different mechanism). Update the narrative accordingly.

### Minor Weaknesses

**W6. Missing details for reproducibility of thought segmentation (Page 3 - Section 3.1).**
The entropy threshold tuning procedure lacks specification: (a) Which token probability distribution is used (raw logits, softmax, etc.)? (b) What metric is optimized during threshold tuning (accuracy, token count, or a joint objective)? (c) Is the delimiter ".\n\n" robust across different response formats? **Fix:** Add explicit details on entropy computation source, tuning metric, and delimiter robustness analysis.

**W7. Related work section reads as a list rather than a comparative analysis (Page 8 - Section 5.1).**
The paragraph on over-thinking and under-thinking presents methods chronologically without clear comparative axes. The final positioning sentence ("our approach considers that some switching is necessary") is qualitative and does not cite quantitative evidence showing ST's advantage. **Fix:** Reorganize around comparative axes (e.g., training vs. inference-time intervention, global vs. selective suppression, token-level vs. thought-level granularity) with quantitative references to Table 1.

**W8. Conclusion lacks limitations and future work (Page 9 - Section 6).**
The conclusion is a single paragraph that recaps the method without acknowledging any limitations or proposing concrete next steps for the community. **Fix:** Add a limitations paragraph covering the issues noted in W1-W5 above, and a short future work section with 2-3 concrete research directions.

**W9. Unsupported causal attribution in ablation analysis (Page 8 - Section 4.4.4).**
The paragraph on training methods states that "SimPO introduces length-normalized rewards, which effectively eliminates the impact of these length differences, allowing the model to better learn the deep patterns embedded within the data." This attributes STPO's advantage specifically to length normalization, but the ablation only compares STPO against DPO and SFT. A controlled comparison (STPO vs. SimPO applied at the response level, not the thought level) would be needed to support this causal attribution. **Fix:** Add an additional baseline using response-level SimPO (without thought-level conditioning) to isolate the benefit of thought-level conditioning from length normalization.

**W10. Novelty assessment deferred due to retrieval unavailability.**
External literature search was not available in this run. The paper addresses a timely problem and the proposed framework appears novel in its specific combination of entropy-based segmentation, forced completion, and thought-level preference optimization. However, a definitive novelty verdict requires manual verification against closely related concurrent works (e.g., step-level DPO variants, token-level reward methods, and representation-space steering methods). This verification should be performed before final acceptance.

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a timely and practically important problem (inefficient reasoning in LRMs) with a well-motivated, cleanly designed framework. The three-stage pipeline is logically coherent, and the empirical results show consistent efficiency gains (17.3–25.5% token reduction) across multiple model families and benchmarks. The positive transfer to an out-of-distribution coding benchmark is promising.

However, the score is constrained by several significant weaknesses that affect the strength of the conclusions:

- **Research value and novelty (moderate):** The thought-level preference optimization approach is a novel contribution, but its core differentiator — preserving exploration ability while promoting commitment — is not empirically validated. Without this validation, the contribution increment over existing suppression-based methods is uncertain.

- **Methodological rigor (needs improvement):** The distribution mismatch between training (logit-suppressed completions) and inference (unsuppressed decoding), the external oracle dependency for identifying promising thoughts, and the missing statistical significance testing all limit the reliability of the current conclusions.

- **Empirical support (partial):** Accuracy gains are modest (+1.9–3.12%) and reported without variance or significance tests. The central behavioral claim (reduced under-thinking) is partially contradicted by the observation that ST increases thought count on hard problems.

The identified weaknesses are fixable with additional experiments, analysis, and more cautious narrative framing. The paper could be strengthened to the 7-8 range with proper statistical reporting, the "unpromising-start" experiment for exploration verification, and acknowledgment of the distribution mismatch and recognition-commitment distinction.