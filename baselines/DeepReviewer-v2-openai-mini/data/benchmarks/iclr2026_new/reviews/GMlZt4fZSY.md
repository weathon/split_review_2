## Summary
# Final Review Report

## Summary

This paper presents MobileLLM-R1, a series of sub-billion parameter language models (140M, 360M, 950M) trained with a data-centric framework designed to elicit strong reasoning capabilities under tight token budgets. The authors make two primary methodological contributions: (1) a benchmark-free, influence-based data mixing strategy for pre-training that leverages cross-domain influence scores (extending the AutoMixer framework), and (2) an iterative data-model co-evolution approach for mid-training that compresses datasets by filtering samples with non-positive influence scores. Using only 4.2T training tokens (drawn from ~2T curated open-source data), MobileLLM-R1-950M achieves competitive results against models trained on substantially larger corpora (e.g., Qwen3-0.6B trained on 36T tokens). All models, data recipes, and training configurations are open-sourced, supporting reproducibility.

The paper addresses an important question — whether strong reasoning can emerge in small models without massive data — and provides a transparent, fully open-source benchmark. The empirical results show impressive gains over prior fully open-source models (OLMo, SmolLM) at comparable or smaller scales. However, several methodological details limit the strength of the conclusions: lack of statistical variance reporting, reliance on an external influence approximation without independent validation, potential selection bias in the data-model co-evolution loop, and rhetorical overclaiming in the positioning against Qwen3-0.6B. The overall contribution is valuable as an open-source recipe paper, but the scientific claims about data efficiency require more controlled validation.

```text
ASCII Diagram — Paper Structure & Evidence Map

[Claim: Token-efficient reasoning in small models is achievable with principled data curation]
    |
    ├── [C1: Benchmark-free influence-based data mixing]
    │   ├── Evidence: Leave-one-out NLL analysis (Fig 3)
    │   ├── Evidence: Perplexity improvement over uniform mixing (Fig 4)
    │   └── Gap: Influence approx (AutoMixer) not independently validated
    │
    ├── [C2: Data-model co-evolution for mid-training compression]
    │   ├── Evidence: Influence score convergence (Fig 5)
    │   ├── Evidence: MMLU improvement over original data (Fig 6)
    │   └── Gap: Selection bias from using same model for filtering & training
    │
    └── [C3: State-of-the-art results among fully open small models]
        ├── Evidence: GSM8K, HumanEval, MATH, AIME, LCBv6 comparisons (Figs 8-9)
        ├── Evidence: Controlled SFT comparison (Table 2)
        └── Gap: No statistical variance; confounds in cross-model comparisons
```

## Strengths
1. **Timely and well-motivated research question.** The paper tackles a practically important problem: whether small language models can develop strong reasoning abilities without requiring massive (36T+) token budgets. With growing interest in on-device AI, the question of token-efficient training for small models is both timely and impactful. The central hypothesis — that principled data curation can substitute for scale — is clearly stated and directly tested.

2. **Fully open-source transparency.** The authors release all trained model weights, complete training recipes, data sourcing details, mixing ratios, and code. This level of openness is a significant strength that enables reproducibility and follow-up research. Among the comparisons, MobileLLM-R1 is one of the most thoroughly documented sub-billion reasoning model efforts.

3. **Methodologically interesting data curation pipeline.** The combination of leave-one-out analysis for dataset importance (Section 2.1.2), influence-based cross-capability data mixing (Section 2.2), and iterative mid-training compression (Section 3) forms a coherent and novel pipeline. The idea of using influence scores from domain-specialized checkpoints to guide data mixing is creative, and the convergence analysis of influence scores during iterative compression provides useful insight into when additional data stops being beneficial.

4. **Strong empirical results against fully open baselines.** In the controlled SFT comparison (Table 2), MobileLLM-R1 substantially outperforms SmolLM2 and OLMo-2 at comparable or smaller model sizes. The 140M model achieving 4.8 MATH vs 3.2 for SmolLM2-135M, and the 950M model achieving 68.5 GSM8K vs 50.5 for SmolLM2-1.7B, represent meaningful improvements that clearly demonstrate the value of the proposed data curation approach.

5. **Informative ablation studies.** The post-training ablation (Table 1) provides clear insights into the staged training pipeline, especially the finding that instruction-following SFT before reasoning SFT outperforms joint training on math and general reasoning. The finding that domain-specific reasoning data can reduce MMLU performance is honestly reported and provides useful guidance for practitioners.

## Weaknesses
### W1. No statistical variance or significance testing across all experiments (Severity: Major)

