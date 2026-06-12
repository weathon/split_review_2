## Summary

This paper introduces In-Context Watermarking (ICW), a novel approach to embedding watermarks in LLM-generated text solely through prompt engineering, without requiring access to the model's decoding process. The authors propose four ICW strategies at different granularity levels (Unicode, Initials, Lexical, and Acrostics) and evaluate them in both Direct Text Stamp (DTS) and Indirect Prompt Injection (IPI) settings. The key finding is that ICW effectiveness scales with LLM capability, achieving strong detection performance with sufficiently powerful models like GPT-o3-mini, while offering a practical solution for scenarios where model access is unavailable.

## Strengths

- **Novel and practically motivated problem formulation**: The paper identifies a genuine gap in existing watermarking methods—the inability to watermark text when the LLM's decoding process is inaccessible—and addresses it through a creative prompt-engineering approach. The peer review misuse scenario is a compelling and timely motivation.

- **Comprehensive exploration of multiple strategies**: The four ICW methods (Unicode, Initials, Lexical, Acrostics) span different levels of linguistic granularity and provide a systematic investigation of the design space. The trade-off analysis across LLM requirements, detectability, robustness, and text quality is well-structured and informative.

- **Strong empirical results with capable models**: The detection performance with GPT-o3-mini is impressive, achieving near-perfect ROC-AUC scores across multiple methods in both DTS and IPI settings. The robustness results, particularly for Initials and Acrostics ICW under paraphrasing attacks, are competitive with or exceed existing post-hoc baselines.

- **Theoretical grounding for false alarm control**: The paper provides formal guarantees for controlling false positive rates in Initials and Lexical ICW, which is important for practical deployment where false accusations carry significant consequences.

## Weaknesses

### Major

- **Limited practical viability of the IPI setting**: The paper's central motivating example—embedding invisible watermarking instructions in academic manuscripts—faces significant practical challenges that are not adequately addressed. Reviewers who use LLMs for review generation are likely to copy-paste text selectively rather than input the entire PDF, or may use models that strip invisible text. The paper acknowledges but does not seriously evaluate the effectiveness of obfuscation methods (white text, zero-width characters) against common PDF extraction tools or reviewer workflows. Without demonstrating that the hidden instruction survives realistic document processing, the IPI application remains speculative.

- **Incomplete comparison with post-hoc detection methods**: The paper compares ICW against PostMark and YCZ+23 in the DTS setting but does not provide a direct comparison with post-hoc detection methods (e.g., GPTZero, DetectGPT) in the IPI setting, where these methods are the primary alternative. The claim that ICW is "well-suited for IPI" would be stronger if accompanied by evidence that post-hoc detectors fail in this scenario, rather than simply stating they are "not applicable."

- **Limited attack analysis**: The paper evaluates robustness against random deletion, replacement, and paraphrasing, but does not consider adaptive attacks where an adversary aware of the watermarking scheme attempts to remove it. For Initials and Lexical ICW, the green set can be inferred, enabling targeted removal. For Acrostics ICW, an adversary could simply restructure sentences. The paper mentions these vulnerabilities but does not quantify their impact, leaving the practical security of ICW unclear.

### Minor

- **Dependence on proprietary models**: The experiments rely exclusively on GPT-4o-mini and GPT-o3-mini, both proprietary. The paper's central claim that ICW effectiveness scales with LLM capability would be strengthened by evaluation on open-source models (e.g., Llama, Mistral) to demonstrate generalizability and enable reproducibility.

- **Text quality evaluation limitations**: The LLM-as-a-Judge evaluation uses Gemini-2.0-flash, which may have its own biases. The perplexity evaluation uses LLaMA-3.1-70B, but the paper does not report whether the perplexity differences between watermarked and unwatermarked text are statistically significant. The clarity scores for ICW methods (around 3.7-4.5) are notably lower than unwatermarked text (4.99), suggesting some quality degradation that deserves more discussion.

- **Limited exploration of instruction design**: The paper uses relatively simple watermarking instructions and acknowledges that advanced prompt engineering could improve performance. However, the experiments do not systematically explore instruction variations (e.g., few-shot examples, chain-of-thought, different phrasing) to understand sensitivity or optimize performance.

### Trivial

- The paper states that "major LLM providers do not publicly use watermarks" but does not cite a source for this claim.

## Nice-to-Haves

- Evaluation on open-source LLMs (e.g., Llama-3, Mistral) to demonstrate generalizability
- A study of how the hidden instruction survives different PDF extraction pipelines (e.g., PyPDF2, pdfplumber, Adobe Acrobat)
- Analysis of adaptive attacks where the adversary knows the watermarking scheme and attempts to remove it
- Systematic ablation of instruction design choices (e.g., position of instruction, use of few-shot examples, different phrasing)

## Novel Insights

The paper's core insight—that watermarking can be achieved purely through prompt engineering by leveraging LLMs' instruction-following capabilities—is genuinely novel and opens a new direction for content attribution. The finding that ICW effectiveness scales with model capability is particularly interesting, as it suggests a "virtuous cycle" where more capable models enable more reliable watermarking, which in turn supports safer deployment. The observation that different granularity levels (character, word, sentence) offer different trade-offs between detectability, robustness, and quality provides a useful framework for future research. The IPI setting, while practically challenging, introduces a creative threat model reversal where benign entities embed watermarking instructions to detect misuse, rather than attackers injecting malicious prompts.

## Suggestions

- Conduct a systematic evaluation of how the hidden instruction survives realistic PDF processing pipelines (e.g., text extraction, copy-paste, OCR) to validate the IPI setting's practical viability.
- Include open-source LLMs in the evaluation to demonstrate generalizability and enable community reproduction.
- Evaluate adaptive attacks where the adversary knows the watermarking scheme and attempts to remove it, quantifying the robustness of each ICW method under worst-case assumptions.
- Provide statistical significance tests for text quality comparisons (perplexity, LLM-as-a-Judge scores) to support claims of quality preservation.

## Score and Decision

The paper presents a novel and well-motivated approach to LLM watermarking that addresses a genuine gap in existing methods. The empirical results with capable models are strong, and the systematic exploration of four strategies provides useful insights. However, the practical viability of the central motivating application (IPI for peer review) is not convincingly demonstrated, and the security analysis against adaptive attacks is incomplete. The paper makes a meaningful contribution to the field but requires further validation of its practical applicability.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>