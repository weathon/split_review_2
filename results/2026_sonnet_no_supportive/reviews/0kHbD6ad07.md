## Summary
This paper proves that decoder-only Transformer language models are almost-surely injective as maps from discrete prompt sequences to last-token hidden representations, and that this property is preserved under gradient-based training via a Jacobian non-degeneracy argument. Building on this result, the authors introduce SIpIT, an algorithm that recovers the exact input prompt from per-position hidden states at a fixed intermediate layer, with provable worst-case T·|V| forward-pass bound. Experiments covering up to 70B-parameter models with five billion pairwise collision tests empirically confirm the theory.

## Strengths
- **Theorem 2.2's proof strategy is genuinely elegant.** The key insight — that h(θ)=‖r(s;θ)−r(s′;θ)‖² is real-analytic, and the measure-zero zero-set property converts a single explicit witness into an almost-sure guarantee — is clean. The witness construction (attending to the first-mismatch position; distinct embeddings for position-differing prompts) is concrete and verifiable from §2.
- **Theorem 2.3 (training preservation) closes a critical gap.** Showing gradient descent preserves absolute continuity of the parameter law via the non-degenerate Jacobian of the update map φ(θ)=θ−η∇L(θ) ensures injectivity is not an initialization artifact. As stated at §2: "A single GD step is the map φ(θ)=θ−η∇L(θ)…its Jacobian determinant det Dφ(θ) is itself real-analytic and not identically zero…" This is the most substantive step and is non-trivial.
- **Empirical confirmation is appropriately scaled.** Five billion pairwise comparisons across models from GPT-2 to Llama-3.1-70B (Tables 1–3, Figures 3–5), quantized variants (Table 2), stress-tests with nearest-neighbor prefixes (Figure 4), and vocabulary-scaling robustness (Table 4) provide thorough coverage.
- **Clear differentiation from prior work.** §5 precisely distinguishes the last-token, training-preserving injectivity from Sutter et al. (2025)'s full-hidden-matrix, initialization-only result and Thomas et al. (2025)'s sequential recovery without exactness guarantees.

## Weaknesses

### Fatal
None.

### Major
- **Structural mismatch between the headline theorem and the algorithm.** Theorem 2.2/2.3 establishes injectivity of s↦r(s;θ) (last-token state). SIpIT, however, requires access to the full per-position hidden matrix H^(ℓ)∈ℝ^{T×d} at an intermediate layer (§3, Eq. 5, Algorithm 1). The paper acknowledges this in §3: "our injectivity result guarantees that exact recovery from only the final embedding is possible in principle, but designing an efficient algorithm for that setting is nontrivial and left to future work; here we assume access to all per-position states at a given layer ℓ." The acknowledgment is honest, but the two main contributions — last-token injectivity and efficient exact recovery — operate on different access models, and the privacy/interpretability claims in §6 conflate them. §6 states hidden states are "the prompt in disguise" and that "any system that stores or transmits them is effectively handling user text itself," yet SIpIT needs full per-position access while the injectivity proof guarantees only last-token losslessness. The paper would be stronger if these were more clearly separated in scope.
- **Missing direct comparison with Thomas et al. (2025).** §5 identifies Thomas et al. (2025) as "most closely related" — a sequential algorithm using an LLM-based policy to recover prompts from hidden states. The experimental baseline in §4.2 instead uses HARDPROMPTS (Wen et al., 2023), a gradient-based approximate prompt optimizer that the paper itself concedes was "designed for approximate prompt discovery." HARDPROMPTS achieving 0.00 accuracy in Table 5 tells the reader nothing about SIpIT's advantage over the specific prior art for this task. An empirical or even qualitative comparison with Thomas et al. is needed to substantiate the efficiency and exactness claims relative to the state of the art.

### Minor
- **"Linear time" framing needs explicit qualification.** The abstract, §1, and Theorem 3.1 all claim "linear-time guarantees." The T·|V| bound counts forward-pass invocations, not arithmetic operations; each forward pass costs at minimum O(t·d·L) operations. The cost model is never stated, and wall-clock runtimes in Table 4 (549 seconds for a 10-token prompt on Llama-3.1-8B) confirm this is not linear in a conventional sense. A single clarifying parenthetical ("linear in sequence length T, measured in forward-pass invocations") would prevent misreading.
- **Quantization observation lacks explanation (Table 2).** The paper claims FP4/INT8 quantization "more than doubles the minimum distance between representations" without any mechanistic explanation. This is counterintuitive — quantization reduces reachable parameter states, which could concentrate pairwise distances away from zero as a statistical artifact, but the paper does not note this possibility. A brief remark is warranted.
- **§6 mechanistic interpretability claim overstates the implication of injectivity.** §6 states: "if probes or inversion methods fail, it is not because the information is missing." Injectivity guarantees algebraic losslessness, not linear or computationally tractable accessibility. The logical gap between "injective encoding" and "probes should succeed" should be acknowledged with a qualifier.

