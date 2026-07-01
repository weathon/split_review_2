Now I have a clear calibration picture. Let me produce the final consolidated review.

## Summary

This paper proposes Augmented Intermediate Representations (AIR), a method that injects instruction hierarchy (IH) signals into every decoder layer of an LLM instead of only at the input layer. The core insight is that per-layer trainable IH embeddings maintain discriminability between privilege levels throughout the network, addressing a limitation in prior input-only methods. Evaluations across three model families (3B–8B), two training paradigms (SFT and DPO), six attack types, and two datasets show consistent ASR reductions of 1.6× to 9.2× on gradient-based attacks compared to prior IH injection mechanisms (delimiters, ISE), with minimal utility degradation.

## Strengths

- **Well-motivated core insight (Section 3, Fig. 3).** The paper empirically demonstrates that input-only IH signals (delimiters, ISE) lose discriminability as token representations propagate through deeper layers, with cosine similarity between different privilege levels converging toward 1.0. This observation is clean, testable, and directly motivates the architectural intervention of per-layer injection.

- **Simple, low-overhead method (Section 4).** AIR adds one trainable embedding vector per privilege level per decoder layer — only ~0.4M parameters (0.005% increase for Llama-3.1-8B with 3 privilege levels). The design is clearly specified (Eq. 1, Fig. 4) and the analogy to the shift from input-only positional encoding to per-layer RoPE provides an intuitive justification.

- **Comprehensive experimental evaluation (Sections 5–6, Table 1, Figs. 6–8).** The evaluation covers three model families (Llama-3.2-3B, Qwen-2.5-7B, Llama-3.1-8B), two training paradigms (full SFT, LoRA DPO), both static attacks (Naive, Ignore, Completion, Escape Separation) and gradient-based attacks (GCG, Astra), and two datasets (AlpacaFarm, SEP). This is the most systematic comparison of IH injection mechanisms in a single paper, and includes combinations (e.g., AIR+DPO, ISE+DPO) not explored in prior work.

- **Large, consistent improvements on gradient-based attacks.** The empirical gains are dramatic and nearly monotonic. For example, on Llama-3.2-3B with SFT, GCG ASR drops from 38% (Delim) to 4.1% (AIR); with DPO, from 29.1% to 5.2%. The GCG loss curves (Fig. 7) show non-overlapping standard deviation bands, confirming robustness. SEP separation scores also favor AIR, especially with DPO.

## Weaknesses

### Major

- **No adaptive attack evaluation.** AIR is evaluated against standard gradient-based attacks (GCG, Astra) designed without knowledge of AIR's per-layer IH embeddings. For a defense paper, the relevant threat model includes an adaptive adversary who knows the mechanism and crafts attacks to bypass it — e.g., optimizing a prefix that minimizes the influence of per-layer IH embeddings or "cancels out" the IH signal. The paper neither evaluates such attacks nor discusses this as a limitation. This does not invalidate the contribution (the paper shows improvement over prior methods under the standard evaluation protocol), but it bounds the strength of the robustness claims.

- **ASR results in Table 1 reported without variance or replication information.** Table 1 reports attack success rates as point estimates without standard deviations, confidence intervals, or number of independent runs. This is a concrete evidential gap: (a) several comparisons involve small absolute differences where sampling noise could flip rankings (e.g., SEP: Delim 3.1 vs AIR 2.7 on Llama-3.2-3B SFT; GCG: ISE 4.0 vs AIR 2.8 on Llama-3.1-8B DPO); (b) gradient-based attacks use stochastic optimization (random prefix initialization), making single-run ASR values unreliable. While Fig. 7 provides standard deviation bands for GCG loss curves, the ASR point estimates in Table 1 are not tied to these bands, and the paper does not state whether they come from the same runs or separate evaluations.

### Minor

- **No ablation isolating per-layer injection from additional capacity.** AIR introduces (layers × privilege levels) trainable vectors — 99 vectors for a 32-layer, 3-level model. A natural control would be an AIR-Input variant that concentrates the same total number of trainable IH-related parameters at the input layer only (e.g., 99 input-level IH embeddings). This would cleanly separate whether the improvement is due to per-layer injection or simply having more IH-encoding capacity. While the overhead is tiny (0.4M parameters), the architectural claim is about distribution across layers, not about capacity.

- **Cosine similarity motivation (Fig. 3) is cleaner for ISE than for delimiters.** For the delimiter method, the IH signal is carried by actual tokens ([INST], [INPT]) that persist through all layers, and their near-1.0 cosine similarity is a known phenomenon (token representations become more uniform in deeper layers). This does not necessarily indicate signal "degradation" — the model can still attend to these tokens. The paper uses "hypothesize" language throughout, which tempers this concern, and the empirical validation of AIR stands independently. Nevertheless, the framing of Fig. 3 as evidence of failure for all prior methods is slightly overstated for the delimiter case.

