## Summary

This paper introduces LPFQA, a benchmark of 505 questions sourced from real professional technical forums across 20 fields, designed to evaluate LLMs on long-tail professional knowledge and complex reasoning. The benchmark is constructed via an automated pipeline (crawling, MLLM-based QA extraction, LLM-based cleaning, expert verification, difficulty calibration), and 12 models are evaluated. The core idea — sourcing evaluation questions from authentic practitioner discussions rather than exam banks or synthetic data — addresses a genuine gap in LLM evaluation.

## Strengths

- **Authentic sourcing from professional forums (Section 3.2.1).** Questions originate from real discussions on platforms like Project Euler, CONTROL.com, mathematics and chemistry forums, reflecting actual problems practitioners encounter. This is a principled departure from synthetic or exam-based benchmarks and justifies the paper's claim of measuring authentic long-tail professional knowledge.

- **Broad disciplinary coverage with structured evaluation dimensions (Section 3.1).** 20 fields (CS, Math, Biology, Physics, Chemistry, Finance, Law, etc.) is broader than many specialized benchmarks. The four proposed evaluation dimensions (knowledge depth, reasoning, terminology comprehension, contextual analysis) provide a more structured approach than single-accuracy-per-domain reporting.

- **Clear automated construction pipeline (Section 3.2).** The eight-step pipeline from crawling to expert verification is systematically described, and the three-phase organization (data collection, automated QA generation, expert verification + difficulty adjustment) is logical and reproducible in principle.

## Weaknesses

### Major

- **Factual error in the main performance analysis (Section 4.1, line 265).** The paper states: *"Among all evaluated systems, DeepSeek-V3 demonstrates the most balanced and consistent performance across disciplines, with no apparent weaknesses, and can thus be regarded as the overall best-performing model."* In Table 1, DeepSeek-V3 scores **32.60** — the second-lowest score among all 12 models, well below the average of 39.08. GPT-5 scores 47.28 (highest). Calling a model that underperforms nearly every other model "the overall best-performing" is incoherent and contradicts the paper's own data. This error undermines confidence in the analysis section and must be corrected.

- **Missing correlation analysis with existing benchmarks.** For a benchmark paper, the central validation question is whether the benchmark measures something distinct from what existing benchmarks already capture. The paper provides no correlation analysis between model rankings on LPFQA and established benchmarks (MMLU, HLE, Arena-Hard, etc.). Without this, the claim that LPFQA captures distinct long-tail professional capabilities is unsubstantiated. If rankings correlate perfectly with MMLU, the benchmark is redundant; if they diverge in interpretable ways, that is the key evidence the paper should present. This is the most consequential validation gap.

- **Circularity in the post-hoc filtering procedure (Section 4.2.1).** The paper removes questions that "none of the evaluated models could correctly answer" (505→436) and questions that "all models could answer" (436→421), using the **same 12 models** that are then re-evaluated on the filtered set. This creates circularity: the benchmark is pruned to differentiate the specific cohort being tested. The filtered variants (LPFQA⁻, LPFQA⁼) are therefore not independent evaluation instruments but sets engineered for these particular models. While the paper is transparent about the procedure, it does not acknowledge or address this circularity (e.g., by holding out some models during filtering).

- **Unsupported conclusions from the ablation studies (Section 4.2.2).** 
  - **Code Interpreter (Table 3):** The paper finds adding a code interpreter decreases scores and concludes *"LPFQA primarily reflects a model's mastery of domain knowledge rather than its reasoning ability."* This is a non-sequitur. A code interpreter assists with *computational* reasoning; if the questions predominantly test declarative knowledge (e.g., "What happens to endplate potentials when firing frequency decreases?"), the tool is simply the wrong instrument. The drop could equally reflect poor tool-integration or interference with normal inference.
  - **Search Tool (Table 4):** The paper attributes decreased performance to long-tail knowledge being hard to retrieve. This is plausible but unsupported — no evidence distinguishes this from alternatives (poor query formulation, failure to integrate retrieved information, search noise). The claim that "simply augmenting models with online search does not provide a positive effect" overgeneralizes from a single configuration.

### Minor

