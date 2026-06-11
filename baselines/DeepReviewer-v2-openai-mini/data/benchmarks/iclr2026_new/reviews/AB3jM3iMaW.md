## Summary
# Final Review Report

## Summary

This paper proposes **ReaL-TG** (Reasoning-Enhanced Learning for Temporal Graphs), a reinforcement learning framework that fine-tunes large language models (LLMs) for explainable link forecasting on real-world temporal graphs. The core idea is to use Grouped Regularized Policy Optimization (GRPO) with an outcome-based F1 reward, allowing the LLM to self-explore reasoning strategies without process-level supervision. The framework includes a Temporal Context Graph Selection (T-CGS) algorithm to extract relevant subgraphs, which are verbalized as text prompts for the LLM. For evaluation, the authors introduce a penalized MRR (pMRR) metric to penalize over-generation and an LLM-as-a-Judge system assessing faithfulness, logical consistency, and answer-explanation alignment of reasoning traces. The fine-tuned ReaL-TG-4B (based on Qwen3-4B) is evaluated on 6 TGB datasets (4 seen, 2 unseen), where it outperforms frontier LLMs including GPT-5 mini and Llama3.3-70B on ranking metrics while providing human-validated reasoning traces. The paper addresses important limitations of existing TG link forecasting methods—lack of explainability and inability to generalize to unseen graphs—and makes contributions in methodology (RL-based LLM fine-tuning for TGs), evaluation protocol (pMRR + LLM Judge), and empirical demonstration that a 4B model can surpass much larger models through targeted RL fine-tuning.

**Novelty assessment (deferred — Retrieval-Disabled Mode):** The scoped first claim ("first RL-based framework for LLM-based TG link forecasting") appears plausible given the paper's thorough related-work survey, but external literature verification is unavailable in this run. The evaluation protocol (pMRR + LLM Judge) is a genuinely useful contribution independent of the method.

## Strengths
**1. Novel problem formulation and framework design.** The paper identifies a genuine gap in TG link forecasting—the lack of explainability and zero-shot generalization in traditional neural methods—and proposes a well-motivated RL-based LLM fine-tuning framework to address both issues simultaneously. Using GRPO with an outcome-based F1 reward (rather than process-level supervision) is an elegant design choice that allows the model to self-explore reasoning strategies without requiring expensive human-annotated reasoning chains. The T-CGS algorithm for context graph selection, while having notation issues (see Weaknesses), is conceptually sound: extracting temporally relevant subgraphs before verbalization makes the LLM's input manageable and focuses reasoning on the most informative interactions.

**2. Comprehensive evaluation protocol.** The paper makes a strong secondary contribution by proposing an evaluation protocol specifically tailored to LLM-based TG link forecasting. The pMRR metric correctly identifies a failure mode unique to generative LLM forecasting (over-generation) that standard MRR misses. The LLM-as-a-Judge system with three explicit criteria (faithfulness, logical consistency, answer-explanation alignment) provides a systematic framework for assessing reasoning quality—an aspect entirely overlooked in prior TG-LLM work. The inclusion of human evaluation (50 samples, 5 annotators) to validate both the Judge system and the reasoning traces adds credibility to the evaluation methodology.

**3. Impressive empirical results.** ReaL-TG-4B (4B parameters) outperforms much larger models including GPT-5 mini and Llama3.3-70B on combined MRR (0.552 vs. 0.521 and 0.456) and pMRR (0.508 vs. 0.423 and 0.351) across 6 TGB datasets. The gains are particularly striking on unseen graphs (uci: 0.607 MRR, enron: 0.492 MRR), demonstrating genuine zero-shot transfer capability. The reasoning quality metrics (\(\delta_f=0.885, \delta_c=0.880\)) are competitive with those of Llama3.3-70B, confirming that RL fine-tuning can improve both accuracy and explainability simultaneously.

**4. Transparent limitation awareness.** The paper honestly discusses reward hacking (ReaL-TG-0.6B case), family bias in LLM judging, and dataset-specific weaknesses (e.g., poor performance on tgbl-flight). The ethics statement appropriately cautions against over-reliance on LLM outputs in safety-critical applications. This transparency enhances trust in the results.

**5. Strong reproducibility practices.** The authors provide source code, curated QA datasets, and detailed setup instructions (README.md). The evaluation filtering procedure is consistently applied across all models. The inclusion of confidence information (annotation variances in human evaluation) and explicit timeout handling for TGNN baselines demonstrates methodological diligence.

