## Summary

This paper introduces *Calgacus*, a protocol that uses an LLM to hide a secret text inside a different, steerable text of the same token length. The method is strikingly simple: record the rank of each token of the secret text under the LLM, then generate a stegotext by selecting the token at that rank from the distribution conditioned on a public key/prompt. Decoding is exact given the key and the same LLM. The paper demonstrates the method on Reddit posts with Llama 3 8B and follows with a philosophical discussion reframing hallucination as a failure of attributed intention rather than factual error, and a concrete "shipping unfiltered LLMs" scenario. The paper is a hybrid of a new-methods contribution and a position piece.

## Strengths

1. **The core idea is genuinely clever and elegantly simple.** The protocol (Section 3) is almost trivial to describe — record ranks, then reproduce them under a different prompt — yet it achieves the notable property that the stegotext and secret are the same token length. This simplicity is a virtue: the method is transparent, easy to implement, and decoding is exact by construction. The "low entropy token choices" analysis (paragraph bridging pages 4–5) gives a clear mechanistic explanation for why stegotexts are slightly less probable than originals, which is a genuine insight.

2. **The concrete examples (Figure 1) convincingly demonstrate the method working.** The political speech about Caesar hidden inside a roasted boar recipe, using different steerable prompts, makes the claimed property tangible and shows that the method produces coherent, topically steerable stegotexts.

3. **The philosophical discussion is thought-provoking and well-written.** The reframing of hallucination as "lack of intention" rather than factual error (Section 4), the connection to the Calgacus figure from Tacitus, and the discussion of the entangled probabilistic nature of LLM knowledge raise genuine questions that the field has not resolved. The writing is engaging throughout.

## Weaknesses

### Major

1. **No human evaluation for claims about human perception.** The paper asserts that stegotexts are "opaque to humans" (line 43) and that "while for a human both the original and fake texts are plausible" (line 132). The only evidence offered is log-probability assigned by the *same LLM that generated the stegotexts*, falling within the range of real Reddit posts. Log-probability is a fluency measure, not a human judgment of coherence or naturalness. The paper explicitly acknowledges this measure's defect (line 128: "this definition has a clear defect") but then proceeds to use it as the sole basis for claims about human perception. For a steganography paper that makes claims about human indistinguishability, the absence of even a simple A/B discrimination study is a significant gap. This weakness does not invalidate the core method, but it means the strength of the human-perception claims is unsupported.

2. **Quantitative evaluation is thin for the breadth of claims.** The evaluation uses:
   - 1 dataset (1000 Reddit posts, 85 tokens each, from one unspecified scrape)
   - 3 source texts selected at distributional landmarks (μ, μ-2σ, μ+2σ)
   - 100 stegotexts per source text
   - 1 generation LLM (Llama 3 8b)
   - 1 metric (log-probability)
   
   Three source texts, one length, one LLM, and one metric do not establish how the method generalizes across content types, lengths, different LLM sizes/families, or different secret text styles (technical writing, poetry, code, etc.). The paper's own Limitations section (line 148) notes dependencies on *e*, *k*, and the LLM, but the main evaluation does not systematically vary these. Broader evaluation would strengthen confidence in the method's general applicability.

### Minor

3. **No quantitative comparison to prior generative steganography methods.** The paper cites Ziegler et al. (2019), Kaptchuk et al. (2021, "Meteor"), Wu et al. (2024), and Zamir (2024) in Related Work, and positions Calgacus as novel due to the "same length" property. However, no empirical comparison of stegotext quality, capacity, or computational cost against any of these methods is provided. While the paper's contribution is primarily the same-length property rather than improved quantitative performance, a comparison would help the reader assess the practical significance of this property relative to existing approaches.

4. **Security and deniability claims have limited supporting evidence.** The deniability argument (Section 3.1) relies on the observation that for "some prompts the stegotexts can attain probabilities in the same ballpark as the original" (line 166). This is supported by only one ambiguous case in Figure 4 (the green distribution shows overlap, others are clearly separated). The brute-force bound of O(d^|k|) is standard, but the paper then notes an attacker could use semantic information to reduce the search space and calls this "an open research question" — which is honest but means the actual security posture is unclear. These limitations are acknowledged but they weaken the concrete security claims the paper makes.

### Trivial

None.

## Nice-to-Haves

- A human evaluation study (A/B discrimination or plausibility rating) would directly support the "opaque to humans" claims and significantly strengthen the paper.
- Testing on longer texts (200–500 tokens), additional LLMs (e.g., Llama 3 70B, Mistral, Qwen), and different text genres (news, fiction, technical writing) would improve generality.
- An ablation study varying the key *k* to measure its effect on stegotext quality.
- A comparison of decoding reliability across different hardware/quantization settings (the paper flags this concern but does not test it).

## Removed Points

These points are flagged to be removed; treat them with caution:

- **"The same-length claim is less significant than presented because the key must also be communicated."** The paper is clear that the same-length claim is about *s* and *e*, with *k* as a separately communicated key. This is properly scoped and not misleading.
- **"Floating-point determinism is a significant practical concern relegated to one sentence."** The paper explicitly addresses this in the Limitations section (line 148), which is the appropriate place. The paper acknowledges the concern rather than ignoring it.
- **"Figures 11 and 12 are in the appendix which is stripped."** The appendix exists in the original submission; the parser removed it. The paper should not be penalized for this.
- **"The tone is grandiose" and other style nitpicks.** These are presentation choices, not substantive weaknesses.
- **"The paper should cite more recent work."** Cannot be verified without external sources; the cited work ranges from 2019–2025, which is appropriate for a 2026 submission.

## Novel Insights

Beyond the paper's own contributions, no genuinely novel insight emerged from the reviews that the paper does not already articulate. The reviewer's identification of the human-evaluation gap is the most significant concern but is a straightforward reading of what the paper does vs. does not provide, not an external insight.

## Suggestions

1. Add a human evaluation study — even a small-scale A/B test — to substantiate the "opaque to humans" claim, or remove/qualify that claim commensurately.
2. Broaden the evaluation to more source texts, longer texts, multiple LLMs, and multiple text genres. Even doubling the source text count to 20–50 and testing on 2–3 additional LLMs would substantially improve confidence in generality.
3. Include a comparison against at least one prior method (e.g., Meteor) on a common metric (e.g., stegotext perplexity at comparable capacity) to contextualize the "same length" contribution.
4. Either provide a concrete test of the "shipping unfiltered LLMs" scenario end-to-end, or present it less as a demonstrated capability and more as an illustrative thought experiment.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>