## Summary
# Final Review Report

## Summary

This paper investigates whether incorporating the Task-Method-Knowledge (TMK) knowledge representation framework into LLM prompts improves planning performance on the PlanBench Blocksworld benchmark. The authors replace the natural-language domain description in standard PlanBench prompts with a TMK-formatted JSON structure that explicitly encodes tasks (goals), methods (mechanisms), and domain knowledge. Experiments across OpenAI models (GPT-4, GPT-4o, o1-mini, o1, GPT-5) show that TMK-structured prompts consistently improve accuracy on Classic, Mystery, and Random Blocksworld variants, with the largest gain observed on o1 for Random Blocksworld (31.5% → 97.3%). The paper argues that TMK acts as a "symbolic steering mechanism" that shifts model inference from linguistic pattern-matching toward code-like symbolic processing.

**Strengths:** The paper addresses a timely and well-motivated question (whether structured knowledge representation can improve LLM planning), uses a rigorous benchmark (PlanBench with formal plan validation), and reports comprehensive experiments across multiple model families. The "performance inversion" finding (o1 performing better on Random than Mystery under TMK) is an interesting empirical observation.

**Core weaknesses:** (1) The central mechanistic claim — that TMK steers models toward code-like reasoning — is not supported by the experimental design, which only measures output accuracy without internal-state analysis or necessary control conditions (e.g., JSON-format-only without TMK semantics). (2) The comparison between TMK one-shot and plain-text zero-shot baselines introduces a confound that is inadequately addressed. (3) No statistical significance testing or variance reporting is provided, making it unclear whether key findings (including the "performance inversion") are reliable. (4) The paper's theoretical contributions (steering mechanism hypothesis, cognitive scaffolding) are stated as findings rather than speculations, over-interpreting the available evidence.

**External literature verification:** This run operates in Retrieval-Disabled Mode (paper_search unavailable). Consequently, novelty/comparison claims (e.g., "surpassing SoTA") are deferred for manual verification and should be treated as provisional until independently confirmed against the published literature.

**Recommendation:** The empirical finding that TMK-structured prompts improve planning accuracy is reasonably well-supported and of interest to the community. However, the paper's stronger claims about mechanisms (steering, code-adjacent inference) require substantial additional evidence and more cautious framing. Major revision is needed focusing on tightening the experimental design (adding JSON-only controls, reporting variance, aligning prompting regimes) and recalibrating the strength of causal claims to match the evidence level.

## Strengths
**1. Well-motivated research question.** The paper tackles an important and timely question: whether structured knowledge representation (TMK) can improve LLM performance on planning tasks — a domain where LLMs are known to struggle. The motivation is grounded in prior critiques of existing prompting methods (CoT, ReACT), and the connection to cognitive science provides an interesting interdisciplinary perspective.

**2. Rigorous benchmark selection.** Using PlanBench with its formal plan validation (VAL, Fast Downward) is a strength. The benchmark requires every step of a plan to be formally correct, avoiding the evaluation inflation common in less structured reasoning tasks. The inclusion of Classic, Mystery, and Random variants is a well-designed testbed for assessing sensitivity to semantic priors.

**3. Broad model coverage.** Experiments span five OpenAI models (GPT-4, GPT-4o, o1-mini, o1, GPT-5) covering both standard LLMs and reasoning models (LRMs). This breadth adds confidence that the observed accuracy improvements are not specific to a single model architecture.

**4. Interesting empirical finding.** The "performance inversion" — o1 performing better on Random Blocksworld (97.3%) than Mystery (83.3%) under TMK — is a genuinely interesting observation. If replicable with proper statistical testing, this result could inform hypotheses about how model scale and reasoning capability interact with prompt structure.

**5. Clear presentation of TMK framework.** Figure 1 provides a useful visual overview of the TMK decomposition for Blocksworld. The description of TMK components (Tasks, Methods, Knowledge) and their mapping to the planning domain is conceptually clear and helps readers understand what is being prompted.

**6. Thoughtful discussion of potential mechanisms.** While the mechanistic claims are stronger than evidence supports (as noted in Weaknesses), the paper does attempt to articulate two coherent hypotheses (code-execution steering and cognitive scaffolding) that future work can test. The paper is transparent about some of its limitations, acknowledging the single-domain focus and the need for broader validation.

## Weaknesses
The weaknesses are organized from highest to lowest impact on the paper's validity and contribution claims.

### W1. Mechanistic claims exceed experimental evidence (Severity: Critical, Fixable: Yes — with substantial revision)

The paper's central theoretical contribution is that TMK acts as a "symbolic steering mechanism," shifting model inference "away from default linguistic modes to engage formal, code-execution pathways." This claim is stated in the Abstract, Introduction, Discussion, and Conclusion as a finding, but the experiments provide no evidence about internal model mechanisms:

