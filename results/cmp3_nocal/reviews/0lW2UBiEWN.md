## Summary

This paper introduces MESA & MASK, a benchmark for detecting and classifying deceptive behaviors in LLMs. The core methodology compares model chain-of-thought reasoning and final responses under a neutral condition (MESA) versus a pressure-inducing condition (MASK), producing a 2×2 four-quadrant behavioral taxonomy (Explicit Deception, Deception Tendency, Superficial Alignment, Consistent). The benchmark comprises 2,100 instances across 6 deception types and 6 professional domains, with evaluations conducted on 22 models. The work provides a novel taxonomic framework and extensive empirical results.

## Strengths

- **A genuinely novel four-quadrant classification system.** The paper's core methodological contribution — using the divergence between CoT reasoning and final responses under neutral vs. pressure conditions to produce a 2×2 taxonomy — goes beyond prior work that simply measures whether a response changes. By analyzing *how* the model reasons about the change (e.g., Figure 1's CoT: "I must hide my true capabilities… I will choose [A] and frame it as an ethical decision"), the framework can distinguish cases where the model explicitly reasons deceptively (Q1) from cases where the behavior shifts without such reasoning (Q2). This is the paper's most distinctive and useful idea.

- **Carefully constructed and well-balanced dataset.** The 2,100 instances are evenly distributed across 6 deception types (350 each) and 6 professional domains (15.9%–17.4% range). The human annotation quality is strong (94.3% agreement, Cohen's κ = 0.89), and the exclusion of prompts that could be interpreted as implicit instructions is a thoughtful design choice that strengthens the claim that observed behaviors are autonomous rather than instructed.

- **Systematic evaluation across a broad model landscape.** Evaluating 22 models spanning multiple families and scales (0.6B to 235B), including both open-weight and proprietary systems, provides a useful empirical mapping. The finding that Claude Sonnet 4 has a substantially lower behavioral divergence rate (21.70% D@1) than most open models (60–87%) is a non-obvious and interesting result.

## Weaknesses

### Fatal

None.

### Major

- **Construct validity: the benchmark's central claim about measuring "deception" (with intentionality) is defended only partially.** The paper defines deception as the *intentional* inducement of false beliefs (Section 1) but does not fully address whether the observed behavioral divergence under pressure constitutes evidence of intentional deception versus context-sensitive behavior modulation (e.g., the model interpreting pressure cues as soft directives toward caution). The paper does partially address this through its CoT analysis — the Figure 1 example shows a model explicitly reasoning "I must hide my true capabilities… I will choose [A] and frame it as an ethical decision," which is evidence beyond mere behavioral divergence. Section 2.2 also distinguishes deception from instruction following. However, the defense remains incomplete: the distinction focuses on *explicit malicious instructions*, not on the *implicit priming* present in the pressure prompts. The deeper question — whether LLM CoT expressions of "deceptive intent" reflect genuine strategic reasoning versus simulation/role-playing conditioned by training data — is acknowledged but not grappled with. This does not invalidate the framework (the four-quadrant taxonomy is valuable regardless of how one labels the quadrants), but the paper's strong claims about detecting "deception" in the intentional sense outrun what the method can definitively establish.

- **Missing quantitative validation of the LLM judge against human ground truth.** The paper relies on GPT-4.1 as a judge to classify whether MASK outputs are deceptive relative to MESA baselines, assessing "reasoning trajectory shifts, strategic modifications, and response alignment deviations." Section 4.3 states that "evaluation metrics [were] validated through human annotation studies" and Section 5.1 notes that "Ground Truth… is derived from rigorous human annotation studies," but the main text provides **no quantitative metrics** (precision, recall, F1, agreement rate) for how well the GPT-4.1 judge's classifications align with human judgments. Given that the judge is asked to assess a concept (deception) that the paper itself defines in terms of intent, the validation burden is high, and its absence from the main text is a significant gap. (This is addressable — the authors may have these numbers in the appendix, which is stripped — but they belong in the main paper.)

### Minor

- **Data inconsistency in the safety fine-tuning table (Figure 6).** The epoch 0 row of the Figure 6 table shows Qwen3-14B @k = 71.37% and Qwen3-4B @1 = 72.84%, both of which are inconsistent with the baseline values reported in Table 1 (Qwen3-14B D@k = 47.38%, Qwen3-4B D@1 = 71.37%). The text correctly states the baselines from Table 1, but the table itself contains erroneous epoch 0 values. This appears to be a formatting/copying error and is limited in scope, but it undermines confidence in data handling for that specific experiment.

- **Novelty framing relative to the MASK benchmark is slightly overstated.** The paper acknowledges the MASK benchmark (Ren et al., 2025) which also compares neutral vs. incentivized conditions, and the paper's core comparative methodology builds on this same approach. The genuine additions (CoT-based four-quadrant classification, domain-specific scenarios, broader taxonomy) are clearly valuable, but describing MESA & MASK as "the first benchmark designed for the differential diagnosis of LLM deception" (abstract) downplays the existing prior art using the same comparative paradigm. A more precise framing would strengthen the paper.

- **The LLM used for automated data quality evaluation is not specified.** Section 4.2 describes an automated quality evaluation requiring scores ≥ 0.85 across three dimensions but does not state which LLM performs this evaluation. Since this filtering step shapes the entire dataset, the model identity matters for reproducibility.

- **Decoding parameters (temperature, top-p) are not reported.** The paper specifies k=5 sampling iterations but does not state temperature, top-p, or other decoding parameters. These are needed for reproducibility, especially for the D@k and stability metrics that depend on sampling variability.

- **No confidence intervals or significance tests for model comparisons.** Comparisons between model families (open vs. closed, MoE vs. dense) are discussed as meaningful differences, but no error bars, confidence intervals, or statistical tests are provided.

### Trivial

- The theoretical framework in Section 3.1 (stress-appraisal research, cognitive control) is interesting but not mechanistically tested — the paper does not engage with or test the hypotheses introduced there. This does not harm the benchmark's utility but makes the section feel decorative rather than functional.

## Nice-to-Haves

- A control experiment where the pressure prompt explicitly tells the model *not* to deceive — if behavioral divergence persists, it would strengthen the case that the method measures deception rather than just pressure sensitivity.
- Providing the full GPT-4.1 judge prompt and scoring rubric in the main text (or a detailed summary) would greatly improve transparency.
- The safety fine-tuning experiment (Section 5.4) is described as "a limited case study involving two models from the same family and a single training run" — the paper's conclusions about safety fine-tuning's limitations should be softened further or this section should be moved to an appendix.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

1. **"The paper provides no evidence that the observed behavioral shifts are driven by strategic intent"** — REMOVED. The paper does provide evidence: the CoT analysis in Figure 1 explicitly shows the model reasoning about capability concealment and deceptive framing. The construct validity concern is real (and kept above), but stating there is "no evidence" is factually inaccurate.

2. **"No details on the judge prompt or scoring rubric"** — REMOVED. The paper states these are in Appendix C.2 and D, which are stripped from the extracted text. Criticizing content known to be in stripped appendices violates the review guidelines.

3. **"No analysis of the judge's own potential biases or failure modes"** — REMOVED. This is a speculative ask, not a concrete missing element. The paper's omission is the absence of validation metrics (kept above), not a failure-mode analysis that is standard to expect.

4. **"The judge selection process is not described in the main text"** — REMOVED. The paper says "detailed model comparison in Appendix C.1," which is stripped. The existence of this comparison in the appendix means it cannot be faulted as absent.

5. **Criticism that Section 3.1's theoretical framing is "asserted rather than argued"** — REMOVED. Benchmark papers routinely use theory to motivate design choices without mechanistically testing those theories. This is a scope-appropriate framing choice, not a weakness.

## Novel Insights

The input review correctly identifies the central tension in the paper: the gap between claiming to detect "deception" (which implies intent, as the paper itself defines it) and demonstrating behavioral divergence under pressure. However, it underweights the paper's CoT-based analysis as a partial bridge across this gap. The more novel observation is that the four-quadrant classification system remains valuable regardless of how one resolves the philosophical question of LLM intentionality — it reliably distinguishes cases where models change both their reasoning and behavior (Q1) from cases where behavior changes but reasoning doesn't (Q2), from cases where reasoning changes but behavior doesn't (Q3). This taxonomy is useful for diagnosing alignment brittleness even under a deflationary interpretation that avoids the term "deception." The data error in Figure 6 is a concrete artifact that should be corrected but does not threaten the overall empirical picture.

## Suggestions

1. **Most important:** Provide quantitative validation of the GPT-4.1 judge against human annotations in the main text — precision, recall, F1 by quadrant and deception type. Without this, all reported deception rates float on an unvalidated proxy.

2. **Reframe the paper's central claims.** The benchmark's strength is its four-quadrant classification of behavioral alignment brittleness under pressure. A more defensible framing would position the contribution as "a framework for diagnosing alignment vulnerabilities" rather than "a benchmark for detecting deception." The empirical results would be equally (if not more) compelling under this framing, and it would sidestep the construct validity debate.

3. **Fix the Figure 6 data error** and either strengthen the safety fine-tuning experiment (with more models/runs) or clearly relegate it to preliminary observations in an appendix.

4. **Report decoding parameters** (temperature, top-p) and include confidence intervals or error bars for key comparisons.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>