## Summary
This paper proposes In-Context Watermarking (ICW), a method for watermarking LLM-generated text entirely through prompt engineering — without modifying the decoding process or accessing model internals. It explores four watermarking strategies (Unicode, Initials, Lexical, Acrostics) at different linguistic granularities, applied in a Direct Text Stamp (DTS) setting and an Indirect Prompt Injection (IPI) case study targeting AI-generated peer reviews. Experiments with GPT-o3-mini show near-perfect detection (AUC > 0.99) across all strategies, while GPT-4o-mini succeeds only on Unicode ICW.

## Strengths

1. **Novel problem framing.** ICW identifies a genuine gap in LLM watermarking: scenarios where the detector has no access to the model's internals or decoding process and can only influence the input prompt. The peer-review misuse case study (Section 3.2) grounds this in a concrete operational need, clearly differentiated from existing in-process and post-hoc methods.

2. **Systematic design space exploration.** The four ICW strategies span character-level (Unicode), word-initial (Initials), word-level (Lexical), and sentence-level (Acrostics) watermarking, with a clear qualitative comparison of their trade-offs (Table 1). The paper candidly discusses failure modes for each strategy.

3. **Strong empirical results with capable models.** With GPT-o3-mini, all four methods achieve ROC-AUC > 0.99 in both DTS and IPI settings (Table 2), and maintain high detection rates under paraphrasing attacks (Figure 3). These results demonstrate feasibility of the approach with sufficiently capable LLMs.

4. **Transparent about limitations.** The paper does not hide the fact that three of four methods fail on GPT-4o-mini (Table 2, AUCs of 0.57–0.62 for Initials and Acrostics). The discussion in Section 5.2 and Section 6 frames this as a direction that will improve as models advance, rather than overclaiming.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Unvalidated null distribution for Initials ICW detection.** For Initials ICW, γ (expected proportion of words starting with green letters under H0) is estimated from the Canterbury Corpus (Section 4.2.2). The paper provides no empirical validation that the distribution of initial letters in the evaluation datasets (ELI5 for DTS, ICLR papers for IPI) matches this corpus. If the true null distribution differs, the reported T@1%F and T@10%F values could be unreliable, since the z-statistic thresholds depend on correct γ. The paper references theoretical false-alarm guarantees (Appendix B), but these bounds are only as good as the null model they assume. An empirical calibration check against held-out human text from the evaluation domains would strengthen the FPR claims.

2. **No error bars or variance estimates.** All results in Table 2, Table 3, and Figure 3 are reported as point estimates with no confidence intervals, despite 500 samples per condition being sufficient to compute them. Without variance estimates, it is unclear whether gaps between methods (e.g., Lexical ICW AUC=0.910 vs. PostMark AUC=0.963 on GPT-4o-mini) are meaningful or within noise.

3. **Critical "ignore prior prompts" attack deferred to appendix.** The paper mentions investigating the "ignore prior prompts" countermeasure as an "Additional Main Result" in Appendix D.1 (line 286–287), but does not report results in the main body. Since this attack directly targets the instruction-following mechanism that ICW depends on — especially in the IPI setting — its success or failure is central to assessing the approach's practical viability. Relegating this to the appendix undercuts the main narrative.

4. **Unaddressed IPI deployment ambiguities.** The IPI setting (Section 3.2) faces practical challenges that the paper acknowledges as future work but does not scope concretely: (a) key management — if each paper receives a different secret key, how does the detector efficiently determine which key to check against which review? (b) behavioral ambiguity — if a reviewer uses an LLM to summarize or analyze the paper rather than generate a full review, the watermark would still be present, potentially flagging legitimate LLM use. The threat model as presented (Figure 2) implicitly treats any LLM use as dishonest, which oversimplifies real reviewer workflows.

### Trivial

5. **Table 1 is uninformative for three methods.** Initials, Lexical, and Acrostics ICW all show the same pattern (●●●●) across all four criteria, so the table cannot communicate any trade-offs among these methods. Only Unicode ICW (○●○●) differs.

## Nice-to-Haves
- **Ablate the role of the secret key.** An experiment comparing detection with a known green set (watermark scenario) versus a fixed/inferred green set would isolate whether the watermark key adds value beyond observable instruction-following behavior, clarifying the security properties of ICW.
- **Consider the "wrong model" scenario.** In the IPI setting, if the conference embeds instructions targeting GPT-o3-mini behavior but the reviewer uses Claude or Gemini, would the watermark still work? The instructions are natural language, so they may generalize, but this is untested.
- **Validate the null distribution empirically** (as discussed in Weakness 1) by computing γ from held-out human text in the actual evaluation domains.

