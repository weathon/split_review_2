Now I have enough calibration data. Let me synthesize everything and write the final review.

**Calibration Summary:**

Round 1 anchors across all bands:
- 1-1.5: NEMESIS (1.4), systematic review (1.0), cross-lingual (1.0), financial markets (1.0)
- 1.5-3.5: Inverse Prompt Engineering (3.0), Bridging Safety Gap (3.0), System-Prompt Attention (2.33), Code-of-thought (3.0)
- 3.5-5.5: Baseline Defenses (5.25, Reject), Defending Alignment-Breaking (5.33, Reject), VLMGuard (5.0, Reject), LLM Jailbreak Detection (4.25, Reject)
- 5.5-7.5: JudgeRail (5.75, Reject), Probe before You Talk (6.0, Accept), Beyond Mere Token Analysis (6.5, Accept), GuardAgent (6.0, Reject)
- 7.5-8.5: Booster (8.0, Accept), Backtracking (8.0, Accept), Privacy-Preserving ICL (8.0, Accept), Context-Parametric Inversion (8.0, Accept)

Round 2 anchors:
- Agent Security Bench (6.25, Accept), AutoAdvExBench (6.17, Reject), AgentHarm (6.75, Accept), Rapid Response (5.75, Reject), Dissecting Adversarial Robustness (6.25, Accept)
- Robustness Over Time (6.75, Reject), BEAT (6.0, Accept), Scaling Laws for Adversarial Attacks (6.5, Accept), ReFAT (5.75, Accept), Jailbreaking with Simple Adaptive Attacks (6.14, Accept)

**Initial bracket:** 6.0-7.0

**Narrowing:** PromptArmor has stronger empirical results than most 6.0 papers (e.g., BEAT which is 6-6-6-6 but narrower problem), comparable thoroughness to 6.25 papers (ASB), but less novelty than 6.5+ papers. The evaluation is exceptionally thorough (3 benchmarks, 7 baselines, multiple models, adaptive attacks, memorization test). The core finding (prompting works now) is practically important but methodologically simple. Score: **6.5**.

---

## Summary
PromptArmor proposes that simply prompting a modern reasoning-capable LLM to detect and remove prompt injections from untrusted data is an effective baseline defense. Evaluated on AgentDojo, Open Prompt Injection, and TensorTrust benchmarks, GPT-4o/GPT-4.1 achieve FPR and FNR below ~5% across all benchmarks, with PromptArmor-GPT-4.1 achieving 0.00% ASR and 72.02% utility under attack on AgentDojo—outperforming seven diverse baselines. The paper argues this approach should serve as a standard baseline for future prompt injection defense research.

## Strengths
- **Outperforms all baselines on AgentDojo with near-perfect defense**: PromptArmor-GPT-4.1 achieves 0.00% ASR with 72.02% UA (Table 2), simultaneously beating all seven baseline defenses—none of which achieve both low ASR and high UA (e.g., Tool Filter: 0.79% ASR but only 18.80% UA; DataSentinel: 38.63% ASR). The removal-based approach also improves utility over the undefended baseline (72.02% vs 64.27% UA).

- **Comprehensive multi-benchmark evaluation**: Results span three distinct benchmarks—AgentDojo (629 adversarial agent scenarios), Open Prompt Injection (non-agent scenarios with 5 attack types), and TensorTrust (competition-collected human-written attacks)—demonstrating generalization across settings rather than benchmark-specific overfitting (Table 1).

- **Systematic ablation on model size and reasoning capability**: The Qwen3 experiments (Section 4.4) show a clear progression: Qwen3-0.6B is non-functional (62.57% FPR or 75.71% FNR), Qwen3-8B is moderately effective, and Qwen3-32B achieves near-GPT-4.1 performance (0.99% FPR, 0.33% FNR with reasoning). This provides concrete evidence that model capacity, not just prompt engineering, drives effectiveness.

- **Robustness under adaptive attacks and memorization testing**: Table 4 shows PromptArmor-GPT-4.1 maintains 0.00% ASR against AgentVigil-NoDefense and 0.16% against AgentVigil-Adaptive attacks. Section 4.5 applies the memorization test from Carlini et al. (2021) and Staab et al. (2023), finding only 3.5% of samples exceeding the 0.6 similarity threshold, directly addressing the plausible data contamination concern.

- **Post-injection removal preserves utility**: Unlike prior detection defenses that discard contaminated inputs, PromptArmor extracts and removes injected content via fuzzy matching (Section 3.1), allowing the backend LLM to continue processing sanitized input. This yields 72.02% UA with 0.00% ASR—better than the 64.27% UA with no defense.

