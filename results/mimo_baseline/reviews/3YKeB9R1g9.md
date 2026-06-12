## Summary

This paper extends the "supercollapse" phenomenon of Qiu et al. (2025)—where normalized training loss curves (TLCs) from different model sizes collapse onto a universal trajectory—to practical LLM scaling recipes that co-scale width, depth, batch size, and weight decay under μP. The authors identify three scale-invariant controls governing TLC shape (AdamW timescale τ, tokens-per-parameter ratio TPP, and LR schedule), introduce the Celerity model family trained in a collapse regime, and demonstrate two practical applications: using collapse residuals for early detection of training pathologies and using collapse-based prediction for early stopping in hyperparameter tuning.

## Strengths

- **Well-motivated and practically significant research question.** The paper clearly identifies a gap from Qiu et al. (2025), which called for tests at larger scales with practical scaling ladders. The paper directly addresses this, showing collapse persists in full-scale LLM families with weight decay, μP, and co-scaled architecture parameters.

- **Systematic, well-designed experiments isolating each control variable.** Figures 3 and 4 cleanly demonstrate that TLC shape is modulated by τ, TPP, and LR schedule through controlled sweeps (varying η, λ, or B while holding τ fixed). The finding that matching τ produces matching curve shapes across hyperparameter choices (Fig. 3) is convincing evidence that τ captures a meaningful quantity.

- **Genuine practical applications with strong evidence.** The collapse-residual diagnostic is compelling: in the 1.8B run, divergence from the reference curve was detectable at ~60% of training, while the raw loss only showed issues at ~90% (Fig. 6 right). The early stopping experiments (Fig. 9) show negligible loss gaps when stopping after just 10–30% of training for λ sweeps at 1.7B and 3.3B, compared to unreliable "current best" selection.

- **Celerity as a concrete instantiation.** The Celerity family demonstrates that collapse-based training lands on the compute-efficiency frontier (Fig. 2), with models competitive against comparable open models. The TPP trade-off analysis (Fig. 5) showing 62% parameter reduction at 1.67× compute cost is a useful contribution.

- **Theoretical grounding via noisy quadratic model.** The bias-variance decomposition (Eq. 3) provides clear intuition for why τ modulates TLC shape: smaller τ yields faster initial descent but higher variance floor, while larger τ suppresses variance but slows early progress. The scale-invariance argument (curvature factor cancels in normalization) is elegant.

## Weaknesses

### Fatal
None.

### Major

- **Limited model scale for the core claims.** The largest Celerity model is 3.9B parameters, and the early stopping validation goes up to 3.3B. The paper makes strong claims about utility for "very large models" and "$1B runs," but the experiments don't validate at scales where the practical value would be most compelling. While the underlying regularities are scale-invariant by construction (via μP), there could be failure modes at larger scales (e.g., from different hardware, different optimization dynamics) that remain undetected. A 7B+ experiment, even partial, would substantially strengthen the paper.

- **Celerity evaluation scope is limited.** The downstream evaluation uses average accuracy on 7 tasks (arc-c, arc-e, boolq, hellaswag, piqa, siqa, winogrande), which is a narrow slice of LLM capability. While the paper notes this is about methodology rather than benchmark-chasing, the claim that Celerity is "at the compute-efficiency frontier" is only demonstrated on this specific task set. Adding MMLU, common-sense reasoning diversity, or perplexity on standard corpora would make the frontier claim more convincing.

### Minor

- **The early stopping procedure has practical overhead.** The method requires training small proxy models for each unique combination of TLC controls (τ, TPP, LR schedule), fitting a parametric surrogate with alternating optimization, and then aligning partial curves. While cheaper than training to completion, the overhead is non-trivial and could be better quantified—e.g., what fraction of the cost of a single full large-scale run does the entire early-stopping pipeline consume?

- **LR warmup inconsistency at 20 TPP.** The paper notes "small early deviations" at 20 TPP (Fig. 6 left), attributing them to differing LR warmup proportions (Table 2 shows warmup as min(10% of tokens, 375M tokens), which varies by model size). This suggests the collapse framework requires additional care about warmup scheduling that the paper doesn't fully address.

### Trivial
None.

## Nice-to-Haves

- A discussion of how collapse interacts with learning rate warmup schedules, especially given the 20 TPP deviation observed in experiments.
- Quantification of the computational cost of the early-stopping pipeline relative to full training runs.
- Analysis of whether collapse residuals could be used not just for detecting issues but for *predicting* downstream task performance, not just final loss.

## Novel Insights

The paper's most novel insight is that collapse is not merely a mathematical curiosity but a *signature of compute-efficient training*—it emerges precisely when optimization hyperparameters are set optimally for the given data budget. This reframes collapse from an observed regularity into a practical diagnostic tool: if your training curves don't collapse when they should (fixed TPP, optimal τ), something is wrong. The connection between the AdamW timescale as an EMA over weight updates and the bias-variance decomposition of training dynamics provides a satisfying mechanistic explanation. Additionally, the observation that fixing τ during hyperparameter sweeps (rather than fixing λ) preserves loss ordering throughout training (Fig. 7) is a practically valuable finding for HPO methodology.

## Suggestions

- Include at least one experiment at 7B+ scale, even if partial, to validate that the collapse framework and early stopping methodology scale as predicted.
- Add MMLU or a broader evaluation suite to the Celerity benchmark comparison to strengthen the compute-efficiency frontier claim.
- Quantify the total computational cost of the early-stopping pipeline (proxy model training + surrogate fitting + partial large-scale runs) versus naive full training, to give practitioners a clear cost-benefit picture.
- Investigate and formalize the warmup schedule conditions needed for tight collapse, especially at lower TPP.

## Score and Decision

The paper presents a well-executed extension of the collapse phenomenon to practical LLM training, with clear methodology, solid experiments, and two genuinely useful applications (training diagnostics and early stopping). The core scientific contribution—identifying τ, TPP, and LR schedule as the three scale-invariant controls governing TLC shape—is sound and well-supported. The main limitation is scale: the experiments top out at 3.9B parameters, which limits confidence in the practical utility claims for frontier-scale training. The early stopping application is novel and demonstrated convincingly at multi-billion parameter scale. Overall, this is a solid methodology paper that would be valuable to the LLM training community.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Accept</decision>