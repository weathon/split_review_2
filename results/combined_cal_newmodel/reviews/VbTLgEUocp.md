Now I have all the information I need to produce the final review. Let me compile everything.

## Summary of Calibration Anchors

| Anchor | Avg Score | Round | Topical Relevance | Comparison to this paper |
|--------|-----------|-------|-------------------|--------------------------|
| OD-Stega (steganography) | 3.50 | R1 | High | More mathematical but less philosophical; similar evaluation gaps |
| Plausibly Deniable Encryption | 4.80 | R1 | High | More formal; has deniability application; lacked security definitions |
| Hidden in Plain Text (steg collusion) | 5.00 | R1 | High | More thorough experiments; novelty questioned; stronger evaluation |
| Sparse Watermarking | 3.00 | R1 | Medium | Watermarking, not steganography; narrower contribution |
| I Know You Did Not Write That (watermark) | 3.67 | R2 | Medium | Watermarking paper with similar evaluation breadth issues |
| Hiding Images in Diffusion Models | 4.75 | R1 | Medium | Different modality; comparable evaluation depth |

**Round 1 Bracket:** Based on the high topical similarity to OD-Stega (3.50) and Plausibly Deniable Encryption (4.80), the paper sits in the 3.0–5.0 range.

**Narrowing (Round 2):** Comparing itemized favorabilities:
- The paper's strengths (11.84, 13.78) are stronger than OD-Stega's (10.60–12.23) and competitive with Plausibly Deniable Encryption's (10.81–12.38)
- The paper's weaknesses (−1.97 to 0.00 for majors) are comparable to OD-Stega's (−2.21 to +4.99) but the paper has NO positive-major weaknesses dragging it up
- The lack of baselines, detection experiments, human eval, and narrow source-text scope are verified gaps that place it below Plausibly Deniable Encryption (4.80) which at least had extensive evaluation

**Final Score: 4.0** — The paper has genuine intellectual merit (elegant method, unique philosophical contribution) but the experimental evaluation is insufficient for ICLR. The method's core correctness is not in question, but the evidence for practical viability is too thin.

Now let me write the final review.

Let me be careful about the removed points section. Let me trace through:

1. The circularity criticism: I weakened this because the paper cross-validates with Phi-3. So it's partially addressed but the remaining concern is captured in "no human evaluation."

2. The appendix references: removed per rule.

3. The implementation details criticism: removed per rule (nitpick about reproducibility).

4. The "well-written" strength: I removed it per rule about generic strengths.

5. The section-by-section notes: mostly merged into existing weaknesses or removed.

6. The "missing parts" about reproducibility info: removed per rule about nitpicks.

7. The "same length desirability" question: removed per rule about speculation.

Let me also verify: the harsh critic's criticism about "no detection experiment" - is this accurate? The paper says (line 132): "while for a human both the original and fake texts are plausible, generally the original text can be discerned from its stegotexts by picking the most probable one according to a LLM." And "We verified this statement also using LLMs different from the one used to generate the stegotexts. For instance, the same probability shifts between real and fake texts can be observed when using Phi-3 3.8B in Figure 14."

So the paper claims LLMs can distinguish originals from stegotexts by comparing log-probability, and verifies this with a different model. But this is not a formal detection/classification experiment (no ROC, no accuracy metric). The reviewer is correct that no detection experiment is performed in the standard sense.

Actually wait - I should double-check one thing. Let me re-read the security section more carefully about the "shipping unfiltered LLMs" scenario. The reviewer said "the key t is transmitted in plain sight alongside s. This means any auditor monitoring the channel also has t, and can therefore extract u."

Let me re-check: Act 4 says "The USER receives on the chatbot platform the censored answer to their query c, which includes the reasoning trace t and the actual answer s."

The key is t. The user receives t as part of the response. An auditor monitoring the channel would see t too. With t and s, the auditor can extract u.

But wait - the company's defense is "the user just made an unconventional choice for their sampling strategy." This means the company claims the user, not the company, generated u on their local machine. The company provided s, which was generated normally by oLLM (the "safe" model). The user then (on their own machine) used the ranks from s to extract u from oLLM.

