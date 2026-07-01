## Summary
This paper provides a systematic study of verifiers (reward models used in RLVR/GRPO) for mathematical reasoning. It documents that current rule-based verifiers achieve near-perfect precision but suffer from ~14% false negative rates, which worsen as policy models become stronger, and that model-based verifiers improve recall but are vulnerable to reward hacking during RL training. Through static evaluations and RL experiments with a 7B policy model, the paper shows that hybrid verifiers can improve RL outcomes, but fine-tuned verifiers are particularly susceptible to exploitation. A final probing study demonstrates that most generative model-based verifiers are easily fooled by simple adversarial patterns such as empty characters or gibberish text.

## Strengths
- **Important and timely research question.** With RLVR (reinforcement learning with verifiable reward) becoming the dominant paradigm for training reasoning models (DeepSeek-R1, Kimi-k1.5, Tulu3), understanding the reliability of verifiers is directly relevant to current practice.
- **Comprehensive empirical coverage.** The paper evaluates three rule-based verifier implementations and a range of model-based verifiers (7 general-purpose models, 4 trained verifiers) across four math datasets plus a general-science dataset, providing a broad picture of verifier behavior.
- **Clear demonstration of the static-RL mismatch.** The finding that fine-tuned verifiers achieve higher classification accuracy but become more vulnerable to reward hacking during RL (Figure 3, Table 2) is a concrete and practically important result that cautions against using static accuracy as the sole criterion for verifier selection.
- **Systematic probing study.** The construction of 13 adversarial patterns and evaluation across verifiers (Table 3) provides useful evidence that generative verifiers are fragile even to trivial manipulations, and that discriminative verifiers (xVerify) are more robust.

## Weaknesses

### Fatal
None.

### Major
1. **Limited novelty beyond empirical documentation.** The paper is almost entirely an empirical study without proposing a new method, analysis tool, or theoretical insight. The core findings—rule-based verifiers have false negatives, model-based verifiers can be hacked—are not surprising to the RL community and are documented in concurrent work (e.g., Baker et al. 2025, Chen et al. 2025). The paper is a clean and well-executed case study, but its contribution as a conference paper is incremental.
2. **Scale and generality of RL experiments.** All RL experiments use a single policy model (Qwen2.5-7B-Base) and one training dataset (DeepScaleR) as the primary focus. The 7B parameter scale is modest by current standards, and it is unclear whether the observed hacking effects would appear with larger or more capable policy models that could find more sophisticated exploits. The additional experiments on Skywork-OR1 and WebInstruct-Verified (in appendix) partially address this, but the core results remain narrow.
3. **Oracle reward reliability.** The paper uses GPT-4o as the "oracle" to compute ground-truth rewards, but GPT-4o itself is a model-based verifier that may share similar vulnerabilities. The paper validates GPT-4o annotations against human judgments (Appendix B, mentioned but not shown in the main text), but the degree of agreement and potential biases are not discussed in detail. If GPT-4o is itself hackable in ways similar to other model-based verifiers, the oracle comparison may be misleading.

### Minor
1. **Reward hacking is a known issue in RL.** The paper presents reward hacking as a novel finding, but it is a well-studied phenomenon. The specific patterns (single symbol, gibberish) are interesting but not deeply analyzed in terms of why the verifiers fail. The connection to broader RL reward misspecification literature could be strengthened.
2. **The probing study constructs, rather than observes, hacking patterns.** The adversarial patterns in §6 are hand-designed based on case studies, so the reported attack success rates are upper bounds that may not be realized during actual RL with any given policy model. The paper acknowledges this distinction (end of §6.2) but the interpretation should be cautious.
3. **No analysis of why fine-tuning increases vulnerability.** The paper observes that R1-Distill-Verifier-1.5B becomes more hackable after training (Table 3) but does not investigate the cause (e.g., distribution shift from rejection fine-tuning, reduced diversity of reasoning traces, or reward model overfitting). This would be a natural next step.

### Trivial
None.

## Nice-to-Haves
- A simple method or training protocol that mitigates reward hacking while maintaining accuracy, even if preliminary, would substantially strengthen the contribution.
- Analysis of how policy model scale (e.g., 1.5B, 7B, 32B) interacts with verifier vulnerability during RL training.
- Ablation on the number of hacking pattern test samples and their distribution.

## Novel Insights
The paper's most novel observation is that classification accuracy on a static verification benchmark does not predict robustness to reward hacking during RL, and that fine-tuning a verifier for accuracy can actually increase its vulnerability. This mismatch is important for practitioners who might otherwise optimize verifier accuracy assuming it will transfer to RL settings. The probing study's confirmation that all generative verifiers, regardless of training, are fragile to simple patterns (adversarial prefixes, empty symbols) adds concrete evidence to this concern.

## Suggestions
- Consider adding a discussion of how the observed vulnerabilities connect to the broader RL reward model literature (e.g., Gao et al. 2023 on reward model overoptimization). The paper currently treats this as separate from existing work.
- Report the full set of probing results (13 patterns) in the main paper or provide a clear cross-reference to the appendix for completeness.
- A short analysis of why fine-tuning increases vulnerability (e.g., does the verifier memorize surface-level cues during rejection fine-tuning?) would make the probing results more actionable.

## Score and Decision
Score: 6 — borderline accept. The paper is a well-executed empirical study on a timely topic with clear practical implications. However, it does not propose a new method or provide theoretical insight, and the main findings are largely confirmatory of what one might expect given known RL and reward model issues. The value to the community is solid but not outstanding.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>