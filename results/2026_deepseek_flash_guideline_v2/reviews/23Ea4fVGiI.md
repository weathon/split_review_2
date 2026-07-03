Below is my final consolidated review, synthesized from the Harsh Critic and Strength Finder inputs, with every weakness verified against the paper's own text.

---

## Summary

This paper introduces the Task-Method-Knowledge (TMK) framework from cognitive science as a structured prompting strategy for LLM planning. The authors evaluate TMK on the PlanBench Blocksworld benchmark (Classic, Mystery, Random variants) using several OpenAI models (GPT-4, GPT-4o, o1-mini, o1, GPT-5). The headline finding is that TMK produces large accuracy gains, most strikingly on o1 for Random Blocksworld (31.5% → 97.33%), and induces a "performance inversion" where the model performs better on opaque symbolic tasks than on semantically-obfuscated ones. The paper argues that TMK acts as a "symbolic steering mechanism."

## Strengths

1. **Performance inversion is a specific and interesting empirical pattern.** The finding that TMK flips the relative difficulty ordering for o1 (Random becomes easier than Mystery under TMK, while the reverse holds for plain text) is more informative than a uniform accuracy gain. The paper correctly argues that if TMK merely added useful context, one would expect uniform gains; the reversal suggests a qualitative shift in reasoning mode (Section 5.2.1, Table 2). This is the paper's most compelling observation.

2. **Methodological precautions against known criticisms of prompting research.** The paper explicitly addresses three critiques raised by Stechly et al. (2024) and Bhambri et al. (2025) (Section 5.1): (a) the one-shot example is random and untailored, and the paper verifies that plain-text zero-shot outperforms one-shot, isolating the gain to TMK rather than the example (Section 3.2, points 2–3); (b) every step of the plan must be formally correct via PDDL validation; (c) improvements are shown across multiple models and domain variants. This is a concrete improvement over prior work criticized for using instance-specific examples or approximate evaluation.

3. **Formal plan validation using classical planning tools.** Following PlanBench methodology, outputs are validated using VAL and fast-downward — automated planners that verify PDDL-level correctness — rather than approximate metrics like LCS or final-state matching (Section 2.2). This provides rigorous evaluation.

4. **Detailed exposition of TMK applied to planning.** Figure 1 provides a concrete three-layer TMK decomposition of Blocksworld, making the prompting strategy transparent and reproducible. The design choices (JSON serialization, three-layer hierarchy for context-window constraints) are clearly explained (Section 3.1).

5. **Honest documentation of a negative result.** The paper reports that o1-mini's accuracy on Mystery Blocksworld drops from 19.1% to 16.83% under TMK (Table 2), and offers a specific hypothesis about capacity limitations (Section 4.2). This transparency strengthens credibility.

## Weaknesses

### Fatal

None.

### Major

1. **Asymmetric extraction function confounds the headline results.** The paper's central claim — particularly the 65.8 pp gain on o1 Random Blocksworld — rests on a comparison between TMK results evaluated with an "enhanced extraction function" and plain-text baseline numbers taken from the public PlanBench leaderboard (Valmeekam, 2023), which used the original stricter extraction. The paper documents (Section 3.2, lines 183–191) that it "added new code to the extraction criteria which was applied for random blocksworld," an enhanced function that tolerates extra words, symbols, and formatting artifacts. Crucially, the paper states these artifacts are "evident within random blocksworld domains" but "rare in classic blocksworld" (line 191). This creates a directly confounding pattern: **the domain where the extraction was loosened (Random) is the domain where TMK improvement is largest.** The paper argues these artifacts "do not take away from the ability to assess if language models can plan and reason," but this misses the point: the concern is whether the *asymmetric* evaluation inflates TMK's scores relative to the baseline. Without re-evaluating both conditions through the same extraction pipeline, the magnitude — and in Random especially, the credibility — of the claimed gains cannot be assessed. This issue is major because the paper's most dramatic result (o1 Random: 31.5% → 97.33%) is the one most directly affected.

### Minor

2. **Unclear provenance of plain-text baselines and extraction consistency.** For o1 and GPT-5, the paper states it "ran the PlanBench benchmark for newer models for which it has not been reported" (line 193), but does not clarify whether these runs used the original or the enhanced extraction function. The Table 2 caption describes plain-text as "best of sampled Zero & One shot" while noting only o1-preview's numbers are "extracted from Valmeekam (2023)." This opacity makes it difficult to assess whether the o1 and GPT-5 comparisons are fair, compounding the extraction concern.

