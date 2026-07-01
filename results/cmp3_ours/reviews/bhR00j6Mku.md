Now let me write the final consolidated review.

**Final calibration bracket**: After examining anchors, I narrow my bracket to 6.0–7.0. The paper is stronger than "Evading Data Contamination Detection" (avg 4.25, rejected) — better experiments, stronger mechanistic analysis, clearer presentation. It is comparable to "To the Cutoff... and Beyond?" (avg 6.75, accepted) and "Detecting Pretraining Data" (avg 6.25, accepted). Its weaknesses (theory-experiment framing gap, missing error bars) are real but not fatal and are standard in empirical analysis papers.

## Summary

This paper systematically studies whether existing benchmark contamination detection methods remain effective for Large Reasoning Models (LRMs) under two realistic contamination scenarios: (Stage I) contamination introduced during SFT that is then put through RL training, and (Stage II) contamination applied to already-advanced LRMs via CoT SFT. The paper finds that (1) PPO-style RL training (GRPO, RAFT++) can conceal otherwise-detectable SFT contamination by collapsing member/non-member NLL separability, with ablation and theory pointing to importance sampling and clipping as the mechanism; and (2) SFT contamination with CoT on advanced LRMs leaves detection methods performing near random, as LRMs generalize to non-members rather than memorizing trajectories.

## Strengths

- **Comprehensive experimental scope.** The paper evaluates 10 detection methods spanning generation-based, perturbation-based, reference-based, and reference-free approaches across 6 diverse reasoning benchmarks and multiple base/LRM architectures. This breadth meaningfully supports the paper's negative claim that detection broadly fails, not just for one method or one setting.

- **Clean mechanistic identification via ablation (Table 3).** RAFT (no importance sampling/clipping) leaves detection essentially intact (AUROC 77.51). RAFT++ and GRPO with clipping enabled produce sharp drops (57.58, 61.26). Removing clipping from either restores detection. This isolates the mechanism tightly and is well-supported by the theoretical decomposition in Section 3.2. The theory and ablation mutually reinforce each other.

- **Control experiment ruling out "forgetting" (Section 3.1).** The paper directly addresses the most obvious alternative explanation by showing that (a) GRPO on both clean+member data still drops AUROC and (b) additional SFT on clean data does NOT drop AUROC while pass@1 continues to rise. This convincingly rules out the trivial explanation that the model simply forgot the contaminated data.

- **Surprising Stage II finding.** The result that SFT contamination with CoT on advanced LRMs leaves detection at near-random performance across all methods is genuinely striking and non-obvious. The inflated performance gains (e.g., DeepSeek-R1-Distill-Qwen-14B goes from 59.83 to 69.24 average pass@1) while detection fails is the kind of surprising empirical finding that can reshape how the field thinks about contamination.

## Weaknesses

### Major

None. The issues identified are genuine but none rise to the level of invalidating the paper's core claims.

### Minor

- **Theory-experiment framing gap.** Section 3.2's theoretical analysis assumes RL training on the benchmark data (line 188: "We assume that the RL training is performed on the benchmark data (i.e., training data is the combination of members M and non-members N)"). However, the headline experimental demonstration (Table 2, "RL w/ Clean") uses RL on clean data containing neither members nor non-members. The theory's assumptions are not directly met in this setting. The empirical validation in Section 3.2.1 (Table 3) does use the same clean-data setting and confirms the predicted mechanism, which partially bridges the gap. Nevertheless, the paper's narrative frames the theory as explaining the clean-data result without acknowledging the assumption mismatch. The authors should either extend the analysis to the clean-data setting or restructure the presentation so the theory is explicitly tied to settings where its assumptions hold.

- **Missing uncertainty quantification.** All AUROC values (Tables 2, 3, 5) are reported as point estimates without standard deviations, confidence intervals, or significance tests. For Stage II, where values like 65.55% (LiRA on DS Qwen-14B) and 62.59% (Loss on DS Llama-8B) are characterized as "near random guesses," readers cannot assess whether these represent weak but real signals or are genuinely indistinguishable from chance. While single-run evaluation is the norm in many large-scale benchmark papers, the "near random" claim would be materially strengthened by uncertainty measures.

