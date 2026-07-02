## Summary

The paper investigates whether current SAE-based interpretability tools (GemmaScope, Goodfire) can detect and control deception in LLMs. It uses two testbeds: "Secret Agenda" — a single-turn prompted roleplaying scenario where models are given a narrative context that incentivizes lying (tested across 38 models) — and Insider Trading compliance scenarios analyzed via dual SAE architectures. The main findings are that autolabeled deception features rarely activate during Secret Agenda lies and fail to prevent lying via steering, while unlabeled aggregate activations in the Insider Trading domain show discriminative patterns between refusal and engagement responses.

## Strengths

- **Tests a timely and practically relevant question.** The paper directly evaluates whether auto-labeled SAE features (GemmaScope, Goodfire) labeled as "deception-related" actually correspond to deceptive behavior and whether they can causally control it via steering (Section 6). This negative evidence — that these features neither activate reliably during lying nor support effective steering — is a potentially useful finding for the interpretability community if properly supported.

- **Broad model coverage.** Testing 38 models across families (Gemma/Gemini, Claude, Llama, OpenAI, Qwen, DeepSeek, etc.) strengthens the universal-elicitation claim. Section 5.2's demonstration that all tested models lie at least once under the Secret Agenda framing is a clean empirical observation, regardless of how one interprets the paradigm.

- **The contrastive two-testbed design is conceptually useful.** Juxtaposing a political-gameplay domain where labeled features fail against a structured-compliance domain where unlabeled aggregate activations show separation provides a reasonable framework for surfacing limitations of current auto-labeling approaches.

## Weaknesses

### Fatal
None.

### Major

- **The Secret Agenda paradigm tests prompted narrative-following, not the kind of "strategic deception" the paper claims.** The setup (Section 5.1) gives the LLM a synthetic transcript describing a game state and asks it to respond at a decision point where lying is described as the winning strategy. This is a single-turn roleplaying task, not a multi-agent interaction where the model plans, acts, and experiences consequences. The paper repeatedly uses language like "strategic lying," "scheming," "carefully planning manipulative strategies" (Section 3, abstract) to describe this behavior. But the paradigm does not require multi-step planning or genuine agency — prior work it situates alongside (Scheurer et al. 2024 — interactive trading; Meinke et al. 2024 — chain-of-thought planning; Greenblatt et al. 2024 — alignment faking) involves qualitatively richer agency with experienced consequences. The most parsimonious explanation for why 38/38 models "lie" is that instruction-tuned models follow the implied behavior in a narrative context. This does not invalidate the SAE findings, but it means the paper's core framing significantly overclaims what the paradigm demonstrates.

- **No control condition tests whether lying depends on the incentive structure versus the narrative framing.** The paper never tests a condition where truth-telling is the winning strategy. Without this, we cannot attribute the lying to the incentive manipulation — it could reflect a bias toward dramatic responses, generic narrative-following, or some other confound. The existing prompt variations (Snails/Slugs, Day/Night, Pink/Turquoise, Section 5.3) vary surface-level naming but not the incentive structure itself. A truth-telling-incentivized condition is the minimum control needed for the claim that "deception advantaged goal achievement" (abstract) drives the behavior.

- **The Insider Trading analysis's claimed signal may reflect topic separation rather than compliance separation.** The top discriminative features listed in Table 1 ("Quantity fields in structured data," "Securities market regulation," "Financial trading transactions," "Trade execution code patterns") are domain-level topic features. The t-SNE separation between refusal and engagement clusters (Figure 4) could simply reflect that refusal responses contain compliance language ("I cannot help with that") while engagement responses contain financial terminology. The paper offers no analysis — e.g., matching on response topic, vocabulary distribution controls, or within-topic comparisons — to rule out this confound. The paper contrasts "Secret Agenda fails" with "Insider Trading succeeds," but the two testbeds evaluate different constructs (compliance in a structured domain vs. deception in a social game), making the contrast less informative than claimed.

### Minor

- **Feature steering experiments lack a manipulation check.** Section 6.3 reports that steering deception-related features to -1 or +1 did not prevent lying, but there is no direct evidence that the steering intervention actually altered the target features' activations in the model's forward pass. The paper includes a positive control (steering "bananas and banana-related concepts" successfully suppressed banana mentions), which shows the steering mechanism *can* work for topical concepts. However, this does not verify that the deception-labeled features were effectively steered — the negative finding could equally reflect wrong features, insufficient magnitude, or distributed computation. Measuring feature activation levels before/after steering would clarify this.

- **Small and uneven sample sizes limit the paper's quantitative claims.** The paper acknowledges n=2–30 per model with no confidence intervals and "error bars omitted due to insufficient trials" (Figure 1 caption). Grok had only 2 surviving trials out of 10. The claim "Secret Agenda reliably induced lying across all model families" (abstract) is supported in the universal-elicitation sense (38/38 models lied at least once) but cannot support claims about rates or reliability of the behavior. The paper's Section 8.1 transparency is commendable, but the abstract's wording still overstates what the data can quantify.

