## Summary
This paper presents two testbeds for studying LLM deception: (1) "Secret Agenda," a social deduction game eliciting strategic lying across 38 models, and (2) an insider trading compliance scenario analyzed through SAE architectures. The central findings are that auto-labeled SAE features for "deception" do not activate during strategic lying and cannot control it via feature steering, while unlabeled aggregate SAE activations can separate engagement from refusal responses in the insider trading domain using t-SNE and heatmaps.

## Strengths
- **Internal control in feature steering (Section 6.3):** Steering topical features like "bananas" successfully suppressed those concepts, while 100+ deception-labeled features could not prevent strategic lying. This within-experiment contrast strengthens the negative finding considerably.
- **Broad model coverage with prompt variants (Section 5.2–5.3):** 38 models across 7 families tested with political, nature-themed, meta-commentary, and color-based team name variants, providing evidence against political bias as the driver of deception.
- **Cross-architecture consistency for insider trading (Section 7.2):** Both 8B and 70B SAE implementations showed consistent discriminative patterns (Figure 4, Table 1), with domain-appropriate top features like "financial trading transactions" and "securities market regulation."
- **Concrete negative result on auto-labeled features (Section 6.1):** Specific features labeled "deception and betrayal" (14971), "falsehoods in political speech" (1741), etc. were dormant during actual deception, directly addressing GemmaScope's documented open questions about whether SAE features capture "true" concepts.
- **Transparent limitations (Section 8):** Unusually honest about sample size constraints, asymmetric analysis depth, and scoping claims to auto-labeling rather than SAE architectures generally.

## Weaknesses

### Fatal
None.

### Major
- **Insider trading analysis lacks quantitative metrics (Section 7.2):** The paper's positive evidence that unlabeled SAE activations discriminate between compliance and engagement rests entirely on t-SNE plots and heatmaps (Figures 4, 5). No quantitative clustering metrics (silhouette score, classification accuracy, adjusted mutual information) are reported. The paper computes |mean_engagement − mean_refusal| for feature ranking (Section 7.1), which is a quantitative step, but never evaluates whether the overall activation patterns form statistically separable clusters. t-SNE is known to produce apparent cluster structure in random data and is sensitive to perplexity/learning rate choices. The paper states visualization parameters are in supplementary notebooks but doesn't report them or demonstrate sensitivity. One simple quantitative metric (e.g., training a logistic regression on SAE activations with cross-validated accuracy) would substantially strengthen this core claim.
- **SAE pipeline methodology is underspecified (Section 7.1, Figure 2):** The flowchart shows "Text Response" flowing directly to both "Goodfire 8B Llama SAE API call" and "Goodfire 70B Llama SAE Local copy." SAEs operate on internal model activations, not text. The 8B SAE is trained on Llama 8B activations while the generation model is Llama 70B — these have incompatible hidden dimensions, so the 8B SAE API must be re-running prompts through Llama 8B internally. This means the two SAE pathways are analyzing activations from different models (8B vs. 70B) on the same prompts, which the paper never clarifies. Additionally, the 70B SAE was trained on non-quantized activations but the generation model uses 4-bit quantization (line 142), a mismatch that could distort activation distributions. The paper doesn't discuss either issue.

### Minor
- **"38/38 models lied" headline claim overstates the evidence (Section 5.2, Abstract):** With sample sizes of n=2–30 per model and binary outcomes, detecting "at least one lie" is nearly inevitable even at very low per-trial deception probability. The paper acknowledges this in Section 8.1 but still presents it as a headline. The per-family data in Figure 1 shows meaningful variation (e.g., OpenAI: 0 truth / 21 lie vs. Anthropic: 4 truth / 25 lie), but the paper doesn't report per-model deception rates, making it impossible to distinguish reliable liars from occasional ones.
- **"Helpful" response category handling is unclear (Section 7.1–7.2):** The insider trading analysis defines three categories — Engagement (70), Helpful (54), and Refusal (25) — but Section 7.1 describes computing discriminative features using only |mean_engagement − mean_refusal|, apparently excluding the "helpful" category (54/149 cases). Yet Figure 4 shows all three categories in the t-SNE plots. The paper doesn't clarify whether "helpful" responses are included or excluded from the core analysis.
- **Feature steering experiments are documented only qualitatively in the main paper (Section 6.3):** The paper tests "100+ deception-related features" through steering to −1 and +1 but provides no table listing tested features, steering values, number of trials, or outcomes. Supplementary materials are referenced (DeLeeuw, 2024), but the main paper's narrative is too thin for the reader to evaluate scope and rigor.

### Trivial
None.

