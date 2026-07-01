## Summary

This paper presents **RedSage**, an open-source 8B cybersecurity LLM trained via a three-stage data-centric pipeline: (1) large-scale continual pretraining on 11.7B tokens of filtered web and curated high-quality cybersecurity documents, (2) supervised fine-tuning on 266K multi-turn dialogues produced by an agentic augmentation pipeline that transforms seed resources into realistic expert conversations, and (3) direct preference optimization (DPO) on general preference data. To evaluate the model, the authors introduce **RedSage-Bench**, a 30K-question benchmark spanning knowledge, practical offensive skills, and tool expertise, alongside 240 open-ended Q&A items with LLM-as-judge scoring. At the 8B scale, RedSage achieves state-of-the-art results on multiple external cybersecurity benchmarks (up to +5.59 points over baselines) and also improves on general LLM leaderboard tasks (+5.05 points). The authors commit to releasing all models, datasets, and code, enabling privacy-preserving local deployment.

## Strengths

- **Comprehensive open-source release.** RedSage is one of the few efforts that combine large-scale continual pretraining, curated seed data, agentically augmented SFT, and a new benchmark, all with open data, model, and code. This directly advances reproducibility in a domain where closed-data pipelines are the norm (Table 2).
- **RedSage-Bench fills a gap.** Existing cybersecurity benchmarks either lack tool proficiency evaluation, omit open-ended quality assessment, or cover only knowledge. RedSage-Bench jointly evaluates knowledge, offensive/defensive skills, and tool expertise (CLI, Kali), and includes a quality dimension for free-form answers (Table 1). This provides a more holistic evaluation framework.
- **Strong empirical results across multiple benchmarks.** RedSage variants consistently outperform strong baselines (including Qwen3-8B and larger models like Qwen3-32B on several metrics) on both cybersecurity-specific benchmarks (CTI-Bench, CyberMetric, SecBench, SECURE, SecEval) and general benchmarks (Open LLM Leaderboard). The improvements are not limited to one evaluation setting.
- **Novel agentic augmentation for cybersecurity conversations.** The Planner–Augmenter pipeline (Fig. 4) converts static seed documents into role-based multi-turn dialogues that reflect real analyst workflows, significantly expanding the training data in a grounded, scalable manner.

## Weaknesses

### Fatal
None.

### Major

1. **Missing ablation isolates the effect of cybersecurity-specific data on general performance.** The paper claims that domain-aware training “helps to improve general reasoning and instruction-following.” However, the instruction-tuned RedSage models (Ins/DPO) are trained with general SFT data (SmolTalk2) and general DPO data (Tulu3) in addition to cybersecurity conversations. The observed gains on general benchmarks (e.g., +7.42 points over Qwen3-8B-Instruct on mean accuracy) could be entirely due to better-quality general instruction data, not the cybersecurity pretraining or agentic augmentation. Without a baseline that trains only the general SFT/DPO data on Qwen3-8B-Base (without any cybersecurity data), the claim is unsupported.

2. **RedSage-Bench is automatically generated with limited human verification.** The MCQ portion (30K items) is created by an LLM teacher and verified by an LLM verifier using chain-of-thought, with only random audits mentioned. The open-ended portion (240 items) is human-verified. Given that the benchmark shares the same seed data used for training, and the decontamination step removes only 0.31% of the training corpus, the risk of distributional bias toward the RedSage family is non-trivial. While external benchmarks partially alleviate this concern, RedSage-Bench is used heavily for analysis (Tables 4, Figure 6) and its reliability as a rigorous evaluation instrument is not fully established.

3. **No human evaluation of open-ended responses.** The open-ended QA evaluation relies entirely on an LLM-as-judge rubric. For a critical domain like cybersecurity, expert human judgment is needed to verify factual correctness, helpfulness, and safety of free-form answers. The absence of any human assessment weakens the validation of the model’s conversational capability.

### Minor

- **Experimental design could be stronger.** The paper does not ablate the agentic augmentation component (e.g., training with RedSage-Seed alone vs. augmented conversations). Similarly, the effect of the two-stage CPT (CyberFineWeb then Seed) versus a single-stage mix is not systematically compared beyond the results in Table 4.
- **Some baseline comparisons are outdated or mismatched.** Llama-Primus-Merged and Lily-Cybersecurity are based on Llama-2/Mistral architectures, while the proposed model uses Qwen3-8B, which is a stronger starting point. The gains over Qwen3-8B itself are modest (+2–3 points on most cybersecurity benchmarks).
- **The benchmark generation pipeline may introduce calibration issues.** The teacher/verifier LLMs are 70-72B models; their own domain knowledge affects both the questions and the scoring. The “quality scores” for open-ended answers are used as the primary metric, but the LLM judge might favor stylistic patterns common in the training data.

### Trivial

- “RedSage-8B-CFP” in Table 4 appears to be a typo for “CFW”.

## Nice-to-Haves

- Perform an ablation experiment that trains Qwen3-8B-Base with only the general SFT and DPO data (no cybersecurity data) and compare to RedSage-Ins/DPO. This would directly measure the value added by the cybersecurity-specific pipeline.
- Include human expert evaluation on a sample of open-ended Q&A responses to complement LLM-based scoring.
- Report inter-annotator agreement or human accuracy on a subset of RedSage-Bench MCQs to validate the quality of the automatic benchmark construction.

## Novel Insights

The paper demonstrates that a carefully constructed data pipeline—combining large-scale web filtering, curated expert resources, and agentically augmented multi-turn conversations—can produce an 8B model that rivals or exceeds much larger models (Qwen3-32B, GPT-5) on domain-specific benchmarks while maintaining competitive general performance. The finding that different data sources (CyberFineWeb vs. Seed) yield complementary strengths (e.g., CFW on general knowledge, Seed on math reasoning) is a practical insight for domain-adapted LLMs. However, the paper’s core claim that cybersecurity-specific training improves general reasoning remains unsubstantiated without proper controls.

## Suggestions

1. Provide the missing ablation described above (general-only SFT/DPO training without cybersecurity data). This is critical to support the claim about general reasoning improvement.
2. Conduct a small-scale human expert study (e.g., 50 responses) to validate the LLM-as-judge scores on the open-ended QA and report agreement rates.
3. For the benchmark, publish the human audit results and the list of open-ended QA items so that the community can reproduce the quality assessment.
4. Clarify in the abstract and conclusion that the general benchmark improvements may stem from the high-quality general instruction data used in post-training, not solely from cybersecurity pretraining.

## Score and Decision

The paper makes valuable contributions—open resources, a new benchmark, and a strong empirical effort—but the lack of an essential ablation to isolate the effect of cybersecurity-specific data on general performance and the reliance on an automatically generated benchmark without sufficient human validation are significant concerns. These weaknesses do not invalidate the paper’s core contributions (the model and benchmark are still useful), but they prevent a higher score.

**Score: 6**  
**Decision: Borderline Accept**

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>