## Weaknesses
### W1. T-CGS Transition Probability Formula is Ill-Defined (Major)

**Location:** Page 1 - Temporal Context Graph Selection paragraph; also Page 3-4 (formula area)

The transition probability for the α-temporal random walk is given as:

$P_{(e, t)}(e', t') = \beta \{[(e', t'') \mid (e'', t'') \in \text{Nei}(e, t), t'' \geq t'] / \sum_{z=1}^{|\text{Nei}(e, t)|} \beta^z\}$

This formula has three technical problems:
- **Notation ambiguity:** The numerator uses a set comprehension $\{[(e', t'') \mid (e'', t'') \in \text{Nei}(e, t), t'' \geq t']\}$ where it is unclear whether the intent is to count neighbors with timestamp $\geq t'$ or to produce a weight vector. The variable $(e', t'')$ appears without being bound to the target node $(e', t')$ being evaluated.
- **Denominator mismatch:** The example calculations use $\beta + \beta^2$ in the denominator, suggesting $z$ indexes hop order, but the formula defines $z$ as ranging over $|\text{Nei}(e, t)|$ (the number of neighbors). The rank-based decay intuition does not match the index-based summation.
- **Missing rank mapping:** There is no explicit mapping between temporal proximity and the exponent $z$, making the algorithm irreproducible from the main text.

**Impact:** A reader implementing T-CGS from the paper text must guess the intended formula. This reproducibility gap is significant because T-CGS is the core mechanism connecting raw graph data to LLM input.

**Recommended fix:** Replace the formula with a clear softmax over neighbor ranks. A corrected version is provided in the annotation on this paragraph. This is a **Must** revision.

### W2. Evaluation Data Filtering Creates Selection Bias (Major)

**Location:** Page 1 - Training Data Collection paragraph; also Experimental Setup

The paper filters out queries where (i) T-CGS does not contain all ground-truth answers or (ii) the context graph exceeds 600 links. This filtering is applied to both training and evaluation data. While practical, it introduces systematic selection bias: the evaluation only measures performance on queries where T-CGS already succeeds at retrieving all relevant nodes. In real deployment, T-CGS has no such guarantee, and the hardest prediction failures likely occur precisely when the retrieved context is incomplete.

**Impact:** The reported MRR/pMRR numbers (0.552/0.508 overall) likely overestimate real-world performance. The paper does not report the filtering rate per dataset, nor does it measure performance on the excluded queries using a fallback strategy. Without this information, readers cannot gauge the true reliability of the approach.

**Recommended fix (Must):**
1. Report the percentage of queries filtered per dataset (separately for training and evaluation).
2. Conduct a sensitivity analysis: report MRR/pMRR on the full (unfiltered) query set using a fallback (e.g., empty prediction or graph-agnostic baseline).
3. Add a limitations paragraph discussing this issue.

### W3. TGNN Comparison is Incomplete and Asymmetric (Major)

**Location:** Page 7-8 - Table 4 and surrounding text

The comparison with traditional TG link forecasting methods has four fairness issues:
- **Datasets with timeout (coin, flight):** Three of four TGN baselines time out after 24 hours on coin and flight, which are precisely the datasets where ReaL-TG-4B shows its largest gains. The comparison is incomplete on 2/6 datasets.
- **Asymmetric training paradigm:** ReaL-TG-4B is RL-fine-tuned on seen datasets and evaluated zero-shot on unseen ones. TGNs are trained per-dataset from scratch. The framing "outperforms strong traditional methods" conflates two different evaluation scenarios.
- **pMRR incompatibility:** TGNs cannot be evaluated with pMRR, so the paper's proposed metric does not apply to the main baseline family.
- **Weak EdgeBank baseline:** Beating a non-learned heuristic does not constitute strong evidence.

**Impact:** The claim "our fine-tuned model outperforms strong traditional methods" is overstated given incomplete data and incompatible evaluation frameworks.

**Recommended fix (Must):**
1. Report results for TGNs on coin/flight using a sampling-based ranking approach within the 24-hour budget.
2. Explicitly distinguish the zero-shot vs. per-dataset-training comparison in the narrative.
3. Consider adding a precision/recall metric applicable to both paradigms.

### W4. LLM-as-a-Judge System Has Circularity and Bias Risks (Major)

**Location:** Page 6 - Reasoning Trace Evaluation; Page 8 - Table 3 and human evaluation

Using GPT-4.1 mini as the Judge for all models creates two risks:
- **Family bias acknowledged but not controlled:** GPT-5 mini is excluded from reasoning evaluation due to potential family bias from GPT-4.1 mini. However, the same bias could systematically affect scores for non-OpenAI models (Gemma 3, Llama) vs. Qwen3-based ReaL-TG.
- **Atomic claim decomposition reliability:** The faithfulness score depends on the Judge correctly splitting reasoning into atomic claims and verifying each against the context graph. The paper does not evaluate the reliability of this decomposition step (no inter-annotator agreement between different Judges).
- **Only 50 human validation samples:** The human evaluation validates absolute score quality but has limited statistical power to detect model-level bias.

**Impact:** The reasoning quality rankings in Table 3 may reflect Judge preferences rather than genuine differences in TG reasoning capability.

**Recommended fix (Must):**
1. Add agreement analysis between GPT-4.1 mini and a second Judge (e.g., Gemini 2.5 Pro or Llama-based) on ≥100 examples, reporting Cohen's kappa per criterion.
2. If family bias is detected, use an ensemble of Judges from different model families.
3. Expand the human evaluation sample size justification.

### W5. Conclusion Overclaims "Low-Cost Prediction" Without Evidence (Major)

**Location:** Page 8 - Real-TG-4B vs. Traditional Methods paragraph; Page 9 - Conclusion

The paper states "our framework enables low-cost prediction in real-world applications" and "eliminates the need to train a model from scratch for new TGs." Neither claim is experimentally supported:
- Inference cost (latency, FLOPs, tokens per query, GPU memory) is not reported for ReaL-TG-4B or any baseline.
- A 4B-parameter LLM processing prompts with up to 600 verbalized links is unlikely to be "low-cost" compared to traditional TGNNs.
- The paper only evaluates on 2 unseen datasets; claiming "eliminates" retraining overstates the evidence from a single fine-tuning run.

**Impact:** These unsupported claims could mislead practitioners about deployment feasibility.

**Recommended fix (Must):** Remove or qualify both claims. Report inference cost measurements (average tokens per query, latency, GPU hours) for ReaL-TG-4B and compare with TGNN inference costs.

### W6. Reward Hacking Analysis is Under-Explored (Minor)

**Location:** Page 8 - Influence of Base Model Size

The paper identifies reward hacking for ReaL-TG-0.6B (predicting "already seen" links) but does not analyze whether ReaL-TG-4B exhibits subtler forms of reward hacking. The reasoning quality scores (\(\delta_f=0.885\), \(\delta_a=0.732\)) leave room for improvement, but their root causes are not diagnosed.

**Recommended fix (Nice-to-have):** Add a systematic analysis of failure modes for both models, and discuss whether the GRPO KL penalty is sufficient to prevent reward hacking.

### W7. Introduction Narrative Density (Minor)

**Location:** Page 1 - Introduction paragraph 3

The third introduction paragraph tries to present the entire method framework, evaluation protocol, and metrics in a single dense block. The reader cannot easily separate the method contribution from the evaluation contribution. This reduces narrative impact.

**Recommended fix (Nice-to-have):** Split into two paragraphs: (A) method framework with intuitive explanation of why outcome-based RL enables self-exploration; (B) evaluation protocol as a separate contribution.

### W8. pMRR Metric Arbitrary Penalty Constant (Minor)

**Location:** Page 6 - Prediction Label Evaluation

The pMRR penalty constant (1.1, or "any number > 1") is chosen arbitrarily. The paper does not analyze how the choice affects rankings across datasets with different node set sizes (e.g., enron: 296 nodes vs. coin: 9,194 nodes). For large node sets, a fixed constant of 1.1 may have negligible effect.

**Recommended fix (Nice-to-have):** Add sensitivity analysis varying the penalty constant or replace with a principled penalty (e.g., rank false positives at position N+1).

---

**ASCII Diagram — Paper Structure & Evidence Map**
```text
[Problem: TG link forecasting lacks explainability & zero-shot generalization]
    |
    v
[Method: ReaL-TG (RL fine-tuning of LLMs with GRPO + F1 reward)]
    |-- T-CGS: temporal subgraph extraction (formula needs fix)
    |-- Prompt verbalization of graph context
    |-- RL: GRPO with outcome-based reward
    |-- Output: <think>reasoning</think><answer>predictions</answer>
    |
    v
[Evaluation Protocol]
    |-- pMRR (penalized MRR for over-generation)
    |-- LLM-as-a-Judge (faithfulness, consistency, alignment)
    |
    v
[Experiments]
    |-- Seen datasets (wiki, subreddit, coin, flight)
    |-- Unseen datasets (uci, enron) -> Zero-shot transfer shown
    |-- vs. Frontier LLMs (GPT-5 mini, Llama3.3-70B)
    |-- vs. Traditional TGNNs (incomplete comparison due to timeout)
    |
    v
[Key Gaps/Risks]
    |-- W1: T-CGS formula ill-defined (reproducibility risk)
    |-- W2: Evaluation filtering bias (overestimation risk)
    |-- W3: TGNN comparison incomplete and asymmetric
    |-- W4: Judge bias and circularity
    |-- W5: Unsupported "low-cost" claim
```

---

**ASCII Diagram — Revision Strategy Roadmap**
```text
Priority     | Issue                    | Fix                                  | Expected Impact
-------------|--------------------------|--------------------------------------|-----------------
P0 (Must)    | W1 (T-CGS formula)      | Rewrite transition probability       | Reproducibility restored
P0 (Must)    | W2 (Evaluation bias)    | Add filtering rates + sensitivity    | Honest performance bounds
P0 (Must)    | W3 (TGNN comparison)    | Complete comparison + clarify setup  | Fair empirical positioning
P0 (Must)    | W4 (Judge bias)         | Add agreement analysis + 2nd Judge  | Reliable reasoning metrics
P0 (Must)    | W5 (Low-cost overclaim) | Report cost metrics + qualify claims | Honest deployment framing
P1 (Nice)    | W6 (Reward hacking)     | Systematic failure mode analysis     | Deeper understanding of RL behavior
P1 (Nice)    | W7 (Intro density)      | Split into two paragraphs            | Improved readability
P2 (Nice)    | W8 (pMRR constant)      | Sensitivity analysis                 | Metric robustness confirmed
```

---

**ASCII Diagram — Related-Work Taxonomy Tree (Layered)**
```text
TG Link Forecasting (Root)
├── Branch 1: Traditional Neural Methods
│   ├── Leaf 1.1: Memory-based (TGN, TCNN, JODIE)
│   ├── Leaf 1.2: Sequence models (TCL, DyGFormer, DyGMamba)
│   ├── Leaf 1.3: Heuristic/MLP (EdgeBank, GraphMixer, Base 3)
│   └── Leaf 1.4: Snapshot-based (ROLAND, UTG)
│   └── Common limitation: No explainability, no zero-shot transfer
│
├── Branch 2: LLMs for Static Graph Reasoning
│   ├── Leaf 2.1: Prompt-based (Fatemi et al. 2024)
│   ├── Leaf 2.2: Joint LLM-Graph training (GraphToken, GraphLLM, LLaGA)
│   └── Leaf 2.3: RL-enhanced (Guo et al. 2025 — GI)
│   └── Gap: Not designed for temporal dynamics
│
├── Branch 3: LLMs for Temporal Graph Reasoning
│   ├── Leaf 3.1: Text-attributed TGs (Lee, Liao, Wang, Wu — leakage risk)
│   ├── Leaf 3.2: Synthetic TGs (LLM4DyG — up to 20 nodes)
│   ├── Leaf 3.3: ICL-based (Li et al. 2025, TGTalker)
│   └── Leaf 3.4: THIS PAPER — ReaL-TG (RL fine-tuning, real-world TGs)
│   └── Novelty: First RL-based LLM fine-tuning for TG link forecasting
│   └── Value: Explainability + zero-shot transfer without leakage
│
└── Novelty Verdict (deferred — external retrieval unavailable)
    └── Provisional: partially_overlapping (TGTalker, GI share partial goals)
    └── Need manual verification against TGTalker (ICL-based) and GI (RL for static graphs)
```

**Page Coverage Audit**

| Page | Annotation Count | Coverage Status | Skip Reason |
|------|-----------------|-----------------|-------------|
| 1 (Abstract) | 1 | Covered | — |
| 1 (Introduction P1) | 1 | Covered | — |
| 1 (Introduction P2) | 1 | Covered | — |
| 1 (Introduction P3 + Contributions) | 2 | Covered | — |
| 1 (Related Work: Traditional) | 1 | Covered | — |
| 1 (Related Work: LLMs) | 0 | Skipped | Non-substantive: properly covers prior work, no major defect found beyond list-style issue already addressed |
| 1 (Preliminaries) | 0 | Skipped | Definitions are clear and standard; no substantive defect |
| 1 (Method: T-CGS) | 1 | Covered | Formula error annotated |
| 1 (Method: Prompt + Training Data) | 1 | Covered | Selection bias annotated |
| 1 (Method: Fine-tuning RL) | 0 | Skipped | GRPO formula is standard (from Shao et al.); no unique defect in this paragraph beyond what GRPO inherits |
| 1 (Evaluation: pMRR) | 1 | Covered | — |
| 1 (Evaluation: Reasoning Trace) | 1 | Covered | Judge bias annotated |
| 1 (Experimental Setup) | 0 | Skipped | Setup is standard; relevant concerns captured in data filtering annotation |
| 1 (Table 2 results) | 0 | Skipped | Table-text consistent; narrative is clear |
| 1 (Table 3 reasoning quality) | 0 | Skipped | Table-text consistent |
| 1 (Table 4 TGNN comparison) | 1 | Covered | Major comparison fairness issue |
| 1 (Base model size + reward hacking) | 1 | Covered | Under-explored analysis |
| 1 (Human evaluation x2) | 0 | Skipped | Supporting evidence; properly reported with variances |
| 1 (Conclusion) | 1 | Covered | Overclaim annotation |
| 1 (Ethics/Reproducibility) | 0 | Skipped | Standard boilerplate, no substantive defect |

**Coverage Summary:** 13 annotations across ~15 substantive paragraph groups. Main gaps: related work (LLMs for graphs), fine-tuning RL details, and experimental setup paragraphs were not annotated individually because their defects are either absent or already addressed in cross-referencing annotations. The annotations adequately cover the core claims and major issues.

## Score
**Final Score: 6.5/10**

**Scoring rationale:**

The paper presents a novel and well-motivated framework (ReaL-TG) that addresses a genuine gap in TG link forecasting—the lack of explainability and zero-shot generalization. The empirical results are impressive for a 4B model, and the proposed evaluation protocol (pMRR + LLM-as-a-Judge) is a meaningful methodological contribution that extends beyond this specific method.

However, the score is constrained by four major weaknesses that require substantial revision:

1. **Reproducibility risk (W1):** The T-CGS transition probability formula contains notation errors that prevent faithful re-implementation from the main text. This is fixable but currently a barrier.
2. **Evaluation overestimation (W2):** The query filtering procedure removes cases where T-CGS fails, creating a selection bias that likely inflates reported performance. The magnitude of this bias is unquantified.
3. **Incomplete traditional baseline comparison (W3):** 2 of 6 datasets time out for TGN methods, and the comparison paradigm (zero-shot vs. per-dataset training) is asymmetric. The strong claims about outperforming traditional methods are not fully supported.
4. **Judge bias and overclaims (W4, W5):** The LLM-as-a-Judge evaluation has unresolved reliability concerns, and the conclusion makes unsupported claims about "low-cost" deployment.

All four major weaknesses are fixable with reasonable effort (clarifying formulas, adding sensitivity analyses, completing comparisons, and toning down claims). The core technical contribution—using RL fine-tuning to make LLMs self-explore effective reasoning strategies for temporal graph forecasting—remains valid and interesting.

**Novelty note (deferred):** The paper claims to be the "first RL-based framework for LLM-based TG link forecasting." Due to Retrieval-Disabled Mode, external literature verification is unavailable. The scoped qualifiers ("RL-based," "real-world TGs," "LLM fine-tuning") make the claim plausibly narrow, but authors should verify against concurrent works (TGTalker, GI, ICL-based approaches) before asserting "first" in the final version.

**Revision expectations:** With completion of P0 fixes (W1-W5), the paper could reach 7.5-8.0/10. The core idea is sound, the experiments are largely well-conducted, and the contributions are clearly scoped. The main lift required is in honesty of presentation (completing comparisons, quantifying limitations, qualifying claims) rather than in redesigning the method.