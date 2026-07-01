## Summary

This paper proposes In-Context Watermarking (ICW), a family of watermarking techniques for LLMs that operates purely through prompt engineering — requiring no access to model weights, logits, or sampling processes. It introduces four strategies at different granularity levels (Unicode, Initials, Lexical, Acrostics), evaluates them in a Direct Text Stamp (DTS) setting and an Indirect Prompt Injection (IPI) case study motivated by AI misuse in peer review, and demonstrates near-perfect detection (AUC > 0.99) with GPT-o3-mini while showing that effectiveness depends critically on the model's instruction-following capability.

---

## Strengths

1. **Genuinely novel problem framing.** The core insight — that instruction-following LLMs can be prompted to produce output with detectable statistical patterns, enabling black-box watermarking — is clean, non-obvious, and well-motivated. ICW fills a position in the design space that no prior work occupies: watermarking without any decoding-process access.

2. **Systematic coverage of the granularity dimension.** The four strategies span character-level (Unicode), word-initial-letter-level (Initials), word-level (Lexical), and sentence-level (Acrostics). This is principled, and the paper is honest about which levels require stronger models.

3. **Honest reporting of the model-capability dependency.** The contrast between GPT-4o-mini (Initials and Acrostics AUC ~0.57–0.59, essentially random) and GPT-o3-mini (all four methods AUC > 0.99) is striking and transparently reported. A weaker paper would cherry-pick only the best results; this paper foregrounds the dependency as a finding.

4. **Strong results with the capable model.** With GPT-o3-mini, detection AUC is near-perfect across all four methods in both DTS and IPI settings. Robustness under paraphrasing is also competitive (AUC 0.887–0.924).

---

## Weaknesses

### Fatal
None.

### Major

1. **"Model-agnostic" claim not supported by evidence.** The abstract describes ICW as a "model-agnostic, practical watermarking approach." However, experiments test only two models (GPT-4o-mini and GPT-o3-mini), both from a single provider (OpenAI). With only two points on one provider's capability curve, the paper cannot substantiate claims of model agnosticism. Testing even one open-weight model (e.g., Llama-3-70B, DeepSeek-V3, Qwen-2.5-72B) would be necessary to characterize which specific capabilities (instruction-following? long-context retrieval?) are the binding constraint. This is the most significant gap in the empirical case.

2. **No variance or uncertainty reported for any experimental result.** All results in Table 2 and Figure 3 are single point estimates. There are no confidence intervals, error bars, or any indication of run-to-run variability. This is especially problematic for results near random chance (GPT-4o-mini: Initials AUC=0.572, Acrostics AUC=0.590) where the reader cannot assess whether these values are stable or dominated by noise. Reporting variance is standard practice for experimental evaluation at a top venue.

3. **IPI adversarial validation gap.** The paper's headline motivating application — detecting AI misuse in peer review — is inherently adversarial. A dishonest reviewer who is aware of ICW has incentives to evade it. The paper acknowledges this (line 101: "a detailed investigation of attack and defense methods is left for future work") and states that two attacks are investigated in the appendix. However, the central question — can ICW survive a reviewer who actively tries to evade detection? — remains unanswered in the main text. The gap between the motivating scenario (catching dishonest reviewers) and the evaluation (non-adversarial settings where the reviewer blindly submits the paper) is substantial. The paper would benefit from prominently reporting adversarial robustness results rather than deferring them.

### Minor

1. **Key exposure in the IPI setting.** In the IPI setting, the watermarking instruction (including the secret key: green letter set, green word list, or secret string) is physically embedded in the paper. Anyone who finds the hidden instruction learns the key, enabling spoofing. The paper partially acknowledges this for Initials ICW (line 148: "the green letter set can be easily inferred, making the method vulnerable to spoofing attacks"), but the concern applies broadly and is not addressed.

2. **Unicode ICW is a proof-of-concept, not a practical tool.** The paper honestly notes that Unicode ICW is "highly fragile to transformations like LLM paraphrasing" (line 133). This means one of the four methods collapses under a standard and realistic transformation, and carries no practical value beyond demonstrating the concept.

3. **Logistical challenge of detection under blind review.** For the IPI peer-review scenario, it is unclear how conference organizers could detect the watermark in submitted reviews without reading the papers (which would break double-blind review), since the detector needs the paper-specific secret key. This logistical issue is not discussed.

4. **Two of four methods are unusable with widely deployed models.** Initials and Acrostics ICW produce near-random detection with GPT-4o-mini (AUCs ~0.57–0.62). The paper's defense that better models will emerge is a forward-looking claim, not a current validation of these methods.

### Trivial
None.

---

## Nice-to-Haves

- A qualitative comparison with in-process watermarking methods (Kirchenbauer et al., Aaronson, Christ et al.) would help readers assess the trade-off between model-access requirements and detection performance, even if a controlled experiment is not possible given different operating conditions.
- Error analysis for GPT-4o-mini failures: when the LLM does not follow the instruction, what goes wrong? Partial compliance? Complete disregard?
- The "ignore prior prompts" attack results (currently in Appendix D.1) deserve a place in the main text given their relevance to the IPI scenario.

---

## Removed Points

These points are flagged to be removed; treat them with caution.

1. **Speculation about "ignore prior prompts" attack results in Appendix D.1.** The reviewer speculates whether this attack defeats ICW and argues the results should be in the main text. The appendix exists in the original submission but was stripped by the parser; speculating about its contents is not valid. *(Rule: missing-appendix speculation)*
2. **Baselines "not clearly beaten."** The reviewer claims the paper does not establish ICW is preferable in DTS, but the paper only claims performance "comparable to" baselines (line 222) and identifies IPI applicability as the differentiator. The paper does not claim DTS superiority, so this criticism is a strawman. *(Rule: strawman weakness)*
3. **Missing comparison with in-process watermarking.** Moved to Nice-to-Haves. The reviewer acknowledges a controlled experiment is impossible since the methods operate under fundamentally different conditions (black-box vs. decoding-access). *(Soft rule: scope creep)*
4. **Unicode ICW "trivially defeated."** The paper explicitly acknowledges this limitation (line 133: "highly fragile to transformations like LLM paraphrasing"). The reviewer's point restates what the paper already says. Retained only as Minor weakness 2 above but the severity is noted as already addressed. *(Rule: paper already addresses)*

---

## Novel Insights

None beyond the paper's own contributions.

---

## Suggestions

1. **Broaden model evaluation** to at least one open-weight model family (Llama, DeepSeek, Qwen) to substantiate the "model-agnostic" claim, or qualify/remove the term.
2. **Report variance** (confidence intervals or standard deviations across multiple runs) for all main experimental results.
3. **Address adversarial robustness of the IPI setting directly** — even mixed results would be more informative than deferring the analysis.
4. **Tone down "model-agnostic"** in the abstract, or qualify it with the current limited evidence (two models, one provider).

---

## Score and Decision

The paper introduces a genuinely novel idea — prompt-based black-box watermarking — and systematically explores the design space at four granularity levels. The DTS results with GPT-o3-mini are compelling and demonstrate that the approach works with sufficiently capable models. The paper's transparency about the model-capability dependency is commendable.

However, the experimental validation has significant gaps: only two models from one provider are tested (undermining the "model-agnostic" claim), no variance is reported for any result, and the headline IPI application is evaluated under non-adversarial conditions while the motivating scenario is inherently adversarial. These are addressable in a revision, and the core idea is strong enough to warrant the work.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>