## Removed Points
These points from the input review were removed with justification:

1. "Comparison against baselines is structurally uninformative" — REMOVED. The paper explicitly labels PostMark and YCZ+23 as post-processing methods and notes they are not applicable in IPI (Section 5.1, line 189). The comparison is presented for reference within the DTS setting, and line 222 distinguishes the paradigms. The critic ignores these caveats.

2. "Most relevant baseline (secret key ablation) is absent" — REMOVED. This is a nice-to-have ablation rather than a missing baseline. The paper's contribution is the ICW framework; the secret key is integral to the watermarking security model.

3. "Missing implementation details (size of V, V_G, γ for Lexical ICW)" — REMOVED. The paper states these details are in Appendix C (line 185). Per review guidelines, criticisms about content deferred to the appendix (stripped by parser) should not be held against the paper.

4. "Section 5.2.1 overstates 'comparable'" — REMOVED. The paper qualifies this with "When used with high-capability LLMs" (line 222), which is accurate — with GPT-o3-mini, ICW methods are indeed comparable.

5. "Unicode ICW and zero-width space stripping by LLM providers" — REMOVED. This is speculative without evidence. The paper already acknowledges Unicode ICW's fragility.

6. "H0 definition conflates human and LLM text" — REMOVED. This is standard formulation in watermarking. The hypothesis-testing framework treats both as "non-watermarked," which is correct.

7. "LLM-as-a-Judge bias in Table 3" — REMOVED. This is a community-wide known limitation, not a specific flaw. Within-method comparisons (ICW vs. baselines) remain informative.

8. "model-agnostic claim imprecision" — REMOVED. The term is standard in the field to mean "no model internals required," which is true. The paper separately and transparently discusses model capability dependence.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Add confidence intervals (bootstrap or standard error) to all ROC-AUC and T@FPR results.
2. Move the "ignore prior prompts" attack results from the appendix to the main body, or at minimum summarize them in Section 5.2.2.
3. Validate the null distribution for Initials ICW against held-out human text from ELI5 and the ICLR dataset, or switch to a data-driven null estimate.
4. Clarify the key management protocol for the IPI setting and acknowledge the "LLM as reading aid" ambiguity in the threat model discussion.

## Score and Decision

**Calibration Anchors Report:**

| Anchor | Avg Score | Round | Itemized | Comparison to ICW Paper |
|--------|-----------|-------|----------|------------------------|
| 5kMwiMnUip.md (NEMESIS jailbreaking) | 1.40 | R1 | No | Non-watermark paper, much weaker |
| 8QTpYC4smR.md (Survey of LLMs) | 1.00 | R1 | No | Survey paper, not comparable |
| jbfDg4DgAk.md (Sparse Watermarking) | 3.00 | R1 | Yes | New watermark method criticized for lacking novelty (-4,-4). ICW paper has greater novelty. |
| ecbRyZZmKG.md (Double-I Watermark) | 5.25 | R1 | Yes | Similar method paper, criticized for limited technical contribution (-4). ICW paper stronger. |
| KRMSH1GxUK.md (Watermarks for IP Infringement) | 5.80 | R2 | Yes | Strong empirical performance (+5) but limited domain coverage (-2). ICW paper has broader scope. |
| 9k0krNzvlV.md (Learnability of Watermarks) | 5.75 | R2 | Yes | Novel problem (+4,+4) but practical assumption concerns (-3). ICW paper similar profile. |
| DEJIDCmWOz.md (Reliability of Watermarks) | 6.00 | R1 | Yes | Comprehensive robustness study (+5). ICW paper has similar evaluation depth + method novelty. |
| E4LAVLXAHW.md (Black-Box Detection) | 7.00 | R1 | Yes | First practical study (+4,+3) with clean experimental design. ICW paper has comparable novelty but less experimental rigor. |

**Bracket:** Round 1 bracketing placed the ICW paper between 5.5 and 7.0. The weighted-item comparison shows it shares the "novel and important problem" strength with the 5.75–6.00 anchors (KRMSH1GxUK, 9k0krNzvlV, DEJIDCmWOz) while having greater methodological novelty than those anchors. It falls below the 7.00 anchor (E4LAVLXAHW) which had stronger experimental rigor. The presence of multiple addressable but real minor weaknesses (no error bars, unvalidated null, critical attack in appendix) prevents a higher score. The paper is a solid borderline accept — it introduces a genuinely new watermarking paradigm with clear feasibility evidence, but the experimental presentation needs tightening to be a clear accept.

MY FINAL SCORE: 6.0
MY FINAL DECISION: Accept