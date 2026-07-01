Now I have a comprehensive understanding of the paper. Let me draft my review before calibration.Now let me calibrate. Round 1 — Bracketing:Let me read the two most directly relevant anchor papers to compare:Now let me read the accepted CipherChat paper (6.75) more carefully to understand the acceptance bar:Now I have sufficient calibration data. Let me finalize my assessment.

**Round 1 Bracket**: Based on my comparisons:
- The paper is clearly above the strong-reject tier (1.0-1.5) — it has genuine substance.
- It's similar in profile to "Plausibly Deniable Encryption with LLMs" (4.80, Reject) — same domain, similar thin evaluation, similar elegance of core idea.
- It's somewhat stronger than "Hidden in Plain Text: Steganographic Collusion" (5.00, Reject) due to its more novel insight.
- It's weaker than "CipherChat" (6.75, Accept) which had more systematic evaluation across multiple models, ciphers, and domains.
- **Initial bracket: 4.5–6.0**

The paper has a genuinely novel insight but insufficient empirical support compared to accepted papers in this space. The closest comparable (Plausibly Deniable Encryption, 4.80) was rejected for very similar reasons: thin formal analysis, practical limitations underexplored, insufficient evaluation. This paper is slightly stronger due to its more elegant insight and novel threat model, but shares the same structural weaknesses.

**Final score: 5.0** — between borderline reject and borderline accept. The insight is real but the paper doesn't meet the evidential standard for acceptance.## Summary
This paper presents Calgacus, a steganographic protocol that hides text within another plausible text of the same token length using LLMs. The method encodes a source text as its token-rank sequence under the LLM, then uses that rank sequence to select tokens during generation from a different prompt. The paper also articulates a novel AI safety threat model (the "Shibbolethian Theatre") and includes philosophical discussion about hallucination, intentionality, and what it means for an LLM to "know" something.

## Strengths

- **The core observation is genuinely illuminating.** The insight that standard LLM text generation is structurally a steganographic channel—and that the protocol is "a mere variation of the standard algorithm used to generate text with LLMs" (Section 5)—is a real intellectual contribution. The simplicity of the method (Section 3, Figure 3: encode source tokens as ranks, generate from a different prompt following those ranks) makes the observation accessible and compelling.

- **The "low entropy token choices" analysis is non-obvious and well-supported.** The explanation of why stegotexts are systematically less probable despite preserving token ranks (Section 3: rank-1 frequency ~40% in source text vs. >95% probability mass in low-entropy stegotext positions) is a clean piece of reasoning with clear empirical support in Figure 5.

- **The "Shibbolethian Theatre" scenario (Section 4) articulates a genuinely novel AI safety threat.** The concrete protocol showing how a company could expose only compliant answers while covertly delivering uncensored content through rank encoding is a plausible attack vector not previously articulated in this form.

- **The paper is exceptionally well-written**, with genuine intellectual engagement (connections to Oulipo, Tacitus, constraint satisfaction) rather than superficial ornamentation.

## Weaknesses

### Fatal
None

### Major

- **Thin quantitative evaluation undermines the core plausibility claim.** The entire evaluation (Section 3, Figure 4) consists of log-probability comparison for 300 stegotexts (100 each for 3 source texts at μ, μ−2σ, μ+2σ) against 1000 Reddit posts, using primarily Llama 3 8b. There is no human evaluation of stegotext plausibility, no direct comparison with any prior LLM steganography method (Meteor, Ziegler et al., Wu et al.), and only 3 source texts sampled from a single distribution. The paper's own analysis shows LLMs *can* distinguish stegotexts from originals—it needs to show humans cannot, since steganographic security is fundamentally defined against human observers.

- **The "full capacity" framing (Section 2) is misleading.** The paper states Calgacus has "the notable property of having full capacity, that is, the stegotext and the secret message being of the same length." Prior methods encode arbitrary bitstrings at ~3-5 bits/token; Calgacus encodes natural language text (which carries ~5-10 bits/token of information content) in same-length text. The paper never measures bits-per-token capacity, never compares with prior methods on any common metric, and conflates token count with information-theoretic capacity. The contribution is genuinely different (text-to-text encoding) but the "full capacity" label overstates what is demonstrated.

### Minor

- **The reproducibility requirement is acknowledged but underexplored.** The Limitations section (Section 3) devotes a single sentence to the fact that "sender and receiver must run the chosen LLM under identical conditions, performing the same approximations and obtaining identical logits. This may be a challenge when using different GPU architectures." For the Shibbolethian Theatre scenario—where the company encodes on servers and the user decodes on commodity hardware—this is a significant practical constraint. No experiments demonstrate successful cross-hardware encoding/decoding, and no error-correction mechanisms are discussed.

- **The security analysis (Section 3.1) is entirely informal.** The brute-force upper bound O(d^|k|) is trivially true, and the deniability argument is qualitative without quantification of how often outlier prompts produce text with probability comparable to the original. While the paper explicitly disclaims formal models (Section 2), the security claims would benefit from even a simple empirical test (e.g., a trained classifier attempting detection).

- **No timing benchmarks.** The paper claims "an entire article can be encoded and decoded on commodity hardware in seconds" (Introduction, Abstract) but provides no actual timing measurements.

### Trivial
None

## Nice-to-Haves
- A human indistinguishability study (even small-scale) to complement log-probability analysis
- Bits-per-token measurement and comparison with Meteor/Ziegler et al. to properly contextualize the capacity claim
- Empirical demonstration of cross-hardware deterministic decoding
- A trained classifier attack experiment testing detectability
- Quantification of deniability: what fraction of random keys produce decodable text within ε log-probability of the original?

