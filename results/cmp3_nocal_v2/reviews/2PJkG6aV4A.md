Here is the final consolidated review.

## Summary

This paper proposes a guardrail-agnostic method for measuring societal bias in LVLMs. The core idea is to replace attribute-inferring prompts (which trigger refusals in safety-guarded models) with person-irrelevant prompts, while attaching face images as "user context" via a textual prefix. The method is instantiated across three tasks (story generation, term explanation, exam-style QA) and evaluated on 20 models (16 open-source, 4 proprietary) for gender and racial bias. The method achieves zero refusals where prior benchmarks fail, and reveals that all tested models exhibit demographic disparities in person-irrelevant outputs.

## Strengths

- **Clean solution to a real, growing problem.** The paper identifies that safety-guarded models increasingly refuse attribute-inferring prompts used by existing bias benchmarks, making those benchmarks unreliable. Table 1 starkly demonstrates this: refusal rates reach 100% in some cases. The proposed fix — person-irrelevant prompts with images as user context — is simple and effective, driving refusal rates to zero across all six representative models tested. This is a genuinely clever methodological contribution.

- **Substantial empirical scope.** Evaluating 20 LVLMs (16 open-source, 4 proprietary) across 3 tasks and 2 demographic axes (gender and race) is a large and systematic effort. The results in Table 2 and Figures 2–4 are presented cleanly, and the scale makes the findings more robust than a small-scale demonstration.

- **The three-task design reveals non-trivial structure.** The finding that bias scores do not strongly correlate across tasks (Observation 2.3, solid-line correlations −0.11 to 0.21) is an important methodological lesson: bias is task-dependent and cannot be proxied by a single measurement. This insight is useful for the field.

- **The refusal-rate verification is decisive.** Table 1 provides direct empirical validation of the paper's motivation: four prior benchmarks × six models, showing a clear pattern of unreliability vs. zero refusals for the proposed method. This single comparison strongly supports the practical value of the contribution.

## Weaknesses

### Fatal
None.

### Major

- **Exam-style QA task lacks a clear mechanism and its "bias score" strongly tracks model capability.** The paper defines bias in exam-style QA as accuracy differences across user demographic groups on MMLU questions (e.g., "How many numbers are in the list 25, 26, ..., 100?"). It offers no hypothesis about *why* or *how* a user's attached photo should affect a model's reasoning accuracy on such questions. Moreover, the paper itself reports that exam-style QA bias scores correlate very strongly with overall model performance (r = −0.81/−0.84 for gender/race, Observation 2.5). This correlation suggests the exam-style QA "bias score" may primarily reflect that better models have less noisy/random outputs, rather than measuring a distinct bias construct. The paper should either articulate a plausible mechanism or explicitly acknowledge that this task's interpretation is less clear than the other two tasks. (Lines 133, 265, 330)

- **No uncertainty quantification for any reported quantity.** All bias scores in Table 2 are reported as point estimates without confidence intervals, standard errors, or significance tests. TVD scores on 500 stories (story generation) or 100 explanations (term explanation) have sampling variability that is not reported. The correlation coefficients (Figures 3, 4) are reported as precise r values without confidence intervals or significance levels — particularly problematic with only n=20 models, where correlation estimates are highly uncertain. This is the single largest methodological gap. (Table 2, Figures 3–4)

- **The "user photo" framing lacks a control experiment.** The paper uses FairFace face images prefixed with "I've attached my photo." and assumes models treat these as user-context demographic cues. No control condition (e.g., comparing "I've attached my photo" vs. a neutral prefix like "Here is an image") is run to validate that the demographic effects depend on the "user context" framing rather than simply reflecting the model's standard image captioning/description behavior. Without this control, the interpretation of what the bias scores measure is less grounded than the paper claims. (Lines 56, 109–110)

### Minor

- **Construct framing could be sharper.** The paper presents itself as solving the problem with prior bias benchmarks (abstract: "enabling reliable bias measurement"). But prior benchmarks measured a specific construct: whether the model applies demographic stereotypes to the *person depicted in the image*. This paper measures a different (though related and valuable) construct: whether the model's outputs for *person-irrelevant tasks* differ based on a user's perceived demographics. Both are forms of societal bias, but they are not substitutes for each other. The paper would be stronger if it explicitly acknowledged this distinction rather than using "societal bias" as an umbrella that conflates them. (Lines 9, 52–58, 111–117)

