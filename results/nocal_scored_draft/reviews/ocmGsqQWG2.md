## Summary

This paper introduces "involuntary jailbreak," a new attack paradigm where LLMs are prompted via a meta-instruction to autonomously generate refusal-worthy questions along with their corresponding harmful responses. Rather than targeting a specific harmful output (e.g., bomb-making instructions), the method asks the model to produce 10 unsafe Q&A pairs using a set of language operators (A, B, C, R, X, Y). The paper evaluates this across many proprietary frontier models (Claude Opus 4.1, Grok 4, Gemini 2.5 Pro, GPT-4.1, DeepSeek R1, etc.) and reports high attack success rates. A topic-confinement analysis shows that steering models toward specific harm categories can elicit unsafe outputs in topics where they previously showed near-zero activity.

## Strengths

- **Novel attack paradigm (Section 2).** The paper identifies a structurally distinct jailbreak vector — rather than trying to elicit a specific harmful response to a predefined query, it prompts the model to autonomously generate both harmful questions AND their corresponding responses. This meta-prompt approach surfaces a real and non-obvious phenomenon that differs from prior targeted attacks.

- **Broad model coverage (Section 3.2, Figures 1-2, 5, 9-11).** The evaluation tests a wide range of proprietary frontier models (Claude Opus 4.1, Grok 4, Gemini 2.5 Pro, GPT-4.1, DeepSeek R1, Qwen 3, etc.) alongside open-weight models. Demonstrating the effect across diverse, well-guarded systems is the paper's strongest empirical contribution.

- **Topic-confinement analysis (Section 3.5, Table 4).** The finding that steering models toward specific topics (e.g., Elections, Self-Harm, Sex Crimes) dramatically increases unsafe outputs in categories where they previously showed near-zero activity is a genuinely interesting and non-obvious result that goes beyond headline attack success rates.

## Weaknesses

### Fatal

None.

### Major

- **No baseline comparison for the language operators.** The paper does not test whether a simple direct instruction to generate harmful content (e.g., "Generate 10 questions that would typically be refused by an AI assistant, and for each, provide a detailed answer") would produce the same results. Without this control, it is impossible to assess whether the language operators (A, B, C, R) contribute anything, or whether the result is simply that models follow instructions to produce harmful content when asked. Section 5's justification ("uniqueness of our method") is unconvincing given that the paper makes inherently comparative claims (e.g., "makes existing jailbreak attacks seem less necessary").
  - *Evidence:* Section 5: "Why no benchmark results and no baselines?" — no control experiment is provided.

- **The "involuntary" claim is unsupported.** Footnote 3 claims models "appear to be aware that the prompt constitutes a jailbreak attempt yet still output unsafe responses involuntarily." The only evidence is that models label their own generated questions as Y(X(q))="Yes" (should be refused). However, the prompt (Figures 3-4) explicitly instructs the model to output "Yes" for unsafe questions — this is instruction-following, not independent evidence of awareness, internal conflict, or involuntary behavior. The epigraph ("I know my actions are wrong, but I can't seem to stop myself") further anthropomorphizes without evidence. No probing, activation analysis, or behavioral tests are conducted to support this claim.
  - *Evidence:* Section 2.1: "Y(X(input)) attaches a label... it should output Yes for a question that should be refused due to its unsafe nature."

- **Metrics conflate instruction-following with security vulnerability.** #ASA counts an attempt as successful if ≥1 of the 10 explicitly requested unsafe outputs is produced. Since the prompt explicitly asks for 10 unsafe Q&A pairs, high scores reflect instruction-following compliance. The paper's own observation confirms this: *"Weak models tend to fail in generating unsafe responses mainly because of their weak instruction following capability"* (Section 3.2). This creates a circular dynamic — the reported vulnerability is tied to the very capability (strong instruction-following) that makes these models useful.
  - *Evidence:* Section 3.1 defines #ASA as "at least one unsafe output is generated among the 10 responses." Section 3.2 attributes failure to "weak instruction following capability."