- **No control for JSON formatting.** The TMK prompt uses JSON syntax, but there is no control condition where the same domain knowledge is presented in JSON *without* TMK's semantic decomposition. Observed gains could be entirely due to JSON structure activating different attention patterns rather than TMK-specific semantics.
- **No reasoning-trace analysis.** The paper speculates about "code-like internal token manipulation" but never analyzes model outputs, attention patterns, or reasoning tokens to verify this claim.
- **No falsifiable operationalization.** The hypothesis is stated as "TMK improves planning by steering toward code-like reasoning" but no testable predictions are derived that could distinguish this from alternative explanations (e.g., TMK simply provides better-structured context).
- **The "cognitive scaffolding" explanation** (Section 5.2.2) is presented as an explanation but is entirely speculative — the paper does not analyze whether TMK produces qualitatively different reasoning traces.

**Required action:** (a) Add a JSON-only control experiment, (b) replace causal claims with evidence-consistent phrasing ("is consistent with," "suggests"), (c) operationalize the steering hypothesis into testable predictions for future work, (d) either provide reasoning-trace analysis or explicitly state that mechanism remains unverified.

### W2. Comparison confound: One-shot TMK vs. zero-shot baseline (Severity: Major, Fixable: Yes)

TMK is tested in one-shot mode but compared against zero-shot results from the public PlanBench leaderboard. The authors argue this is "inconsequential" for three reasons, but each has counterarguments:

1. Original PlanBench used one-shot, but the comparison target (Valmeekam 2023 leaderboard) is zero-shot. The paper's justification does not address this mismatch.
2. "Zero-shot outperforms one-shot for plain text" — if true, comparing TMK one-shot against a plain-text zero-shot baseline means TMK is tested in its *weaker* regime while the baseline is tested in its *stronger* regime. This could underestimate TMK advantage, but it also means the results are not directly comparable.
3. Without reporting plain-text one-shot results for the same models under the same conditions, the magnitude of TMK's improvement relative to a truly matched baseline remains unknown.

**Required action:** Report plain-text one-shot baselines alongside TMK one-shot results for at least one representative model per category (LLM and LRM) in the main results table. If the data already exists in the OSF repository, add it to Table 2.

### W3. Missing statistical significance and variance reporting (Severity: Major, Fixable: Yes)

Table 2 reports only single-point accuracy percentages with no variance, confidence intervals, or significance tests. This has several consequences:

- The key "performance inversion" (o1: 97.33% Random vs. 83.3% Mystery under TMK) may or may not be statistically significant — the reader cannot assess reliability.
- Gains of a few percentage points (e.g., GPT-4o Classic: 35.5% → 45.3%) could be within noise range without multiple trials.
- o1-mini Mystery degradation (19.1% → 16.83%) could be random fluctuation.
- The number of test problems per variant is not stated in the main text.

