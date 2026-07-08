Now I have sufficient calibration data. Let me produce the final consolidated review.

## Summary

This paper presents Calgacus, a steganographic protocol that uses LLMs to hide a text within another text of the same length. The method is strikingly simple: tokenize the secret message, record each token's rank in the LLM's probability distribution, then generate the stegotext by selecting tokens at those same ranks from a different context (the secret key). This achieves "full capacity" — the stegotext is exactly as long as the secret message, a property not shared by prior LLM steganography methods. The paper also includes an extended philosophical discussion reframing hallucinations as a void of intention rather than a failure of factuality.

## Strengths

- **The core idea is genuinely simple and elegant.** The method (§3) is described clearly: tokenize the secret message, record token ranks in the LLM's probability distribution, then generate the stegotext by selecting tokens at those same ranks from a different context (the key). This simplicity means the protocol can be implemented trivially on top of any LLM that exposes logits. **[weight=9.55]**

- **The "full capacity" property is genuinely novel.** Prior LLM steganography methods (Kaptchuk et al., 2021; Wu et al., 2024; Zamir, 2024) embed bits by modulating token sampling strategies, which typically shorten the available capacity or require multiple tokens per bit. The stegotext being exactly as long as the secret message (in tokens) is a non-trivial property. **[weight=9.38]**

- **The philosophical discussion (§4) is genuinely thought-provoking.** The reframing of hallucination as "a void of intention" rather than a failure of factuality, the comparison to Oulipo constraints, and the GEB-inspired Figure 6 are well-written and provocative. This is a genuine secondary contribution, even though it is not the paper's main deliverable. **[weight=10.18]**

## Weaknesses

### Fatal
None.

### Major

- **No human evaluation of the paper's central claim.** The paper repeatedly asserts that stegotexts are "coherent," "plausible," and "meaningful" to human readers (abstract, §1, §3), but provides no human evaluation. The only quantitative evidence is Figure 4, which shows that cumulative log-probability assigned by Llama 3 8b to stegotexts falls within the range of log-probabilities assigned to real Reddit posts. The paper itself notes (end of §3) that LLMs can *distinguish* original from fake by their probability, and acknowledges (footnote on log-probability limitations) that this proxy measure has known defects ("a difficult position to hold even for reviewer 2"). The Figure 1 examples are cherry-picked illustrations, not a systematic evaluation. This is the most significant evidential gap: the core claim — that Calgacus produces texts that appear natural and unremarkable to humans — is not backed by human-subject evidence. [weight=-2.07]

- **No experimental comparison to any baseline.** The related work (§2) discusses several existing LLM steganography methods (Ziegler et al., 2019; Kaptchuk et al., 2021; Wu et al., 2024; Zamir, 2024). The paper distinguishes itself via the "full capacity" property, but provides no head-to-head comparison of stegotext quality, decoding accuracy, or detection resistance. Without baselines, it is impossible to assess whether the full-capacity property comes at a meaningful cost to quality, security, or robustness. [weight=-3.26]

- **Extremely limited experimental scope.** The evaluation (§3, Figure 4) uses only 3 original texts (selected at μ, μ−2σ, μ+2σ from the Reddit distribution), 1 fixed length (85 tokens), 1 LLM for the main result (Llama 3 8b, with Phi-3 3.8B mentioned for one additional check in the appendix), and 1 dataset (Reddit posts). There is no systematic variation of text type (narrative, technical, poetic, code, multilingual), length, or LLM family/scale. The paper acknowledges that some texts (e.g., hashes) produce gibberish but never quantifies the failure rate. For a method paper whose central claim is that it "works effectively" (§5), the experimental foundation is too narrow to support the generality of the claims. [weight=-1.82]

### Minor

- **Security analysis is informal and lacks quantitative support.** Section 3.1 on security is essentially a paragraph of informal reasoning: brute-force key search bound (O(d^|k|)), a note that the attacker could reduce the search space, a suggestion to add a random string to k, and a deniability argument. There is no attack experiment, no formal security model, and no quantitative security bound. The paper states upfront that it will avoid formal steganographic models (§2), so this is partly by design, but the claims about security and deniability would benefit from experimental verification. [weight=+2.39 — the model considers this a positive aspect, likely because the paper pre-emptively acknowledges its limited security framing.]

### Trivial
None.

## Nice-to-Haves

1. **Human evaluation study** (e.g., AMT or Prolific) where raters judge coherence/naturalness of stegotexts vs. real texts without knowing which is which. This directly tests the paper's foundational claim.
2. **Expand experimental scope**: vary text length (50–500+ tokens), try more LLMs (especially smaller models the paper touts), report success/failure rates across a larger and more diverse set of texts from different genres.
3. **Baseline comparisons** to at least one prior method (e.g., Kaptchuk et al. 2021 or Zamir 2024) on stegotext quality and capacity.
4. **Timing measurements** to support the efficiency claim ("seconds on a laptop").
5. **Security experiments** (attempt to detect or decode stegotexts without the key).

