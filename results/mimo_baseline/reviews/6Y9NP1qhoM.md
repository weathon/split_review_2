## Summary

This paper addresses misinformation injection attacks in LLM-based Multi-Agent Systems (MAS), distinguishing misinformation (semantically benign but factually incorrect) from overtly malicious content. The authors introduce MISINFOTASK, a 108-task dataset for evaluating MAS robustness against misinformation, and propose ARGUS, a training-free defense framework that combines adaptive channel localization (using topological centrality, semantic relevance, and frequency) with goal-aware CoT-based persuasive rectification. Experiments across four LLMs and three attack methods show ARGUS reduces misinformation toxicity by ~28% and improves task success rates by ~10% over baselines.

## Strengths

- **Important and underexplored problem**: The paper meaningfully distinguishes misinformation from overtly malicious content in MAS, identifying a genuine gap. Most prior MAS security work focuses on jailbreaks or overt attacks; the covert, factually-incorrect-but-semantic-benign threat is practically relevant and under-studied.

- **Well-structured two-stage defense design**: The ARGUS framework's separation of localization (spatial) and rectification (temporal) is architecturally clean. The adaptive re-localization mechanism that combines topological importance, semantic relevance to inferred goals, and communication frequency (Equations 2-9) is well-motivated and the ablation in Table 3 demonstrates each component contributes.

- **Comprehensive experimental breadth**: The evaluation spans 4 LLMs from different families (GPT-4o-mini, GPT-4o, DeepSeek-V3, Gemini-2.0-flash), 3 attack vectors (Prompt Injection, RAG Poisoning, Tool Injection), 5 topological configurations, and includes temporal analysis across rounds. The round-by-round MT analysis (Figure 5) convincingly shows misinformation toxicity escalates without defense but decreases with ARGUS.

- **Training-free and modular**: The framework requires no additional training, making it practical to deploy on existing MAS architectures.

## Weaknesses

### Fatal
None.

### Major

- **Small and potentially limited dataset**: MISINFOTASK contains only 108 tasks. For a benchmark dataset intended to evaluate MAS robustness, this is quite small, raising concerns about statistical reliability and generalizability. The paper does not discuss confidence intervals or conduct power analysis. With only ~108 tasks split across multiple conditions, individual experimental cells may contain very few samples, making the reported averages fragile.

- **Circularity in misinformation definition and detection**: The paper defines misinformation as "content that contradicts the factual knowledge implicitly stored in the parameters of an LLM" (Section 2.3), and the defense relies on the corrective agent's own LLM to detect misinformation via "Internal Knowledge Resonance" (Section 4.2). This means ARGUS can only catch misinformation that contradicts what the defending LLM already knows—it fundamentally cannot detect novel misinformation that the LLM's parameters encode as plausible. This limitation is not adequately discussed and represents a significant boundary on the framework's applicability.

- **Limited and potentially weak baselines**: Only Self-Check (simple prompting for self-reflection) and G-Safeguard (GNN-based agent risk scoring) are compared. A natural and stronger baseline would be a simple "knowledge verification" approach where agents cross-check claims against their own parametric knowledge without the complex localization machinery. Without this, it's unclear how much of ARGUS's benefit comes from the localization versus simply having an additional agent that can fact-check.

- **Evaluation judge bias**: GPT-4o (2024-08-06) is used as the automated judge for both MT and TSR metrics, while GPT-4o is also one of the four core LLMs being evaluated. This creates a potential circularity where the judge may favor outputs from models in its own family. The paper does not discuss this concern or validate the judge's reliability.

### Minor

- **Statistical significance not reported**: Table 1 shows standard deviations (subscripts), and several improvements fall within or near the noise margin (e.g., Gemini-2.0-flash TSR improvement from 69.85±1.47 to 72.41±4.43). No statistical significance tests are conducted, making it difficult to assess whether improvements are reliable.

- **Goal inference accuracy is moderate**: Figure 4 shows the corrective agent's accuracy in identifying misleading goals ranges from ~50% to ~80%. The paper does not analyze how errors in goal inference propagate to downstream localization and rectification performance, nor does it discuss what happens when the inferred goal is wrong.

- **Ablation limited to single model**: Table 2's ablation appears to be conducted only on GPT-4o-mini (matching the attack-only numbers from Table 1). This limits confidence in the generalizability of the ablation findings across different LLMs.

- **Cost analysis absent**: The paper acknowledges computational overhead as a limitation but provides no quantification. The framework deploys corrective agents on up to k communication channels per round with CoT reasoning, which could substantially increase latency and API costs. This is important for practical adoption.

### Trivial
None.

## Nice-to-Haves

- A "knowledge-only" baseline that simply has agents verify claims against their own knowledge without the localization mechanism, to isolate the contribution of adaptive localization.
- Analysis of failure cases: when does ARGUS fail, and what characteristics of misinformation cause failures?
- Sensitivity analysis on the number of monitored channels k and the number of MAS rounds.
- Cross-model judge evaluation (e.g., using Claude or Gemini as judge) to validate metric reliability.

## Novel Insights

The paper's most novel observation is that misinformation in MAS exhibits a progressive contamination pattern across rounds (Figure 5), where toxicity escalates over time without intervention—demonstrating that MAS communication topologies amplify misinformation rather than naturally correcting it. This finding motivates the temporal, multi-round defense approach and provides empirical evidence that MAS are not self-correcting against subtle factual errors, which is a meaningful insight for the community. The distinction between misinformation and malicious content as a threat model for MAS is also a useful conceptual contribution, even if the defense approach itself is somewhat incremental.

## Suggestions

- Expand MISINFOTASK significantly (ideally 500+ tasks) and report per-condition sample sizes to improve statistical reliability.
- Add a "knowledge verification only" baseline to isolate the value of the localization component.
- Conduct statistical significance tests (e.g., bootstrap confidence intervals or paired t-tests) for all reported improvements.
- Discuss the fundamental limitation that ARGUS can only detect misinformation contradicting the LLM's existing knowledge, and explore how this boundary could be extended (e.g., through retrieval augmentation).
- Report computational cost (tokens consumed, latency) of ARGUS versus the baselines.

## Score and Decision

The paper addresses a relevant and underexplored problem with a reasonable framework and shows consistent improvements across multiple settings. However, the small dataset (108 tasks), limited baselines, circularity in the misinformation definition, and lack of statistical rigor temper enthusiasm. The contributions are solid but incremental rather than transformative.

MY FINAL SCORE: <score>5.0</score>
MY FINAL DECISION: <decision>Reject</decision>