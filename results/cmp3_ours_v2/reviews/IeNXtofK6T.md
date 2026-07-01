Now I have all the calibration data I need. Let me finalize the review.

## Summary

This paper revisits the simple idea of prompting an off-the-shelf LLM as a guardrail against prompt injection attacks in LLM agents, a direction prior work (2023) had dismissed as ineffective on older models. The authors show that with modern reasoning-capable LLMs (GPT-4o, GPT-4.1), the same approach achieves ≤0.6% FPR and ≤0.3% FNR on AgentDojo, reduces ASR from 55% to below 1%, and can additionally remove—not just detect—injected content so the agent can continue processing. Ablations on model size (Qwen3 0.6B→32B) and reasoning mode cleanly separate the effects of capacity and reasoning capability. The paper argues that this simple prompting baseline should now be the standard comparator for future prompt injection defense work.

## Strengths

1. **Empirically decisive central finding.** The paper provides clear evidence that a prompting-based defense, previously dismissed as ineffective, works at near-perfect levels when powered by a sufficiently capable modern LLM (e.g., GPT-4.1 achieves 0.56% FPR, 0.13% FNR, 0.00% ASR on AgentDojo). This changes what should count as a minimal baseline for this task.

2. **Informative model-size/reasoning ablation (Section 4.4, Figure 3).** The Qwen3 experiments (0.6B, 8B, 32B, with/without reasoning) cleanly separate the effects of model capacity and reasoning mode. The finding that a 0.6B model cannot trade off security and utility regardless of reasoning, while 32B matches GPT-4.1, is non-trivial and useful for practitioners.

3. **Memorization test (Section 4.5).** The paper tests whether GPT-4.1 has memorized AgentDojo samples (avg similarity 0.34, only 3.5% above the 0.6 threshold), ruling out a real confound that is rarely addressed in benchmark evaluations of frontier models.

4. **Honest characterization of weaker models.** The paper does not hide that GPT-3.5 performs poorly (FNR 16–68% depending on benchmark) and requires an explicit definition of "prompt injection." This transparency strengthens the central thesis that reasoning capability, not just prompting strategy, is the key factor.

## Weaknesses

### Fatal
None.

### Major

1. **Asymmetric baseline comparison (Table 2).** The comparison pits PromptArmor (using GPT-4.1/4o—frontier models) against baselines that use much smaller models (Deberta, Llama Prompt Guard 2, DataSentinel with Mistral-7B, etc.). The paper acknowledges this implicitly for DataSentinel ("uses Mistral-7B as the guardrail LLM, which has limited reasoning ability") but the table is still framed as "PromptArmor vs. existing defenses," inviting the conclusion that PromptArmor is strictly better. The actual finding is more nuanced: *if you are willing to run a frontier model on every input*, prompting is extremely effective. The Qwen3-32B results (Section 4.4) partially mitigate this by showing that comparable performance is achievable with a 32B open-weight model, but those results are not included in the main comparison table. The paper would be strengthened by adding an inference-cost column or by comparing PromptArmor using similarly-sized models directly against the same baselines in Table 2.

2. **"Computational efficiency" rationale conflates development and inference cost (Section 3.2).** The paper lists "computational efficiency" as a core advantage, arguing it "avoids the significant costs associated with developing and training custom security models." This justification addresses *development* cost, not *inference* cost. Screening every tool-call result through GPT-4.1 could be substantially more expensive at inference time than a fine-tuned small detector. The paper later shows that Qwen3-32B works well, partially supporting the efficiency claim, but the Section 3.2 framing should be revised to explicitly separate the two cost axes.

### Minor

1. **Limited adaptive attack scope (Section 4.6).** The adaptive attack evaluation uses AgentVigil, an automated fuzzing method that modifies attack templates. The paper appropriately qualifies its claim as "robustness against fuzzing-based adaptive attacks." However, a stronger threat model would involve an adversary who knows the guardrail's system prompt and deliberately crafts injections that appear benign to the guardrail while remaining effective against the backend LLM. The robustness claim should therefore be read with this scope limitation in mind.

