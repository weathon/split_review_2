Now I have the favorability signals. The strengths about the novel contribution score very high (0.93–1.00), while the evaluation weaknesses are rated very damaging (0.00–0.23). This confirms the paper has a genuine contribution but the evaluation is critically thin. Let me produce the final consolidated review.

## Summary

This paper presents Calgacus, a steganographic protocol that uses an LLM to encode an arbitrary text within a different coherent text of the same token length. The core idea — preserving token rank-order from one text while generating a different surface text under a different prompt — is simple and correct by construction: decoding is exact because rank(*e_i* | *e*_{<*i*}) = rank(*s_i* | *k*, *s*_{<*i*}) for every position. The paper demonstrates the method on 3 source texts drawn from a 1000-text Reddit corpus, showing that the log-probabilities of the resulting stegotexts fall within the distribution of real texts. It then discusses philosophical implications for authorship, hallucination, and AI safety, including a speculative scenario where an unfiltered LLM is covertly deployed through a compliant model's responses.

## Strengths

- **[Novel same-length capacity]** Calgacus is the first steganographic protocol achieving full capacity — the stegotext and the secret message have the same number of tokens. This is a genuine technical contribution, clearly stated and demonstrated (Section 3, Figure 3). The symmetry prevents one from distinguishing which text is authentic at first glance. (favorability: 0.93)

- **[Elegant rank-transfer mechanism]** The core idea is simple, correct by construction, and clearly explained. Decoding is exact by design. The paper's formal description (Figure 3) and the running example (hiding a Caesar critique in a boar recipe) make the concept immediately concrete. (favorability: 1.00)

- **[Transparent about limitations]** The paper explicitly acknowledges key limitations: no guarantee of coherence for arbitrary inputs (hash example), the requirement of bit-exact LLM across encoder/decoder, the need for padding tokens to avoid abrupt endings, and the defect of using log-probability as a plausibility measure. This awareness is to the authors' credit. (favorability: 0.96/0.91/0.54)

## Weaknesses

### Fatal
None.

### Major

- **Thin empirical evaluation.** The entire evaluation consists of log-probability analysis on only 3 source texts (selected at μ, μ-2σ, μ+2σ of the distribution), each generating 100 stegotexts, all at a fixed length of 85 tokens. There are three critical gaps: **(a) No human evaluation.** The paper asserts that stegotexts are "plausible to humans" and "remain opaque to humans" (lines 43, 132), but log-probability under an LLM is not a validated proxy for human plausibility judgments — even though the authors acknowledge this metric's defects, they still draw conclusions about human perception from it. **(b) No baseline comparisons.** The paper cites prior generative steganography methods (Ziegler et al., Kaptchuk et al., Wu et al., Zamir) but does not compare against any of them on any metric — not on stegotext quality, not on detection resistance, not on capacity, not on computational cost. This makes it impossible to assess whether Calgacus offers practical advantages beyond the theoretical same-length property. **(c) No systematic characterization of failure modes.** The paper gives one hash example but does not characterize how often failure occurs, for what kinds of source texts, or how to predict it. For a submission to ICLR, where empirical claims need solid support, this evaluation is substantially below what is needed to substantiate claims that the method works "effectively" (line 250). (favorability: 0.00–0.02)

- **The "disguised unaligned chatbot" scenario has an acknowledged but untested feasibility gap.** In the AI safety scenario (Section 4), the uncensored answer *u* from uLLM must be rank-encoded through the open model oLLM conditioned on the user request *c*. As the paper itself notes, oLLM "may not even know how to tamper a gas meter" — meaning the ranks of *u* under oLLM (given *c*) could be very high, which would make the stegotext *s* incoherent. The paper provides no analysis of when this scenario would actually work, what fraction of queries would succeed, or any end-to-end test. As presented, this remains a speculative thought experiment rather than a demonstrated concern. (favorability: 0.00–0.23)

### Minor

- **Claims about human plausibility go beyond the evidence.** The paper states that texts are "plausible to humans" (line 132) based solely on log-probability analysis. While the authors acknowledge the metric's limitations, they nonetheless draw conclusions about human perception without human-subject validation. The qualitative examples (Figure 1) are striking but anecdotal. (favorability: 0.00)

### Trivial
None.

## Nice-to-Haves

- A human evaluation study (e.g., asking participants to distinguish stegotexts from real texts) would directly address the paper's core concern about eroding trust in communication and would be far more impactful than the log-probability analysis.
- Baseline comparisons against prior generative steganography methods, even on the same log-probability metric, would help calibrate Calgacus's practical performance.
- Systematic characterization of success/failure across diverse source text domains, lengths, LLMs, and key properties would turn the acknowledged limitations into a quantitative understanding.
- The paper claims encoding/decoding takes "seconds on a laptop" (abstract); including runtime measurements would substantiate this.

## Removed Points

Points that were flagged for removal; treat with caution:
- **"Same-length property is less significant/misleading"** — Removed. The critic's argument about total communication cost applies to any steganographic protocol with a shared key. The same-length property refers to stegotext vs. secret text length parity, which is genuinely novel and correctly framed.
- **"Security analysis is superficial"** — Removed. The paper explicitly states it will not provide formal security guarantees (line 61). Within its self-declared scope, the security discussion covers key secrecy, brute-force bounds, and deniability qualitatively.
- **"No LLM-based detection experiment with ROC/precision-recall"** — Removed. The paper does present an LLM-based detection analysis (Figure 4, line 132) showing original texts have higher log-probability on average, and validates this across different LLMs (Phi-3 3.8B, Figure 14).
- **Various minor presentation/implementation nitpicks** — Removed as trivial or unsupported (missing tie-handling details, tokenizer discussion, delimiter questions). These do not affect the core contribution.

## Novel Insights

None beyond the paper's own contributions. The reviews identify the same fundamental trade-off the paper itself acknowledges: the method is elegant and correct, but the empirical evidence for its practical usefulness is thin.

## Suggestions

1. Strengthen the evaluation with at least one of: (a) a human study on stegotext plausibility, (b) quantitative comparisons against prior steganography methods, or (c) systematic failure-mode analysis across diverse source texts, lengths, and LLMs.
2. Either provide an end-to-end test of the chatbot-disguise scenario under realistic conditions, or explicitly reframe it as speculative discussion rather than a demonstrated threat.
3. Add runtime measurements to support the efficiency claim in the abstract.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>