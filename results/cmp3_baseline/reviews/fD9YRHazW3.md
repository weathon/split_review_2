## Summary

This paper introduces In-Context Watermarking (ICW), a novel approach to watermarking LLM-generated text that operates solely through prompt engineering, without requiring access to the model's decoding process. The authors propose four distinct watermarking strategies (Unicode, Initials, Lexical, and Acrostics) at different linguistic granularities, each paired with tailored detection methods, and evaluate them in both Direct Text Stamp (DTS) and Indirect Prompt Injection (IPI) settings. The work demonstrates that as LLMs become more capable, ICW offers a practical, model-agnostic alternative to traditional watermarking approaches, with promising results on GPT-o3-mini across detection accuracy, robustness, and text quality.

## Strengths

- **Novel and important problem framing**: The paper identifies a genuine gap in the watermarking literature—situations where third parties (e.g., conference organizers) need to watermark LLM outputs but lack access to the model's decoding process. The IPI setting for detecting AI-generated peer reviews is a timely and socially relevant application.

- **Comprehensive exploration of multiple strategies**: The four ICW methods (Unicode, Initials, Lexical, Acrostics) span different levels of linguistic granularity and provide a systematic investigation of the design space. The trade-off analysis in Table 1 is useful for understanding when each method is appropriate.

- **Strong empirical results with capable models**: The detection performance on GPT-o3-mini is impressive, with several methods achieving near-perfect ROC-AUC scores (0.995-1.000) in both DTS and IPI settings. The robustness results, particularly for Initials and Acrostics ICW under paraphrasing attacks, are compelling.

- **Theoretical grounding for false alarm control**: The paper provides formal guarantees for controlling false positive rates for Initials and Lexical ICW (Appendix B), which is important for practical deployment where false accusations could have serious consequences.

## Weaknesses

### Major

- **Limited practical feasibility of the IPI setting**: The paper's central motivating example—embedding invisible watermarking instructions in academic papers—faces significant practical hurdles. Modern PDF readers and LLM preprocessing pipelines often strip or ignore invisible text (zero-width characters, white-on-white text). The paper acknowledges this briefly but does not provide empirical evidence that the hidden instructions survive the PDF-to-text conversion process that reviewers would use. This is a critical gap for the paper's primary application scenario.

- **Incomplete comparison with relevant baselines**: The paper compares against PostMark and YCZ+23 (post-hoc methods) and GPTZero, but does not compare against in-process watermarking methods that could be adapted to the black-box setting through API-level access. More importantly, the paper does not compare against simple baselines like "ask the LLM to include a specific phrase" or "ask the LLM to use a specific structure" without the sophisticated detection machinery. This would help isolate whether the complexity of the proposed methods is warranted.

- **Limited investigation of adversarial robustness**: The paper only evaluates robustness against random deletion, synonym replacement, and paraphrasing. However, a motivated adversary aware of the watermarking scheme could employ more targeted attacks. For Initials ICW, the green letter set is trivially inferable from a few watermarked samples. For Lexical ICW, the green word list could be extracted. The paper acknowledges these vulnerabilities but does not evaluate them empirically. Given that the IPI setting involves adversarial reviewers who are actively trying to avoid detection, this is a significant limitation.

### Minor

- **Dependence on model capability**: The dramatic performance gap between GPT-4o-mini and GPT-o3-mini (e.g., Initials ICW AUC from 0.572 to 0.999) raises questions about the generalizability of the approach. The paper frames this as a feature ("as LLMs become more capable, ICW becomes more powerful"), but it also means the method is currently only viable with the most advanced (and expensive) models.

- **Text quality evaluation methodology**: The LLM-as-a-Judge evaluation uses Gemini-2.0-flash, which may have its own biases. The paper reports that ICW methods achieve "comparable" quality to unwatermarked text, but the unwatermarked GPT-o3-mini text scores near-perfect (4.98-5.00), while ICW methods show noticeable degradation in clarity (e.g., Initials ICW: 3.706 vs 4.994). The paper's claim of "comparable" quality is somewhat overstated.

- **Limited analysis of detection in the IPI setting**: The IPI results in Table 2 show strong performance for GPT-o3-mini, but the paper does not analyze how the length of the paper context affects detection. Longer contexts might dilute the watermarking instruction's effectiveness, and this is not investigated.

### Trivial

- The paper uses "gpt-o3-mini" and "gpt-4o-mini" inconsistently in tables (sometimes with backticks, sometimes without).

## Nice-to-Haves

- An ablation study on the length of the watermarking instruction and its position within the prompt would be valuable for practical deployment.
- A cost analysis comparing ICW (which requires additional tokens for instructions) against traditional watermarking methods would help practitioners understand the trade-offs.
- A user study evaluating whether human readers can detect the watermark (especially for Initials and Lexical ICW) would strengthen the "imperceptible" claim.

## Novel Insights

The paper's key insight is that watermarking can be achieved purely through prompt engineering by exploiting LLMs' instruction-following capabilities, without any modification to the model's internals. This reframes watermarking from a model-provider responsibility to a third-party capability, opening up applications where the entity wanting to watermark text has no control over the model. The finding that different linguistic levels (characters, words, sentences) can serve as watermark carriers, each with different robustness-quality trade-offs, provides a useful framework for future work. The demonstration that the effectiveness scales with model capability suggests that this approach will become increasingly viable as LLMs advance.

## Suggestions

- Provide empirical evidence that the hidden watermarking instructions in the IPI setting survive realistic PDF-to-text conversion pipelines (e.g., PyPDF2, pdfplumber, OCR). Without this, the primary application scenario remains unvalidated.
- Evaluate the vulnerability of each ICW method to an adversary who knows the scheme and can collect watermarked samples. For Initials ICW, show how many samples are needed to infer the green letter set. For Lexical ICW, evaluate detection after the adversary removes or replaces words from the green list.
- Include a baseline where the LLM is simply instructed to include a specific secret phrase, and compare detection performance against the proposed methods. This would help justify the complexity of the statistical detection approaches.

## Score and Decision

The paper addresses a novel and important problem with a creative approach, and the empirical results on capable models are strong. However, the practical feasibility of the primary motivating application (IPI for peer review) is not adequately validated, and the vulnerability to adversarial attacks is insufficiently explored. The paper represents a solid initial exploration but requires additional validation before the claims about practical applicability can be fully accepted.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>