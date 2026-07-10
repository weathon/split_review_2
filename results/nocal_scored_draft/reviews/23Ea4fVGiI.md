Now let me write the final review.

## Summary

This paper introduces Task-Method-Knowledge (TMK) structured prompting — adapted from cognitive science — to improve LLM performance on classical planning tasks. Evaluated on PlanBench's Blocksworld variants (Classic, Mystery, Random), the method reports striking results, including o1's Random Blocksworld accuracy rising from 31.5% to 97.3%. The paper also observes a "performance inversion" where TMK makes opaque symbolic tasks easier than semantically meaningful ones for reasoning models, and proposes that TMK steers models toward "code-execution pathways."

## Strengths

- **Novel cross-domain inspiration.** Importing the TMK framework from cognitive science/education into LLM prompting is genuinely original. Unlike most prompting papers that propose variants of CoT or structured few-shot examples, this paper draws from a distinct intellectual tradition (knowledge-based self-explanation, Murdock & Goel, 2008) and grounds its motivation in that literature.

- **Striking raw results on o1 Random Blocksworld.** The jump from 31.5% to 97.3% (Table 2) is a 65.8 percentage-point improvement on the hardest variant for the best reasoning model. This is large enough to be interesting regardless of interpretation.

- **Rigorous evaluation framework using PlanBench**, which validates every plan step with classical planners (VAL, Fast Downward), requires complete stepwise correctness, and includes domain obfuscation (Mystery, Random) to decouple reasoning from semantic priors. This is substantially more rigorous than typical prompting paper benchmarks.

- **The performance inversion observation** (Section 4.2): for o1, TMK makes Random easier than Mystery (97.3% vs. 83.3%), reversing the plain-text pattern (31.5% vs. 74.3%). This is a genuinely interesting empirical pattern worth investigating further.

## Weaknesses

### Major

- **The comparison does not isolate TMK's specific framework as the causal factor.** The TMK prompt replaces the "domain portion" of the PlanBench prompt (line 169) with a JSON-structured TMK model containing explicit preconditions (Given), effects (Makes), descriptions, and a domain ontology. The paper does not specify what the plain-text baseline's domain portion contains — whether it includes action schemas with preconditions and effects. This conflates at least two variables: (a) format (JSON vs. plain text), and (b) information content (presence/absence of action definitions). The paper cannot attribute gains to TMK's specific teleological/hierarchical framework rather than to simply providing the PDDL domain model in any structured format. No control condition with the same information in a non-TMK format (e.g., bulleted list, PDDL) exists, making it impossible to determine whether TMK's specific Task-Method-Knowledge decomposition matters.

- **The "code-execution pathway" mechanistic claim is unsupported by the evidence.** The abstract (lines 9–10) and conclusion (line 300) state or strongly imply that TMK "steers reasoning models away from their default linguistic modes to engage formal, code-execution pathways." The evidence offered is: (a) TMK is JSON-like, therefore code-like (analogy), and (b) the performance inversion supposedly proves a modality shift (non-sequitur). The paper never tests this hypothesis directly — e.g., by comparing TMK to an explicit code-generation prompt, by analyzing the model's reasoning tokens, or by examining internal representations. Simpler explanations (TMK provides a lookup table, or the explicit action schemas reduce cognitive load) are equally consistent. The paper acknowledges the cause is "left to future work" (line 304), but the abstract and conclusion present it more confidently than warranted.

- **The enhanced extraction function (lines 183–191) applied to TMK results for the Random Blocksworld domain introduces a potential evaluation asymmetry.** The paper states that the original Valmeekam (2023) code "required update" and that new extraction criteria were "applied for random blocksworld data set." If the plain-text baselines from the public leaderboard were evaluated with the original (stricter) extraction while TMK results used the enhanced (more lenient) one, the comparison is not apples-to-apples. The paper does not clarify whether the same extraction function was applied to both conditions. Since the largest reported improvement (o1 Random: 31.5% → 97.3%) is in this domain, the confound is consequential.

### Minor

