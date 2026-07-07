Now I have all the calibration data. Let me write the final consolidated review.

## Summary

This paper revisits the idea of using an off-the-shelf LLM to detect and remove prompt injection attacks — an approach prior work (using GPT-3.5) found ineffective. The authors show that with a carefully designed system prompt and modern LLMs (GPT-4o, GPT-4.1, Qwen3-32B), the method achieves near-perfect detection (FPR <1%, FNR <1% on AgentDojo) and can sanitize inputs via fuzzy matching so the backend agent can still complete the original task (ASR dropping from ~55% to <1%). The evaluation covers three benchmarks, seven baselines, prompting strategy ablations, model-size/reasoning scaling (Qwen3 family), data contamination checks, and adaptive attacks.

## Strengths

- **Systematic evaluation across multiple dimensions.** The paper tests on three benchmarks (AgentDojo, Open Prompt Injection, TensorTrust), compares against seven baselines spanning four defense categories, studies prompting strategies, varies model size and reasoning mode via the Qwen3 family (Section 4.4), checks for data contamination (Section 4.5), and evaluates against adaptive attacks (Section 4.6). This is more thorough than typical for an empirical baseline paper. [Weight: +4.47]

- **The Qwen3 scaling analysis (Section 4.4) genuinely strengthens the core thesis.** Showing that Qwen3-32B achieves near-perfect detection (FPR 0.99%, FNR 0.33%) while Qwen3-0.6B fails regardless of reasoning mode cleanly supports the claim that model capacity — not some artifact of the GPT-4 API — drives performance. Figure 3 tells a coherent story that would survive a change of model family. [Weight: +3.14]

- **The prompting strategy ablation (Section 4.3, Table 3) is the right experiment to run.** Showing that GPT-3.5 without a definition of "prompt injection" achieves 60.24% FNR but drops to 15.74% with the definition demonstrates that prompt *design* matters, not just the model. This prevents the paper from being merely "bigger model = better." [Weight: +3.88]

- **The removal mechanism, while technically simple, is practically valuable.** Prior work mostly treated detection as a binary reject-or-pass decision. Showing that the guardrail can extract and remove the injected text so the agent can still complete the user task (ASR dropping from ~55% to <1% while maintaining UA ~68-72%) is a real improvement in utility under attack. [Weight: +3.92]

## Weaknesses

### Fatal

None.

### Major