## Weaknesses

### Fatal
None

### Major
- **Benchmark attacks are predominantly formulaic/instruction-like, limiting generalizability claim**: AgentDojo tests four attack types—"Ignore Previous Instructions," "### System," "### Important Messages," and "Tool Knowledge"—all following recognizable template patterns (Section 4.1). TensorTrust and OPI similarly feature template-based injections. The adaptive attack evaluation uses AgentVigil, which "generates new attack templates optimized based on feedback" (Section 4.6). Since the paper's central claim is that PromptArmor "should now be regarded as a standard baseline for evaluating defenses" (Abstract), the absence of evidence against subtler, semantically disguised injections (e.g., data that shifts agent reasoning without explicit instruction patterns) limits the strength of this positioning. The paper provides no evidence against this broader class of attacks.

- **No failure mode analysis**: The paper reports only aggregate metrics across benchmarks. For a paper positioning a method as a baseline, understanding what the defense gets wrong is essential—future researchers need to know where PromptArmor fails to establish clear challenge problems. Even a qualitative categorization of false negatives (injections that pass through) and false positives (clean inputs flagged) would substantially strengthen the baseline argument.

### Minor
- **"Computational efficiency" claim is incomplete**: Section 3.2 states PromptArmor "avoids the significant costs associated with developing and training custom security models," which is valid regarding development cost. However, the paper provides no data on deployment costs (inference latency, token usage, API cost). Since PromptArmor adds a full GPT-4o/GPT-4.1 inference to every tool call in an agent's pipeline, and agents can make dozens of tool calls per task, the absence of any cost/latency analysis weakens the practical deployment argument—especially compared to baselines like Deberta and Llama Prompt Guard 2 which are small models with much lower per-sample costs.

- **Limited prompt sensitivity study**: Section 4.3 reveals GPT-3.5 "does not understand the term 'prompt injection'" and needs a definition injected into the system prompt. This important finding about prompt sensitivity is treated as a minor ablation rather than investigated systematically. Only one model's sensitivity is studied, leaving open how robust the approach is to prompt wording variations across different models.

## Nice-to-Haves
- Report per-sample latency and token cost for each guardrail LLM, even as rough estimates, so readers can assess practical trade-offs.
- Test against at least some injection attacks that don't follow the "Ignore previous instructions" template pattern.
- Discuss what kinds of attacks would likely defeat PromptArmor, establishing a clear challenge problem for the community.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Formatting/style nitpicks from any reviewer are removed (per hard rules).
- No criticisms about missing appendix content since the parser strips appendices.

## Novel Insights
The paper's most significant observation is the sharp capability threshold for prompt injection detection: GPT-3.5 fails badly (11.24% FPR, 15.74% FNR) while GPT-4o achieves near-perfect detection (0.07% FPR, 0.23% FNR) on the same task with the same prompting approach. Combined with the Qwen3 experiments showing that even a 32B open-source model can match GPT-4.1, this reveals that the prior consensus dismissing prompting-based defenses was model-dependent, not fundamental. This reframes the research landscape: instead of asking "can prompting work?" the community should now ask "where does prompting fail?"

## Suggestions
- Add a failure case analysis showing examples of injections PromptArmor misses and clean inputs it flags, to help the community understand where the baseline breaks down.
- Include a brief cost/latency comparison table so readers can assess practical trade-offs between PromptArmor's accuracy and the cost of running a frontier model as a guardrail.
- Discuss limitations against non-template-based attacks explicitly, even if testing against them is deferred to future work.
- Expand the prompt sensitivity study beyond GPT-3.5 to understand robustness of the approach across model families.

## Reporting

