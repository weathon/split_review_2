## Summary

The paper introduces In-Context Watermarking (ICW), a novel approach to watermarking LLM-generated text that operates entirely through prompt engineering, without requiring access to the model's decoding process. It proposes four strategies at different linguistic granularities (Unicode, Initials, Lexical, Acrostics), each with a tailored detection method, and evaluates them in both a direct text stamp (DTS) setting and an indirect prompt injection (IPI) setting motivated by detecting AI misuse in peer review. Experiments on GPT-4o-mini and GPT-o3-mini demonstrate that ICW can achieve strong detection performance, especially with more capable models, while maintaining reasonable text quality and robustness.

## Strengths

- **Novel and timely research direction**: The paper introduces a genuinely new paradigm for LLM watermarking—embedding watermarks purely through prompt engineering, bypassing the need for decoder access. This addresses a practical limitation of existing methods and opens up watermarking to third parties who are not LLM providers.
- **Clear problem formulation and motivation**: The IPI setting for peer review misuse is a concrete, well-motivated application that resonates with the community. The paper carefully defines the threat model, entities, and goals.
- **Comprehensive exploration of strategies**: The four ICW strategies span multiple levels of language structure (character, word initial, word, sentence), with a clear discussion of trade-offs across LLM requirements, detectability, robustness, and text quality. The detection methods are tailored to each strategy.
- **Solid empirical evaluation**: Experiments cover both DTS and IPI settings, include robustness tests (word deletion, replacement, paraphrasing), and compare against relevant post-hoc baselines (PostMark, YCZ+23). The use of two LLMs with different capabilities effectively demonstrates the dependence on model strength.

## Weaknesses

### Major

1. **Unrealistic IPI threat model**: The core application (detecting dishonest reviewers) assumes that a reviewer will blindly input the entire PDF (including hidden white-text instructions) into an LLM. In practice, reviewers may copy-paste relevant sections, manually type, or use LLM-based tools that strip invisible content. The paper acknowledges this but leaves detailed analysis of realistic reviewer behavior and evasion strategies to future work. This significantly weakens the claimed practical impact.

2. **Heavy dependence on LLM capability**: The paper shows that Initials, Lexical, and Acrostics ICWs perform poorly on GPT-4o-mini (ROC-AUCs around 0.57–0.59 in DTS, many near random). Only Unicode ICW works well across models, but Unicode is fragile to paraphrasing. The paper's core claim that ICW "will become correspondingly more powerful" as LLMs advance is speculative and not supported by evidence across a broader range of models. Without demonstrating effectiveness on currently available open-source models (e.g., LLaMA-3, Mistral), the practical utility of most ICW strategies is limited.

3. **Lack of rigorous false positive control for Acrostics ICW**: The detection method for Acrostics ICW uses Levenshtein distance and resampling from the suspect text to estimate the null distribution. This is a heuristic with no theoretical guarantee; the paper does not analyze how well the resampling reflects the true null or provide a formal false positive rate bound. In contrast, the paper provides theoretical guarantees for Initials and Lexical ICWs. This inconsistency weakens the overall methodological soundness.

4. **Limited robustness evaluation**: The robustness attacks (random deletion/replacement of 30% of words, paraphrasing) are relatively mild. More aggressive attacks—such as full paraphrasing by a different LLM, summarization, translation, or deliberate attempts to remove the watermark by an informed adversary—are not evaluated. Given that the paper discusses adversarial scenarios, this gap is notable.

5. **Lexical ICW details are underspecified**: The size of the green word list and the vocabulary partition method are not provided. The paper mentions that LLMs struggle with large vocabularies, but no ablation on vocabulary size is performed. This makes it difficult to assess the scalability and sensitivity of Lexical ICW.

### Minor

- The paper uses only two proprietary LLMs (GPT-4o-mini, GPT-o3-mini). Results may not generalize to other models, and reliance on proprietary APIs limits reproducibility.
- The LLM-as-a-Judge evaluation uses Gemini-2.0-flash, but the paper does not discuss potential biases or calibration of this judge for watermark quality assessment.
- The paper states that "major LLM providers do not publicly use watermarks" – this is increasingly inaccurate (e.g., OpenAI has deployed text watermarking), though it does not affect the core contribution.
- The paper does not discuss computational overhead or latency of ICW versus existing methods, which is relevant for practical deployment.

## Nice-to-Haves

- Evaluate ICW on a broader set of models, including open-source LLMs with varying capabilities, to better understand the capability threshold.
- Provide a more realistic analysis of the IPI setting, including a user study or simulation of reviewer behavior (e.g., copy-pasting, using LLM-based assistants).
- For Acrostics ICW, develop a statistical test with provable false positive rate control (e.g., using a permutation test).
- Include robustness against stronger attacks (full paraphrasing, translation, adversarial removal of watermarks).
- Ablate the green list size for Lexical ICW and analyze its impact on detection and quality.

## Novel Insights

None beyond the paper's own contributions. The paper's key insight—that watermarking can be achieved through prompt engineering alone, leveraging instruction-following—is genuinely novel and shifts the watermarking paradigm from model-internal modifications to input-level control. The mapping of watermark granularity to LLM capability requirements is also a useful conceptual contribution.

## Suggestions

- For the IPI setting, consider a sensitivity analysis where the watermarking instruction is partially or fully removed by the reviewer (e.g., via PDF text extraction tools). This would strengthen the practical claims.
- Include results on at least one strong open-source model (e.g., Llama-3-70B) to demonstrate generalizability beyond proprietary APIs.
- Provide a statistical test for Acrostics ICW detection with theoretical false positive rate guarantees, or clearly state that it is currently a heuristic.
- Report the green list size and vocabulary partition method for Lexical ICW, and include an ablation varying the green list ratio.
- Add a discussion of the detectability of the watermark by an adversary: how easily can the presence of an ICW be inferred, and how can the adversary remove it?

## Score and Decision

The paper introduces a novel and important research direction for LLM watermarking, with a clear motivation and a well-structured exploration of multiple strategies. However, the major weaknesses—particularly the unrealistic IPI threat model, heavy dependence on model capability, and lack of rigorous false positive control for Acrostics ICW—substantially limit the current contribution's practical impact and methodological soundness. The paper is a promising initial exploration but is not yet ready for acceptance at a top venue without addressing these issues. I lean towards rejection, but the novelty and potential justify a borderline score.

MY FINAL SCORE: 4.5</score>
MY FINAL DECISION: Reject</decision>