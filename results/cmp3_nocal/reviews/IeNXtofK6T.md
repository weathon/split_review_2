Now I have all the evidence I need. Let me write the final consolidated review.

## Summary

This paper revisits the previously dismissed idea of using an off-the-shelf LLM to detect and remove prompt injection attacks. The authors propose PromptArmor, a simple guardrail that prompts a modern LLM to identify injected text in data samples and removes it via fuzzy matching. Evaluated on three benchmarks (AgentDojo, Open Prompt Injection, TensorTrust) with GPT-3.5, GPT-4o, GPT-4.1, and the Qwen3 family, the paper shows that with strong modern LLMs (GPT-4o, GPT-4.1, Qwen3-32B), this simple approach achieves very low false positive and false negative rates — e.g., FPR 0.56% and FNR 0.13% on AgentDojo with GPT-4.1 — and reduces attack success rate from 54.53% to 0.00%.

## Strengths

- **Compelling quantitative results on AgentDojo.** PromptArmor-GPT-4.1 achieves 0.56% FPR and 0.13% FNR on AgentDojo (Table 1), and reduces ASR from 54.53% (undefended) to 0.00% (Table 2). These are striking improvements over prior results and over all seven baselines tested.

- **Thorough ablation on model scale vs. reasoning mode.** The Qwen3 experiments (Section 4.4, Figure 3) are the most informative part of the paper. Showing that reasoning mode helps mid-sized models (Qwen3-8B: FNR drops from 26.50% to 15.78%) but cannot rescue too-small models (Qwen3-0.6B: FNR 75.71% with reasoning), and that Qwen3-32B achieves near-perfect results without reasoning, provides useful practical guidance and disentangles the roles of scale and reasoning.

- **Data contamination check.** The memorization test (Section 4.5) is a necessary sanity check given that benchmark data could plausibly have been encountered during training. Average similarity of 0.34 with only 3.5% above threshold strengthens confidence that results reflect genuine detection capability.

- **Well-structured evaluation across multiple benchmarks.** The paper evaluates on three diverse benchmarks (AgentDojo for agents, Open Prompt Injection and TensorTrust for non-agent settings), and compares against seven existing defenses spanning four categories. This breadth supports the claim that the finding is not benchmark-specific.

## Weaknesses

### Fatal
None.

### Major

- **Adaptive attack claim is broader than the evidence supports.** The introduction states that PromptArmor "is robust against adaptive attacks specifically designed to circumvent it" (Section 1, last paragraph). However, the adaptive attack evaluation (Section 4.6) tests only a single automated red-teaming framework (AgentVigil) that generates attacks via fuzzing-based template optimization. The results section itself acknowledges this by saying "fuzzing-based adaptive attacks." Known evasion techniques for LLM-based classifiers — paraphrasing, encoding obfuscation, split-injection across data fields, or directly targeting the guardrail's output format — are not tested. The paper should either (a) qualify the claim in the introduction to match the evidence (e.g., "robust against fuzzing-based adaptive attacks"), or (b) conduct a broader adaptive evaluation. As written, the introduction overclaims.

- **Detection prompt is adjusted per dataset without specification.** Section 4.1 states "Given the varying settings of the benchmarks, we adjusted the detection prompt for each dataset" — a single sentence with no detail about what was adjusted, how, or why. This is a non-trivial design choice: if the prompt was substantively adapted per benchmark, it could affect claims about generalizability. The paper should specify what adjustments were made and justify that they do not undermine the approach's generality.

### Minor

- **Section 3.2 ("Design Rationale") inflates the presentation.** The four paragraphs describe generic properties of any API-based guardrail LLM — modularity, generalization, computational efficiency, benefiting from LLM improvements — rather than specific design decisions of PromptArmor. These are properties of *the LLM it calls*, not of PromptArmor itself. The system prompt (Figure 2) is a standard instruction format. Condensing this section would bring the presentation into better alignment with the paper's technical content.

- **No discussion of inference cost or latency.** The paper positions PromptArmor as a "standard baseline" and "practical" defense, yet provides no analysis of the cost or latency of using GPT-4.1 as a real-time guardrail. A guardrail that doubles API calls and uses a frontier model for every data sample may be impractical in many deployment scenarios. The Qwen3-32B results (near GPT-4.1 performance at much lower cost) partially address this, but the paper does not draw the connection or provide any cost comparison.

