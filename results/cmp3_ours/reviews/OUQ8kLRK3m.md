## Summary

DRE-Bench is a benchmark for evaluating LLMs' fluid intelligence through abstract reasoning grid tasks organized along a four-level cognitive hierarchy (Attribute → Spatial → Sequential → Conceptual), grounded in the Primi (2001) psychological framework. The benchmark uses a code-based generator-solver pipeline to create dynamic variants of each latent rule, addressing data contamination. The paper evaluates 11 LLMs and reports that performance declines with cognitive level, with models struggling particularly at high-level and conceptual tasks.

## Strengths

1. **Cognitive hierarchy grounded in psychological theory.** The four-level framework (Attribute, Spatial, Sequential, Conceptual) is explicitly tied to Primi (2001), which argues these levels form a true cognitive hierarchy with increasing demands on abstraction and working memory. This enables more granular statements about model capabilities (e.g., "model X succeeds at Level-1 but fails at Level-3") beyond a single aggregate accuracy score. (Section 3.1, Figure 2)

2. **Code-based generator-solver pipeline for dynamic evaluation.** Each latent rule is backed by a code generator and solver, parameterized by a dynamic variable, enabling generation of multiple variants at different complexity levels. The code verification step with feedback loops aims for correctness of generated data and directly addresses data contamination—a genuine concern for static benchmarks. (Section 3.2, Figure 3)

3. **Human validation study.** The paper conducts a human study with 40 professional annotators on 10% of the benchmark data. Human accuracy decreases with cognitive level (from 77.51% at Level-1 to 47.33% at Level-4), validating that higher-level tasks are genuinely harder for humans too, not just for LLMs. (Section 4.2, Table 1)

4. **Spatial orientation asymmetry finding.** The discovery that models perform systematically better on vertical (up/down) movement than horizontal (left/right) movement, and better on horizontal symmetry than vertical symmetry, is a genuinely interesting and non-obvious result that reveals systematic divergence from human cognitive patterns. (Section 4.5, Table 3)

## Weaknesses

### Major

1. **Data integrity issues in Table 1 erode confidence in quantitative findings.** Three specific problems are verifiable from the paper:
   - **Duplicate or mislabeled model rows.** Two rows are both labeled "o3-mini" but report substantially different numbers (e.g., Shape: 18.33 vs 71.67; Level-4 Mechanics: 0.00 vs 31.75). The Figure 4 caption references an "o1-mini" that appears in Table 3 but not in Table 1, while the paper claims 11 models but Table 1 has at most 10 unique names—suggesting one "o3-mini" row is mislabeled.
   - **Arithmetically impossible average.** Row 148 (first o3-mini) shows Level-2 subscores Rotation=63.04, Move=32.10, Symmetry=0.00 with Avg-2=91.78. An average cannot exceed every individual subscore—91.78 is impossible regardless of weighting scheme and indicates a data-entry or calculation error.
   - **Inconsistent level averages.** The "Avg" columns for several models do not match a simple average of the subscores shown. Examples: DeepSeek-R1 Level-1 average of {60.83, 60.42, 8.33} = 43.19, but table says 37.86; Claude-3.7 Level-1 average of {65.22, 63.14, 13.33} = 47.23, but table says 58.76; QwQ-32B Level-1 average of {78.89, 61.05, 13.33} = 51.09, but table says 65.49. If these averages include additional tasks beyond the columns shown, this must be stated. If miscalculated, the quantitative findings are unreliable.
   
   These are not minor formatting issues—they directly affect whether the paper's empirical results can be accepted. (Table 1, lines 136–154)

2. **Level-4 tasks conflate fluid intelligence with domain-specific knowledge, weakening construct validity.** The paper defines fluid intelligence as "the ability to reason abstractly and generalize rules in novel situations" (Abstract, Introduction), yet Level-4 tasks (Gravity, Reflection, Expansion) require knowledge of specific physical phenomena—objects fall due to gravity, light reflects off walls, objects expand when heated. These require crystallized intelligence: knowledge of specific facts about the world. The paper acknowledges this tension ("require not only high-level abstract reasoning but also the application of conceptual knowledge," Section 3.1) but never resolves it. The finding that "all existing models fail" at Level-4 (Section 4.2) could reflect lack of domain knowledge rather than lack of fluid reasoning. Consequently, the benchmark does not cleanly measure fluid intelligence across all four levels as claimed.

### Minor

3. **No comparison against existing abstract reasoning benchmarks.** The paper positions DRE-Bench as superior to ARC-AGI, PHYSICO, and others along three axes (cognition hierarchy, scalability, dynamic evaluation) but provides no direct comparison. It is therefore difficult to assess whether DRE-Bench provides genuinely new information about model capabilities or largely recapitulates what could be learned from existing benchmarks. Adding correlation plots of model rankings across benchmarks would substantially strengthen the paper's claims.

