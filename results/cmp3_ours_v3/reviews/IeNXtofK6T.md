**Calibration Anchors Considered:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| NAbqM2cMjD (Prompt Infection) | 5.20 | R1 | Attack paper with novelty but weaker execution; PromptArmor is cleaner |
| 0VZP2Dr9KX (Baseline Defenses) | 5.25 | R1 | Similar "baseline defense" framing but studied only one attack on small models; PromptArmor is more comprehensive |
| l3bUmPn6u5 (PFT) | 4.25 | R1 | Fine-tuning defense with narrow scope; PromptArmor is stronger empirically |
| V4y0CpX4hK (ASB) | 6.25 | R1, R2 | Comprehensive benchmark with methodology questions; PromptArmor is simpler but cleaner |
| YixNDE12wm (GuardAgent) | 6.00 | R1 | Different approach (guardrail agent); comparable quality |
| YauQYh2k1g (Dissecting Adversarial Robustness) | 6.25 | R2 | Strong empirical study of agent robustness; PromptArmor is comparable in quality |
| rnJxelIZrq (Hypergraph defense) | 6.50 | R2 | More sophisticated methodology; PromptArmor is more straightforward but well-executed |
| V892sBHUbN (Rapid Response) | 5.75 | R2 | Similar scope (practical defense); comparable quality |

**Round 1 bracket:** 5.5–7.5. **Narrowing rationale:** The paper is clearly stronger than the 4–5 range papers (PFT, Baseline Defenses) which had significant methodological flaws. It is comparable to the 5.75–6.5 range papers (ASB, GuardAgent, Dissecting Adversarial Robustness). The weaknesses (scale-confounded baselines, under-developed adaptive attacks) prevent it from reaching the 7+ level, placing it solidly in the borderline-accept range. **Final score: 6.0.**

## Summary

This paper revisits the idea of prompting an off-the-shelf LLM as a defense against prompt injection attacks. Prior work (2023–2024) found this approach ineffective on older models like GPT-3.5. The authors show that with modern LLMs (GPT-4o, GPT-4.1) and a carefully designed system prompt, detection accuracy reaches <1% FPR and FNR on AgentDojo and <5% on two other benchmarks. The paper also introduces PromptArmor, which removes injected content via fuzzy matching rather than discarding the entire input, and evaluates across multiple benchmarks, model sizes, reasoning modes, and adaptive attacks.

## Strengths

1. **Timely and important empirical finding.** The paper identifies and corrects a stale belief in the literature — that prompting an off-the-shelf LLM to detect prompt injection is ineffective. Prior negative results (Liu et al., 2024) were based on GPT-3.5-era models. The paper provides clear evidence that with GPT-4o/GPT-4.1, detection accuracy is dramatically higher (both FPR and FNR below 1% on AgentDojo). This is a genuinely useful update for the field.

2. **Solid evaluation across multiple benchmarks.** AgentDojo (a challenging agent environment), Open Prompt Injection, and TensorTrust all show consistent patterns, strengthening the generalizability claim.

3. **Systematic study of model size vs. reasoning (Section 4.4).** The controlled experiment with Qwen3-0.6B/8B/32B in both reasoning and non-reasoning modes cleanly shows that model capacity is the primary driver of performance, with reasoning providing secondary, model-size-dependent benefits. This goes beyond simply reporting "GPT-4o works well."

4. **Memorization test (Section 4.5).** The paper responsibly addresses data contamination concerns by showing average edit-distance similarity of 0.34 and only 3.5% of samples exceeding the 0.6 threshold, ruling out memorization as an explanation for the main results.

5. **Honest framing of contribution.** The paper frames itself as a "revisit" of a previously dismissed approach, characterizes PromptArmor as a *baseline* rather than a silver bullet, and clearly distinguishes its contributions.

## Weaknesses

### Major

1. **Baseline comparison confounds approach with model scale (Section 4.2, Table 2).** The comparison pits GPT-4o and GPT-4.1 (frontier-scale models) against Deberta (BERT-sized), Llama Prompt Guard 2 (7B-scale), and DataSentinel (Mistral-7B). The paper acknowledges DataSentinel's poor performance is partly due to using Mistral-7B with "limited reasoning ability" (p. 6), but this is not surfaced as a structural limitation of the comparison. The question of whether the *approach* (prompting) or the *scale* primarily drives performance is left partially unanswered by Table 2 alone. While the Qwen3 experiments (Section 4.4) partially address this by showing Qwen3-32B achieves near-perfect results, a direct comparison at matched scale (e.g., PromptArmor using a 7B–8B model vs. DataSentinel/Llama Prompt Guard) would more cleanly isolate the contribution of the approach from the contribution of the model. This does not threaten the core thesis (prompting with modern LLMs is effective), but it means the comparative claims in Section 4.2 are broader than the evidence supports.

