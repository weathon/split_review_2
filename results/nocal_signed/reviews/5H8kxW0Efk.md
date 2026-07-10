Now I have a clear picture. Let me compose the final review.

## Summary

This paper proposes Neural Network Ising Machines (NPIM), applying algorithm unrolling — parameterizing the update step of a dynamical Ising machine with a small odd-symmetric MLP — to NP-hard Max-Cut/Ising problems. The architecture is carefully designed (no biases for symmetry, truncated coupling-field history as input, Fourier basis for time-varying weights), and the parameters are trained via zeroth-order evolutionary optimization (avoiding the vanishing-gradient and reward-attribution problems that plague backprop/REINFORCE through long trajectories). The method is evaluated on neural-CO benchmarks (MIS, MaxClique, MaxCut) and G-set Max-Cut instances, achieving competitive results in both traditions.

## Strengths

- **Genuinely novel combination of techniques.** The paper is the first to apply algorithm unrolling — a technique previously successful in convex signal reconstruction — to NP-hard combinatorial optimization via Ising machine dynamics. The specific architecture (odd-symmetric MLP without biases, truncated history of coupling fields as input, Fourier basis for time-varying weights, §3.3) is well-motivated and respects the symmetries of the Ising problem. This is not an incremental combination; it required nontrivial bridging between the dynamical-systems and neural-CO literatures.

- **Competitive results across two evaluation traditions.** The method achieves strong objective values on neural-CO benchmarks (Table 1: best average on 4/5 tasks) and competitive TTS on G-set Max-Cut instances (Table 2: best TTS on 3/5 instance types). That the same architecture performs well on both the neural-CO metrics (solution quality + wall-clock time) and the Ising-machine metric (TTS) is non-trivial and demonstrates empirical reach.

- **Principled approach to training.** The use of zeroth-order optimization (§2.4, §3.4) is justified by the impossibility of backpropagation through many-timestep Ising machine trajectories (vanishing gradients, noisy REINFORCE). This is a real problem correctly identified, in contrast to prior work that struggles with reward attribution for CO algorithms (Zhang et al. 2023, Sanokowski et al. 2024).

## Weaknesses

### Major

- **SOTA claims outpace supporting evidence.** The paper claims "state-of-the-art performance" (abstract, intro, conclusion) but the G-set comparison in Table 2 is against results from Reifenstein et al. (2021) and Goto et al. (2021). While the paper cites more recent work (e.g., Leleu & Reifenstein 2025 for CAC), the benchmark table does not incorporate these contemporary results, making the strongest SOTA claims unsubstantiated for 2026 standards. The paper should either update baselines to 2024–2026 results or soften the SOTA framing to "competitive."

- **Asymmetric comparison in neural-CO benchmarks (Table 1).** dNPIM uses a "top 30" multi-trajectory selection strategy — running 30 trajectories in parallel and taking the best — while the comparison methods (DiffUCO, SDDS, LTFT) do not appear to use this advantage. Additionally, dNPIM is 40–60× slower on large instances (MIS-large: 1:20 vs. 0:03; MaxCut-large: 1:20 vs. 0:02), which the paper attributes to implementation differences (dense PyTorch vs. sparse graph library) rather than algorithm. Controlled comparisons (single-trajectory dNPIM, or multi-trajectory baselines) are needed to disentangle whether the advantage comes from learned dynamics or from parallel selection. The paper acknowledges both issues but does not resolve them.

- **Training cost is not reported.** The paper never states the number of epochs, training instances per epoch, GPU-hours for pretraining vs. fine-tuning, or how these costs scale with problem size N and parameter count. For a data-driven method where training overhead is a key practical consideration, this omission prevents assessment of whether the optimization budget is justified by the performance improvement.