- **Per-field conclusions are drawn from tiny sample sizes (Section 3.3).** Several fields have single-digit or very small counts: Data Science (3), Information and Communication Engineering (7), Aerospace (8), Artificial Intelligence (8), Energy (9). After filtering to LPFQA⁼, these become even smaller. The paper draws per-field conclusions (e.g., "GPT-5 shows clear superiority in Phys and AI," "Seed-1.6 leads in Aero and Bio") without acknowledging that these claims rest on 3–8 questions. No confidence intervals or measures of variance are reported anywhere.

- **Missing construction pipeline details.** (a) The specific MLLM used for question generation is not named (Section 3.2.2 only says "MLLM"). (b) The specific LLM used for cleaning/formatting is not named. (c) The expert verification step (Section 3.2.3) provides no information on number of experts, their qualifications, or the rate of corrections. (d) The "empirical difficulty test" uses "multiple LLMs" (line 134) without naming them, raising ambiguity about whether the same models used for evaluation were also used for difficulty calibration.

- **Inconsistency between abstract and body (Abstract vs. Section 3.1).** The abstract states **502 tasks**, while the body (lines 21, 207, Figure 2 caption) states **505 questions**. This discrepancy suggests sloppiness in final editing.

- **No qualitative or error analysis.** The paper evaluates models on four dimensions (knowledge depth, reasoning, terminology comprehension, contextual analysis) and surfaces performance disparities, but provides no analysis of *what kinds of errors* models make. Characterizing error types would substantiate the claimed evaluation dimensions and provide actionable insights.

### Trivial

- **No statistical dispersion reported.** Results are "averaged over three trials" (line 211) but presented as point estimates without standard deviations or confidence intervals in any table.

## Nice-to-Haves

- Correlation/divergence analysis with at least MMLU and HLE would answer the decisive question of whether LPFQA captures distinct capabilities. This is the single highest-leverage improvement and would require no additional data collection.
- If post-hoc filtering is retained, split models into a calibration set (for identifying floor/ceiling questions) and a held-out evaluation set to avoid circularity.
- The per-field radar charts (Figure 3) with 12 overlapping plots are difficult to read; a heatmap or grouped bar chart would better support cross-model comparison.

## Removed Points

The following points from the input review are removed, with justification:

- **"Reproducibility statement is a promise, not a current reality."** — REMOVED per hard rule: criticism of release status/availability of the paper's own dataset is disallowed. The paper states it will release the benchmark, which is an acceptable reproducibility commitment for a submission.
- **"Introduction's characterization of MMLU as overly simple is unfair."** — REMOVED as a scope-creep criticism; the paper's characterization of prior benchmarks is a matter of positioning, and even if slightly overstated, it does not affect the paper's own contributions.
- **"HLE comparison: LPFQA's questions also have limited everyday relevance."** — REMOVED as a misinterpretation; the paper contrasts with HLE's *extreme* difficulty (not everyday relevance), while LPFQA targets *professional* scenarios. Both are valid but different scopes.
- **"Radar charts are difficult to interpret."** — DEMOTED from weakness to nice-to-have; this is a presentation preference, not a methodological flaw.
- **"The 'per-field radar charts (Figure 3) are difficult to interpret with 12 overlapping plots'"** — A formatting/style critique; moved to nice-to-haves.

## Novel Insights

None beyond the paper's own contributions. The reviewer's critiques are standard methodological assessments of benchmark validation (correlation analysis, circularity in filtering, sample size issues, unsupported causal conclusions from ablation). There is no novel synthesis that the authors themselves have not already considered or that meaningfully reframes their contribution.

## Suggestions

- Correct the DeepSeek-V3 "overall best-performing" claim to be consistent with Table 1. If the intent was to highlight balanced per-field performance, state this explicitly and reconcile with the aggregate data.
- Add a correlation analysis (e.g., Spearman rank correlation) between model rankings on LPFQA and at least MMLU and HLE. This is the standard validation step for a new benchmark and is necessary to substantiate claims of measuring distinct capabilities.
- Either (a) drop post-hoc filtering and argue for the full 505-item benchmark on its own merits, or (b) hold out a subset of models from the filtering step and use them solely for evaluation.
- Restructure the ablation experiments to actually test the claims: compare performance on knowledge-heavy vs. reasoning-heavy question subsets, or use models with known reasoning strengths to validate the benchmark's discriminative properties.
- Resolve the 502/505 discrepancy and report confidence intervals or standard deviations for all main results.

## Score and Decision

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>