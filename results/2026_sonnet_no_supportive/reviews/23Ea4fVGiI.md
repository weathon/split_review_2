Now I have a thorough understanding of the paper. Let me draft the review and proceed with calibration.**Round 1 Bracket**: Based on the calibration, this paper sits in the **3–5** range. "LLMs Can Plan Only If We Tell Them" (K3KrOsR6y9, avg 6.40) is the closest topical match but is significantly stronger: it runs ablations, tests multiple benchmarks, and isolates its method's contribution. "Planning in Strawberry Fields" (jOuHjFw71C, avg 3.00) also evaluates o1 on PlanBench but was rejected for limited novelty. The current paper has a more focused novel finding (TMK + performance inversion), but lacks ablations, has an unresolved content/structure confound, reports no statistics, and covers only one domain. I place it at **3.5**.

---

## Summary
This paper applies the Task-Method-Knowledge (TMK) framework—a cognitive-science knowledge representation—as a structured prompt to improve LLM performance on PlanBench Blocksworld planning tasks. Using automated PDDL validation, the authors demonstrate accuracy improvements across GPT-4, GPT-4o, o1-mini, o1, and GPT-5, with the headline result being o1's jump from 31.5% to 97.3% on Random Blocksworld. The authors additionally observe a "performance inversion" on o1 under TMK—where opaque symbolic tasks (Random) become easier than semantically misleading ones (Mystery)—and hypothesize that TMK's structured JSON format steers the model toward code-execution reasoning pathways.

---

## Strengths

- **Striking, validator-verified empirical gain.** o1's improvement from 31.5% to 97.3% on PlanBench Random Blocksworld (Table 2) is large and the metric is rigorous: PlanBench's automated PDDL validators check formal plan correctness step-by-step, not just final-state matching, making the result difficult to game.
- **Performance inversion is a concrete, novel observation.** Under plain text, o1 follows the typical LLM pattern (Mystery 74.3% > Random 31.5%); under TMK this reverses (Random 97.33% > Mystery 83.3%). This is a specific, reproducible finding that goes beyond "better prompting helps" and merits explanation.
- **Principled engagement with canonical criticisms of prompting-for-planning research.** Section 5.1 directly addresses three established critiques (n-shot similarity exploitation, CoT contradicting final answer, cross-domain generalization), takes concrete precautions (non-matching one-shot example, full step-by-step validation), and documents why zero-shot outperforms one-shot for plain-text to de-confound example provision from TMK formatting.

---

## Weaknesses

### Fatal
None.

### Major

- **Unresolved content/structure confound undermines the central causal claim.** The TMK prompt (Figure 1, Section 3.1) encodes for each Blocksworld action: natural-language description, explicit parameters, formal preconditions (`Given`/`Requires`), formal postconditions (`Makes`/`Provides`), and a process description. The plain-text PlanBench baseline does not include this explicit action-specification content. The paper claims that TMK's *specific representational features*—teleological linking, Task-Method-Knowledge hierarchical decomposition—are responsible for the gains. But the experiment cannot distinguish this from the simpler explanation that supplying *any* formal, complete action specification (in any format) helps models plan. The natural control—same semantic content in flat prose or a minimal JSON schema—is never run. Section 5.3 (Limitations) does not acknowledge this as a limitation; it discusses only scope (Blocksworld, OpenAI models). Without the ablation, the specific TMK contribution is indistinguishable from an information-delivery effect.

- **No variance or sample sizes reported.** Table 2 presents point estimates only with no denominators, confidence intervals, or statistical tests. For the most important result (o1 Random: 97.33%), the reader cannot assess whether 97.33% is over 30 problems or 300. For smaller gains—GPT-4 Classic (34.6%→39.7%), GPT-4o Random (0.83%→4.83%)—it is impossible to determine whether the improvement is statistically meaningful or noise.

- **One-shot TMK vs. zero-shot baseline comparison is incompletely defended.** Section 3.2 argues that comparing one-shot TMK to zero-shot is conservative because zero-shot outperforms one-shot for plain text. However, the TMK one-shot example includes the full domain specification in TMK format, making it structurally and informationally far richer than a plain-text one-shot. The relevant comparison is TMK one-shot vs. a content-equivalent one-shot baseline—not zero-shot. This compounds the content/structure confound.

### Minor

- **Performance inversion mechanism is underspecified due to opaque inter-variant prompt differences.** Section 3.1.4 acknowledges that "there are also differences in TMK in classic blocksworld, mystery blocksworld, and random blocksworld." These differences are hosted on an OSF link, not presented in the paper. If the Mystery TMK introduces an additional translation step (two naming systems in context simultaneously), the inversion could arise from parse difficulty rather than "semantic overload." The interpretation in Section 4.2 and 5.2.1 cannot be evaluated without seeing the variant prompts directly.

- **Extraction function modification is inadequately characterized.** Section 3.2 describes changes to PlanBench's extraction code for Random Blocksworld to handle stochastic artifacts (extra words, symbols). The paper does not clearly state whether this modified extraction was applied identically to all model conditions—including the plain-text baselines—or only to TMK outputs. If asymmetrically applied, the modification could inflate TMK accuracy relative to leaderboard baselines.

