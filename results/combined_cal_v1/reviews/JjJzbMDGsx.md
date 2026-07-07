Now I have all the information I need. Let me write the final consolidated review.

## Summary

This paper introduces the Language Confusion Gate (LCG), a lightweight plug-in intervention that reduces language confusion in multilingual LLMs during decoding. LCG uses norm-adjusted self-distillation to train a small MLP that predicts permissible language families at each generation step and masks inappropriate tokens. The method is motivated by a mechanistic analysis showing that token embedding norms are biased toward high-resource languages, and that correct-language tokens are typically present in the top-k predictions at confusion points. Evaluated across four model architectures (Qwen3, Llama3.1, Gemma3, GPT-OSS) on FLORES and INCLUDE benchmarks, LCG reduces confusion by 2-45× while preserving task performance and adding only 0.4% inference overhead.

## Strengths

- **Mechanistic insight linking token embedding norms to language confusion (Section 3.2).** The decomposition of logits into norm × cosine similarity and the demonstration that high-resource languages dominate the top 5% of token embedding norms (Table 1) is a novel, measurable finding that directly motivates the method. This is not simply a rerun of known results — it identifies a concrete, exploitable bias.

- **Elegant solution design that follows from the analysis.** The three observations in Section 3.1 (confusion is rare, correct tokens are in top-k, norm bias inflates high-resource tokens) directly motivate each design choice: sparsity justifies a targeted gate; top-k presence justifies self-distillation from debiased logits; norm bias justifies norm-adjustment during training. The method is a coherent pipeline from analysis to intervention, not a bag of tricks.

- **Dramatic and consistent confusion reduction with preserved task performance across multiple architectures.** Across four model architectures with varied sizes (Table 3), CJ confusion drops substantially (e.g., Qwen3-8B: 4.5%→0.1%; Llama3.1-8B: 3.0%→0.4%) and Latin confusion drops meaningfully (e.g., 12.1%→2.0%), while BLEU and accuracy remain flat. The effect also holds on thinking/reasoning models (Table 4). These results are consistent and hard to explain away as artifacts.

- **Principled handling of the code-switching dilemma.** The FLORES-WITH-LATIN / FLORES-NO-LATIN split cleanly separates evaluation of confusion from evaluation of legitimate code-switching. The 86.7% token-level preservation rate on human-validated code-switch examples (Section 5.3) provides direct evidence that the gate does not blindly suppress all language mixing.

- **Practicality.** The 0.4% overhead in generation time (15.95ms → 15.99ms per step) and the 0.3–0.4% intervention rate make this deployable in production. The plug-in design (no base model modification, no retraining) is a genuine advantage over retraining-based approaches.

## Weaknesses

### Fatal
None.

### Major

1. **Response-level confusion metric mismatches the token-level analysis.** The paper defines confusion rate as "the percentage of model responses that contain at least one character from an unintended language script" (Section 5.2) — a response-level binary indicator. A single confused token in a 500-token response counts the same as one where 50% of tokens are confused. This is a mismatch with the token-level probability analysis in Section 3.1 that motivates the method. The paper already collects token counts (e.g., "523 among 139354 tokens" for Qwen3-8B), so reporting token-level confusion rates alongside response-level rates would be straightforward and would directly connect the evaluation to the mechanistic analysis. This is especially important for the repeated "order of magnitude" claim.

2. **The code-switching preservation claim is partially overstated.** (a) The human-validated preservation experiment (86.7%) uses only one model (Qwen3-8B) on selected outputs, with no reported inter-annotator agreement. (b) In the aggregate evaluation (Table 5), LCG pushes code-switch rates below ground-truth levels for some models (Qwen3-8B: 25.90% vs. 38.36% ground truth; Llama3.1-8B: 31.60% vs. 38.36%). The paper acknowledges this but defends by comparison to Claude Sonnet 4's rate (23.29%), which is not a normative target. The ground-truth rate is the more meaningful reference, and LCG falls roughly a third below it. The claim that LCG "preserves" code-switching ability would be strengthened by reporting per-model ratios of post-LCG Latin usage to ground-truth usage and discussing the contexts where over-suppression occurs.

### Minor

3. **Latin confusion on INCLUDE is not reported.** Table 3 reports only CJ confusion and accuracy for the INCLUDE benchmark, even though INCLUDE covers Arabic, Hebrew, Greek, Russian, and Vietnamese — all non-Latin-script languages where Latin characters would signal confusion. Reporting Latin confusion on INCLUDE would complete the picture of whether LCG preserves task performance across all metrics.

4. **No confidence intervals or statistical significance for main results.** Confusion rates are reported as point estimates (e.g., 4.5%→0.1%). For a low-rate phenomenon like CJ confusion, small absolute differences can be unstable. The paper should bootstrap confidence intervals or at minimum report raw counts underlying each percentage.

