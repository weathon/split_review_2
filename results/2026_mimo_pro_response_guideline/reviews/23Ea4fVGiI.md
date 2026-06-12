## Summary
This paper proposes using the TMK (Task-Method-Knowledge) framework from cognitive science as a structured prompting strategy to improve LLM planning on PlanBench Blocksworld variants. The key empirical result is o1 improving from 31.5% to 97.3% on Random Blocksworld, accompanied by a "performance inversion" where the difficulty ordering between Random and Mystery reverses under TMK prompting. The paper also presents a theoretical hypothesis that TMK acts as a "symbolic steering mechanism" shifting LLMs from linguistic to code-like reasoning.

## Strengths
- **Performance inversion is a genuinely interesting, falsifiable observation**: Under plain text, o1 scores Mystery (74.3%) > Random (31.5%); under TMK, this reverses to Random (97.33%) > Mystery (83.3%) (Table 2, Section 4.2). If TMK merely added context, one would expect uniform gains rather than a difficulty-ordering flip — this is a specific, falsifiable pattern.
- **Novel cross-disciplinary contribution**: Bringing the TMK cognitive science framework (originally for modeling teleology of intelligent agents) into LLM prompting distinguishes this work from standard prompt engineering papers. The framework is clearly presented in Figure 1 with explicit mapping to Blocksworld actions, preconditions, effects, and mechanisms.
- **Directly addresses prior criticisms of prompting-for-planning work**: The paper engages with Stechly et al. (2024) and Bhambri et al. (2025) by requiring complete stepwise plan correctness (Table 2 footnote), using non-tailored one-shot examples, and demonstrating that zero-shot often outperforms one-shot for plain text (Section 3.2, 5.1).
- **Cross-model evaluation with honest reporting of mixed results**: Table 2 covers GPT-4, GPT-4o, o1-mini, o1, and GPT-5 across three Blocksworld variants, and explicitly acknowledges the o1-mini Mystery regression (19.1%→16.83%) in Section 4.2.
- **Well-motivated benchmark selection**: The three Blocksworld variants (Classic/Mystery/Random) create a semantic-to-symbolic gradient (Table 1) that directly enables mechanistic analysis of how TMK interacts with semantic cues.

## Weaknesses

### Fatal
None

### Major
- **Confounded comparison methodology undermines headline results**: Table 2 caption explicitly states "comparing plain-text prompts (best of sampled Zero & One shot) and TMK structured prompts (One shot)." The baseline uses the better of zero-shot and one-shot plain text, while TMK uses only one-shot. Even though the authors argue zero-shot outperforms one-shot for plain text (line 180), the one-shot TMK example demonstrates the expected TMK-JSON output format — a form of format scaffolding that zero-shot plain text does not provide. A zero-shot TMK condition is needed to disentangle format demonstration from TMK structure. Additionally, the authors acknowledge "added new code to the extraction criteria" for Random Blocksworld (lines 183–184), but it is ambiguous whether the baseline leaderboard numbers were re-processed with the same extraction code or only the TMK results were. Without matching shot counts, extraction logic, and inference parameters, the accuracy comparisons cannot be confidently attributed to TMK.

- **No ablations to isolate TMK's specific contribution from structured domain knowledge**: The TMK prompt (Figure 1) provides a complete formal domain specification — all four actions with preconditions, effects, and process descriptions in structured JSON. This is functionally similar to a PDDL domain specification encoded in JSON. The paper does not include any ablation distinguishing "the TMK teleological framework helps" from "providing a complete formal domain specification in structured format helps." Two critical missing conditions: (1) a structured plain-text prompt with equivalent domain knowledge completeness, and (2) a non-TMK JSON specification (e.g., flat key-value encoding of actions and effects). Without these, the paper cannot support its central claim that TMK's teleological hierarchy is responsible for improvements.

### Minor
- **No statistical reporting for stochastic model outputs**: All accuracy numbers in Table 2 appear to be from single evaluation runs with no error bars, confidence intervals, or variance measures. While common in large-scale benchmark reporting, this is concerning for the headline claim (o1 Random: 31.5%→97.3%), where the improvement magnitude is extraordinary and reliability across runs cannot be assessed.

