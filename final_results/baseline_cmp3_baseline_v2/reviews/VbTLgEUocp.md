## Summary

The paper presents *Calgacus*, a simple protocol that uses a Large Language Model to hide an arbitrary secret text inside a different, coherent, and plausible cover text of exactly the same length (in tokens). The method works by recording the rank of each token of the secret text in the LLM’s probability distribution, then generating the cover text by selecting tokens at those same ranks conditioned on a secret prompt. The authors demonstrate the protocol with modest open-source LLMs, evaluate the plausibility of the generated cover texts via log-probability comparisons to real Reddit posts, and discuss far-reaching implications for AI safety, the nature of LLM knowledge, and the concept of hallucination.

## Strengths

- **Novel and striking capability**: The paper introduces a method that achieves full-capacity steganography (secret and cover text of equal length) while maintaining plausible cover text. This is a non-trivial and conceptually interesting result.
- **Simplicity and efficiency**: The protocol is extremely simple—essentially a deterministic variant of standard autoregressive generation—and works on consumer hardware with 8B-parameter models in seconds, making it immediately accessible.
- **Thought-provoking discussion**: The paper raises deep questions about authorial intent, LLM knowledge, and the definition of hallucination, connecting the technical result to broader philosophical and safety concerns in a compelling way.

## Weaknesses

### Fatal
None.

### Major
- **Limited empirical evaluation**: The plausibility evaluation uses only three original texts (each generating 100 stegotexts) and a single dataset of 1000 Reddit posts. No human evaluation of cover-text quality is performed, and the only metric is log-probability from the same LLM used for generation, which may be biased. The paper does not compare against any existing steganographic method (e.g., Meteor, Ziegler et al.) to contextualize the trade-offs.
- **Weak security analysis**: The security discussion is informal and lacks rigorous threat modeling or quantitative attack analysis. The claim of deniability is supported only by a single anecdotal example (Figure 15, not visible in the main text). The protocol’s reliance on exact reproducibility of logits across different hardware/software is noted but not addressed experimentally.
- **No ablation or failure analysis**: The paper does not systematically study how the quality of the cover text degrades with the entropy of the secret text, the choice of LLM, or the length of the secret. The hash example shows failure, but no systematic characterization is provided.

### Minor
- **Evaluation metric limitations**: Log-probability is used as a proxy for plausibility, but the authors themselves acknowledge its defects (length dependence). Perplexity is dismissed without a thorough justification, and no alternative metrics (e.g., human ratings, grammar scores, topic coherence) are considered.
- **Lack of comparison to prior work**: While related work is cited, the paper does not quantitatively compare Calgacus to existing LLM-based steganography methods in terms of capacity, security, or text quality. The claim of “full capacity” is highlighted, but the cost in plausibility or detectability is not benchmarked.

### Trivial
None.

## Nice-to-Haves

- A human evaluation study (e.g., Amazon Mechanical Turk) to assess whether humans can distinguish cover texts from real texts.
- A comparison with prior steganography methods (e.g., Meteor, Ziegler et al.) on the same dataset, measuring capacity, perplexity, and detection rate.
- An analysis of the protocol’s robustness to different LLMs, tokenizers, and floating-point precision.

## Novel Insights

Beyond the technical contribution, the paper offers a genuinely novel perspective on LLM-generated text: it argues that the very coherence of LLM output is a form of constraint satisfaction, and that the absence of authorial intent—made vivid by the ability to encode arbitrary messages—should lead us to redefine hallucinations not as factual errors but as a failure of the reader to attribute intention. This reframing is insightful and connects the steganographic result to fundamental questions about trust in machine-generated text.

## Suggestions

- Conduct a human evaluation to validate that cover texts are indeed plausible and indistinguishable from real texts.
- Compare Calgacus against at least one prior LLM steganography method (e.g., Meteor) on a common dataset, reporting both capacity and text quality metrics.
- Provide a more rigorous security analysis, including a quantitative estimate of the key space and a discussion of known-plaintext or chosen-plaintext attacks.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>  
MY FINAL DECISION: <decision>Reject</decision>