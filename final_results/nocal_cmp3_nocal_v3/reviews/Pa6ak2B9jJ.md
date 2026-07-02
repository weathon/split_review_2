Now let me produce the final review.

## Summary

AUTO-RT proposes a reinforcement learning framework for automated jailbreak strategy exploration in LLM red-teaming. The method introduces two technical contributions: Dynamic Strategy Pruning (DSP) to terminate redundant/inconsistent exploration branches early, and Progressive Reward Tracking (PRT) with a First Inverse Rate (FIR) metric that uses a sequence of downgraded target models to smooth sparse reward signals. Experiments across 16 white-box and 2 black-box LLMs show AUTO-RT consistently outperforms its ablations (FS, IL, RL) on ASR and achieves notably higher Defense Generalization Diversity (DeD) scores.

## Strengths

1. **Hierarchical strategy decomposition (AM^g + AM^r) is well-motivated and transparently evaluated.** Separating strategy generation from strategy rephrasing cleanly decouples *what* to attack from *how* to phrase it. The same two-model architecture is used across all baselines, ensuring the comparison isolates the learning algorithm rather than confounded by architecture differences (Section 2.2, Table 1).

2. **PRT with the FIR metric is a creative solution to a recognized sparse-reward problem.** The idea of using downgraded models to provide graded reward signals, with FIR as a principled stopping criterion for how much to weaken the model, is non-obvious. The ablation study (Table 2) confirms that PRT independently improves performance on most models, validating its contribution beyond the full system.

3. **Evaluation breadth is genuinely extensive.** Results span 16 white-box models across 6 model families (Llama, Mistral, Yi, Zephyr, Gemma, Qwen) plus 2 black-box models (70B–72B scale). This is not a paper that cherry-picks one or two models.

4. **Black-box setting results (Table 4) with ICL-based downgrading extend practical applicability.** The method does not require parameter access, meaningfully broadening its deployment scenarios.

## Weaknesses

### Fatal
None.

### Major

1. **The abstract's headline claim of ASR improvement is contradicted by the strongest comparable baseline.** The abstract and introduction state that AUTO-RT "significantly outperforms existing methods" and "significantly improves success rates (by up to 16.63%)." However, Table 3 shows AutoDAN achieving **55.23** ASR against AUTO-RT's **38.38** — a 16.85 percentage point advantage for AutoDAN. The paper relegates this comparison to a separate table labeled "human-based" (line 243), even though AutoDAN uses a genetic algorithm to *automatically evolve* prompts from handcrafted templates. The paper further characterizes AutoDAN as operating within "narrow, predefined strategy sets" (line 30), which understates its automatic exploration capability. If the most competitive automated method substantially outperforms AUTO-RT on the primary attack-success metric, the blanket claim that AUTO-RT "significantly improves success rates" is not supported. The paper's actual strength — diversity and sustained attack capability (DeD: 38.19 vs. AutoDAN's 17.88) — is not what the abstract advertises.

2. **The DeD (Defense Generalization Diversity) metric is critically underspecified.** The paper defines DeD as "assessed by first attacking the target model, then constructing defenses based on the successful attacks, and evaluating the ASR of second-round attacks on the defended model" (line 152). No details are given about: what type of defense is constructed, how many or which successful attacks are used, whether the defense is tailored to the attack distribution, or how the defense is trained/evaluated. Since DeD is the metric where AUTO-RT shows its largest advantage (e.g., 38.19 vs. 17.88 over AutoDAN in Table 3), this underspecification makes the paper's strongest evidence uninterpretable and non-reproducible.

3. **The main comparison (Table 1) uses weak baselines and excludes the strongest established methods.** The primary baselines (Few-Shot, Imitate Learning, RL) are essentially ablations of the same architecture rather than established red-teaming methods. AutoDAN, Rainbow-Teaming, GPTFuzzer, GCG, PAIR, and TAP — all cited in the paper's own related work — are absent from the main comparison table. AutoDAN appears only in a separate aggregate table (Table 3), and the other methods are not compared at all. If the contribution is about "strategy-level exploration," the method should be compared against other automated strategy-exploration methods under the same conditions on a model-by-model basis.

### Minor

4. **The "up to 16.63%" improvement figure in the abstract and introduction (lines 9, 34) has no identifiable referent in the results section.** No table, figure, or computed value in the paper produces 16.63%. This quantitative claim in the headline summary is unsubstantiated and should be connected to a specific experimental result or removed.

5. **No variance or statistical significance is reported for key comparisons.** All results in Table 1 are single-point estimates. On several models the differences are small (Llama 3 8B: AUTO-RT 15.00 vs. RL 14.55; Mistral 7B: AUTO-RT 52.65 vs. IL 54.88, where AUTO-RT *loses*). Without standard deviations or multi-run averages, it is impossible to assess which differences are meaningful. The violin plots (Figure 3) only cover 4 models and 2 methods.

