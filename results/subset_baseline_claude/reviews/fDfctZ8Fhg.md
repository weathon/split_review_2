## Summary

The paper presents a structural analysis of hallucination *persistence* in autoregressive pre-LayerNorm (pre-LN) residual transformers. It proves that such architectures exhibit "neutral dynamics" — predictive divergence between two continuations of the same prompt neither grows nor shrinks in expectation. Three main results follow: (1) closed neutrality (same token input, zero expected drift), (2) a predictable drift corridor bounding systematic deviation, and (3) a mean-field lift showing neutrality aggregates to population scale. Experiments on GPT-2 variants and Qwen2.5 (0.5B–3B) support the predictions.

---

## Strengths

- **Novel framing of a real gap.** The distinction between hallucination *onset* and *persistence* is conceptually sharp and under-addressed. The paper correctly identifies that existing mitigation work (RLHF, RAG, etc.) targets onset and leaves the propagation mechanism unanalyzed.
- **Formal decomposition is clean.** The closed/open decoding split and the drift identity (eq. 2) cleanly isolate architectural effects from stochastic token-sampling effects, enabling principled hypothesis testing.
- **Empirically falsifiable.** The blended reporting rule (Theorem 1) links the theory to finite-sample statistics using Azuma–Hoeffding and anytime e-processes, and the results across four GPT-2 scales plus three Qwen2.5 models are internally consistent with the theoretical predictions.
- **Practical implications are stated honestly.** The authors are careful to note neutrality is a *necessary but not sufficient* condition for semantic hallucination persistence, and the limitations section is candid.

---

## Weaknesses

### Fatal
None identified.

### Major

1. **The core theoretical claim (closed neutrality, Lemma 5) is asserted but not provably derived in the main text, and its plausibility is unclear.** In the closed regime, both continuations consume the same token τ drawn from p_t, so h_{t+1} = F(h_t, τ) and h̃_{t+1} = F(h̃_t, τ) are both deterministic functions of τ. The claim E[D_{t+1}^{closed} − D_t | F_t] = 0 therefore requires E_{τ~p_t}[JS(S(F(h_t,τ)), S(F(h̃_t,τ)))] = JS(S(h_t), S(h̃_t)) — an exact equality for *any* weights of a pre-LN transformer. It is not obvious why this would hold for a general pre-LN architecture. The proof is deferred entirely to Appendix A.3 (Lemma 5), and the main text provides no intuition or proof sketch for why this structural property should follow from the pre-LN design specifically. Without this, the architectural claim — the paper's centerpiece — cannot be evaluated.

2. **The implication for hallucination mitigation overstates what neutral dynamics implies.** Section 5's conclusion that "interventions that do not modify the residual backbone cannot eliminate persistence" does not follow from the theory. RLHF and fine-tuning change the learned weights W and G_ℓ, which in turn change F and S — they do modify the backbone in the relevant sense. The neutrality result is weight-agnostic (holds for any weights in the architecture class), so it cannot say whether a trained model can or cannot correct deviations; it only says the *functional form* of the update provides no automatic restoring force. The current framing conflates architecture class with specific learned behavior.

3. **The empirical scope is modest and the demonstrated drift values are trivially small.** Open-probe mean drifts on the order of 10⁻⁸ to 10⁻¹⁰ — many orders of magnitude below the theoretical corridor — suggest the experiments confirm the theory only in an extremely weak sense. It would be informative to show what happens to drift for prompts that actually elicit factual hallucinations versus correct continuations; the current setup uses arbitrary prompt/continuation pairs with no semantic grounding.

### Minor

- The mean-field "lift" (Section 3.6) is mathematically routine. Proposition 2 is just the law of large numbers applied to mean-zero bounded i.i.d.-like variables. The agent/MFG language adds terminology without yielding new structural insight beyond what the trajectory-level analysis already provides.
- The CRN construction (Section 3.2) is described in terms of "mirror-image modifications" without a clear formal statement of what "the same non-token randomness" means across arms; this is likely formalized in the appendix but is hard to follow in the main text.
- Horizon N=32 is short for meaningful hallucination analysis; the paper acknowledges this but it limits interpretation.

### Trivial
None worth noting.

---

## Nice-to-Haves
- An ablation or case study on prompts where one continuation actually becomes semantically hallucinated (grounded via an external factuality oracle), to show whether JS divergence persists for those pairs specifically.
- A brief proof sketch for why E[D_{t+1}^{closed}|F_t] = D_t should hold structurally for pre-LN (vs. post-LN) architectures.
- Testing on at least one model ≥ 7B to strengthen the scaling claim.

---

## Novel Insights
The most genuinely novel observation is the formal separation of drift into a deterministic (architectural) component and a stochastic (token-mismatch) component via the CRN, combined with the quantitative result that the deterministic component is bounded by a Lipschitz chain through the residual stack. This provides a principled tool for empirically auditing hallucination dynamics in any pre-LN model that exposes logits, which is more actionable than prior diagnostic approaches. However, the value of this tool depends critically on whether closed neutrality (Lemma 5) is actually provable — if the proof has a gap, the entire framework reduces to an interesting but unvalidated conjecture.

---

## Suggestions
- Provide at minimum a self-contained proof sketch for Lemma 5 (closed neutrality) in the main text, not just a pointer to the appendix. This is the load-bearing result; its derivation should be inspectable.
- Soften the implications claim in Section 5: the correct statement is "architectures in this class provide no *automatic* corrective force" rather than "post-training interventions cannot eliminate persistence."
- Include at least a few examples tying the JS divergence metric back to observable hallucination events to bridge the predictive/semantic gap the paper itself acknowledges.

---

## Score and Decision

The paper addresses a meaningful gap (structural account of hallucination persistence), introduces a clean analytical decomposition, and provides consistent empirical evidence. However, the central theoretical claim rests entirely on a lemma whose derivation is inaccessible in the main text and whose plausibility from first principles is unclear. The over-strong implication for mitigation further weakens the contribution. The experiments, while consistent, operate at trivially small drift magnitudes and do not connect to grounded hallucination events. This is a borderline paper — interesting idea, promising framework, but the core proof obligation is unmet in the reviewable text.

MY FINAL SCORE: <score>4</score>
MY FINAL DECISION: <decision>Reject</decision>