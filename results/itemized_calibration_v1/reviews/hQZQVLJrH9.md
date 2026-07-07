Now I have strong calibration. Let me finalize my review.

**Calibration Summary:**

**Closest anchors in order of relevance:**
1. **9wjGUN65tY** (avg 5.00) — Steering Vectors to Conceptors: novel theoretical connection, outperformed baselines, but no error bars, small models, unclear presentation. The paper under review has a more novel connection (steering↔influence are completely separate fields) but empirically loses to CAA, whereas conceptors beat additive steering.
2. **ZrnzGzUhNX** (avg 5.00) — Closed-Form Interpretation: theoretical interpretability paper with interesting idea but limited scope and unjustified assumptions. 
3. **JCCPtPDido** (avg 5.50) — Jet Expansions: strong theoretical development with serious exposition issues. The paper under review has cleaner exposition but concrete mathematical errors.

**Bracket (Round 1):** 3.5–5.5 based on comparison with these anchors.

**Narrowing:** The paper is stronger than 3.0-level papers (which lack novelty or have severe theoretical flaws), but below 5.0–5.5 papers because: (a) IAS empirically loses to CAA, unlike conceptors which beat baselines; (b) Equation (2) has a concrete error; (c) Corollary 1's proof is nonsensical; (d) key claimed benefits unvalidated. **Final score: 4.5.**

---

## Summary

This paper establishes a first-order equivalence between activation steering and influence functions through subspace projection. The core construction (IAS) computes the minimum-norm activation edit that reproduces a given parameter-space logit change. The paper derives an alignment diagnostic γ (the smallest principal angle between two Jacobian subspaces), a spectral optimality direction, and generalization bounds. Experiments on GPT-2 Medium (detoxification) and ResNet-50 (spectral direction) are presented.

## Strengths

1. **First formal connection between steering and influence.** Sections 3–5 present a mathematically coherent framework relating these previously separate techniques. The construction of IAS as Δh* = J_{h→y}^† J_{θ→y}Δθ (the minimum-norm activation edit matching an influence logit change) is sound and explicitly stated. The paper is the first to make this connection rigorous, giving practitioners a shared language.

2. **The γ diagnostic is well-motivated and computationally cheap.** The alignment cosine γ(x) (principal angle between Im(J_{θ→y}) and Im(J_{h→y})) provides a clear, computable criterion for when steering can approximate influence, requiring only two JVP/VJPs plus a small SVD. The empirical finding that γ increases with layer depth (Figure 2, from 0.64 at L0 to 0.94 at L11) matches intuition and is a clean observation.

3. **The spectral optimality direction (Theorem 5.3) is a principled alternative.** Rather than hand-crafting steering vectors from prompt contrasts, the top eigenvector of Σ provides a theoretically grounded choice. The recipe to estimate it via power iteration over mini-batches is practical.

## Weaknesses

### Fatal
None.

### Major

1. **Equation (2) contains a concrete mathematical error.** The paper states Δh* = J_{h→y}^T J_{θ→y}Δθ (line 84). The correct derivation from the Lagrangian yields Δh* = J_{h→y}^T (J_{h→y}J_{h→y}^T)^† J_{θ→y}Δθ = J_{h→y}^† J_{θ→y}Δθ. The published expression is missing the pseudoinverse (J_{h→y}J_{h→y}^T)^†. Theorem 5.2 correctly states Δh* = J_{h→y}^† J_{θ→y}Δθ, so the error is confined to equation (2), but it is an inconsistency that would produce incorrect numerical results if implemented as written.

2. **The experimental evidence does not support the paper's practical claims.**
   - **Table 1 (detoxification):** IAS produces *worse* toxicity (0.0164) and *worse* perplexity (13701) than CAA (0.0150, 13291). The paper presents these numbers without comment, error bars, or statistical tests. IAS is better than the baseline but strictly worse than the existing method it is compared against.
   - **Figure 1 slope discrepancy:** The reported slope is 1.50, meaning actual logit shifts are 50% larger than first-order predictions, yet the caption calls this "consistent with the expected linear regime." A 50% systematic deviation from unity is not explained and undermines the claimed fidelity of the first-order approximation. No analysis of this discrepancy is provided.
   - **Section 7.4 (spectral optimality):** Only shows the spectral direction is better than random (p≈0.005), with no comparison to existing steering methods, no downstream task evaluation, and no demonstration of useful behavior change.
   - **Data-provenance claim unvalidated:** Corollary 1 states that steering vectors can be mapped back to "causal training examples," but no experiment actually traces a steering vector to training examples and verifies their causal role (e.g., via removal or re-labeling).
   - **γ threshold unvalidated:** The paper recommends γ < 0.5 as a threshold to "skip steering and switch to weight-space editing" (line 206) but never experimentally tests this decision rule.

