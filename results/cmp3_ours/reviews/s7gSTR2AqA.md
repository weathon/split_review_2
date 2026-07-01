Now I have a clear calibration picture. Let me write the final review.

## Summary

This paper applies the Information Bottleneck (IB) principle and iterated language learning to study whether LLMs exhibit human-like inductive biases toward efficient semantic categorization. It conducts (1) an English color-naming study across 39 models, finding large variation with instruction-tuned models approaching English; and (2) an Iterated In-Context Language Learning (IICLL) study showing that LLMs restructure random category systems toward greater IB-efficiency. Only Gemini 2.0 recapitulates the full human range of IB tradeoffs, while other tested models converge to low-complexity solutions.

## Strengths

- **Comprehensive model coverage in the naming study.** Testing 39 models across 6 families (Gemini, Gemma, Llama, Qwen, Olmo, GPT-2) with controlled variation along size, instruction-tuning, and modality is genuinely thorough. The finding that many state-of-the-art models fail at English color naming despite English-heavy training data is a meaningful empirical contribution (Section 4.1, Figure 2).

- **The IICLL paradigm is a well-motivated extension.** By adapting I-ICL (Zhu & Griffiths, 2024) to replicate human iterated language learning experiments (Xu et al., 2013) — using pseudo-terms, random initial partitions, and limited in-context examples — the paper creates a clean comparison between LLM and human inductive biases. The result that models restructure random systems toward IB-efficient solutions without being told the stimuli are colors (only "features," line 143-144) is a genuine, nontrivial finding.

- **Principled evaluation through the IB framework.** Using efficiency loss (distance from the IB bound) and NID-based alignment provides a theoretically grounded quantitative lens beyond simple accuracy. The rotation analysis (Section 4.2, Appendix H) provides evidence that emergent structure is non-arbitrary for Gemini.

- **Honest reporting of limitations.** The paper explicitly states that only Gemini 2.0 recapitulates the full human range of IB tradeoffs (line 9, line 23), that rotation results are "less conclusive" for other models (line 145), and that the Shepard circles result is preliminary (line 159).

## Weaknesses

### Fatal
None.

### Major

- **The headline claim overgeneralizes from Gemini 2.0 to "LLMs."** The abstract states that "LLMs iteratively restructure initially random systems towards greater IB-efficiency" and that "human-aligned semantic categories can emerge in LLMs." However, in the IICLL experiment — the core evidence that this behavior goes beyond training-data mimicry — only 1 of 4 tested models (Gemini 2.0) fully recapitulates the human range of IB tradeoffs. The other three (Gemma 3 27B, Llama 3.3 70B, Qwen 2.5 32B) converge to low-complexity solutions covering only a narrow portion of the IB bound, and the rotation analysis is inconclusive for them (line 145). The paper acknowledges this in individual sentences but the title, abstract, and conclusion frame the result as a general LLM phenomenon. This is not fatal to the empirical work — it is an honest result — but the narrative should match the evidence: what is shown is that *some* LLMs (specifically Gemini 2.0) exhibit this behavior to a human-like degree, while others show it in a weaker form.

- **The causal claim that IB-efficiency is the "driving principle" outruns the evidence.** The paper writes that LLMs are "guided by the same IB-efficiency principle that underlies human languages" (Discussion, line 167). But the IICLL experiment provides correlational evidence, not causal. Two alternative explanations are equally consistent: (a) *Learned statistical regularity* — LLMs trained on human language data that is itself IB-efficient may have learned that "good" category systems partition perceptual space in particular ways (contiguous regions, certain boundary locations), producing a learned prior rather than an emergent principle of intelligence. The paper acknowledges this in passing ("the precise origins of the bias...are unclear," line 169-170) but the dominant narrative treats IB-efficiency as a fundamental force. (b) *Simplicity bias as a confound* — the IICLL task requires generalization from limited examples; any model with regularization or simplicity bias would tend to produce simpler partitions, some of which happen to lie near the IB bound (because the IB bound favors simpler solutions at lower complexity). The paper does not run controlled experiments distinguishing IB-efficiency from generic simplicity bias (e.g., comparing IICLL trajectories against alternative objective functions like minimum description length without the IB accuracy constraint, or category contiguity alone).

### Minor

