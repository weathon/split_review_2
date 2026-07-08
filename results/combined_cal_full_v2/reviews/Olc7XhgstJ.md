Now I have sufficient calibration data. Let me compile the final review.

## Summary

This paper proposes Steady Thought (ST), a three-stage framework (Thought Segmentation → Thought Completion → Fine-Grained Preference Optimization) to mitigate "under-thinking" in large reasoning models. The key idea is to segment model responses into thought-level units via entropy, evaluate each thought by forcing the model to complete it without switching (via logit suppression), and then construct thought-level preference pairs to train the model to commit to promising reasoning trajectories. Experiments across three model sizes (1.5B–14B) and four datasets (including the OOD LiveCode benchmark) show simultaneous accuracy improvements (up to +5.3%) and token reductions (19.0–39.3%).

## Strengths

- **Well-motivated problem with clear empirical grounding.** Section 1 and Figures 1a/1b concretely demonstrate that LRMs often find a correct thought early but continue switching excessively—a precise, measurable characterization of under-thinking, not just an anecdotal claim. Weight: **9.67**

- **Coherent and novel three-stage pipeline.** The pipeline—segmenting via entropy, completing each thought under suppressed switching, then constructing preference pairs at the divergence point—is internally consistent and non-obvious. The alignment between the stages and the stated goal (teaching models when to commit vs. when to switch) is clear. Weight: **8.85**

- **Strong and consistent empirical results across scale and domain.** Table 1 reports accuracy improvements across all three model sizes and all four datasets, including OOD LiveCode. Token reductions of 19.0–39.3% are substantial and, critically, are not achieved at the cost of accuracy—accuracy improves up to +5.3% on LiveCode for Qwen3-8B. Weight: **9.78**

- **Sound ablation design.** Section 4.4.4 compares STPO against SFT and DPO under the same data-generation pipeline, showing that the preference optimization formulation (specifically the length-normalized reward from SimPO) is essential. Section 4.4.3 examines entropy threshold sensitivity, and Section 4.4.2 provides a diagnostic (PCT) supporting the claimed mechanism. Weight: **9.96**

## Weaknesses

### Fatal

None.

### Major

1. **Baseline configuration is underspecified, undermining comparison fairness.** NOWAIT on Qwen3-8B shows a dramatic and atypical failure: accuracy on MATH-500 collapses from 91.4% to 61.0% and GSM8K token count explodes from 1,759 to 12,369 (a 7× increase). This behavior is far outside what the original NOWAIT paper reports and strongly suggests either an implementation issue or inappropriately tuned hyperparameters (suppression strength, keyword list). Similarly, SEAL has an α scaling parameter whose value per model is not stated. Without transparency on baseline configuration, it is impossible to determine whether ST's gains over these baselines reflect genuine superiority or merely that the baselines were run with suboptimal settings. Weight: **0.35** *(Note: low weight from the scoring model reflects that this concern does not affect the core contribution—ST also outperforms vanilla baselines—but it is a methodological transparency issue that must be addressed.)*

2. **No variance or confidence intervals are reported for any result.** Given that AIME 2024 has only 30 problems, a 2–3 point accuracy difference (~1 problem) could easily be noise. The paper averages 8 runs for AIME and 2 for LiveCode, which is a reasonable attempt to reduce variance, but without reporting the variance itself or any significance test, the reader cannot assess whether the reported improvements (e.g., +0.6% on GSM8K for Qwen3-8B: 95.6→96.1) are statistically meaningful. Weight: **2.40**

### Minor

3. **The analysis in Section 4.4.1 partially undermines the paper's central claim of teaching "commitment to promising thoughts."** For DeepSeek-R1-Distill-Qwen-1.5B on AIME 2024, ST *increases* the average number of thoughts from 12.87 to 18.21. The paper explains this as "in-depth exploration" on hard problems, but this directly contradicts the narrative of reduced switching and increased commitment. The mechanism appears to be more nuanced—perhaps "more efficient exploration" or "better termination"—and the paper should reconcile this tension explicitly rather than letting "in-depth exploration" do double duty to cover both fewer thoughts (easy problems) and more thoughts (hard problems for small models). Weight: **5.03**

4. **The preference pairs that drive the learning signal are constructed from a modified decoding regime (logits of trigger words suppressed to force the model to complete a thought without switching).** There is no analysis validating that these forced completions represent genuinely better reasoning rather than artifacts of the suppression. The paper's SFT ablation (Table 4) trains on the same forced completions and underperforms STPO, but this does not establish the quality of the completions—it only shows STPO is a better objective for using them. A human evaluation or comparison against a stronger model's completions would strengthen the evidential basis for the preference signal. Weight: **4.41**

5. **The "Overall" accuracy column in Table 1 averages accuracies across four datasets of vastly different sizes** (AIME: 30 problems, MATH-500: 500 problems, GSM8K: 1,319 problems) and difficulties. This treats each dataset equally regardless of size, which is statistically unusual. Reporting per-dataset results is cleaner and avoids this aggregation issue. Weight: **4.87**

6. **Training data details are sparse.** The paper states that training data is sampled from Omni-Math using a target model but provides no details on the sampling strategy, how many training examples were used, how responses were filtered, or any data quality checks. For a training-based method, these are important reproducibility details. Weight: **2.88**

### Trivial

None.

## Nice-to-Haves

- A human evaluation or stronger-model comparison validating that the forced completions produced by logit suppression are genuinely better reasoning (not just different reasoning) would substantially strengthen the paper.
- Reporting the specific suppression strength (logit penalty magnitude) used for the thought completion stage and the hyperparameters (β, γ, learning rate, batch size, training steps) would improve reproducibility.
- A computational cost analysis comparing ST's total training compute against simply running the baseline with more inference-time compute would help contextualize the efficiency gains.

