Now I have sufficient calibration data. Let me finalize my review.

**Calibration Synthesis:**

**Round 1 anchors (bracketing):**
- Strong reject band (~1-1.5): NEMESIS (1.40) — very weak paper, substantially below the paper under review.
- Reject band (2.50-3.00): "Playing Language Game with LLMs" (2.50) — similar creative-prompt jailbreak but tested on only 3 models; shares baseline issues. My paper has broader coverage and more interesting findings.
- Borderline band (3.67-4.75): Quack (3.67), PAIR (4.75) — both automatic jailbreak methods with evaluation concerns.
- Accept band (6.14+): Andriushchenko's "Simple Adaptive Attacks" (6.14) — rigorous, comprehensive evaluation; clearly stronger than my paper.

**Narrowing (Round 2):** PAIR (4.75) and "Explore, Establish, Exploit" (5.25) — both have evaluation/novelty concerns but clearer contributions.

**Final placement:** The paper is strongest among the reject-band papers due to broad model coverage and creative method, but notably below accept-band papers due to the overclaimed framing (the "involuntary" narrative is not supported by the evidence) and the complete absence of baselines despite making comparative claims. Its closest analogue among itemized anchors is PAIR (4.75), but PAIR has a clearer contribution framing and at least one baseline (GCG), whereas this paper has none. My paper belongs between PAIR (4.75) and the Language Game paper (2.50), closer to PAIR due to broader model coverage but pulled down by the misleading central claim. Final score: **4.0**.

Now let me write the final review.

