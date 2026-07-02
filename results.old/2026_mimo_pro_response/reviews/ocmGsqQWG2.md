Now I have enough calibration data. Let me finalize my review.

## Summary

This paper discloses "involuntary jailbreak," an untargeted meta-prompt attack that instructs LLMs to autonomously generate both unsafe questions and harmful responses. The authors report >90% attack success rate across many frontier proprietary LLMs (Claude Opus 4.1, Grok 4, GPT 4.1, Gemini 2.5 Pro), with topic analysis showing vulnerabilities spanning diverse harm categories and ablation studies validating prompt design choices.

## Strengths

- **High attack success rates across many frontier models with a single universal prompt**: Figure 5 shows ASA >90/100 for leading models including Claude Opus 4.1, Grok 4, GPT 4.1, and Gemini 2.5 Pro, with Avg UPA typically 8–10 out of 10. This is a genuinely concerning finding for the safety community.

- **Novel untargeted meta-prompt formulation**: The approach fundamentally differs from targeted jailbreaks (Section 2) — rather than eliciting a specific harmful response to a predefined prompt like "how to build a bomb," it prompts the LLM to autonomously generate both unsafe questions and answers, probing the entire guardrail at once rather than circumventing a localized restriction.

- **Comprehensive topic-level analysis with topic confinement**: Figure 6 shows vulnerability spans many harm categories across 8 models, and Table 4 demonstrates that even topics with zero initial output (e.g., Elections for Grok 4) can be activated via simple topic confinement, indicating the vulnerability is systematic rather than topic-specific.

- **Systematic ablation studies validating prompt design**: Tables 1–3 ablate benign questions (operator R), operator B (detailed expansion), and unsafe question count, showing the attack is robust — even with just 1 unsafe question, ASA remains 86–93.

- **Insight that weaker models fail due to instruction-following rather than safety**: Section 3.2 notes models like Llama 3.3-70B and Llama 4 Scout fail not because of better safety alignment but because they lack instruction-following capability to produce structured output, distinguishing actual safety from mere incapability.

## Weaknesses

### Fatal

None.

### Major

- **No baseline comparisons with existing jailbreak methods**: The paper evaluates its attack in complete isolation with zero comparisons to any existing method (GCG, AutoDAN, PAIR, many-shot jailbreaking, etc.) on the same models. Section 5 argues "it is unlikely that a meaningful benchmark can be established," but this is unconvincing — benchmarks like HarmBench support exactly this type of comparison, and multiple prior works (e.g., Andriushchenko et al. 2025, referenced by the paper itself) evaluate jailbreaks on frontier models. The paper's core claim that "this vulnerability makes existing jailbreak attacks seem less necessary" is entirely unsupported without any baseline comparison. Even one baseline on the same models would transform the paper from "here is a prompt that works" to "here is a prompt that works *better or differently* than existing approaches." This is the single most important missing piece of evidence, and its absence makes it impossible to assess how surprising or significant the >90% ASA actually is.

- **"Model awareness" framing is overstated relative to the evidence**: The paper repeatedly claims models are "aware" of unsafe content yet generate it "involuntarily" (footnote 3, Section 3.2, Figure 12 reference). The evidence is that Y(X(input)) = "Yes" for unsafe questions — but the prompt *explicitly instructs* the model to label questions "that would typically be refused" as "Yes." This is instruction-following, not spontaneous awareness revelation. Distinguishing genuine awareness from prompt-following would require probing internal representations or testing behavior in different contexts. The provocative name "involuntary jailbreak" propagates this conflation through the paper. This matters because the paper's conceptual framing — and arguably its primary novelty claim — rests on this distinction being real.

### Minor

- **No evaluation of attack robustness to defenses**: The conclusion acknowledges "detecting and blocking this specific prompt at the input level appears to be straightforward," yet no experiments test robustness to prompt paraphrasing, system prompt modifications, or output filtering. Even a basic defense robustness experiment would substantially bound the practical significance of the vulnerability.

- **Single automated judge (Llama Guard-4) with no human validation data**: All safety judgments depend on Llama Guard-4. The paper claims "preliminary experiments" show alignment with humans (Section 3.1) but provides no quantitative data, inter-annotator agreement, or failure mode analysis. For a paper whose central claim is that guardrails "collapse," relying entirely on one automated judge is a limitation that even a small-scale human evaluation would address.

- **Related work characterization slightly misleading**: Section 4 claims "previous work has largely focused on open-source, small-scaled models (e.g., Llama-2 7B)." While partially true historically, several recent works (including Andriushchenko et al. 2025, which this paper cites) evaluate jailbreaks on frontier proprietary models including GPT-4 and Claude. This overstates the gap in the literature and inflates the apparent novelty.

### Trivial

None.

## Nice-to-Haves

