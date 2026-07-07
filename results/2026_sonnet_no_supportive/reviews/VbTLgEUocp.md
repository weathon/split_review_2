Now let me draft the review and call draft_review.Now let me do one narrowing pass to read the two most topically similar anchors.## Summary
Calgacus is a steganographic protocol that exploits LLM rank sequences to achieve token-for-token length-preserving hiding of a secret text *e* inside a cover text *s*. The key insight: record the rank of each token of *e* under an LLM's conditional distribution, then generate *s* from a secret key prompt *k* by selecting, at each step, the token at that rank. Recovery is the exact inverse. The paper demonstrates that stegotexts fall within the log-probability distribution of real Reddit posts, discusses deniability and security, and proposes an AI safety application in which an unfiltered LLM's answers can be embedded in compliant responses.

## Strengths
- **Elegant, lossless bijection**: The rank-based encoding is simple, implementable in an evening, achieves exact token-length preservation, and runs on 8B open-source models on commodity hardware. Prior methods such as Meteor produce longer stegotexts in low-entropy regimes; Calgacus avoids this by construction.
- **Honest empirical evaluation (Figure 4)**: Stegotexts from three anchor texts (at μ, μ−2σ, μ+2σ of the Reddit distribution) all fall within the log-probability distribution of 1,000 real Reddit posts, while random ASCII and random-English-word strings fall far outside. The authors are transparent that originals are on average more probable than their stegotexts.
- **Substantive deniability argument (Section 3.1)**: The observation that some key prompts yield stegotexts "in the same ballpark" as the original, combined with the formal notion of sender deniability under coercion (Canetti et al., 1997), is a real security property, not hand-waving.

## Weaknesses

### Fatal
None.

### Major
- **LLM-detectability is a structural limitation that is acknowledged but not characterized**: Section 3 and Figure 4 jointly establish that stegotexts are statistically distinguishable from authentic text by any LLM running a log-probability test—without knowledge of the key. The paper explains the mechanism precisely: low-entropy token choices are "wasted" on non-top-1 tokens ("a low-entropy token choice...the likelihood of having a rank 1 does not reflect the token's intrinsic probability"), systematically depressing stegotext log-probabilities. The paper then pivots to deniability rather than characterizing *when* the gap is small enough that detection fails. For a steganography paper, the absence of any characterization of the regimes where stegotexts are statistically indistinguishable from authentic text is a significant gap. The comparison to Zamir (2024), whose method does not modify the LLM's response distribution and therefore evades this attack entirely, is made in one sentence with no security-theoretic discussion.

### Minor
- **Imprecise use of "full capacity"**: The paper distinguishes itself via "full capacity: the stegotext and the secret message being of the same length." In information-theoretic steganography, capacity refers to bits per symbol of channel output—a quantity Calgacus does not characterize. What the method achieves is *token-length preservation*. This is real and useful, but calling it "full capacity" invites misreading and the paper does not provide a formal argument for why prior methods cannot also achieve length preservation.
- **AI safety threat model overstated**: The "Shibbolethian Theatre" in Section 4 requires the user to (a) know the Calgacus protocol, (b) run the exact same oLLM locally, and (c) correctly identify the reasoning trace *t* as the key. The framing suggests this challenges AI safety oversight ("regulators would be deceived"), but the scenario as written is a co-conspiracy between the company and a colluding user—not a deception of external oversight. The paper notes "the company can argue that *u* was obtained by the user on their machine," but this argument requires the user's active participation. The threat is real as a circumvention protocol, but the paper should distinguish the oversight threat (company behavior) from the user-collusion assumption.
- **Hardware reproducibility impact unquantified**: The Limitations paragraph states "sender and receiver must run the chosen LLM under identical conditions...This may be a challenge when using different GPU architectures (Shanmugavelu et al., 2024)." The practical decoding error rate across GPU architectures is not measured, leaving the question of whether the protocol is practically usable across heterogeneous hardware unanswered.

### Trivial
None beyond what is noted above.

## Nice-to-Haves
- Measure the log-probability gap as a function of the entropy of *e* and identify regimes where detection is hardest. This would identify the strongest operating point for Calgacus and convert a limitation into a positive result.
- An end-to-end demonstration of the gas-meter scenario (Figures 11–12 are mentioned but not included in the parsed text) with decoding accuracy measured across key prompt variations would materially strengthen Section 4.
- A comparison clarifying why prior methods cannot simultaneously achieve token-length preservation and distributional indistinguishability, or whether a hybrid is possible.

## Removed Points
*These points are flagged to be removed, treat them with caution:*

