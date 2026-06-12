## Summary

The paper proposes *Forget-to-Focus (F2F)*, a two-stage protocol for domain specialization of LLMs: first, perform targeted unlearning on a “forget set” of general-domain data (with an optional “retain set” from the target domain for stability), then fine-tune on the domain-specific dataset. Experiments across coding, mathematics, and medical domains, using models ranging from 0.6B to 72B parameters, report consistent improvements over standard fine-tuning, DAPT, and LoRA baselines. The paper also analyzes representational drift via CKA and SVCCA to argue that unlearning reshapes internal geometry toward structures more conducive to specialization.

## Strengths

- **Broad experimental scope**: The evaluation spans three challenging domains (coding, math, medical), five model families and scales (0.6B to 72B), and multiple unlearning and fine-tuning variants, providing a thorough empirical investigation.
- **Interesting conceptual framing**: Repurposing machine unlearning—traditionally a privacy tool—as a preparatory step for domain adaptation is a creative and potentially valuable direction if validated rigorously.
- **Representational analysis**: The use of CKA and SVCCA to characterize representational changes after unlearning and fine-tuning adds a useful mechanistic perspective beyond raw performance metrics.

## Weaknesses

### Fatal

- **Confounded comparison due to retain set leakage**: The unlearning phase uses a retain set that is explicitly a subset of the domain-specific fine-tuning data (e.g., 1000 samples from PubMedQA for medical tasks). This means that during the “unlearning” stage, the model already receives supervised training on domain data (via gradient descent) that is completely absent from the standard fine-tuning baselines. Consequently, the observed performance gains may arise from this additional domain training rather than from the intended removal of interfering general knowledge. The paper lacks any control experiment (e.g., standard fine-tuning that also includes those same retain samples, or comparison with a protocol that only trains on the retain set before fine-tuning). Without such a control, the core claim that *unlearning* is the source of improvement is unsubstantiated.

### Major

- **Unsubstantiated calibration claim**: The abstract and introduction claim that F2F “improves calibration on medical QA tasks, reducing overconfidence,” but no calibration results (e.g., expected calibration error, reliability diagrams) are presented in the main paper or the available content. This claim is not supported by evidence.
- **Limited novelty claim**: The paper states it is the “first comprehensive study of machine unlearning … to enhance fine-tuning,” yet it does not discuss or compare with prior works that use forgetting mechanisms for domain adaptation (e.g., active forgetting during pretraining, gradient-based removal of interfering features). Overclaiming novelty without adequate literature engagement weakens the positioning.

### Minor

- **Theoretical analysis overly simplistic**: The linear model proposition and corollary assume an oracle decomposition of parameters into “relevant” and “irrelevant” subspaces and rely on strong convexity, which does not hold for deep neural networks. While the analysis provides intuition, it does not convincingly transfer to the practical setting.
- **Forget set construction details**: The forget sets (BC-Select, BC-Mixed, BC-Cosine) are small (100–1000 samples) and drawn from BookCorpus, which is not the pretraining distribution of the evaluated models. The effect of unlearning on such a small and non-representative set is unclear; the paper does not justify why BookCorpus is an appropriate proxy for interfering general knowledge.

### Trivial

- Some inconsistency in model naming: “Qwen-2 72B-Instruct” in the model list versus “Qwen 72B” in tables and “Qwen 3 0.6B” elsewhere.

## Nice-to-Haves

- A controlled baseline that includes the retain set in standard fine-tuning (e.g., first train on retain set then finetune on full domain data) would directly address the confound.
- Calibration metrics (ECE, reliability diagrams) for the medical QA experiments should be reported if the claim is to be made.
- Ablation on the size and source of the forget set using data from the actual pretraining corpus (if identifiable) would strengthen the relevance of the unlearning step.

## Novel Insights

None beyond the paper’s own contributions. The idea of using unlearning for domain specialization is interesting, but the core empirical evidence is undermined by the confound described above, and the mechanistic insights (CKA/SVCCA shifts) are correlational rather than causal.

## Suggestions

- **Run a control experiment** where standard fine-tuning is performed on a dataset that includes the same retain samples used in F2F’s unlearning phase. If F2F still outperforms this control, the unlearning component is credibly beneficial.
- **Remove or substantiate the calibration claim** by including calibration errors and reliability plots for medical QA tasks.
- **Tone down the “first” claim** and compare with more closely related work (e.g., Chen et al. 2023a, any work that uses forgetting for downstream adaptation).
- **Report statistical significance** or variability across multiple runs to ensure the improvements are robust.

## Score and Decision

The paper presents an interesting and timely research direction, but the fatal confound between unlearning and additional domain data exposure invalidates the central empirical finding. The reported gains cannot be confidently attributed to the proposed forgetting mechanism. Without a proper control, the core claim is unsupported.

MY FINAL SCORE: <score>2</score>
MY FINAL DECISION: <decision>Reject</decision>