3. **Overstated framing of the "equivalence."** The central result is subspace projection — the minimum-norm solution to a linear system — wrapped in primal-dual language that adds rhetorical weight. The paper states the subspace-inclusion condition but then proceeds as if equivalence is the normal case, when even at the best layer (γ=0.94) the bound allows up to √(1−0.94²) ≈ 34% relative logit error. For most layers where γ is lower, the equivalence degrades rapidly.

### Minor

4. **Corollary 1's proof sketch is nonsensical.** The argument claims that if another measure ν had smaller ℓ₁ norm, "one could scale ρ_s down and still match the shift, contradicting the definition of α as the steering magnitude." This does not follow — a smaller ℓ₁ norm for ν does not imply ρ_s can be scaled down. The sketch provides no actual justification for ℓ₁-minimality.

5. **Several results are standard or derivative.** Theorem 6.1 (Rademacher complexity) is directly applied from Pinto et al. (2024) and applies to any rank-k perturbation, providing no steering-specific insight. Theorem 6.2 restates the principal-angle bound from Theorem 5.1. Corollary 2 is a standard Taylor remainder bound under an unverified κ-Lipschitz assumption. These results add length but not depth to the steering-influence narrative.

6. **No engagement with known influence-function fragility.** Basu et al. (2021) ("Influence functions in deep learning are fragile") appears only in the references. The main text does not discuss how damping λ trades off bias vs. stability or whether the resulting influence vectors are reliable enough for the mapping, despite the entire framework depending on influence computations.

7. **No measures of uncertainty.** Every quantitative result (Table 1, Figure 1 cosine/slope, Figure 3 p-value) lacks error bars, variance estimates, or multiple seeds, making single-run artifacts impossible to rule out.

8. **Single model for primary experiments.** All language experiments use only GPT-2 Medium. Results on at least one larger model (e.g., Llama 2 7B) would be needed to claim scalability.

### Trivial
- Lemma 5.4's rewritten form on line 186 (γ = √(1−(1−γ²))) is an identity, making the rewriting circular; only the inequality γ₁₂ ≥ γ₁γ₂ carries content.

## Nice-to-Haves
- Validate the data-provenance pipeline: trace a steering vector to training examples and verify causality via removal or re-labeling.
- Test the γ < 0.5 threshold experimentally: compare always-steer, always-edit, and γ-based switching.
- Include larger models (e.g., Llama 2 7B) and provide error bars.
- Analyze the slope 1.50 discrepancy in Figure 1 (is it from Taylor remainders? specific influence computation? layer choice?).

## Removed Points
- "The central 'equivalence' is straightforward linear algebra, not a deep duality" → Kept in modified form as Major weakness 3 (overstated framing); the primal-dual framing is technically correct for the quadratic program.
- "Claim that practitioners face 'an unsatisfying dichotomy' is overstated" → Subjective interpretation; the paper's motivation is reasonable.
- "Theorem 6.2 name 'No-Free-Lunch' is disproportionate" → Purely a naming complaint; substance already covered.
- "Section-by-section granular notes" → Distilled into structured weaknesses.
- "Strengthening the Paper on Its Own Terms" section → Redundant with Nice-to-Haves.
- Generic strengths ("addressed an important problem", "targeted an interesting question") → Dropped; only concrete, evidenced strengths retained.

## Novel Insights
None beyond the paper's own contributions.