Every benchmark result in the paper — including the main comparisons (Table 2, Figures 8-9), ablations (Table 1), and data efficiency claims — is reported as a single point without variance, confidence intervals, or significance tests. For small models where training noise can be proportionally larger, single-run results are insufficient to establish statistical reliability. For example, Table 1 shows MATH scores ranging from 16.2 (Tulu-3 + C) to 60.0 (Tulu-3 + M+S). Without variance, the reader cannot assess whether the gap between 57.8 and 60.0 is meaningful or within noise range. The paper's central claim about matching Qwen3-0.6B's performance with only 11.7% of the tokens is particularly vulnerable without multi-seed validation.

**Recommended fix:** Report mean ± std over at least 3 random seeds for all main experiments. For pairwise comparisons (e.g., MobileLLM-R1 vs. Qwen3-0.6B), add a paired bootstrap or permutation significance test. At minimum, include a statement acknowledging this limitation and providing single-seed results as preliminary evidence.

### W2. Influence score computation lacks independent validation and sufficient description (Severity: Major)

The influence-based data mixing (Section 2.2) is one of the paper's two core methodological contributions, yet the approximation that makes Eq. 2 tractable is not described in the paper. The text states that AutoMixer "bypasses explicit Hessian inversion," but no details of the approximation, its assumptions, its error bounds, or its computational cost are provided. This creates a reproducibility gap: a reader cannot implement or assess the core contribution from the paper alone.

Additionally, the domain-specialized checkpoints ($\theta_{\mathcal{C},t}$, $\theta_{\mathcal{M},t}$, $\theta_{\mathcal{K},t}$) require training three separate models to convergence — a significant computational overhead whose cost-benefit ratio is not quantified. An ablation comparing the AutoMixer influence-based mixture against simpler heuristic mixtures (e.g., equal weighting, perplexity-based weighting) would establish the value of this complexity.

**Recommended fix:** (1) Provide a self-contained description of the influence approximation, including any simplifying assumptions (e.g., empirical Fisher, Neumann series truncation, or K-FAC). (2) Add an ablation comparing influence-based mixing against uniform and heuristic baselines at a smaller scale. (3) Report the computational cost of training domain-specialized checkpoints.

### W3. Potential selection bias in the data-model co-evolution loop (Severity: Major)

The mid-training compression (Section 3) filters samples based on influence scores computed from the same model being trained (Eq. 6-7). This creates a feedback loop where the model may discard samples that are currently unhelpful but would become beneficial at a later training stage. The observed convergence of influence scores toward zero (Figure 5) could reflect specialization to a narrow filtered distribution rather than genuine exhaustion of the dataset's information content.

The comparison in Figure 6 shows an unexplained dip in the "original" data at 30K steps (from 38.0 to 29.0 between 20K and 30K, then back to 31.0 at 40K). This non-monotonic behavior in the original data is not explained and could indicate a training instability rather than a systematic advantage of subsampling. Without understanding this dip, the claim that subsampling "leads to more robust and stable performance trends" is weakened.

**Recommended fix:** (1) Add a small experiment where samples with negative influence at phase t are re-introduced at phase t+1 to test whether they become beneficial later. (2) Investigate and explain the 30K step dip in the original data condition. (3) Report the fraction of samples retained after each compression stage.

### W4. Controlled comparison confounded by instruction-tuning asymmetry (Severity: Major)

Table 2 is designed to "disentangle the contribution of curated pre-training and mid-training data" by applying identical reasoning SFT to all models. However, the baseline models use their "instruct checkpoints" while MobileLLM-R1 uses an intermediate Tulu3-SFT checkpoint. Different baseline models received different instruction-tuning recipes (e.g., OLMo-2-0425-1B-SFT uses its own SFT data, SmolLM2-Instruct uses different alignment data). This asymmetry means the comparison does not isolate pre-training quality as cleanly as claimed.

Furthermore, MobileLLM-R1's Tulu3-SFT checkpoint was trained for 2 epochs on Tulu-3, while baselines may have had more or less instruction tuning. The 950M model's advantage of 57.8 vs 53.0 MATH over OLMo-2-1.48B could partly reflect differences in the instruction-tuning phase rather than pre-training quality alone.

**Recommended fix:** Add a control condition where all models start from their base (non-instruct) checkpoints, receive the identical Tulu-3 instruction tuning (same data, epochs, learning rate), and then receive the shared reasoning SFT. This would genuinely isolate pre-training quality.

### W5. Overclaiming in positioning against Qwen3-0.6B (Severity: Major)

