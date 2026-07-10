Now I have a clear calibration picture. Let me compile the final review.

**Calibration Summary:**

| Anchor | Avg Score | Decision | Round | Itemized? | Comparison |
|--------|-----------|----------|-------|-----------|------------|
| Hidden in Plain Text (urQi0TgXFY) | 5.00 | Reject | R1,R2 | Yes | Thorough experiments (+9.97) but lacks novelty (-10.00). Opposite profile to our paper. |
| Plausibly Deniable Encryption (7suavRDxe8) | 4.80 | Reject | R1,R2 | Yes | Strong eval (+9.79, +9.85) but no security model (-10.00), limited novelty (-10.00). Our paper has stronger novelty. |
| Hiding Images in Diffusion (kRJNV8RCE3) | 4.75 | Reject | R2 | Yes | Strong results (+9.98) but limited novelty (-10.00). |
| Sparse Watermarking (jbfDg4DgAk) | 3.00 | Reject | R1 | Yes | Missing baselines (-10.00), lack of novelty (-10.00). |
| I Know You Did Not Write (eKGEsFdpin) | 3.67 | Reject | R1 | Yes | Similar to prior work (-10.00), insufficient evaluation (-10.00). |

**Round 1 Bracket:** Between 4.0 and 5.5 (below the Hidden in Plain Text at 5.0 because experiments are thinner; above Sparse Watermarking at 3.0 because core idea is much more novel).

