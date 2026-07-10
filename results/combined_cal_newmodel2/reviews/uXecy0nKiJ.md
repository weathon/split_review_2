## Summary

This paper investigates whether activation steering — a technique for controlling LLM behavior by adding vectors to hidden states — can unintentionally compromise safety alignment. Through experiments on Llama3, Qwen2.5, Falcon3, and Llama3.1-8B (with Goodfire's SAE), the authors show that even *random* steering vectors increase harmful compliance from 0% to non-trivial rates (2–27%), that steering with benign SAE features has comparable effects, and that averaging prompt-specific jailbreak vectors can produce a "universal" attack vector that generalizes to unseen harmful prompts. The paper's core empirical finding — that random activation perturbation systematically degrades safety — is a genuine and practically important discovery.

## Strengths

- **The core finding is a genuine empirical discovery with practical importance.** The observation that even random (unsupervised, non-adversarial) activation steering systematically degrades safety alignment — raising compliance from 0% to substantial rates across multiple model families — fills a real gap in the literature. Prior work focused almost entirely on adversarially optimized jailbreak vectors; showing that random vectors suffice is surprising and significant (Sec. 4.1, Fig. 2). [favorability=14.93]

- **The case study with a real production API (Sec. 4.3) is compelling.** Demonstrating that a "brand identity" SAE feature deployed via Goodfire's public API actually produces detailed scam emails and cannibalism instructions grounds the paper's claims in practical risk, not just toy experiments. [favorability=13.22]

- **The universal attack construction is novel for threat modeling.** Averaging prompt-specific jailbreak vectors to produce a vector that generalizes to unseen harmful prompts — requiring no model weights, gradients, or logits — is a practically relevant contribution (Sec. 4.4, Fig. 6). [favorability=11.07]

- **The paper is well-structured** with a logical progression from single-prompt sweep → full-dataset evaluation → case study → universal attack. [favorability=9.86]

## Weaknesses

### Major

- **Overclaimed generality of the universal attack.** The "4× average increase" claim is heavily driven by two Falcon3 models (~12× improvement); for most other models the improvement is only 1.5–2×, and for Qwen2.5-32B compliance actually *decreases* from the individual-vector baseline. The paper acknowledges model-dependence in one sentence, but the overall framing ("universal attack," "4× increase," "significantly increasing harmful compliance") conveys a much stronger claim than the data support (Fig. 6, lines 235–239). [favorability=1.31]

- **SAE experiments limited to a single configuration with broad generalization.** The SAE experiments use only Llama3.1-8B with Goodfire's SAE trained on layer 19. This is stated transparently in Sec. 3.3, but neither the abstract nor the conclusion carries this caveat. Claiming SAE-based steering "demonstrates a comparable harmful potential" (abstract) and "proves even more dangerous" (conclusion) without qualifying the single-model, single-SAE basis overstates the evidence. [favorability=0.85]

### Minor

- **No uncertainty quantification for any reported compliance rate.** All results are point estimates without standard errors, confidence intervals, or variance measures. For the universal attack (Fig. 6), 20 universal vectors are constructed per model but only the average is shown; the range across constructions is not reported. While the sample sizes (1,000 vectors per configuration) are large enough for tight estimates, the absence of any variance reporting makes it impossible to assess statistical reliability. [favorability=2.56]

- **The causal interpretation is undersupported in the main text.** The paper claims steering "compromises safety mechanisms," but the main text only briefly references an analysis in Appendix E to distinguish this from general capability degradation. A controlled experiment (e.g., measuring benchmark accuracy under identical steering conditions) would substantially strengthen the claim that the effect is safety-specific rather than generic performance collapse. [favorability=3.95]

### Trivial

None.

## Nice-to-Haves

- Add standard errors or confidence intervals for all compliance rates, and show the range/variance across the 20 universal vector constructions.
- Add a control experiment measuring benchmark accuracy (e.g., MMLU, GSM8K) under the same steering conditions to distinguish safety-specific effects from general capability degradation.
- Add at least one additional SAE (e.g., Gemma Scope) on a different model to support the generality of the SAE findings.
- Qualify the universal attack claims explicitly in the abstract and conclusion (e.g., "effective for some models but highly model-dependent").

## Removed Points

- *"The paper compares the universal vector against random steering rather than against individual jailbreak vectors"* — Factually incorrect: Fig. 6 shows three bars per model including "Individual Unsafe Direction." REMOVED.
- *"Figure 3 comparison is confounded"* — The figure's purpose is to show the vulnerability pattern across categories, not to compare SAE vs. random directly (which is done correctly in Fig. 2c). Too weak to retain. REMOVED.
- *"Abstract's 0% to 2–27% range is ambiguous"* — Trivial presentation point that doesn't affect the paper's contribution. REMOVED.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Add explicit caveats about model-dependence in the abstract/conclusion for both the universal attack and the SAE findings.
2. Report error bars or confidence intervals for all main compliance rate figures.
3. Add a control experiment (e.g., MMLU under the same steering) to help distinguish safety-specific degradation from general capability loss.
4. Include the range/variance across the 20 universal vector constructions rather than only the average.

## Calibration Report

**Anchors retrieved across all rounds:**

| Path | Avg Score | Round | Itemized | Comparison |
|------|-----------|-------|----------|------------|
| `5kMwiMnUip.md` | 1.40 | R1 | No | Weak reject paper; not comparable |
| `BeOEmnmyFu.md` | 2.50 | R1 | No | Jailbreak paper; weaker contribution |
| `KyKTjRtyNG.md` | 3.00 | R1 | No | Multi-round jailbreak; weaker |
| `z1yI8uoVU3.md` | 3.00 | R1 | Yes | Activation steering evaluation paper; my paper has stronger core finding (favorability 14.93 vs 10.24) and less severe weaknesses (all positive favorability) |
| `kT6oc5CpEi.md` | 3.00 | R1 | No | Black-box jailbreak; weaker |
| `HuNoNfiQqH.md` | 4.75 | R1 | Yes | Jailbreak latent dynamics; my paper has higher-strength strengths (14.93 vs 12.07) and comparable weakness severity |
| `2XBPdPIcFK.md` | 5.00 | R1 | Yes | ActAdd steering method paper; my paper has comparable strengths but milder weaknesses |
| `hTEGyKf0dZ.md` | 4.75 | R2 | Yes | **Most comparable anchor** — same phenomenon type (unintended safety degradation). My paper's top strength (14.93) exceeds their top (12.16), and my weaknesses are less severe (all favorability > 0 vs some < -3). My paper is clearly stronger. |
| `NIouO0C0ex.md` | 5.67 | R2 | Yes | Reverse alignment through fine-tuning; my paper has higher strengths and less severe weaknesses. |
| `hXA8wqRdyV.md` | 6.14 | R1 | Yes | Comprehensive jailbreak attack paper; my paper is somewhat weaker — this paper had more comprehensive evaluation across more models |
| `YzxMu1asQi.md` | 6.50 | R1 | Yes | Activation attack scaling laws; different contribution type, stronger formal results |
| `45rvZkJbuX.md` | 6.50 | R2 | No | Cross-modal safety; different domain |
| `gT5hALch9z.md` | 6.00 | R2 | No | Safety-tuned LLaMAs; stronger empirical methodology |

**Round-1 bracket:** 4.0–6.5 (based on comparison with z1yI8uoVU3 (3.00) and hXA8wqRdyV (6.14))

**Round-2 narrowing:** The closest anchor is `hTEGyKf0dZ.md` (avg 4.75, accepted), a phenomenon paper about unintended safety degradation from fine-tuning. My paper's core finding is more surprising (random vectors vs. fine-tuning), its top-rated strength has higher favorability (14.93 vs. 12.16), and its weaknesses are milder (all positive favorability compared to several negative in the anchor). This places the paper above 4.75. However, the overclaiming on the universal attack and limited SAE scope prevent it from reaching the level of `hXA8wqRdyV` (6.14), which had more comprehensive evaluation. **Final score: 5.5**, calibrated between these two anchors based on the favorability comparison of shared high-strength items (core empirical discovery) and differentiating low-strength items (overclaiming on universality, limited SAE breadth).

## Score and Decision

MY FINAL SCORE: <score>5.5</score>
MY FINAL DECISION: <decision>Accept</decision>