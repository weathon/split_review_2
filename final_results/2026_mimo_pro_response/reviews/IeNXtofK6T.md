## Summary
This paper presents PromptArmor, a defense against prompt injection attacks that uses an off-the-shelf LLM as a guardrail to detect and remove injected prompts from data samples before they reach the backend LLM. The central thesis is that modern LLMs' improved reasoning capabilities make this previously dismissed approach highly effective, and it should serve as the standard baseline for evaluating future prompt injection defenses. Evaluation across three benchmarks (AgentDojo, Open Prompt Injection, TensorTrust) shows near-perfect detection with frontier models (FPR/FNR <1% on AgentDojo with GPT-4o/4.1), 0.00% ASR with 72.02% utility-under-attack on AgentDojo against 7 baselines, and robust performance against adaptive attacks (0.16% ASR).

## Strengths
- **Strongest defense on AgentDojo with best security-utility tradeoff**: Table 2 shows PromptArmor-GPT-4.1 achieves 0.00% ASR and 72.02% UA on AgentDojo, simultaneously outperforming all seven baselines (Deberta, Llama Prompt Guard 2, DataSentinel, MELON, Repeat Prompt, Delimiter, Tool Filter) in security while maintaining competitive utility. Notably, its UA of 72.02% *exceeds* the no-defense baseline (64.27%), demonstrating that sanitization actually improves end-to-end agent performance under attack.
- **Systematic ablation of model size and reasoning capability**: Section 4.4 evaluates Qwen3-0.6B/8B/32B in reasoning and non-reasoning modes, cleanly establishing that model capacity is the primary factor (32B achieves near-GPT-4.1 performance), reasoning helps mid-sized models (Qwen3-8B FNR drops from 26.50% to 15.78%), and neither compensates for insufficient capacity (0.6B). This provides actionable guidance for practitioners.
- **Robustness against adaptive attacks**: Table 4 shows PromptArmor-GPT-4.1 maintains 0.00% ASR against AgentVigil-NoDefense and 0.16% ASR against AgentVigil-Adaptive (attacks specifically optimized to evade PromptArmor), directly addressing the likely critique that prompting-based defenses would be trivially bypassed.
- **Comprehensive benchmark coverage spanning agent and non-agent scenarios**: Evaluation on AgentDojo (629 adversarial scenarios, agent), Open Prompt Injection (non-agent), and TensorTrust (human-collected adversarial prompts) strengthens generalizability claims beyond a single setting.
- **Practical investigation of prompting strategy sensitivity**: Table 3 shows GPT-3.5 yields FNR=60.24% without defining "prompt injection" but only 15.74% with a definition, demonstrating that prompt design matters and providing useful practical guidance.

## Weaknesses

### Fatal
None

### Major
- **No analysis of failure cases**: The paper reports aggregate FPR/FNR numbers but never examines specific samples that PromptArmor misses. On TensorTrust, GPT-4o has FNR of 4.61% (~1 in 22 injections missed); on Open Prompt Injection, GPT-4.1 has FNR of 4.24%. What characterizes these misses — adversarial prompts with unusual structure, injections lacking instruction-like patterns, or ambiguous cases? Without understanding failure modes, it is difficult to assess how the defense generalizes beyond these benchmarks or what attack strategies would defeat it. For a paper arguing this should be *the* standard baseline, showing *why* it works and *where* it breaks down is essential — not just *that* it works on aggregate.
- **No inference cost or latency analysis**: Section 3.2 lists "computational efficiency" as a core design advantage, but this refers exclusively to development cost (no training, no data collection). PromptArmor adds an additional LLM API call for every data sample processed. For agents making many tool calls — the AgentDojo banking agent interacts with multiple tools per task — this means significant additional latency and cost. The paper should report average guardrail LLM calls per task, added latency, and cost comparison with baselines. Without this, the "computational efficiency" claim is incomplete — cheap to build but potentially expensive to run.