## Removed Points

These points from the input review were removed after verification against the paper:

- **Entropy threshold tuning not reported for all models (Critic's Issue 4):** The paper states that threshold tuning results for other models are in Appendix D. Since the parser strips appendices, this criticism cannot be verified from the main text and is removed per guidelines.
- **Claim about formalization being overstated:** The critic's opinion that the formalization is "a straightforward application of the Bradley-Terry model" is a subjective assessment, not an identified flaw.
- **Arrow direction in Table 1 headers:** Identified as a parser artifact by the critic; the original submission does not have this issue.
- **Data contamination concern:** Speculative and not grounded in evidence from the paper.
- **Entropy calibration dependence:** Speculative without evidence that the model is poorly calibrated.
- **Missing hyperparameters (β, γ, lr):** Per guidelines, undisclosed training hyperparameters are classified as removal-worthy nitpicks.
- **SFT ablation not being the right control:** The critic mischaracterized the SFT ablation—it does in fact train on the forced completions (Section 4.4.4: "we used the x from the preference data pairs as the input and the chosen response as the output"). The broader concern about validating forced completions is retained above (Minor #4).
- **Criticisms about missing appendix content, missing proofs in appendix, or absent references:** All removed per guidelines (parser strips these sections).

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface any perspective that meaningfully reframes or deepens the paper's analysis beyond what the authors already provide.

## Suggestions

- Add confidence intervals or error bars to Table 1 using the multiple runs already collected. Report the NOWAIT and SEAL hyperparameter values (suppression strength, keyword list, α scaling) used for each model, and explain the anomalous NOWAIT behavior on Qwen3-8B.
- Explicitly reconcile the increase in thought count for small models on AIME (Section 4.4.1) with the paper's "commitment" narrative. This could be framed as a shift from random switching to more purposeful exploration.
- Validate the forced-completion preference signal via human evaluation or comparison against a stronger model's completions, and include the results in the main paper.
- Replace the "Overall" average with per-dataset reporting or use a weighted average reflecting dataset sizes.

## Score and Decision

Calibration anchors used across rounds:

| Anchor Paper | Path | Avg Score | Round | Itemized? | Comparison to Our Paper |
|---|---|---|---|---|---|
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | 1 | No | Irrelevant topic, far weaker |
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | 1 | No | Irrelevant (survey), far weaker |
| Supervised Chain of Thought | pXIbcRPxWR | 2.50 | 1 | Yes | Much weaker paper (no empirical validation, formulation issues) |
| Planning in Strawberry Fields | jOuHjFw71C | 3.00 | 1 | Yes | Less novel (evaluation-only), our paper has stronger contribution |
| Direct Judgement PO | ToWKyjwDqO | 5.00 | 1 | Yes | Comparable preference-opt topic but different domain (judges); similar weakness levels |
| Planning with MCTS | sdpVfWOUQA | 3.00 | 1 | No | Less relevant (MCTS framework) |
| Thinking Forward/Backward | cWrqs2lwCJ | 3.00 | 1 | No | Less relevant (backward planning) |
| Synergistic Weak-Strong | 3iJ7eSj2rE | 4.00 | 1 | No | Different alignment setting |
| TPO | O0sQ9CPzai | 6.33 | 1,2 | Yes | **Most comparable**: preference optimization for reasoning. Our paper has stronger/cleaner empirical results and comparable strengths, with similar-level weaknesses. Lower than our paper. |
| Visual Agents Fast/Slow | ncCuiD3KJQ | 6.75 | 1 | Yes | Different domain (vision) but similar "dynamic switching" framing. Comparable quality. |
| OPAD | cfn2O1qvxp | 6.00 | 1 | Yes | Different approach (decoding-time alignment). Similar quality tier. |
| WSPO | f7KxfUrRSb | 7.25 | 2 | Yes | Preference optimization for alignment. Higher quality—stronger theory, but some similar hyperparameter concerns. Our paper is below this. |
| FlexPrefill | OfjIlbelrT | 8.00 | 1 | No | Higher quality (solid efficiency method, unanimous accept) |
| Take a Step Back | 3bq3jsvcQ1 | 8.00 | 1 | No | Higher quality (elegant prompting approach) |

**Round 1 bracket:** (5.5, 7.5) based on comparable papers (TPO at 6.33, Visual Agents at 6.75, OPAD at 6.00).

**Round 2 narrowing:** The most comparable anchor is TPO (6.33), which was accepted with scores [8,5,6]. Our paper shares TPO's high-weighted strengths (well-motivated problem, coherent method, solid ablations) but our weaknesses are slightly higher weighted (max 5.03 vs TPO's max 4.61). Our empirical results are stronger—3 model sizes vs TPO's single model family, 4 datasets including OOD, and simultaneous accuracy + efficiency gains. The WSPO anchor (7.25) showed stronger theory and higher reviewer enthusiasm, setting an upper bound. Within the (5.5, 7.5) bracket, our paper sits above TPO (6.33) but below WSPO (7.25).

The four strengths all have very high weights (8.85–9.96), comparable to top anchors. The three most impactful weaknesses (5.03, 4.87, 4.41) are genuine but addressable concerns about mechanism clarity and evidence quality, not fatal methodology flaws. The two "Major" weaknesses have low model weights (0.35, 2.40), indicating they do not threaten the core contribution.

**Final score: 6.5**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>