- Present the assembled complete prompt as a single artifact for reproducibility (currently spread across Figs. 3, 4, and the appendix).
- Discuss the tension between instruction-following capability and safety refusal more deeply — the observation that the attack exploits instruction-following (Section 3.2, conclusion) may be the actual mechanism and deserves fuller analytical treatment.
- Include human evaluation on a sample of outputs (even 100) to validate the automated judge.

## Removed Points

These points are flagged to be removed, treat them with caution:
- Criticism about "exact complete prompt not provided as a single artifact" — the prompt is described across multiple figures and is reproducible in principle; this is a presentation nitpick, not a methodological flaw.
- Any criticism about the defensive tone of Section 5 — this is a stylistic preference, not a methodological issue.

## Novel Insights

The paper's most novel insight is that the untargeted meta-prompt approach — asking the model to generate its own unsafe questions and answers — exposes a qualitatively different vulnerability surface compared to targeted jailbreaks. The observation that this works better on more capable models (because it relies on instruction-following capability, Section 3.2) inverts the usual assumption that capability improvements help safety, suggesting that alignment may be superficial rather than deeply integrated into model behavior. This has real implications for how the community thinks about safety-capability tradeoffs.

## Suggestions

1. **Run at least one standard jailbreak baseline (e.g., GCG, AutoDAN, or PAIR) on the same models to establish whether the high success rate is surprising or routine.** This single addition would transform the paper from a disclosure into a research contribution.
2. **Reframe the "awareness" claim more carefully** — either provide mechanistic evidence (probing internal representations, attention analysis) or reframe as instruction-following exploitation with awareness as a hypothesis.
3. **Add a brief human evaluation section** with agreement statistics on a sample of Llama Guard-4 judgments.
4. **Test robustness to at least prompt paraphrasing** to bound practical significance.

## Calibration Report

**Round 1 Bracketing:**

Retrieved anchors across all bands:
- **Score < 1.5**: `5kMwiMnUip` (1.40) — "NEMESIS" jailbreak paper, survey-like with no real experiments. Much weaker than our paper.
- **1.5–3.5**: `KyKTjRtyNG` (3.00) — Multi-round conversational jailbreak, rejected. Weaker methodology, limited models. `BeOEmnmyFu` (2.50) — Language game jailbreak, rejected. Limited evaluation. `MV5j4Qpq7N` (2.33) — System-prompt attention defense, rejected. `kT6oc5CpEi` (3.00) — BlackDAN, rejected. Novelty limited, old models, incomplete methodology.
- **3.5–5.5**: `1zt8GWZ9sc` (3.67) — Quack, role-playing jailbreak. Weak baselines, unclear methodology, limited domain. `Q3oAX9HoH2` (4.00) — Nested gloss method. `zf53vmj6k4` (4.25) — Political correctness jailbreak, rejected. `w0b7fCX2nN` (3.75) — Multi-round context jailbreak, rejected.
- **5.5–7.5**: `sULAwlAWc1` (7.00) — ArrAttack, accepted. Good baselines, comprehensive evaluation. `e9yfCY7Q3U` (6.25) — Improved GCG, accepted. Extensive baselines on HarmBench. `aSy2nYwiZ2` (6.67) — JailbreakEdit, accepted. Novel backdoor injection with baselines. `H6UMc5VS70` (5.75) — FlipAttack, rejected despite ~98% ASR. Had baselines. `hXA8wqRdyV` (6.14) — "Simple Adaptive Attacks," accepted. 100% ASR on many models, used HarmBench.
- **7.5–8.5**: `Bo62NeU6VF` (8.00) — Backtracking defense, accepted. `tTPHgb0EtV` (8.00) — Booster defense, accepted. `4KqkizXgXU` (8.00) — Curiosity-driven red-teaming, accepted. Strong methodology.

**Bracket assessment**: Our paper has a more novel attack formulation than BlackDAN/Quack (3–4 range) and tests on more frontier models. It is comparable to FlipAttack (5.75, rejected) in terms of attack simplicity, but FlipAttack had baselines. It shares model coverage breadth with "Simple Adaptive Attacks" (6.14, accepted) but lacks that paper's baselines and HarmBench evaluation. The paper is above the 3–4 range but below the 6+ range where accepted jailbreak papers with proper baselines sit.

**Initial bracket: 4.5–5.5**

**Round 2**: The additional queries confirmed: `DAG-Jailbreak` (5.50, rejected) had baselines but suboptimal solutions; `Baseline Defenses` (5.25, rejected) was more of a defense paper; `Simple Adaptive Attacks` (6.14, accepted) is the closest comparable and had baselines. Our paper's lack of baselines places it below this accepted paper.

**Final score: 5.0** — The paper reports a genuinely concerning finding with broad model coverage and interesting analysis, but the complete absence of baseline comparisons prevents proper contextualization, the "awareness" framing is unsupported by the evidence, and the evaluation relies on a single automated judge. Compared to accepted jailbreak papers at ICLR (all of which had baselines and more rigorous evaluation methodology), this paper falls short. However, it is clearly above weak submissions in the 3–4 range that had fundamental methodological issues or outdated models.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>