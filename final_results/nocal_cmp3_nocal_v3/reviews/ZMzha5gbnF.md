Now I have all the verification I need. Let me write the consolidated review.

## Summary
2-3 sentence summary of the paper's contribution.

The paper identifies a novel "priming vulnerability" in Masked Diffusion Language Models (MDLMs): when tokens consistent with a harmful response appear at intermediate denoising steps, even safety-aligned models are steered toward harmful completions. The authors analyze this vulnerability under two threat models (intervention and non-intervention), propose Recovery Alignment (RA) — a method that trains models to generate safe responses from intentionally contaminated intermediate states — and demonstrate that RA dramatically reduces attack success rates on multiple MDLMs with negligible utility degradation while also improving robustness against conventional jailbreak attacks.

## Strengths

1. **A genuinely novel vulnerability specific to the MDLM inference mechanism.** The paper clearly distinguishes the priming vulnerability from ARM prefilling attacks (Section 1, lines 17–33): in ARMs the effect is sequential and left-to-right, whereas in MDLMs the iterative parallel denoising means even a single unmasked token at step 1 can cascade through the full generation trajectory. This is a non-obvious structural consequence of the MDLM architecture and constitutes the paper's core contribution.

2. **Principled two-threat-model analysis (Section 4).** The paper separates analysis into (a) a hypothetical attacker who can intervene in the denoising process (anchoring attack, Section 4.1) and (b) a realistic attacker who can only modify the prompt (First-Step GCG, Section 4.2). The intervention setting cleanly establishes that the vulnerability exists and quantifies its severity; the non-intervention setting shows it is practically exploitable, not merely a theoretical artifact.

3. **Strong empirical results on the anchoring attack (Table 2).** RA reduces ASR from baselines of ~20–44% (at t_inter=4 on LLaDA/LLaDA 1.5) to near 0–1%. At t_inter=8, RA's ASR is 1.3% (LLaDA) and 0.7% (LLaDA 1.5) compared to 24–44% for MOSA and 31.7–42.7% for SFT. The ablation RA w/o inter (same data, same RLHF, but no contaminated states) confirms the benefit comes specifically from training on intermediate contaminated states rather than from alignment in general.

4. **Generalization beyond the specific vulnerability (Table 3).** RA improves ASR on PAIR from 44.3%→10.0% (LLaDA) and from 45.3%→16.0% (LLaDA 1.5). This is a genuine surprise — a method designed for a mechanism-specific MDLM attack also improves robustness against conversational attacks designed for ARMs — and substantially increases the significance of the contribution.