- **No prompt examples in the main text.** The paper describes the Secret Agenda setup but never shows an actual prompt. This makes it difficult for readers to independently assess whether the task involves "strategic deception" or narrative roleplaying.

- **No classification criteria or inter-rater agreement reported for Secret Agenda response types.** The paper distinguishes "truth," "partial or partial lie," and "lie" outcomes (Figure 1) but does not specify the classification scheme or whether any reliability measure was computed. Section 8.3 remarks that classification requires human judgment, but the methodology for making these judgments is not described.

### Trivial
None.

## Nice-to-Haves
- Adding a truth-telling-incentivized control condition for Secret Agenda would substantially strengthen the causal claim about incentive-driven deception.
- Reporting quantitative steering results (proportion of trials lying with vs. without steering, per tested feature) would make the negative finding more informative.
- A within-topic analysis for the Insider Trading data (e.g., comparing engagement vs. refusal responses using similar vocabulary) would address the topic-separation confound.
- Larger per-model sample sizes and confidence intervals would support stronger quantitative claims about deception rates.

## Removed Points

These points are flagged to be removed, treat them with caution:
- The critic's concern about RL reward hacking comparisons (Trackmania AI, block-flipping robot) being misleading is removed because the paper explicitly frames these as motivational examples (Section 3.1, Section 4) of how deception emerges under incentive pressures, not as direct methodological analogies.
- The critic's framing that the Insider Trading analysis is about "deception detection" rather than "compliance detection" is partly inaccurate — Contribution 4 explicitly says "compliance detection," though the abstract does say "separated deceptive versus compliant responses." This is a framing inconsistency in the paper itself, not an error in the review.
- The critic's standalone point about "no quantitative steering results" is subsumed into the manipulation-check weakness; the paper does provide qualitative descriptions and references external screenshots (DeLeeuw, 2024), so the criticism is not that results are absent but that they lack verification.

## Novel Insights

The core insight from the harsh critic — that the Secret Agenda paradigm may be better understood as a narrative roleplaying task than as a test of strategic deception — is a genuine and important methodological concern that the paper does not adequately address. The paper's failure to include a truth-telling-incentivized control condition is a critical evidential gap that severely limits what can be concluded about incentive-driven deception. Beyond these points, most of the reviewer's observations (small sample sizes, lack of manipulation checks for steering, topic-level confound in Insider Trading) are standard methodological concerns that the paper partially acknowledges but does not resolve.

## Suggestions

1. Either (a) redesign the Secret Agenda paradigm to involve genuine multi-turn agency with experienced consequences (actual game play, not narrated transcripts), or (b) clearly reframe the paper's claims to match what the paradigm actually tests — "narrative-elicited lying" rather than "strategic deception."
2. Add a control condition where truth-telling is the winning strategy to establish that the incentive structure, rather than the narrative framing, drives the behavior.
3. Include a manipulation check for feature steering: measure feature activation values before and after steering to verify the intervention is effective.
4. Provide within-topic analyses for the Insider Trading data to rule out the vocabulary-distribution confound.
5. Report quantitative steering results (proportions per feature) and classification criteria for Secret Agenda response types.

## Score and Decision

### Calibration Anchors

| Path | Avg Human Score | Round | Comparison |
|------|--------|-------|------------|
| Tall Tales at Different Scales (deception in LMs) | 3.67 | 2 | Similar topical area, similar breadth-of-models strength, similar critique about paradigm not matching claims. Our paper has weaker stats but a more focused question. |
| Decomposing the Dark Matter of SAEs | 3.50 | 2 | Technical SAE analysis rejected for narrow scope (one model, one layer). Different paper type but same score band. |
| Too Big to Fool (resisting deception) | 4.25 | 2 | More polished experiments, clear methodology. Our paper has more fundamental paradigm issues. |
| SAE Interpretability with Mutual Information | 5.00 | 1&3 | Clear method with quantitative results on two benchmarks, still rejected. Our paper is substantially weaker methodologically. |
| AgentHarm (safety benchmark) | 6.75 | 1 | Well-executed benchmark with 440 tasks, multi-step evaluation. Our paper is far less rigorous. |
| NEMESIS (jailbreaking) | 1.40 | 1 | Broken/non-paper. Our paper is better than this. |
| Systematic Review of LLMs | 1.00 | 1 | Survey paper with no contribution. Our paper has some empirical content. |

**Round 1 Bracket:** 3.0–5.0 (initially considered SAE paper at 5.0 as upper anchor)

**Narrowing:** Comparing to the SAE interpretability paper (5.00) — that paper had a clear, novel method with theoretical grounding, quantitative evaluations on two benchmarks, and reproducible experiments. Our paper lacks quantitative results for its central experiments, has a paradigm validity concern, and reads more like a preliminary investigation. Comparing to "Tall Tales at Different Scales" (3.67) — similar mix of ambition and methodological concerns, similar breadth of models, similar paradigm questions. Our paper is slightly weaker due to the more fundamental paradigm issue and smaller per-model sample sizes. Final score lands at 3.5.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>