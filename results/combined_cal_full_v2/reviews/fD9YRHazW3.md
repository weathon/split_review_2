## Summary

This paper introduces In-Context Watermarking (ICW), a watermarking modality for LLMs that operates *solely through prompt engineering* — without modifying or even accessing the decoding process. The authors propose four strategies (Unicode, Initials, Lexical, Acrostics) at character, word, and sentence granularity, each with a tailored detection method. They evaluate these in two settings: Direct Text Stamp (DTS), where the watermark instruction is given as a system prompt, and Indirect Prompt Injection (IPI), where instructions are covertly embedded in documents (e.g., hidden in PDFs). With a sufficiently capable model (GPT-o3-mini), all four methods achieve ROC-AUC ≥ 0.995 in DTS and ≥ 0.997 in IPI, with text quality scores comparable to unwatermarked LLM output and superior to post-hoc baselines.

## Strengths

1. **A genuinely new watermarking modality.** The core idea — embedding detectable signals through prompt engineering alone, without any form of model access — is novel and clearly distinct from both in-process (decoding-modification) and post-hoc (text-editing) watermarking. This opens a design axis not explored in prior work. The paper convincingly demonstrates that the concept is feasible with capable models.

2. **Strong detection results with capable LLMs.** With GPT-o3-mini, all four ICW methods achieve ROC-AUC ≥ 0.995 in the DTS setting and ≥ 0.997 in IPI, with T@1%F at or near 1.0 for Unicode and Acrostics (Table 2). These results show that prompt-only watermarking can match the performance of methods that control decoding, provided the model is capable enough. Robustness to deletion, replacement, and paraphrasing attacks is also strong for Initials and Acrostics ICWs, often outperforming post-hoc baselines.

3. **Systematic strategy design across granularity levels.** The paper proposes four strategies (Unicode, Initials, Lexical, Acrostics) operating at character, word, and sentence levels, each paired with a tailored detection statistic. Table 1 honestly summarizes the trade-offs among LLM requirements, detectability, robustness, and text quality. This breadth makes the paper a useful starting point for future work on ICW and helps characterize which design dimensions matter.

## Weaknesses

### Fatal
None.

### Major

- **The "model-agnostic" claim in the abstract is contradicted by the paper's own evidence.** The paper tests only two models (GPT-4o-mini and GPT-o3-mini), both from a single provider (OpenAI), and finds that three of four ICW methods perform near-randomly on GPT-4o-mini (Initials ICW: ROC-AUC 0.572, Acrostics ICW: 0.590). The contribution list itself states that "the effectiveness of ICW is highly dependent on the capability of the underlying LLMs," which directly undermines the "model-agnostic" descriptor. Without testing on at least one non-OpenAI model (e.g., Claude, Gemini, or Llama-3), the paper cannot support claims of generality. The paper should either remove "model-agnostic" or qualify it precisely.

- **The IPI setting — the paper's headline application — is evaluated without testing the most obvious countermeasure.** The IPI scenario (catching reviewers who paste papers into LLMs) is the paper's primary real-world framing. The proposed embedding method uses hidden white text in PDFs. However, a reviewer who selects only visible text (standard PDF copy-paste or PDF-to-text conversion) would never ingest the hidden instruction. This attack is not tested or discussed beyond a one-sentence deferral to future work. While the paper tests "ignore prior prompts" as an adversarial prepend (mentioned in Section 5.2.3, results in appendix), the copy-only-visible-text gap means the practical viability of the paper's central motivating scenario is undemonstrated.

### Minor

- **The Acrostics ICW detection procedure is underspecified.** The detector estimates the null distribution by "randomly resampling N sequences of sentence initial letters from the suspect text" (Section 4.2.4) without describing how this resampling works — permutation, bootstrap, or sampling from an external reference corpus. If the resampling merely permutes the order of sentence-initial letters from the suspect text, it may be valid (since permutation breaks sequential alignment with the secret key), but the description is insufficient for reproducibility or statistical justification.

- **The evaluation is limited to models from a single provider (OpenAI).** While the paper acknowledges model-dependence in principle, testing only GPT-4o-mini and GPT-o3-mini leaves open the question of whether ICW generalizes to other model families (e.g., Anthropic, Google, Meta) that may have different instruction-following or formatting-resistance characteristics. This is particularly relevant because the paper's findings show dramatic performance differences even between two OpenAI models.

- **IPI robustness results (Table 6) and the "ignore prior prompts" attack results are deferred to the appendix.** Given that IPI is a central contribution and the robustness of the watermark under adversarial conditions is critical for any real deployment, these results would strengthen the main narrative.

### Trivial
None.

## Nice-to-Haves

- **Quantify the gap relative to in-process watermarking.** The paper compares ICW against post-hoc methods (same access assumption), which is the correct comparison. However, a brief quantification of how many more tokens ICW needs to match the power of in-process methods (e.g., Kirchenbauer et al.) under otherwise identical conditions would help readers understand what ICW trades for its access advantage. This is not a required comparison for the paper's core claim but would strengthen it.

- **Statistical power vs. text length.** The paper fixes text at 300 words. An ablation showing how detection performance varies with text length would be practically useful (especially for the IPI setting where review lengths vary).

- **Move IPI robustness results and adversarial prompt results to the main text.** Given the centrality of the IPI scenario, including these results (or at least a summary figure) in the main paper would substantially strengthen the narrative.

## Removed Points

These points from the input review are flagged to be removed; treat them with caution:

