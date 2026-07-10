Now let me compile the final review with the scoring feedback.

## Summary

This paper introduces TMK (Task-Method-Knowledge), a knowledge representation framework from cognitive science, as a prompting strategy for LLMs on planning tasks. The authors evaluate TMK on PlanBench's Blocksworld domain (Classic, Mystery, Random variants) across several OpenAI models, reporting that TMK improves accuracy — most strikingly for o1 on Random Blocksworld (31.5% → 97.33%). The paper also observes a "performance inversion" where o1 performs better on Random than Mystery under TMK, which the authors interpret as evidence that TMK steers models toward "code-execution reasoning pathways." The central claim is that TMK functions as a "symbolic steering mechanism" beyond simply providing context.

## Strengths

- **Novel interdisciplinary connection (Section 2.3):** TMK is a genuinely novel import from cognitive science and education into LLM prompting. Unlike CoT, ReACT, or CoS variants, TMK originates from a formal knowledge representation literature and provides hierarchical decomposition into Tasks, Methods, and Knowledge — including explicit teleological (why) reasoning. This is not a rebranding of existing ideas.
- **Striking empirical result (Table 2, Section 4.2):** The o1 improvement on Random Blocksworld from 31.5% to 97.33% (a 65.8 percentage point gain) is the paper's strongest finding. The performance inversion (Random surpassing Mystery under TMK) is genuinely interesting and warrants follow-up.
- **Methodological rigor in evaluation (Section 5.1):** The paper uses formal plan validation (PlanBench's PDDL-based verification), evaluates complete plan correctness rather than partial matches or plausibility, and avoids instance-matched examples — addressing several well-documented criticisms of prior prompting research.

## Weaknesses

### Major

- **Information confound between TMK and baseline conditions:** The TMK prompt (Figure 1) provides explicit action preconditions, effects, domain concepts, and relational knowledge — e.g., "Given (Preconditions): On(block, table), IsClear(block), HandEmpty()" and "Makes (Effects): Holding(block), NOT On(block, table), NOT HandEmpty()" — along with an explicit Knowledge section defining all domain concepts and relations. The paper states (line 169) that TMK "replaces the domain portion of the PlanBench prompt," but the precise content of the baseline "domain portion" is never documented. If the standard PlanBench prompt does not equally provide all action preconditions and effects, then the TMK condition has an information advantage that confounds attribution to TMK's structure. The model might simply do better because it now explicitly knows the rules of Blocksworld (e.g., to stack A on B it must be holding A and B must be clear). A control providing the same information in plain text prose is needed to determine whether TMK's specific structure adds value beyond the information it conveys.

- **Gap between the central theoretical claim and the available evidence:** The abstract states that TMK "steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways," and Section 5.2.1 elaborates a "code-execution reasoning pathways" hypothesis. The evidence offered is (a) TMK improves performance and (b) the performance inversion for o1. Both observations are consistent with a much simpler explanation: providing missing domain knowledge helps more where it is most needed (Random Blocksworld, where semantic labels give no cues). No internal model analysis, token-level probing, code-format control, or any direct evidence is provided for a shift in reasoning modality. The paper itself hedges at line 304 ("the cause of that increase is left to future work"), creating a clear tension with the stronger causal language in the abstract and discussion. The mechanism claim should be either supported with direct evidence or explicitly labeled as speculation throughout.

### Minor

- **One-shot vs. zero-shot confound partially addressed but key evidence deferred (Section 3.2):** The paper argues the comparison is fair because zero-shot outperforms one-shot for plain text, but the actual supporting numbers are deferred to an OSF link (Anonymous, 2025). A reader of the submitted paper cannot verify this claim. While Table 2's "best of sampled Zero & One shot" is a reasonable approach, transparent reporting of the one-shot baseline would strengthen the paper.
- **o1-mini regression on Mystery Blocksworld receives only a post-hoc explanation (Section 4.2):** Performance drops from 19.1% to 16.83% under TMK. The paper attributes this to "capacity limitations," but this is untested. If TMK is a generally useful cognitive scaffold, its failure mode on smaller models deserves more serious investigation — it suggests TMK's benefits may be model-scale-dependent or may add cognitive load that smaller models cannot absorb.
- **No variance estimates or significance tests (Table 2):** All results are single accuracy values with no indication of multiple runs, confidence intervals, or statistical significance. Given LLM output stochasticity, especially for smaller gains (e.g., GPT-4o Classic 35.5% → 45.3%, GPT-5 Mystery 98.1% → 98.3%), it is impossible to assess reliability. While single-run evaluation is common in PlanBench literature, the paper's central claims about TMK as a mechanism would benefit from multiple-run reporting.

### Trivial

None.

## Nice-to-Haves

- A control condition providing the same domain knowledge (action preconditions, effects, concepts) in plain text prose, matched for information content, to isolate whether TMK's specific structure adds value.
- Reporting with confidence intervals or multiple independent runs.
- One-shot plain text baseline results included in the main paper.
- Analysis of where TMK helps most (e.g., by plan length, number of blocks) to give insight into mechanism.
- Comparison with other structured formats (PDDL, alternative JSON schemas) to isolate what about TMK specifically matters.

## Removed Points

These points from the harsh critic input were removed or downgraded with justification:
- **"The plain text baseline is 'much sparser'"** — Reformulated as a more precise statement about the lack of documentation. The exact information content of the baseline "domain portion" is not provided in the paper, so the degree of confound is real but the strong "much sparser" characterization goes beyond what can be verified from the paper.
- **"Enhanced extraction function could differentially benefit TMK"** — Speculative; no evidence provided that extraction function creates a systematic bias favoring TMK.
- **Requests for PDDL comparison, cost/latency analysis, per-plan-length analysis** — Scope creep; moved to Nice-to-Haves. These are outside the paper's stated scope and not standard requirements for a prompting paper.
- **"o1-mini regression undermines the general claim"** — Overstated. The paper does address it (Section 4.2) with a hypothesized explanation; it's a real concern but better characterized as Minor rather than the implied structural flaw.

## Novel Insights

None beyond the paper's own contributions. The reviews raise valid methodological concerns (information confound, overclaimed mechanism) but do not identify any novel synthesis or overlooked finding that the authors do not present.

## Suggestions

1. Add a control condition providing the same domain knowledge in plain text prose to disentangle information content from structural contribution.
2. Add multiple-run reporting with confidence intervals for all conditions.
3. Include one-shot plain text baseline results in the main paper.
4. Tone down the mechanistic claims in the abstract and introduction to match what the experimental design can support — frame TMK as improving performance rather than definitively steering models toward code-execution reasoning, unless direct evidence is provided.
5. Investigate the o1-mini failure mode more systematically — understanding when and why TMK hurts performance would strengthen the paper.

## Score and Decision

The paper introduces a genuinely novel perspective (TMK from cognitive science) and reports one striking empirical result (o1 on Random Blocksworld). However, two major weaknesses limit its contribution in the current form: (1) the experimental design does not control for whether observed gains come from TMK's structure versus simply providing more domain knowledge, and (2) the paper's central theoretical claim — that TMK acts as a "symbolic steering mechanism" activating code-execution pathways — is asserted in the abstract and discussion but is unsupported by direct evidence. The gap between what the paper claims and what its experimental design can establish is too large for acceptance. The contribution could be rehabilitated with proper controls (plain text with equivalent information, direct one-shot baselines, variance reporting), but as submitted, the evidence does not match the strength of the claims.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>