- **No error analysis by attack type.** AgentDojo includes four distinct attack types (Ignore Previous, System Message, Important Messages, Tool Knowledge), but only aggregate metrics are reported. Some attack types may be systematically harder to detect, and knowing which would be valuable for practitioners and for understanding the limits of prompting-based detection.

- **Limited model family diversity for a "standard baseline" claim.** Only OpenAI models (GPT-3.5, GPT-4o, GPT-4.1) plus one open-source family (Qwen3) are tested. For a paper arguing that this should be a universal baseline, results on Claude or Gemini would substantially strengthen the claim that the finding generalizes across alignment/post-training approaches.

### Trivial

- **The 3.5% memorization rate (~22 samples out of 629) is noted but not discussed.** While low, the paper could discuss whether these ~22 near-memorized samples could influence the aggregate results. This is a minor omission from an otherwise careful analysis.

## Nice-to-Haves

- **Error analysis by attack type on AgentDojo** (already noted as a weakness; expanding here as a concrete improvement direction). The four attack types likely differ in detectability; reporting per-type breakdown would increase practical value.

- **Direct evaluation of sanitization quality.** The paper frames detection+removal as an improvement over prior work that only discards detected inputs, but does not evaluate the fuzzy matching removal step itself — e.g., does it ever remove non-injection content or leave fragments that confuse the backend LLM? The end-to-end UA metric partially captures this but a direct evaluation would strengthen the claim.

- **Deeper analysis of *why* modern LLMs succeed.** The paper attributes improvement to "reasoning capabilities" in the abstract and introduction, while the Qwen3 analysis shows model scale is the primary driver. A careful error comparison (what does GPT-4.1 catch that GPT-3.5 misses? what types of injections are still missed on TensorTrust?) would provide more insight than is currently offered.

- **Claude and Gemini evaluations** to test the generality of the finding across model families.

## Removed Points

These points were flagged by the harsh critic review but are removed under the filtering guidelines:

1. **"Paper is presented as a method paper when contribution is empirical"** — Partially removed. The paper explicitly frames itself as revisiting a known idea ("we revisit this idea," "should be regarded as a standard baseline"). However, the observation about Section 3.2's inflated presentation is retained as a Minor weakness above.

2. **"The finding confirms what one would reasonably expect / is not surprising"** — Removed as subjective opinion. Prior work (Liu et al., 2024) explicitly found this approach ineffective, making the positive result non-obvious.

3. **"Paper should acknowledge prior work used GPT-3.5"** — Removed as factually incorrect. The paper already states: "these benchmark results, conducted in 2023, were based on older LLMs with weaker reasoning capabilities" (Section 1).

4. **"Paper attributes improvement entirely to reasoning capabilities"** — Removed as a misreading. The Qwen3 analysis (Section 4.4) explicitly states "sufficient model capacity appears to be the primary factor."

5. **"2-5% FNR on TensorTrust is problematic in a security context"** — Removed as commentary rather than a weakness of the paper. The paper reports these numbers transparently; the observation does not identify an error or omission.

6. **Criticisms rooted in stripping-guided speculation** (e.g., claims about unknown missing appendix content or unverifiable model availability) — Removed per guidelines.

## Novel Insights

None beyond the paper's own contributions. The reviews surface the adaptive-claim mismatch and the dataset-specific prompt adjustment as the most significant issues, but these are observations about the paper's presentation and evidence scope rather than novel analysis of the underlying problem.

## Suggestions

1. **Qualify the adaptive attack claim in the introduction** to match the evidence: "robust against fuzzing-based adaptive attacks" rather than the current unqualified claim.

2. **Disclose what "adjusted the detection prompt for each dataset" means** — either specify the adjustments or confirm they were minor and provide the exact prompts used.

3. **Add a brief cost/latency analysis** showing the inference cost of GPT-4.1 vs. Qwen3-32B vs. fine-tuned small models, to support the "practical baseline" framing.

4. **Include per-attack-type breakdown** for AgentDojo results; this is already collected data that would add value at no experimental cost.

5. **Condense Section 3.2** to one paragraph, since the four "design rationale" points describe properties of the underlying LLM rather than design decisions.

## Score and Decision

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>