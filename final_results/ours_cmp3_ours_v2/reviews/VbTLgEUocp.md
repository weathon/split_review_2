Now I have good calibration anchors. Let me compose the final review.

**Bracket reasoning**: Based on calibration, the most topically similar paper ("Hidden in Plain Text", score 5.00) was rejected despite having more thorough experiments. The SIRA paper (4.75, rejected) had extensive empirical evaluation across 7 methods. The current paper has greater fundamental novelty than either (the same-length property is genuinely new) but significantly less evaluation breadth. Papers in the 3.0 range (Sparse Watermarking) had comparable or better empirical evaluation but less novelty. This places the paper between 3 and 5 — the narrowest plausible bracket is 3.5–5.0.

**Narrowing**: Within this bracket, the paper's core idea is more novel than the 3.0 anchor, but the evaluation falls well short of the 4.75–5.0 anchors. I settle on 4.0.

Now let me produce the final review.

## Summary
2-3 sentence summary of the paper's contribution.

This paper presents Calgacus, a protocol that uses an LLM to encode a hidden text within a second "stegotext" of exactly the same token length. The method works by recording the rank of each token of the hidden text under the LLM's conditional distribution, then generating the stegotext by choosing those same ranks after a secret prompt — a simple recipe that is clearly described and trivially reproducible. The paper demonstrates the method with Llama 3 8b on Reddit posts, reports that stegotext log-probabilities fall within the real-text distribution, and includes a discussion section connecting the technique to questions about authorial intent, hallucinations, and AI safety.

## Strengths
- **Novel same-length property for LLM steganography.** Prior work (Ziegler et al., 2019; Kaptchuk et al., 2021) requires the stegotext to be longer than the hidden message or modifies an existing covertext. Calgacus achieves full capacity — the stegotext is exactly as long (in tokens) as the hidden message. This is a new and non-obvious consequence of the rank-based encoding scheme (Section 3, Figure 3).
- **Extremely simple and reproducible method.** The recipe in Section 3 is straightforward: tokenize the hidden text, record the rank of each token under the LLM's conditional distribution, then generate the stegotext by choosing those same ranks after a secret prompt. Anyone with access to logits can implement it in an afternoon.
- **Insightful "low entropy token choices" analysis.** Section 3's explanation (lines 134–146) of why stegotexts have lower probability than originals — rank-1 tokens in stegotexts correspond to higher-entropy positions than rank-1 tokens in originals — is a clean mechanism-level insight that goes beyond simply presenting the method.
- **Thought-provoking discussion.** The reframing of hallucinations as a failure of intention-attribution rather than factuality (Section 4), and the connection to Oulipo constraints and Hofstadter's aperiodic crystals, gives the paper intellectual texture that is unusual and memorable.

## Weaknesses

### Fatal
None.

### Major
- **No human evaluation of stegotext plausibility, despite the paper's central claim depending on it.** The abstract states that the hidden text is placed "inside another, completely different yet still coherent and plausible, text." The paper claims "while for a human both the original and fake texts are plausible" (line 132). The only quantitative evidence is LLM-assigned log-probabilities (Figure 4), which measures what the *model* finds plausible, not what a human reader would find plausible. The cross-check with Phi-3 (Figure 14) mitigates this only slightly — it is still an LLM-as-evaluator, not a human-as-evaluator. There is no Turing-test-style evaluation, no crowdsourced plausibility rating, and no detection experiment with human participants. For a method whose defining claim is that the output should appear genuine to a human reader, the absence of any human evaluation is a significant empirical gap.

- **Evaluation scope is too narrow to support the paper's general claims.** The quantitative experiment uses exactly three source texts drawn from a single domain (Reddit posts/comments, 85 tokens), a single model (Llama 3 8b), and a single token length. The paper claims "an entire article can be encoded" but provides no article-length experiments. There is no evaluation across different content types (news, fiction, code, instructions, dialogue), different lengths, or different generator LLMs. The generalizability claim rests on 3 × 100 = 300 stegotexts of one length from one model on one domain. The paper acknowledges some limitations (e.g., hashes fail) but does not systematically characterize the boundary between success and failure.

### Minor
- **No comparison to any prior steganography method.** The experimental section compares Calgacus stegotexts only against a null model (random ASCII, random English words) and real texts. While the same-length property makes direct comparison non-trivial (prior methods produce longer stegotexts), a comparison on output plausibility or decoding accuracy would help readers assess trade-offs. This limits the paper's ability to position its contribution relative to existing work.

