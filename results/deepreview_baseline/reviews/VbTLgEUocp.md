## Summary

This paper introduces *Calgacus*, a protocol that uses Large Language Models (LLMs) to hide a secret text within a generated stegotext of the same token length, while allowing the stegotext to be coherent, stylistically steerable, and plausible. The method works by recording the rank of each token of the secret message in the LLM’s probability distribution, then generating the stegotext by selecting tokens at those same ranks conditioned on a secret prompt. The paper further discusses implications for LLM knowledge, hallucinations, and the erosion of trust in written communication, and sketches a scenario where unaligned LLM outputs can be covertly shipped inside aligned ones.

## Strengths

- **Simple and efficient protocol** – The method is remarkably straightforward, requiring only rank extraction from an LLM’s logits and rank-guided generation, making it easy to implement and fast to run even on consumer hardware.
- **Same-length hiding** – Unlike many prior steganographic schemes that expand messages or embed bits across multiple tokens, Calgacus achieves a 1:1 token-length ratio between the secret and the stegotext, which is a noteworthy property.
- **Thought-provoking discussion** – The paper raises genuinely interesting philosophical questions about the nature of LLM knowledge, hallucinations as absence of intention, and the decoupling of text from authorial intent. These reflections are well-motivated by the method and provide a broader context for the technical contribution.
- **Open-source model feasibility** – The demonstration that an 8-billion-parameter open-source LLM (Llama 3) suffices to produce plausible stegotexts makes the protocol concrete and reproducible.

## Weaknesses

### Major

- **Insufficient empirical evaluation** – The quantitative assessment relies on only three original texts (drawn from 1000 Reddit posts) and 100 stegotexts per original, all truncated to a fixed length of 85 tokens. This limited scale makes the claims about plausibility and detectability hard to generalise. Human evaluation of stegotext coherence, topic adherence, and detectability is entirely absent. The paper lacks a systematic comparison to existing LLM-based steganographic methods (e.g., Ziegler et al. 2019, Kaptchuk et al. 2021, Zamir 2024) in terms of capacity, quality, or security.
- **Security analysis is heuristic and incomplete** – The resistance to brute-force key search is argued via vocabulary size, but no empirical attack or formal security model is provided. The deniability claim relies on a single qualitative example (Figure 15, referenced but not shown in the main text) and the observation that some stegotexts have probabilities close to the original. A rigorous treatment of deniability (e.g., computational or information-theoretic) is missing.
- **Lack of comparison to non-steganographic baselines** – The paper shows that stegotext log-probabilities fall within the range of real Reddit texts, but this alone does not demonstrate that the stegotexts are indistinguishable from genuine human writing. Automated steganalysis classifiers or human perceptual studies would be needed to assess imperceptibility more convincingly.
- **Dependence on secret message predictability** – The method fails when the secret message is not predictable by the LLM (e.g., the hash example produces gibberish). The paper acknowledges this but does not quantify the regime of applicability (e.g., what types of texts yield acceptable stegotext quality). This is a significant practical limitation that is under-explored.

### Minor

- **Probability measure limitations** – The paper uses cumulative log-probability as a proxy for text plausibility, which is known to be sensitive to length and tokenisation. While the authors partially address this by fixing length, the measure conflates grammaticality, topical coherence, and style. Alternative metrics (e.g., perplexity difference from in-domain texts, or human-rated coherence) are not employed.
- **No analysis of tokenisation discrepancies** – The encoding/decoding process assumes identical tokenisation across sender and receiver, but subtle differences in tokeniser implementations or floating-point arithmetic could break exact recovery. This is briefly mentioned as a “challenge” but not tested or mitigated.

### Trivial

- The paper refers to figures (e.g., 11, 12, 13, 14, 15) that appear to be in the (removed) appendix, making some claims about concrete examples unverifiable from the main text alone. (Per instructions, this is a parsing issue and not penalised.)

## Nice-to-Haves

- A more extensive evaluation with multiple LLMs (beyond Llama 3 8B and a brief mention of Phi-3) and on longer texts would strengthen the generalisability.
- An automated steganalysis experiment (e.g., using a classifier trained to distinguish real texts from stegotexts) would provide a clearer picture of security.
- A discussion of how the method compares to *decoding-time* steganography (e.g., sampling token choices based on message bits) and why rank encoding is preferable would help position the work.

## Novel Insights

None beyond the paper’s own contributions: the recognition that LLMs’ ability to produce coherent text under rigid token-rank constraints reveals that standard generation is itself a constrained optimisation problem, and that this undermines the traditional link between textual coherence and authorial intent. The idea that hallucinations can be reframed as a lack of attributed intention rather than factual error is provocative, though not fully developed.

## Suggestions

- Expand the experimental section with a systematic comparison to at least one prior LLM steganography method (e.g., Meteor or the scheme of Ziegler et al.) on common metrics such as stegotext perplexity, bit-per-token capacity, and detection rate by a simple logistic regression classifier.
- Include a human evaluation study (e.g., Amazon Mechanical Turk) where participants rate the coherence and topic-consistency of stegotexts vs. genuine texts, and attempt to guess which texts hide messages.
- Provide a more detailed analysis of the trade-off between secret message predictability and stegotext quality, and offer guidance on when the method can be applied reliably.

## Score and Decision

The paper presents a simple and elegant protocol for same-length steganography with LLMs, accompanied by stimulating discussion. However, the technical evaluation is too limited in scale, breadth, and rigour to support the claimed contributions in a top venue. The lack of comparison to prior work, absence of human or automated detection experiments, and heuristic security analysis are major weaknesses that prevent acceptance. The work is better suited to a workshop or a venue where the conceptual contribution can be appreciated with less stringent experimental requirements.

MY FINAL SCORE: 4.0</s>  
MY FINAL DECISION: Reject</s>