6. **The R2D2 failure case is acknowledged but not analyzed.** On R2D2, which incorporates targeted defenses, AUTO-RT (12.45 ASR) is outperformed by Few-Shot (27.18) and Imitate Learning (24.24). The paper notes this result (line 185) but does not investigate *why* a defended model causes AUTO-RT to systematically underperform. Understanding this failure mode would strengthen the paper.

7. **The containment assumption for reward shaping is stated without empirical validation.** Figure 2 and its caption assert that "the unsafe region of m is fully contained within that of m'" (line 105). This monotonicity assumption is central to the PRT motivation but is never theoretically justified or empirically checked. The paper's own observation that over-weakened models provide "diminished guidance quality" (line 229) suggests containment may fail in practice for some downgrade levels.

8. **The characterization of AutoDAN as operating within "narrow, predefined strategy sets" (line 30) is imprecise.** AutoDAN employs a genetic algorithm that *evolves* handcrafted templates — a form of automated exploration, not a purely static set. This framing inflates the perceived gap that AUTO-RT fills.

### Trivial
None.

## Nice-to-Haves

- **Recenter the paper around diversity/sustained attack (DeD).** The paper's strongest evidence is that AUTO-RT maintains high ASR after defense construction while AutoDAN's ASR collapses (DeD 38.19 vs. 17.88). Framing the contribution around this capability would align the claims with the evidence.
- **Include AutoDAN in the main per-model comparison table** so the ASR vs. DeD tradeoff is transparent on a model-by-model basis.
- **Report results over multiple random seeds** with standard deviations for the most important comparisons.
- **Validate the containment assumption empirically** by measuring whether attacks that fail on the target model also fail on the downgrade model across a sample of strategies.
- **Specify the defense construction pipeline** for DeD in full operational detail.

## Removed Points

These points are flagged to be removed; treat them with caution.

- *No hyperparameters reported in the main text* — Reproducibility nitpick; such details standardly reside in the appendix (which was stripped by the paper parser, not missing from the submission). Rule: remove nitpicks about reproducibility such as undisclosed hyperparameters.
- *The FIR description is technically dense* — A stylistic judgment, not a substantive weakness.
- *Related work reads as a literature summary rather than positioning* — Vague; no concrete flaw identified.
- *Conclusion lacks limitations section* — The appendix (stripped) may contain this.
- *Theoretical guarantee relies on Sun et al. (2021)* — Referencing prior theoretical results is standard practice.
- *Reproducibility statement is insufficient* — Largely about missing appendix content.
- Generic strengths ("addressed an important problem") — Not specific to this paper.

## Novel Insights

Beyond the paper's own contributions, the cross-review reveals a tension worth noting: the paper's most interesting empirical finding — that strategy-level exploration produces attacks that are harder to defend against (DeD 38.19 vs. 17.88 over AutoDAN) — is currently buried under a conventional ASR framing. This mismatch between the paper's actual evidence and its advertised contribution highlights a broader pattern where red-teaming methods are primarily evaluated on first-attack success rate even when their comparative advantage lies in attack diversity and robustness to countermeasures. The DeD advantage is larger and more consistent than the ASR scores, suggesting the community may benefit from metrics that capture sustained adversarial pressure rather than single-shot success.

## Suggestions

1. Substantiate or remove the "16.63%" claim from the abstract and introduction.
2. Include AutoDAN in the main per-model comparison table alongside ASR and DeD.
3. Fully specify the DeD defense construction pipeline — what defense, how trained, on what data, with what hyperparameters.
4. Add standard deviations or confidence intervals from multiple runs for the most important comparisons.
5. Include an analysis of the R2D2 failure case and conditions under which AUTO-RT's strategy-level exploration underperforms sampling-based methods.
6. Add a limitations paragraph discussing the containment assumption and when downgrade model calibration might fail.

## Score and Decision

AUTO-RT presents two well-motivated technical components (DSP and PRT/FIR) with broad evaluation and an ablation study confirming each component's contribution. However, the paper's headline claims are in tension with its own evidence: the abstract promises ASR improvement while the strongest comparable baseline (AutoDAN) outperforms AUTO-RT on that very metric. The DeD metric — where the paper genuinely excels — is defined too vaguely to be interpreted or reproduced. The main comparison uses weak baselines and omits the most relevant competitors. These issues are fixable through honest reframing and additional specification, but in the current form the gap between claims and evidence is too wide. The score reflects a paper with solid technical ideas whose presentation and evaluation need substantial revision before the claimed contributions are supported.

MY FINAL SCORE: <score>5</score>
MY FINAL DECISION: <decision>Reject</decision>