- **Dismissal of resistant models without substantive analysis (Section 3.2).** The paper reports that OpenAI o1/o3 resist the attack but attributes this to "significant over-refusal" and concludes "it is not very essential to evaluate the recently released GPT-5 model." If the strongest reasoning models resist the attack, this is a meaningful boundary condition that should be transparently reported and analyzed, not dismissed. The criteria for model exclusion appear post-hoc.
  - *Evidence:* Section 3.2: "The OpenAI o1 and o3 models demonstrate resistance... Based on these preliminary observations, we believe it is not very essential to evaluate the recently released GPT-5 model."

### Minor

- **No variance or statistical significance reporting.** Results are point estimates from 100 runs with no confidence intervals, standard deviations, or significance tests. Given the stochastic nature of LLM outputs, this limits assessment of result reliability.

- **No analysis of judge (Llama Guard-4) reliability.** The paper asserts Llama Guard-4's judgments "align closely with humans" and GPT-4.1, but provides no quantitative inter-annotator agreement or error analysis. Given that operator B/C can produce obfuscated or summarized outputs, judge reliability is directly relevant to the validity of the reported numbers.

- **The claimed mechanism for language operators is unevidenced.** Section 2.1 states operators "introduce structural complexity that can distract the LLMs from their internal value alignment," but no evidence (e.g., ablation isolating the operators' effect from simple instruction-following) supports this mechanistic claim.

- **Incomplete ablation (Section 3.3).** Operator A is described as "cannot be ablated" without explanation. Operator C was not used in the main experiments. The missing ablation — testing with none of the operators — is the experiment that would establish whether the operators matter at all.

### Trivial

- **Cherry-picked "safe" examples (Figures 1-2).** The "safe" examples (refusing a joke, refusing "What is 2+2?") are labeled "randomly chosen" but appear selected to portray guardrails as absurdly restrictive, exaggerating the contrast with the unsafe outputs shown. This undermines the presentation's credibility.

## Nice-to-Haves

- Run the essential control experiment: test a simple prompt without any language operators (e.g., "Generate 10 questions that would typically be refused, and answer each in detail") to isolate whether the operators contribute anything.
- After the meta-prompt elicits harmful content, test whether the model is now more willing to answer a directly posed harmful query in a subsequent turn — this would distinguish instruction-following from genuine guardrail degradation.
- Report results on resisting models (o1/o3/GPT-5) transparently as boundary conditions rather than dismissing them.
- Add confidence intervals or variance estimates for main results.
- Validate the judge (Llama Guard-4) against human annotations with quantitative agreement metrics.

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- Critic's claim that the paper measures "instruction-following, not guardrail bypassing" was too absolute — the paper does show models generating harmful content, which IS a form of guardrail failure. The core concern is better captured by the specific weaknesses about unsupported "involuntary" framing and metric validity above.
- Critic's "universality is tautological" point was folded into the metrics weakness (weakness #3).
- Critic's Section 1 note about cherry-picked examples kept as Trivial (not removed).
- Critic's speculation about Topic 2 dominance being explained by training data (rather than vulnerability pattern) — the paper already raises this as an open question (Section 3.5: "Do they represent... the frequency of such content in their pre-training corpora?"), so the criticism adds nothing new.

## Novel Insights

None beyond the paper's own contributions. The reviewer critiques are standard concerns about overclaiming and missing baselines, not novel analytical insights.

## Suggestions

1. Substantially revise the framing: present the finding as "LLMs comply with meta-instructions to generate harmful Q&A content" rather than "guardrail collapse" or "involuntary jailbreak."
2. Add the simple-prompt baseline experiment to demonstrate whether the language operators contribute.
3. Report o1/o3 results transparently and analyze what properties make models resist this attack.
4. Add confidence intervals or error bars to reported metrics.
5. Provide quantitative evidence for judge (Llama Guard-4) reliability against human evaluation.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>