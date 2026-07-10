Now I have all the information I need. Let me compile the final review.

## Summary

This paper presents *Calgacus*, a protocol for full-capacity (same-length) steganography using LLMs. The core idea is elegant: record the ranks of tokens in a secret text under an LLM's probability distribution, then generate a cover text by selecting tokens at those same ranks under a different prompt. The result is a coherent cover text of identical token length that can be decoded back to the original secret by anyone who knows the secret prompt. The paper demonstrates the protocol on a small set of examples, provides a theoretical analysis of why stegotexts have systematically lower log-probability, and discusses far-reaching implications for trust in text, hallucination, and AI safety.

## Strengths

- **Genuinely novel protocol with a clean property.** The idea of using rank-preserving generation to achieve same-length steganography is simple, elegant, and directly accomplishes what prior LLM steganography methods (which embed compressed bitstrings, producing longer stegotexts) cannot. This full-capacity property is a genuinely distinct capability. [favorability=15.44]

- **Qualitative examples are striking.** Figure 1 convincingly demonstrates a political speech about Roman tyranny hidden inside a roasted-boar recipe that reads naturally. At the demonstrated length (~85 tokens), the method plainly works on concrete instances. [favorability=15.61]

- **The "low entropy token choices" analysis (Section 3) is theoretically illuminating.** The paper identifies *why* stegotexts are systematically less probable despite matching ranks: rank-1 tokens occur at ~40% frequency in the secret text but are "wasted" on low-entropy positions in the cover text where the LLM would assign near-100% probability anyway. This is a genuine insight beyond just presenting results. [favorability=9.55]

- **The Discussion (Section 4) is thoughtful and well-grounded.** The reframing of hallucinations as a failure of intention rather than factuality, the connection to Oulipo constraints, and the "shipping unfiltered LLMs" scenario are substantive philosophical observations that follow from the protocol rather than being bolted on. [favorability=14.52]

## Weaknesses

### Fatal
None.

### Major

- **The experimental evaluation is strikingly thin relative to the scope of claims.** Only 3 source texts are used (chosen at μ, μ−2σ, μ+2σ of a 1000-text Reddit distribution), all at a single fixed length of 85 tokens (~60 words), using a single LLM (Llama 3 8B) for generation. The paper frames capabilities like hiding "the first page of the unreleased 8th Harry Potter book" or enabling covert communication, but has not demonstrated the method at longer lengths (500+ tokens), with diverse text types (code, technical, poetry), or with texts containing rare tokens. A systematic characterization of failure modes beyond the hash counterexample is absent. [favorability=-3.78]

- **The paper makes claims about human plausibility without human evaluation.** The text states "while for a human both the original and fake texts are plausible" (Section 3), yet the evidence for plausibility rests entirely on LLM-assigned log-probabilities matching the distribution of real Reddit texts. Prior work on neural text detection has shown that fluency metrics and human judgment can diverge. Without human evaluation, the central practical claim about stegotext indistinguishability is unsupported. [favorability=-2.40]

- **No quantitative comparison to prior steganographic methods.** The paper mentions Ziegler et al. (2019), Kaptchuk et al. (2021), Wu et al. (2024), and Zamir (2024) but never measures what is sacrificed for full capacity: does this method produce more detectable text? Texts of lower fluency? Weaker security? Without baselines, the practical trade-offs of the approach are uncharacterized. [favorability=-2.30]

### Minor

- **The security analysis (Section 3.1) is informal.** The brute-force bound O(d^|k|) assumes the key space is the full vocabulary, while natural-language keys have vastly lower entropy. The paper acknowledges this but provides no estimate of the actual search space reduction or empirical test of key recovery difficulty. The deniability argument relies on a single appendix example (Figure 15). [favorability=0.73]

- **The choice of 85 tokens is unexplained.** The paper truncates Reddit texts to this length but never justifies why this specific length was chosen or characterizes how the protocol scales to longer/shorter texts. [favorability=5.22]

