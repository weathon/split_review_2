Now let me finalize the review with the calibration data.

## Final Review

**Round 1 Bracket:** Based on calibration search, the narrowest plausible score range for this paper is between **4.0 and 5.5**. The paper has a genuinely novel core idea that places it well above strong-reject-level papers (1.0–1.5, which tend to be surveys or non-functional proposals). Compared to "Hidden in Plain Text" (score 5.00, Reject) — which had more thorough experiments but a less novel core idea — our paper has a more original contribution but thinner evaluation. Compared to "Sparse Watermarking in LLMs" (score 3.00, Reject) — which lacked novelty and had missing baselines — our paper's core idea is clearly more novel. Compared to "GPT-4 Is Too Smart To Be Safe" (score 6.75, Accept) — which combined a novel finding with multi-model experiments — our paper's evaluation is substantially thinner.

**Calibration Anchors Considered:**
- `5kMwiMnUip.md` (avg 1.40, Jailbreaking LLMs): much weaker overall, no working method. Our paper is clearly above this.
- `8QTpYC4smR.md` (avg 1.00, Systematic Review of LLMs): a literature survey with no original contribution. Not comparable.
- `jbfDg4DgAk.md` (avg 3.00, Sparse Watermarking): limited novelty, missing baselines. Our paper has stronger novelty.
- `urQi0TgXFY.md` (avg 5.00, Steganographic Collusion in LLMs): more thorough experiments, but novelty questioned. Our paper has a more novel core idea but weaker experiments. Comparable overall quality.
- `kRJNV8RCE3.md` (avg 4.75, Hiding Images in Diffusion Models): limited novelty, some experiments. Our paper has stronger novelty.
- `MbfAK4s61A.md` (avg 6.75, CipherChat): strong novelty and multi-model experiments, accepted. Our paper's evaluation is substantially thinner.
- `E4LAVLXAHW.md` (avg 7.00, Black-Box Detection of Watermarks): rigorous theoretical and experimental work. Not comparable in rigor.
- `LdIlnsePNt.md` (avg 6.00, Watermarking using Semantic-aware Speculative Sampling): theory + practice, rejected despite theoretical contribution. Our paper has less rigorous evaluation.

---

## Summary

This paper presents **Calgacus**, a protocol for LLM-based steganography that hides a secret message inside a stegotext of the same length. The method records the rank of each token of the secret message under an LLM's probability distribution, then generates a stegotext by following those same ranks under a different prompt. The authors demonstrate the protocol experimentally (3 source texts, 85 tokens, Llama 3 8B) and discuss broad philosophical implications about authorship, intention, hallucination, and AI safety.

## Strengths

- **Core idea is genuinely novel and simple.** The rank-preserving protocol is clever and non-obvious. Its simplicity (store ranks from one prompt, follow them under another) makes it immediately accessible and implementable. This is a genuinely new protocol, not a minor variant of existing methods.

- **Same-length property is a crisp, clearly defined differentiator from prior generative steganography.** Prior LLM steganography methods (Ziegler et al., Kaptchuk et al., Wu et al.) embed messages into longer cover texts or adjust bit rates based on entropy. The 1:1 length ratio is a clean advance that creates distinct attack/defense properties.

- **Deniability is plausibly demonstrated.** Figure 4 shows that for some prompts, stegotexts achieve log-probabilities comparable to the original text, providing an empirical basis for plausible deniability — a practically meaningful property that many steganographic schemes lack.

- **The philosophical discussion about hallucinations, intention, and authorship is thoughtful and substantive.** The reframing of hallucination from "false statement" to "void of intention" (Section 4), the connection to Oulipo constraints, and the discussion of what it means for an LLM to "know" something go beyond literary flourish and constitute a genuine conceptual contribution that stands apart from the experimental apparatus.

## Weaknesses

### Fatal
None.

### Major

- **The evaluation is far too thin for the scope of claims made.** The experimental basis consists of: (1) 1,000 Reddit posts truncated to 85 tokens as a reference distribution; (2) only **3** source texts selected from that pool for encoding; (3) **100** stegotexts per source text (300 total); (4) one primary LLM (Llama 3 8B), with one cross-check to Phi-3 3.8B deferred to the appendix; (5) one metric (LLM-assigned log-probability). The paper claims that stegotexts are "coherent and plausible" to humans, but provides **no human evaluation whatsoever** — not even a small study. LLM log-probability is acknowledged as an imperfect proxy, yet it is the only evidence for the central plausibility claim. Additionally, the method is tested only at 85 tokens (~60–70 words) on a single dataset (Reddit) in one register of English. There is no systematic failure analysis: the paper mentions encoding a hash fails but never characterizes across diverse source texts what properties correlate with success or failure. For a paper whose abstract speaks of "a radical decoupling of text from authorial intent" and positions the method as an urgent AI safety concern, this level of empirical support is insufficient.

