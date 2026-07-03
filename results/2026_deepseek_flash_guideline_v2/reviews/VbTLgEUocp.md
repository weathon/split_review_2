Now I have all the evidence I need. Let me write the final consolidated review.

## Summary
This paper presents Calgacus, a protocol that uses LLMs to hide a secret text within a different coherent text of the same token length. The method records the rank of each token of the secret message in the LLM's probability distribution, then generates the stegotext by selecting tokens at those same ranks after a secret steering key. The paper also includes a philosophical discussion about hallucination, intentionality, and LLM knowledge.

## Strengths
- **Full-capacity generative steganography**: Calgacus achieves the property that the stegotext and the hidden secret message have exactly the same token length, which prior LLM steganography methods do not offer (Section 2). This is a direct consequence of the rank-recording algorithm (Figure 3).
- **Quantitative evidence that stegotexts fall within the real-text distribution**: Figure 4 shows that 300 stegotexts (100 each from 3 source texts at μ, μ−2σ, μ+2σ) all have log-probabilities within the distribution of 1000 real Reddit posts when evaluated by Llama 3 8B, while random ASCII and English-word strings fall far outside. This provides an empirical basis for the plausibility claim.
- **Clear mechanistic explanation of the probability gap**: The paper provides a concrete analysis (Section 3, "Low entropy token choices") of why stegotexts are less probable than originals despite identical rank sequences, grounded in a specific example ("Britain was invaded twice by Gaius Julius" → "\_Caesar") and supported by rank-frequency data from a 1.3k-token Economist article (Figure 5).
- **Cross-model verification**: Figure 14 verifies that the same probability shift pattern is observable using Phi-3 3.8B, a different LLM from the one used to generate the stegotexts (Llama 3 8B), addressing potential circularity concerns.
- **Intellectually stimulating discussion**: The discussion (Section 4) on hallucination as a "void of intention" rather than factual error, the Oulipo comparison, and the "shipping unfiltered LLMs" application scenario are genuinely thought-provoking.

## Weaknesses

### Fatal
None.

### Major
- **Reconstruction accuracy is never empirically verified**: The paper claims the original text is "exactly recoverable" (line 17) and describes the decoding procedure (line 108), but never runs an experiment to confirm perfect recovery. Even under identical models, floating-point non-determinism, tokenization edge cases, rank ties, or subtle implementation differences could cause failures. This is the most basic sanity check for any steganographic method, and its absence makes it impossible to assess whether the protocol works reliably in practice.

- **No comparison with any prior LLM steganographic method**: The paper cites Ziegler et al. (2019), Kaptchuk et al. (2021, Meteor), Wu et al. (2024), and Zamir (2024) but provides no empirical comparison against any of them — not on stegotext quality, capacity, security, or computational cost. The reader cannot assess whether Calgacus is an improvement, a trade-off, or simply a different (and possibly weaker) approach. This is particularly problematic because the paper's claimed advantage ("full capacity") cannot be evaluated in context without baseline comparisons.

- **No human evaluation of stegotext naturalness**: The paper's central claim is that stegotexts are "coherent and plausible" to humans. The only evidence is LLM-assigned log-probabilities (which the paper itself acknowledges conflate many factors beyond naturalness) and qualitative examples. Given that the entire application scenario depends on human-imperceptibility of the steganographic channel, the absence of any human rating study is a significant gap.

### Minor
- **Limited evaluation scope**: The experiments use only one model size (Llama 3 8B), one text domain (Reddit posts truncated to 85 tokens), three source texts, and English only. There is no systematic variation of model size, key length, source text perplexity, text domain, or language. The paper acknowledges that "the quality of the result depends on e, k, and the LLM used" (line 148) but does not characterize these dependencies empirically.

- **Security analysis is informal and incomplete**: The paper explicitly declines to provide a formal security model (line 61: "we will avoid building a palace on the sand"), which is a reasonable scope choice. However, it still makes substantive claims about deniability and key security. The brute-force bound (O(d^{|k|})) is trivially true for any key-based scheme. The deniability claim rests on qualitative observations that some stegotexts have probabilities "in the same ballpark" as originals, without a rigorous definition of what constitutes deniability or an evaluation of how often this property holds.

### Trivial
None.

## Nice-to-Haves
- A reconstruction accuracy experiment confirming perfect recovery under ideal conditions (same model, key, and hardware).
- Human evaluation of stegotext naturalness (e.g., an A/B test where participants distinguish real texts from stegotexts).
- Comparison against at least one prior method (e.g., Meteor) on a shared metric.
- Systematic variation of model size (e.g., 1B, 8B, 70B), domain, and language.
- The paper could benefit from clearer positioning: if it intends to be a methods paper, the evaluation needs substantial strengthening; if a discussion/position piece with a demonstration, the title and framing should reflect this to match reader expectations.

## Removed Points
- **"Same length claim is misleading"** (Harsh Critic point 3): Removed because the paper clearly states "in terms of LLMs tokens" (line 19). The title is accurate for the technical claim, and the paper is transparent about using tokens. A reader who misses the qualifier may be misled, but the paper itself is not dishonest.
- **"Falls between two stools" framing criticism**: Moved to Nice-to-Haves as a constructive suggestion about positioning rather than a weakness of the paper's content.
- **Generic evaluation complaints lacking specific anchors**: Merged into the concrete points above (reconstruction accuracy, baselines, human eval, scope).

## Novel Insights
The paper's most novel observation is the reframing of hallucination as a "void of intention" rather than factual error — a philosophical argument that is both well-supported by the steganographic protocol and genuinely thought-provoking. The connection to Oulipo constraint literature (Perec's *La Disparition* written without the letter "e") is an insightful analogy for the constraint-satisfaction nature of LLM text generation, whether the constraint comes from steganographic rank-preservation or random sampling. These insights are intellectually valuable but largely independent of the specific Calgacus protocol — they could be made (and partially have been made elsewhere) without it.

## Suggestions
1. **Add reconstruction accuracy**: This is the single most important missing experiment. Report exact recovery rate across multiple texts, keys, and random seeds. If the method is deterministic (as described), confirm this empirically.
2. **Include at least one baseline comparison**: Compare against Meteor (Kaptchuk et al., 2021) or another cited method on a shared metric such as stegotext perplexity or capacity.
3. **Run a human evaluation study**: Even a small-scale study (e.g., 30–50 participants rating naturalness of real vs. stegotexts) would directly support the core plausibility claim.
4. **Expand the evaluation scope**: Add at least one additional model size and one additional text domain to characterize when the method works well and when it breaks.

## Score and Decision
Based on my analysis of the paper content: The core idea is genuinely clever and well-explained, and the discussion is intellectually stimulating. However, the experimental evaluation is substantially insufficient for a methods paper at a top conference. The three major weaknesses — no reconstruction accuracy verification, no baseline comparisons, and no human evaluation — combine to leave the paper's central claims empirically unsupported. The paper reads more as a position piece with a proof-of-concept demonstration than as a rigorous technical contribution.

I calibrate this as follows: a methods paper with adequate evaluation on this topic would score 6–8. A position paper making only conceptual claims might score 5–7. This paper sits between these frames but meets neither standard fully: it makes concrete technical claims ("simple and efficient protocol," "high-quality results") but does not support them with sufficient evidence. Among papers at this venue, this is a borderline reject — the idea merits development but the submission as-is does not meet the evidentiary bar for acceptance.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>