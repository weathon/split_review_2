## Summary

This paper extends the study of emergent misalignment (Betley et al., 2025b) across diverse settings: 9 synthetic advice domains, reinforcement learning on reasoning models, and models without safety training. It uses sparse autoencoders to identify "misaligned persona" features — particularly a "toxic persona" latent — that bidirectionally steer misalignment, and shows that ~200 benign samples reverse the effect.

## Strengths

1. **RL and reasoning model extension (Section 2.3, Figures 3–5).** Demonstrating emergent misalignment under RL — which provides only a scalar reward — meaningfully strengthens the case that misalignment generalization is easy to elicit, not a brittle artifact of SFT. The chain-of-thought analysis (Figures 4–5) showing reasoning models explicitly adopt misaligned personas provides convergent evidence.

2. **Cross-domain generalization (Section 2.2, Figure 2).** Systematic demonstration across 9 advice domains (health, legal, automotive, finance, etc.) convincingly establishes breadth beyond the insecure-code setting.

3. **Bidirectional steering with SAE-identified features (Section 3, Figures 6–7).** The identification of specific SAE latents — especially latent #10 ("toxic persona") — that causally induce misalignment in the original model and suppress it in multiple fine-tuned models provides clean causal evidence, robust across diverse misaligned models.

4. **Emergent re-alignment (Section 4, Figure 10).** The finding that 120–200 benign, even out-of-distribution, samples reverse misalignment is practically useful and includes informative in-distribution vs. out-of-distribution comparison.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **"Perfect discrimination" claim outruns the evidence.** The paper states that latent #10 activation "perfectly discriminates aligned models from misaligned models" (Figure 7 caption) and "can be used to predict whether a model will exhibit such behavior" (Abstract). However, the latent was *selected* because its activation increases most on the same 44 evaluation prompts used to measure discrimination. While the paper does test on *models* not used in selection (correct-dataset models), the evaluation *prompts* are shared. This does not demonstrate generalization to new prompts or truly prospective prediction. The finding is still a useful correlation but should be described as such.

2. **SAE advantage over simpler methods is claimed but not demonstrated.** The discussion states "We were more quickly able to make progress using SAEs, compared to simpler representation engineering approaches" (Section 5). No comparison to simpler methods (e.g., mean activation difference as in Soligo et al., 2025, which the paper cites) is presented anywhere. The paper should either provide evidence for this claim or remove it.

3. **RL experiments lack multiple seeds.** The SFT experiments report three random seeds (Figure 2 caption), but the RL experiments (Section 2.3) do not mention seed variation. This makes checkpoint-selection sensitivity unassessable.

4. **"Early warning" framing is aspirational.** The paper discusses SAE-based "early warning system" (Section 4, Section 5) for detecting misalignment before it manifests behaviorally. While Appendix G shows latent #10 activates more in a reward-hacking model with 0% misalignment score — which is suggestive — the broader claim about detecting "extremely rare" or "unforeseen" misalignment is not supported by the experimental design. The paper's own Discussion (Section 5) acknowledges this, but the earlier framing could mislead.

### Trivial
- The paper does not discuss whether SAE features trained on pre-training data maintain consistent interpretations when applied to post-fine-tuning models (feature absorption / concept drift). This is common practice in SAE work but worth acknowledging.
- The grader uses a rubric-based GPT-4o evaluator with resampling of incoherent responses, creating a minor selection bias concern. The paper mentions manual verification of high-scoring responses (false positives) but not low-scoring ones (false negatives).

## Nice-to-Haves
- A direct comparison of the SAE-discovered steering direction to a simple activation-mean-difference direction (paralleling Soligo et al., 2025) would either justify the SAE approach or honestly delimit its advantages.
- Testing latent #10's discrimination on held-out prompts or held-out domains would strengthen the prediction claim.
- Reporting RL experiment variance across seeds would improve rigor.

## Removed Points

- **Re-alignment ease undermines phenomenon significance (removed).** The paper already explicitly addresses this: "Our results do not imply that all misaligned behaviors can be mitigated with light fine-tuning—only that this specific type of emergent misalignment can easily be mitigated" (Section 4). This is a matter of interpretation, not a factual weakness.
- **Concurrent work (Soligo et al.) diminishes SAE contribution (removed).** The paper honestly cites this work. The SAE approach identifies *multiple interpretable features* (10 latents with distinct interpretations) that go beyond finding a single direction. The superiority claim is already captured in weakness #2 above; the existence of concurrent work does not invalidate the paper's findings.

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Temper or remove the "perfect discrimination" / "early warning" framing; describe the finding as a strong correlation on the studied models.
2. Remove the unsubstantiated "more quickly able to make progress" claim, or back it with evidence.
3. Report multiple seeds for the RL experiments or note the limitation.
4. Add a brief discussion of SAE feature consistency across pre- and post-fine-tuning.
5. Consider a simple ablation comparing the SAE direction to an activation-mean-difference direction (even as an appendix experiment) to strengthen the mechanistic contribution.

## Score and Decision

**Calibration anchors (retrieved across rounds):**

| Path | Avg Score | Round | Comparison |
|------|-----------|-------|------------|
| 5kMwiMnUip.md (Jailbreaking LLMs) | 1.40 | R1 | Much lower quality; unserious paper |
| 8QTpYC4smR.md (LLM Survey) | 1.00 | R1 | Literature review, not research |
| tcsZt9ZNKD.md (Scaling sparse autoencoders) | 8.20 | R1 | Different work; SAE scaling paper |
| Wxl0JMgDoU.md (Chess SAE) | 2.50 | R1 | Lower quality SAE application paper |
| sknUS8X9q0.md (SAE evaluation framework) | 4.00 | R1 | Methodological contribution on SAE eval; comparable rigor but less empirical breadth |
| VrHiF2hsrm.md (Catastrophic Forgetting) | 5.75 | R1 | Similar tier — studies fine-tuning generalization; our paper has more breadth but similar depth |
| lXE5lB6ppV.md (Do as I do Safely) | 5.75 | R1 | Similar tier — studies fine-tuning safety risks; our paper has more mechanistic depth |
| A0HKeKl4Nl.md (Mechanistically analyzing fine-tuning) | 6.67 | R1 | Similar tier — manages more controlled analysis but studies simpler phenomenon |
| I4e82CIDxv.md (Sparse Feature Circuits) | 8.00 | R1 | Stronger paper — novel methodology with rigorous validation; our paper is below this level |

**Round 1 bracket:** 5.5–7.5 (based on comparison with anchors).

**Narrowing:** The paper is most comparable to the 5.75–6.67 anchors. It has solid empirical breadth and a non-trivial RL extension, but the overclaiming on prediction/early-warning, the unsupported SAE-superiority claim, and the missing RL seeds place it toward the lower end of this range.

**Final score:** 6.0 — a solid empirical paper with genuine contributions, tempered by overclaims and a few methodological gaps that should be corrected in revision.

<score>6.0</score>
<decision>Accept</decision>