## Removed Points
These points are flagged to be removed, treat them with caution:

- **"Related work doesn't engage with AI safety literature"** — Scope creep. The paper's related work is appropriately focused on steganography; the AI safety application is discussed in Section 4 where it belongs.
- **"Philosophical discussion is tangential and takes too much space (~2 pages)"** — The paper explicitly frames philosophical implications as a core contribution (stated in abstract, introduction, and conclusions). Whether a venue values this framing is a matter of fit, not a flaw in the paper.
- **"The degree of thematic control over stegotexts is not systematically evaluated"** — The paper makes modest claims about steerability ("the topic and tone and style of the fake text are steerable") and demonstrates this qualitatively. It never claims precise thematic opposition.
- **"Qualitative examples are cherry-picked"** — The examples (Figures 1, 11–13) demonstrate the protocol working as described; they are illustrative, and the quantitative evaluation in Figure 4 addresses the distributional question separately.

## Novel Insights
The paper's central insight—that LLM text generation is structurally equivalent to steganographic encoding because any sequence of token selections can simultaneously be interpreted as encoding a different text through rank correspondence—is genuinely novel and illuminating. The corollary that "any original text could be a beautiful and treacherous, and spacious, Trojan horse" reframes the nature of LLM-generated text. The "low entropy token choices" analysis provides a clean theoretical explanation for why rank-preserving transformations systematically reduce probability, connecting to fundamental properties of language model distributions.

## Suggestions
- Reframe "full capacity" as "text-to-text encoding of the same token length" with explicit acknowledgment that prior methods encode different types of payloads, making direct comparison complex.
- Include a human evaluation study—even 30-50 participants in a two-alternative forced choice task distinguishing stegotexts from real texts would dramatically strengthen the plausibility claim.
- Demonstrate the protocol working across 2-3 common hardware configurations (e.g., same quantization on different GPUs, CPU inference) to establish practical viability.
- Quantify deniability empirically: generate 1000 random keys, report what fraction produces log-probability within various thresholds of the original.

## Score and Decision

### Calibration Anchors

| Paper | Avg Score | Round | Comparison to Paper Under Review |
|-------|-----------|-------|----------------------------------|
| 5kMwiMnUip (NEMESIS Jailbreaking) | 1.40 | R1 | Much weaker; no real technical contribution |
| 8QTpYC4smR (LLM Survey) | 1.00 | R1 | Much weaker; a survey with no novel contribution |
| gwZ90hFSL2 (Chinese NLP Robots) | 1.00 | R1 | Much weaker; unclear contribution |
| jbfDg4DgAk (Sparse Watermarking) | 3.00 | R1 | Weaker; less novel core idea, similar evaluation issues |
| BeOEmnmyFu (Language Game Jailbreaking) | 2.50 | R1 | Weaker; less novel, narrower contribution |
| RfYD6v829Y (TrojanRAG) | 3.40 | R1 | Weaker; more incremental, less insightful |
| **urQi0TgXFY (Steganographic Collusion)** | **5.00** | **R1** | **Similar level; emergent stego in LLMs, but less novel core insight, better evaluation** |
| **7suavRDxe8 (Plausibly Deniable Encryption)** | **4.80** | **R1** | **Most similar paper; same domain, same thin evaluation, similar elegance. Paper under review has more novel insight and threat model.** |
| 0KHW6yXdiZ (E2E Watermarking) | 5.25 | R1 | Similar level but different focus; more rigorous evaluation |
| 0koPj0cJV6 (Black-Box Watermark) | 4.60 | R1 | Similar level; more formal but less novel |
| **MbfAK4s61A (CipherChat)** | **6.75** | **R1** | **Stronger; similar novelty of finding but much more systematic evaluation across multiple models and domains** |
| YzxMu1asQi (Adversarial Scaling Laws) | 6.50 | R1 | Stronger; empirical laws with clear methodology |
| 9k0krNzvlV (Learnability of Watermarks) | 5.75 | R1 | Similar-to-slightly-stronger; more rigorous |
| xP1radUi32 (Bijection Jailbreaking) | 6.25 | R1 | Stronger evaluation, systematic results |
| j7b4mm7Ec9 (Lightweight Watermarking) | 7.60 | R1 | Much stronger evaluation and formalism |
| oZtt0pRnOl (Privacy-Preserving ICL) | 8.00 | R1 | Much stronger; formal guarantees, extensive experiments |

**Round 1 bracket: 4.5–6.0.** The paper is clearly stronger than the 3.0-3.5 papers (which have less novel ideas and worse execution) but weaker than the 6.25+ accepted papers (which have more rigorous evaluation). Its closest comparator is "Plausibly Deniable Encryption" (4.80) which shares nearly identical structural weaknesses (thin evaluation, practical concerns, informal security) but a slightly less novel core insight.

**Narrowing to final score:** The paper under review is somewhat stronger than 4.80 due to: (1) the "ranks = steganographic channel" insight being more elegant and general than the compression-based approach, (2) the Shibbolethian Theatre scenario being a genuinely novel threat model, and (3) superior writing quality. However, it remains below the acceptance threshold because its evaluation gaps are the same ones that led to rejection of similar papers: no human study, no baselines, thin sample, undemonstrated practical viability.

**Final score: 5.0** — The paper presents a genuinely novel and illuminating insight with a provocative threat model, but the evaluation is too thin and the empirical support too narrow to meet the acceptance bar at a top venue. It reads more as an elegant proof-of-concept essay than a fully substantiated research contribution.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>