**All anchor papers retrieved:**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 5kMwiMnUip.md (NEMESIS) | 1.40 | 1 | Clearly weak jailbreaking survey; PromptArmor is far stronger |
| 8QTpYC4smR.md (Systematic Review) | 1.00 | 1 | Generic survey; incomparable |
| gwZ90hFSL2.md (Cross-lingual) | 1.00 | 1 | Unrelated weak paper |
| nSDOkm0SKo.md (Financial Markets) | 1.00 | 1 | Unrelated weak paper |
| 3MDmM0rMPQ.md (Inverse Prompt Engineering) | 3.00 | 1 | Guardrail approach, poor presentation, simple experiments; PromptArmor much stronger |
| KjxZ4BdUdN.md (Bridging Safety Gap) | 3.00 | 1 | Guardrail pipeline, rejected; PromptArmor has stronger results |
| MV5j4Qpq7N.md (System-Prompt Attention) | 2.33 | 1 | Defense against jailbreaks, rejected; PromptArmor stronger |
| lUyYX9VFgA.md (Code-of-thought) | 3.00 | 1 | Safety evaluation, rejected; PromptArmor stronger |
| 0VZP2Dr9KX.md (Baseline Defenses) | 5.25 | 1 | Most comparable topic but single attack, inconsistent setup, weak models; PromptArmor substantially stronger |
| V01FPV3SNY.md (Defending Alignment-Breaking) | 5.33 | 1 | Different defense approach; PromptArmor has more thorough eval |
| JwoCs9O3QL.md (VLMGuard) | 5.00 | 1 | VLM defense; PromptArmor has stronger empirical contribution |
| RC5x3OkywQ.md (LLM Jailbreak Detection) | 4.25 | 1 | Jailbreak detection; PromptArmor stronger |
| CEvGuwMum0.md (JudgeRail) | 5.75 | 1 | Harmful text detection; PromptArmor has stronger results |
| EbxYDBhE3S.md (BEAT/Probe before You Talk) | 6.00 | 1, 2 | Accepted defense paper, narrower problem (backdoor only), comparable quality but PromptArmor has stronger results on broader problem |
| rnJxelIZrq.md (Beyond Mere Token Analysis) | 6.50 | 1 | Accepted with theoretical novelty; PromptArmor has stronger practical results but less theoretical contribution |
| YixNDE12wm.md (GuardAgent) | 6.00 | 1 | Rejected despite similar score; PromptArmor has stronger evaluation |
| tTPHgb0EtV.md (Booster) | 8.00 | 1 | Strong accepted paper on alignment; different problem, higher novelty |
| Bo62NeU6VF.md (Backtracking) | 8.00 | 1 | Strong accepted paper with novel technique; PromptArmor not at this novelty level |
| oZtt0pRnOl.md (Privacy-Preserving ICL) | 8.00 | 1 | Strong accepted paper; different topic |
| SPS6HzVzyt.md (Context-Parametric Inversion) | 8.00 | 1 | Strong accepted paper; different topic |
| V4y0CpX4hK.md (Agent Security Bench) | 6.25 | 2 | Accepted benchmark paper; comparable quality, both solid empirical contributions |
| leSbzBtofH.md (AutoAdvExBench) | 6.17 | 2 | Benchmark paper; PromptArmor has stronger results |
| AC5n7xHuR1.md (AgentHarm) | 6.75 | 2 | Accepted benchmark paper with broader impact; slightly stronger contribution |
| V892sBHUbN.md (Rapid Response) | 5.75 | 2 | Rejected defense paper; PromptArmor stronger |
| YauQYh2k1g.md (Dissecting Adversarial Robustness) | 6.25 | 2 | Accepted empirical paper; comparable quality |
| eC4WlSZc4H.md (Robustness Over Time) | 6.75 | 2 | Longitudinal study, rejected; PromptArmor has clearer contribution |
| YzxMu1asQi.md (Scaling Laws for Adversarial Attacks) | 6.50 | 2 | Accepted theoretical/empirical paper; different contribution type |
| s5orchdb33.md (ReFAT) | 5.75 | 2 | Accepted defense paper; PromptArmor has more thorough evaluation |
| hXA8wqRdyV.md (Jailbreaking with Simple Adaptive Attacks) | 6.14 | 2 | Attack paper; different direction |

**Round 1 bracket:** 6.0-7.0. PromptArmor is clearly stronger than all papers scored below 5.5 (weak methodology, limited evaluation), comparable to accepted papers at 6.0-6.5 (BEAT, ASB, Dissecting Adversarial Robustness), and slightly below papers at 6.75+ (AgentHarm has broader impact).

**Round 2 narrowing:** The additional anchors confirm the 6.0-7.0 range. PromptArmor has stronger empirical results than BEAT (6.0, 6-6-6-6) but less novelty than papers scoring 6.75+. The thorough evaluation (3 benchmarks, 7 baselines, ablations, adaptive attacks, memorization test) is a distinguishing strength versus similarly-scored papers.

**Final score: 6.5.** The paper is a solid empirical contribution with exceptionally thorough evaluation, strong results, and a practically important finding (prompting works now). It lacks the methodological novelty of higher-scoring papers but clearly advances the field's understanding.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>