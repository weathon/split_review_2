## Summary
The paper proposes a data-driven method for combinatorial optimization (Max-Cut/Ising) that parameterizes the update rule of an iterative “Ising machine” with a small MLP, then learns the MLP weights via zeroth-order evolutionary optimization. This combines algorithm unrolling with physics-inspired dynamical systems to learn effective search strategies from data. Results on standard Max-Cut, MIS, and Max-Clique benchmarks show competitive or state-of-the-art performance compared to both neural-CO methods and classical Ising machine algorithms.

## Strengths
- **Novel integration of algorithm unrolling with Ising machines.** Applying unrolling to NP-hard combinatorial optimization problems and tuning the dynamics of a physics-inspired iterative solver with a learned neural component is a creative and underexplored direction.
- **Use of zeroth-order optimization avoids gradient pathologies.** The evolutionary training bypasses the severe vanishing/exploding gradient issues that would arise from backpropagation through many unrolled steps, making the approach practical.
- **Strong empirical results across multiple benchmarks.** The method (especially dNPIM) achieves better or comparable performance to recent neural CO methods (DiffUCO, SDDS) on MIS/MaxClique/MaxCut benchmarks, and outperforms state-of-the-art Ising machines on most G-set Max-Cut instances in terms of time-to-solution.
- **Ablation and analysis provide insight.** The study of architecture parameters (Tc, D, M) and the visualization of learned dynamics (emergence of momentum-like behavior) help understand how the network learns effective search strategies.

## Weaknesses
### Fatal
None.

### Major
- **Limited comparison to the broader neural CO literature.** Table 1 only compares to one recent paper (Sanokowski et al. 2025). Other important neural CO baselines for Max-Cut/MIS (e.g., GNN-based methods such as Schuetz et al. 2022, LwD, or RL-based approaches) are absent. The “state-of-the-art” claim is therefore not fully justified.
- **Unfair computational budget in Table 1.** dNPIM runs 30 trajectories in parallel and selects the best solution, while the compared methods (DiffUCO, SDDS) appear to report single-trajectory results. This makes the time comparison misleading and the performance advantage less clear.
- **Training scalability is a practical limitation.** The authors note that training from scratch on N=500 is impossible, requiring bootstrapping from smaller N. This limits the method’s applicability to large problems and suggests the training cost could be prohibitive for new instance distributions.
- **G-set results on planar instances are poor (TTS 4.42e7 vs. CAC 1.81e6).** The paper attributes this to general difficulty but offers no analysis or solution. A systematic reason for this failure mode would strengthen the work.

### Minor
- **The difference between cNPIM and dNPIM is discussed qualitatively but not rigorously explained.** The claim that cNPIM overfits to a relaxed objective is plausible but not backed by concrete evidence (e.g., correlation with the Ising gap).
- **The method requires generating a training set for each problem distribution (e.g., each G-set type).** This contrasts with classical heuristics that work out-of-the-box and limits practical deployment after training.
- **Some figures are hard to parse.** Figure 2 contains many subplots with small labels; the meaning of “Network A” and “Network B” could be clearer in the caption. Figure 1b/c are not directly referenced in the main text.

### Trivial
None.

## Nice-to-Haves
- A direct wall-clock time comparison on G-set (not just iterations) would clarify the practical impact of the method.
- Analysis of how the learned dynamics differ from existing Ising machines beyond the momentum observation (e.g., frequency analysis of the learned weights).
- Experiments on a real-world or industrial CO problem instance to demonstrate practical utility.

## Novel Insights
The paper demonstrates that effective search dynamics for NP-hard problems can be learned entirely from data, without hand-crafted heuristics. The emergence of momentum and annealing-like behavior from a simple MLP trained only to maximize solution quality provides evidence that these physically-inspired mechanisms are not unique to hand-designed algorithms but are natural outcomes of learning to navigate non-convex landscapes. This bridges the gap between theoretical physics-inspired algorithms and data-driven optimization.

## Suggestions
- Normalize the computational budget in Table 1 (e.g., report single-trajectory time and performance, or use a fixed total wall-clock budget for each method).
- Add a comparison to at least one more recent neural CO method for Max-Cut (e.g., LwD or GNN-based local search) to strengthen the state-of-the-art claim.
- Provide a more detailed discussion of why the planar G-set instances are particularly hard for the learned dynamics, and whether a different architecture or training distribution could close the gap.
- Include a brief analysis of training convergence and sample efficiency (e.g., how many trajectories are needed per epoch).

## Score and Decision
The paper presents a novel and well-executed combination of algorithm unrolling with Ising machines, supported by competitive experimental results on several benchmarks. The weaknesses—limited baseline comparison, unfair computational budget in one table, and scalability concerns—are significant but not fatal. The contribution is solid and should be of interest to the ICLR community.

MY FINAL SCORE: <score>6.0</score>
MY FINAL DECISION: <decision>Accept</decision>