**Required action:** (a) Report the number of problems per Blocksworld variant, (b) conduct multiple trials (≥3 seeds) and report mean ± std, (c) add appropriate significance tests (e.g., McNemar's test for paired accuracy comparisons).

### W4. Unsupported SOTA claim (Severity: Major, Fixable: Yes — with better scoping)

The paper states TMK "surpasses state-of-the-art (SoTA) performance identified in recent literature for flagship models" and makes similar claims throughout. However:

- Without external literature verification (which is disabled in this run), the SOTA claim cannot be independently verified.
- The comparison against PlanBench leaderboard results is confounded by the one-shot vs. zero-shot mismatch (W2).
- Even if accuracy numbers are higher, the paper does not provide a fair comparison of inference costs, latency, or implementation complexity.

**Required action:** Bound SOTA claims to the specific experimental conditions. Use phrasing such as "outperforms the best reported results on the PlanBench Blocksworld leaderboard for OpenAI models under one-shot prompting." Where direct comparison is unavailable, acknowledge this explicitly.

### W5. Over-claiming in title, abstract, and conclusion (Severity: Moderate, Fixable: Yes)

Several statements are stronger than the evidence supports:
- Title: "KNOWLEDGE MODEL PROMPTING INCREASES LLM PERFORMANCE ON PLANNING TASTS" — implies general planning, but only Blocksworld was tested.
- Abstract: "functions not merely as context, but also as a mechanism that steers reasoning models" — claims mechanism without mechanistic evidence.
- Conclusion: "This confirms that TMK acts as a symbolic scaffold" — confirmation requires stronger evidence.
- "Fundamental performance inversion" — "fundamental" is an overstatement for a single observation without significance testing.

**Required action:** Replace certainty and causal language throughout with bounded, evidence-grounded phrasing. The title should either be narrowed (e.g., "TMK Prompting Improves Accuracy on PlanBench Blocksworld") or include a qualifier (e.g., "Evidence That Structured Knowledge Representation Improves LLM Planning Performance").

### W6. Omitted prompt details harm reproducibility (Severity: Moderate, Fixable: Yes)

The Methods section describes the TMK framework conceptually but does not include the actual prompt template used. Appendix A is referenced but not included in the submission. Since prompt engineering results are highly sensitive to formatting details, the following information is essential:

- Exact JSON structure of the TMK prompt for each Blocksworld variant
- The one-shot example provided (with caveats about its relation to the query)
- System prompt, if any
- Temperature, sampling parameters, and number of response tokens allocated

**Required action:** Include complete prompts for all three variants (Classic, Mystery, Random) either in the main text or a clearly referenced appendix. Provide exact inference parameters.

### W7. o1-mini negative result not adequately analyzed (Severity: Moderate, Fixable: Yes)

The o1-mini results are puzzling: TMK helps on Random (9.33% → 27.0%) and Classic (56.7% → 57.0%) but hurts on Mystery (19.1% → 16.83%). The paper's explanation ("capacity limitations in resolving semantic interference") is a post-hoc speculation without support from the data. Understanding when TMK *hurts* performance is as important as when it helps, and this case deserves dedicated analysis.

**Required action:** Analyze o1-mini outputs to understand the failure mode. Is the model producing invalid actions, incomplete plans, or semantically confounded steps? Add a dedicated analysis paragraph in the Discussion and, if possible, a small ablation experiment to test the semantic overload hypothesis.

### W8. Introduction narrative structure could be improved (Severity: Minor, Fixable: Yes)

The introduction does not follow a clean problem-gap-solution narrative. It mixes critiques of CoT, mentions of cognitive science, descriptions of TMK, and results previews across paragraphs without a clear logical progression. Some paragraphs (e.g., the discussion of optimization techniques and catastrophic forgetting) are tangential.

**Required action:** Restructure the introduction into a clear arc: (P1) LLM planning limitations, (P2) limitations of existing prompting methods (CoT, ReACT), (P3) why TMK is designed to address these gaps, (P4) hypothesis and predictions, (P5) experimental approach and key results preview, (P6) contributions.

### W9. Related work is too list-like (Severity: Minor, Fixable: Yes)

Section 2.1 presents CoT, CoS, and ReACT as separate subsections in a paper-by-paper format rather than organizing around comparison axes. The differences between these methods and their relationships to TMK are not synthesized.

**Required action:** Reorganize around themes: (a) methods for LLM reasoning prompting (CoT, ReACT, CoS), (b) formal planning benchmarks for LLMs (PlanBench), (c) knowledge representation frameworks (TMK, BDI, HTN). For each, explicitly state what TMK adds.

### W10. Title formatting error (Severity: Cosmetic, Fixable: Yes)

The title in the paper text reads "PLANNING TASKS" on the first line — likely a typo for "TASTES" or "TASKS" (the abstract correctly says "planning tasks"). Additionally, the use of all caps in the title makes it harder to read.

## Score
**Final Score: 5/10**

**Scoring rationale (evidence-grounded, prioritizing research value and novelty):**

The paper has a legitimate empirical finding — TMK-structured prompts improve planning accuracy on Blocksworld — which has practical value for the prompt engineering community. The choice of PlanBench as a benchmark is sound, and the multi-model evaluation provides useful breadth.

However, the paper's score is constrained by several fundamental issues:

- **Research value (primary dimension):** The paper's core claimed contribution — that TMK acts as a symbolic steering mechanism — is not supported by the experimental evidence. The empirical finding (accuracy improvements) is useful but incremental without mechanistic understanding. The paper would have higher value if it established why TMK works, not just that it works.
- **Novelty (primary dimension):** External literature verification is unavailable in this run (Retrieval-Disabled Mode). However, based on the paper's own description, the application of TMK (a known framework) to LLM prompting is a reasonable contribution, but the paper does not isolate what is specifically novel about this application vs. simply using structured JSON prompts. The lack of a JSON-only control makes the novelty claims vulnerable.
- **Validity/Soundness:** Several major validity concerns (comparison confound in W2, missing statistics in W3, over-claimed mechanisms in W1) reduce confidence in the paper's conclusions. The core "performance inversion" finding may be reliable, but the paper's stronger theoretical claims are not.
- **Reproducibility:** Missing prompt templates and inference parameters (W6) make independent reproduction difficult.

A score of 5 reflects a borderline paper: the empirical direction is promising, but substantial revisions are required to bring the evidence and claims into alignment. The paper needs tighter experimental controls, more cautious framing, and additional analysis before it can be considered a strong contribution.

**Post-Revision Target: [6, 7]/10**

A revision that (a) adds JSON-only control experiments, (b) reports variance and significance tests, (c) recalibrates all causal claims to match evidence level, (d) adds plain-text one-shot baselines, and (e) provides complete prompt templates could reasonably achieve a score of 6-7. The upper bound of 7 reflects the inherent limitation that the core hypothesis about mechanisms cannot be fully tested without reasoning-trace analysis or probing experiments.