### Trivial
None.

## Nice-to-Haves
- An ablation isolating the gradient-guided candidate policy (Algorithms 2/3) from the injectivity-based termination criterion would clarify which component drives SIpIT's speedup over BRUTEFORCE (Table 5: 28s vs. 3890s).
- A partial result bridging the last-token theory and the full-matrix algorithm — e.g., showing the last-token state alone suffices to recover the final token while the full matrix is needed for earlier positions — would significantly tighten the paper's narrative.
- A brief sentence in the main text (beyond the appendix) confirming that SwiGLU/SiLU are real-analytic would help readers not already familiar with the smooth approximation literature.

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **Jacobian non-degeneracy sketch is insufficient in the main paper.** The harsh critic notes the main paper's sketch for Theorem 2.3 defers to Appendix C. This is a criticism about a missing appendix proof and is removed under the hard rule — the full proof exists in the original submission.
- **"Related works that may be missing"** — Not raised but pre-emptively excluded; no external verification possible.
- **Threat model scope vs. §6 regulatory claims as a separate weakness.** This concern is partially merged into the Major structural-mismatch weakness above; the standalone version is redundant.

## Novel Insights
The paper's most distinctive contribution is not any individual ingredient but their combination: the real-analyticity of the full Transformer pipeline, applied to the *discrete-to-continuous* map s↦r(s;θ), yields an almost-sure guarantee that is (a) about the operationally relevant last-token state rather than the full hidden matrix, and (b) stable under gradient-based training — closing two gaps simultaneously that prior work addressed only one at a time. The Jacobian non-degeneracy argument for the gradient-descent update map is particularly clean and may have broader applicability to analyzing invariants of deep networks under standard training dynamics.

## Suggestions
- Add a sentence at the beginning of §3 explicitly stating that SIpIT's access model (full per-position hidden matrix) is strictly stronger than what Theorem 2.2/2.3 requires (last-token state), and scope the privacy claims in §6 accordingly.
- Include at least a runtime or qualitative accuracy comparison with Thomas et al. (2025) in §4.2; even a brief discussion of where their LLM-based policy stands relative to SIpIT's gradient-guided policy would address the most natural question.
- Replace "linear time" in the abstract/§1 with "linear in sequence length T, measured in forward-pass invocations" or similar.
- Add one sentence explaining why quantization increases minimum pairwise distances (Table 2), even speculatively.

---

## Calibration Anchors

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| 8QTpYC4smR.md | 1.00 | R1 | LLM survey with no technical contribution; no comparison |
| NSBP7HzA5Z.md | 3.00 | R1 | Informal inductive-bias transformer paper, lacks rigorous proofs |
| fp77Ln5Hcc.md | 4.50 | R1 | Theoretical decoder extrapolation study, narrower scope and thinner empirical base |
| nxQ0Bjp8zD.md | 5.00 | R1 | Theoretical ICL for mixture regression, solid but narrower and less empirically confirmed |
| 1lFZusYFHq.md | 6.20 | R1 | Approximation+optimization analysis of induction heads — comparable rigor, slightly narrower scope |
| ikwEDva1JZ.md | 6.50 | R1 | ICL with representations, comparable style, accepted |
| WULjblaCoc.md | 5.60 | R1 | Counting tasks in Transformers, solid theory but narrower |
| STUGfUz8ob.md | 7.60 | R1 | Abstract symbol reasoning with clean proofs and practical architecture changes |
| Tzh6xAJSll.md | 7.60 | R1 | Scaling laws for associative memories with rigorous derivations |
| dpDw5U04SU.md | 7.00 | R2 | Minimum-width universal approximation, clean tight theorem |
| yC2waD70Vj.md | 7.25 | R2 | Inverse approximation theory for RNNs, rigorous theory with applications |
| P7KIGdgW8S.md | 8.00 | R2 | Hölder stability of GNNs, very clean parametric separation analysis |
| uZfjFyPAvn.md | 6.80 | R2 | Implicit neural representations + algebra, niche but rigorous |

**Round 1 bracket:** Between 6 and 7.5. The paper is solidly above the 5–6 range (stronger theory, broader empirical scope, cleaner proofs) but the theory-algorithm access-model mismatch and absent Thomas et al. comparison keep it below the 7.5+ tier where the theoretical contribution ties more directly to its operational tool.

**Round 2 narrowing:** The second calibration confirms the 6.5–7 range as most appropriate. Papers at 7.0–7.25 (minimum-width universal approximation, inverse approximation for RNNs) are clean theorems with direct practical implications and no significant access-model gap between theory and application. This paper's acknowledged mismatch and comparison gap place it slightly below those, while its broader empirical validation and more operationally significant result place it above the 6.2 induction-head paper.

**Final score: 6.5**

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>