3. **Causal mechanism claims exceed the evidence.** The paper repeatedly asserts that TMK "acts as a symbolic scaffold" and "steers reasoning models toward formal code-execution pathways" (Abstract, Section 5.2.1, Conclusion). While the performance inversion is suggestive, the paper provides no direct evidence for this mechanism — no attention analysis, probing, or ablation demonstrating that code-execution pathways are actually engaged. The Conclusion overstates the finding ("This confirms that TMK acts as a symbolic scaffold") relative to what the experiments support.

4. **o1-mini anomaly is acknowledged but not resolved.** The drop on Mystery Blocksworld (19.1% → 16.83%) and negligible gain on Classic (56.7% → 57%) are reported honestly, but the offered explanation (capacity limitations, optimization artifacts) is unsupported speculation. A model in the same family showing degradation under TMK weakens the generality of the claimed effect.

5. **No statistical rigor.** The paper reports single-run accuracy without confidence intervals, error bars, or significance tests. While single-run evaluation is not uncommon in PlanBench publications, the dramatic central claim (65.8 pp gain) would be far more convincing with variance estimates showing the improvement is well outside run-to-run noise.

### Trivial

6. **Sparse limitations section.** Section 5.3 acknowledges only the narrow domain scope (Blocksworld only) but omits the extraction confound, the lack of ablations, and the o1-mini anomaly as limitations worth flagging for readers.

## Nice-to-Haves

- **JSON-only ablation:** Providing the same domain information in JSON format *without* TMK's teleological Task-Method-Knowledge decomposition would test whether gains come from structured formatting or from TMK's specific causal/teleological structure.
- **Component ablation:** Disentangling which TMK component (Tasks, Methods, Knowledge) drives the gains.
- **Comparison to alternative structured prompting methods** (e.g., PDDL in the prompt, HTN/BDI-style decompositions).
- **Error analysis** characterizing remaining failure modes under TMK.
- **Cost/latency comparison** between TMK and plain-text prompts.

## Removed Points

These points were raised by reviewers but are removed from the main review after verification:

1. **Criticism about one-shot vs zero-shot comparison being unaddressed.** The paper explicitly addresses this in Section 3.2 with three detailed reasons. The critic's claim that the OSF reference is insufficient is a missing-appendix concern (the paper references the OSF link for data); per instructions, such concerns are removed.

2. **Criticism about insufficient documentation of model versions/API parameters.** This level of detail is typically placed in appendices; the paper references the OSF link for full results. Not a reviewable weakness.

3. **Generic complaint about "no comparison to CoT/ReACT."** The paper is about evaluating TMK against plain-text baselines on PlanBench, not about comparing TMK to other prompting methods on the same benchmark. The paper explicitly discusses CoT and ReACT limitations (Section 2.1) and scopes out head-to-head comparisons as future work. Scope-creep criticism.

4. **Formatting/style nitpicks** and claims about garbled text or broken characters: These are parser artifacts, not author errors.

5. **Claims about missing appendix, missing proofs, or unreleased code:** Per instructions, appendices and supplementary materials are stripped by the parser; these exist in the original submission.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Re-run all plain-text baselines through the same enhanced extraction pipeline used for TMK.** This is the single highest-leverage fix. If the gains persist (likely, though potentially attenuated), the paper's core claims become credible. If they attenuate substantially, the paper must recalibrate its claims.

2. **Run at least 3–5 trials per condition** and report means with ranges or confidence intervals, at least for the most dramatic result (o1 Random).

3. **Add a JSON-only ablation condition** that provides domain information in structured JSON without TMK's teleological decomposition, to isolate whether the TMK structure per se matters.

4. **Soften the mechanistic claims** in the Abstract and Conclusion. The paper can describe TMK as "suggestive of" or "consistent with" a shift toward symbolic reasoning, rather than asserting it as confirmed.

5. **Clarify the provenance of every number in Table 2** — which were from the public leaderboard, which were the authors' own runs, and which extraction function was used in each case.

---

## Score and Decision

The paper targets a promising and under-explored direction — applying the TMK knowledge representation framework from cognitive science to LLM prompting for planning. The performance inversion finding is genuinely interesting and goes beyond a simple "TMK helps" claim. However, the paper's central empirical contribution is compromised by a documented asymmetry in the evaluation pipeline: an enhanced extraction function was applied to TMK results for Random Blocksworld but not to the public-leaderboard baselines, and the largest claimed gains are concentrated precisely in that domain. The paper also makes causal mechanism claims that outrun the evidence and lacks basic error bars for its most dramatic numbers. The idea is worthwhile but the evaluation needs substantial revision before the claims can be accepted.

Given these trade-offs — a novel framing and an interesting empirical pattern weighed against a significant evaluation confound — I assign a score that reflects a borderline rejection: the paper has genuine potential but cannot be accepted in its current form due to methodological concerns that affect its main empirical claims.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>