Now I have sufficient calibration data. Let me compile the final review.

**Bracket assessment:** Round 1 brackets showed most similar papers at 3.0-4.67 (rejected). Our paper is empirically stronger than the ~3.0 evaluations but has a similar confound issue. Round 2 confirms the 4.0-5.0 range.

**Final score: 4.5** — borderline reject. The paper identifies a real problem and provides extensive empirical evidence of an interesting phenomenon, but the central CRI metric conflates concept quality with reasoning self-consistency, weakening the headline claim of measuring "annotation sufficiency."

---

## Summary

This paper proposes the Fast and Slow Effect (FSE) framework for evaluating whether LLM/VLM-generated concept annotations in XAI provide sufficient semantic coverage to support accurate concept-class mapping. It introduces a 5-stage hierarchical annotation process and the Class Representation Index (CRI) metric. Experiments across 6 models (GPT-4o, GPT-4o-mini, Llama-3.2 90b/11b, QwenVL2 72b/7b) and 5 datasets reveal that the "slow mode" (concept-only classification) underperforms "fast mode" (direct visual classification) by 25-27% on fine-grained datasets, despite the opposite trend on general datasets. The paper also shows that fused (vision+concepts) mode achieves ~90% CRI while the same concepts alone score ~50%, arguing that downstream utility does not proxy for annotation sufficiency.

## Strengths

- **Table 4 directly refutes the utility-as-proxy assumption (Section 6).** Fused-mode CRI reaches ~90-96% while the identical concept annotations in slow mode alone score only ~42-68% across GPT-4o and GPT-4o-mini. This cleanly demonstrates that high downstream accuracy can coexist with insufficient concept annotations — a finding with direct practical significance for how the community evaluates annotation quality.

- **Table 2 shows the CRI gap is systematic across diverse model families.** All six models from three families (GPT, Llama, Qwen) and two size scales show negative CRI gaps on fine-grained datasets, averaging -25% to -27%. Only 2 out of 18 entries are positive. This breadth rules out the possibility that the insufficiency is an artifact of a single model architecture or size.

- **Table 3 provides a positive control that validates framework specificity.** On general object recognition datasets (CIFAR-100, Caltech-101), slow mode eventually outperforms fast mode (e.g., GPT-4o on CIFAR-100: 94.07% at t=5 vs. 84.84% at t=0). This contrast demonstrates that FSE does not uniformly penalize slow mode — it correctly identifies when annotations *are* sufficient — strengthening the conclusion that the problem is specific to fine-grained semantic coverage.

- **Preliminary experiment (Table 1) validates the distractor selection methodology.** The paper empirically shows that semantically related distractors raise contradiction rates from ~14-20% to ~34-45% versus random selection, ensuring the evaluation task is meaningfully challenging.

## Weaknesses

### Fatal
None.

### Major

- **CRI conflates concept quality with reasoning self-consistency (Definition 3.1, Eq. 2).** The CRI operationalizes "annotation sufficiency" as: *can the same model that generated the concepts correctly classify using only those concepts?* This is a joint test of concept quality *and* the model's ability to reason from its own text. A model might generate genuinely discriminative concepts but fail at multi-step textual reasoning (false negative), or generate vague concepts but still guess correctly through memorized associations (false positive). The semantically similar distractors partially mitigate false positives but do not eliminate the confound. The paper's headline framing ("annotation sufficiency") overclaims what the metric can certify; it is more accurately a measure of self-consistent discriminability. This does not invalidate the empirical findings (the fast/slow gap is real and robust) but does require reframing the contribution.

- **No external calibration of what "sufficient" annotations look like.** The paper presents no human annotation baseline to contextualize CRI scores. If human domain experts also achieved ~60% CRI on fine-grained datasets (because text alone is hard for these tasks), the paper's central finding would be unremarkable. If humans achieved >90%, it would be highly meaningful. Without this anchor, the reader cannot assess whether a 60% CRI reflects genuine annotation deficiency or inherent task difficulty. This is especially important given the paper's goal of certifying annotation sufficiency without human supervision — validation against an independent standard is needed before such a claim is warranted.

### Minor

- **Experimental sample sizes for main CRI experiments are unreported.** The paper defines *l* as "the total number of cases" (Section 4.1) but never states its value for Tables 2-4. Only the preliminary contradiction test specifies "100 images." Without sample sizes, the reader cannot assess the precision of reported CRI values or whether the claimed 25% gaps are statistically reliable given the number of test cases.

- **Distractor selection uses a single model's confusion patterns.** The Semantic Similarity Dictionary is built from ResNet-18 predictions (Section 5.3). This introduces a dependency on one model's error patterns; models whose confusion patterns differ from ResNet-18's would face differently calibrated distractors. While this is a reasonable methodological choice, it should be acknowledged as a limitation.

- **The "Slow Mode Superiority" hypothesis is weakly motivated (Section 4.2).** Invoking Kahneman's dual-process theory is a conceptual stretch: the paper's fast/slow modes differ in *modality* (visual vs. textual), not in cognitive strategy applied to the same input. The hypothesis that text-only reasoning should outperform direct visual recognition for fine-grained visual tasks was never well-motivated, and its refutation is less surprising than the paper suggests. This does not undermine the empirical results, but the framing is distracting.