- **No empirical comparison against captioning-style prompts on contextual confounds.** The paper argues (lines 95–97) that captioning-style prompts ("Describe the image") suffer from contextual confounds (e.g., kitchen utensils correlating with women), and claims its method reduces this problem. However, no experiment compares the two approaches on the same images to demonstrate this advantage empirically. The claim is logical but unverified.

- **Proprietary vs. open-source comparison is confounded.** Observation 2.1 (lower bias in proprietary models) is presented as a headline finding, but "proprietary vs. open-source" is confounded with training budget, data scale, and alignment effort. The paper partially acknowledges this in Section 5, but the discussion does not sufficiently caveat the early presentation of this finding (lines 191).

### Trivial

- Section 5's discussion of continuous monitoring as a bias-reduction factor is presented in a discussion section without experimental evidence, which is appropriate, but the tone sometimes veers toward implying the finding follows from the results when it remains a hypothesis. (Lines 342–348)

## Nice-to-Haves

- A control experiment comparing different image prefixes ("I've attached my photo" vs. a neutral description) would substantially strengthen mechanistic interpretation.
- Confidence intervals or bootstrap estimates for all bias scores and correlations would significantly improve the methodological rigor.
- Intersectional analysis (e.g., Black women vs. White men) would be a natural extension given the FairFace dataset supports it.
- An analysis of whether model rankings are consistent across tasks would help practitioners prioritize which tasks to use.

## Removed Points

These points are flagged to be removed, treat them with caution:

- **"Figure 3 contains impossible asymmetric r values":** The harsh critic flagged that the Figure 3 caption lists asymmetric correlation pairs (e.g., −0.11 vs. 0.11, 0.08 vs. 0.93). The paper's body text (Observations 2.3 and 2.4) is internally consistent, reporting solid-line task-wise correlations in the range −0.11 to 0.21 and dotted-line gender-race correlations of 0.49, 0.60, 0.93. The caption values are almost certainly a parser artifact from extracting bidirectional arrow labels in a path-type diagram embedded in the figure. Per the formatting-artifact rule, this criticism is removed. (The separate, valid concern about missing confidence intervals on these correlations remains in Major weaknesses.)

- **"Hypothesis 1 is a value judgment":** This philosophical point (could a model legitimately adapt to perceived user traits?) is outside the paper's stated scope. The paper clearly states its normative assumption (Hypothesis 1) and builds on it consistently.

- **"LLM judge may have demographic biases":** The paper reports alignment with human judges (Appendix D). The speculation that human judges also have biases is too speculative and not anchored in the paper's content.

- **"Missing related work on user-context bias in LLMs":** Per the rules, missing related work citations cannot be raised without external verification.

## Novel Insights

The reviews converge on a genuine insight that the paper itself partially obscures: the paper measures *differential treatment of users by perceived demographics* — a construct that is distinct from, but complementary to, prior benchmarks that measure stereotype attribution to depicted persons. Recognizing this distinction actually strengthens the paper by clarifying what is novel (the user-context framing and the three task designs) vs. what carries over from prior work. The reviews also surface that the exam-style QA task's interpretation depends on an implicit mechanism (accuracy varies with user photo) that is never explained, and that its dominant correlation with model performance may undermine its claim to measure bias rather than capability noise.

## Suggestions

1. Add confidence intervals or bootstrapped error bars to all bias scores (Table 2) and correlation coefficients (Figures 3, 4). With n=20 models, correlation estimates in particular need uncertainty bounds.
2. Either articulate a plausible mechanism for how a user photo affects MMLU accuracy, or explicitly acknowledge the ambiguity and reframe the exam-style QA task as exploratory.
3. Run a control experiment comparing the "I've attached my photo" prefix against a neutral prefix to validate that the demographic effects depend on the "user context" framing.
4. Revise the framing (Sections 1, 4, 6) to explicitly distinguish the construct measured (user-demographic differential treatment) from prior work's construct (visual stereotype attribution) rather than treating the method as a drop-in replacement.

**MY FINAL SCORE: 6**
**MY FINAL DECISION: Accept**