Now I have all the information I need. Let me produce the final review.

## Summary

This paper presents Calgacus, a simple protocol that uses an LLM to hide a meaningful text inside another text of the same token length. The method works by extracting the rank of each token of the secret text in the LLM's probability distribution, then generating a new text under a different prompt (the key) by choosing the token at each corresponding rank. The same-length property is a genuine differentiator from prior LLM steganography methods. The paper also devotes substantial space to a philosophical discussion about how this capability challenges notions of authorial intent, hallucination, and LLM knowledge.

## Strengths

1. **The method is genuinely simple, elegant, and novel.** The core idea — encode the rank of each secret-message token in the LLM's predictive distribution, then generate the stegotext by replicating those ranks under a different prompt — is stated concisely (lines 104–108) and is easy to understand and reproduce. The same-length property is a clear differentiator from prior methods that expand the message. The examples in Figure 1 are striking visual demonstrations.

2. **The "same-length" property is a meaningful distinction from prior work.** The paper correctly identifies that most LLM-based steganography embeds bits in low-entropy token choices, which typically expands the message (line 67). Achieving a 1:1 token ratio between secret and stegotext is a genuine differentiator, and the method delivers on this property.

3. **The discussion of hallucinations as a failure of intention attribution (Section 4) is thoughtful and well-argued.** The connection to Tacitus (lines 232–236), Oulipo constraint literature (line 244), and Hofstadter's aperiodic crystals (Figure 6) is genuinely illuminating. This discussion constitutes a meaningful conceptual contribution that would be interesting even without the method.

4. **The "Low entropy token choices" analysis (lines 134–146) is an insightful technical contribution.** It correctly diagnoses why stegotexts are less probable than originals: rank-1 tokens from the secret are "wasted" on high-entropy positions in the stegotext, where many tokens are nearly equally probable. This provides genuine understanding beyond the method itself.

## Weaknesses

### Major

1. **No comparison against any baseline method.** The Related Work section (line 67) names four prior LLM steganography methods (Ziegler et al., 2019; Kaptchuk et al., 2021/Meteor; Wu et al., 2024; Zamir, 2024), but none is used as a baseline. The paper cannot demonstrate that Calgacus offers any advantage — in stegotext quality, capacity, security, or anything else — over existing approaches. The paper's novelty claim is the "full capacity" (same-length) property, but without measuring what capacity other methods achieve (in bits per token), the reader cannot assess whether this is a substantial improvement. Since the paper positions itself as introducing *a protocol*, baseline comparisons are essential.

2. **The evaluation is too thin to support the scope of the claims.** The paper evaluates Calgacus on exactly **3** original texts from a set of 1000 Reddit posts (lines 130–131), truncated to 85 tokens, generating 300 stegotexts total. This does not support the generality claimed in the abstract ("A meaningful text can be hidden inside another... coherent and plausible text"). The paper tests only one text length, one genre (Reddit posts), and one language (English; Chinese appears only anecdotally in Figure 6). The abstract's claim of "high-quality results" is never operationalized beyond LLM log-probability. The paper acknowledges that hashes fail and that the method has limitations, but does not systematically explore the boundaries of when it works.

3. **No human evaluation of stegotext quality despite claims about human perception.** The paper states that results are "opaque to humans" and that the method "prevents one from establishing at first sight which text is authentic" (lines 17–19). It also asserts that "while for a human both the original and fake texts are plausible" (line 132). Yet no human study is conducted. The paper relies entirely on LLM log-probability as a proxy for textual plausibility; while the paper acknowledges the metric's limitations (lines 128–129), it never validates the proxy against human judgment. This is a significant gap between the claims and the evidence.

4. **No quantification of decoding reliability.** The paper claims that the original text is "exactly recoverable" (line 17) but acknowledges that sender and receiver must run the LLM under identical conditions (line 148). The paper provides no empirical data on decoding success rates, sensitivity to hardware differences, or numerical precision issues. For a method whose central functional claim is exact recovery, this is a notable omission.

### Minor

5. **No timing data for claimed efficiency.** The abstract states that "a message as long as this abstract can be encoded and decoded locally on a laptop in seconds," but no timing measurements are reported in the main text. The claim is plausible given the method's simplicity, but remains unsubstantiated.

6. **Capacity is never quantified in bits per token.** The paper claims "full capacity" but never states what this means in information-theoretic terms. Since ranks range from 1 to V (~100k), each token could encode up to ~17 bits, but the effective capacity given that high ranks degrade stegotext quality is never bounded or measured.

### Trivial

7. The decoding procedure description (line 108) should specify what initial context is used when regenerating *e* — the empty string, a base system prompt, or something else — since the first token's rank is defined relative to the unconditional distribution.

