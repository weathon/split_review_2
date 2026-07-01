Now let me verify specific claims against the paper content. Let me read the critical sections more carefully.Now I have a thorough understanding of the paper. Let me draft the review and then submit it for calibration.Now let me do calibration. Round 1 — Bracketing:Let me read the most relevant anchor papers to calibrate properly.Now let me do Round 2 calibration to narrow the bracket. Based on my analysis:

- The paper is clearly above strong-reject (1.0) territory — it has real experiments and a real question.
- It appears to sit below the 4.25 anchors (Nk1MegaPuG, rAylWUIKtu) because its evidence actively contradicts its claims, has missing controls, and the TACD is unimplemented.
- It's above 1.0 papers which are non-contributions.

**Initial bracket: 3.0–4.5**Now I have enough calibration data. Let me finalize the review.

**Round 1 bracket: 3.0–4.5**

Key comparisons:
- The paper is weaker than Nk1MegaPuG (4.25, "Evading Data Contamination Detection") — that paper at least proposed an implemented technique (EAL), whereas this paper's TACD is unimplemented and the evidence is self-contradictory.
- The paper is weaker than rAylWUIKtu (4.25, "Benchmark Inflation") — that paper at least demonstrated consistent results within its narrow scope.
- The paper is comparable to JL42j1BL5h (3.50, "All Languages Matter: Multilingual Safety") and fSbPwHjdDG (3.00, "Llamas think in English") — multilingual LLM studies rejected for methodological gaps and insufficient evidence.
- The paper is clearly above the 1.0 strong-reject papers (pure surveys, non-contributions).

**Round 2 narrowing: 3.0–3.5**

The internal contradiction (Section 4.2 claims vs Table 2 data) and missing critical controls push it to the lower end.

---

## Summary
This paper investigates whether translating English benchmarks (MMLU, XQuAD, MLQA) into Arabic can mask data contamination in LLM evaluation. The authors fine-tune four open-weight models on English data plus varying proportions (0–100%) of Arabic-translated benchmark content, evaluate on the original English benchmarks, and apply TS-Guessing (with a novel choice-reordering extension) as a contamination probe. They also propose an unimplemented Translation-Aware Contamination Detection (TACD) framework.

## Strengths
- **Choice-reordering extension to TS-Guessing is a concrete methodological contribution (Section 3.3, Figure 1):** By shuffling answer choices and checking whether the model recalls pre-shuffle indices, this provides a contamination signal harder to confound with genuine reasoning. The Index-Recall Rate (IDR) metric is well-defined (Section 3.4: `IdxRec = 1/N Σ 1{ℓ̂_i = ℓ_i^{pre-shuffle}}`).
- **Consistent MMLU finding across all four models (Table 2):** MMLU exhibits monotonic performance increases with contamination for all four models (Mistral: 0.577→0.690, Gemma: 0.220→0.284, LLaMA: 0.332→0.431, Qwen: 0.553→0.581). This is the paper's most robust empirical finding and provides genuine evidence that cross-lingual contamination can inflate closed-book MCQ accuracy.
- **Breadth of experimental coverage:** Four models (LLaMA, Mistral, Gemma, Qwen) across three benchmarks and four contamination proportions allow cross-model comparison rather than relying on a single setup.

## Weaknesses

### Fatal
None

### Major

- **Ambiguous baseline contamination undermines all conditions (Section 3.1)** — The training data is defined as $\mathcal{D}_{\text{train}}^d(p) = \mathcal{D}_{\text{EN}}^d \cup \mathcal{D}_{\text{AR}}^d(p)$, where $\mathcal{D}_{\text{EN}}^d$ for MMLU is described as "English test items formatted as MCQ" (line 132). This implies the English *test set* is included in training at ALL contamination levels, including p=0. If so, every condition is already fully contaminated in English, and the experiment measures only the marginal effect of adding Arabic translations to an already-contaminated model — a fundamentally different experiment from one starting with a clean baseline. The paper never clarifies this, making all results ambiguous to interpret. The same ambiguity applies to XQuAD/MLQA ("English QA" — train or test split?).

- **Paper's central interpretive claim is directly contradicted by its own data (Section 4.2 vs. Table 2)** — Section 4.2 states: "the models exhibit approximately equal performance on all evaluated benchmarks" and "The consolidated results in Tables 2 and 3a show that scores remain broadly stable as p increases." But Table 2 shows: Mistral MMLU jumps from 0.580 to 0.690 (+11 points from 10%→50%); Mistral XQuAD collapses from 0.455 to 0.114 (−34 points); Qwen MLQA spikes from 0.162 to 0.409 then crashes to 0.153. These dramatic swings are not "broadly stable." The paper's core masking claim rests on a mischaracterization of its own evidence.