2. **Adaptive attack evaluation does not fully stress-test the defense (Section 4.6).** The adaptive attack (AgentVigil) optimizes templates for *attack success rate* (ASR) on the full pipeline, not for *evading detection by the guardrail LLM*. Moreover, the adaptive attacks actually produce *weaker* attacks than the non-adaptive ones even *without* the defense (21.46% ASR vs. 52.73%, Table 4), which the paper does not discuss. This suggests the optimization loop may not have correctly targeted the guardrail. The paper's claim of robustness is therefore supported only against a specific fuzzing-based attack generation procedure, not against a knowledgeable adversary aware of the defense mechanism.

### Minor

3. **Prompt design ablation is under-developed (Section 4.3).** The investigation of prompting strategies is confined to one binary comparison for GPT-3.5 (with vs. without a definition of "prompt injection"). The authors claim GPT-4o and GPT-4.1 "perform equally well across different prompting strategies" without showing data for any alternatives or specifying what was tried. Since the method's effectiveness rests heavily on prompt design, this gap limits reproducibility and actionable guidance for practitioners.

4. **Removal quality is not evaluated (Section 3.1).** The paper reports ASR as a proxy for removal effectiveness, but this conflates detection (was the injection found?) with removal (was the right span extracted without collateral damage?). The fuzzy matching technique (constructing a regex from extracted words) could accidentally remove non-injected content or miss parts of the injection. A separate analysis of removal precision/recall would strengthen the paper's claimed novelty over prior work (removal vs. discard).

5. **Deployment costs not quantified (Section 3.2).** The paper claims "computational efficiency" as an advantage but does not provide any latency, throughput, or cost estimates. Running GPT-4o/GPT-4.1 as a guardrail for every tool return in an agent pipeline has non-trivial costs. Even a rough estimate would help practitioners evaluate the trade-off.

### Trivial

None.

## Nice-to-Haves

- A direct comparison where PromptArmor uses a model of comparable scale (e.g., 7B–8B) to DataSentinel and Llama Prompt Guard 2.
- A properly adaptive attack that optimizes specifically for evading the guardrail LLM's detection.
- An analysis of removal quality (precision/recall of the fuzzy matching).
- Brief cost/latency estimates for deployment with frontier models.

## Removed Points

These points from the input review were flagged for removal per the filtering rules:

1. **"System prompt not shown in main paper (deferred to Appendix C)"** — REMOVED: the appendix is stripped by the parser; the paper shows a minimal version of the prompt in Figure 2 and references Appendix C for the full version.

2. **"Missing related works"** — REMOVED: missing related work claims cannot be verified without external sources.

3. **The critic's "Fatal" severity label for the scale-confounding issue** — DEMOTED to Major: the Qwen3 experiments partially address the scale concern; the paper's main thesis (prompting-based detection deserves reconsideration) does not depend on the Table 2 comparison holding up; the paper frames PromptArmor as a baseline, not as outperforming all defenses.

4. **"Reproducibility nitpicks about trivial implementation details"** — REMOVED per instructions.

5. **"What happens when the guardrail LLM is the same as the backend LLM"** — REMOVED: the paper explicitly mentions this is possible (Section 3.1); this is a nice-to-have extension, not a weakness.

## Novel Insights

None beyond the paper's own contributions. The paper's central finding — that modern LLMs make prompting-based detection viable contrary to 2023-era results — is itself the primary insight. The Qwen3 ablation's finding that model capacity is the primary driver (with reasoning providing secondary benefits) is the most informative secondary result.

## Suggestions

1. Add a row to Table 2 using PromptArmor with a 7B–8B model (e.g., Qwen3-8B) to provide a scale-matched comparison with DataSentinel and Llama Prompt Guard 2.
2. Design an adaptive attack that explicitly optimizes to evade the guardrail LLM's detection (not just to achieve task-level ASR), or at minimum discuss the unexplained drop in ASR for the adaptive attacks without defense.
3. Show ablation results for at least 3–4 prompt variants on GPT-4o to demonstrate robustness to prompt design choices.
4. Add a brief analysis of removal quality — how often does the fuzzy matching correctly extract the injection without removing benign content?
5. Include a rough estimate of deployment costs (e.g., additional API cost per user task).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>