### Minor
- **Superficial memorization test (Section 4.5)**: The paper reports 3.5% of AgentDojo samples exceed the 0.6 similarity threshold and concludes GPT-4.1 is "not likely to have memorized the data samples." However, (a) 3.5% corresponds to ~22 out of 629 samples — non-trivial, (b) the paper doesn't break down which samples are memorized or check whether they correlate with detection performance, and (c) only AgentDojo is tested, not the other two benchmarks. Attack templates like "Ignore Previous Instructions" are widely discussed online. The Qwen3 replication partially mitigates this concern but the analysis section as written acknowledges the issue more than it resolves it.
- **Prompt tuning per benchmark without sensitivity analysis**: Line 199 states "we adjusted the detection prompt for each dataset." If each benchmark gets a tailored prompt, strong results may partly reflect prompt engineering rather than general capability. Section 4.3 claims GPT-4o/4.1 "perform equally well across different prompting strategies" but this is asserted without tabulated evidence. A brief paraphrase sensitivity experiment would substantially strengthen the generalizability claim.
- **Same model as guardrail and backend is acknowledged but not analyzed**: Line 72 notes "in practice, both of them may use the same underlying model" but this scenario — where a sophisticated attacker could craft injections that exploit the guardrail model's own detection logic — is never evaluated.
- **Minor numerical inconsistency**: Line 276 states Qwen3-8B FNR improves from "26.59%" to "15.78%" but Table (line 265) reports 26.50%.

### Trivial
- System prompt described as "carefully designed" but the actual prompt is only in the appendix; at least a summary of key design choices should appear in main text since the prompt is the core methodological contribution.

## Nice-to-Haves
- Report baseline defense performance on TensorTrust and Open Prompt Injection (currently Table 1 only shows PromptArmor's FPR/FNR; Table 2 comparisons are AgentDojo-only).
- Test whether DataSentinel's approach performs better with a stronger backbone than Mistral-7B.

## Removed Points
These points are flagged to be removed, treat them with caution.
- Strength finder's claim that "data contamination test rules out memorization as an explanation" conflicts with the verified weakness about the superficial memorization test. The 3.5% memorization rate and incomplete analysis mean this "strength" overstates the evidence. The weakness wins.

## Novel Insights
The most genuinely novel finding is the clean scaling relationship between LLM capability and defense effectiveness: model capacity is the primary factor (32B achieves near-perfect regardless of reasoning mode), reasoning helps mid-sized models, and neither compensates for insufficient capacity. Additionally, the finding that PromptArmor sanitization actually *improves* utility under attack (72.02% > 64.27% no-defense) — because removing injections allows correct task completion rather than merely preventing harm — is a practically valuable insight for the defense community.

## Suggestions
1. Add a failure case analysis: categorize false negatives on each benchmark by injection type/structure. This would make the baseline maximally useful for future defense comparison.
2. Report inference cost: average guardrail calls per AgentDojo task, added latency, and cost. Even a brief table would address the gap.
3. Provide prompt sensitivity data: show FPR/FNR for paraphrased system prompts on at least one benchmark to demonstrate robustness to wording.
4. Expand memorization analysis to all three benchmarks and break down memorized samples by type (injection templates vs. benign data vs. user tasks).

## Score and Decision

**Anchoring notes:**
- "Baseline Defenses for Adversarial Attacks Against Aligned Language Models" (avg 5.25, Reject): A baseline paper studying defense techniques but with significant methodological issues — single-attack study, inconsistent experimental setups, only weak models evaluated. PromptArmor is substantially stronger: evaluates across 3 benchmarks, multiple frontier models, includes adaptive attacks, and delivers strong results.
- "GuardAgent: Safeguard LLM Agent" (avg 6.00, Reject): Both are guardrail papers for LLM agents. PromptArmor has stronger evaluation with direct head-to-head comparisons against 7 baselines and adaptive attack robustness.
- "Agent Security Bench" (avg 6.25, Accept): A comprehensive but broad benchmark paper. PromptArmor is more focused with stronger targeted empirical results.
- "AgentHarm" (avg 6.75, Accept): A well-evaluated benchmark paper. PromptArmor is at a similar level of rigor — focused contribution with strong evaluation, though with the noted gaps.
- Multiple papers at 8.0 (Booster, Backtracking, etc.): These represent more complete, polished contributions that are clearly above PromptArmor.

**Round 1 bracket**: Between 6.0 and 8.0. PromptArmor is clearly above GuardAgent (6.0) and Agent Security Bench (6.25) due to stronger evaluation and more compelling empirical results. It is comparable to AgentHarm (6.75) in rigor. It is below the 8.0 papers which have more complete analyses and fewer gaps.

**Narrowing**: PromptArmor's strong empirical core (near-perfect defense, 7 baselines, adaptive attacks, model scaling ablation) puts it solidly in the accept range. The major gaps (no failure analysis, no cost analysis) and minor gaps (superficial memorization test, unverified prompt sensitivity) prevent it from reaching 8.0 territory where papers are more thorough. I place it at 7.0 — strong contribution that meets the bar for acceptance, with clear room for improvement in a revision.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>