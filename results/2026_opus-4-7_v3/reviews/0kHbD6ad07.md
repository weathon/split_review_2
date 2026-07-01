Now let me verify a few more specific claims about the paper's framing and the comparison details.Now I have a thorough understanding of the paper. Let me draft my review before calibration.Now let me run the calibration search — Round 1 bracketing.Let me read a few anchor papers for calibration.Now I have enough calibration data to form my bracket and write the final review.

**Round 1 bracket assessment:**
- The paper clearly sits above the 3-5 reject range — its theoretical contribution is clean, novel, and well-executed, unlike the incremental or poorly-proven papers in that band.
- It compares favorably to borderline-accept papers in the 6-6.5 range (like "Induction Heads" at 6.20, "Universal In-context Learners" at 6.67) because it has a more self-contained, practically relevant result with stronger empirical validation.
- It falls slightly below the strongest 7.5-8 papers (like "When can transformers reason" at 7.60, "Scaling Laws for Associative Memories" at 7.60) due to the theory-algorithm coherence gap and narrow algorithm evaluation.

**Initial bracket: 6.5–7.5**

Now let me produce the final review.

## Summary
This paper proves that decoder-only Transformer language models are almost-surely injective: the discrete-to-continuous map from prompts to last-token representations is injective for all but a measure-zero set of parameters, a property established at initialization (Theorem 2.2) and preserved under gradient-based training (Theorem 2.3). The authors validate this empirically through ~5 billion pairwise collision tests across 10+ model families, observing no collisions, and introduce SIFT/SIPIT, an algorithm that reconstructs exact input text from hidden activations with provable linear-time guarantees.

## Strengths
- **Clean and novel theoretical result.** The key insight — that while individual transformer components (LayerNorm, attention) are non-injective on continuous inputs, the *discrete*-to-continuous map from prompts to hidden states is almost surely injective — is genuinely clarifying. The proof strategy (real-analyticity → measure-zero collision sets → constructive existence of non-colliding parameters) is elegant. The construction in Theorem 2.2's proof, where attention is routed to the first mismatched position, is a particularly nice touch that makes the non-trivial step accessible.

- **Meaningful extension over prior work.** Sutter et al. (2025) proved injectivity only at initialization and with respect to the full hidden-state matrix. This paper extends to (i) preservation under training via absolute continuity (Theorem 2.3), and (ii) the operationally relevant last-token state. The SGD/mini-batch extension (Corollary 2.3.1) is cleanly handled.

- **Thorough empirical validation of the theory.** Testing across GPT-2 S/M/L, Gemma-3 1B/4B/12B, Llama-3.1-8B/70B, Mistral-7B, Phi-4-mini, TinyStories-33M, and Phi-4 14B with ~5 billion pairwise comparisons and observing minimum L2 distances consistently orders of magnitude above the collision threshold (Table 1, Figure 3) provides strong corroboration. The stress test on closest-prefix prompts (Figure 4) and the layer-by-layer distance growth analysis add rigor.

- **Surprising quantization results.** The finding that FP4 and INT8 quantization preserves and even *increases* minimum pairwise distances (Tables 2, 3) is both surprising and practically relevant, since quantization breaks the analyticity assumptions.

## Weaknesses

### Fatal
None

### Major
- **Theory–algorithm coherence gap.** The theory proves injectivity at the last-token state alone (Theorem 2.2; footnote 2: "the last-token state... is the property of real operational interest"). However, SIPIT requires access to the *entire* hidden-state matrix H^(ℓ) ∈ ℝ^{T×d} — all per-position states at a given layer. The paper acknowledges this explicitly (§3: "designing an efficient algorithm for [the last-token-only] setting is nontrivial and left to future work"). This means the algorithm does not operationalize the proven injectivity result but rather a strictly easier problem (recovering from T·d values rather than d values). The abstract and introduction frame SIFT as turning "injectivity into an operational tool," which overstates the connection. This is not a flaw in either the theory or the algorithm individually, but it is a coherence problem in the paper's narrative arc.

