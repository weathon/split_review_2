## Summary

This paper investigates whether activation steering — adding vectors to LLM hidden states during inference to control behavior — can inadvertently compromise safety alignment. Through extensive experiments across multiple model families (Llama3, Qwen2.5, Falcon3, FalconH1, 3B–70B), the authors find: (1) even steering in a random direction increases harmful compliance from a 0% baseline to 2–27%, (2) SAE feature steering (supposedly interpretable, benign features) shows comparable harmful potential to random noise, and (3) averaging 20 random vectors that jailbreak a single prompt creates a more potent attack that partially generalizes to unseen prompts. A production-API case study grounds the findings in a deployed system.

## Strengths

1. **Demonstrates benign/random steering vectors compromise safety, not just adversarially optimized ones**: The paper fills a clear gap identified in prior work (Section 2, ¶3), where existing studies only examined vectors "explicitly designed to be harmful" (Wang & Shu 2023; Chia et al. 2025; Dunefsky 2025). Random steering increases compliance from 0% to 2–27% across models (Figs. 2a–b, 3), and SAE feature steering achieves comparable rates (11% overall on Llama3.1-8B, Fig. 3).

2. **Universal attack constructed from averaged prompt-specific vectors with minimal requirements**: Section 4.4 shows averaging 20 random vectors that jailbreak a *single* prompt creates a vector that achieves a 4× average increase in compliance rate on unseen JailbreakBench prompts (Fig. 6). The attack needs only black-box steering capability — no model weights, gradients, or harmful training data — making it qualitatively different from prior adversarial steering methods that required per-vector optimization.

3. **Large-scale, multi-model evaluation with systematic sampling**: The paper evaluates 4 model families at 3B–70B scale, sampling 1,000 vectors per steering condition and processing ~300,000 responses (Sections 3.3, 3.4, 4.1). The sweep across 6 scaling coefficients and 3 canonical layer depths (Section 3.2) provides more systematic coverage than prior single-vector or single-model studies.

4. **Systematic SAE feature analysis linking widespread dangerousness to benign semantics**: Section 4.2 (Fig. 4a) shows 668 out of 1,000 SAE features jailbreak at least 5 prompts, with the most dangerous features corresponding to semantically benign concepts (e.g., "brand identity"). The cross-category generalization heatmap (Fig. 4b) shows poor generalization, meaning comprehensive safety screening would be practically infeasible.

5. **Production-API case study validating real-world exploitability**: Section 4.3 demonstrates jailbreaking a production model through the public Goodfire API using a benign "brand identity" SAE feature, with concrete examples showing "disclaimer-then-compliance" and "justification via fictional framing" failure modes (Fig. 5).

## Weaknesses

### Fatal
None.

### Major

1. **The "universal attack" label overclaims given the model-dependent results**: The term "universal attack" (used in the abstract, Finding 3, and Section 4.4 title) is too strong. From Fig. 6's data:
   - Qwen2.5-32B: Random Direction 9%, Average of 20 Unsafe Directions 9% — **zero improvement.**
   - Falcon-H1-34B: Random 11% → Average 18% — marginal improvement.
   - The headline "4× average increase" is driven disproportionately by Falcon3-3B (5% → 64%, ~12.8×) and Falcon3-7B (5.7% → 59%, ~10.4×).
   - Most models show 1.6–2.3× improvement at best.
   
   A method that completely fails on one model and shows marginal gains on others should not be called "universal." This framing appears in the abstract and conclusion without sufficient qualification.

2. **No measures of variability or statistical significance**: All compliance rates are reported as point estimates from 1,000 random vectors or 20 universal vectors, without confidence intervals, standard deviations, or any significance testing. Many of the key comparative claims involve small effects (e.g., the 2–4% difference between SAE and random in Fig. 2c). Given that the evaluation depends on an LLM-as-judge (which introduces its own noise), this is a significant gap. The reader cannot assess whether observed differences are reliable or within noise.

### Minor

1. **SAE feature steering results are limited to a single model, SAE, and layer**: All SAE experiments use Goodfire's SAE on Llama3.1-8B at layer 19 (Section 3.3). The paper acknowledges this limitation but the abstract and introduction state findings as general properties of SAE-based steering. The claim that "SAE feature steering has comparable harmful potential to random noise" (Claim 2) would be substantially stronger with evidence from at least one additional model or SAE.

2. **Narrative framing conflates two different findings**: The paper's title, abstract, and conclusion frame the contribution as being about *activation steering* as a technique. However, much of the primary evidence (Sections 4.1, 4.2, 4.4) comes from random Gaussian perturbations. While random-direction steering is technically a form of activation steering, it conflates two distinct claims: (a) "alignment is fragile to any activation perturbation" (the random noise finding) and (b) "semantic steering vectors are dangerous" (the SAE finding). These have different implications for mitigation and should be more cleanly separated in the narrative.

