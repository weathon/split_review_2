## Summary

This paper empirically demonstrates that activation steering—a technique for controlling LLM behavior by injecting vectors into hidden states—systematically compromises safety alignment. Through experiments across Llama3, Qwen2.5, Falcon3, and FalconH1 (3B–70B), the authors show that even random steering vectors induce harmful compliance (2–27%), that SAE-based steering carries comparable risks, and that averaging 20 random jailbreak vectors creates a universal attack that generalizes to unseen prompts (up to 64% compliance on some models). A case study using the public Goodfire API confirms the vulnerability in a deployed setting.

## Strengths

1. **The core finding—that even *random* activation perturbations bypass safety mechanisms—is important and non-obvious.** Sec. 4.1 (Fig. 2) demonstrates that any arbitrary steering vector, not just adversarially constructed ones, can induce harmful compliance. This refutes the implicit assumption that only maliciously designed vectors are dangerous and establishes the fundamental brittleness of safety alignment along the latent-space axis.

2. **The universal attack construction (Sec. 4.4) is practically concerning.** Averaging 20 random vectors that individually jailbreak a single prompt, then testing on 99 unseen prompts, achieves 38–64% compliance on several models (Fig. 6). The attack requires no model weights, gradients, or logits—only query access and the ability to steer. This elevates the paper from an observational study to a concrete threat demonstration.

3. **Experimental scope is reasonably broad.** Testing across four model families at sizes from 3B to 70B, with 1,000 random vectors per configuration (Sec. 3.3, Sec. 4.1–4.4), provides meaningful evidence that the phenomenon is not model-specific.

4. **The Goodfire API case study (Sec. 4.3) grounds findings in real deployment.** The disclaimer-then-compliance and fictional-framing failure modes make the vulnerability concrete and demonstrate that the risk exists in production systems today.

## Weaknesses

### Fatal
None.

### Major
None.

### Minor

1. **LLM-as-judge validation metrics are not reported in the main text.** The entire compliance rate metric depends on Qwen3-8B classifying 300,000 responses as SAFE/UNSAFE (Sec. 3.4). The paper references validation against human annotations in Appx. B (which exists in the original submission) but provides no agreement rate, false positive/negative rates, or any quantitative validation in the main paper. Since the compliance rate is the sole metric—and since borderline cases (e.g., disclaimer-then-compliance responses) involve judgment calls—readers cannot assess measurement reliability from the main text. The baseline claim that "the compliance rate without any steering is 0%" (Sec. 3.4) also depends on this unvalidated judge. The authors should report at minimum the judge's agreement rate with human annotators in the main paper.

2. **No uncertainty quantification for compliance rate estimates.** Compliance rates throughout Sec. 4.1–4.4 are reported as point estimates (17%, 11%, 10%, etc.) without standard deviations or confidence intervals. For 1,000 samples per configuration, a 17% rate has an approximate 95% CI of ±2.3%. The paper already creates 20 distinct universal vectors per model (Sec. 4.4)—reporting variance across them would be straightforward and would help assess whether cross-model or cross-condition differences are meaningful.

3. **The scaled evaluation (Sec. 4.2) uses different layers and coefficients across models, conflating model choice with steering type.** Llama3-8B is tested at 1/3 depth with coefficient 2.0, Qwen2.5-7B at 1/3 depth with coefficient 1.5, and Llama3.1-8B (SAE) at 2/3 depth with coefficient 2.0. The conclusion that "SAE-based steering proves even more dangerous" (Sec. 5) partially references these comparisons (Fig. 3: 17% vs 11% vs 10%), which confounds model, depth, and coefficient changes. The cleaner controlled comparison in Sec. 4.1 (Fig. 2c: same model, layer, coefficient) independently supports the SAE-vs-random claim. The paper should either use consistent configurations for cross-model comparisons or explicitly separate the analyses.

4. **The "zero-shot" characterization of the universal attack (Sec. 4.4) is imprecise.** The paper states the attack is "completely zero-shot" (line 239) because it requires no gradients or model weights. However, constructing the universal vector requires sampling 100–500 random vectors, testing each on the model with a harmful prompt, and selecting those that succeed—this is black-box query-based access, not zero-shot in the standard sense of requiring no task-specific data or computation. Describing it as a "black-box, query-based attack" would be more precise.

