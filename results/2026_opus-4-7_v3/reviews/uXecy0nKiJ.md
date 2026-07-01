Now I have a thorough understanding of the paper. Let me draft the review before calibration.Now let me do Round 1 calibration — bracketing across score bands for papers on LLM safety, activation steering, and jailbreaking vulnerabilities.Let me read a few key anchor papers to calibrate more precisely.Now I have enough calibration data. Let me form my initial bracket and finalize the review.

**Round 1 Bracket Assessment:**

- **Strong reject (1-1.5):** Papers like NEMESIS (1.4) are fundamentally flawed. The paper under review is far better. Ruled out.
- **Reject (2.5-3.5):** "Measuring Effects of Steered Representation" (3.0) has limited novelty and weak experiments. The paper under review has clearer findings and broader experiments. Above this range.
- **Borderline reject (3.5-5.5):** "Understanding Jailbreak Success" (4.75) and "Steering Language Models with Activation Engineering" (5.0) — both rejected. The paper under review is comparable: strong experiments but significant framing/evidential issues.
- **Borderline accept (5.5-7.5):** "Jailbreaking Leading Safety-Aligned LLMs" (6.14, accepted) achieves 100% success and has clearer threat model. "Scaling Laws for Adversarial Attacks" (6.5, accepted) has a more analytical contribution with scaling laws. The paper under review has more overclaiming and inconsistent threat model than these accepted papers.
- **Accept (7.5+):** Papers like "Backtracking Improves Generation Safety" (8.0) are clearly stronger.

**Initial bracket: 4.5–6.0**

The paper sits in the borderline territory — better than clear rejects in this space but with enough framing overreach and evidential gaps to fall below accepted papers. Now let me write the final review.

---

## Summary
This paper demonstrates that activation steering — including with random directions and benign SAE features — can systematically compromise LLM alignment safeguards. Through experiments across multiple model families (Llama-3, Qwen2.5, Falcon-3/FalconH1) at scales from 3B to 70B parameters, the authors show that random steering increases harmful compliance from 0% to 2–27%, SAE features perform comparably (2–4% margin over random), and averaging 20 jailbreaking vectors from a single prompt creates a transferable attack vector achieving up to 64% compliance on unseen prompts.

## Strengths
- **Novel universal attack construction (Sec. 4.4).** Averaging just 20 randomly-sampled jailbreaking vectors from a single prompt produces a transferable attack requiring no gradient access, harmful training data, or per-prompt optimization. Achieving up to 64% compliance on Falcon3-3B and 50% on Llama3-70B (Fig. 6) from such a simple procedure is a genuinely interesting and non-obvious finding — it implies the "jailbreaking subspace" has enough shared structure that averaging amplifies the safety-bypassing component while canceling noise.
- **Substantial breadth of experimental coverage.** The paper tests across three model families at scales from 3B to 70B, sweeping over layers, steering coefficients, and vector types, generating ~300,000 responses. The consistency of the random-steering vulnerability across architectures (Figs. 2, 3) provides strong evidence this is not model-specific.
- **Goodfire API case study (Sec. 4.3) grounds the finding in production reality.** Demonstrating that a "brand identity" SAE feature deployed through a production API can jailbreak Llama3.1-8B — using the API's own default hyperparameters — is concrete and actionable. The two documented failure modes (disclaimer-then-compliance, justification via fictional framing) are well-illustrated in Figure 5 and represent genuinely concerning patterns.
- **Conservative evaluation protocol.** Classifying incoherent, repetitive, or nonsensical responses as SAFE (Sec. 3.4) is the right methodological choice and prevents the most obvious source of inflated compliance rates.

## Weaknesses

### Fatal
None

### Major
1. **Framing overreaches the evidence: the core finding is perturbation fragility, not an interpretability-specific vulnerability.** The paper's own data (Fig. 2c) shows SAE features outperform random vectors by only 2–4%. If random noise of sufficient magnitude degrades alignment, the vulnerability lies in alignment fragility to activation perturbations generally, not in something specific to interpretable steering. Yet the abstract claims these results "challenge the paradigm of safety through interpretability," and the conclusion states "SAE-based steering proves even more dangerous" (Sec. 5). This characterization of a 2–4% margin as "even more dangerous" is disproportionate. The paper acknowledges the parity in Sec. 4.1 ("SAE feature steering yields compliance rates comparable to random directions") but continues to frame SAE features as posing "particular risks" (Sec. 4.2) without establishing why the small margin constitutes a qualitatively different concern. This framing-evidence mismatch weakens the paper's narrative coherence and undermines its most prominent claim.

2. **The "universal" attack claim is overstated given extreme model-dependent variance.** From Fig. 6, the averaged vector achieves 64% on Falcon3-3B but only ~9% on Qwen2.5-32B, where it performs no better than random steering. The paper's "4× average improvement" figure (Fig. 6 caption) obscures this critical variance. Describing an attack as "universal" when it fails entirely on some models is misleading. The paper does acknowledge "the effectiveness of this method is highly model-dependent" (Sec. 4.4), but the section title ("Weaponizing Random Steering: From Noise to Universal Attacks") and the finding statement in the introduction ("We can create a universal attack that generalizes to unseen harmful prompts") do not adequately convey this limitation.