4. **Statistical reporting is incomplete.** Results are reported as "average results over three trials" (Section 4.1) but no standard deviations, confidence intervals, or per-trial variance are reported for Table 1. While the paper discusses variance in scatter plots (Figure 5), the main results table lacks basic uncertainty quantification.

5. **Human study validation lacks key methodological details in the main text.** While the paper references Appendix E.4 for details (which was stripped by the parser), the main text omits: how annotators were trained on abstract grid reasoning, whether they were given the same few-shot exemplars as LLMs, and the time limit per problem. The t-test claim ("statistical significance of humans' and models' results") is vague—the relevant question is whether the pattern across levels is consistent between humans and models, not whether group means differ.

### Trivial

6. The exact-match metric (output grid must match ground truth exactly) is strict for grids up to 30×30. The paper mentions auxiliary metrics (grid size precision, grid matching percentage) only in the appendix. Reporting partial credit scores in the main text would give a fairer picture of whether models partially grasp the rules.

## Nice-to-Haves

- Show that the cognitive hierarchy provides information beyond overall accuracy—e.g., demonstrating that two models with similar overall accuracy have different "cognitive profiles" across levels.
- Analyze whether dynamic variants at extreme complexity levels (e.g., planning 1 step vs. 10 steps) genuinely test the same latent rule or become qualitatively different.
- Separate the "Model-avg" row by model class (general vs. reasoning LLMs) rather than pooling all models together.

## Removed Points

These points from the input review are removed with justification:

- "No comparison against existing abstract reasoning benchmarks" — kept but placed in Minor, as many benchmark papers do not include such comparisons and this does not invalidate the core contribution.
- "Human study validation is underdescribed" — kept but placed in Minor; the paper explicitly references Appendix E.4 which was stripped by the parser, so some described details likely exist in the full submission.
- "Error bars not reported" — kept in Minor since the paper does report variance in Figure 5.
- The claim that "first to introduce dynamic evaluation for abstract reasoning" is contradicted by DyVal — removed as a presentation phrasing issue, not a substantive weakness.
- "Model-avg pooling concern" and "exact-match metric too strict" — moved to Nice-to-Have and Trivial respectively as they do not threaten core claims.

## Novel Insights

The finding that models perform systematically better on vertical (up/down) movement than horizontal (left/right) movement (Section 4.5, Table 3), and better on horizontal symmetry than vertical symmetry, is genuinely interesting. This reveals a systematic divergence from human cognitive patterns—where directional distinctions are typically perceived as equivalent—and suggests LLMs process spatial orientation differently from humans, possibly due to how spatial relationships are encoded in text training data. This kind of fine-grained cognitive profiling is exactly what the paper's hierarchy framework should enable.

## Suggestions

1. **Fix all numerical inconsistencies in Table 1:** Resolve the duplicate o3-mini / missing o1-mini labeling issue; correct or explain the impossible Avg-2=91.78; clarify whether Avg columns include additional tasks beyond the subscores shown, or recalculate them as proper averages.
2. **Address the Level-4 construct validity** by either (a) renaming Level-4 as "Conceptual Application" and explicitly stating it measures a blend of fluid and crystallized intelligence, or (b) redesigning tasks so they are solvable from first-principles abstract reasoning without requiring domain-specific physics knowledge.
3. **Add a comparison against ARC-AGI or similar benchmarks** to demonstrate what DRE-Bench's cognitive hierarchy reveals that overall accuracy does not.
4. **Add standard deviations or per-trial ranges** to the main results table.

## Score and Decision

**Bracket (Round 1):** 4.5 – 5.5

**Anchors used for calibration:**
- **28gMnEAgl9.md** (5.33, Rejected) — "Large Language Models Are Not Strong Abstract Reasoners": similar abstract reasoning benchmark; rejected for limited novelty. DRE-Bench has greater methodological novelty but worse data quality.
- **SVRRQ8goQo.md** (7.00, Accepted) — KOR-Bench: well-executed reasoning benchmark with clean data and clear central concept. DRE-Bench sits below this due to data integrity issues.
- **WrBqgoseGL.md** (5.80, Rejected) — Putnam-AXIOM: dynamic variation concept similar to DRE-Bench; rejected for small size and manual effort.
- **THSm9HyCKo.md** (5.00, Rejected) — JustLogic: synthetic deductive reasoning benchmark with methodological concerns.
- **1KvYxcAihR.md** (5.75, Rejected) — TMGBench: strategic reasoning benchmark; mixed reviews.

DRE-Bench's cognitive hierarchy and code-generated dynamic pipeline are genuinely novel and address important limitations of prior work. The spatial orientation asymmetry finding is a concrete demonstration of the framework's diagnostic value. However, the data integrity issues in Table 1 (duplicate rows, impossible averages, inconsistent calculations) are verifiable errors that prevent full confidence in the empirical conclusions. Until these are corrected, the quantitative findings cannot be accepted at face value. The Level-4 construct validity concern further weakens the central claim of measuring fluid intelligence. These issues place the paper below the acceptance threshold despite its promising framework.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>