- **The primary baseline comparison (Table 2) is confounded by model scale, making it uninformative about the relative merits of the approach.** PromptArmor uses GPT-4o and GPT-4.1 — frontier proprietary models — while the main comparison baselines use far smaller models: DataSentinel uses Mistral-7B, Llama Prompt Guard 2 is a small specialized model, and Deberta is BERT-sized. The paper acknowledges this (Section 4.2 line 241 notes DataSentinel's Mistral-7B "has limited reasoning ability"). The Qwen3 experiments partially mitigate this by showing that a 32B open model can match GPT-4.1, but the headline comparison in Table 2 remains the paper's primary evidence and it compares models at vastly different scales. The reader cannot tell whether prompting is better than fine-tuning at comparable model size, which is the real question. [Weight: -6.11]

### Minor

- **No variance, confidence intervals, or raw counts are reported for any result.** With temperature=0, LLM outputs are deterministic, but the extremely low error rates on AgentDojo (e.g., GPT-4o FNR 0.23% vs GPT-4.1 FNR 0.13%) could be driven by 1–2 cases out of 629 adversarial scenarios. The paper should report raw confusion counts, especially for the GPT-4o vs GPT-4.1 comparisons where sub-percentage-point differences are not meaningfully distinguishable. [Weight: -4.12]

- **The adaptive attack evaluation (Section 4.6) is narrower than the section heading implies.** The paper explicitly qualifies its claim as being "against fuzzing-based adaptive attacks" (line 288), which is honest, but the section title "Adaptive Attacks" suggests a broader evaluation. The paper does not test attacks specifically designed to exploit the guardrail LLM's weaknesses (e.g., making injected text resemble benign content, targeting the specific phrasing of the PromptArmor system prompt, or embedding injections in languages/formats the guardrail handles poorly). [Weight: -3.08]

- **The paper's framing as a proposed "method" (named PromptArmor with a "Design Rationale" section in Section 3.2) somewhat overstates the contribution.** The mechanism — prompting an off-the-shelf LLM with a detection prompt and regex-based fuzzy matching — is technically straightforward. The paper's real contribution is an empirical finding: sufficiently capable models make this approach viable, contrary to prior studies using weaker models. The framing in the abstract, introduction, and conclusion could more cleanly own this empirical nature. [Weight: -1.29]

- **The memorization test (Section 4.5) is standard but narrow.** Following Staab et al. (2023), the paper tests for near-exact memorization of benchmark samples (average similarity 0.34, 3.5% exceeding the 0.6 threshold). However, this does not rule out the model having seen similar prompt injection patterns during training that would give it a detection advantage without memorizing the exact strings. This is a standard limitation of the approach and should be stated explicitly. [Weight: -0.39]

### Trivial

None.

## Nice-to-Haves

- Report raw confusion counts (TP, FP, TN, FN) for the GPT-4o vs GPT-4.1 comparisons on AgentDojo so readers can assess whether sub-percentage-point differences are meaningful.
- Add a controlled comparison using the same base model for both PromptArmor and a fine-tuned defense (e.g., fine-tune a small model vs. prompt a large model at comparable cost, or prompt the same small model with and without fine-tuning).
- Rename Section 4.6 heading to "Fuzzing-based Adaptive Attacks" to match the scope of the evaluation.
- Provide a cost/throughput analysis of the guardrail LLM calls, especially since the paper claims computational efficiency (Section 3.2) but provides no latency or cost measurements.

## Removed Points

- **"The removal contribution is overstated"** (Harsh Critic Issue 5): The paper describes the removal mechanism straightforwardly (Section 3.1: "extract all words from the guardrail LLM's output and construct a regular expression") as a practical implementation detail, not as a novel technical contribution. This is a strawman criticism.
- **"System prompt deferred to appendix"**: This is a parser artifact — the appendix was stripped by the extraction process, not omitted by the authors.
- **"No analysis of guardrail LLM jailbreaking"**: Outside the paper's stated scope; the paper explicitly evaluates PromptArmor as a detection layer, not as an adversarially robust system against all possible attack vectors.
- **"Cost/throughput analysis missing"**: While the paper claims computational efficiency (Section 3.2), providing latency/cost measurements would strengthen the paper but is not a core flaw. Moved to Nice-to-Haves.

## Novel Insights

The reviews surface a structural tension in the paper: the headline comparison (Table 2) compares PromptArmor (GPT-4o/4.1) against detection models that are orders of magnitude smaller, yet the paper's own Qwen3 experiments (Section 4.4) demonstrate that a 32B open model can match GPT-4.1. This undercuts the framing of PromptArmor as a distinct "method" — it shows that model scale, rather than the prompting approach per se, is the primary driver. The paper's actual contribution is an empirical finding about capability thresholds for few-shot detection, which is valuable but should be framed accordingly.

## Suggestions

1. **Own the empirical nature.** Frame the contribution explicitly as "We establish that, with sufficiently capable models (≥32B parameters), a well-designed prompt achieves near-perfect detection across multiple benchmarks." Drop the apparatus of proposing a "method" with a Design Rationale section — the contribution is the finding, not the tool.

2. **Fix the model-scale confound.** Either (a) compare PromptArmor using the same base model as DataSentinel (Mistral-7B) to control for model scale, or (b) add a comparison where a frontier model is used as the detector but with a different detection approach (e.g., fine-tuned on the same data), or (c) acknowledge explicitly that Table 2 compares models at different scales and reframe it as a cost-agnostic capability demonstration rather than a method comparison.

3. **Report raw counts** for the key comparisons so readers can distinguish a 1-case difference from a meaningful one.

## Score and Decision

**Initial bracket (Round 1):** 5.25–5.75, anchored by:
- 0VZP2Dr9KX (5.25, "Baseline Defenses for Adversarial Attacks Against Aligned Language Models"): Similar empirical-baseline paper. Had more severe negatives (-9.62, -8.51, -7.21) about single-attack study and weak model evaluation. Our paper has better evaluation breadth but a model-scale confound. Itemized.
- CEvGuwMum0 (5.75, "JudgeRail"): Prompting-based guardrail paper. Had stronger positives (+6.22 for elegant approach) but also stronger negatives (-8.39 for lack of novelty). Our paper sits similarly. Itemized.

**Narrowing (Round 2):** Additional anchors confirm the band:
- MsRdq0ePTR (5.25, "Prompt Injection Benchmark"): Similar topic, comparable negative weight structure (-6.18). Itemized.

**Final score grounded in weighted-item comparison:** Our draft's strongest negative (-6.11, model scale confound) is comparable to the 5.25 anchor's strongest negatives (-6.18), but our paper lacks the more severe -8 to -9 negatives seen at both 5.25 and 5.75. Our strongest positive (+4.47) is below the 5.75 anchor's +6.22. The balance places the paper between these anchors at 5.5.

The paper provides a timely and practically useful empirical finding, and the evaluation is more thorough than typical for this class of work. However, the model-scale confound in the headline comparison weakens the evidence for the central claim, and the framing as a "method" overstates what is fundamentally an empirical observation. The weaknesses are addressable in revision.

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Reject</decision>