- **No empirical measurement of decoding accuracy.** The paper describes the protocol as lossless in principle (ranks are recorded and then followed) but never empirically verifies that decoding always recovers the exact original text across multiple trials. Floating-point determinism across different hardware or software stacks is mentioned as a concern, but no systematic measurement is reported.

- **Security analysis is acknowledged as incomplete.** The paper notes that "the attacker could reduce the search space using the information revealed by s" and that this "remains an open research question" (lines 154–155). The deniability argument relies on a single appendix example (Figure 15). For a reader evaluating whether to use the protocol for anything security-sensitive, the analysis is insufficient. However, the paper's primary contribution is the protocol itself and its implications, not a rigorous security proof, so this is a minor rather than major weakness.

### Trivial
None.

## Nice-to-Haves
- A broader evaluation across text types (news, fiction, dialogue, code), lengths (including article-length texts of 500+ tokens), and target LLMs (at least one additional model as generator).
- Ablation of key design choices: whether to use a single key k or an additional k', length of k, effect of different LLMs on output quality.
- Even a small-scale human evaluation (e.g., 50–100 samples rated by crowdsourced workers for naturalness) would substantially strengthen the core plausibility claim.

## Removed Points
- **Weakness about the "shipping unfiltered LLMs" scenario having a logical problem.** The reviewer argued that transmitting k alongside s breaks security since an eavesdropper can decode u. This misunderstands the scenario: the paper describes a plausible deniability argument against a platform/regulator, not cryptographic security against an eavesdropper. The paper explicitly frames this as a regulatory argument ("the company can argue that u was obtained by the user on their machine through the open-source model..."). The threat model is different from what the reviewer assumed.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. **Add a human evaluation study** as the highest-priority improvement — a simple crowdsourced Turing-test-style experiment asking participants whether each text looks naturally written or machine-generated, using a few hundred samples across different content types.
2. **Broaden the experimental evaluation** to include at least 3–5 different text types, multiple lengths (including article-length ~500+ tokens), and at least one additional LLM as generator (not just as evaluator).
3. **Empirically measure decoding accuracy** across a set of trials to confirm the lossless claim and characterize conditions where it might fail.
4. **Add a conceptual or empirical comparison** to at least one prior steganography method (e.g., reporting plausibility metrics for Ziegler et al. or Kaptchuk et al. on the same evaluation setup) to help readers understand the trade-offs of the approach.

## Score and Decision

My calibration used the following anchors from the deepreview corpus:

| Paper / Path | Avg Score | Round | Comparison |
|---|---|---|---|
| Hidden in Plain Text: Emergence & Mitigation of Steganographic Collusion (urQi0TgXFY) | 5.00 | R1 | More thorough experiments on a related topic, less fundamental novelty. Rejected. |
| SIRA: Exposing Vulnerabilities in Text Watermarking (8Me0Y01mkY) | 4.75 | R1 | Extensive experiments across 7 methods; comparable methodological novelty but significantly more evaluation breadth. Rejected. |
| Watermark Smoothing Attacks (1AYrzmDK4V) | 4.25 | R1 | Solid experiments with multiple baselines; comparable novelty level. Rejected. |
| Sparse Watermarking in LLMs (jbfDg4DgAk) | 3.00 | R1 | Less novelty than current paper, similar evaluation narrowness. Rejected. |
| A Watermark for Black-Box Language Models (0koPj0cJV6) | 4.60 | R1 | Thorough theoretical+empirical paper. Rejected despite solid contribution. |

Round 1 bracket: 3.5–5.0. The current paper has stronger fundamental novelty than most anchors in this range but weaker empirical evaluation. I place it at the lower end of this bracket.

**Final score: 4.0. Decision: Reject.**

The paper has a genuinely novel and interesting idea, presented clearly and with admirable simplicity. However, the empirical evaluation falls short of ICLR standards for a method paper. The central claim — that stegotexts are coherent and plausible to human readers — is supported only by LLM-assigned log-probabilities on 300 stegotexts from 3 source texts of a single domain and length, with no human evaluation. The paper would benefit from being reframed as a provocative demonstration and position piece, and strengthened with a human study and broader evaluation before resubmission.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>