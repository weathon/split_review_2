## Summary

The paper proposes Neural Network Ising Machines (NPIM), a method that applies algorithm unrolling to dynamical Ising machines for solving NP-hard Max-Cut/Ising problems. The update function of an Ising machine is parameterized by a small MLP, and the network weights are trained via zeroth-order evolutionary optimization. The method achieves competitive or state-of-the-art performance against both neural combinatorial optimization approaches and classical Ising machine algorithms on G-set and other benchmarks.

## Strengths

- **Novel combination of ideas.** The paper brings together algorithm unrolling, dynamical Ising machines, and zeroth-order optimization in a genuinely new way. Applying algorithm unrolling to NP-hard combinatorial optimization (beyond ILP) is, to my knowledge, unexplored territory. The proposed formulation in Eqs. 2–5 is clean and general, providing a principled framework for learning Ising machine dynamics.

- **Thorough and multi-faceted benchmarking.** The paper benchmarks against both neural CO methods (Table 1: DiffUCO, SDDS, LTFT on MIS/Max-Clique/Max-Cut) and classical Ising machine algorithms (Table 2: CAC, CFC, dSBM on G-set). dNPIM outperforms SOTA in 4/5 neural CO benchmarks on solution quality and outperforms Ising machine baselines on most G-set instances (800-node, with TTS improvements of ~2–6× over CAC on random and toroidal instances). This dual-benchmarking is valuable and positions the work clearly within two communities.

- **Interesting emergent dynamics analysis.** Section 4.1 demonstrates that a single-layer NPIM learns a "momentum" mechanism during training—transitioning from greedy steepest descent to a strategy that escapes local minima. Figure 2 provides a compelling visualization of how network weights evolve from all-negative (greedy) to a mixture of positive and negative (momentum-like), grounding the learned dynamics in physically interpretable concepts.

- **Clear treatment of cNPIM vs. dNPIM trade-offs.** Section 4.5 provides a nuanced analysis showing that continuous coupling (cNPIM) achieves higher average success rate but overfits to easier instances, while discrete coupling (dNPIM) generalizes better to hard instances. This is a valuable practical insight supported by the scatter plots in Figures 3b and 3e.

## Weaknesses

### Fatal
None.

### Major

- **Method-specific tuning undermines generality claims.** The paper repeatedly emphasizes the simplicity and flexibility of the approach, yet the practical deployment requires: (i) bootstrapping and fine-tuning across problem sizes/difficulty levels (Section 4.3), (ii) training separate networks for each graph type in the G-set (Appendix I reference), and (iii) choosing between cNPIM and dNPIM based on the benchmark. This is a significant practical burden that tempers the claimed generality. The fine-tuning requirement is essentially per-instance-distribution hyperparameter tuning, which is similar to what classical Ising machine algorithms already do.

- **Scalability with parameters is a real concern.** The zeroth-order optimization has O(P) sample complexity per gradient estimate (where P is parameter count), and Figure 4 (referenced but from appendix) presumably shows increasing training overhead. With the network having only ~50–140 parameters for competitive performance, the method cannot easily learn non-local moves or more sophisticated strategies. The authors acknowledge this but provide no concrete mitigation beyond suggesting hybrid approaches. This limits the ceiling of what the method can learn.

- **Missing comparison with recent diffusion-based methods on G-set.** Table 2 compares against CAC (2019–2021), CFC, and dSBM, but diffusion-based methods like Sanokowski et al. (2024, 2025) are only compared on the neural CO benchmarks (Table 1). Given that the paper positions itself against both communities, a comparison with diffusion samplers on G-set would strengthen the Ising machine benchmark results.

### Minor

- **G-set results use dated baselines.** The TTS comparisons in Table 2 use Reifenstein et al. (2021) and Goto et al. (2021) as state-of-the-art. The field has advanced since then, and while the results are still impressive, the "SOTA" claim is qualified by the specific baselines chosen.

- **TTS metric in "number of iterations" is convenient but incomplete.** Since different algorithms may require vastly different numbers of iterations *and* per-iteration computational costs differ, reporting TTS in iterations alone (Table 2) could be misleading. The authors justify this by saying the matrix-vector product dominates, but this should be validated with wall-clock comparisons.

- **The Fourier basis choice for temporal modulation (Eq. 7) is not strongly motivated.** While Appendix C.2 shows the basis type matters little compared to M, the choice of Fourier basis over other smooth bases deserves at least a brief justification in the main text.

- **The claim about learning dynamics "from scratch" is partially overstated.** The bootstrapping and fine-tuning process (Section 4.3) means the network is not learning entirely from scratch on the target problem distribution. The initialization from easier problems carries significant implicit information.

### Trivial
None.

## Nice-to-Haves

- A wall-clock time comparison across all methods (including the neural CO baselines in Table 1) would make the benchmarks more interpretable.
- An analysis of what specific non-trivial strategies the learned MLPs encode beyond the momentum intuition—for example, via visualization of the learned function F across different problem types.
- Comparison on at least one real-world or large-scale industrial problem instance to demonstrate practical utility.

## Novel Insights

The paper's most novel insight is that algorithm unrolling—traditionally applied to convex optimization problems in signal processing—can be effectively applied to NP-hard combinatorial optimization when paired with zeroth-order training. The observation that zeroth-order methods sidestep the vanishing/exploding gradient problem inherent in long-horizon Ising machine trajectories is practically important and distinguishes this approach from policy-gradient methods that suffer from poor reward attribution. The finding that discrete coupling (dNPIM) provides better worst-case generalization than continuous coupling (cNPIM) despite lower average-case performance is an interesting practical observation with potential implications for other neural CO methods that use continuous relaxations.

## Suggestions

- Add a wall-clock time comparison alongside the iteration-based TTS for the G-set benchmarks, or at least provide a per-iteration FLOPS analysis for NPIM vs. CAC vs. CFC.
- Quantify the overhead of the fine-tuning process (number of training epochs, compute required) to give practitioners a realistic picture of the total cost.
- Consider reporting results on larger problem instances (N > 800) to better assess scalability, even if only for a subset of G-set types.
- Provide a clearer comparison with the zeroth-order method from Reifenstein et al. (2024) to distinguish the contribution of the NPIM architecture from the training method.

## Score and Decision

The paper makes a genuine and novel contribution by bridging algorithm unrolling with dynamical Ising machines for combinatorial optimization, using an appropriate training methodology (zeroth-order optimization) to handle the long-horizon dynamics. The experimental results are competitive across two distinct benchmarking traditions, and the analysis of emergent dynamics and the cNPIM/dNPIM trade-off provides useful insights. However, the need for instance-specific fine-tuning weakens the generality claim, the scalability limitations of zeroth-order optimization are a genuine concern, and some benchmark comparisons use dated baselines. The work is solid and publishable but falls short of a strong accept due to these practical limitations.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>