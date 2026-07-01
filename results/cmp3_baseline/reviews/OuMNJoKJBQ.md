## Summary

This paper investigates why current LLM safety alignment methods are vulnerable to jailbreak attacks. Using causal intervention (neuron deactivation), the authors show that existing alignment relies on shallow refusal heuristics rather than deep reasoning. They construct and release a Chain-of-Thought (CoT) safety fine-tuning dataset, and propose Alignment-Weighted DPO (AW-DPO), which decomposes responses into reasoning and final-answer segments and assigns different preference weights to each. Experiments across multiple LLMs (Llama-2-7B, Llama-3.1-8B, Llama-3.2-3B, Mistral-7B) and 20 jailbreak attacks show that AW-DPO consistently improves safety alignment while maintaining competitive utility.

## Strengths

- **Novel causal analysis of alignment superficiality**: The paper provides empirical evidence through neuron deactivation and linear probing that current safety alignment is largely independent of reasoning ability. This is a clean contribution that motivates the rest of the work and offers insight beyond previous observation-only studies.
- **Principled and motivated method design**: AW-DPO is directly motivated by a concrete error analysis (15% of failures involve reasoning–answer mismatches), and the weighted decomposition into reasoning and response components is a natural, well-justified extension of DPO that addresses these cases.
- **Strong and extensive evaluation**: The authors evaluate across four model families/sizes, compare against 10+ baselines (including recent methods like STAIR and Representation Rerouting), test 20 jailbreak attack types, and include both safety (ASR) and utility (MMLU) metrics with standard deviations. The transferability study (Table 3) and ablation on hyperparameters (learning rate, scaling factor) further strengthen the empirical claims.
- **Practical contribution**: The CoT safety dataset and the principle of decomposable preference weighting are likely to be useful to the community, and the released dataset enables reproducibility and further research.

## Weaknesses
### Fatal
None.

### Major
- **Reliance on an unvalidated judge model for harmfulness scoring**: AW-DPO’s weight computation depends on harmfulness scores from “another LLM as a judge” (Section 4). The paper does not specify which judge model is used, nor does it provide any calibration, sanity checks, or ablation on judge choice. If the judge scores are noisy or biased, the weight assignments could be unreliable, undermining the method’s fine-grained advantage. This is a significant gap in the experimental setup.
- **Modest improvement over standard DPO in several settings**: While AW-DPO outperforms DPO on average, in some configurations (e.g., Mistral-7B-v0.3 Base ASR: DPO 1.14% vs. AW-DPO 1.82%) the improvement is not uniform. The paper does not fully characterize when the fine-grained weighting helps versus when it might hurt, making the claimed advantage partially qualitative rather than consistently quantitative.

### Minor
- **Error analysis scope**: The 15% failure mode breakdown is described as a key motivation, but it is based on qualitative inspection of one model (LLaMA-3.1-8B). The paper would benefit from a systematic, cross-model quantification of these error patterns to confirm the motivation generalizes.
- **Computational cost not reported**: Generating K candidates and scoring them with an LLM judge adds non-trivial overhead. The paper does not discuss training time, inference cost, or candidate count K used, making it hard for practitioners to assess the trade-off.
- **Some baseline comparisons are not fully apples-to-apples**: In Table 2, SAFECHAIN and RR are listed without standard deviations, and the paper does not clarify whether the numbers are from the original papers or re-implemented. The utility scores of strong baselines like STAIR-DPO-3 are considerably higher than the authors’ method, yet the paper attributes this to iterative training without fully controlling for data or tuning differences.

### Trivial
- Figure 3(a) is hard to interpret; the coupling of the legend and color coding could be clearer.

## Nice-to-Haves

- Adding an ablation where the judge model is varied (e.g., GPT-4 vs. Llama-guard vs. a smaller model) would substantially strengthen the reliability of AW-DPO.
- Reporting the number of candidates K and the wall-clock time for AW-DPO dataset construction and training would improve practical usability.
- A more fine-grained utility evaluation beyond MMLU (e.g., on instruction-following or reasoning tasks) would help assess whether safety gains come at a hidden utility cost.

## Novel Insights

Beyond the paper’s own contributions, the most novel insight is the empirical demonstration that alignment uses distinct, non-reasoning neural pathways: deactivating reasoning-critical neurons degrades reasoning but leaves safety refusal nearly untouched. This suggests that current safety mechanisms are implemented as shallow pattern-matching shortcuts rather than integrated into the model’s reasoning pipeline. The complementary finding that general-purpose reasoning models (Phi-4-Reasoning) perform poorly on alignment further underscores that alignment-specific reasoning must be explicitly trained, not assumed to transfer from general reasoning improvements.

## Suggestions

1. Report the specific judge LLM used and include a short validation that its harmfulness scores correlate with human judgments or with the evaluation benchmark’s own safety labels.
2. Provide a systematic quantification of the two failure modes across all evaluated models (not just one) to confirm that the motivation is broadly applicable.
3. Add a column or note in Table 2 clarifying which baseline numbers are author-run versus cited, and include standard deviations for all baselines where possible.
4. Include a brief discussion of the computational overhead (K value, judge model calls) and whether there is a practical efficiency–safety trade-off.

## Score and Decision

The paper presents a well-motivated method with a strong empirical foundation and novel analysis. The major concern about the unvalidated judge model is significant but not fatal, as the core approach is principled and the ablation results show robustness. The contributions are solid and likely to be of interest to the ICLR community. Under the guidelines, this merits acceptance.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>