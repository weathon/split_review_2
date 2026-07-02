## Summary

This paper investigates whether activation steering — a technique for controlling LLM behavior by adding vectors to hidden states — can inadvertently compromise safety mechanisms. Through experiments across Llama3, Qwen2.5, and Falcon3 model families (3B–70B) with both random vectors and SAE features, the authors show that even benign or random steering systematically increases harmful compliance. Key findings: (1) random steering produces 2–27% compliance depending on model, (2) SAE features show comparable or slightly higher risk, (3) averaging jailbreak-inducing vectors creates a cross-prompt attack that generalizes to unseen prompts, and (4) a real API case study demonstrates practical exploitability.

## Strengths

1. **Important and timely question.** The paper identifies a genuine gap: whether benign steering vectors (used for legitimate control, not adversarial attacks) can inadvertently compromise safety. This is well-motivated (Sec. 1) and clearly distinguished from prior work on adversarial jailbreak vectors (Sec. 2).

2. **Broad model coverage.** Experiments span three model families at multiple scales (3B–70B), testing both random vectors and SAE features. This breadth substantially strengthens the claim that the phenomenon is systematic rather than model-specific (Sec. 3.3, Sec. 4.1–4.2).

3. **Universal attack finding (Sec. 4.4) is genuinely non-obvious.** Averaging 20 random vectors that each jailbreak a single prompt, then generalizing to unseen harmful prompts (up to 63% compliance on Falcon3-7B), is a novel demonstration. The fact that this requires no model weights, gradients, or harmful training data gives it practical security implications.

4. **Ecological validity via Goodfire API case study (Sec. 4.3).** Demonstrating that a benign SAE feature ("brand identity") deployed through a public production API can jailbreak a model on harmful requests grounds the paper's claims in practical reality. The two failure modes (disclaimer-then-compliance, justification via fictional framing) are empirically documented.

## Weaknesses

### Major

1. **No variance or uncertainty reported for any compliance rate.** All compliance rates are reported as point estimates (e.g., "17% for Llama3-8B," "11% for Qwen2.5-7B," "2–4% higher for SAE") from 1,000-vector samples, but without standard deviations, confidence intervals, or any measure of uncertainty. Without variance, the reader cannot assess whether the 2–4% SAE-vs-random difference is meaningful or within sampling noise, whether the "4×" universal attack improvement is robust or driven by outliers, or how reliable any individual model's compliance rate is. The data to compute these statistics is already available from the 1,000-vector sampling procedure; the omission undermines the precision of all quantitative claims.

### Minor