2. **TensorTrust failures not analyzed.** The FNR on TensorTrust (4.61% for GPT-4o, 2.67% for GPT-4.1) is notably higher than on AgentDojo. TensorTrust contains human-crafted adversarial prompts from a competition, which may be more diverse and harder to detect than template-based attacks. The paper does not discuss what these missed cases look like or what they reveal about boundary conditions. A brief qualitative analysis would strengthen the paper.

### Trivial
None.

## Nice-to-Haves
- An inference cost comparison (e.g., API cost per input for GPT-4.1 vs. Deberta vs. Llama Prompt Guard 2) would let readers directly evaluate the security-utility-cost trade-off.
- Including Qwen3-32B results in the main comparison table (Table 2) would address the asymmetric comparison concern directly.
- 2–3 concrete examples of false negatives from TensorTrust would help clarify the method's boundary conditions.

## Removed Points
- *Adaptive attack criticism (overstated by reviewer):* The original criticism claimed the paper overclaims on adaptive attack robustness, but the paper already qualifies its claim as "fuzzing-based adaptive attacks" (Section 4.6, line 288). Moved to minor with appropriate scope qualification.
- *ASR metric definition concern:* The reviewer noted that partial executions wouldn't be counted as successes. This is the standard ASR definition used in AgentDojo and prior work; it is not a flaw particular to this paper.
- *Fuzzy matching false-match concern (speculative):* The concern about common words causing false matches is speculative, and the paper references appendix code. Scaled back to a minor reproducibility note.

## Novel Insights
The reviews surface one genuinely novel observation that is not simply restating the paper's contributions. The harsh critic notes that the paper's main contribution—showing that prompting works with capable LLMs—inherently implies that model *scale* may matter more than detection *methodology* for this task. If fine-tuned small detectors also improved dramatically when given a large backbone (which the paper does not test), the field's design space shifts: the choice of which approach to use becomes secondary to the choice of which model to deploy. This is an important implication that the paper itself does not fully explore but that follows from its results.

## Suggestions
1. **Revise Table 2** to either include Qwen3-32B results or add an inference-cost column so readers can evaluate the security-cost trade-off directly.
2. **Revise Section 3.2** to explicitly distinguish development cost savings from inference cost, and cite the Qwen3-32B results as evidence that useful efficiency can be achieved with a moderately-sized model.
3. **Add a brief qualitative analysis** of 2–3 TensorTrust false negatives to clarify boundary conditions.

## Score and Decision

**Bracket determination.** Round 1 calibration retrieved anchors across all bands. The paper is clearly above the rejection band (1.5–3.5) and above the borderline band (3.5–5.5). The most relevant comparative anchors are:
- *Baseline Defenses for Adversarial Attacks* (5.25, rejected): Similar "baseline defense" framing but criticized for single-attack evaluation and weak models. Our paper is substantially stronger on both dimensions.
- *GuardAgent* (6.00, rejected): LLM-as-guardrail approach; criticized for limited comparison and task-dependency. Our paper has a sharper contribution and more thorough evaluation.
- *Agent Security Bench* (6.25, accepted): Comprehensive benchmark; broader scope but limited new insights. Our paper's contribution is more focused and its central finding more surprising.
- *Jailbreaking Leading Safety-Aligned LLMs* (6.14, accepted): Strong empirical demonstration; concerns about novelty. Comparable in empirical rigor.
- *Follow My Instruction and Spill the Beans* (6.75, accepted): RAG data extraction; some found the attack obvious. Our paper has a similarly straightforward method but a more impactful finding (reversing a prior negative result).

The Round 1 bracket was **6.0–7.5**. The paper has a clear, well-supported empirical contribution and the weaknesses are fixable without changing the core claims. It is above the acceptance threshold but not at the level of the strongest papers (8+) that introduce novel methodology or substantially broader frameworks.

**Final score: 7.0.** This reflects a solid paper with a focused, well-supported contribution, above the acceptance threshold, with fixable weaknesses that do not undermine the core findings.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>