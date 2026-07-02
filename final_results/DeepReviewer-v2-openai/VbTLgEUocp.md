## Summary
# Final Review Report

## Summary

This paper presents *Calgacus*, a protocol for generative steganography using Large Language Models that achieves a notable property: the stegotext (the text carrying the hidden message) is exactly the same length as the secret message — "full capacity." The protocol is elegantly simple: it records the token-rank sequence of the secret message under an LLM's probability distribution, then generates the stegotext by following those same ranks from a different prompt. The paper demonstrates that, for 85-token Reddit posts encoded with Llama 3 8B, the resulting stegotexts fall within the log-probability distribution of real texts. The discussion connects this capability to broader questions about AI safety (covert deployment of unfiltered LLMs), the nature of hallucination (reframed as lack of authorial intent rather than factual error), and what it means for an LLM to "know" something.

**Strengths:** Conceptually elegant protocol with a clear technical contribution (full-capacity generative steganography); thought-provoking discussion of implications for AI safety and LLM epistemology; open-source demo for reproducibility.

**Weaknesses:** Experimental validation is narrow (85 tokens only, one primary LLM, no human subject evaluation); security analysis is entirely informal with no formal guarantees or quantified attack resistance; the novelty claim ("full capacity") lacks a systematic comparison table against prior methods; speculative application scenarios (censorship evasion, covert LLM deployment) are presented without feasibility validation; the philosophical argument for redefining hallucination is evocative but lacks rigorous support. External literature verification was unavailable in this run; novelty and comparison conclusions are deferred for manual follow-up.

## Strengths
1. **Conceptual simplicity and elegance.** The Calgacus protocol is remarkably simple — it records token ranks from the secret message and reuses them to generate the stegotext from a different prompt. This simplicity is a genuine strength: it makes the protocol easy to understand, implement, and audit. The open-source demo (GitHub) further supports reproducibility.

2. **Full-capacity property.** The claim that the stegotext and secret message are the same length is a clear, measurable differentiator from prior LLM-based steganography methods, which typically produce longer stegotexts. If substantiated through systematic comparison, this is a meaningful technical contribution.

3. **Provocative discussion of implications.** The paper raises genuinely interesting questions about LLM knowledge, hallucination, and the decoupling of text from authorial intent. The AI safety scenario (encoding unfiltered LLM answers within aligned responses) is a thought-provoking challenge to current safety paradigms, even if not fully validated as a practical attack.

4. **Transparency about limitations.** The paper acknowledges several important limitations: the protocol does not guarantee coherence for all inputs (hash example), the quality depends on e, k, and the LLM, and identical LLM conditions are required for recovery. The "Limitations" paragraph (Page 5) is candid and specific.

5. **Cross-model validation.** The use of Phi-3 3.8B (Figure 14, appendix) to verify that probability shifts between real and fake texts persist across different LLMs adds robustness to the empirical claims, though this cross-check is only briefly mentioned in the main text.

## Weaknesses
### W1. Narrow experimental validation (Major)
The empirical evaluation is limited to 85-token Reddit posts using Llama 3 8B as the primary model (see annotation on Page 1 - Method: quantitative measure paragraph). Key gaps: (a) only one text length is tested — claims about encoding "an entire article" are unvalidated; (b) only one LLM is used for the main experiment, with a brief cross-check to Phi-3 in the appendix; (c) no systematic evaluation of how performance varies with text domain, length, or model size; (d) the claim that stegotexts are "within the real text distribution" is stated without statistical quantification (no overlap metric, no hypothesis test). The selection of the three source texts from the same Reddit distribution used as the reference introduces circularity.

**Required action:** Add experiments with varying text lengths (50–500 tokens), multiple LLMs (e.g., Llama 2 7B, Mistral 7B, GPT-2), and report quantitative overlap measures (e.g., Wasserstein distance, KS statistic) with confidence intervals.

### W2. Informal security analysis (Major)
The security analysis (Section 3.1) is entirely heuristic (see annotation on Page 1 - Security paragraph). The claimed key space bound $O(d^{|k|})$ assumes a random key, but the authors immediately acknowledge $k$ is natural language — reducing the effective search space dramatically. No analysis is provided for: known-plaintext attacks, LLM fingerprinting (attacker enumerates known open-source models), or statistical attacks on the rank distribution. The deniability argument depends on finding "outlier prompts" but no constructive method or prevalence analysis is given.

**Required action:** Provide a formal or semi-formal security model, quantify the effective key space for natural-language keys, analyze known-plaintext resistance, and discuss the limitations of heuristic security arguments explicitly.

### W3. Overclaimed novelty positioning (Major)
The paper positions "full capacity" as its distinguishing contribution but does not provide a systematic comparison table against prior methods (see annotation on Page 1 - Related Work: Steganography and LLMs paragraph). Without a side-by-side comparison of token-length ratios, bit-per-token rates, computational costs, and success rates under comparable settings, the novelty claim remains unsubstantiated. The cited methods (Ziegler et al., 2019; Kaptchuk et al., 2021; Wu et al., 2024; Zamir, 2024) are described only qualitatively.