But this defense only works if the auditor believes the user was the one who chose the sampling strategy. The auditor can see that s was the output from the company, and that s's token ranks correspond to u when decoded. The question is: who generated s? If the company generated s, then the company encoded u in s. The company's defense is that the USER chose the weird sampling strategy, not them.

Actually, re-reading more carefully: Act 3 says "the COMPANY embeds u in s: by obtaining the oLLM ranks of u after k' = c, and then generating s following that same ranks after k = t."

So the COMPANY generates s with u embedded. Then the USER receives s and t.

The company's defense (Comment 1): "the company can argue that u was obtained by the user on their machine through the open-source model addressing the request the user made. LLMs only provide token probabilities, and should be completed by a sampling policy when used for text generation."

This defense seems to claim that the USER could have independently generated u on their machine by using the ranks from s. But the ranks from s come from s, which the company generated. So the defense is circular - the company generated s with the encoding, then claims the user decoded it themselves.

Hmm, actually I think the defense is more subtle: the company could claim they generated s using oLLM with standard sampling (not rank-based). Then the user, independently, chose a non-standard sampling strategy on their local oLLM to extract u from s. The company could say "we didn't encode anything; that's just what oLLM generated."

But this is a weak defense because to extract u, you need to know the ranks, which requires knowing k (t). Since t was part of the response, the auditor can verify: do the ranks of s after t correspond to u? If yes, u is encoded in s.

The fact that t is public means anyone with the right tools can extract u. The company can claim plausible deniability, but the auditor can still detect the presence of hidden information. So the reviewer's point is valid but the paper's defense partially addresses it through plausible deniability rather than security against detection.

I'll keep this as a minor weakness. 

Now let me write the final review.Now let me write the final review.

## Summary

This paper presents **Calgacus**, a simple protocol that uses an LLM to hide an arbitrary text inside a different coherent text of the same length. The method works by recording the rank (position in sorted probability) of each token of the secret message, then generating the stegotext by selecting tokens at those same ranks under a different prompt (the secret key). The paper also develops a thoughtful philosophical discussion arguing that this protocol reveals LLM text generation as extreme constraint satisfaction, and reconceptualizes hallucination as a failure of attributed intention rather than factuality.

## Strengths

- **The Calgacus protocol (Section 3) is genuinely simple and elegant:** record the rank of each token of the original text under the LLM, then generate the stegotext by selecting tokens at those same ranks under a different prompt. The full-capacity property (stegotext and secret message same length) follows naturally from the design. The method's correctness is immediate from the construction.

