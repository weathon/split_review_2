The impact scores confirm that the two MAJOR weaknesses are rated as highly damaging (-10.0, -9.5) while most strengths are moderate. The evaluation thinness and lack of baselines are decisive. Now producing the final review.

---

## Summary

This paper presents Calgacus, a protocol that uses LLMs to hide one meaningful text inside another coherent text of the same length. The method records token-level ranks from the text to be hidden, then uses those ranks as a generation template under a different prompt. The protocol is simple, requires no training, and achieves the notable property that the stegotext is exactly as long as the hidden message. The paper also discusses philosophical implications about LLM knowledge, hallucinations, and authorial intent.

## Strengths

- **Clever, minimalist idea.** The core protocol — recording token-level ranks from one text and using them to guide generation of another text with a different prompt — is genuinely elegant. It requires no training, no model modifications, and is trivially reversible by construction. (Section 3)

- **The "full capacity" property is a clear differentiator.** The fact that the stegotext and the hidden text have the same token length follows directly from the design and distinguishes Calgacus from prior generative steganography methods that encode multiple tokens of hidden message per token of stegotext or vice versa.

- **Striking qualitative examples.** The concrete examples in Figure 1 — a political critique hidden in a boar recipe, Caesar's defense hidden in a political speech — vividly illustrate the claim that coherent texts of different topics can be generated from the same rank sequence. These examples are the paper's most memorable evidence.

- **Well-written with intellectual ambition.** The paper is engaging and the philosophical discussion (Section 4) about hallucinations as a deficit of intention rather than factuality raises genuinely interesting questions that the steganographic lens usefully sharpens.

## Weaknesses

### Fatal

None.

### Major

1. **The evaluation is too thin to support the paper's central claims.** The main experiment consists of 3 hidden texts × 100 stegotexts each, all 85 tokens long, generated and evaluated with a single LLM (Llama 3 8B, line 130). Quality is measured only by LLM log-probability with no human evaluation of stegotext fluency. There is no evaluation across different text lengths, no evaluation across different generator LLMs, and the structural detection vulnerability that the paper itself identifies (line 132: "generally the original text can be discerned from its stegotexts by picking the most probable one according to a LLM") is not quantified with ROC curves or false-positive rates at relevant thresholds. The paper acknowledges that detection is possible but never measures how easy it is.

2. **No comparison to existing LLM-based steganography methods.** The related work (line 67) describes Meteor (Kaptchuk et al.), Wu et al., and Zamir but provides no controlled comparison on fluency, detection rate, or bitrate. Without baselines, the reader cannot evaluate whether the same-length property justifies the detection cost the paper itself documents. The paper's central tradeoff — fixed 1:1 token mapping regardless of token entropy — cannot be assessed relative to methods like Meteor that adaptively minimize distortion.

### Minor

3. **The security analysis does not adequately address the detection vulnerability.** The analysis in Section 3.1 focuses on message recovery given an attacker who already knows a message is hidden. But the paper's own evidence shows LLMs can distinguish stegotexts from originals by log-probability, which is a detection weakness. The deniability argument (line 166) applies only after detection has occurred. The suggestion about inserting a random string in k (line 164) is stated without demonstration or analysis.

4. **Limited cross-model evidence.** Only Llama 3 8B is used as the generator (line 130). Phi-3 3.8B is used only as a detector (Figure 14, appendix). The claim that "even modest 8B models are sufficient" rests on a single model, and no results from smaller or larger models are reported.

5. **No evaluation of the claimed steerability.** The paper states that "the topic and tone and style of the fake text are steerable" via k (line 19), but no controlled experiment verifies that different keys reliably produce different styles or topics.

6. **No ablation of key design choices.** The paper mentions that including k' before e or using a longer k can lower ranks (lines 119-120) but provides no systematic analysis of how to choose k for a given e, or how this choice affects both stegotext quality and security.

7. **The Shibbolethian Theatre scenario overclaims practical credibility.** The scenario (Section 4) is presented as a concrete AI safety challenge, but the company generates both the aligned and unaligned responses, so any auditor inspecting the aligned response can detect the steganographic encoding. The deniability argument ("unconventional sampling strategy," line 205) is clever but would not withstand serious scrutiny. The scenario works as a thought experiment but not as a credible threat model.

### Trivial

None.

## Nice-to-Haves

- A systematic ablation of how different keys k affect stegotext quality would strengthen the practical guidance for users.
- Evaluating the protocol at longer text lengths (e.g., 200, 500 tokens) would test generalizability.
- A controlled steerability experiment (e.g., classifying generated stegotexts by topic to verify alignment with the key) would validate the claimed steering capability.

## Removed Points

These points from the input review were removed after cross-checking against the paper:

- **"The claim about radical decoupling applies to any LLM-generated text"** — REMOVED because the paper itself acknowledges this parallel (Section 4: "Standard LLM text generation is not immune to the last argument"). This is a philosophical observation, not a technical weakness.
- **"The paper's dismissal of formal models seems designed to excuse its own lack of security analysis"** — REMOVED as speculative about author intentions. The paper states its position transparently (line 61).
- **"References to Figures 10-15 in the appendix suggest heavy reliance on supplementary material"** — REMOVED per policy: the parser strips appendices from all papers; these figures exist in the original submission.
- **"The comparison to prior LLM steganography is too brief"** — MERGED into Major weakness #2 (absence of controlled comparison, not brevity of description).

## Novel Insights

The key insight — that token-level rank sequences can be decoupled from content and re-used as a generation template under a different prompt — is genuinely novel. The paper's diagnosis of why this produces systematically lower-probability stegotexts (the "low entropy token choices" analysis, line 146) goes beyond simply noting the effect and provides a mechanistic explanation: rank-1 tokens are "wasted" in high-entropy positions where the original text had an extremely probable token but the stegotext substitutes a rank-1 token at a position where many tokens are similarly probable.

## Suggestions

1. Conduct a proper detection-evaluation study: generate stegotexts from many source texts at varying lengths, and measure whether a detector (statistical, LLM-based, or human) can distinguish them from natural text. Report ROC curves and false-positive rates, not just aggregate log-probability histograms.
2. Add a controlled comparison to a representative prior method (e.g., Meteor) at comparable bitrates, measuring fluency (human-rated), detectability, and bitrate.
3. Include a systematic ablation of how the choice of key k affects both stegotext quality and security.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>