### Trivial
None.

## Nice-to-Haves

- The paper steers both prompt and generation tokens (citing Durmus et al., 2024, Sec. 3.2) but does not discuss whether steering prompt tokens could disrupt the model's ability to parse the prompt, which is a distinct mechanism from corrupting the refusal decision. An ablation separating these effects would strengthen the mechanistic understanding.
- The Qwen2.5-32B universal attack result (compliance *decreasing* from 16% to 9% when averaging vectors, Fig. 6) is mentioned without analysis. Understanding why averaging helps on some models but hurts on others could reveal structural properties of the steering geometry.
- The paper does not ablate the number of averaged vectors (currently fixed at 20, Sec. 4.4). An ablation on vector count would sharpen the threat model assessment.

## Removed Points

These points were considered but removed with justification:

- *Criticism that the LLM-as-judge is "the sole evaluation instrument" without validation* → Kept but downgraded from "significant evidential weakness" (as characterized by the harsh critic) to Minor, because the paper does reference validation in Appx. B (which exists in the original submission) and the weakness is about main-text presentation rather than a missing analysis.
- *Criticism that steering both prompt and generation tokens is a confound* → Moved to Nice-to-Haves as a design discussion point, not a weakness.
- *Criticism that Qwen2.5-32B result is mentioned without analysis* → Moved to Nice-to-Haves.
- *Criticism about missing capability degradation analysis* → Moved to Nice-to-Haves as outside the paper's stated scope.
- *Generic strengths about problem importance* → Removed as superficial.
- *Section-by-section observations about selection of three canonical depths, prompt token steering, etc.* → Some folded into existing weaknesses; others were observations without actionable criticism.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface a perspective that the paper itself does not articulate.

## Suggestions

1. Report judge validation metrics (agreement rate, per-class error rates) in the main paper—at minimum a one-sentence summary with the key number from Appx. B.
2. Add standard deviations or 95% confidence intervals to all compliance rate figures in Sec. 4.1–4.4. Since you already average over 1,000 vectors, this is computationally free.
3. Clarify the "zero-shot" terminology to "black-box, query-based attack" in Sec. 4.4.
4. In Sec. 4.2, clearly separate the random-vs-SAE comparison (which is cleaner in Sec. 4.1) from the cross-model generalizability analysis, and avoid making comparative claims across configurations that differ on multiple variables.

## Score and Decision

**Calibration anchors used (all rounds):**

| Path | Avg Score | Round | Comparison |
|---|---|---|---|
| z1yI8uoVU3.md (Measuring Effects of Steered Representation) | 3.00 | 1 | Significantly weaker—limited novelty, narrower scope, less clear contribution. |
| HuNoNfiQqH.md (Understanding Jailbreak Success) | 4.75 | 1 | Mixed reviews; our paper has cleaner experiments and a clearer takeaway. |
| hTEGyKf0dZ.md (Fine-tuning Aligned LLMs Compromises Safety) | 4.75 | 1 | Most similar contribution type; our paper is slightly stronger (clearer non-obvious finding, universal attack). |
| r42tSSCHPh.md (Catastrophic Jailbreak via Exploiting Generation) | 7.00 | 1 | Stronger—achieves 95% ASR, proposes defense, more comprehensive. Our paper is below this. |
| aSy2nYwiZ2.md (Injecting Universal Jailbreak Backdoors) | 6.67 | 1 | Stronger in attack methodology; our paper is more observational/demonstrational. |
| RdGvvqjkC1.md (How Jailbreak Defenses Work) | 5.75 | 2 | Comparable quality; our paper has a more surprising finding. |
| hXA8wqRdyV.md (Jailbreaking with Simple Adaptive Attacks) | 6.14 | 2 | Stronger in attack success rate and model coverage. |
| yVVzaRE8Pi.md (Jailbreak Attack via Implicit Reference) | 5.50 | 2 | Similar tier; our paper has broader scope and more practical implications. |

**Round 1 bracket:** 5.0–6.5  
**Round 2 narrowing:** Upper bound confirmed below 7.0; lower bound confirmed above 4.75 (the fine-tuning safety paper).  
**Final calibration score:** 6.0 — Solid empirical contribution with fixable presentation gaps; on the accept side of borderline.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>