The abstract and introduction claim that MobileLLM-R1 "matches or surpasses Qwen3-0.6B across multiple reasoning benchmarks" despite using only 11.7% of the tokens. This comparison has several confounds that are not adequately disclosed: (a) Qwen3-0.6B uses a different tokenizer, vocabulary size, and architecture; (b) MobileLLM-R1's 4.2T tokens exclude mid-training (200B extra tokens) while the 36T figure for Qwen3 refers to pre-training only; (c) MobileLLM-R1 uses considerably more recent SFT datasets (OpenMathReasoning, OpenCodeReasoning-2 released in 2025) that may overlap with benchmarks differently than Qwen3's training data; (d) Table 2 does not include Qwen3-0.6B, so the controlled comparison that would support the claim is missing.

The paper also claims "state-of-the-art results among small models with a fully open-sourced recipe" in the conclusion without specifying the comparison scope. SOTA claims require precise definition of the comparison set (model size range, benchmark set, evaluation protocol) and should be bound to the evidence.

**Recommended fix:** (1) Replace "matches or surpasses" with "achieves competitive results with" or "achieves comparable scores on several benchmarks." (2) Include Qwen3-0.6B in Table 2's controlled SFT comparison. (3) Specify exact comparison scope for SOTA claims. (4) Clearly state that token efficiency is one dimension and that total compute (FLOPs) is another relevant axis.

### W6. Ask-LLM curation may introduce circular bias (Severity: Moderate)

The capability-probing dataset construction (Section 2.1.1) uses Ask-LLM to score samples for "reasoning relevance." The paper does not specify which LLM is used for this scoring. If the Ask-LLM model shares training data or inductive biases with MobileLLM-R1's training pipeline, the filtering could preferentially select samples aligned with the scoring model's distribution rather than universally informative samples. This is particularly relevant because the same data sources (e.g., FineWeb-Edu, StarCoder) may appear in both the scoring model's training and the probing dataset.

**Recommended fix:** (1) Disclose the specific LLM used for Ask-LLM scoring. (2) Add a small ablation comparing Ask-LLM-filtered vs. randomly-sampled capability-probing datasets. (3) Test whether results hold with different scoring models.

### W7. Related work lacks structured comparison (Severity: Moderate)

Section 5 is a brief chronological listing of model families without organizing them around decision-relevant axes. The paper's core contribution is a data curation framework, yet the related work does not discuss prior work on data selection, data mixing, or curriculum learning for LLM pretraining (e.g., DoReMi, DITTO, data influence methods). This makes it difficult for readers to assess what is genuinely novel versus incremental. The section reads more as a citation checklist than as a critical positioning of the contribution.

**Recommended fix:** Restructure around 3-4 comparison axes: (a) data-efficient pretraining methods, (b) reasoning elicitation in small models, (c) open-source training recipes. For each axis, identify what prior work achieves, what limitation remains, and how this paper addresses it.

```text
ASCII Diagram — Revision Strategy Roadmap

Priority | Issue | Fix Required | Expected Gain
---------|-------|-------------|--------------
P0 | W1: No statistical variance | Add multi-seed reports + significance tests | Core scientific validity
P0 | W5: Overclaiming | Tighten Qwen comparison + SOTA wording | Scientific credibility
P1 | W2: Influence approximation gap | Self-contained description + ablation | Reproducibility 
P1 | W4: Confounded comparison | Add base-checkpoint control in Table 2 | Claim-evidence alignment
P1 | W3: Selection bias in mid-training | Add re-introduction experiment + explain dip | Methodological soundness
P2 | W6: Ask-LLM bias | Disclose model + add ablation | Robustness
P2 | W7: Related work depth | Restructure by comparison axes | Reader positioning
```

## Score
**Final Score: 6/10**

**Rationale:** The paper addresses a timely and practically important problem (token-efficient training of small reasoning models) and provides a fully open-source recipe that demonstrates clear improvements over prior open baselines. The methodological ideas — influence-based cross-capability data mixing and iterative mid-training compression — are creative and well-motivated. However, the core contribution is weakened by: (a) absence of any statistical variance or significance testing, which undermines the reliability of all reported results; (b) incomplete specification of the influence approximation method, creating a reproducibility gap; (c) potential confounds in the key comparisons that are not adequately controlled or disclosed; and (d) rhetorical overclaiming in the positioning against Qwen3-0.6B and in SOTA assertions. The paper's value as an open-source recipe and empirical benchmark is clear, but the scientific validation of the proposed methods requires substantial strengthening. The six P0/P1 issues identified above should be addressed before publication.

**Note:** External literature verification was unavailable in this run (Retrieval-Disabled Mode). Novelty and comparison conclusions are therefore based on internal manuscript evidence and should be verified with targeted literature review before final acceptance decisions.