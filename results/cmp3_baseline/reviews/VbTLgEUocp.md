## Summary

This paper presents *Calgacus*, a simple protocol that uses Large Language Models to hide a secret text within another coherent, plausible text of the same length. The method works by recording the ranks of tokens from the secret message under an LLM's probability distribution, then generating the stegotext by selecting tokens at those same ranks conditioned on a secret prompt. The paper demonstrates that even modest 8B-parameter open-source LLMs can produce high-quality stegotexts that fall within the distribution of real texts, and discusses the profound implications for AI safety, authorial intent, and the nature of LLM knowledge.

## Strengths

- **Novel and thought-provoking contribution**: The paper introduces a simple yet powerful protocol (Calgacus) that achieves full-capacity steganography—hiding a text within another text of the same length—which is a genuinely new capability. The method is elegant, requiring only rank-preserving token selection, and is clearly explained with concrete examples.

- **Strong empirical validation**: The authors provide convincing quantitative evidence (Figure 4) that stegotexts fall within the distribution of real texts (Reddit posts) in terms of LLM-assigned log-probability, while random strings and random English words do not. The analysis of rank frequencies and the "low entropy token choices" explanation (Figure 5) provides a principled understanding of why stegotexts are slightly less probable than originals.

- **Deep and provocative discussion**: The paper goes far beyond a technical steganography method. The discussion on hallucinations as a void of intention rather than factual error, the challenge to what it means for an LLM to "know" something, and the concrete AI safety scenario (shipping unfiltered LLMs disguised as aligned ones) are genuinely thought-provoking and raise important questions for the community.

- **Clear exposition and reproducibility**: The method is described with exceptional clarity (Figure 3 is excellent), the protocol is simple to implement, and the paper provides sufficient detail for reproduction. The use of open-source models (Llama 3 8B) and publicly available datasets (Reddit posts) supports reproducibility.

## Weaknesses

### Fatal
None.

### Major
1. **Limited empirical evaluation of the core claim**: The paper claims that stegotexts are "plausible" and "coherent," but the only quantitative evaluation is the log-probability comparison (Figure 4), which measures statistical plausibility under an LLM, not human-judged coherence. The paper lacks any human evaluation study (e.g., human raters judging whether stegotexts are natural, or whether they can distinguish real from fake texts). Given that the paper's central claim is that the stegotexts are "coherent and plausible" to humans, this is a significant gap. The paper even acknowledges that LLMs can distinguish real from fake texts on average, but does not test whether humans can.

2. **The security analysis is superficial and lacks rigorous evaluation**: The paper discusses attack scenarios and deniability at a conceptual level but provides no empirical security evaluation. There is no attempt to demonstrate or quantify the difficulty of key recovery, no analysis of the information leakage from the stegotext, and no comparison to existing steganographic methods in terms of security guarantees. The claim that inserting a random string in the key "is enough to nip it in the bud" is stated without evidence. For a paper that presents a steganographic protocol, the lack of any security evaluation is a significant weakness.

3. **The "same length" property is in tokens, not characters or words**: The paper emphasizes that the stegotext is the same length as the secret message, but this is measured in LLM tokens, not in human-perceptible units (characters, words, or sentences). Since tokenization is not transparent to users, the practical significance of "same length" is diminished. A 100-token secret message and a 100-token stegotext could differ substantially in character count or word count, which undermines the claimed symmetry that prevents establishing which text is authentic "at first sight."

4. **The AI safety scenario is speculative and lacks concrete validation**: The "shipping unfiltered LLMs" scenario (Section 4) is presented as a concrete application, but the paper does not demonstrate it working end-to-end. There is no experiment showing that the protocol can successfully encode an unfiltered answer within a compliant response, nor any analysis of the practical challenges (e.g., the oLLM must generate the exact same ranks as the encoding step, which requires identical model versions, quantization, and hardware). The scenario is compelling but remains a thought experiment.

### Minor
1. **The quantitative evaluation is limited to a single LLM (Llama 3 8B) for the main experiment**: While the paper mentions using Phi-3 3.8B for verification (Figure 14 in the appendix), the core results (Figure 4) rely on a single model. More diverse evaluation across different model families and sizes would strengthen the claims.

2. **The "soundness" metric has acknowledged limitations**: The paper correctly notes that log-probability is not a perfect measure of meaningfulness, but then uses it as the primary quantitative evidence. The reliance on a single, imperfect metric is a concern, especially since the paper itself points out its defects.

3. **The deniability argument is not empirically supported**: The paper claims deniability based on the observation that some stegotexts have probabilities comparable to the original text, but only provides a single example (Figure 15 in the appendix). A systematic analysis of how often this occurs and under what conditions would strengthen the claim.

### Trivial
None.

## Nice-to-Haves
- A human evaluation study (e.g., Amazon Mechanical Turk) where raters judge the naturalness of stegotexts vs. real texts, or attempt to distinguish them.
- A systematic security evaluation, including attempts to recover the key from stegotexts using search or optimization methods.
- An end-to-end demonstration of the "shipping unfiltered LLMs" scenario with concrete examples and success metrics.
- Comparison to existing generative steganography methods (e.g., Meteor, Ziegler et al.) in terms of capacity, quality, and security.

## Novel Insights

The paper's most novel insight is the reframing of LLM hallucinations as a failure of intention attribution rather than factual inaccuracy. By showing that an LLM can generate perfectly coherent text that is entirely divorced from any authorial intent (since every token is chosen to encode an external message), the paper argues that the unsettling experience of reading LLM-generated text is not about falsehood but about the absence of a trustworthy authorial voice. This reframing is genuinely thought-provoking and connects to philosophical questions about text, authorship, and meaning that are rarely discussed in ML venues. The connection to Oulipo literature and the constraint of chance in standard LLM generation is also insightful.

## Suggestions
1. Conduct a human evaluation study to validate the claim that stegotexts are "coherent and plausible" to human readers. This is the most critical missing piece.
2. Provide a systematic security analysis, including attempts to recover the key from stegotexts using search or optimization, and quantify the difficulty.
3. Demonstrate the "shipping unfiltered LLMs" scenario end-to-end with a concrete example, including the encoding and decoding steps.
4. Compare the method to existing generative steganography approaches (e.g., Meteor, Ziegler et al.) in terms of capacity, stegotext quality, and security.

## Score and Decision

The paper presents a genuinely novel and elegant method for full-capacity steganography using LLMs, with a clear exposition and thought-provoking discussion of implications. However, the empirical evaluation is insufficient to fully support the core claims: there is no human evaluation of stegotext plausibility, the security analysis is entirely conceptual, and the AI safety scenario is not demonstrated. These gaps prevent the paper from being a complete contribution. The method itself is interesting and the discussion is valuable, but the lack of rigorous empirical validation for the central claims (human plausibility, security) is a significant weakness.

MY FINAL SCORE: 6.0score</score>
MY FINAL DECISION: Borderline Accept</decision>