3. **The "black-box access" claim is inaccurate.** The paper states "this reveals how localized vulnerabilities can be scaled into universal attacks with minimal effort and black-box access" (Sec. 4.4). However, activation steering requires injecting vectors into hidden-state activations at specific layers — this is definitionally internal access, not black-box. The Goodfire API provides a grey-box steering interface, but claiming "black-box access" in general is misleading. The paper also does not contextualize what else an adversary with the ability to modify hidden-state activations could already achieve, which would be necessary to establish the incremental security concern of this specific attack vector.

### Minor
1. **Ecological validity of steering magnitudes is only partially established.** The scaling coefficients c = 0.75–2.0, where α = c · μ^(l), mean perturbations are 0.75× to 2× the average activation norm — large relative to the signal. The paper's strongest results come from c = 1.5–2.0. The Goodfire API case study partially addresses ecological validity by demonstrating jailbreaking at production defaults, but the paper does not report what those default hyperparameters are (Sec. 4.3 states only "the API's proprietary default hyperparameters"), making it impossible to judge correspondence with the controlled experiments. This gap weakens the "inadvertent compromise" framing — without knowing whether typical benign steering uses comparable magnitudes, the paper cannot distinguish "steering is inherently dangerous" from "steering with unusually large coefficients produces unreasonable behavior."

2. **LLM-as-judge with a single 8B model for 300K responses.** Reliance on Qwen3-8B as sole judge raises calibration concerns for nuanced edge cases, particularly the "disclaimer-then-compliance" pattern where classification is inherently ambiguous. The conservative protocol (classifying incoherent outputs as SAFE) mitigates inflation risk, and the scale of evaluation necessitates automated judging, but single-judge reliability remains a limitation, especially for borderline cases that constitute much of the interesting signal.

3. **The paper oscillates between inadvertent-failure and adversarial-attack framings without fully committing to either.** The "scalpel" metaphor, SAE emphasis, and Sec. 4.3 suggest inadvertent safety failure; Sec. 4.4 is framed as a deliberate adversarial attack. These are distinct threat models with different implications: the inadvertent framing requires evidence about practical steering magnitudes (partially missing), while the adversarial framing requires contextualizing what else is possible at the same access level (not provided). Treating both framings as unified weakens each individually.

### Trivial
None

## Nice-to-Haves
- Survey of what coefficient ranges practitioners actually use for legitimate steering, to firmly establish (or refute) ecological validity
- Deeper analysis of *why* random vectors work comparably to SAE features — the mention of Appendix E's "preliminary analysis" is insufficient for the main text; even a brief treatment of whether jailbreaking vectors share a common subspace or align with known refusal directions would substantially strengthen the contribution
- Ablations on the universal attack: how does performance scale with number of averaged vectors beyond 20? Does varying the source prompt matter?
- Testing whether standard robustness defenses (activation norm clipping, output-level safety classifiers) mitigate the vulnerability, which would clarify practical severity

## Removed Points
*These points are flagged as removed; treat them with caution.*

- **"Comparison with other perturbation-based attacks at the same access level is missing"** — Removed as scope creep. The paper's contribution is documenting activation steering's safety implications, not benchmarking attack modalities. This is a nice-to-have for contextualization.
- **"The paper does not test steering applied only during generation"** — Removed. Applying steering during both prompt and generation is a standard approach (paper cites Durmus et al. 2024); this is a design choice, not a weakness.
- **"Cross-category poor generalization makes the vulnerability less concerning rather than more"** — Removed. The reviewer's alternative reading (shallow/unsystematic = less concerning) is one interpretation, but the paper's reading (monitoring infeasibility) is equally defensible. Both are valid; neither is clearly wrong.
- **"Selection bias from single-prompt initial analysis"** — Partially removed. While using a canonical harmful prompt may influence initial results, the paper explicitly acknowledges this and extends to 100 prompts in Sec. 4.2, adequately addressing the concern. Retained only as minor note.
- **"Confidence intervals not reported"** — Removed. Single-run evaluation at this scale (300K responses) is standard practice; requesting variance estimates is a nice-to-have, not a weakness.

## Novel Insights
The most genuinely novel insight is that localized, prompt-specific vulnerabilities from random activation perturbations can be aggregated through simple averaging into a transferable attack vector — this implies the safety-bypassing component of jailbreaking vectors occupies a shared low-dimensional subspace that averaging selectively amplifies. The finding that 668/1000 SAE features can jailbreak at least 5 prompts, and that the most effective ones represent benign concepts ("brand identity," "physical positioning"), is also informative for safety monitoring: it demonstrates that dangerous steering vectors are indistinguishable from legitimate ones, creating a blind spot for feature-level safety screening.