- **Bootstrapping limitation.** The paper states that "training a network from scratch at the larger problem size (N=500) is not possible" (§4.3). The method requires pretraining on N=100 and fine-tuning. It is unclear whether this curriculum can be constructed for novel problem distributions where no easier instances exist, and how much of the fine-tuning performance derives from learned knowledge vs. lucky initialization from pretrained weights.

### Minor

- **Overfitting on hard instances (§4.5).** cNPIM has zero success rate on some problem instances (Figure 3b). While the paper openly acknowledges this and shows dNPIM mitigates the issue, the root cause — optimizing average reward across instances inherently sacrifices performance on hard instances — is not addressed. This limits applicability for users needing worst-case reliability, though the paper's framing centers on average-case performance.

## Nice-to-Haves

- A single-trajectory ablation of dNPIM in Table 1 would directly test whether the advantage comes from learned dynamics or parallel selection.
- Reporting variance / confidence intervals across random seeds for main results, especially given the zeroth-order optimizer's inherent variance.
- Comparing against simpler temporal schedules (piecewise constant, linear) beyond the Fourier/Chebyshev/Legendre comparison.

## Removed Points

These points from the input review were removed or demoted after verification against the paper:

1. **"Fourier temporal basis not ablated"** — The paper states this comparison (Fourier, Chebyshev, Legendre) exists in Appendix C.2 (Fig. 5); the appendix is stripped by the parser, so this criticism cannot be verified against the available text. The critic's further request for piecewise-constant/linear schedules is valid but falls under Nice-to-Haves.
2. **"No comparison against hand-tuned classical Ising machine on neural-CO benchmarks"** — Scope creep; the neural-CO benchmarks in Table 1 are drawn from the neural CO literature (Sanokowski et al. 2025), not the Ising machine literature. The Ising machine comparison is done separately on G-set (Table 2).
3. **"Catastrophic overfitting as disqualifying"** — Overstating the severity. The paper acknowledges the issue, dNPIM mitigates it, and the paper's claims are about average-case performance. Moved to Minor weakness.
4. **Section-by-section presentation nitpicks** (equation density in 4–5, error bars in Fig 3c) — minor formatting observations with no bearing on the paper's contribution.

## Novel Insights

The emergence-of-momentum analysis (§4.1, Figure 2) is a genuinely interesting interpretability result: networks first learn greedy descent (all negative weights), then gradually develop positive weights corresponding to momentum effects that help escape local optima. This connects data-driven learning to known physical intuition about effective Ising machine dynamics and demonstrates that complex search heuristics can emerge from a simple objective (maximizing reward) without explicit inductive bias toward those heuristics.

## Suggestions

1. Add a single-trajectory dNPIM column to Table 1 to normalize the computational budget.
2. Either compare against the best published G-set TTS results through 2025–2026, or replace "SOTA" claims with "competitive" throughout.
3. Report training cost concretely: GPU-hours, epoch count, instances per epoch, and how cost scales with N.
4. Include variance estimates (e.g., multiple random seeds) for the main benchmark results.

## Score and Decision

The paper makes a genuinely novel contribution — applying algorithm unrolling to Ising machine dynamics for NP-hard CO, with a carefully designed architecture and principled training approach. The empirical results are competitive across two evaluation traditions. However, the evaluation has significant gaps: the SOTA claims on G-set rest on 2021 baselines without contemporary comparison, the neural-CO benchmark comparison is asymmetric (multi-trajectory selection vs. single-trajectory baselines, with timing confounded by implementation differences), training cost is entirely unreported, and the method requires bootstrapping from smaller problem sizes. These are fixable issues — contemporary baselines exist in the literature, a single-trajectory ablation would clarify the comparison, and training costs can be reported — but in their current form, the strongest claims are not fully supported. The paper demonstrates a promising new direction with solid evidence for its core thesis (learned dynamics can be effective), but needs stronger evidential support for its SOTA framing.

MY FINAL SCORE: <score>6</score>
MY FINAL DECISION: <decision>Borderline Accept</decision>