- **The philosophical discussion (Sections 4–5) is thoughtful and well-grounded:** the argument that the protocol exposes LLM text generation as extreme constraint satisfaction, and the reconceptualization of hallucination as a failure of attributed intention rather than factuality, is genuinely thought-provoking. The connection to Oulipo (Perec's novel written without 'e') is apt and illuminating, and the "Shipping unfiltered LLMs" scenario provides a compelling concrete application.

## Weaknesses

### Major

- **Limited experimental scope:** The main quality evaluation (Figure 4) uses only 3 original texts, all drawn from a single source (Reddit). Lines 130–131 state: "We take three texts from the 1000 to produce 100 stegotexts for each with our method." The method's claim to hide "any meaningful text" (abstract) within a "coherent and plausible" cover is not tested across diverse genres, lengths, or topics. The boundary of when the method works versus when it fails (as with the hash example in Section 3) is not systematically characterized.

- **No human evaluation of stegotext coherence:** The paper repeatedly asserts that stegotexts are "plausible" and "coherent" (abstract, Section 3, Conclusions) and states "While remaining opaque to humans" (line 43), but provides no human ratings, fluency judgments, or pairwise preference tests. The only quantitative evidence is LLM-assigned log-probability. Even though the paper cross-validates with a different model (Phi-3, Figure 14), this does not substitute for human judgment — especially when the core claim is about stegotexts being indistinguishable from human-written text to human readers.

- **No comparison to baseline steganographic methods:** The paper cites Ziegler et al. (2019), Kaptchuk et al. (2021), and others in Related Work (line 67) but conducts no experimental comparison. Without baselines, the practical significance of the full-capacity property — whether it comes at a meaningful cost in coherence, detectability, or throughput relative to existing approaches — cannot be assessed. The paper correctly notes its method differs on the "same-length" property, but never measures the trade-offs.

- **No detection/classification experiment:** The paper claims that "LLMs can uncover a distinction between original texts and most of their encoded counterparts" (line 43, line 132), but this claim rests only on visual inspection of distribution overlap in Figure 4. No ROC curve, classifier accuracy, or formal detection experiment is performed. The paper also notes this property could be exploited by an adversary, yet provides no quantitative characterization of how detectable the stegotexts actually are.

- **Security analysis is informal and incomplete for a steganographic protocol:** The security section (lines 150–166) consists of only two short paragraphs. The brute-force complexity bound O(d^|k|) (line 154) assumes k is uniformly random across the token vocabulary, when in practice k is natural language with far lower entropy. The paper acknowledges this concern but does not quantify the reduced search space. There is no discussion of statistical detectability beyond log-probability (e.g., rank distribution artifacts, n-gram statistics, or model-specific features an adversary could exploit). For a protocol presented as a steganographic method with security claims, this analysis is insufficient.

### Minor

- **Deniability argument conflates probability with message plausibility:** Line 166 argues that deniability follows from stegotexts having log-probabilities in the same range as originals. But deniability requires that a wrong key yields a *plausible alternative message*, not just one with comparable probability. These are different criteria, and the argument as stated is too weak.

- **Shipping unfiltered LLMs scenario has a logical tension:** In the scenario (lines 197–198), the secret key t (the reasoning trace) is transmitted as part of the visible response. Any auditor monitoring the channel who has t, s, c, and oLLM can extract u. The company's plausible-deniability defense (Comment 1, line 205) mitigates this but does not fully resolve the tension with the claimed application.

### Trivial

None.

## Nice-to-Haves

- A systematic evaluation across diverse text types, lengths, and genres to characterize the method's success/failure boundary.
- A human evaluation study (fluency ratings or pairwise preference) to validate the claim that stegotexts are coherent to human readers.
- Experimental comparison to at least one baseline steganographic method (e.g., Ziegler et al. 2019, Kaptchuk et al. 2021).
- A formal detection experiment (e.g., ROC-based LLM classifier) rather than relying on visual distribution overlap.
- Quantitative security analysis accounting for natural-language key entropy.
- Analysis of whether the same-length property creates detectable statistical signatures (e.g., unusual length distributions).

## Removed Points

These points are flagged to be removed; treat them with caution:

- **Log-probability circularity as a fatal flaw** — The harsh critic claimed using the same LLM family for generation and evaluation is "methodologically circular." However, the paper cross-validates with Phi-3 (Figure 14), partially addressing this. The remaining concern (absence of human eval) is captured above. Removed as overclaimed.
- **Missing appendix content** (Figures 13, 14, 15, Appendices A.1, A.2, A.5) — Removed per rules: the parser strips these sections from all papers.
- **Reproducibility implementation details** (quantization, GPU architectures) — Removed per rules: nitpicks about trivial implementation details.
- **Whether same-length property is desirable in practice** — Removed as speculation about potential adversarial reactions, not a verified methodological weakness.
- **"Well-written and engaging" as a strength** — Generic, removed per rules. Specific aspects (lively prose, apt references) are subsumed by the retained strengths.
- **Abstract overclaiming re: hash counterexample** — Already covered by the limited experimental scope weakness.

## Novel Insights

None beyond the paper's own contributions. The reviews raise valid concerns about evaluation depth but do not surface methodological insights the paper itself does not identify.

## Suggestions

1. Add a systematic evaluation across diverse text types, lengths, and genres to characterize when the method succeeds and when it fails.
2. Conduct a human evaluation study (fluency ratings or pairwise preference between stegotexts and natural text) to directly validate the claim that stegotexts are coherent to human readers.
3. Add experimental comparisons to at least one baseline steganographic method (e.g., Ziegler et al. 2019, Kaptchuk et al. 2021) to contextualize the full-capacity property against existing trade-offs.
4. Run a formal detection experiment (e.g., ROC analysis for an LLM-based classifier) rather than relying solely on visual distribution overlap.
5. Strengthen the security analysis with quantitative treatment of the key space (accounting for natural-language entropy) and discussion of statistical detection channels beyond log-probability.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>