- **Missing critical control condition undermines causal attribution** — No condition fine-tunes models on non-benchmark Arabic text (e.g., Arabic Wikipedia, Arabic translations of non-overlapping QA pairs). Without this control, performance changes from adding Arabic data could result from general multilingual fine-tuning effects (improved cross-lingual transfer, regularization) rather than contamination specifically. This makes it impossible to isolate contamination as the causal factor, which is the paper's central empirical claim.

- **TS-Guessing contamination probe yields incoherent results (Table 3)** — The contamination detection results are inconsistent and sometimes anti-correlated with contamination level. Gemma IDR *decreases* from 0.350 to 0.005 as contamination *increases* — the opposite of memorization. LLaMA IDR peaks at 50% (0.643) and drops at 100% (0.410). XQuAD EM values are near-zero across all models (0.000–0.103). These patterns do not tell a coherent contamination story. The paper interprets the flatness as evidence of "masking" but does not consider the alternative that the probe simply lacks sensitivity in the cross-lingual setting.

### Minor

- **Post-hoc narrative shifting across models (Section 4.1)** — Each model's behavior receives a bespoke explanation. When MMLU rises, it's "contamination-driven memorization." When Mistral XQuAD collapses, it's "memorization that helps option selection while harming calibration and span localization." When Qwen MLQA is non-monotonic, it's "dataset-specific leakage or language/domain mismatch." The paper would be more convincing with pre-specified hypotheses tested consistently.

- **TACD framework is overclaimed (Section 5 vs. Abstract)** — The abstract states "we propose a Translation-Aware Contamination Detection framework," but Section 5 is ~1 page of bullet points with no implementation, evaluation, or comparison. The paper itself acknowledges it is "a forward-looking blueprint rather than a complete implementation" (Section 5.3). Presenting this as a contribution is misleading.

- **No same-language contamination baseline for TS-Guessing** — The paper claims translation masks contamination signals but never shows what those signals look like when they *should* be present (i.e., English-only contamination at varying proportions). Without this positive control, the flat TS-Guessing results cannot be distinguished from probe insensitivity.

- **No statistical testing or variance reporting** — All results are single-run point estimates. Given small absolute differences (e.g., Qwen MMLU: 0.553→0.581, a 2.8-point change) and known LoRA fine-tuning instability across seeds, it is unclear which observed differences are meaningful vs. noise.

### Trivial
None

## Nice-to-Haves
- Focus analysis primarily on MMLU where results are cleanest and consistent, treating XQuAD/MLQA as supplementary exploration.
- Run TS-Guessing on English-only contaminated models at varying proportions as a positive control to establish what "detected contamination" looks like.
- Describe the Arabic translation process (machine vs. human, system used, quality controls), as translation quality directly affects the central claim.
- Trim the literature review (~4 pages of 9) to allocate more space to experimental analysis and controls.

## Removed Points
*These points are flagged to be removed; treat them with caution:*

- **"Embedding figure" reference in Section 4.3:** The reviewer noted that Section 4.3 references "the embedding figure" with no figure in the main text. This likely refers to an appendix figure stripped by the parser. Removed per rules about appendix content.
- **Circularity of cosine similarity argument (Section 4.3):** The reviewer argued the embedding similarity discussion is circular. While somewhat valid, this is a minor interpretive point in the discussion section, not a core claim; merged into the broader evidence-quality concerns above.
- **Reproducibility details (LoRA rank, learning rate, epochs):** These are deferred to Appendix A (line 264: "All hyperparameters... are enumerated in Appendix A"). Removed per rules about hyperparameter details in appendix.
- **Literature review length:** ~4 pages of survey-style review in a 9-page paper. This is a presentation/style concern rather than a substantive weakness. Moved to nice-to-have.

## Novel Insights
None beyond the paper's own contributions. The consistent MMLU finding (monotonic gains from cross-lingual contamination across all four models) is the most interesting empirical observation, but the paper does not develop it into a convincing contribution due to missing controls and ambiguous baselines.

## Suggestions
- **Clarify whether $\mathcal{D}_{\text{EN}}^d$ contains the test split or a separate training split** — this single clarification would fundamentally change how all results are interpreted.
- **Add a non-benchmark Arabic fine-tuning control** to isolate contamination-specific effects from general multilingual fine-tuning effects.
- **Include a same-language (English) contamination baseline for TS-Guessing** to calibrate the cross-lingual probe against known-positive contamination.
- **Run multiple seeds per condition** and report standard deviations to distinguish meaningful changes from noise.
- **Reconcile Section 4.2's claims with Table 2's data** — either revise the claims to match the evidence or explain why the large swings are consistent with the masking interpretation.
- **Narrow scope to MMLU** as the primary finding, treating XQuAD/MLQA as exploratory, which would produce a tighter and more convincing paper.