- **Abstract "radical decoupling" overpromises**: The harsh critic argues the paper "fulfills only partially" the framing. In fact, the method delivers a concrete rank-bijection that genuinely decouples text from authorial intent. Not a real weakness; removed.
- **Demand for broader empirical evaluation (more LLM sizes, domains, entropy levels)**: Reasonable as a nice-to-have but not a structural flaw in a first-presentation paper; demoted.
- **Philosophical discussion on hallucinations is loosely connected**: The harsh critic notes the redefinition of hallucination is "loosely argued." This is fair but the paper explicitly frames Section 4 as a discussion, not a formal claim. This is a tone criticism, not a scientific flaw; removed.
- **Missing end-to-end AI safety demonstration**: Figures 11–12 are cited in the paper body; the parsed version strips them. Per instructions, removed.

## Novel Insights
Calgacus reveals a structural observation that applies to all autoregressive LLM generation: sampling from an LLM is itself a form of rank-constrained token selection, where the "constraint" is a random seed. Replacing that random seed with the rank sequence of an unrelated meaningful text is a minimal perturbation of the generation algorithm—and yet the result is a fully coherent stegotext. This has an interesting implication: any autoregressive model with full vocabulary access can, in principle, be repurposed as a steganographic channel without any training or fine-tuning. The Oulipo analogy in Section 4 is apt—just as constraint-driven literature produces semantically valid text under an arbitrary formal constraint, an LLM's rank mechanism produces valid stegotexts under the constraint of encoding an unrelated message. This connection between the theory of constrained writing and the mechanics of autoregressive generation is genuinely novel.

## Suggestions
- Add a figure or table showing the log-probability gap between stegotext and original as a function of the per-token entropy of *e*. This would identify the "safe regime" for Calgacus and directly address the detectability concern.
- Replace "full capacity" with "token-length preservation" throughout, with a note clarifying that this means one token of *e* maps to exactly one token of *s*—a weaker property than information-theoretic channel capacity but practically valuable.
- In Section 4, clarify that the "Shibbolethian Theatre" threat is a company-user co-conspiracy that circumvents oversight from the perspective of regulators inspecting company outputs, not deception of users.

---

## Anchor Summary and Score Calibration

**Round 1 — Bracketing**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|-----------|
| 5kMwiMnUip.md | 1.40 | R1 | LLM jailbreaking survey — far weaker, no novel method |
| 8QTpYC4smR.md | 1.00 | R1 | Generic LLM review — not comparable |
| jbfDg4DgAk.md | 3.00 | R1 | Sparse watermarking — incremental, less novel than Calgacus |
| z3DMFpaP6m.md | 3.00 | R1 | LLM entropy semantics — unrelated topic |
| DsMxVELk3K.md | 3.00 | R1 | Text compression — unrelated |
| KBixkDNE8p.md | 3.00 | R1 | LLM psychology — unrelated |
| **urQi0TgXFY.md** | **5.00** | **R1** | **Steganographic collusion in LLMs — most topically similar; rejected at ICLR; more empirically thorough but more complex** |
| **7suavRDxe8.md** | **4.80** | **R1** | **Plausibly deniable encryption with LLMs — close in spirit; rejected; had fundamental crypto flaws** |
| eKGEsFdpin.md | 3.67 | R1 | LLM watermarking — less novel |
| 0KHW6yXdiZ.md | 5.25 | R1 | End-to-end LLM watermarking — more empirically grounded |
| LdIlnsePNt.md | 6.00 | R1 | Watermarking with theory — strong theoretical analysis, borderline |
| E4LAVLXAHW.md | 7.00 | R1 | Black-box detection of watermarks — rigorous, accepted |
| 9k0krNzvlV.md | 5.75 | R1 | Watermark learnability — accepted, good theory |
| jlhBFm7T2J.md | 6.50 | R1 | Undetectable image watermark — strong security guarantee |
| j7b4mm7Ec9.md | 7.60 | R1 | Deep watermarking — solid engineering contribution |

**Round 1 bracket**: The two most topically similar papers (steganography/deniable encryption with LLMs) scored 5.0 and 4.8 and were rejected. Accepted papers in this space (watermarking with security theory) score 6–7, with substantially stronger formal security analysis. **Initial bracket: 4.5–6.0.**

**Round 2 — Narrowing**: Calgacus is more elegant and cleanly presented than urQi0TgXFY (5.0) and does not have the fundamental crypto flaws of 7suavRDxe8 (4.8). However, it lacks formal security analysis (e.g., does not characterize the detection-resistant regime), and the core steganographic property (distributional indistinguishability) is not achieved. Compared to the accepted papers in the 6–7 range, which all provide either rigorous statistical theory or comprehensive empirical defenses, Calgacus falls short. The contribution is real but the security gap is a meaningful weakness for a steganography paper presented at ICLR.

**Final score: 5.0 (borderline reject)**

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>