## Nice-to-Haves

- A comparison against even one prior method (e.g., implement rank-based encoding from Ziegler et al. 2019 on the same 300 test cases) would transform the evaluation.
- A small human evaluation (binary forced-choice between original and stegotext) would validate the claims about opacity to humans.
- Testing across diverse text types (narrative, argumentative, instructional) and lengths would provide a more robust evaluation.
- Reporting decoding reliability across different hardware configurations would strengthen the method's practical claims.

## Removed Points

- **"AI safety scenario is purely theatrical"** — Removed from Major to Minor (not in main weaknesses). The paper explicitly frames this as a "play" and discussion of implications (lines 180–206). It never claims to have empirically validated this deployment scenario. The references to Figures 11 and 12 show concrete examples exist in the appendix. Criticizing the paper for not implementing a full system it doesn't claim to implement would be unfair.
- **"Security analysis is informal/qualitative"** — Removed. The paper explicitly states it is avoiding formal models ("we will avoid building a palace on the sand," line 61). This is a conscious scoping choice, not an oversight.
- **Figure caption artifacts** — Removed. These are parser errors, not paper problems.
- **Missing related work / outdated baselines** — Removed per instructions (lack of external sources to verify).
- **Various section-by-section nitpicks** — Removed (formatting notes, minor presentation points that don't affect the core evaluation).

## Novel Insights

The single most valuable synthesis emerging from the reviews is that the paper's fundamental tension is between its two natures: as a method paper it has a genuinely elegant protocol but an evaluation far too thin to support its claims; as a position paper it has a genuinely thoughtful discussion but one that would benefit from a more clearly demarcated speculative framing. The "low entropy token choices" analysis bridges these two aspects — it is simultaneously a technical explanation of an observed phenomenon and a conceptual contribution about why rank-based steganography inherently degrades quality. The paper would be substantially stronger if the evaluation matched the ambition of the discussion, or if the discussion were explicitly scoped as the primary contribution with the method as illustration.

## Suggestions

1. Add baseline comparisons against at least Ziegler et al. (2019) or Meteor (Kaptchuk et al., 2021) on the same metrics (log-probability distribution, capacity in bits/token, decoding accuracy).
2. Conduct a human evaluation (e.g., 50+ participants, binary forced-choice) to validate the claim that stegotexts are "opaque to humans."
3. Report timing measurements to substantiate the "laptop in seconds" claim.
4. Report decoding reliability across different hardware configurations.
5. Provide capacity analysis in bits per token, including effective capacity accounting for quality degradation at higher ranks.
6. If the paper is primarily a conceptual/position piece, reframe it accordingly and clearly demarcate which claims are empirically supported vs. speculative.

## Score and Decision

**Calibration anchors used:**

| Anchor Path | Avg Score | Round | Comparison |
|---|---|---|---|
| OD-Stega (`IQafqgqDzF.md`) | 3.50 | 1 | LLM steganography paper with more rigorous math but rejected for weak evaluation and questionable practical relevance. Current paper has a more novel core idea and better discussion but similarly weak evaluation. |
| Hidden in Plain Text (`urQi0TgXFY.md`) | 5.00 | 1 | Steganographic collusion paper with thorough experiments. Rejected despite solid evaluation. Current paper has less rigorous evaluation but a more novel protocol. |
| Plausibly Deniable Encryption (`7suavRDxe8.md`) | 4.80 | 1 | Idea-driven LLM+crypto paper with insufficient formal evaluation. Most similar in structure and weaknesses to current paper. Rejected. |
| Alignment Problem from DL Perspective (`fh8EYKFKns.md`) | 5.25 | 2 | Pure position paper accepted at ICLR. Current paper is a hybrid but makes stronger empirical claims without adequate support. |
| LLM Spark (`0sJ8TqOLGS.md`) | 5.25 | 2 | Position/evaluation paper. Rejected. |
| Clever Hans (`PtnttTKgQw.md`) | 5.00 | 2 | Simple-features paper with interesting findings. Rejected. |
| Textbooks Are All You Need (`Fq8tKtjACC.md`) | 6.00 | 2 | Strong empirical results but rejected for low novelty. Current paper has higher novelty but much weaker evaluation. |

**Round 1 bracket:** 4.0 – 6.0
**Final score determined by:** Narrowed against OD-Stega (3.50, rejected — current paper has more novelty and better discussion but similarly weak evaluation for a method paper) and Plausibly Deniable Encryption (4.80, rejected — most structurally similar). Raised slightly above those due to the genuinely novel same-length property and the unusually thoughtful discussion, but kept below 5.5 because the empirical gaps are significant.

MY FINAL SCORE: 5.0
MY FINAL DECISION: Reject