- **Overclaimed theoretical framing relative to acknowledged evidence gap**: The abstract states "TMK functions not merely as context, but also as a mechanism that steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways" — presented as a finding. Section 5.2.1 elaborates this hypothesis extensively. Yet line 304 acknowledges "the cause of that increase is left to future work." No direct evidence is provided (no analysis of reasoning traces, representations, or attention patterns). The performance inversion is suggestive but has alternative explanations — e.g., TMK's formal preconditions provide disambiguation that Random tokens need but that Mystery tokens partially disrupt via semantic interference.

- **Cherry-picked headline framing**: The abstract highlights "up to an accuracy of 97.3%" and "65.8%" gain, both from o1 on Random. The full table shows much more mixed results: GPT-4/GPT-4o on Random improve from ~0% to ~4–5% (trivially small), o1-mini degrades on Mystery, and GPT-5 starts at 92.5% with only 6.5pp gain. The paper does not discuss these modest or negative results with the same emphasis.

### Trivial
None

## Nice-to-Haves
- Report prompt token counts for TMK vs. plain-text to address whether information density differences contribute to improvements.
- Discuss GPT-5's high baseline (92.5% on Random) as evidence that very capable models may not need TMK for this domain, tempering generalizability claims.
- Provide qualitative analysis of model reasoning traces to partially test the code-steering hypothesis.

## Removed Points
These points are flagged to be removed, treat them with caution:
- Harsh critic's concern about API version/temperature mismatches — standard when comparing against published leaderboard results; the authors provide code via OSF.
- Harsh critic's point about GPT-5 results not being discussed — the paper presents all results in Table 2; modest improvement is visible.
- Harsh critic's framing of "no direct evidence" for code-steering as a structural flaw — better characterized as overclaimed theoretical framing (captured as a minor weakness).

## Novel Insights
The "performance inversion" observation — where TMK reverses the difficulty ordering between Random and Mystery Blocksworld for o1 — is a genuinely novel empirical finding. If TMK merely added better-organized context, one would expect uniform gains across domains; the domain-dependent reversal is a specific, falsifiable pattern suggesting something deeper about how prompt structure interacts with LLM reasoning modes. This observation, if replicated with proper controls, could open productive research directions.

## Calibration Anchors

**All anchors retrieved across Round 1:**
| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| koza5fePTs | 2.0 | 1 | Combines existing benchmarks, overfitting in fine-tuning; our paper is more novel |
| jOuHjFw71C | 3.0 | 1 | Just evaluates o1 on existing benchmarks; our paper has a novel method |
| sdpVfWOUQA | 3.0 | 1 | MCTS for LLM planning; our paper has more interesting cross-disciplinary angle |
| cWrqs2lwCJ | 3.0 | 1 | Backward planning with similar experimental limitations |
| 85Ik12q2hP | 4.0 | 1 | Critical ReAct evaluation with sensitivity analysis; similar weakness severity |
| OhUoTMxFIH | 5.67 | 1 | Novel async planning benchmark; accepted, our paper less comprehensive |
| K3KrOsR6y9 | 6.4 | 1 | AoT+ with clear ablations on Blocksworld; our paper lacks comparable ablations |
| NUD03NBDOE | 6.75 | 1 | Novel benchmark with ramifications; accepted, our paper has weaker methodology |
| T5QLRRHyL1 | 7.0 | 1 | Comprehensive embodied planning benchmark; higher quality |

**Round 1 bracket: 4.0–5.0.** The paper has a genuinely novel cross-disciplinary idea and a real empirical insight (performance inversion), placing it above the 2.0–3.0 reject papers. But the confounded comparison and missing ablations prevent it from reaching the 6.0+ accept papers, which have clearer methodology and proper ablations. No second round needed.

**Final score: 4.5.** The conceptual contribution is real and the performance inversion is interesting, but the experimental execution has genuine methodological gaps that must be addressed before the core claims can be fully supported.

## Suggestions
- Run a controlled comparison: test TMK and plain text under identical conditions (both zero-shot or both one-shot with equivalent format guidance), with the same extraction code and inference parameters.
- Add at minimum one ablation: a structured plain-text prompt with equivalent domain knowledge to isolate TMK's teleological contribution specifically.
- Report 3–5 independent runs with mean ± std for key configurations to establish reliability.
- Examine a few model reasoning traces (even qualitatively) to test the code-steering hypothesis.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>