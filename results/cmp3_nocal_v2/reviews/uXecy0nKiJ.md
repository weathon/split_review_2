Now let me write the final consolidated review.

## Summary

This paper investigates whether *benign* activation steering — the kind used for legitimate model control via interpretable directions, not adversarially optimized vectors — inadvertently compromises LLM safety. Through experiments across Llama3, Qwen2.5, Falcon3, and FalconH1 (3B–70B), the authors show that (1) even random-direction steering increases harmful compliance from 0% to 2–27%, (2) SAE features with benign semantic labels (e.g., "brand identity") can jailbreak models, and (3) averaging 20 random vectors that jailbreak a single prompt yields a universal attack that generalizes to unseen harmful prompts. A case study using the Goodfire API validates the practical risk.

## Strengths

- **Broad experimental scope for random steering.** The paper systematically tests random steering across four model families at scales from 3B to 70B, with sweeps over layers and steering coefficients (Sec. 4.1, Fig. 2). This breadth across Llama3, Qwen2.5, Falcon3, and FalconH1 strengthens the claim that the vulnerability is not model-specific.

- **The universal attack finding is simple and impactful.** Section 4.4 demonstrates that averaging 20 random vectors that jailbreak a single prompt produces a vector that generalizes to unseen harmful prompts — achieving up to 64% compliance on Falcon3-7B and 50% on Llama3-70B (Fig. 6). The attack requires only black-box access and no gradients or model weights, which is a clean, practical finding with clear security implications.

- **Practical validation via a real API.** The case study in Sec. 4.3 using the Goodfire API adds ecological validity that pure lab experiments lack. The behavioral failure modes identified ("disclaimer-then-compliance" and "justification via fictional framing") are genuinely interesting and would be encountered by practitioners.

## Weaknesses

### Fatal
None.

### Major

- **No statistical uncertainty reported for any headline number.** Every major result is presented as a point estimate — "17% overall compliance" (Fig. 3), "668 out of 1000 features can jailbreak at least five prompts" (Sec. 4.2), "4× increase" (Sec. 4.4) — without confidence intervals, standard errors, or variance estimates. The experiments involve multiple sources of randomness (which vectors are sampled, which features are tested, which prompts are used), yet all are run with a single fixed seed (42). For example, the claim that 668/1000 features "can jailbreak at least five prompts" depends on the threshold of five and the specific 100 prompts; a binomial confidence interval would quantify the uncertainty. The absence of any variance measure downgrades the paper from a rigorous empirical study to a suggestive one. This is the most significant gap, as the paper's contribution is entirely empirical.

### Minor

- **The universal attack's "4×" headline overstates typical efficacy.** The Fig. 6 data show that the improvement is heavily model-dependent: Qwen2.5-32B gets 9% (identical to random, worse than the single-vector baseline of 16%); Qwen2.5-7B gets ~1.8×; Qwen2.5-3B gets ~1.8×; Falcon-H1-34B gets ~1.6×. The "4×" average is driven almost entirely by the Falcon3 family (11–13×). The paper does acknowledge model dependence in the body ("effectiveness varies substantially across model families," "reduction in performance observed for Qwen2.5-32B"), but the abstract, introduction, and conclusion lead with the 4× headline without qualifying how few models actually achieve it. The core finding is still real and important, but the rhetoric overstates its generality.

- **The SAE vs. random cross-model comparison in Fig. 3 confounds vector type with model architecture.** The paper presents side-by-side compliance rates for Llama3-8B (random, 17%), Qwen2.5-7B (random, 11%), and Llama3.1-8B (SAE, 10%) as if they jointly inform the SAE-vs-random question. But the clean SAE vs. random comparison exists only on Llama3.1-8B in Fig. 2c (where SAE is 2–4% higher). The reader cannot tell from Fig. 3 whether the 10% SAE rate is lower than the 17% random rate because SAE is less dangerous or because Llama3.1-8B is simply more robust than Llama3-8B. The paper should either confine its headline SAE-vs-random comparison to the within-model setting or explicitly note the confound.