## Removed Points

These points are flagged to be removed — treat them with caution:

- **Deployment scenario criticism (Critical Issue #5)**: The reviewer claimed that if both the reasoning trace t and the stegotext s are public, anyone can recover the hidden message. However, the paper's "Comments" section (§4) explicitly addresses this through a deniability argument — the company can claim the unfiltered output was produced by the user's own machine via an unconventional sampling strategy. This is presented as plausible deniability, not secrecy, so the criticism conflates the paper's own framing. Removed because the paper already addresses this concern.
- **Overclaimed "arbitrary topic and style"**: The conclusion uses this phrase, which is standard summary language. The method is indeed steerable via the key k, and the paper acknowledges limitations. This is too minor to retain as a weakness.
- **Missing timing measurements**: Not a core claim; the paper states efficiency but doesn't provide tables. A nice-to-have, not a weakness.
- **Reproducibility concern about logit-level reproducibility**: The paper explicitly acknowledges this in the Limitations paragraph (§3).
- **Generic section-by-section notes** (e.g., "related work reads like a textbook"): These are style preferences, not substantive weaknesses.
- **Strength about "addressing an important problem"**: Generic; removed as insufficiently specific.
- Some reviewer framing about the paper being "not a real method paper" due to discussion-heavy structure: This is a genre preference, not a weakness. The paper's contribution is both the method and the discussion.

## Novel Insights

None beyond the paper's own contributions. The harsh review's most valuable insight is identifying the gap between the paper's plausibility claims and the absence of human-subject evidence — a gap the paper itself partially acknowledges but does not close. The observation that the paper's experimental scope is too narrow for its claimed generality is also well-taken but not surprising given the paper's stated focus on introducing the concept and its implications.

## Suggestions

1. Add a human evaluation study (e.g., AMT or Prolific) where raters judge the coherence/naturalness of stegotexts vs. real texts. This is the single highest-leverage improvement because it directly tests the paper's central claim.
2. Expand experimental scope: vary text length, try more LLMs (including the smaller models the paper touts), report success/failure rates across a larger and more diverse set of texts from different genres.
3. Add baseline comparisons to at least one prior LLM steganography method.
4. Provide timing measurements to support efficiency claims.
5. Add a basic security experiment (attempting to detect or decode stegotexts without the key).

---

**Calibration Report**

Round 1 bracket: I identified this paper as plausibly sitting in the 5–7 range based on its novel method but limited evaluation.

Round 2 anchors (itemized):

| Anchor | Path | Avg Score | Round | Itemized | Comparison |
|--------|------|-----------|-------|----------|------------|
| "Hidden in Plain Text" | urQi0TgXFY.md | 5.00 | 1 | Yes | Steganography in LLMs. Strengths ~7-9, weaknesses ~-4 to -5. My paper's strengths are higher (~9-10) and negatives milder (~-2 to -3). |
| "Plausibly Deniable Encryption" | 7suavRDxe8.md | 4.80 | 1 | Yes | Also LLM+steganography. Very high strengths (7-12) but severe fatal flaws (-7, -6). My paper lacks such severe negatives. |
| "Sparse Watermarking" | jbfDg4DgAk.md | 3.00 | 1 | Yes | LLM watermarking. Lower strengths and more severe negatives. My paper is clearly stronger. |
| "Controlled Text Gen via LM Arithmetic" | SLw9fp4yI6.md | 7.00 | 2 | Yes | Method paper with strong evaluation. Strengths 8-12, weaknesses mostly positive-weighted. My paper's weaknesses are more negative. |
| "ProtoLLM" | kymuzakf7V.md | 5.67 | 2 | Yes | Method paper. Strengths ~6-10, weaknesses -4 to +6. My paper's strengths are higher and negatives milder. |
| "LLM Censorship" | lr806pdNZa.md | 4.50 | 2 | Yes | Theoretical/position paper. Strengths 7-11, weaknesses -5 to +6. My paper is more empirical but also more limited in scope. |

**Weighted-item comparison**: My draft's three strengths have very high weights (9.38–10.18), comparable to the accepted 7.0 paper (8–12). My major weaknesses have moderate negative weights (-1.82 to -3.26), which are more negative than the accepted 7.0 paper's weaknesses (mostly positively weighted) but less severe than the rejected 5.0 paper's (-4 to -5) or the 4.8 paper's (-6 to -7). The absence of fatal-weight negatives (no -5 or below) is notable.

The critical difference from the 7.0 paper is that its weaknesses were mostly positively weighted by the model (suggesting they were minor or well-handled), while my paper has clear negative-weight weaknesses. This places the paper below 7.0 but above 5.0 — in the 5.5–6.5 range.

## Score and Decision

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>