- **SFT vs. DPO comparison is confounded by training procedure (Section 5.2).** SFT uses full fine-tuning while DPO uses LoRA (parameter-efficient fine-tuning). Within-paradigm comparisons (AIR vs. baselines under SFT, or under DPO) are fair, but the paper's observation that DPO yields "more robust models than SFT" is confounded by the different training procedures. The paper's main claims do not depend on this cross-paradigm comparison, so this does not affect the core contribution.

- **No limitations section.** The paper lacks an explicit discussion of limitations. Acknowledging the scope of evaluation (adaptive attacks not considered, fixed number of privilege levels, reliance on standard attack benchmarks) would improve rigor.

### Trivial

None beyond the minor points above.

## Nice-to-Haves

- A study of how AIR scales with more privilege levels (the paper uses 3; real deployments may need more).
- A variant that injects IH at only a subset of layers to understand the minimum injection density required.
- Clarification in the text on whether the IH embedding is added exactly at the block input (as shown in Fig. 4) or at additional locations within the block.
- Discussion of potential judge model bias in AlpacaEval 2.0 (the judge model Llama-3-70B-Instruct shares a family with some evaluated models).

## Removed Points

*These points are flagged to be removed; treat them with caution.*

- **"Code and data release not specified."** — Removed per hard rule: questioning artifact availability is not permissible.
- **"Table 1 'None' column header is confusing."** — Removed as a formatting nitpick.
- **"The paper should have a conclusion."** — The paper has a conclusion (Section 7). Factually incorrect; removed.
- **Generic strength ("addressed an important problem").** — Removed per filtering rules as insufficiently specific to this paper.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. **Add an adaptive-attack evaluation**, or at minimum add a limitations paragraph discussing the threat model and why adaptive attacks were not evaluated. A concrete design: a variant of GCG that augments the loss to minimize the influence of per-layer IH embeddings.
2. **Report ASR in Table 1 with standard deviations and number of independent runs.** Specify whether the ASR numbers derive from the same runs used for the loss curves in Fig. 7.
3. **Add the input-only parameter-matched ablation (AIR-Input)** to isolate whether the improvement is due to per-layer injection or additional IH-encoding capacity.
4. **Add a limitations section** explicitly discussing the scope of evaluation, including adaptive attacks, fixed hierarchy structure, and potential overfitting to the evaluated attacks.
5. **Clarify the exact placement of the IH embedding** within the decoder block in the text (Eq. 1 is clear, but a sentence specifying "at the input to each decoder block, before the first layer norm" would remove ambiguity).

## Calibration Report

Anchors retrieved across all rounds (topically similar papers from the review corpus):

| Paper | Score | Round | Comparison |
|---|---|---|---|
| Instructional Segment Embedding (ISE) | 6.00 | R2 | Direct baseline; AIR improves upon ISE with per-layer injection and more comprehensive evaluation, while ISE scored 6 across all reviewers |
| Toward Robust Defenses Against LLM Weight Tampering (TAR) | 5.83 | R2 | Similar defense paper with comparable concerns about evaluation scope; accepted |
| Baseline Defenses for Adversarial Attacks | 5.25 | R1 | Studied existing defenses without novel method; less strong than AIR |
| Inverse Prompt Engineering for LLM Safety | 3.00 | R1 | Poorly executed with weak experiments; much weaker than AIR |
| Safety Alignment Should Be Made More Than Just a Few Tokens Deep | 9.50 | R1 | Very strong paper with broad implications; stronger than AIR |
| Deciphering the Chaos: Enhancing Jailbreak Attacks | 5.75 | R2 | Attack paper; comparable execution quality to AIR but different task |

**Round 1 bracket:** 4.0–7.0 (based on topical similarity to defense papers in the 3.0–6.0 range and the stronger 8.0+ papers).

**Round 2 narrowing:** Comparing directly against ISE (6.00), which AIR demonstrably improves upon with a cleaner architectural insight and broader evaluation, the score should be at least 6.0. The missing adaptive attacks and variance reporting prevent it from reaching 7.0+, but do not undermine the core contribution. The paper is comparable to TAR (5.83) and clearly stronger than Inverse Prompt Engineering (3.0) or Baseline Defenses (5.25).

**Final calibration:** 6.0 — a solid paper with a genuine contribution, sound evaluation methodology, and clear empirical evidence, held back from a higher score by the absence of adaptive attack evaluation and limited variance reporting.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>