- **Asymmetries between IICLL and human iterated learning are under-explored.** The paper compares LLM IICLL dynamics to human IL (Xu et al., 2013) as though the two paradigms reveal the same kind of inductive bias, but there are important differences: (i) human participants operate under memory constraints and perceptual noise; LLMs process all examples with perfect recall; (ii) human IL uses different participants at each generation (sampling variability from a population prior), while IICLL uses the same model iteratively refining its own output; (iii) convergence rates are compared only visually ("after roughly four generations") without statistical tests. These do not invalidate the experiment but mean the strong claim that IICLL "reveals" inductive biases *in the same sense* as human IL is overstated. The relationship should be characterized as an analogy, not an identity.

- **The Shepard circles experiment is too thin to support claims about domain generality.** Section 4.3 tests only Gemini, only k=4, provides no IB-efficiency analysis, presents no quantitative evaluation beyond qualitative visual inspection, and makes no comparison to human data. The paper is appropriately cautious in the text ("initial evidence," "potentially," "an important direction for future work," line 159), yet the result is listed among the paper's numbered contributions in the introduction (line 23-24). This section should either be relegated entirely to future work or substantially expanded with quantitative analysis.

### Trivial
None.

## Nice-to-Haves

- **Disentangle IB-efficiency from generic simplicity bias.** Comparing observed IICLL trajectories against predictions from alternative formal principles (maximum entropy, minimum description length without the IB accuracy constraint, category contiguity alone) would substantially strengthen the claim that IB-efficiency — rather than generic regularization — is the specific driving principle.

- **Test what drives the Gemini vs. others gap.** The paper attributes the difference to "strongest in-context capabilities" but this is underspecified. Probing whether non-Gemini models fail specifically because they cannot utilize long contexts (e.g., by varying the number of in-context examples systematically, or testing context-extended variants) would sharpen the finding.

- **Formal statistical comparisons between LLM and human trajectories.** Reporting effect sizes and significance tests comparing the distribution of efficiency losses at the final generation between LLM and human chains would strengthen the central comparative claim.

- **Deeper analysis of why some models converge to low-resource WCS-like systems** (Section 4.1, line 105-106). The finding that Olmo 2 32B and Qwen 2.5 VL 7B produced systems resembling non-English languages is one of the paper's most interesting results but is only mentioned in passing.

## Removed Points

- **Criticism about "all four models show an impressive ability" being overstatement.** The paper uses this phrasing in context of the models evolving IB-efficient systems despite not knowing the stimuli are colors (line 143-144). All four models do show decreasing efficiency loss (Figure 4a). The claim is about IB-efficiency, not about full complexity range. This is a reasonable statement in context. *Removed: does not hold up against the paper's actual claim.*

- **"No analysis of the k=14 condition separately."** The paper explicitly notes that in the k=14 condition "most of the LLMs immediately converge to low-complexity solutions" (line 143). While a deeper breakdown would be nice, the paper does reference this condition. *Removed: partially addressed.*

- **"No control for the IB bound being too permissive."** The paper does not report distribution of efficiency losses for random systems as a baseline. This is a reasonable suggestion but the IICLL experiment uses random initializations (shown as small black dots in Figure 3) which serve as a visual baseline. *Removed: partially addressed in the figure.*

- **"The Olmo training trajectory analysis deserves more space."** This is a presentation preference, not a weakness. *Removed: subjective presentation judgment.*

- Various section-by-section notes that are primarily summaries or restatements of the critical issues. *Removed: redundant with the weaknesses above.*

## Novel Insights

The key insight that emerges across the two reviews is that the paper's strength lies in the thoroughness and theoretical grounding of its empirical work, but its narrative vulnerability is the gap between the broad framing ("LLMs") and the concentrated evidence (Gemini 2.0). The most interesting finding that merits deeper investigation — beyond the Gemini result — is that some models converge to WCS-like systems resembling low-resource languages rather than English, which raises questions about what model properties (training data composition, tokenization, language distribution in pre-training) drive a model's "default" categorization system.

## Suggestions

1. Reframe the abstract and conclusion to match the evidence: state clearly that a human-like range of IB tradeoffs was observed in one frontier model (Gemini 2.0), while other models showed a weaker form of the bias (converging to low-complexity solutions). Replace "LLMs" with the specific models tested where appropriate.
2. Either remove the Shepard circles result from the list of main contributions or substantially expand it with quantitative IB-efficiency analysis and human data comparison.
3. Add a discussion of alternative explanations (learned statistical regularity, simplicity bias as confound) and explain why the IB-efficiency interpretation is preferred over these alternatives, or acknowledge that further work is needed to distinguish them.
4. Clarify the relationship between IICLL and human IL as an analogy rather than an identity, noting the key asymmetries (no perceptual noise, same model across generations, lack of statistical convergence comparison).

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>