- **No comparison to prior LLM steganography methods.** Section 2 lists several prior methods (Ziegler et al., Kaptchuk et al., Wu et al., Zamir) and positions "same length" as the key differentiator, but provides **zero empirical comparison** — not on stegotext quality, information rate, security, or any shared metric. Without quantification of trade-offs against existing methods, a reader cannot assess the practical significance of the contribution relative to the state of the art.

### Minor

- **Detectability is acknowledged but not quantified.** The paper states that stegotexts are "on average" less probable than originals and can be distinguished by an LLM picking the most probable text. However, it never runs a systematic detection experiment reporting AUC, accuracy, or precision-recall. The paper's response to this central attack scenario is entirely qualitative. For a steganographic protocol, the question of whether an attacker can detect the presence of a hidden message is first-order, and the paper's treatment of it is insufficient.

- **The security analysis is informal, and the shipping scenario has a concrete structural issue.** The paper explicitly declines to frame the method in a formal security model (line 61), which is a defensible choice but leaves security properties undefined. More concretely, in the "shipping unfiltered LLMs" scenario (Section 4), the secret key k (= reasoning trace t) is transmitted alongside the stegotext s as part of the chatbot response. Any censor with knowledge of the protocol who intercepts the response has both k and s and could decode the hidden message. The paper's defense — that the company can claim the user made an "unconventional sampling strategy" — is a rhetorical/legal argument, not a technical security guarantee.

- **Limited text length exploration.** All experiments use 85-token texts (~60–70 words). The abstract claims "a message as long as this abstract can be encoded," but the abstract is substantially longer (~150 words, probably ~200 tokens). The method may face compounding errors or tighter distributional constraints at longer lengths; this is neither tested nor discussed.

### Trivial
None.

## Nice-to-Haves

- Conduct a human evaluation of stegotext plausibility (even a small study with 20–50 raters) to validate the central claim.
- Run a systematic detection experiment (classifier accuracy, AUC) to quantify the protocol's vulnerability to the most obvious attack scenario.
- Scale from 3 to at least 30–50 source texts across diverse domains (news, fiction, technical writing, dialog).
- Test at multiple lengths (50, 100, 200 tokens) to validate scaling behavior.
- Add empirical comparison to at least one prior LLM steganography method on a shared metric.
- Vary the LLM systematically (3–5 models) in a factorial encoding/evaluation design.

## Removed Points

- **"Main empirical finding undermines the primary claim" (Harsh Critic Issue 2):** The paper is transparent about stegotexts being distinguishable. Its primary claim is about hiding text of the same length that remains "coherent and plausible" — not undetectability. The paper does not claim perfect indistinguishability. This criticism overstates the gap. The legitimate concern (detectability not quantified) is retained as a Minor weakness above.
- **"Mismatch between rhetorical register and evidential foundation" (Harsh Critic Issue 4):** A stylistic/subjective observation about the paper's tone. While noted, it is not a technical weakness and is better handled as a general observation rather than a listed weakness.
- **"Reproducibility details are minimal":** The paper notes the sender and receiver must run the LLM under identical conditions. Standard model and decoding details are roughly at the level expected for an exploratory protocol paper.
- **"Secrecy condition underspecified":** The paper discusses key management (random string in k, Figure 13 examples). Full key management protocol is beyond the paper's scope.
- **"Full capacity is potentially misleading":** The paper defines "full capacity" as same-length encoding, which is clear from context. This is a definitional choice, not a technical error.
- **Brute-force bound notation criticism:** The harsh critic claimed the notation was technically inaccurate, but O(d^{|k|}) is correctly exponential in |k|. This was a reviewer error.

## Novel Insights

The harsh critic's observation that the paper's most technically informative finding (stegotexts being systematically less probable) is also its most significant limitation creates a useful framing: the "low entropy token choices" analysis (lines 134–146) correctly identifies that rank-1 tokens from the source are "wasted" on high-entropy positions in the stegotext. This insight — that the gap arises from the frequency of rank-1 tokens (~40%) being much lower than the probability of the truly dominant token in deterministic contexts (~95%) — is the paper's clearest technical contribution to understanding both why the method works and where its limits lie. The connection between this statistical observation and the philosophical discussion about the nature of LLM-generated text (Section 4) is the paper's most distinctive intellectual contribution.

## Suggestions

1. **Human evaluation is the single highest-leverage addition.** Without validating that stegotexts are actually plausible to human readers (not just to an LLM-based proxy), the central claim remains unsubstantiated.

2. **Run a systematic detection experiment.** Report AUC, accuracy, or comparable metrics for distinguishing stegotexts from real texts. This would either validate or bound the protocol's vulnerability to the most obvious attack.

3. **Add at least one empirical comparison to a prior LLM steganography method** (e.g., Kaptchuk et al., Wu et al.) on a shared metric such as stegotext perplexity, decoding accuracy, or detection rate.

4. **Scale the source text sample** to at least 30–50 texts across diverse domains and test at multiple lengths (50, 100, 200 tokens).

5. **Calibrate the claims to the evidence.** The paper's philosophical discussion is valuable in its own right and does not require extensive experimental support. But the empirical claims (about coherence, plausibility, and safety implications) should match what the evidence supports.

## Score and Decision

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>