## Suggestions
1. Fix the mathematical error in Equation (2) to match Theorem 5.2.
2. Provide a proper proof for Corollary 1's ℓ₁-minimality claim, or cite a known result.
3. Add error bars / multiple seeds to all experiments.
4. Explain the slope 1.50 in Figure 1 or adjust the claim about linearity.
5. Validate the data-provenance pipeline end-to-end.
6. Validate the γ threshold decision rule experimentally.
7. Add discussion of influence function fragility (Basu et al., 2021).
8. Include at least one larger model (e.g., Llama 2 7B).

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Itemized? | Comparison |
|------|-----------|-------|-----------|------------|
| nSDOkm0SKo.md | 1.00 | R1 | No | Unrelated finance paper, not comparable |
| Uj0h13lVrR.md | 1.00 | R1 | No | Unrelated GFlowNets paper, not comparable |
| u1cQYxRI1H.md | 0.50 | R1 | No | Unrelated diffusion paper, not comparable |
| gwZ90hFSL2.md | 1.00 | R1 | No | Unrelated robotics paper, not comparable |
| fdvSCcB7i8.md | 3.00 | R1 | Yes | Instance attribution paper; weaker theoretical novelty than current paper |
| WT2bL7sCM1.md | 3.00 | R1 | Yes | Hessian-free IF paper; had serious theoretical confusion |
| z1yI8uoVU3.md | 3.00 | R1 | Yes | Steering evaluation paper; limited novelty, small models |
| v5lmhckxlu.md | 3.40 | R1 | No | Model explanation paper; less directly comparable |
| esYrEndGsr.md | 3.75 | R1 | Yes | IF for diffusion models; scored 8.00 but different topic |
| 9wjGUN65tY.md | 5.00 | R1/R2 | Yes | **Closest anchor**: conceptors+steering, novel theory, outperformed baselines, but no error bars |
| 1CRu6bGx25.md | 3.67 | R1 | No | LLM stability; not directly comparable |
| yeEWZ8qvlS.md | 5.00 | R1 | No | Interpretable directions; similar space |
| GdbQyFOUlJ.md | 6.50 | R1 | No | Neuron group interpretation; stronger experiments |
| HE9eUQlAvo.md | 6.40 | R1 | No | Influence-based data selection; stronger experiments |
| KjBG4JNOc2.md | 6.20 | R1 | No | Influence measure for training; stronger experiments |
| wozhdnRCtw.md | 7.00 | R1 | Yes | Instruction-following via steering; strong empirical paper |
| 4xWQS2z77v.md | 8.00 | R1 | No | Convex duality for NNs; very different topic |
| uHLgDEgiS5.md | 8.00 | R1 | No | Temporal dependence of IF; very different topic |
| AoraWUmpLU.md | 8.00 | R1 | No | Neural ODEs; different topic |
| kbjJ9ZOakb.md | 8.00 | R1 | No | Single-neuron invariance; different topic |
| 2XBPdPIcFK.md | 5.00 | R2 | No | Steering Language Models (activation engineering); similar domain, stronger empirical support |
| Pghg8dJnUe.md | 4.33 | R2 | No | Random feature models; unrelated |
| G4P1q2G0XK.md | 3.75 | R2 | No | Implicit neural representations; unrelated |
| ZrnzGzUhNX.md | 5.00 | R2 | Yes | Closed-form interpretation of latent spaces; theoretical paper, similar quality level |
| fDaLmkdSKU.md | 5.80 | R2 | No | Constrained learning; unrelated |
| 4bSQ3lsfEV.md | 5.75 | R2 | No | Feature complexity; unrelated |
| JCCPtPDido.md | 5.50 | R2 | Yes | Jet expansions; theoretical framework paper with exposition issues |

**Round 1 bracket:** 3.5–5.5.

**Narrowing:** The paper shares heavy-weight positive items with 9wjGUN65tY (novel theoretical connection to steering, well-motivated framework) but lacks its strongest positive item (empirically outperforming baselines). Instead, IAS empirically loses to CAA, which is a heavy-weight negative. The paper also shares heavy-weight negatives with z1yI8uoVU3 (limited models, no error bars) but has stronger theoretical novelty. The concrete error in Equation (2) and the nonsensical Corollary 1 proof pull the score below the 5.0 anchors (9wjGUN65tY, ZrnzGzUhNX). The paper is clearly above 3.0-level papers (fdvSCcB7i8, WT2bL7sCM1) which lacked theoretical novelty or had severe theoretical confusion.

**Final score: 4.5** — A borderline reject. The theoretical contribution is genuinely novel and the core construction is sound, but the experimental evidence is too weak to support the practical claims (the main comparison shows IAS is worse than CAA), and there are concrete mathematical/argumentation errors that need fixing.

MY FINAL SCORE: <score>4.5</score>
MY FINAL DECISION: <decision>Reject</decision>