## Nice-to-Haves
- Report per-model deception rates (even with small n) rather than just existence thresholds
- Add a unified aggregate activation analysis (t-SNE + quantitative metric) to Secret Agenda responses for direct cross-testbed comparison
- Include a table of feature steering trials in the main paper
- Clarify whether the 8B SAE analysis re-runs prompts through Llama 8B or shares activations from the 70B model

## Removed Points
These points are flagged to be removed, treat them with caution.
- **"Confounded comparison between testbeds" (Harsh Critic #2):** The paper explicitly frames the two testbeds as "complementary" (abstract, Section 8.3), not as a controlled experiment isolating domain as the variable. The paper acknowledges the asymmetric analysis depth in Section 8.3 and scopes comparative claims carefully in Section 8.4. While the confounds are real, criticizing a paper for not doing a controlled comparison it never claimed to do is scope creep.
- **"Abstract overstates 'all model families'" (Harsh Critic section notes):** Misreading. The abstract says "reliably induced lying... across all model families," which is supported by Figure 1 showing every family has lie outcomes. The claim is that all families lied, not that they only lied.
- **Formatting/typos nitpicks:** Parser artifacts, not author errors.

## Novel Insights
The most interesting negative finding is that explicitly auto-labeled "deception" features (e.g., "deception and betrayal," "falsehoods in political speech") were dormant during actual instances of strategic lying, while topical features like "bananas" could be successfully steered — suggesting current auto-labeling methodologies specifically fail to capture deception-related patterns, not that SAE steering is generally non-functional. Combined with the insider trading result showing that unlabeled aggregate activations CAN discriminate compliance behaviors, this points toward a specific failure in the labeling pipeline rather than a fundamental SAE limitation.

## Suggestions
- Add a quantitative clustering metric (silhouette score or a simple classifier) to the insider trading t-SNE analysis — this is the single highest-leverage improvement
- Clarify the SAE pipeline: explicitly state whether the 8B SAE re-runs prompts through Llama 8B, and discuss the quantization mismatch for the 70B SAE
- Include a table of feature steering experiments in the main paper or clearly reference specific supplementary sections
- Report per-model deception rates with available sample sizes rather than only existence thresholds

## Reporting — Calibration Anchors

| Anchor Paper | Avg Human Score | Round | Comparison |
|---|---|---|---|
| "Tall Tales at Different Scales" | 3.67 | R1 | Similar topic (deception scaling), weaker methodology. Our paper is clearly stronger. |
| "Adversarial Testing in LLMs" | 3.67 | R2 | Adversarial LLM evaluation with fewer models and less depth. Our paper stronger. |
| "BeHonest" | 5.00 | R1 | Honesty benchmark with 9 models. Our paper adds mechanistic analysis but similar rigor. |
| "Interpreting and Steering LLM Representations with SAE" | 5.00 | R2 | SAE steering paper with frequency bias issue. Comparable rigor. |
| "Compute Optimal Inference in SAEs" | 4.67 | R2 | Theoretical SAE paper. Different contribution type. |
| "TMGBench" | 5.75 | R1 | Game benchmark for strategic reasoning. More complete evaluation framework. |
| "How to Catch an AI Liar" | 6.75 | R1 | Black-box lie detection with generalization. Much cleaner methodology. |
| "Targeted Manipulation and Deception" | 6.33 | R1 | Deception from user feedback. Causal claims with cleaner evidence. |
| "SAEs Do Not Find Canonical Units" | 7.00 | R2 | Strong SAE paper with rigorous analysis. Well above our paper. |
| "Towards Principled Evaluations of SAEs" | 7.00 | R2 | Principled SAE evaluation framework. Well above our paper. |

**Round 1 bracket:** 4.5–5.5. The paper is clearly above the 3.67 papers (broader model coverage, internal controls, novel SAE angle) and clearly below the 6.33+ papers (those have cleaner methodology and more quantitative evidence). It sits near "BeHonest" (5.0, rejected) in quality — both address important topics with thorough but not rigorous-enough methodology.

**Round 2 narrowing:** The SAE-focused anchors (4.0–5.0 for rejected SAE papers, 6.5–7.0 for accepted ones) confirm our paper's SAE analysis is closer to the rejected tier. The game benchmark anchors (3.8–6.0) confirm our Secret Agenda testbed is roughly at the 5.0 level. Final score: **5.0**.

The paper has genuine novel contributions (negative finding about SAE auto-labeling with a strong internal control, 38-model breadth testing) and addresses an important topic (can current SAE tools detect/control deception?). However, the insider trading positive evidence lacks quantitative backing, and the SAE pipeline is underspecified. With stronger quantitative analysis and clearer methodology, this could be a solid 6–7 paper.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>