**Narrowing:** Closest anchor is Plausibly Deniable Encryption (4.8) and Hidden in Plain Text (5.0). Our paper has a genuinely novel core idea (unlike Hidden in Plain Text's novelty issue), but experiments are notably thinner than either. Thus score is slightly below both: **4.5**.

---

## Summary

This paper presents *Calgacus*, a protocol for LLM-based steganography that hides a secret text inside a generated text of the same length by preserving token ranks across different prompts. The core idea: record the ranks of each token in the secret text under one context, then use those ranks to guide generation under a different secret prompt to produce a coherent cover text. The receiver, knowing the secret prompt and using the same LLM, recovers the ranks from the stegotext and regenerates the original. The paper also offers a substantial philosophical discussion about hallucinations as a failure of intent rather than factuality, and about the implications of text becoming decoupled from authorial purpose.

## Strengths

- **The core idea is genuinely novel and elegant.** Encoding a secret message by recording its token ranks under one prompt and using those ranks to guide generation under a different prompt is a simple, clean mechanism that is clearly novel relative to prior LLM steganography work (which typically embeds bits into the sampling process with longer stegotexts). The "same length" property is a notable differentiating feature. The method is described clearly in Section 3 (Figure 3) and is immediately reproducible.
  
- **The philosophical discussion is thoughtful and distinctive.** Sections 4–5 engage with reconceptualizing hallucinations as a failure of intent rather than factuality, connect the protocol to Oulipo constraint-based literature (Perec's *La Disparition*), and use the Tacitus/Calgacus framing to explore text without authorial purpose. This gives the paper an intellectual richness unusual for a technical submission.

- **The paper is transparent about its limitations.** It explicitly demonstrates a failure case (the hash example), states upfront that it will not provide a formal security model ("we will avoid building a palace on the sand"), and enumerates practical constraints (dependence on $e$, $k$, and the LLM; need for identical decoding conditions).

## Weaknesses

### Fatal
None.

### Major

- **The experimental evaluation is far too thin to support the paper's claims.** The core quantitative experiment tests exactly **3 original texts** (85 tokens each), using **one LLM** (Llama 3 8b) for the primary generation. The paper's abstract claims that "even modest 8-billion-parameter open-source LLMs are sufficient to obtain high-quality results" and that "a message as long as this abstract can be encoded and decoded locally on a laptop in seconds." These are strong empirical claims resting on essentially minimal evidence — three data points, one model, one length, no replication across domains, languages, or text types. For a protocol that is presented as practically usable and raises urgent AI safety concerns, this level of evaluation is insufficient.

- **The paper asserts stegotexts are "opaque to humans" (line 43) but provides no human evaluation whatsoever.** The primary evidence for plausibility is log-probability comparisons under the same model family (Llama 3 8b) that generated the stegotexts. This creates an evaluation-circularity concern: the stegotext is constructed to have high-probability tokens under that model's distribution, so of course it scores well. The paper notes that Phi-3 3.8B shows similar shifts (Figure 14, in the appendix), but this still measures LLM-perceived plausibility, not human perception. For a paper whose central applied claim is that text can be hidden "in plain sight," the absence of even a small human subject experiment is a critical gap that directly undermines the headline assertion.

- **No experimental comparison to any prior LLM steganography method.** The paper correctly identifies Ziegler et al. (2019), Kaptchuk et al. (2021), and Zamir (2024) as related work, describing their different properties. But it never compares Calgacus to any of them on any metric — capacity, detectability, computational cost, or stegotext quality. Without such comparison, it is impossible to assess what the protocol contributes beyond being different. The paper positions itself as a methods contribution, and methods papers require comparative evaluation.

### Minor

- **The security analysis (Section 3.1) is informal and unquantified.** While the paper honestly disclaims a formal security model, the discussion that remains is too casual to be meaningful. The brute-force bound $O(d^{|k|})$ is of limited practical relevance since $k$ is a natural language phrase that admits a far smaller semantic search space — a point the paper acknowledges but does not quantify. The deniability claim rests on observing that "for some prompts the stegotexts can attain probabilities in the same ballpark as the original" (referencing a single example in Figure 15 in the appendix), with no systematic characterization of how common such prompts are. The proposed countermeasure (inserting a random string in $k$) re-introduces key-length overhead that the "same length" framing had minimized.

- **A potential confound in the experimental design is not addressed.** The 1000 Reddit baseline texts are noted to be "more recent than Llama 3 and therefore cannot appear in its training corpus" (line 130). This means the real-text baseline is systematically out-of-distribution relative to the evaluating LLM, which could systematically lower their log-probabilities and make the stegotexts appear comparatively more plausible than they actually are. This confound is acknowledged by the paper in passing but not discussed as a limitation.

### Trivial
None.

## Nice-to-Haves
- A human evaluation study (even small-scale) to support the "opaque to humans" claim.
- A larger and more varied test set (different lengths, domains, languages).
- A comparison to at least one prior LLM steganography method on a shared metric.

## Removed Points
- *Criticism about the "same length" framing eliding full communication overhead.* The paper's claim is about the stegotext $s$ being the same length as the hidden text $e$, which is technically correct. The secret key $k$ is transmitted separately in any steganographic protocol — this is a standard framing.
- *Criticism about the brute-force bound being "irrelevant."* The paper acknowledges the attacker could reduce the search space. The criticism adds nothing beyond what the paper already states.
- *Criticism about missing scaling analysis, success rate, or failure characterization.* These could be in the appendix (which is stripped by the parser). Per hard rules, weaknesses about missing appendix content are removed.
- *Criticism about rhetorical claims outrunning evidence.* This is a judgment call, not a specific verifiable weakness.
- *Overall assessment framing (e.g., "reads as a preprint").* Generic editorializing, not a specific weakness.

## Novel Insights
The harsh critic's most valuable observation is the unaddressed confound in the experimental design: the 1000 Reddit texts used as a real-text baseline are explicitly noted to be out-of-distribution relative to Llama 3's training data ("more recent than Llama 3 and therefore cannot appear in its training corpus"). This means the baseline texts are systematically assigned lower log-probabilities by the evaluating LLM, potentially inflating the perceived plausibility of the stegotexts relative to real text. The paper mentions this fact but never discusses it as a limitation. Additionally, the pairing of a genuinely novel steganographic protocol with a philosophical discussion about intentionality is an unusual and potentially fruitful combination of technical and conceptual contributions — though the paper currently under-delivers on the technical side.

## Suggestions
1. **Add a human evaluation** — even a small one (e.g., 50 participants rating 20 text pairs on plausibility/authenticity) would directly support the central claim that stegotexts are "opaque to humans" and dramatically strengthen the paper.
2. **Expand the experiment** to more originals (20–30+) across different domains and lengths, and report success rates and failure modes systematically.
3. **Include a baseline comparison** to at least one prior LLM steganography method (e.g., Ziegler et al. or Kaptchuk et al.'s Meteor) on a shared metric such as capacity, detectability, or stegotext quality.
4. **Address the out-of-distribution confound** for the Reddit baseline, either by using an in-distribution corpus or by explicitly discussing the potential bias.

## Score and Decision

**Score: 4.5**

**Decision: Reject**

**Calibration grounding (required by protocol):** 
My draft's scored items show the paper has strengths that push its score up by ~10 points (novel core idea +9.97, philosophical discussion +10.00, honest limitations +6.67) and weaknesses that pull it down by ~10 points (thin evaluation -10.00, no human evaluation -9.99, no comparison to prior work -10.00, informal security -1.25). The closest anchors are "Hidden in Plain Text: Emergence & Mitigation of Steganographic Collusion in LLMs" (avg 5.00, Reject) and "Plausibly Deniable Encryption with Large Language Models" (avg 4.80, Reject). Both share the pattern of an interesting idea undermined by significant evidential or novelty gaps. Our paper is stronger than both on core-idea novelty (the "Hidden in Plain Text" paper was heavily criticized for lacking novelty, with -10.00 impact on that dimension), but weaker on experimental thoroughness (the Hidden in Plain Text paper had experiments rated at +9.97, while our paper's thin evaluation scored -10.00). Given this tradeoff, the paper sits slightly below both anchors, at 4.5. Round 1 bracket was 4.0–5.5; subsequent comparison to the 4.8 and 5.0 anchors narrowed to 4.5. The paper's genuinely novel idea is commendable, but the empirical evidence is too minimal to support the strong claims made in the abstract and introduction. The paper would benefit substantially from expanded evaluation, human studies, and baseline comparisons before it meets the bar for a top venue.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>