## Suggestions
- **Reframe around "activation perturbation fragility"** rather than specifically targeting the interpretability paradigm. The evidence supports the broader claim more convincingly, and the paper would be stronger for it.
- **Replace "universal" with "transferable" or "generalizable"** when describing the attack, and prominently report model-dependent variance alongside averages.
- **Correct "black-box access" to "grey-box" or "steering-interface access"** to accurately reflect the required capabilities.
- **Report or characterize the Goodfire API default hyperparameters** to bridge the gap between controlled experiments and the production case study.
- **Center the paper's narrative on the universal attack construction** as the primary contribution — it is the most novel and least disputed finding.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|---|---|---|---|---|
| NEMESIS: Jailbreaking LLMs with Chain of Thoughts | 5kMwiMnUip.md | 1.40 | R1 | Far weaker — no real contribution; paper under review is substantially better |
| Systematic Review of LLMs | 8QTpYC4smR.md | 1.00 | R1 | Not comparable — survey paper, fundamentally different |
| Playing Language Game with LLMs Leads to Jailbreaking | BeOEmnmyFu.md | 2.50 | R1 | Weaker — limited method, less thorough evaluation; paper under review has broader experiments and novel universal attack |
| Measuring Effects of Steered Representation in LLMs | z1yI8uoVU3.md | 3.00 | R1 | Directly comparable topic (activation steering evaluation); paper under review has clearer findings, broader coverage, and a more novel contribution |
| Incremental Exploits: Multi-round Conversational Jailbreaking | KyKTjRtyNG.md | 3.00 | R1 | Paper under review is stronger — more novel mechanism, broader experimental coverage |
| Safety Alignment Should be Made More Than Just a Few Tokens Deep | 6Mxhg9PtDE.md | 9.50 | R1 | Far stronger — provides deep mechanistic understanding and proposes solutions; paper under review lacks this depth |
| Understanding Jailbreak Success: Latent Space Dynamics | HuNoNfiQqH.md | 4.75 | R1 | Comparable — similar scope (latent space analysis of jailbreaks), similar weaknesses (limited model range, unclear generalization); paper under review has broader experiments but more overclaiming |
| Quack: Automatic Jailbreaking via Role-playing | 1zt8GWZ9sc.md | 3.67 | R1 | Paper under review is stronger — more novel findings and broader coverage |
| Do LLMs Have Political Correctness? | zf53vmj6k4.md | 4.25 | R1 | Paper under review is stronger — more focused and experimentally thorough |
| Steering Language Models with Activation Engineering (ActAdd) | 2XBPdPIcFK.md | 5.00 | R1 | Most directly comparable — also about activation steering with framing issues and split reviews; paper under review has comparable experimental depth and similar overclaiming problems |
| Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks | hXA8wqRdyV.md | 6.14 | R1 | Accepted; achieves 100% success rate, tests closed-source models; paper under review has lower effectiveness and more overclaiming, but novel access model (no gradients) |
| Catastrophic Jailbreak via Exploiting Generation | r42tSSCHPh.md | 7.00 | R1 | Accepted; cleaner contribution with clearer threat model; paper under review has more overreaching claims |
| Scaling Laws for Adversarial Attacks on LM Activations | YzxMu1asQi.md | 6.50 | R1 | Accepted; more analytical with scaling laws and clearer theoretical framework; paper under review documents a vulnerability but lacks this depth |
| Injecting Universal Jailbreak Backdoors (JailbreakEdit) | aSy2nYwiZ2.md | 6.67 | R1 | Accepted; proposes a concrete method with high success; paper under review has a simpler but less reliable attack |
| Backtracking Improves Generation Safety | Bo62NeU6VF.md | 8.00 | R1 | Clearly stronger — proposes a solution, not just documents a problem |
| Booster: Tackling Harmful Fine-tuning | tTPHgb0EtV.md | 8.00 | R1 | Clearly stronger — deeper analysis and proposes mitigation |

**Round 1 bracket:** 4.5–6.0

**Narrowing analysis:** The paper is clearly above the 3.0-range rejected papers on activation steering (z1yI8uoVU3) — it has a novel finding (universal attack), broader experiments, and a practical case study. It is comparable to the ActAdd paper (5.0) which also has interesting contributions but significant framing issues and split reviews. However, it falls below accepted papers in the 6.14–6.67 range (hXA8wqRdyV, YzxMu1asQi, aSy2nYwiZ2), which have clearer threat models, stronger results, or more analytical depth. The paper's three major weaknesses — framing overreach, overstated "universal" claim, and misleading "black-box" characterization — are all addressable with revision but collectively represent a significant gap between claims and evidence that prevents acceptance in the current form.

**Final score: 5.0** — The paper documents a real and interesting phenomenon with genuine experimental rigor and a novel contribution (universal attack construction). However, the systematic overclaiming — framing a perturbation-fragility finding as an interpretability critique, calling a model-dependent attack "universal," and claiming "black-box access" for an internal-access technique — creates a meaningful gap between what the paper promises and what it delivers. These issues are addressable through reframing and more precise language rather than additional experiments, but they are substantial enough that the paper is not ready for acceptance in its current form.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>