- **Limited model scale in Stage I + overbroad section title.** Stage I experiments use only Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct (~7-8B parameters). Section 3's title "RL CONCEALS CONTAMINATION" is broader than the evidence warrants — RAFT (a form of RL/rejection sampling) does NOT conceal contamination. The concealment mechanism is specific to PPO-style objectives with importance sampling and clipping, as the paper correctly identifies in the text. The title and framing should be more precise.

### Trivial

- The paper uses "extensive contamination" in Stage II without specifying the number of training steps/epochs in the main text (deferred to the appendix). Including this basic detail in the main text would improve readability.

## Nice-to-Haves

- Varying contamination intensity (number of training steps, fraction of benchmark) in Stage II and showing AUROC as a function of intensity would clarify whether the failure is fundamental or a matter of degree.
- Extending Stage I experiments to larger base models (e.g., a 32B or 70B class model) would strengthen generality.

## Removed Points

- **"LiRA assumes access to training data distribution — may not hold in practice."** The paper already acknowledges this on line 87. Not a weakness.
- **"The theory only shows CAN cause concealment under idealized conditions."** The paper provides empirical validation (Table 3) that confirms the mechanism in actual neural networks. The claim is appropriately supported.
- **"Contamination vs. legitimate learning in Stage II."** The paper already discusses this interpretation in the Discussion paragraph (lines 330–331). Not an unaddressed issue.
- **"Stage II contamination intensity not varied."** Downgraded to Nice-to-Have. The paper's claim that "extensive contamination evades detection" is supported as stated.
- **"Timely and important problem" strength.** Generic — praises the problem, not the paper's specific contribution. Removed.

## Novel Insights

The Harsh Critic's most distinctive observation is that the paper's theoretical analysis (assuming RL on benchmark data) and its headline experimental demonstration (RL on clean data) are misaligned in a way the paper's narrative does not acknowledge. This is a real framing issue, though the empirical validation in Section 3.2.1 partially addresses it. No other novel insight beyond the paper's own contributions.

## Suggestions

1. Address the theory-experiment framing gap by explicitly stating the assumption difference and either (a) extending the theoretical argument to cover the clean-data setting, or (b) restructuring so the theory is confined to the benchmark-data setting and the clean-data concealment is presented as an independent empirical finding.
2. Add error bars or confidence intervals to AUROC tables, especially for Stage II where the "near random" claim depends on knowing whether values in the 55–65% range are significantly different from 50%.
3. Qualify claims about "RL" more precisely throughout the paper (e.g., "PPO-style RL objectives with importance sampling and clipping" rather than "RL") to match the evidence.
4. Include the number of training steps/epochs for Stage II contamination in the main text.

## Score and Decision

**Initial bracket (Round 1):** 6.0–7.0. The paper is clearly stronger than "Evading Data Contamination Detection for Language Models is (too) Easy" (avg 4.25, rejected) which addressed a related topic with less rigorous experiments and weaker presentation. It is comparable to "To the Cutoff... and Beyond?" (avg 6.75, accepted) and "Detecting Pretraining Data from Large Language Models" (avg 6.25, accepted), both of which are empirical analysis papers with solid experimental design and real findings. The structural issues (theory-experiment framing gap, missing error bars) prevent a higher score but do not undermine the core empirical contributions.

**Anchors retrieved:**

| Paper | Avg Score | Round | Comparison |
|-------|-----------|-------|------------|
| Evading Data Contamination Detection (Nk1MegaPuG) | 4.25 | R1 (3.5–5.5) | Weaker: less rigorous experiments, unclear methodology |
| Benchmark Inflation (rAylWUIKtu) | 4.25 | R1 (3.5–5.5) | Weaker: narrow scope (one benchmark) |
| Cheating Automatic LLM Benchmarks (syThiTmWWm) | 7.75 | R1 (3.5–5.5)* | Different topic (gaming LLM-as-judge); stronger result |
| To the Cutoff... and Beyond? (m2NVG4Htxs) | 6.75 | R1 (5.5–7.5) | Similar quality: well-executed empirical analysis |
| How much can we Forget (Nsms7NeU2x) | 6.75 | R2 (5.5–7.5) | Similar quality: contamination analysis with theory+experiment |
| Detecting Pretraining Data (zWqr3MQuNs) | 6.25 | R2 (5.5–7.5) | Similar quality: strong empirical detection benchmark |

*Retrieved in a lower band due to a database score discrepancy; actual human scores average 7.75.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>