## Score and Decision

### Calibration Anchors

| Paper | Path | Avg Score | Round | Comparison |
|-------|------|-----------|-------|------------|
| Systematic Review of LLMs | 8QTpYC4smR | 1.00 | R1 | Pure survey with no experiments; the paper under review is substantially stronger. |
| NEMESIS Jailbreaking | 5kMwiMnUip | 1.40 | R1 | Non-contribution; the paper under review has real experiments. |
| Cross-Lingual Humanoid Robots | gwZ90hFSL2 | 1.00 | R1 | Pseudoscience; irrelevant comparison except as floor. |
| Financial Markets Neural Network | nSDOkm0SKo | 1.00 | R1 | Hypothetical scenario with no real contribution; far below paper under review. |
| Language Models for Data Valuation | OdoS6cH8MP | 2.00 | R1 | Weak methodology; paper under review has more substance. |
| Traffic Incident Benchmarking | JQbqaQjV7D | 3.00 | R1 | Small test set, unsupported claims, narrow scope — similar issues to paper under review. |
| Instruction Following Evaluation | RuY1r1PDdQ | 3.00 | R1 | Benchmark paper with under-explored analysis; comparable quality issues. |
| DataSciBench | BltaWJZMeR | 3.20 | R1 | Broader benchmark paper but also rejected for methodological gaps. |
| Evading Data Contamination Detection | Nk1MegaPuG | 4.25 | R1 | Directly relevant; proposes an implemented attack (EAL), clearer evidence chain — stronger than paper under review. |
| Benchmark Inflation | rAylWUIKtu | 4.25 | R1 | Retro-holdout methodology with consistent results — stronger execution than paper under review. |
| Elephants Never Forget | lwtaEhDx9x | 4.75 | R1 | Multiple contamination tests with coherent results — clearly stronger. |
| Linguini benchmark | QiyQJqpcYe | 4.75 | R1 | Novel benchmark with clearer contribution — stronger. |
| To the Cutoff... and Beyond | m2NVG4Htxs | 6.75 | R1 | Rigorous longitudinal analysis with statistical evidence — much stronger. |
| How Much Can We Forget | Nsms7NeU2x | 6.75 | R1 | Theory + experiments on contamination forgetting — much stronger. |
| Detecting Pretraining Data | zWqr3MQuNs | 6.25 | R1 | Min-K% Prob method with dynamic benchmark — much stronger. |
| LiveBench | sKYHBTAxVa | 7.33 | R1 | Contamination-free benchmark design — far above paper under review. |
| Training on the Test Task | jOmk0uS1hl | 8.00 | R1 | Clear contribution, broad experiments — far above. |
| All Languages Matter | JL42j1BL5h | 3.50 | R2 | Multilingual safety benchmark across 14 issues/10 languages — more comprehensive execution but similar score range. |
| LLM-as-a-Judge | QhsbF2RZeu | 3.80 | R2 | Multilingual evaluation paper with broader analysis — slightly stronger. |
| Llamas Think in English | fSbPwHjdDG | 3.00 | R2 | Cross-lingual LLM study with causal interventions but criticized for imprecise analysis — comparable quality. |
| Luganda MT for Medical Domain | g7DHM6MRE4 | 3.50 | R2 | Narrow scope but cleaner execution — comparable. |
| Is Memorization Necessary | GbEmJmnQCz | 4.40 | R2 | Critiques prior work's methodology with cleaner evidence — stronger. |
| FreeLM | qgLyKwXVDs | 2.00 | R2 | Weak methodology and unclear contribution; paper under review is better. |
| Cross-lingual Information Retrieval | zkNCWtw2fd | 3.00 | R2 | Uses same benchmarks (XQuAD, MLQA), rejected for methodological issues — comparable. |

**Round 1 bracket:** 3.0–4.5
**Round 2 narrowing:** 3.0–3.5

The paper under review asks a genuinely interesting and novel question but fails in execution. The self-contradictory evidence (Section 4.2 claiming "broadly stable" scores when Table 2 shows swings of 11–34 points), the missing critical control condition, the ambiguous baseline design, and the incoherent TS-Guessing results collectively undermine all three of the paper's core claims. It is weaker than the 4.25-scoring contamination papers (Nk1MegaPuG, rAylWUIKtu) which at least delivered consistent evidence within their scope. It is comparable to the 3.0–3.5 multilingual LLM papers (fSbPwHjdDG, JL42j1BL5h, zkNCWtw2fd) that were rejected for insufficient evidence and methodological gaps.

**Final score: 3.0**

MY FINAL SCORE: <score>3.0</score>
MY FINAL DECISION: <decision>Reject</decision>