5. **Minimal utility degradation across 11 benchmarks (Table 4).** Average accuracy on LLaDA changes from 52.2% to 52.6%; on LLaDA 1.5 from 52.7% to 52.8%. For a safety alignment method, this is unusually clean.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **Theorem 4.1's assumption is insufficiently justified in the main text.** The theorem assumes log π_θ(𝐫̃_{t+1}=𝐫 | 𝐪, 𝐫_t) ≥ log π_θ(𝐫̃_1=𝐫 | 𝐪, 𝐫_0) for all t — i.e., that the log-likelihood of the target response increases monotonically as the denoising process progresses. The paper's rationale (lines 130–131) conflates *distributional concentration* (the model's probability mass narrows to fewer candidates at later steps) with the *probability of a specific string 𝐫* under potentially different conditioning contexts. If the already-unmasked tokens at step t are not from 𝐫, the conditional probability of exactly 𝐫 could be near zero, making the assumption fragile. The paper claims empirical validation in Appendix C.2, but the main-text justification alone is logically incomplete. This does not undermine the core contribution because (a) First-Step GCG's effectiveness is independently validated in Table 1 (20× speedup, 3–5× higher ASR than MC-GCG), and (b) the paper frames the theorem as motivation rather than as a necessary condition for the method to work. Nonetheless, the authors should either provide a more rigorous theoretical argument or clearly state that the theorem is a heuristic motivator validated empirically.

2. **RA's performance at late intervention steps receives insufficient analysis.** At t_inter=32, RA's ASR is 50.7% (LLaDA), 43.0% (LLaDA 1.5), and 79.3% (MMaDA) under the anchoring attack (Table 2). The paper acknowledges this briefly (line 241: "when the intervention step is very late...generating a fully safe response becomes challenging") and notes that excessively large t_max leads to "reward hacking, where the model generates responses that are meaningless" (line 315). However, the paper does not discuss what this means for practical security: an attacker who can inject tokens at step 32 (25% through denoising) can still succeed roughly half the time on the better models. The paper should either discuss whether the DPO-style alternative mentioned in Limitations could address late-step contamination, or explicitly characterize this as a bounded mitigation where the adversary's required control level determines the defense's reliability.

3. **The mechanism by which RA improves robustness against conventional jailbreak attacks is asserted but not analyzed.** The paper states that a "plausible mechanism" is that the model "re-detect[s] harmfulness at later steps" (lines 243, 301) and steers generation back to safety. This is explicitly framed as speculation ("plausible"), but no analysis of intermediate states during PAIR or Crescendo attacks is provided to support it. Without such evidence, the reader cannot distinguish between (a) a genuine recovery mechanism, (b) RA making the model more conservative across the board, or (c) an interaction between RA's training distribution and the specific attack surface. Adding a qualitative comparison of intermediate states for successful vs. failed defenses would substantially strengthen this finding.

4. **Limited discussion of sensitivity to generation length L and denoising steps T.** The paper fixes L=128 and T=128 without discussing how these choices affect the vulnerability or the mitigation. Since the vulnerability is about token injection into a fixed-length sequence and the masking schedule depends on T, the quantitative results could shift with different configurations. A brief analysis would improve the evaluation's robustness.

5. **Reward model specification is incomplete.** The reward model R is described as scoring "safety and usefulness" using DeBERTaV3 "without additional fine-tuning" (lines 196, 205), but it is unclear (a) whether it outputs a single scalar combining both dimensions, (b) how the two are weighted, and (c) how it was validated as a reliable safety signal for MDLM outputs. Since RA directly optimizes against this reward model, its quality is central to the method's success.

### Trivial

1. **The "affirmative token" terminology is imprecise.** The definition (line 84: "tokens which endorse or advance a harmful intent") is used throughout the paper, but the anchoring attack injects arbitrary tokens from a harmful response — including function words like "Lastly" (Figure 1). Any token from the harmful response can serve as a "primer," making the term circular: a token is "affirmative" because it is part of the harmful response, and it advances harm because it primes the model. A more mechanistic characterization (e.g., based on token position, distributional properties, or conditional probability effects) would improve clarity without affecting the paper's technical contribution.

## Nice-to-Haves

- **Characterize what kinds of tokens serve as effective primers.** The paper would be strengthened by a systematic experiment varying injected token type (random, semantically neutral, from a different harmful response, semantically affirmative) to determine whether the mechanism is semantic or distributional.
- **Provide intermediate-state analysis for conventional attacks.** Even a qualitative analysis of intermediate states (r_t) and token-level probability distributions during PAIR/Crescendo defenses would make the generalization claim more convincing.
- **Include at least one cross-evaluator comparison in the main text.** The paper defers all non-GPT-4o evaluator results (LLaMA Guard 3, keyword matching) and AdvBench results to the appendix. While space-constrained, a brief comparison would strengthen confidence that findings are not evaluator-specific.

## Removed Points
These points are flagged to be removed, treat them with caution:

- **Issue 2 from the harsh critic (Anchoring attack threat model conflates existence proof with severity).** REMOVED because the paper clearly states (a) "Harmful responses are generated by a non-safety-aligned model" (line 106–107), (b) the attacker is explicitly "hypothetical" (line 84), and (c) the anchoring attack procedure is fully specified (lines 88–89). The critic's concern that the "single token" framing might be misinterpreted does not reflect a flaw in the paper's transparent description of its own controlled experiment.

- **"Only GCG is tested" for optimization-based attacks.** REMOVED because the paper states "such as GCG" (line 35) and "focus on GCG as a concrete instantiation" (line 114) — it does not claim to exhaustively test all optimization-based attacks.

## Novel Insights
None beyond the paper's own contributions. The reviewer's analysis does not surface genuinely novel observations that the paper itself fails to articulate.

## Suggestions

1. In Section 4.2, add a caveat that Theorem 4.1 depends on an assumption that is empirically validated in the appendix but whose theoretical justification has known edge cases (e.g., when r_t contains tokens inconsistent with r).
2. Add a brief discussion of what RA's t_inter=32 failure rate implies for practical threat models, distinguishing between attackers with minimal vs. substantial control over the denoising process.
3. Include an analysis of intermediate states during conventional jailbreak attacks (PAIR, Crescendo) by comparing token-level probability distributions for RA vs. baseline models on successful and failed defenses.
4. Clarify the reward model specification: whether R outputs a single combined score, how safety and usefulness are weighted, and any validation of R's reliability on MDLM outputs.

## Score and Decision

<score>8</score>
<decision>Accept</decision>