- **No statistical test comparing distributions in Figure 4.** The claim that stegotext probabilities are "within" the real text distribution is made purely visually. A Kolmogorov-Smirnov test or similar would give a quantitative basis. [favorability=4.62]

- **Variance across different prompts k is not reported.** The number of distinct prompts used is not stated, and the sensitivity of stegotext quality to the prompt is not characterized. [favorability=5.21]

### Trivial
None.

## Nice-to-Haves

- Expand evaluation to more source texts (50–100), additional lengths (50, 100, 200, 500 tokens), and multiple LLMs (e.g., Qwen 3 8B, Phi-3) to strengthen generality claims.
- Add a human evaluation study (e.g., coherence ratings or A/B detection) to support the claim that stegotexts are plausible to humans.
- Include comparison to at least one prior LLM steganography method to contextualize the full-capacity trade-off.
- The paper acknowledges the identical-LLM limitation but does not test or mitigate it; a brief experiment quantifying failure rates across GPU architectures or software versions would strengthen practical claims.

## Removed Points

These points were raised in the input review but are excluded under the filtering rules:

1. "Abstract and Introduction rhetorically inflated" — The paper frames hypothetical scenarios ("the first page of the unreleased 8th Harry Potter book") as illustrative possibilities rather than demonstrated results, which is standard. No factual misrepresentation.
2. "Dependence on identical LLM implementations is a significant practical limitation" — The paper acknowledges this limitation explicitly. The weakness is already disclosed; escalating it adds no new information.
3. "Practical attack scenario (key transmitted in the clear in shipping unfiltered LLMs scenario) not analyzed" — The paper's Comments section does address this via a plausible-deniability argument. The concern is valid about thoroughness, but the paper does not ignore it.
4. "Scale up evaluation," "Characterize when it fails," "Demonstrate shipping unfiltered LLMs end-to-end" — These are constructive suggestions, not weaknesses of the submission as-is.

## Novel Insights

The input review's key insight that the paper's evidence-to-claims ratio is the central weakness is correct and worth emphasizing. However, the reverse side is also noteworthy: the protocol's simplicity and elegance mean that even minimal experimental validation is sufficient to establish that it *works*; the question is how *well* and under what conditions. The paper's strongest contribution may ultimately be conceptual rather than empirical — the protocol itself and the discussion it enables — which is an unusual profile for an ICLR paper.

## Suggestions

1. Most critically, expand the evaluation on the paper's own terms before any revision effort: at minimum 50 source texts, 3+ lengths, and 2+ LLMs.
2. Add a human-subject evaluation of stegotext plausibility (even a small-scale AMT study would significantly strengthen the claims).
3. Include at least one prior steganographic method as a baseline comparison.
4. Report a statistical test (e.g., two-sample KS) for the log-probability distribution comparison in Figure 4.

## Score and Decision

**Round 1 bracket:** 4–6 (based on comparing against anchors in this range: "Plausibly Deniable Encryption with LLMs" avg 4.80, "Hidden in Plain Text" avg 5.00, "WASA" avg 5.50).

**Narrowing to final score:** The closest anchor is "Plausibly Deniable Encryption with LLMs" (4.80, Reject), which shares the profile of an interesting LLM-based protocol with thin evaluation and informal security analysis. The present paper's protocol is more genuinely novel (strength favorability ~15 vs. ~10 for that anchor) and has a substantive Discussion section the anchor lacks. However, its experimental evaluation is weaker (3 source texts vs. extensive experiments in WASA at 5.50, and more modest but still more thorough experiments in Hidden in Plain Text at 5.00). The major weaknesses (thin evaluation, no human study, no baselines) each carry negative favorability (−3.78, −2.40, −2.30) comparable to the structural concerns that resulted in rejection for those anchors.

**Final score: 4.5.** The paper has a genuinely novel protocol and a thoughtful discussion, but the experimental evaluation is insufficiently rigorous for the scope of claims made. The protocol's existence is convincingly demonstrated; its generality, practical security, and human-level plausibility are not.

**Decision: Reject**

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>