- **Narrow experimental evaluation of SIFT.** The main inversion comparison (Table 5) uses only GPT-2 Small (117M parameters) with 20-token prompts. The larger-model experiments (Table 4: Mistral-7B, Llama-3.1-8B) use FP4-quantized models and only 10-token prompts. Given the paper's broad claims about "language models" generally and privacy implications in §6, demonstrating exact recovery on at least one modern full-precision 7B+ model with realistic-length sequences would substantially strengthen the paper.

### Minor
- **Training preservation does not cover Adam/AdamW.** Theorem 2.3 covers GD with step sizes in (0,1) and extends to SGD/mini-batch GD, but all tested pre-trained models (GPT-2, Gemma-3, Llama, Mistral, Phi-4) were trained with Adam or AdamW. The initialization result (Theorem 2.2) still applies, and the empirical collision tests confirm no issues, so the practical impact is limited. However, the formal gap between what is proven and what is tested should be acknowledged more explicitly. The extension to Adam should be straightforward (the update map involves analytic operations with ε > 0 keeping denominators positive), making this a missed opportunity rather than a fundamental gap.

- **Privacy/regulatory overreach in §6.** The paper claims "hidden states are not abstractions but the prompt in disguise: any system that stores or transmits them is effectively handling user text itself." While mathematically supported by the injectivity theorem, practical recovery via SIPIT requires white-box access to all model weights and all per-position hidden states — a highly restrictive threat model. The regulatory conclusions drawn in §6 significantly exceed what the results actually establish for realistic deployment scenarios. The paper would be stronger if it distinguished between theoretical recoverability and practical exploitability.

- **HARDPROMPTS baseline is uninformative.** Table 5 compares against HARDPROMPTS (Wen et al., 2023), designed for approximate prompt discovery to match a target output — a fundamentally different task. Its 0.00 accuracy is expected and not revealing. Thomas et al. (2025), cited in §5 as tackling the same sequential recovery problem, would have been a more meaningful comparison. The BRUTEFORCE ablation is the relevant comparison point and does demonstrate SIPIT's practical speedup.

### Trivial
None

## Nice-to-Haves
- Extend the training preservation proof to Adam/AdamW to eliminate the gap between theory and tested models.
- Provide any quantitative lower bound on the separation Δ (Theorem 3.2) — even asymptotic or probabilistic — to connect mathematical injectivity to numerically exploitable injectivity.
- Discuss weight tying (input/output embedding sharing), standard in many tested models, and whether the measure-zero argument accommodates it.
- Develop even a partial algorithm for inversion from the last-token state alone to tighten the theory-to-practice narrative.

## Removed Points
These points are flagged to be removed, treat them with caution:

- **"GELU implementation caveat"**: The reviewer noted some implementations use piecewise approximations of GELU. The paper's theory concerns the mathematical function, not floating-point implementation. The paper correctly states GELU is real-analytic; this is not a meaningful weakness.
- **"Interpretability implications are modest"**: The reviewer called the probing implication "somewhat trivial" since linear probing failures were already understood as failures of the linear assumption. While the incremental practical import is limited, formally establishing that information is never lost is a genuine (if modest) contribution to the interpretability literature. This does not rise to the level of a weakness.
- **"Naming inconsistency (SIFT/SIPIT/SIpIT/SiPT)"**: Pure formatting/naming issue, removed per rules.
- **"Weight tying discussion missing"**: While potentially interesting, weight tying does not force shared embeddings for different tokens, and the measure-zero argument should hold. Moved to nice-to-have rather than weakness.

## Novel Insights
The paper's central novel insight is that the discrete nature of the prompt domain fundamentally changes the injectivity picture for transformers: while individual components are non-injective on ℝ^d, the countable prompt space means collision sets (each measure-zero by real-analyticity) remain measure-zero even under countable union. The training preservation argument — that finite GD steps preserve absolute continuity and therefore cannot map parameters onto the measure-zero collision set — is a clean, reusable technique. The empirical finding that quantization *increases* rather than decreases minimum pairwise distances, despite breaking the analyticity assumptions, is a noteworthy observation that invites further theoretical investigation.