1. **"Baseline comparison does not test ICW's claimed advantage"** — REMOVED. The paper's claim is enabling watermarking without model access. Comparing against post-hoc methods (same access assumption) is the correct comparison. In-process methods require different access, so a like-for-like comparison is not possible. This is scope creep.
2. **"LLM-as-a-Judge favors machine text"** — REMOVED. While Table 3 shows the LLM judge scores unwatermarked LLM text higher than human text, ICW methods are compared against baselines (PostMark, YCZ+23) in the same evaluation setup. Any bias affects all methods equally and does not undermine the paper's comparisons.
3. **"Post-hoc watermarking omitted from Introduction"** — REMOVED. This is a presentation choice; post-hoc methods are covered in Related Work. The Introduction's gap-framing (no decoding access) is accurate.
4. **"Circle notation imprecise"** — REMOVED. Trivial presentation nitpick.
5. **"Discussion of limitations thin"** — REMOVED. Section 6 discusses instruction improvement and model capability limitations. While not exhaustive, it is acceptable for an exploratory paper.
6. **"Statistical power vs. text length not discussed"** — REMOVED. The paper states in Section 5.2.3 that an ablation study on context/output length effects is conducted in Appendix D.1.

## Novel Insights

Beyond the paper's own contributions, the most interesting finding that emerges across the review is the sharp *cliff* in ICW performance between GPT-4o-mini and GPT-o3-mini. Three of four methods go from near-random to near-perfect detection with a single model upgrade. This suggests the existence of a threshold capability level — in instruction-following, long-context retrieval, or both — above which prompt-based watermarking abruptly becomes viable. Characterizing this threshold precisely (which capability dimensions matter, and at what level) would be a valuable research direction that the paper surfaces but does not itself pursue.

## Suggestions

1. Remove "model-agnostic" from the abstract and replace with a more precise descriptor (e.g., "feasible with sufficiently capable LLMs, and expected to improve as models advance").
2. Test the copy-only-visible-text attack in the IPI setting and report the results — even a negative finding is informative and would strengthen the paper's honesty about limitations.
3. Extend evaluation to at least one non-OpenAI model (e.g., Claude or Gemini) to support any generality claims.
4. Clarify the Acrostics ICW resampling procedure (line 177): specify whether it is a permutation of sentence-initial letters from the suspect text, a bootstrap, or sampling from a reference corpus.
5. Move the IPI robustness and adversarial-prompt results (currently in Appendix D.1) to the main text, or reduce the prominence of the IPI framing if space constraints prevent this.

## Score and Decision

**Calibration anchors used:**

| Path | Avg Score | Round | Itemized | Comparison to ICW paper |
|---|---|---|---|---|
| `jbfDg4DgAk.md` (Sparse Watermarking) | 3.00 | R1 | Yes | Lacks novelty vs. existing work; ICW has much higher novelty |
| `eKGEsFdpin.md` (I Know You Did Not Write That!) | 3.67 | R1 | Yes | Sampling watermark similar to Kirchenbauer; ICW more novel |
| `DEJIDCmWOz.md` (Reliability of Watermarks) | 6.00 | R1 | Yes | Robustness study of existing watermarks; different contribution type, similar quality |
| `E4LAVLXAHW.md` (Black-Box Detection) | 7.00 | R1 | Yes | Very well-executed analysis; ICW is less polished but has more novel method |
| `6p8lpe4MNf.md` (Semantic Invariant Robust Watermark) | 5.50 | R2 | Yes | Novel idea, accepted; similar quality to ICW, comparable strength weights |
| `FDfq0RRkuz.md` (WASA) | 5.50 | R2 | Yes | Unicode-based watermark with threat model concerns; ICW has more novel modality |
| `0KHW6yXdiZ.md` (End-to-End Logits) | 5.25 | R1/R2 | No | In-process watermarking; less novel than ICW |
| `r6aX67YhD9.md` (Learning to Watermark via RL) | 4.75 | R1 | No | In-process; different paradigm |
| `qGLzeD9GCX.md` (EditMark) | 4.25 | R1 | No | Model-editing watermark; less novel |
| `0SpkBUPjL3.md` (Unremovable Watermarks) | 3.75 | R1 | No | Open-source watermark; different setting |
| `LdIlnsePNt.md` (Semantic-aware Speculative Sampling) | 6.00 | R1 | No | Theoretical watermark analysis |
| `KRMSH1GxUK.md` (Watermarks for IP Infringement) | 5.80 | R1 | No | Application paper, different focus |
| `9k0krNzvlV.md` (Learnability of Watermarks) | 5.75 | R1 | No | Analysis paper |
| `ecbRyZZmKG.md` (Double-I Watermark) | 5.25 | R2 | No | Backdoor-based watermark |
| `hTUrBJqECJ.md` (Low-entropy Watermark) | 5.50 | R2 | No | Unbiased watermark analysis |

**Bracket justification:** Round 1 identified a plausible range of 5.5–6.5 based on the gap between papers at 3.0–3.67 (which lacked novelty) and those at 6.0–7.0 (thoroughly executed). Round 2 narrowed the comparison to 5.5-level watermarking anchors (Semantic Invariant, WASA). ICW's highest strength weight (11.05 for strong results with capable models) exceeds most anchors' best strengths, but its most damaging weakness weight (0.90 for the model-agnostic contradiction) is more damaging than the worst weaknesses of the 5.5 anchors. The paper's genuine novelty and strong empirical results (with capable models) place it above 5.5, but the claim-evaluation mismatch and IPI gap prevent it from reaching 6.5 or above.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>