5. **The "order of magnitude" claim varies substantially by confusion type.** The blanket phrase applies cleanly to CJ confusion (e.g., 45× reduction for Qwen3-8B) but less so to Latin confusion, where reductions range from 2.9× (Llama3.1-8B) to 11× (Qwen3-30B). The paper acknowledges the script-level granularity limitation (Section 6) but should be more precise in its claims about the magnitude of reduction per confusion type.

6. **Sampling parameters for thinking model baselines are unspecified.** Table 4 reports "No LCG" CJ% and Pass@1/Pass@10 for thinking models without specifying greedy vs. temperature sampling. Since sampling strategy can affect confusion rates, this should be stated.

### Trivial
None.

## Nice-to-Haves

- Perform an ablation of the gate's MLP hidden dimension to inform practitioners about the capacity-overhead trade-off.
- Provide an error analysis of the residual confusion cases that LCG does not catch — are these gate prediction errors, or cases where the gate correctly allows a language but confused tokens are still sampled?
- Report Latin confusion on INCLUDE (already listed as Minor weakness 3, but worth emphasizing as a high-value addition).

## Removed Points

These points from the harsh critic review are removed with justification:

- **ORPO implementation details deferred to appendix**: REMOVED (per rules: reviewer concerns about missing appendix content are not valid since the appendix is stripped by the parser; the information exists in the original submission).
- **"GPT-OSS" not being a widely known model name**: REMOVED (per rules: if the paper cites it, it exists; do not question cited entities).
- **Norm adjustment figure showing repeated "n" tokens as a parser artifact question**: REMOVED (different BPE tokens can decode to the same character; this is expected behavior).
- **Rule 3 (persistence) potentially propagating errors**: REMOVED (speculative concern; the paper's results show the combined approach works well in practice).
- **Request for ablation of gate MLP size**: MOVED to Nice-to-Haves.
- **Request for error analysis of residual confusion**: MOVED to Nice-to-Haves.

## Novel Insights

None beyond the paper's own contributions. The review surfaces two substantive concerns — the response-level vs. token-level metric mismatch and the code-switching over-suppression risk — but neither invalidates the core contribution. These are fixable with additional analysis and reporting, not fundamental errors.

## Suggestions

1. Add token-level confusion metrics (fraction of confused tokens per language family) to Table 3 alongside the response-level percentages.
2. Report Latin confusion on INCLUDE in Table 3.
3. Add bootstrapped confidence intervals or raw counts for all confusion rate measurements.
4. In the code-switching analysis, report the per-model ratio of post-LCG Latin usage to ground-truth usage, and discuss contexts where LCG over-suppresses.
5. Be more precise about the "order of magnitude" claim: state the reduction factor ranges separately for CJ (e.g., 15-45×) and Latin (e.g., 2.9-11×) confusion.
6. Report sampling parameters (temperature, top-k, top-p) for all baseline evaluations, including thinking models in Table 4.

## Score and Decision

**Calibration.** Round 1 bracketing used 6 queries spanning all score bands. The paper's strongest topical anchors are: SASA (self-detoxification, 6.00) — comparable in having a lightweight decoding intervention but with far weightier weaknesses (−9.92); TA-ITI (token-aware inference-time intervention, 6.00) — similar in having a principled intervention approach but with originality concerns (−8.42, −7.05); Mexa (multilingual evaluation, 5.40) — weaker experimental scope; Crosslingual Capabilities (5.67) — weaker contributions and more severe weaknesses. The narrow calibration (Round 2) added UnifyVocab (5.67), Knowledge in Multilingual LMs (6.00), Vulnerabilities Mitigation (5.80).

**Weighted-item comparison.** This paper's strengths carry strong positive weights (+4.30 to +5.46), comparable to SASA (+4.96) and TA-ITI (+5.34). Crucially, this paper's heaviest weakness (−2.14 for code-switching over-suppression) is far milder than the heaviest weaknesses of SASA (−9.92), Mexa (−11.13), TA-ITI (−8.42), or Crosslingual Capabilities (−10.69). No item in this paper's review reaches even −3.0, meaning the review model considers all weaknesses relatively mild. The paper's "bag of tricks" risk is low — the method follows tightly from the analysis — and no fatal flaw is present.

**Final placement.** The paper is clearly above the 5.5–6.0 band (stronger than SASA, TA-ITI, Mexa in terms of weakness severity) but has two verified major concerns (metric mismatch, code-switching over-suppression) that prevent it from reaching the 7.5+ band. It sits at 6.5: a solid paper with a well-motivated method and strong empirical results, where identified weaknesses are addressable with additional analysis rather than structural.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>