## Summary

This paper hypothesizes that current LLM safety alignment relies on shallow refusal heuristics rather than deep reasoning. To probe this, the authors conduct a causal intervention (deactivating reasoning-critical attention heads) and find that safety classification accuracy remains high while reasoning accuracy drops, which they interpret as evidence that alignment is "superficial." To address this, they construct and release a Chain-of-Thought (CoT) safety fine-tuning dataset, and propose Alignment-Weighted DPO (AW-DPO), which decomposes responses into reasoning and response segments and assigns distinct preference weights to each based on harmfulness scores from a judge LLM. Extensive experiments across multiple model families and sizes show consistent improvements in safety (Attack Success Rate) over standard DPO and other baselines.

## Strengths

- **Hypothesis-driven paper structure.** The paper advances a clear, testable thesis — that alignment failures stem from shallow refusal heuristics — and structures the work around probing this hypothesis, empirically identifying failure modes, and designing a method to address them. This is a genuine strength relative to alignment papers that iterate on methods without diagnosing *why* existing approaches fail.

- **Empirical error analysis directly informs method design.** The qualitative analysis identifying two specific CoT fine-tuning failure patterns (correct reasoning + unsafe answer; incorrect reasoning + safe answer) maps directly onto the AW-DPO weighting mechanism. The method is grounded in observed failures rather than intuition alone.

- **Dataset release and transferability analysis.** The authors construct and commit to releasing a CoT alignment dataset combining safety and utility prompts. The transferability experiment (Table 3) showing that a pre-constructed AW-DPO dataset can be applied to different model architectures is practically useful and reduces the cost barrier for adoption.

- **Thorough evaluation across models and baselines.** Experiments cover four model families/sizes (Llama-2-7B, Llama-3.2-3B, Llama-3.1-8B, Mistral-7B-v0.3), five attack categories, multiple recent baselines (SAFECHAIN, STAIR, Representation Rerouting), and include hyperparameter ablations (scaling factor, learning rate) with clear takeaways.

## Weaknesses

### Fatal
None.

### Major

- **The causal intervention experiment does not conclusively establish that alignment is "superficial" or independent of reasoning.** The paper acknowledges (line 68) that the alignment task (safe vs. unsafe prompt classification) has near-100% probing accuracy from the very first layers, while the reasoning task starts near chance. Deactivating the top 10% of reasoning-critical heads degrades the harder task more than the easier one — this is expected even if both tasks involve some shared circuitry, because a ceiling effect on the easy task masks any degradation. The experiment lacks a control condition (e.g., deactivating an equivalent number of *random* heads, or heads with the *lowest* probing accuracy for reasoning) that would distinguish between "alignment does not use reasoning" and "the alignment task is robust to moderate ablation because it is easy." The paper's headline diagnostic claim is more confident than the evidence supports. However, this experiment is preliminary/motivational and does not undermine the paper's core methodological contribution (AW-DPO), which stands on its own evaluation.

### Minor

- **AW-DPO's safety improvements over standard DPO are modest in absolute terms on strong modern baselines.** For Llama-3.1-8B, the average ASR goes from 1.00% (DPO) to 0.81% (AW-DPO), a 0.19 percentage point reduction. For Llama-3.2-3B: 1.04% → 0.58% (0.46 pp). On already-low baselines (ASR ~1%), these improvements, while directionally consistent, are small. The larger improvements on Llama-2-7B (5.70 pp) and Mistral-7B (2.87 pp) are more compelling but are partly driven by the Multi-languages category where DPO has anomalously high ASR with large variance (±15.59, ±14.08). The paper would benefit from a per-prompt analysis showing that AW-DPO fixes specific failure cases that DPO misses, directly tied to the 15% reasoning-related error patterns identified in Figure 3(a).

- **Utility gap with STAIR is notable.** In Table 2, Ours(Base) achieves better safety than STAIR-DPO-3 (0.81% vs. 1.13% ASR) but substantially lower MMLU utility (58.27% vs. 73.34%). The paper acknowledges the cost difference (one round vs. three rounds of iterative training) but does not analyze *why* utility drops — whether it is the CoT format, the weighted DPO over-optimizing for safety, or the base model choice. Given the paper's stated goal to "preserve competitive utility," a 15-point gap on the primary utility benchmark merits deeper discussion.

- **The judge model scoring of reasoning traces raises a conceptual question not addressed in the main text.** AW-DPO requires a judge LLM to assign separate harmfulness scores to the reasoning trace and the final response. A reasoning trace that correctly identifies *why* a request is harmful (e.g., "this request asks for instructions on making explosives, which is illegal") mentions harmful content but should receive a *low* harmfulness score — it is the desired behavior. The paper does not discuss how the judge model distinguishes between "reasoning that is harmful" and "reasoning that correctly identifies harm." Without knowing the judge model, its prompt, or validation of its scoring for this specific sub-task, this step is underspecified.

### Trivial

- **Notation inconsistency.** Equation (1) uses β as the DPO scaling parameter; Equation (2) renames it to γ without explanation. The paper also uses "respond" and "response" interchangeably in the weight definitions (Section 4).

## Nice-to-Haves

- Report the specific judge LLM and scoring prompt used for harmfulness assignment, along with a manual audit showing agreement with human judgment for reasoning-trace scoring.
- Include a random-ablation control condition for the causal intervention experiment to strengthen the diagnostic claim.
- Add per-prompt case studies showing specific failures that DPO misses and AW-DPO corrects, with direct attribution to the weighting mechanism.
- Report statistical significance (e.g., bootstrap confidence intervals) for DPO vs. AW-DPO comparisons, given the small absolute differences and high variance in some categories.

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"Section 5.3 does not advance the paper's case"** — Removed because the paper uses the finding that reasoning models (Phi-4) are not safer to *support* its argument that alignment-specific reasoning is needed, motivating the method. This is not a weakness.
- **"RR baseline is incomplete in Table 2"** — Removed because the apparent missing cells are likely a PDF parsing artifact; the original table formatting cannot be verified from the parser output.
- **"No statistical significance testing"** — Demoted to Nice-to-Have. Lack of significance tests is common practice in this area and not a weakness unique to this paper.
- **"Why 10% of heads? Why only first 11 layers?"** — The paper justifies both choices: the first 11 layers are where reasoning accuracy is near chance, making them critical for question understanding (line 68); the top 10% are selected as the most important reasoning heads. The thresholds are reasonable even if the exact values could be further justified.

## Novel Insights

None beyond the paper's own contributions. The reviewer identifies specific methodological gaps in the causal intervention and underspecified components of the AW-DPO pipeline, but these are critical observations about the paper as presented rather than novel scientific insights.

## Suggestions

1. In the causal intervention experiment, add a control ablation (random heads or heads with lowest reasoning probing accuracy) to disentangle task-difficulty effects from genuine independence of alignment and reasoning.
2. Specify the judge LLM, scoring prompt, and validation (manual audit or inter-annotator agreement) for the harmfulness scoring of reasoning traces.
3. Add per-prompt qualitative comparisons showing specific failure cases that AW-DPO corrects but DPO does not, directly linked to the 15% reasoning-related error patterns.
4. Analyze why MMLU utility drops relative to STAIR — is the gap inherent to single-round training, or can it be narrowed with better hyperparameter tuning or data composition?

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>