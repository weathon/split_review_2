Now I have a good calibration. Let me write the final review.

**Round-1 bracket:** Based on comparisons with anchor papers, the narrowest plausible range is **5.5–6.5**. The paper sits near the "Transformers are Universal In-context Learners" (6.67, Accept) and "How Transformers Implement Induction Heads" (6.20, Reject) in terms of theoretical depth and empirical support. It is stronger than "Vocabulary In-Context Learning" (6.00, Reject) which had more mixed reviews, and "On Limitation of Transformer for Learning HMMs" (5.25, Reject) which had weaker theory and more significant experimental concerns. However, it has more framing and presentation issues than the "Universal In-context Learners" paper.

**Final score: 6.0** — The paper has a genuine theoretical contribution (clean proof of injectivity at initialization via real-analyticity), a principled algorithm, and reasonable empirical validation. The weaknesses are all minor and addressable (framing overreach, limited inversion scope, unexplained quantization anomaly). The core result is sound and the paper is well-structured.

**Anchor papers used for calibration:**
1. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/YE6N8htoFQ.md` — 6.00, Reject — Theory paper on ICL with mixed reviews; current paper has a clearer narrative arc (theory → algorithm → experiments).
2. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/b5lXUwZiD3.md` — 5.25, Reject — Empirical study on Transformers learning HMMs; current paper has stronger theoretical contribution.
3. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/NHhjczmJjo.md` — 7.00, Accept — Strong theory + experiments on ICL sparse recovery; current paper is less rigorous in its theoretical depth but has a practical algorithm.
4. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/6S4WQD1LZR.md` — 6.67, Accept — Universal approximation theory for Transformers; current paper has more applied components but weaker pure theory.
5. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/1lFZusYFHq.md` — 6.20, Reject — Theory + experiments on induction heads; similar balance of theory and experiments, but current paper has a cleaner contribution.
6. `/home/wg25r/split_review_opus_repro/datasets/deepreview_13k_calibration/ikwEDva1JZ.md` — 6.50, Accept — ICL theory + experiments; similar quality of contribution with a more focused theoretical result.

The current paper is most comparable to the 6.0–6.5 range papers. It has a solid theoretical core but needs better framing and more comprehensive inversion experiments to be a stronger accept.

Here is the final review:

## Summary

This paper proves that decoder-only Transformer language models are almost surely injective on discrete prompt spaces (distinct prompts → distinct last-token hidden states) using a real-analyticity framework. The proof covers both initialization (Theorem 2.2) and preservation under gradient-based training (Theorem 2.3). Building on this, the paper introduces SIFT/SIPIT, an algorithm that recovers the exact input text from hidden states with worst-case O(T·|V|) guarantees and practical efficiency via gradient-guided candidate selection. Empirical collision searches across six model families (GPT-2, Gemma3, Llama-3.1, Mistral-7B, Phi-4, TinyStories) find no collisions, and inversion experiments on GPT-2 Small and quantized large models achieve 100% accuracy.

## Strengths

**1. The real-analyticity framework provides a clean and elegant proof of injectivity at initialization.** The observation that Transformer components (LayerNorm with ε>0, softmax, GELU, residual connections) compose into a real-analytic function of parameters is well-articulated. Applying the real-analytic dichotomy (identically zero vs. measure-zero zero set) to the pairwise difference function h(θ) = ‖r(s;θ) − r(s′;θ)‖² is a clever way to turn the collision question into a topological property. The constructive demonstration of a separating parameter setting for any pair s≠s′ (lines 87–88) closes the argument concretely.

**2. SIFT/SIPIT is a principled algorithm that follows naturally from the theoretical guarantee.** The algorithm's structure (Algorithm 1) is essentially forced by injectivity plus causality: at each position, the recovered prefix means trying vocabulary candidates until one matches the observed hidden state must identify the correct token. The gradient-guided candidate policy (§3, evaluated in §4.2) makes it practically efficient (exploring ~0.2% of vocabulary). Theorem 3.2 (robustness under bounded noise) adds practical relevance.

**3. Extensive model coverage for the collision search.** The empirical collision search spans GPT-2 (Small/Medium/Large), Gemma3 (1B/4B/12B), Llama-3.1-8B, Mistral-7B-v0.1, Phi-4-mini-instruct, TinyStories-33M, plus large-scale models Phi-4 (14B) and Llama-3.1-70B under quantization. The consistent finding of no collisions across this breadth strengthens confidence in the theoretical claim.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

**1. Framing overstates the result relative to its actual scope.** The title "Language Models are Injective" and the rhetorical contrast with "conventional wisdom that Transformers are lossy" (lines 13–14, 331) imply a stronger claim than what is proven. The paper formally establishes injectivity for the *discrete-to-continuous* map (s ∈ 𝒱^{≤K} → r(s;θ) ∈ ℝ^d) — a finite-domain property. The cited concerns about non-injectivity (Dong et al. 2021 on rank decay, Yang et al. 2018 on softmax bottleneck) are about *continuous-to-continuous* maps in the embedding space — a different function. While Section 5 (lines 333) correctly clarifies this distinction, the abstract and introduction frame the result as challenging a broad "lossy" view without clearly demarcating this scope difference. The core result is genuinely interesting as stated; a more precise framing would make the paper stronger.

**2. Unexplained quantization distance anomaly.** Table 2 shows INT8 quantization producing *larger* minimum distances than FP4 (e.g., Llama-3.1-8B: 6.597 for INT8 vs. 2.281 for FP4 vs. 1.274 for FP32). INT8 is generally more precise (less noisy) than FP4, so one would expect INT8 distances to be *closer* to the FP32 baseline than FP4 distances. The paper claims quantization "more than doubles the minimum distance" (line 287) without commentary. This unusual pattern either warrants an explanation or suggests a measurement issue.

**3. Limited scope of the exact inversion experiments.** The primary inversion results (Table 5) are conducted on GPT-2 Small only (100 prompts, 20 tokens). Larger models (Mistral-7B, Llama-3.1-8B) appear only under FP4 quantization (Table 4, 50 prompts, 10 tokens). This asymmetry with the collision search (which covers six model families at full precision) leaves the inversion claims narrower than the collision claims. Demonstrating inversion on at least one non-quantized large model would close this gap.

**4. The HARDPROMPTS comparison is of limited value.** HARDPROMPTS (Wen et al., 2023) is a prompt-optimization method for a different task, not a hidden-state inversion method. Its 0.00 accuracy (Table 5) is inevitable given the task mismatch and does not meaningfully contextualize SIFT's performance. The paper acknowledges the task mismatch (lines 311–312) but including it as a primary baseline inflates the apparent margin of improvement. The BRUTEFORCE ablation is the more informative comparison.

**5. The legal/practical implications are overstated relative to what is demonstrated.** The conclusion (lines 349–350) argues that "any system that stores, caches, or transmits hidden states is effectively handling the user's verbatim text." This argument conflates theoretical injectivity (the map is one-to-one) with practical recoverability. SIFT requires access to model parameters, per-position hidden states at a specified layer, and assumes no significant noise — conditions the paper acknowledges (§3, line 141: exact recovery from "only the final embedding" is future work). The regulatory argument goes beyond what the current empirical results support.

### Trivial
None.

## Nice-to-Haves
- Inversion results on at least one non-quantized large model (e.g., Gemma3-1B, Mistral-7B) to match the breadth of the collision experiments.
- An explanation for the INT8 > FP4 distance anomaly in Table 2.
- Clarifying in complexity claims (e.g., "linear in sequence length" rather than "linear time") that |V| is the constant vocabulary size.
- A more precise title (e.g., "Almost-Sure Injectivity of Decoder-Only Transformers on Discrete Prompt Spaces") would reduce framing concerns.

## Removed Points
- **Criticism that injectivity on a finite domain is "nearly trivial":** Removed because it is incorrect as stated. Proving that a specific complex function (a Transformer) is injective — even on a finite set — is non-trivial. The critic's claim that "any function from a finite set to ℝ^d with d ≥ 1 is injective provided no two inputs map to the exact same point" is a tautology describing injectivity itself, not a reason it is easy to prove.
- **Claimed gap in Theorem 2.3 proof (pushforward of absolutely continuous measure):** Removed from weaknesses. The full proof is in the stripped appendix (Theorems C.1, C.5). The critic admits they cannot verify whether the full version closes this gap. Per the filtering rules, a fatal flaw requires unambiguous evidence on the page, not speculation about a missing appendix. The main-text sketch, while terse, conveys the correct intuition (a local diffeomorphism with non-vanishing Jacobian preserves measure-zero sets under pushforward).
- **Criticism that the collision search (100k prompts) is a vanishingly small fraction of the space:** Removed. This is a standard sanity-check scale in ML papers; exhaustive verification over a combinatorial space is infeasible by design.
- **Strength: "Paper is clearly written":** Removed as generic and superficial.
- **Various section-by-section notes about missing appendix content:** Removed per rules (appendix stripped by parser).

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Reframe the practical/legal claims to match what SIFT actually demonstrates — a system that stores hidden states may be at risk of prompt reconstruction under specific conditions (model access, per-position states, limited noise), not an unconditional equivalence to "handling user's verbatim text."
2. Add inversion results on at least one non-quantized large model to bridge the gap between the collision and inversion experiments.
3. Explain the INT8 vs. FP4 distance anomaly in Table 2 — this is either an interesting phenomenon or an error that needs correction.
4. Consider a more precise title that acknowledges the discrete-domain nature of the injectivity result.

## Score and Decision

Round-1 bracket: 5.5–6.5 based on comparison with calibration anchors.

Anchor papers:
- "Transformers are Universal In-context Learners" (6.67, Accept): Stronger pure theory, weaker application; current paper is comparable in quality.
- "How Transformers Implement Induction Heads" (6.20, Reject): Similar balance of theory/experiments; current paper has a cleaner contribution narrative.
- "On the Learn-to-Optimize Capabilities of Transformers" (7.00, Accept): Stronger theoretical rigor; current paper is slightly below this level.
- "Vocabulary In-Context Learning" (6.00, Reject): Similar theoretical nature but more mixed reviews; current paper is slightly stronger.
- "On Limitation of Transformer for Learning HMMs" (5.25, Reject): Weaker theory; current paper is clearly above this.
- "How Do Transformers Learn In-Context Beyond Simple Functions?" (6.50, Accept): Similar quality; current paper has more framing issues.

Final score: 6.0. The paper has a genuine and sound theoretical contribution (injectivity via real-analyticity), a practical algorithm that flows from it, and reasonable empirical support. The weaknesses are all minor and addressable (framing overreach, limited inversion scope, unexplained quantization anomaly). None threaten the core claims. The paper would benefit from revision of the framing and broader inversion experiments.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>