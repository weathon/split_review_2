## Summary

This paper presents *Calgacus*, a protocol for LLM-based steganography that hides a meaningful text *e* inside another text *s* of the same length. The method is simple: record the token ranks of *e* under an LLM, then generate *s* from a different prompt by selecting tokens at those same ranks. The paper demonstrates the protocol on three Reddit posts using Llama 3 8B, discusses security, and devotes substantial space to philosophical implications for LLM knowledge, hallucination, and authorial intent.

---

## Strengths

1. **The core idea is genuinely clever, simple, and correct.** The Calgacus protocol — recording token ranks from one text, then generating a new text that respects those ranks under a different prompt — is elegant in a way that is rare. It is described in a few lines (lines 96–108) and clearly "works" in the examples shown. The simplicity itself is a strength: the method can be understood, implemented, and deployed by anyone with access to an open-source LLM.

2. **The "full capacity" property is a clean, nontrivial advance over prior work.** Existing LLM-based steganography embeds secret bits within generated text, typically expanding length. Calgacus instead achieves a one-to-one token mapping between secret and stegotext, so both are the same length (line 67). This is distinguished clearly from prior methods (Meteor, Wu et al., Zamir) and matters both practically (a tweet hiding a tweet) and conceptually.

3. **The "low entropy token choices" explanation for why stegotexts are less probable than originals (lines 134–146) is precise and insightful.** The paper identifies the mechanism: rank-1 tokens in the original are "wasted" at positions where the stegotext tokens have much lower intrinsic probability, driving down overall plausibility. This is a genuine mechanistic insight, not just an empirical observation.

---

## Weaknesses

### Fatal

None.

### Major

1. **The evaluation is substantially thinner than the claims require.** The paper claims the protocol can hide "an arbitrary meaningful text" (line 17). The experiments test this on exactly *three* source texts (line 130) — all 85-token English Reddit posts, all evaluated under a single LLM (Llama 3 8B) for the headline plausibility figure (Figure 4). One hundred stegotexts are generated per text, but the variation is in the prompt *k*, not in the secret message *e*. No confidence intervals, significance tests, or variance estimates are reported anywhere. Three texts do not support the breadth of the paper's claims about the protocol's general applicability.

2. **The main plausibility evaluation is circular.** Figure 4 uses Llama 3 8B to evaluate the log-probability of stegotexts that were generated *by* Llama 3 8B. That the generating model finds its own outputs plausible relative to human-written text is not strong evidence of human-level plausibility. The paper mentions a cross-check with Phi-3 (line 132, Figure 14 in the appendix), which partly addresses this, but the headline evidentiary figure has this circularity issue.

3. **Key security claims are stated without supporting evidence.** Two specific claims are asserted rather than demonstrated:
   - *"Inserting a simple random string in k is enough to nip [the key-recovery attack] in the bud"* (line 164) — no analysis of required string length, no empirical test, no discussion of how an attacker might exploit structure in *s* to narrow the search.
   - *Deniability* (line 166) — the claim that outlier prompts produce stegotexts "in the same ballpark" of probability as the original is stated qualitatively. No quantification of how many such prompts exist, or what fraction of wrong keys produce plausible-looking secrets.

### Minor

4. **No statistical reporting.** The paper reports no confidence intervals, significance tests, or distributional overlap metrics (e.g., KL divergence) for any of its quantitative claims. The histograms in Figure 4 are visually useful but do not quantify how well the stegotext and real-text distributions overlap.

5. **Tokenization mismatch is underdiscussed as a practical constraint.** The paper notes (line 148) that sender and receiver must run the chosen LLM under identical conditions. But if the encoder and decoder use different software versions, GPU architectures, or inference settings that affect logit computation, the ranks will differ and the message will be unrecoverable. This is a significant operational limitation that deserves more attention.

6. **The "shipping unfiltered LLMs" scenario mixes technical protocol with legal/practical argument without clear separation.** The scenario (lines 180–206) is provocative, but the deniability it relies on is legal/practical (the company could *argue* the user chose an unconventional sampling policy, line 205), not cryptographic. The paper does not analyze the fragility of this deniability under subpoena, traffic analysis, or forensics. The protocol's technical capabilities and the legal plausibility of the denial are presented in the same register, which may overstate the practical robustness.

### Trivial

None.

---

## Nice-to-Haves

- **Systematic ablation on *k* quality.** The paper mentions that *k* steers the stegotext, but does not study how the method degrades with vague, short, or poorly chosen prompts.
- **Human evaluation.** Even a small-scale plausibility rating study would substantially strengthen the claim that stegotexts are plausible "to humans" (line 43 states this outright, but no human evaluation is conducted).
- **Quantify the deniability claim.** For a given stegotext *s* and many candidate keys (including real *k* and many decoys), what fraction of wrong keys produce plausible-looking *e*? This is directly answerable with the paper's own framework.

---

## Removed Points

- *Appendix unavailability complaint* (from Critical Issue 2): The reviewer noted they could not evaluate Figure 14 because the appendix was not included. Per policy, the appendix exists in the original submission; this criticism is removed.
- *Informal reference concern* (from "Missing Parts"): The reviewer questioned the stability of references "(Akn, 2025)" and "(Trimness8, 2025)". Per policy, cited references are assumed to exist and be released; this criticism is removed.
- *Hash example not reproducible* (from "Missing Parts"): The reviewer claimed the hash example (line 122) is not reproducible without knowing the exact *k*. In fact, *k* is specified as "the same culinary prompt of Figure 1." This criticism misunderstands the paper and is removed.
- *Strength about addressing an important problem* (from input): Several generic strengths were implicit in the review's framing rather than stated explicitly. Only the three concrete, evidenced strengths above are retained.

---

## Novel Insights

The harsh review's most valuable observation beyond the paper's own content is the structural critique of how the paper's broad claims (about "any" text, about deniability, about the shipping scenario) are not proportionally supported by evidence. This is not a failure of the method but a gap between the paper's rhetorical register and its empirical basis. The reviewer also correctly identifies that the "low entropy token choices" insight could itself be used to design better evaluations — a point the paper does not exploit.

---

## Suggestions

1. **Broaden the evaluation** to at least 30–50 source texts across different genres, lengths, and languages to support the claim of general applicability.
2. **Break the circularity** in the plausibility evaluation by putting a cross-model evaluator (or human raters) in the main paper, not just in the appendix.
3. **Quantify the two unsupported security claims**: estimate the random-string length needed to frustrate structured key-search, and measure the fraction of decoy keys that produce plausible secrets.
4. **Add basic statistical reporting** — confidence intervals or bootstrap estimates for the overlap between stegotext and real-text distributions in Figure 4.

---

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>