**Required action:** Add a comparison table with columns: Method | Logit Access Required | Distribution Modified? | Typical Stegotext/Message Length Ratio | Bits per Token | Computational Cost. This would substantiate the claimed advantage and clarify residual novelty.

### W4. Overstated indistinguishability claim (Major)
The paper claims that the length symmetry "prevents one from establishing at first sight which text is authentic" (see annotation on Page 1 - Introduction paragraph 3). However, no human evaluation is conducted. The paper later shows that LLMs can distinguish original from stegotext "on average," which directly undermines the strong indistinguishability claim. Additionally, steerability through the prompt $k$ is conditional — the hash example shows that some inputs produce broken stegotexts regardless of the prompt.

**Required action:** (a) Conduct a human evaluation (e.g., crowdsourced A/B test) to measure human detection accuracy. (b) Report the fraction of inputs for which the protocol produces fluent stegotexts across different prompt types. (c) Qualify the indistinguishability claim to match the actual evidence.

### W5. Attack scenario conflates thought experiment with practical threat (Major)
The "Shipping unfiltered LLMs without really shipping them" scenario (see annotation on Page 1 - Discussion: Unaligned chatbots paragraph) is presented as a concrete application but makes unvalidated assumptions: (a) that the stegotext would evade content moderation (contradicted by the paper's own finding that LLMs can distinguish stegotexts); (b) that the key can be securely distributed through the platform; (c) that the reasoning trace $t$ can be included without detection. The legal argument about "unconventional sampling strategy" is a policy claim outside the paper's technical scope.

**Required action:** Reframe the scenario as a thought experiment with explicit caveats. Discuss each assumption and its failure modes. Remove or substantiate the legal/policy arguments.

### W6. Philosophical arguments lack rigor (Minor-Major)
The redefinition of hallucination as "lack of intention" (see annotation on Page 1 - Discussion: Hallucinations paragraph) is based on an analogy (Tacitus, Pavlov) rather than technical reasoning. The argument conflates semantic knowledge with information-theoretic channel capacity (see annotation on Page 1 - Discussion: LLM knowledge paragraph). While philosophically interesting, these claims are presented as conclusions rather than speculative discussion, which may reduce the paper's scientific credibility.

**Required action:** Clearly demarcate empirical findings from philosophical discussion. If the hallucination redefinition is offered as a contribution, provide a structured argument with testable criteria rather than analogies.

### W7. Style and framing issues (Minor)
The paper uses an unusually informal and rhetorical style for a technical paper: "the end of history itself," "a difficult position to hold even for reviewer 2," "shady tech company," "tyrannical noise." While some readers may appreciate the voice, it risks alienating reviewers expecting standard scientific exposition. The political framing (pro-government vs anti-government, oppressive regimes) may be seen as editorializing.

**Required action:** Consider toning down the most hyperbolic passages and separating technical contributions from political commentary. A more measured tone would increase the paper's accessibility to a broader technical audience.

### W8. Missing appendix content (Minor)
The paper references numerous appendix figures (Figures 10–15, Appendices A.1–A.5) that are not included in the provided manuscript. Without these, key supporting evidence cannot be evaluated — in particular, the Phi-3 cross-validation (Figure 14), the deniability example (Figure 15), and the analysis of rank dependencies on text type (Appendices A.1, A.5).

**Required action:** Ensure all appendix materials are included in the submission and cross-referenced correctly.

## Score
**Final Score: 5.5/10**

**Rationale:** The paper presents a conceptually elegant protocol with a clear technical idea and thought-provoking implications. However, the experimental validation is narrow, the security analysis is informal, the novelty positioning against prior work is not systematically substantiated, and key claims (indistinguishability, practical threat scenario) outrun the available evidence. The philosophical discussion, while engaging, is presented as contribution rather than speculation, which weakens scientific rigor. The score primarily reflects the gap between the strength of the claims and the breadth of the current evidence base. With targeted experimental expansion (multi-length, multi-model, human evaluation), a systematic comparison table, and more measured claims, the paper's value could be substantially increased.

**External literature verification:** This review was conducted under Retrieval-Disabled Mode (external paper search unavailable). Novelty and comparison conclusions are therefore deferred for manual follow-up. The "full capacity" claim relative to prior LLM steganography methods (Ziegler et al., 2019; Kaptchuk et al., 2021; Wu et al., 2024; Zamir, 2024) should be verified by the authors through a systematic comparison table as recommended in Weakness W3.

---

### ASCII Diagram — Paper Structure & Evidence Map

```text
[Problem: Can LLMs hide text of the SAME length in another text?]
    |
    v
[Method: Calgacus protocol — record ranks of e, regenerate s from k using same ranks]
    |
    +---> [Claim C1: Full-capacity generative steganography]
    |         Evidence: Stated qualitatively, no systematic comparison table
    |         Gap: No length-ratio comparison vs prior methods
    |
    +---> [Claim C2: Works with modest 8B LLMs on commodity hardware]
    |         Evidence: 85-token Reddit posts with Llama 3 8B
    |         Gap: Only one length, one primary model tested
    |
    +---> [Claim C3: Radical decoupling of text from authorial intent]
              Evidence: Qualitative examples + log-probability plots
              Gap: No human evaluation; LLMs can distinguish on average
    |
    v
[Discussion: AI safety scenario, hallucination redefinition, LLM knowledge]
    |
    +---> [Safety scenario: thought experiment, not validated attack]
    +---> [Hallucination argument: philosophical, lacks rigorous grounding]
    +---> [Knowledge argument: conflates semantic knowledge with channel capacity]
```

---

### ASCII Diagram — Revision Strategy Roadmap

```text
[Priority 0 — Experimental expansion (highest impact)]
    |
    +---> Add multi-length experiments (50–500 tokens)
    +---> Add multi-model evaluation (Llama 2, Mistral, GPT-2)
    +---> Add human evaluation (crowdsourced A/B test)
    +---> Add quantitative distribution overlap metrics
    |       Expected gain: Substantiate core claims C1 and C2
    |
[Priority 1 — Novelty positioning]
    |
    +---> Add systematic comparison table vs prior methods
    +---> Report length ratios, bits/token, compute costs
    |       Expected gain: Substantiate C1 uniqueness
    |
[Priority 2 — Claim bounding]
    |
    +---> Qualify indistinguishability claim (humans not tested)
    +---> Reframe attack scenario as thought experiment with caveats
    +---> Separate empirical findings from philosophical speculation
    |       Expected gain: Align claim strength with evidence
    |
[Priority 3 — Security analysis]
    |
    +---> Quantity effective key space for natural-language keys
    +---> Discuss known-plaintext attacks
    +---> Explicitly state informal nature of security arguments
    |       Expected gain: Improve rigor without new experiments
```

---

### ASCII Diagram — Related-Work Taxonomy Tree (Layered)

```text
Note: External literature verification unavailable in this run.
The tree below is based on the paper's own cited references and should be 
expanded through systematic literature search by the authors.

Generative Steganography (Root)
├── Branch 1: Cover Modification
│   └── Leaf 1.1: Traditional edit-based steganography
│       [Kahn, 1996; Cachin, 1998]
│       Assumptions: Preexisting cover text modified
│       Difference vs Calgacus: Calgacus generates stegotext from scratch
│
├── Branch 2: Generative (LLM-based)
│   ├── Leaf 2.1: Entropy-adaptive encoding
│   │   [Kaptchuk et al., 2021 — Meteor]
│   │   Key property: Adjusts bits per token based on entropy
│   │   Overlap: Same goal of hiding text using LLM distributions
│   │   Difference vs Calgacus: Not full-capacity (longer stegotext)
│   │
│   ├── Leaf 2.2: Black-box distribution-preserving
│   │   [Wu et al., 2024; Zamir, 2024]
│   │   Key property: No logit access needed; output distribution unchanged
│   │   Overlap: Generative steganography for LLMs
│   │   Difference vs Calgacus: Full-capacity claim specific to Calgacus
│   │
│   └── Leaf 2.3: Logit-based rank-preserving (Calgacus — This Paper)
│       [Norelli & Bronstein, 2025]
│       Key novelty: Full capacity (stegotext length = secret length)
│       Open question: Robustness of novelty requires systematic comparison
│
└── Branch 3: Broader Generative AI Steganography
    └── Leaf 3.1: Image/Audio domain
        [Caron et al., 2021 — DINO; Dhariwal et al., 2020 — Jukebox]
        Difference: Domain difference; not directly comparable
```

---

**Contribution-level Novelty Conclusion (Deferred):** Due to Retrieval-Disabled Mode, external literature verification was not possible in this review. The three contribution claims (C1: full-capacity generative steganography; C2: efficiency with modest LLMs; C3: implications for AI safety and LLM knowledge) have provisional novelty tags of `unclear` pending systematic comparison against the cited prior methods. The authors are strongly encouraged to provide a direct comparison table as discussed in Weakness W3.

**Page Coverage Audit:** The provided manuscript is contained on a single page (page 1 of the PDF viewer) with approximately 147 lines of extracted text. All 14 annotations were placed on this page, covering: Abstract (1 annotation), Introduction paragraphs (4 annotations), Related Work (2 annotations), Method/experiment and low-entropy paragraphs (2 annotations), Security (1 annotation), Discussion/attack scenario (1 annotation), LLM knowledge and hallucination arguments (2 annotations), Conclusion (1 annotation). No appendix content was available for annotation in the provided excerpt.

**External literature verification unavailable in this run (paper_search not started); novelty/comparison conclusions are intentionally deferred.**