## Suggestions
- Close the theory–algorithm gap by developing (even partial) inversion from the last-token state alone, or by proving computational tractability of last-token-only inversion under certain conditions. This would dramatically tighten the narrative.
- Run SIFT on at least one full-precision 7B+ model with 50+ token prompts to substantiate the broader claims.
- Temper §6's regulatory discussion to distinguish between theoretical recoverability and practical threat models with realistic access assumptions.
- Compare against Thomas et al. (2025) as a more appropriate baseline for sequential prompt recovery.
- Explicitly discuss the Adam/AdamW gap and either prove the extension or state it as a conjecture with supporting intuition.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Not comparable; survey paper with no contribution |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.00 | R1 | Not comparable; pseudoscientific |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Not comparable; shallow attack paper |
| Financial Markets Neural Network | nSDOkm0SKo | 1.00 | R1 | Not comparable; no real contribution |
| Inductive Transformers | NSBP7HzA5Z | 3.00 | R1 | Much weaker; vague theoretical contribution, inconsistent reviews |
| Recovering Knowledge by Hardening LMs | uOnElfFuey | 3.00 | R1 | Much weaker; limited novelty, narrow scope |
| Llamas think in English | fSbPwHjdDG | 3.00 | R1 | Weaker; empirical finding without strong theoretical grounding |
| Latent Space Theory for Emergent Abilities | 4y3GDTFv70 | 3.25 | R1 | Weaker; more speculative theory with less empirical support |
| Multi-Round LLM Reasoning | MRPCIForrE | 4.75 | R1 | Weaker; theoretical results considered incremental, proofs hard to follow |
| Variable-order Markov Chains | TdgAtxP6G2 | 4.00 | R1 | Weaker; narrower contribution, limited novelty |
| Depth Extrapolation of Decoders | fp77Ln5Hcc | 4.50 | R1 | Weaker; more limited theoretical result, mixed reviews |
| LLMs Are Not General Learners | e5lR6tySR7 | 4.00 | R1 | Weaker; mostly negative results with limited practical implications |
| When Can Transformers Count to n? | WULjblaCoc | 5.60 | R1 | Weaker; narrower theoretical result, less practical relevance |
| Vocabulary In-Context Learning | YE6N8htoFQ | 6.00 | R1 | Similar tier but less practical relevance; this paper is stronger |
| How Transformers Implement Induction Heads | 1lFZusYFHq | 6.20 | R1 | Similar but incremental; this paper has a cleaner, more novel contribution |
| Transformers are Universal In-context Learners | 6S4WQD1LZR | 6.67 | R1 | Comparable; elegant theory but less practical import. This paper is slightly stronger due to empirical validation and algorithmic contribution |
| When can transformers reason with abstract symbols? | STUGfUz8ob | 7.60 | R1 | Comparable quality of theory, stronger empirical validation in that paper. Slightly stronger due to tighter theory-practice connection |
| Scaling Laws for Associative Memories | Tzh6xAJSll | 7.60 | R1 | Strong theory paper with precise scaling laws; comparable in quality but tighter narrative |
| Context-Parametric Inversion | SPS6HzVzyt | 8.00 | R1 | Stronger; more impactful empirical findings with tighter theoretical grounding |
| Small-scale proxies for training instabilities | d8w0pmvXbZ | 8.00 | R1 | Stronger; direct practical impact and comprehensive experiments |

**Round 1 bracket: 6.5–7.5**

**Narrowing rationale:** The paper's core theoretical contribution (injectivity proof + training preservation) is genuinely novel, clean, and well-validated empirically through collision tests. This places it above the 6.0-6.5 borderline-accept papers that have solid but incremental theory. However, the theory-algorithm coherence gap, narrow SIFT evaluation, and §6 overreach prevent it from reaching the 7.5+ papers where theory and practice are tightly integrated. The paper sits in the upper portion of the bracket — the theory alone is a strong contribution, and the empirical collision validation is excellent. The algorithm, despite the gap, adds practical value. 

**Final score: 7.0**

This is a solid theory paper that makes a genuine, novel contribution to understanding transformer representations. The injectivity result is clean, the proof technique is elegant and potentially reusable, and the empirical validation is thorough. The main weaknesses — the theory-algorithm gap and narrow algorithm evaluation — weaken the broader narrative but do not undermine the core theoretical contribution. The paper merits acceptance as a meaningful advance in our understanding of transformer architectures, though the practical framing would benefit from more careful scoping.

MY FINAL SCORE: <score>7.0</score>
MY FINAL DECISION: <decision>Accept</decision>