- **The "benign features jailbreak models" framing is rhetorically overplayed.** The paper tests 1,000 SAE features and retroactively observes which ones jailbreak and what their semantic labels are. This is a valid observational finding, but the paper's language ("alarmingly," "benign features... demonstrate comparable harmful potential") suggests the paper *set out* to steer a benign concept and *discovered* it jailbreaks — which the case study (Sec. 4.3) does separately support, but the broader 1,000-feature analysis is a correlate study, not a controlled experiment. The finding is genuine, but the alarm in the abstract and introduction outpaces what the data alone establish.

### Trivial

- **The abstract's "0% to 2–27%" range for random steering conflates variation across models, layers, coefficients, and prompts.** The 27% upper bound is not contextualized; a reader might infer it is a typical worst case, but the experimental sweep (Fig. 2) shows most configurations produce much lower rates. Stating which specific condition yields 27% would improve clarity.

## Nice-to-Haves

- **Investigate the mechanism more directly in the main text.** The paper references "preliminary analysis of potential mechanisms (App. E)" but the main text draws no mechanistic conclusions. Even a brief discussion of whether the effect is driven by capability degradation (vs. specific circuit interference) would strengthen the narrative.
- **Compare with one optimized attack baseline.** The paper cites prior work on adversarially optimized jailbreak vectors but never benchmarks against them. A single comparison point (e.g., does the universal vector match or fall short of an optimized attack?) would help calibrate severity.
- **Expand SAE experiments beyond one SAE.** The paper limits SAE experiments to Goodfire's SAE on Llama3.1-8B layer 19 and acknowledges this limitation. Additional SAE sources would strengthen generalizability but are not required for the paper's core claims.

## Removed Points

These points are flagged to be removed; treat them with caution.

- **"Benign framing is methodologically circular"** — Removed because the paper's case study (Sec. 4.3) directly tests an intentionally benign SAE feature ("brand identity") and demonstrates jailbreaking, which exactly matches the narrative. The observational 1,000-feature analysis is complementary, not circular.
- **"No investigation of mechanism"** — Removed because the paper references "preliminary analysis of potential mechanisms (App. E)" in the main text (line 151). The appendix is not visible due to parser stripping, but the paper claims the analysis exists.
- **"Case study disclaimers undermine finding"** — Removed because the paper explicitly identifies and names the "disclaimer-then-compliance" failure mode as part of its finding, not as a counterargument.
- **"Comparison to existing activation-space attack methods missing"** — Removed as outside the paper's stated scope (the paper studies *benign* steering, not whether benign steering is more/less effective than optimized attacks).
- **"Fixed seed limits generalizability"** — Subsumed under the "no statistical uncertainty" Major weakness; the seed itself is fine, the absence of any uncertainty measure is the problem.
- **"Steering coefficient of 2.0 is very large"** — Removed as speculative; the paper normalizes by layer activation norm and tests a sweep, which is standard practice.
- **"Zero-shot claim for universal attack"** — Removed because the paper uses "zero-shot" to mean "requires no harmful training data, model weights, gradients, or logits" (line 239), which is defensible.

## Novel Insights

None beyond the paper's own contributions. The reviews do not surface any novel interpretation of the results that the paper itself does not provide.

## Suggestions

1. **Add confidence intervals or bootstrapped standard errors** to all compliance rate figures. The experimental design (1,000 vectors × 100 prompts) already generates sufficient data to compute uncertainty. This single change would dramatically increase the empirical rigor.
2. **Report the universal attack results per-model** in the abstract and conclusion, not just the 4× average. For example: "the universal attack improves compliance by 1.0–13× depending on the model, with 2 of 8 models showing no improvement."
3. **Separate the SAE-vs-random comparison from the cross-model comparison** explicitly. Use Fig. 2c as the primary comparison and present Fig. 3 as a separate (cross-model) analysis with a clear caveat.

## Score and Decision

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>