2. **LLM-as-judge validation metrics not reported in main text.** The paper uses Qwen3-8B as an automated judge for 300,000 responses and references Appx. B for "quality assessment against human annotations," but no agreement metrics (accuracy, Cohen's κ, confusion matrix) appear in the main paper. Since all quantitative conclusions depend on this classifier, a summary of its performance belongs in the main text rather than only in the appendix.

3. **"Universal attack" framing overstates results.** The attack fails on Qwen2.5-32B (compliance drops from 16% to 9%) and shows only modest improvement on several other models (e.g., Llama3-70B: 42% → 50%). The headline "4× average improvement" is heavily driven by Falcon models. The paper acknowledges model dependence but the "universal" label suggests broader generality than the evidence supports.

4. **No defense evaluation.** The paper identifies a vulnerability but does not test whether existing simple defenses (output filtering, perplexity detection, refusal classifiers) catch steering-induced jailbreaks. The conclusion mentions adversarial training and automated audits but does not evaluate any mitigation.

### Trivial

5. **The "2–27%" range in the abstract is not decomposed per model.** The abstract presents this range without attributing which model gives 2% and which gives 27%, making interpretation opaque without reading the full paper.

6. **No ablation of universal attack components.** The choice of 20 averaged vectors is stated but no curve shows how compliance varies with the number of averaged vectors (e.g., does 5 work? 50?). This would strengthen practical characterization.

## Nice-to-Haves

- An analysis of why steering breaks safety (mechanistic study) would substantially increase the paper's actionable value, but is explicitly scoped as future work.
- Testing SAEs from another source or on another model would strengthen the SAE-specific claims beyond a single case (Llama3.1-8B, layer 19).

## Removed Points

These points are flagged to be removed from the main review; treat them with caution:

- **"No mechanism analysis"** (from harsh critic, classified as major): The paper's contribution is empirical (demonstrating the vulnerability), not mechanistic. The paper explicitly acknowledges this as future work (Sec. 5) and references preliminary analysis in Appendix E (parser-stripped but present in original). This is a scope limitation, not a flaw for the paper's stated contribution.
- **"SAE results limited to one SAE on one model"** (from harsh critic): The paper explicitly acknowledges this limitation in Sec. 3.3. It is a scope constraint, not a flaw in the evidence presented.
- **"Missing appendix content"** (implied by harsh critic regarding judge validation): The parser strips appendices; the original submission contains Appx. B with the quality assessment. The valid concern (metrics should be in main text) is captured in minor weakness 2.
- **"2–27% range is very wide"** (harsh critic's section note): The paper acknowledges variability across models; this is a genuine finding about the phenomenon, not a weakness.
- **Various formatting/style nitpicks and generic "the evaluation lacks rigor" framing** without specific textual anchors.
- **Strawman concerns about reproducibility** (hyperparameters, trivial implementation details).

## Novel Insights

None beyond the paper's own contributions.

## Suggestions

1. Report standard deviations or 95% confidence intervals alongside all compliance rates — the data is already available from the 1,000-vector samples.
2. Include judge validation metrics (agreement rate, Cohen's κ) in the main text rather than only in the appendix.
3. Soften the "universal" framing to "generalizable attack" or "cross-prompt attack" to accurately reflect the model-dependent results.
4. Evaluate at least one simple baseline defense (e.g., output-side refusal classifier) or explicitly discuss why this is non-trivial as future work.
5. Add an ablation showing compliance rate vs. number of averaged vectors for the universal attack.
6. Decompose the abstract's "2–27%" range with model attribution.

---

**Calibration Anchors (all rounds):**

| Path | Avg Human Score | Round | Comparison |
|------|:---:|:---:|-----------|
| `5kMwiMnUip.md` (NEMESIS jailbreak) | 1.40 | 1 | Far weaker — trivial jailbreak collection, no systematic analysis |
| `8QTpYC4smR.md` (LLM systematic review) | 1.00 | 1 | Not comparable — generic survey |
| `z1yI8uoVU3.md` (Measuring Steered Repr.) | 3.00 | 1,2 | Narrower scope, same topic — current paper is substantially stronger |
| `BeOEmnmyFu.md` (Language Game jailbreak) | 2.50 | 2 | Narrow method, fewer models — current paper is stronger |
| `HuNoNfiQqH.md` (Understanding Jailbreak Success) | 4.75 | 1 | Mechanistic analysis but narrower empirical scope — comparable quality but different emphasis |
| `r42tSSCHPh.md` (Catastrophic Jailbreak via Generation) | 7.00 | 1,2 | Similar empirical breadth; achieves higher ASR and includes defense; current paper has more novel mechanism (steering) and real API case study |
| `YzxMu1asQi.md` (Scaling Laws for Adversarial Attacks) | 6.50 | 2 | Deeper theoretical analysis of activation attacks; current paper is more applied |
| `hXA8wqRdyV.md` (Simple Adaptive Attacks) | 6.14 | 2 | Strong empirical jailbreak paper; achieves higher ASR; current paper addresses a different question (benign steering vs adversarial optimization) |

**Round 1 bracket:** 5.5–7.0. **Final score:** 6.0 — borderline accept. The paper addresses an important question with broad experiments and a compelling case study, but is held back by the absence of variance reporting and some overstated framing.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>