- **The code-execution hypothesis (Section 5.2.1) is entirely post-hoc.** The claim that TMK's JSON structure activates code-execution reasoning pathways has no supporting interpretability evidence—no reasoning-trace inspection, no ablation varying JSON format independent of content. The hypothesis may be correct, but as written it is storytelling around a correlation.

### Trivial

- The o1-preview row in Table 2 contributes no comparison value (TMK results listed as "NA" due to deprecation) and adds confusion; it could be relegated to a footnote or dropped.

---

## Nice-to-Haves

- A content-matched ablation (same preconditions/postconditions in flat prose or a minimal `requires`/`provides` JSON without the Task/Method/Knowledge hierarchy) is the single experiment that would directly test whether TMK *structure* adds value beyond information delivery.
- Sample sizes and, where feasible, confidence intervals should appear in Table 2 or a caption note.
- The Mystery and Random TMK prompts should appear in the main text (or an in-paper figure/table), not only in the OSF link, so readers can evaluate the inversion mechanism directly.
- Future work on at least one additional PlanBench domain (e.g., Logistics) would begin to address generalizability.

---

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Harsh critic's "fatal/structural" framing of the content/structure confound**: The critic argues this "cannot be filled in revision." This overstates the severity—the ablation is runnable, and the empirical findings retain value even without the causal attribution being fully resolved. Demoted from "fatal" to "major."
- **o1-preview row criticism as "confusing"**: Retained only as trivial; not a substantive flaw.
- **Generic strength: "addresses an important problem"** — removed as generic; only the concrete strengths (empirical gain scale, performance inversion) are retained.

---

## Novel Insights
The performance inversion—where TMK reverses the typical LLM difficulty ordering (Mystery > Random) to Random > Mystery for o1—is the most distinctive contribution. If the content/structure confound were resolved, this inversion could be a meaningful mechanistic signal about how structured prompts interact with LLM latent space (linguistic vs. symbolic modes). The hypothesis that JSON-structured prompts activate code-training pathways (Section 5.2.1) is speculative but could be tested in models that expose reasoning traces, and aligns with emerging evidence (Chen et al., 2024) that code-based execution outperforms textual reasoning on symbolic tasks.

---

## Suggestions

1. **Run the key ablation**: provide the same preconditions, postconditions, and process descriptions as the TMK but in flat prose or a minimal JSON schema without the Task/Method/Knowledge hierarchy. This is the experiment that would test whether TMK structure—rather than information content—drives the gains.
2. **Report sample sizes and variance**: at minimum, state the number of problems per condition in Table 2's caption, and flag which gains meet a reasonable significance threshold.
3. **Include variant prompts in the main text**: add a table comparing Classic, Mystery, and Random TMK prompts so readers can evaluate the inversion mechanism without following an external link.
4. **Clarify extraction function scope**: add a sentence in Section 3.2 explicitly confirming that the modified extraction was applied to all model/condition combinations, including plain-text baselines.
5. **Update Section 5.3 (Limitations)**: acknowledge the content/structure confound as a primary limitation alongside scope.

---

## Score and Decision

**Anchor papers retrieved:**

| Path | Avg Human Score | Round | Comparison |
|---|---|---|---|
| `koza5fePTs.md` | 2.00 | R1 | Planning benchmark survey; less focused finding, weaker than this paper |
| `cWrqs2lwCJ.md` | 3.00 | R1 | Backward planning prompting; similar empirical scope, also rejected |
| `jOuHjFw71C.md` | 3.00 | R1 | o1 planning/scheduling; rejected for limited novelty beyond evaluating existing models |
| `BW8O4wHgbo.md` | 3.00 | R1 | Multi-agent LLM planning; empirical paper with limited contribution |
| `DZBFchnM3b.md` | 3.67 | R1 | LLM search problem reasoning; new benchmark, broader than this paper |
| `OPdmIxdkPb.md` | 4.75 | R1 | Query-efficient planning; more rigorous with competing frameworks |
| `UiLtbLsiPU.md` | 4.50 | R1 | Embodied planning benchmark; broader scope |
| `SkETBJRKH7.md` | 5.25 | R1 | PFC-inspired planning architecture; deeper mechanistic contribution |
| `K3KrOsR6y9.md` | 6.40 | R1 | "LLMs Can Plan Only If We Tell Them" (AoT+); most topically similar, accepted — has ablations, multi-benchmark, clear method isolation |
| `NUD03NBDOE.md` | 6.75 | R1 | Action reasoning benchmark; new benchmark + evaluation, stronger contribution |

**Round 1 bracket**: 3–5. The paper's empirical finding is real and interesting, but critically lacks the ablation needed to support its central causal claim, has no statistical reporting, and covers only one domain. It is clearly weaker than K3KrOsR6y9 (avg 6.40), which had ablations and multi-domain evaluation. It is somewhat stronger than the avg-3.0 papers (which were rejected for limited novelty without even a structural confound issue), because the performance inversion is a more specific and interesting observation than simply re-evaluating o1. Settled at **3.5**.

MY FINAL SCORE: <score>3.5</score>
MY FINAL DECISION: <decision>Reject</decision>