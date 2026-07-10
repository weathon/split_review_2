Now let me finalize the review based on all the evidence.

## Summary

This paper proposes PromptArmor, a defense against prompt injection attacks that uses an off-the-shelf LLM (a "guardrail LLM") to detect and remove injected prompts from data samples before they reach the backend LLM. The key finding is that with modern LLMs (GPT-4o, GPT-4.1), this simple prompting-based approach achieves FPR < 1% and FNR < 1% on the AgentDojo benchmark — a qualitative improvement over prior work using older models that found prompting-based defenses "marginally effective." The paper evaluates across three benchmarks, compares against seven baselines, and conducts ablation studies on prompting strategies, model size, reasoning capability, and adaptive attacks.

## Strengths

- **Empirically decisive results:** PromptArmor with GPT-4o achieves FPR=0.07% and FNR=0.23% on AgentDojo, and GPT-4.1 achieves ASR=0.00% (Tables 1 & 2). These represent a qualitative regime shift from prior conclusions that prompting-based defenses are only marginally effective.

- **Substantive comparison against multiple defense categories:** Table 2 compares PromptArmor against 7 baselines spanning detection-based (Deberta, Llama Prompt Guard 2, DataSentinel), prompt augmentation (Delimiting, Repeat Prompt), system-level (MELON), and tool filtering defenses. This is more comprehensive than typical defense evaluations in this literature.

- **Controlled study of model size and reasoning capability (Section 4.4):** The Qwen3 experiments (0.6B, 8B, 32B in reasoning and non-reasoning modes) provide genuine evidence about capability thresholds — showing that the 0.6B model cannot balance security and utility regardless of reasoning mode, while the 32B model achieves near-perfect performance regardless. This goes beyond simply comparing black-box API models.

- **Memorization test (Section 4.5):** Checking that the guardrail LLM has not memorized benchmark data (average similarity 0.34, only 3.5% of samples above the 0.6 threshold) is a methodological control many defense papers omit, directly addressing concern about data leakage inflating results.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

- **Adaptive attack evaluation is narrow and the abstract slightly oversells the robustness claim.** The paper tests only one adaptive attack generation method (AgentVigil, a fuzzing tool). The body qualifies this as "fuzzing-based adaptive attacks" (Section 4.6), but the abstract claims robustness against "adaptive attacks specifically designed to circumvent it" without the fuzzing-based qualifier. A broader set of adaptive attacks targeting the guardrail's detection criteria would strengthen the claim.

- **Removal quality is not directly evaluated.** PromptArmor's claimed advantage over prior work is that it removes (not just detects) injected prompts via fuzzy matching (Section 3.1). However, the removal step is never directly assessed — e.g., what proportion of injected content is correctly extracted, or how often benign content is accidentally removed. The end-to-end ASR of 0.00% provides indirect evidence that removal works, but direct component-level evaluation would improve practical deployability.

- **No variance or confidence intervals reported.** All results (Tables 1, 2, 3, 4) lack multiple-run statistics. While single-run evaluation at temperature 0 is standard in this setting, reporting variance or running key experiments multiple times would strengthen reliability claims.

- **No cost, latency, or token overhead analysis.** The paper describes PromptArmor as "easy-to-deploy" and mentions "computational efficiency" (Section 3.2), but provides no concrete measurements of API cost, token overhead per call, or latency. Since every tool-call result requires a guardrail LLM inference, this information is important for practitioners considering adoption of this proposed baseline.

- **Per-attack-type results not reported on AgentDojo.** Section 4.1 notes that AgentDojo includes four attack types (Ignore Previous Instructions, System Message, Important Messages, Tool Knowledge) with likely varying difficulty. Reporting only average FPR/FNR may hide important variation in where the method succeeds or struggles.

- **Memorization test is thin.** Section 4.5 reports only average similarity (0.34) and the proportion above 0.6 (3.5%). More informative statistics (maximum similarity, full distribution, relationship between similarity and detection performance) would strengthen this analysis.

### Trivial
None.

## Nice-to-Haves
- Direct evaluation of injection-extraction quality.
- Per-attack-type breakdown of FPR/FNR for AgentDojo.
- Cost/latency analysis (tokens per call, API cost per 1,000 calls, approximate latency).
- Multiple runs with confidence intervals for at least the main results.
- Tone down the abstract's adaptive-attack claim to match the body's "fuzzing-based" qualification.

## Removed Points
These points are flagged to be removed, treat them with caution:
1. **DataSentinel comparison fairness** — The paper transparently acknowledges DataSentinel's limitations (Mistral-7B, not adapted to agent setting) and does not make the general claim "prompting > training-based detection." The comparison evaluates available defenses as-is.
2. **Combined ASR metric being "unusual"** — The paper clearly explains this conservative metric; it does not distort results.
3. **Method described as "too simple"** — Subjective opinion, not a concrete weakness for a baseline proposal.
4. **Missing appendix content / system prompt** — Removed per policy: parser strips appendix content.
5. **Qwen3 figure/table duplication** — Standard practice.
6. **Various formatting nitpicks and subjective writing comments.**

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
- Add per-attack-type breakdown of FPR/FNR for AgentDojo.
- Include a cost/latency analysis.
- Directly evaluate injection-extraction quality.
- Add multiple runs or confidence intervals for main results.
- Align the abstract's adaptive-attack claim with the body's qualification.

## Score and Decision

The paper presents a clear, well-supported empirical finding: prompting a modern off-the-shelf LLM is a far more effective prompt injection defense than previously believed, achieving near-perfect detection on the challenging AgentDojo benchmark. The evaluation is comprehensive across three benchmarks, seven baselines, multiple model families, and controlled ablation studies. The weaknesses are all minor — they concern missing supplementary evidence, not threats to the core claim. The paper's contribution (reinstating prompting-based defense as a strong baseline) is substantiated and practically significant.

MY FINAL SCORE: <score>8.0</score>
MY FINAL DECISION: <decision>Accept</decision>