- **Three runs are mentioned but standard deviations are not reported in tables** (Section 6, Figure 3 caption). The paper claims "negligible" standard deviations without reporting the values, making it impossible for readers to verify.

### Trivial

- **Equation (2) contains a notation error.** The CRI formula writes (1/t) Σ_{i=1}^t but "t" denotes the annotation step (0-5), not the number of test cases. The paper defines "l" as the total number of cases (Section 4.1); the summation should be to *l*, not *t*. This is a typo in the formula that does not affect the methodology or experiments.

## Nice-to-Haves

- A human annotation baseline on a subset of classes would be the single most impactful addition, calibrating what CRI values mean.
- A control experiment feeding the same concepts to a *different* LLM would help disentangle concept quality from model-specific reasoning ability.
- Ablation of the stage count (why 5 stages?) would strengthen the framework's methodological justification.
- Reporting sample sizes and standard deviation values would improve reproducibility.

## Removed Points

*These points were flagged by reviewers but are removed as invalid, factually incorrect, or noise:*

- **"Utility-as-proxy lacks crucial control (vision-only vs. vision+concepts)"** — REMOVED (factually incorrect). The paper already includes this comparison: Fast mode (t=0) is vision-only, Fuse mode is vision+concepts. Table 4 shows Fuse ≈ Fast, which is the informative comparison showing concepts add no discriminative power beyond vision alone.
- **"The paper confuses annotation with generation"** — REMOVED (too vague/speculative). The paper's framing is internally consistent; the evaluation targets whether the generated annotations (once produced) are sufficient for classification.
- **"CRI formula is garbled"** — REMOVED (overstated). It is a notation typo (t vs. l in the summation bound), corrected to Minor/Trivial above.
- **Missing related works** — REMOVED per protocol (cannot verify existence of missing citations without external knowledge).
- **Reproducibility concerns about unreleased models/code** — REMOVED per protocol (the paper cites existing models and provides code/URL; questioning existence is not permitted).
- **Formatting/typo nitpicks** — REMOVED per protocol (parser artifacts).
- **Generic concern-sweep statements** (e.g., "could the metric be measuring a proxy?") — REMOVED as speculative noise.

## Novel Insights

The most valuable observation emerging from the review process is that the paper's core finding can be productively reframed: rather than claiming that "current annotation methods fail to provide sufficient semantic coverage," the results more precisely show that *LLMs exhibit a systematic self-consistency failure* — they know more than they can write down for fine-grained visual distinctions. This reframing is actually *more* interesting: it points to a fundamental modality asymmetry (visual recognition outpaces textual describability) that has implications for both XAI and for understanding how multimodal models represent knowledge. The paper's empirical contribution is robust under this reframing; only the interpretive framing needs adjustment.

## Suggestions

1. **Reframe the contribution** from "annotation sufficiency evaluation" to "self-consistency diagnostic for concept annotations." The CRI is a valid and useful metric for detecting when a model's textual concepts fail to capture what it visually knows — just don't claim it measures absolute sufficiency without external validation.
2. **Add a human annotation baseline** for at least one dataset (e.g., CUB-Birds). This would provide the missing calibration point and dramatically strengthen the paper's claims.
3. **Report sample sizes** for all main experiments and include standard deviation values in tables.
4. **Acknowledge the self-consistency confound** explicitly in the paper's limitations section, with discussion of how it affects interpretation of the results.

## Score and Decision

**Calibration anchors (all rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| kTjEPEy96Q.md (Evaluating Unseen) | 3.00 | R1 | Similar evaluation framework for CBMs, similar confound issue; our paper has broader experiments |
| KLUDshUx2V.md (Automating Concept Banks) | 3.40 | R1 | LLM concept generation + evaluation; our paper more novel framework |
| 50P9TDPEsh.md (Critique Ability) | 4.67 | R2 | Similar evaluation benchmark for LLMs; comparable quality |
| rp0EdI8X4e.md (Faithful VLC) | 6.25 | R1 | Stronger theoretical grounding; our paper has weaker metric validation |
| 1IeCqgULIM.md (Provably Sufficient Explanations) | 7.25 | R1 | Different topic (formal verification); not directly comparable |

**Round 1 bracket:** 3.0–6.25 (initial broad range)
**Round 2 narrowing:** 3.5–5.5 (removing low end [irrelevant topics] and high end [stronger papers])
**Round 3 confirmation:** 4.0–4.67 (most similar papers cluster here)

**Final score: 4.5**

The paper identifies a genuine, practically important problem and provides extensive, systematic empirical evidence of a robust phenomenon. However, the central CRI metric has a confound between concept quality and reasoning self-consistency that undermines the strongest interpretive claims ("annotation sufficiency"). This is not fatal — the empirical patterns remain interesting under a more modest framing — but in its current form the overclaiming prevents acceptance. With the suggested reframing and a human baseline, this could become a solid borderline accept.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>