- **No statistical or variance information** is reported. Table 2 provides only single point estimates with no confidence intervals, standard deviations, or number of runs. For stochastic LLM outputs, smaller differences (e.g., GPT-4o Classic: 35.5% vs. 45.3%) could shift with additional runs, though the largest effects (e.g., 65.8% improvement on o1 Random) are unlikely to be noise.

- **The one-shot/zero-shot asymmetry** in the comparison is not fully resolved. TMK is always one-shot while the plain-text baselines use the "best of sampled Zero & One shot" (Table 2 caption). The paper defends this as conservative (lines 177–181), arguing zero-shot outperforms one-shot for plain text. However, the cleanest comparison would match shot counts: TMK one-shot vs. plain-text one-shot AND TMK zero-shot vs. plain-text zero-shot. The current design conflates shot count with format.

- **The abstract and some passages in the conclusion overclaim** relative to what is demonstrated. "Bridge the gap between semantic approximation and symbolic manipulation" (line 9) implies a general capability advance from a single-domain Blocksworld study. Claims about steering toward "code-execution pathways" are stated more assertively in the abstract/conclusion than the hedging in the body (where it is called a hypothesis, line 23, and future work, line 304) would warrant.

- **Some improvements reported in Table 2 are negligible** but presented as meaningful. GPT-4's improvements on Mystery (0% → 3.8%) and Random (0% → 4.17%) are near-zero in both conditions. GPT-4o's improvement on Random (0.83% → 4.83%) similarly remains near floor.

## Nice-to-Haves

1. Add a control condition presenting the same domain information in a non-TMK structured format (e.g., PDDL domain definition, bulleted list of actions with preconditions/effects) to isolate whether TMK's specific Task-Method-Knowledge decomposition matters.
2. Test the "code-execution" hypothesis directly: compare TMK to an explicit code-generation prompt, or analyze reasoning tokens for code-like structure.
3. Report statistics (means and standard deviations across multiple runs) and specify the number of test instances.
4. Equalize shot counts between TMK and plain-text conditions.
5. Ablate TMK components (e.g., is the Knowledge section necessary? Is JSON format essential?).
6. Compare TMK to other structured prompting methods (CoT, ReACT) in the same experimental setup.

## Removed Points

These points were raised in the input review but removed after verification:

- **"Cognitive scaffolding contradicts claim of avoiding pattern matching"**: Removed. The paper explicitly acknowledges this tension at line 290: TMK "does not offer n-shot solutions to which the LLM then pattern matches, it instead offers expert knowledge to which the LLM pattern matches." This is a nuanced distinction, not a contradiction; the paper frames TMK's pattern matching as qualitatively different from the criticized solution-level pattern matching in CoT/ReACT.
- **Formatting/style nitpicks**: Removed per policy (parser artifacts, not author errors).
- **"o1preview results are deprecated"**: The paper already flags this with a footnote in Table 2.
- **"Section 3.2 example could be misleading"**: The paper acknowledges the example is random and not tailored; this is a deliberate design choice that cuts against pattern-matching concerns.
- **"GPT-5 already scores 92.5% on Random" as a weakness**: The paper's TMK improvement to 99.0% is modest but the paper does not overclaim it; this is a valid observation but not a weakness.
- **Reproducibility concerns about undisclosed hyperparameters**: Removed per policy (standard for API-based LLM evaluation).

## Novel Insights

None beyond the paper's own contributions. The reviewer analysis sharpens the contrast between the empirical results and the mechanistic interpretation, but does not introduce genuinely novel findings about the method.

## Suggestions

1. **Add a control condition** where the same Blocksworld domain information (action schemas with preconditions/effects) is provided in a non-TMK structured format (e.g., PDDL, bulleted list, or JSON with a different schema). This is the single most important addition to support the paper's claims about TMK specifically.
2. **Clarify the extraction function asymmetry**: state explicitly whether the enhanced extraction was applied to both TMK and plain-text conditions or only to TMK. If only to TMK, re-evaluate the plain-text baselines with the same extraction.
3. **Tone down mechanistic claims** in the abstract and conclusion to match the paper's own admission that the cause is "left to future work" (line 304).

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>