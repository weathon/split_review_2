## Summary

This paper introduces In-Context Watermarking (ICW), a novel approach to LLM text watermarking that embeds detectable signals through prompt engineering alone, without modifying the decoding process. The authors propose four ICW strategies (Unicode, Initials, Lexical, Acrostics) at different linguistic granularities, each with tailored detection methods. They evaluate these methods in a Direct Text Stamp (DTS) setting and an Indirect Prompt Injection (IPI) setting motivated by detecting LLM-generated peer reviews. Results on GPT-o3-mini show strong detection (ROC-AUC > 0.99 across methods), good robustness to paraphrasing and editing, and high text quality.

## Strengths

- **A genuinely novel framing of the watermarking problem (Sections 1, 3).** The core idea — embedding watermarks through instruction-following rather than decoding modification — addresses a real gap: existing methods require model access that third parties (conference organizers, API users without logit access) do not have. The direction is timely and the motivation is solid.

- **Well-structured taxonomy of four ICW strategies with clear trade-off analysis (Section 4, Table 1).** The four methods (Unicode, Initials, Lexical, Acrostics) span distinct levels of linguistic granularity and naturally expose different trade-offs among LLM requirements, detectability, robustness, and text quality. The analysis of *why* each method demands different capabilities (e.g., Lexical ICW requiring long-context retrieval, Acrostics requiring sentence-level instruction-following) is thoughtful and helps the reader understand applicability conditions.

- **Strong detection results on a capable model (Table 2).** With GPT-o3-mini, all four ICW methods achieve ROC-AUC > 0.99 across both DTS and IPI settings, and Acrostics ICW achieves perfect 1.000 AUC in DTS. This convincingly demonstrates that the core idea works when the LLM is sufficiently capable.

- **The IPI scenario is creative and practically motivated (Section 3.2, Figure 2).** Using watermarking instructions covertly embedded in documents to detect downstream LLM misuse — without the LLM provider's cooperation — is a genuinely useful application. The peer-review case study grounds the contribution in a concrete real-world scenario.

## Weaknesses

### Major

- **The IPI experiments test instruction-following in long documents, not covert embedding.** The paper's most distinctive applied contribution is the IPI setting, where watermarking instructions are *covertly* hidden in documents (e.g., as white text or zero-font text). However, the experiments (Section 5.1) simply concatenate the instruction to the paper text — the implementation is described as "each complete paper is provided as input for review" with no mention of how the instruction is hidden or whether it survives PDF-to-text extraction. The formal definition in Eq. (2) uses concatenation ($\tilde{t} = t \oplus \text{Instruction}$). The experiments therefore test whether an LLM follows a *visible* instruction appended to a document, not whether a *covertly hidden and extracted* instruction works. The viability of the IPI scenario depends on three steps: (a) the instruction survives extraction when hidden (white text is often stripped by PDF parsers; zero-width Unicode may be stripped), (b) the LLM treats the extracted instruction as a command, and (c) the reviewer does not notice and remove it. The paper tests only step (b), with the instruction in plain sight. The paper acknowledges this limitation (line 101: "detailed investigation of attack and defense methods is left for future work"), but the applied claim is weakened by the gap. This is a fixable but significant limitation for a paper that prominently features the IPI case study.

### Minor

- **"Model-agnostic" framing is inconsistent with the paper's own results.** The abstract (line 9) describes ICW as "model-agnostic," but Table 2 shows that with GPT-4o-mini, Initials ICW achieves ROC-AUC of only 0.572 and Acrostics ICW only 0.590. The paper itself acknowledges (Section 5.2.1) that effectiveness "highly depends on the capabilities of the underlying LLMs" and that GPT-4o-mini "fails to consistently follow the watermarking instructions." In context, "model-agnostic" likely means "does not require access to model internals" — the paper's main selling point — but the phrasing is ambiguous and the results contradict the literal reading. The paper would benefit from a more precise characterization such as "does not require access to the decoding process."

- **Evaluation uses only two models from a single provider (OpenAI).** The entire experimental evaluation rests on GPT-4o-mini and GPT-o3-mini. The paper's argument that ICW scales with LLM capability would be substantially strengthened by testing at least one non-OpenAI model (e.g., Claude, Gemini, or an open-weight model like Llama). Different models handle long-context instructions, tokenization, and embedded instructions differently, and without broader testing the generalization claim is speculative.

- **The attack/defense analysis in the IPI setting is minimal.** The paper tests two attacks (is the ICW instruction identifiable/removable? does prepending "ignore prior prompts" work?), both acknowledged in Appendix D.1. A moderately sophisticated dishonest reviewer could strip formatting, run the PDF through a plain-text extractor (removing white-text instructions), or simply describe the paper from memory. The paper explicitly scopes this as future work, but the practical deployment claims are commensurately limited.

### Trivial

- The Acrostics ICW detection uses resampling of sentence-initial-letter sequences *from the suspect text itself* to estimate the null distribution (Section 4.2.4). The paper does not explicitly justify why this yields a valid null when the suspect text may be watermarked. (Permuting the sentences breaks the key-ordered sequence, which likely makes it valid, but the reasoning should be stated.)

## Nice-to-Haves

- **Validate the IPI pipeline end-to-end.** The single most impactful experiment would be: take a real PDF, embed a watermarking instruction as white text (or zero-font), convert to text using a standard PDF-to-text tool, feed the extracted text to an LLM, and measure detection. If this works, the IPI claim is validated end-to-end. If not, the paper should be transparent about the practical gap.

- **Test at least one non-OpenAI model** (e.g., Claude, Gemini, or Llama 3.1 70B) to support the claim that ICW depends on *general* instruction-following capability rather than GPT-specific behavior.

- **Include an ablation on green-list size for Lexical ICW.** The paper notes that retrieval accuracy drops as context grows (Section 4.2.3) but does not vary vocabulary size experimentally; this would help practitioners understand the detectability-quality trade-off.

- **Report empirical false positive rate calibration** for Initials and Lexical ICWs — do the empirical FPRs match the theoretical z-statistic expectations?

## Removed Points

- *"The 'attack' analysis in IPI is incomplete in a way that affects the paper's conclusions" (from Issue 4):* Retained as Minor, but the claim that only one attack is tested is corrected — the paper tests two attacks per Appendix D.1. The broader point about limited defense testing stands but is already scoped as future work.

- *Criticisms about missing appendix content (e.g., "full proofs in appendix," "implementation details"):* Removed per rules — the parser strips appendix sections from all papers; they exist in the original submission.

## Novel Insights

None beyond the paper's own contributions. The reviews did not surface a novel interpretation or connection that the authors themselves missed.

## Suggestions

1. **Reframe the abstract and introduction** to drop "model-agnostic" and instead say "does not require access to the LLM's decoding process," which is the paper's actual advantage.
2. **Add an end-to-end IPI validation experiment** with realistic covert embedding (white text in PDF, PDF-to-text extraction, then LLM query). If this succeeds, it closes the main evidential gap.
3. **Expand model diversity** — even a single additional model from a different provider would significantly strengthen generalizability claims.
4. **For the Acrostics detection method**, add a one-sentence justification of why resampling from the suspect text yields a valid null distribution.

## Score and Decision

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>