3. **No comparison with existing jailbreak methods**: The paper does not contextualize the practical severity of steering-based attacks. How does a 17% compliance rate from steering on Llama3-8B compare to well-known prompt-based jailbreaks? This would help readers assess whether this is a moderate concern or a critical vulnerability relative to existing threats.

### Trivial
None.

## Nice-to-Haves
- Bootstrapped confidence intervals or error bars for compliance rate estimates, especially where comparisons are drawn between conditions.
- SAE experiments on at least one additional model/layer combination to demonstrate generality beyond Llama3.1-8B layer 19.
- A brief summary in the main text of the LLM-as-judge calibration results against human annotations (presently deferred to the stripped appendix).

## Removed Points
*These points are flagged to be removed; treat them with caution.*

- **SAE vs. random comparison "confounded by model differences" / "distribution-matched baseline"**: Removed. The critic claimed the comparison is confounded because random noise is not a "distribution-matched" baseline for SAE features. However, the paper never claims distribution-matching — the comparison tests whether interpretable SAE features (semantically meaningful) are more or less dangerous than unstructured random noise (non-informative). This is a standard and appropriate baseline. The critic's demand for a distribution-matched baseline is not required for the paper's claims.

- **Qwen3-8B judge alignment biases**: Removed. The paper notes (Section 3.4) that Qwen3-8B was selected for its "strong balance between calibration accuracy and computational feasibility" and that quality assessment against human annotations was conducted (Appendix B, stripped by parser). The critic's concern is speculative rather than evidence-based.

- **"No analysis distinguishing capability degradation from specific refusal suppression"**: Removed. The paper explicitly addresses this (Section 4.1): "Preliminary analysis of potential mechanisms (App. E) suggests this safety compromise is not due to simple alignment with known refusal directions nor general capability degradation." While the appendix is stripped, the paper does engage with this concern.

- **"Missing related works"**: Removed per meta-reviewer instructions (cannot verify external sources).

- **All formatting/style nitpicks**: Removed per meta-reviewer instructions (parser artifacts, not author errors).

## Novel Insights

The most interesting cross-cutting observation from synthesizing both reviews is that the paper's strongest contribution — showing that benign, interpretable SAE features systematically break safety — is also its narrowest (limited to one model/layer/SAE combination). The tension between the broad claim and the limited evidence base is the central weakness. Conversely, the random-noise finding (alignment is fragile to any activation perturbation) is more robustly demonstrated across models but is arguably a less novel finding (connected to adversarial robustness). The paper's real value lies in connecting these two observations and showing that the very tools (SAE features) that the interpretability community relies on for safe, interpretable control carry the same alignment risks as arbitrary perturbations. The production-API case study (Section 4.3) is the most concretely alarming contribution — it moves the concern from a controlled experiment to a deployed system that users can interact with today.

## Suggestions

1. **Rename "universal attack"** to something more accurate, such as "aggregated steering attack" or "generalized steering attack," with clear caveats about model-dependent effectiveness.

2. **Restructure the narrative arc**: Present random-noise results as establishing the *general fragility* of alignment to any activation perturbation, then position SAE feature results as the core novel finding about *semantic steering vectors* being as dangerous as random perturbations. This would cleanly separate two distinct contributions.

3. **Add error bars or confidence intervals**: Even bootstrapped standard errors over the 1,000 samples per condition would significantly strengthen confidence in the comparative claims (e.g., SAE vs. random differences in Fig. 2c).

4. **Add a brief comparison to prompt-based jailbreak methods** to contextualize the practical severity of the observed compliance rates.

## Score and Decision

**Calibration note**: The calibration search tool encountered a persistent file-system error and could not retrieve anchor papers. The following score and decision are based on direct analysis of the paper content and the reviewer inputs, applying the scoring guidelines' comparative judgment framework.

The paper makes a genuine, timely contribution to a well-motivated question. The experimental scale (300K+ responses, 8 model variants) and the combination of random steering, SAE feature steering, universal attack construction, and a production API case study represent a substantial empirical effort. The core findings — that benign steering vectors systematically break safety, that most SAE features have jailbreaking capability, and that averaging prompt-specific vectors creates a generalized attack — are novel and practically important.

However, the paper's framing exceeds what the evidence supports in two notable ways: the "universal attack" label is contradicted by the paper's own results (zero improvement on Qwen2.5-32B), and the SAE findings are limited to a single model/layer combination despite being stated as general. The lack of any variability measures is a meaningful gap for an empirical paper comparing small differences (2–4%). These issues are fixable and do not invalidate the core findings.

**Score**: 6.5 (borderline accept, leaning toward accept with major revisions)
**Decision**: Accept

The paper's contribution is real and the empirical work is extensive and well-conducted. The framing and methodological gaps are addressable and do not undermine the core claims.

MY FINAL SCORE: <score>6.5</score>
MY FINAL DECISION: <decision>Accept</decision>