Now I have all the data I need. Let me produce the final consolidated review.

## Summary

This paper introduces In-Context Watermarking (ICW), a method for embedding watermarks into LLM-generated text solely through prompt engineering, without access to model internals (weights, logits, or decoding process). The authors propose four strategies spanning different granularity levels — Unicode, Initials, Lexical, and Acrostics — and evaluate them in two settings: Direct Text Stamp (DTS, where the user controls the system prompt) and Indirect Prompt Injection (IPI, where instructions are covertly embedded in documents). On capable LLMs (GPT-o3-mini), three of the four methods achieve near-perfect detection, and the paper provides an honest discussion of model-dependence and trade-offs.

## Strengths

- **Novel framing and problem formulation.** The DTS setting — watermarking through prompt engineering alone, without model access — is a genuinely underexplored problem that existing in-process and post-hoc methods do not address. Section 3.1 formulates this clearly.
- **Systematic exploration of the design space.** The four ICW strategies span character-level (Unicode), word-initial (Initials), vocabulary-level (Lexical), and sentence-level (Acrostics) watermarks. Table 1 and the accompanying discussion honestly enumerate trade-offs among LLM requirements, detectability, robustness, and text quality.
- **Strong empirical results on capable LLMs.** On GPT-o3-mini, three ICW methods achieve AUC ≥ 0.995 in both DTS and IPI (Table 2). Paraphrasing robustness (AUC ≥ 0.887 for Initials, Lexical, Acrostics) is competitive with post-hoc baselines (Figure 3).
- **Intellectual honesty.** The paper transparently reports that ICW methods fail on less capable models (GPT-4o-mini: Initials AUC = 0.572) and acknowledges that detailed IPI attack/defense analysis is future work (line 101).

## Weaknesses

### Major

- **Acrostics ICW detection is methodologically flawed.** The detector (Section 4.2.4, line 177) estimates the null distribution of Levenshtein distances by *resampling sentence-initial letters from the suspect text itself*. Under H₁ (watermarked text), the suspect text's initial letters are biased toward the secret key ζ; resampling from this biased multiset shifts the estimated null toward the alternative, making the test conservative (biasing the z-statistic downward). The paper correctly states (line 163) that theoretical FPR guarantees are only provided for Initials and Lexical ICWs, not Acrostics — but the detection procedure as described cannot provide proper statistical calibration. The strong reported AUC values (1.000 in DTS) are *not* inflated by this bias (the bias is in the conservative direction), so the core empirical finding stands, but the method lacks rigorous statistical foundations and needs to be fixed (e.g., by estimating the null from an external corpus).

- **The IPI case study is incompletely validated as a threat model.** The IPI experiments (Table 2) demonstrate that a capable LLM follows watermarking instructions embedded in a long document — a finding about long-context instruction following. However, the paper does not experimentally validate key practical requirements of the IPI threat model: (a) whether the hidden instruction survives realistic input methods (copy-pasting, PDF parsers that strip invisible text), (b) whether the instruction remains covert (e.g., white text is trivially exposed by selecting text in a PDF viewer), and (c) whether simple countermeasures like prepending "ignore all previous instructions" defeat the watermark. The paper flags these as future work (line 101), but the prominence of IPI in the contributions creates a gap between the claims and the validation.

### Minor

- **The LLM used for the paraphrasing robustness evaluation is not specified.** Section 5.1 mentions "paraphrasing it using an LLM" without disclosing which model or whether it was instructed to remove watermarks. Since the choice of paraphrasing model strongly affects attack difficulty, this omission limits reproducibility and interpretability.
- **No confidence intervals or variance estimates for main detection results (Table 2).** ROC-AUC is reported as a point estimate; without error bars (e.g., bootstrap intervals), it is difficult to assess whether observed differences between methods or settings are statistically meaningful.
- **IPI robustness results are deferred to the appendix (Table 6)** while only DTS robustness appears in the main text (Figure 3). Since IPI is presented as a headline contribution, robustness under the IPI setting should appear in the main body.
- **Table 1's circle notation is imprecise.** Filled/empty circles indicate relative levels of LLM requirements, detectability, etc., without numerical thresholds. Approximate numerical ranges or explicit descriptions would be more informative.
- **Model-access assumptions could be stated more explicitly.** The paper assumes API access with system-prompt control but no logit/logprob access — a realistic configuration — but does not clearly articulate why this boundary is the relevant one for ICW's applicability.

### Trivial

None.

## Nice-to-Haves

- An in-process watermarking baseline (e.g., Kirchenbauer et al.) run on an open-source model would provide an upper-bound calibration for the DTS results, though the paper's scope (black-box watermarking) does not require it.
- Replacing the imprecise circle notation in Table 1 with numerical ranges would improve clarity.

## Removed Points

These points were flagged by the source reviews but are excluded after verification:

1. **Missing in-process baseline (Kirchenbauer et al., Aaronson).** — Removed. The paper's scope is explicitly black-box (no logits/weights access). In-process methods require exactly this access. Comparing against them would conflate fundamentally different settings. The paper appropriately compares against black-box post-hoc baselines (PostMark, YCZ+23).
2. **No comparison to simple statistical baselines for Initials ICW.** — Removed. The paper already estimates the natural frequency γ from the Canterbury Corpus (Section 4.2.2), which serves as the proper null baseline. Random guessing would add no information.
3. **Full instructions deferred to appendix.** — Removed. Abbreviated instructions in the main text (Section 4.2) are sufficient for understanding each method. Full instructions in an appendix is standard practice.
4. **LLM-as-a-Judge bias toward LLM text.** — Removed. This is a known limitation of all LLM-as-a-judge evaluations and does not threaten the relative ranking of ICW methods vs. baselines.
5. **Abstract overstates gap by ignoring post-hoc methods.** — Removed. The paper's introduction (line 15) says "most existing watermarking methods require access to the decoding process," which is accurate for in-process methods. Post-hoc methods are discussed in Related Work and used as baselines.
6. **Criticism about Unicode ICW not persisting in printed formats.** — Removed. The paper explicitly notes this limitation (line 133).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Fix the Acrostics detection method.** Replace within-text resampling with a null distribution estimated from an external corpus (e.g., Canterbury Corpus, as done for Initials ICW's γ estimate). This would give the method a proper statistical foundation.
2. **Reframe the IPI contribution to match the validation.** Either add experiments addressing the covertness and adversarial-robustness requirements of the IPI threat model, or explicitly reframe it as a preliminary exploration / "discussion of potential future application" rather than a validated use case.
3. **Disclose the paraphrasing LLM.** Specify which model was used for the paraphrasing attack in robustness evaluation and whether it was instructed to remove watermarks.
4. **Add confidence intervals.** Report bootstrap confidence intervals or variance estimates for the ROC-AUC values in Table 2.
5. **Add IPI robustness to the main text.** Move IPI robustness results (Table 6 in the appendix) into the main body.

## Score and Decision

This paper identifies a genuinely novel and underexplored problem, provides a systematic exploration of four strategies, and reports strong empirical results on capable LLMs. The core DTS contribution is solid and the paper is transparent about its limitations. However, the Acrostics detection method is statistically unprincipled (though the bias is conservative, not inflationary), and the IPI case study is presented more prominently than its level of validation warrants. These issues are addressable in revision.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>