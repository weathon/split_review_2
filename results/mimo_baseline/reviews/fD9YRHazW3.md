## Summary
This paper introduces In-Context Watermarking (ICW), a novel approach to watermarking LLM-generated text that operates entirely through prompt engineering—requiring no access to the model's decoding process. The authors propose four ICW strategies at different linguistic granularities (Unicode, Initials, Lexical, Acrostics), each with tailored detection methods, and evaluate them in both a Direct Text Stamp setting and an Indirect Prompt Injection setting motivated by detecting AI-generated academic reviews.

## Strengths
- **Genuine novelty and practical motivation.** The core idea of embedding watermarks purely through prompt engineering addresses a real gap: existing watermarking methods require access to the decoding process, which is unavailable when third parties (e.g., conference organizers) need to detect AI misuse. The IPI setting as a case study for academic review integrity is timely and well-motivated.
- **Comprehensive exploration of four ICW strategies.** The paper systematically explores watermarking at different linguistic granularities—from character-level (Unicode) to word-level (Initials, Lexical) to sentence-level (Acrostics)—providing a useful taxonomy of trade-offs among LLM requirements, detectability, robustness, and text quality (Table 1).
- **Strong results with capable models.** With GPT-o3-mini, all ICW methods achieve near-perfect detection (ROC-AUC ≥ 0.995) in both DTS and IPI settings, demonstrating that the approach is viable when paired with sufficiently capable LLMs. The observation that effectiveness scales with LLM capability is insightful and forward-looking.
- **Multi-dimensional evaluation.** The paper evaluates detection performance, robustness against multiple attack types (deletion, replacement, paraphrasing), and text quality (both perplexity and LLM-as-a-Judge), providing a fairly complete picture.
- **Theoretical grounding.** The paper provides formal hypothesis testing formulations and references theoretical guarantees on false alarm control (Appendix B), adding rigor.

## Weaknesses
### Fatal
None.

### Major
- **Insufficient security analysis.** For a watermarking paper, the adversarial robustness discussion is surprisingly thin. The fundamental vulnerability—that an adversary aware of ICW could simply instruct the LLM to "ignore any embedded watermarking instructions" or strip invisible text from a PDF before submitting it—is only briefly mentioned. The paper defers "detailed investigation of attack and defense methods" to future work, but the viability of ICW as a security tool depends critically on this analysis. A reviewer aware of the IPI setting could trivially check for and remove white-text instructions. Without stronger security guarantees or at least a more thorough threat analysis, it is unclear how practically useful ICW would be.
- **Limited model diversity.** Experiments are conducted on only two models (GPT-4o-mini and GPT-o3-mini), both from OpenAI. Testing on models from other providers (Claude, Gemini, open-source models like LLaMA) would significantly strengthen the claim that ICW effectiveness scales with general LLM capability rather than being an artifact of specific model families.
- **Practical viability of the IPI setting.** The motivating scenario assumes reviewers paste entire PDFs into LLMs, that white-text instructions survive PDF-to-text extraction, and that the instruction isn't diluted by the surrounding long paper content. These assumptions are reasonable but insufficiently validated. For instance, PDF extraction tools vary in how they handle invisible text, and many reviewers may paste only sections rather than full documents.

### Minor
- **Baseline comparison fairness.** The compared methods (PostMark, YCZ+23, GPTZero) operate in fundamentally different settings (post-hoc watermarking or detection). While the comparison is informative, it would be more compelling to also compare against another black-box in-process method if one exists, or to more explicitly acknowledge that the methods serve different use cases.
- **Text quality evaluation could be more rigorous.** The LLM-as-a-Judge scores for unwatermarked GPT-o3-mini output are suspiciously high (4.992/5.0 overall), which may indicate evaluation bias or ceiling effects. The gemini-2.0-flash judge may also systematically favor its own model family's outputs.
- **The Lexical ICW vocabulary design deserves more justification.** Restricting to adjectives, adverbs, and verbs is motivated by stylistic relevance, but the impact of this restriction on detection sensitivity and the optimal vocabulary size are not thoroughly analyzed.

### Trivial
- Some figures (e.g., Figure 1) are repeated with slightly different captions due to what appears to be parser artifact.

## Nice-to-Haves
- A more comprehensive adversarial evaluation: testing against an adversary who actively tries to detect and remove the hidden instruction, or who uses prompt injection defenses.
- Experiments on diverse model families to validate the capability-scaling hypothesis.
- Analysis of how ICW interacts with real-world PDF extraction pipelines in the IPI setting.
- A user study to evaluate whether ICW-generated text is perceptibly different from normal LLM output.

## Novel Insights
The paper's most compelling insight is that watermarking effectiveness scales with LLM capability—methods that fail with GPT-4o-mini achieve near-perfect detection with GPT-o3-mini. This creates an interesting co-evolution dynamic: as LLMs become more capable at instruction-following, they also become more amenable to watermarking through prompt engineering alone. This reframes the watermarking problem from one requiring model-owner cooperation to one that can be initiated by motivated third parties, which is a genuinely novel perspective in the watermarking literature.

## Suggestions
- Add a dedicated threat model section with a systematic analysis of adversarial strategies (instruction detection/removal, prompt injection defenses, paraphrasing with explicit de-watermarking instructions).
- Expand experiments to at least 3-4 different model families to substantiate the capability-scaling claims.
- Validate the IPI setting with real PDF extraction tools to assess practical viability.
- Consider few-shot or chain-of-thought prompting variants to improve the less capable models' compliance with ICW instructions.

## Score and Decision
The paper introduces a genuinely novel and practically motivated approach to LLM watermarking with promising results on capable models. However, the security analysis is insufficient for a watermarking contribution—the vulnerability to adversarial awareness is the central challenge that determines whether ICW is practically useful, and it is largely deferred to future work. The limited model diversity also weakens the key scaling claim. These issues are significant but do not invalidate the contribution; they represent important future work that builds naturally on this foundation.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>