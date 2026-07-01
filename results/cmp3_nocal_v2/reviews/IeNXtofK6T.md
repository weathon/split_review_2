Now I have all the evidence I need. Let me write the final consolidated review.

---

## Summary

PromptArmor revisits the dismissed approach of prompting an off-the-shelf LLM to detect prompt injection attacks, finding that modern reasoning-capable models (GPT-4o, GPT-4.1) now achieve near-perfect detection (FPR and FNR below 1% on AgentDojo) and can also remove injected content via regex-based fuzzy matching so the backend LLM can continue processing sanitized inputs. The paper evaluates across three benchmarks, compares against seven baselines, tests adaptive attacks, and checks for data contamination — a more thorough evaluation than typical for this type of defense paper.

## Strengths

- **Clean empirical finding with practical value.** Tables 1 and 2 show striking results: GPT-4o and GPT-4.1 achieve FPR and FNR below 1% on AgentDojo, and reduce ASR from 54.53% to 0–0.47%. This directly contradicts the prior belief in the field that prompting-based detection was dead, making this a genuinely useful result for practitioners and safety researchers.

- **Responsible evaluation scope.** The paper includes adaptive attacks (Section 4.6, AgentVigil-Adaptive with ASR remaining near 0%), a data contamination / memorization check (Section 4.5, average similarity 0.34, only 3.5% above threshold), and an ablation across model sizes and reasoning modes using Qwen3 (Section 4.4). These go beyond what most defense papers provide.

- **Honest framing.** The paper does not oversell PromptArmor as a novel algorithm; it acknowledges prior work found this approach ineffective and frames the contribution as a re-evaluation driven by LLM capability advances. This is the correct framing for an empirical study.

- **Informative ablation on reasoning vs. model size.** The Qwen3 experiments (Section 4.4, Figure 3) cleanly disentangle the effects of model scale and reasoning mode, showing that sufficient model capacity is the primary driver and reasoning provides secondary benefits, especially for mid-sized models.

## Weaknesses

### Fatal
None.

### Major

- **Primary evidence is limited to a single model family.** The paper's central claim is that "prompting an off-the-shelf LLM with strong reasoning capabilities should be reconsidered as a standard baseline." Yet Tables 1 and 2, which carry the headline results, evaluate only OpenAI models (GPT-3.5, GPT-4o, GPT-4.1). The Qwen3 experiments in Section 4.4 are presented as an ablation rather than primary evidence. As written, the headline results could be read as "the most capable OpenAI models can detect prompt injections near-perfectly," which is less generalizable than the paper's claim about "modern LLMs" broadly. Including at least one strong model from another family (Claude, Gemini, or an adequately scaled open-weight model) in the main comparison table would substantially strengthen the paper's thesis. This does not invalidate the core finding — the results with GPT-4o/4.1 are striking even in isolation — but it narrows the claim the evidence can support.

### Minor

- **The injection removal mechanism is unvalidated.** The paper presents removal (rather than discard) as a key differentiator (Section 1: "it further removes the injected prompt so the backend LLM can continue task processing… rather than discarding it entirely"). However, the removal mechanism — regex-based fuzzy matching on words extracted from the guardrail LLM's output — is described in a single sentence (Section 3.1: "we extract all words from the guardrail LLM's output and construct a regular expression that allows arbitrary characters between these words") with no ablation or accuracy evaluation. The downstream metrics (ASR, UA) confound detection and removal errors. A direct comparison of "detect and remove" vs. "detect and discard" would clarify whether removal actually adds value.

- **Unsupported claim about prompting strategies.** Section 4.3 states that "newer models like GPT-4o and GPT-4.1 perform equally well across different prompting strategies" without showing any data for these models. Only GPT-3.5 results are presented (Table 3). This claim needs to be either backed by the corresponding data or qualified.

- **Per-query cost trade-off is not discussed.** Section 3.2 claims "computational efficiency" because PromptArmor avoids training costs, but the baselines in Table 2 (Deberta, Llama Prompt Guard 2, DataSentinel) use models orders of magnitude cheaper per inference than GPT-4.1. The paper never discusses this per-query cost gap or where the cost-performance Pareto frontier lies. The Qwen3-32B result (Section 4.4) partially addresses this, but it is not presented in the main comparison.

- **Security architecture concern unaddressed.** Section 3.2 mentions that "the same LLM can be used as the core module in an agent as well as the detector in PromptArmor" as an advantage. However, using identical models for both roles means an attacker who compromises the backend has also compromised the guardrail. This architectural coupling is worth at least a brief discussion.

### Trivial
None.

## Nice-to-Haves

- **Diversify model families in the main evaluation.** Adding results from Claude 3.5/4, Gemini 2.0 Pro, or Llama 3.1 70B+ to Tables 1 and 2 would directly strengthen the central claim about "modern LLMs" rather than "OpenAI models."

- **Ablate the removal step.** Comparing "detect and remove" vs. "detect and discard" on the same metrics would validate whether removal adds measurable value beyond detection alone.

- **Failure analysis of false negatives.** The 0.13%–4.61% FNR cases across benchmarks could reveal systematic blind spots (e.g., particular attack patterns or contexts the guardrail LLM misses).

- **Rough per-query cost estimates.** Even approximate token costs for PromptArmor vs. Deberta/Llama Prompt Guard 2 would help practitioners assess the cost-performance trade-off.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **Critique that Section 5 "subtly distances PromptArmor from the detection-based category."** This is a framing observation about related-work organization, not a substantive weakness. The paper classifies defenses thematically; PromptArmor uses an off-the-shelf LLM rather than a fine-tuned small model, which is a meaningful distinction.
- **Characterization of the design rationale as "marketing arguments."** This is a subjective stylistic judgment without a concrete anchor in the paper.
- **Question about how AgentVigil generates attacks.** The paper appropriately cites AgentVigil and summarizes its approach; further description of the attack generation method is outside the paper's scope.

## Novel Insights

The reviews surface one insight that goes beyond the paper's own contributions: the observation that PromptArmor's strongest results come from models that are also the most expensive per-query, creating a cost-asymmetry with baselines that the paper does not acknowledge. The paper frames efficiency as an advantage (avoiding training costs), but the relevant efficiency question for practitioners is per-inference cost, which is never quantified. This tension — between the "simple baseline" framing and the reliance on expensive frontier models — is not resolved in the paper and would benefit from explicit discussion.

## Suggestions

- Add at least one non-OpenAI model (Claude, Gemini, or Llama-3 70B+) to the main comparison tables (Tables 1 and 2) to support the generalization claim about "modern LLMs."
- Include an ablation comparing the detect-and-remove pipeline against a detect-and-discard variant to validate that the removal step adds measurable value.
- Acknowledge the per-query cost gap with small-model baselines and provide rough token-cost estimates.

## Score and Decision

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>