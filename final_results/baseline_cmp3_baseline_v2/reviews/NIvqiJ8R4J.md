## Summary

This paper introduces PELICAN, a two-stage adaptive tutoring framework that first performs collaborative cognitive diagnosis to assess a student's knowledge state, then uses this diagnosis to dynamically select teaching strategies. The framework employs a successor-first diagnostic approach with an expert-assistant-verifier pipeline for question accuracy, and a dual-system (fast/slow thinking) strategy selection mechanism that simulates future dialogue paths when students face persistent difficulties. Experiments on the Gaokao dataset and a human study with 169 students show improvements in critical thinking stimulation and task completion rates over baseline methods.

## Strengths

- **Well-motivated problem and clear framing**: The paper clearly identifies a genuine limitation of standard LLM responses in education—they fail to adapt to individual cognitive states—and provides concrete illustrative examples (Figure 1) that make the problem intuitive and compelling.

- **Novel integration of cognitive diagnosis with adaptive tutoring**: The two-stage pipeline that first diagnoses then tutors is a sensible architectural choice, and the successor-first diagnostic strategy that leverages knowledge hierarchy is a principled approach to efficient assessment.

- **Comprehensive evaluation with both automated and human studies**: The paper includes GPT-based evaluation across multiple dimensions, ablation studies, cognitive level analysis, strategy distribution analysis, and a real-world human experiment with 169 students, providing multiple forms of evidence for the method's effectiveness.

- **The slow-thinking simulation mechanism is technically interesting**: The idea of simulating future dialogue paths to select optimal teaching strategies, with a scoring function that penalizes depth, is a creative application of planning to the tutoring domain.

## Weaknesses

### Fatal
None.

### Major

- **The student simulation in experiments is a critical confound**: The main experiments (Tables 1-5) appear to use an LLM-simulated student rather than real students. The paper mentions a "student role" design in Appendix G, but the core evaluation methodology is unclear from the main text. If the "student" being tutored is also an LLM, then the evaluation primarily measures how well the system interacts with another LLM, not how well it teaches real humans. The human study (Table 6) partially addresses this, but the main results rely on simulated students, which is a significant limitation for a paper claiming to solve personalized education.

- **The human study has concerning methodological gaps**: The human study reports 169 students submitting 1335 reports (7.90 per student on average), but the paper does not specify: (1) how students were assigned to conditions, (2) whether this was a between-subjects or within-subjects design, (3) how the tutoring was delivered (through a web interface? chat?), (4) what the "tutoring reports" contain, and (5) how metrics like "Appropriateness" and "Inspiration" were rated. The success rates in Table 6 (80-87% across all methods) are suspiciously high and similar across methods, suggesting the task may have been too easy or the evaluation insufficiently discriminative.

- **The cognitive diagnosis evaluation is circular**: The diagnosis stage is evaluated by comparing estimated knowledge states against "actual" knowledge states (Table 1), but it's unclear how the ground truth knowledge states are established. If they are also derived from LLM-based assessment of the simulated student, the evaluation measures internal consistency rather than diagnostic accuracy.

- **The ablation study results are inconsistent with the main results**: In Table 3, the "w/o Diagnosis & slow" condition achieves an Inspiration score of 4.56, which is higher than PELICAN's 4.30. The paper does not discuss this counterintuitive result. Additionally, the $R_{coverage}$ and Frequency scores in Table 3 (e.g., PELICAN at 54.84 and 61.47) are substantially lower than in Table 2 (72.36 and 72.06), suggesting different experimental conditions or evaluation protocols that are not explained.

### Minor

- **The threshold for slow thinking is set to M=1**: This means slow thinking is activated after just one round of difficulty on a sub-task. This seems too aggressive—a single round of difficulty may not warrant the computational expense of tree search. The paper does not ablate this parameter or justify the choice.

- **The strategy pool of ten strategies is mentioned but not fully described in the main text**: The paper refers to Appendix E for details, but the main text would benefit from at least listing the strategies to make the method self-contained.

- **The token cost analysis is incomplete**: The paper reports that slow thinking consumes ~40% of ~580k total tokens, but doesn't report per-dialogue costs or compare against baseline methods. This makes it difficult to assess the practical deployment cost.

- **The Gaokao dataset has only 184 questions**: This is a relatively small dataset, and it's unclear whether results generalize to other subjects or educational levels.

### Trivial
- The paper uses "Sepwise" in Figure 5 and Table 6 but "Stepwise" in Table 2—likely a typo.
- The reference to "GUIDING" in the introduction appears to be a stray citation tag.

## Nice-to-Haves

- A comparison against a simpler baseline that just uses chain-of-thought prompting with the student's diagnosed knowledge state as context would help isolate the benefit of the slow-thinking mechanism.
- An analysis of when slow thinking actually changes the strategy selection versus when it agrees with fast thinking would be informative.
- The paper could benefit from a discussion of failure cases—when does PELICAN's approach break down?

## Novel Insights

None beyond the paper's own contributions. The paper's main novelty is the specific integration of cognitive diagnosis with a planning-based strategy selection mechanism, but the individual components (knowledge hierarchy, successor-first diagnosis, dual-system theory, tree search for strategy selection) are all established ideas in their respective fields.

## Suggestions

1. Clarify the experimental setup for the main experiments: Are the "students" in Tables 1-5 simulated by LLMs? If so, this must be stated explicitly and the limitations discussed. The human study should be the primary evaluation, not a supplementary one.

2. Provide more detail on the human study methodology: random assignment, blinding, inter-rater reliability, and how each metric was operationalized. The current description is insufficient for reproducibility.

3. Explain the discrepancy between Table 2 and Table 3 metrics (e.g., PELICAN's $R_{coverage}$ drops from 72.36 to 54.84). If these are different evaluation settings, state this clearly.

4. Address the counterintuitive ablation result where removing both diagnosis and slow thinking improves Inspiration scores.

5. Consider adding a baseline that uses the diagnosed knowledge state as a prompt prefix without the slow-thinking mechanism, to isolate the benefit of the tree search.

## Score and Decision

The paper addresses an important problem and presents a technically sound framework with multiple evaluation angles. However, the major methodological concerns—particularly the reliance on simulated students for the primary evaluation and the insufficiently documented human study—significantly weaken the empirical claims. The paper would benefit from clearer experimental design and more rigorous human evaluation before it can be considered a strong contribution to personalized education.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>