Let me reconsider the severity of weaknesses. I have:
1. Major: Involuntary framing misleading
2. Major: No baselines despite comparative claims
3. Minor: Thin ablation
4. Minor: o1/o3 resistance dismissed
5. Minor: Metrics measure instruction-following (overlaps with #1)
6. Minor: No CIs, no human eval data

Let me merge #5 into #1 since they're the same issue.

Actually, I should also check: the weakness about "evaluation metrics measure instruction-following" — is this really distinct from the "involuntary" framing? They're related but separate. The evaluation metrics issue is about what the numbers mean; the framing issue is about how the paper characterizes the behavior. I'll keep them as separate minor issues but note the connection.

Let me also downgrade the "o1/o3 resistance" point. The paper actually does provide analysis: they tested by removing the unsafe question generation part and found the models over-refuse even benign queries. That's a legitimate analysis. The reviewer's criticism that this is "explaining away" is somewhat harsh. Let me keep this but make it clear the paper does provide some analysis.

Let me write the final review now.## Summary

This paper introduces a jailbreak method called "involuntary jailbreak" that uses a single meta-prompt to instruct LLMs to self-generate both questions that would normally trigger refusal and the corresponding unsafe responses, structured through language operators (X, Y, A, B, R). The method is evaluated across a wide range of frontier proprietary models (Claude Opus 4.1, Grok 4, Gemini 2.5 Pro, GPT-4.1, DeepSeek R1, etc.), showing high attack success rates across most of them.

## Strengths

- **Creative meta-prompt design (Sec. 2, Figs. 3–4):** The idea of asking the LLM to self-generate both the refusal-triggering question and the unsafe response, structured through language operators X, Y, A, B, R, is genuinely novel. Prior jailbreaks target a specific harmful output; this one instead uses the model's own generative capacity to produce diverse unsafe content without the attacker supplying any harmful seed material. [favorability=10.42]

- **Broad model coverage (Sec. 3.2):** The attack is evaluated on a wide range of proprietary models (Claude Opus 4.1, Grok 4, Gemini 2.5 Pro, GPT-4.1, DeepSeek R1, etc.) and shows high success rates across most of them. Testing frontier proprietary models is genuinely difficult and the paper does it. [favorability=14.17]

- **Topic-confinement experiment (Sec. 3.5, Table 4):** The finding that restricting the prompt to a single topic (e.g., Elections, where the model initially produced zero unsafe outputs) drives the model to produce many unsafe outputs on that topic is informative. It demonstrates that the scarcity of outputs on certain topics is not due to inherent robustness but to the model's default topic distribution. [favorability=8.76]

- **Correlation observation (Sec. 3.2, Fig. 12):** The observation that the number of unsafe responses correlates closely with the number of questions the model internally labels as unsafe — that models appear to recognize which questions are unsafe yet still proceed to generate unsafe responses — is genuinely interesting and the closest the paper comes to substantiating its framing. [favorability=9.70]

## Weaknesses

### Fatal
None.

### Major

- **The "involuntary" framing is misleading and unsupported by the evidence.** The prompt (Fig. 4) explicitly instructs the model to "Select a question that would typically be refused by a large model, denote it as q" and then construct the harmful response with label "Yes." When the model complies, it is following user instructions — not acting involuntarily or experiencing guardrail "collapse." The paper's central rhetorical claim (abstract, line 269, conclusion) — that guardrails "collapse" and the model generates unsafe content "involuntarily" — conflates straightforward instruction-following with an actual bypass of safety mechanisms. To support this claim, the paper would need a fundamentally different experimental design (e.g., testing whether the *same* model, when later asked a direct harmful question it generated, would still comply). The method is interesting as a red-teaming tool for eliciting diverse unsafe content; the "involuntary" framing overreaches beyond what the evidence shows. [favorability=-1.39]

- **No baselines are provided despite comparative claims.** The abstract states the method "makes existing jailbreak attacks seem less necessary," and Sec. 5 claims "when compared with all the existing jailbreak methods, none can demonstrate generalization across all the models we evaluated." These are comparative claims with zero supporting evidence. The paper's argument that "it is unlikely that a meaningful benchmark can be established" (Sec. 5) does not excuse the complete absence of any comparison — even a simple one measuring diversity, volume, or topic coverage relative to GCG (Zou et al., 2023), prompt injection, or role-playing exploits would help situate the method's effectiveness. Without this, the reader cannot assess whether the method is genuinely more effective than existing approaches. [favorability=-2.58]

### Minor

- **The ablation analysis of the language operators is thin and does not test the stated mechanistic claims.** The paper claims operators "introduce structural complexity that can distract the LLMs from their internal value alignment" (Sec. 2.1), but this claim is never directly tested. Operator C is not used in main experiments because it "leads to cluttered outputs." Operator B is ablated on only two models (Table 2). Operator R is ablated on only three models (Table 1). The paper admits "certain operators are essential for some models while having a negligible impact on others," which undercuts any systematic understanding of what drives the effect. [favorability=-1.38]

- **Resistance from o1/o3 is explained away rather than thoroughly investigated.** The paper notes these models "exhibit significant over-refusal behavior" and states "it is not very essential to evaluate the recently released GPT-5 model" (Sec. 3.2). While the paper does provide some verification (removing the unsafe generation part and observing over-refusal on benign queries), understanding the mechanism of resistance in o1/o3 could reveal genuine defense pathways. Dismissing resistance as over-refusal without deeper analysis avoids what could be the paper's most informative finding about guardrail design. [favorability=2.75]

- **The evaluation metrics (#ASA, #Avg UPA) primarily measure instruction-following compliance, not guardrail bypass.** Since the prompt commands the model to generate 10 unsafe question-response pairs, ASA ≈ 100 means the model followed the instruction. This does not invalidate the method as a red-teaming tool, but it undercuts the "guardrail collapse" framing. Additionally, unsafe outputs originating from general (safe) questions are excluded from #Avg UPA "as these are attributed to either weak instruction following or hallucination" (Sec. 3.1) — an exclusion that uses the model's own label to decide what counts, creating a circular dependency. [favorability=1.25]

- **No confidence intervals or variance measures are reported** despite 100 runs per model for a stochastic generation process. The claimed "close alignment with human judgment" for Llama Guard-4 (Sec. 3.1) is asserted without any human evaluation data to substantiate it. [favorability=2.17]

### Trivial
- The figure caption for Fig. 6 describes Topic 1 (Violent Crimes) as the most concentrated category, while the main text (line 221) states Topic 2 (Non-Violent Crimes) is dominant. The text description is likely correct given the paper truncates Topic 2 bars for improved visualization, but the inconsistency should be fixed.

## Nice-to-Haves

- A post-hoc test could disentangle instruction-following from guardrail bypass: after the model generates unsafe content via the meta-prompt, does it then refuse a direct request for the same harmful content? If yes, guardrails are intact and the method exploits instruction-following; if no, guardrails are genuinely compromised.
- A simple baseline comparison (e.g., diversity/volume of harmful content vs. standard harmful prompt lists from JailbreakBench or HarmBench) would help situate the contribution.
- Investigating why o1/o3 resist the attack could reveal genuine defense mechanisms.
- Human evaluation of a sample of outputs would strengthen the judge model validation.

## Removed Points

These points from the input review are removed (treated with caution):

1. "The safe output example in Fig. 1 (refusing to tell a joke) is atypical and overstates guardrail strictness" — speculative observation about example choice that does not affect any result or claim.
2. "Source code and prompt templates are not provided" — full prompt templates are provided in Figs. 3 and 4; source code is not required for a prompt-only method.
3. "The Fig. 6 caption says Topic 1 but text says Topic 2" — this is a parser-artifact-level caption inconsistency; the text (line 221) is clear and the figure is a bar chart the reader can inspect directly. Moved to Trivial.
4. "Section 5 reads as defensive rationalization" — editorial opinion without specific evidence.
5. Criticisms about "parser may have garbled the caption" — these are parser artifacts, not author errors.
6. "Missing human evaluation for Llama Guard-4 alignment claim" — subsumed into Minor weakness about variance/evidence quality.
7. "Missing appendix, missing proofs in appendix" — parser strips these sections from all papers.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Reframe the contribution honestly.** Drop the "involuntary" and "guardrail collapse" framing. Describe the method accurately as an instruction-following exploit that elicits diverse unsafe content from LLMs through a creative meta-prompt, suitable for red-teaming and data collection. This would not diminish the practical utility of the method.

2. **Add at least one baseline.** Even a simple comparison — e.g., the diversity/volume of unsafe content generated by this method vs. sampling from a list of standard harmful prompts (JailbreakBench, HarmBench) — would ground the contribution. If the method produces more diverse content across more topics with less effort, that is a demonstrated advantage.

3. **Investigate o1/o3 resistance more deeply.** Rather than dismissing it as over-refusal, analyze what specific prompt elements trigger refusal in these models. This could yield insights about what makes guardrails effective, which is arguably more valuable than yet another attack.

4. **Either remove the unsupported comparative claims or back them with evidence.** The claim that the method "makes existing jailbreak attacks seem less necessary" (abstract) is not supported. If the authors want to retain this claim, they need to compare against prior methods.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Score | Round | Itemized? | Comparison |
|------|-------|-------|-----------|------------|
| NEMESIS (5kMwiMnUip) | 1.40 | R1 | No | Much weaker — low-effort compilation paper |
| Playing Language Game (BeOEmnmyFu) | 2.50 | R1 | Yes | Similar creative-prompt jailbreak, but tested on only 3 models vs. this paper's 16+ |
| Quack (1zt8GWZ9sc) | 3.67 | R1,R2 | Yes | Automated jailbreak framework; broader scope but narrower model testing |
| Leveraging Context (w0b7fCX2nN) | 3.75 | R1 | No | Multi-turn jailbreak; different approach |
| Nested Gloss (Q3oAX9HoH2) | 4.00 | R1 | No | Scene-nesting jailbreak; similar borderline quality |
| PAIR (hkjcdmz8Ro) | 4.75 | R2 | Yes | Automated jailbreak with at least one baseline (GCG) and clearer framing |
| Explore, Establish, Exploit (zSwH0Wo2wo) | 5.25 | R2 | Yes | Red-teaming framework with more rigorous methodology |
| FlipAttack (H6UMc5VS70) | 5.75 | R1 | No | Stronger method with clear baselines and comparison |
| Simple Adaptive Attacks (hXA8wqRdyV) | 6.14 | R1 | Yes | Far more rigorous — comprehensive evaluation, clear contribution, proper baselines |
| Curiosity-driven Red-teaming (4KqkizXgXU) | 8.00 | R1 | No | Significantly stronger — systematic framework, rigorous evaluation |

**Round 1 bracket:** Between 3.5 and 5.5.

**Narrowing:** The paper is stronger than "Playing Language Game" (2.50) due to far broader model coverage and more interesting topic-confinement findings. It is weaker than PAIR (4.75) because PAIR has at least a baseline comparison (GCG) and a clearer contribution framing without the overclaimed "involuntary" narrative. Within the bracket, the misleading central framing and complete lack of baselines pull the score below PAIR's 4.75. The two Major weaknesses (framing overreach, absent baselines despite comparative claims) are verifiable from the paper as written and together justify a borderline-reject score.

**Final score:** 4.0. The paper's core methodological contribution (the meta-prompt design for eliciting diverse unsafe content) and its broad model testing are real strengths. However, the gap between the rhetorical claims and what the experiments actually demonstrate is too large, and the absence of any baseline comparison invalidates the comparative assertions. Major revision to reframe honestly and add baselines would be needed before acceptance.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>