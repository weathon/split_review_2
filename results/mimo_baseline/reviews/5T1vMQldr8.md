## Summary

The paper proposes SPOT, a framework that mitigates reward extrapolation errors in offline preference-based reinforcement learning by extracting subgoals from attention weights of a Preference Transformer, training a CVAE to generate subgoals for new states, and using cosine similarity-based reward shaping to guide policy learning toward preference-aligned regions. Experiments across D4RL locomotion, Robosuite manipulation, and Meta-World tasks show that SPOT achieves the highest average performance (78.82) with reduced variance compared to baselines, while also demonstrating improved query efficiency.

## Strengths

- **Novel integration of attention-based subgoal discovery with reward shaping for offline PbRL**: The idea of repurposing attention weights from a Preference Transformer to identify critical states and then using a CVAE to map arbitrary states to preference-aligned subgoals for reward shaping is creative and well-motivated. The dual-criteria filtering (top-K% attention + above-average reward) is a sensible design to avoid selecting poor-quality subgoals.

- **Comprehensive experimental evaluation and analysis**: The paper evaluates across three distinct benchmarks (D4RL, Robosuite, Meta-World) with diverse data qualities (medium, replay, expert, proficient-human, multi-human), includes multiple ablation studies (Top-K% analysis, reward shaping method comparison, weight sensitivity), an extrapolation error analysis (Figure 2), a qualitative case study (Figure 3), and a query efficiency study (Table 4). This breadth of analysis is commendable.

- **Query efficiency benefit**: Table 4 demonstrates that SPOT maintains consistent performance even with significantly reduced preference queries (e.g., from 500 to 50 in walker2d), while the Preference Transformer degrades. This is a practically valuable property for reducing annotation costs.

- **Reduced variance**: SPOT achieves notably lower average standard deviation (7.76) compared to PT (13.80) and MR (11.51), suggesting that subgoal regularization provides more stable training.

## Weaknesses

### Fatal

None.

### Major

- **Inconsistent per-task performance undermines "consistent superiority" claim**: While SPOT achieves the highest average, it underperforms significantly on several individual tasks. On lift-mh, SPOT (65.17) is far below MR (95.62) and even Oracle (81.62). On hop-m-r, DTR (94.18) outperforms SPOT (85.08) by 9 points. On drawer-open, SPOT (66.80) is substantially below IPL (87.64) and MR (86.6). On can-ph, SPOT (63.82) lags Oracle (73.25). The high average is partly an artifact of SPOT avoiding extreme failures rather than consistently excelling. The paper's narrative of "consistent superiority" (Section 5.1) is not well-supported by the results.

- **Weak theoretical justification for extrapolation error reduction**: The paper's central claim is that subgoal-guided reward shaping mitigates extrapolation errors, but this connection is never formalized. The argument that CVAE's KL regularization prevents OOD subgoal generation (Section 4.1.3) is hand-waved without connecting it to how this translates to reduced policy-level extrapolation error. The extrapolation error analysis in Section 5.3 defines error as |predicted - human_label|, but human labels are themselves from the training distribution and don't represent true ground-truth rewards in OOD regions, making the proxy circular.

- **Tight coupling to Preference Transformer**: The entire subgoal extraction pipeline depends on the attention weights from the Preference Transformer architecture. It is unclear whether this approach generalizes to other reward model architectures (e.g., MLP-based Bradley-Terry models, contrastive models like CPL). This significantly limits the scope and generality of the contribution.

### Minor

- **The cosine similarity reward shaping in raw state space is a strong assumption**: This assumes that state-space proximity (as a vector dot product) correlates with task progress, which holds in continuous control where observations are proprioceptive vectors but would break down in high-dimensional or image-based observation spaces. No discussion of this limitation is provided.

- **Limited hyperparameter sensitivity analysis**: λ is fixed at 1, β at 1, and K at 10% throughout most experiments. Only the Top-K% ablation (Table 2) and reward shaping weight analysis (Table 3) are provided. A systematic sensitivity analysis of λ on final performance across multiple tasks would strengthen the paper.

- **Average score computation excludes Meta-World from the Oracle average**: The footnote in Table 1 notes "oracle average is computed over 8 tasks excluding Meta-World" but SPOT's average includes Meta-World, making the comparison somewhat inconsistent. SPOT's advantage over Oracle (78.82 vs 77.25) is partially attributable to this discrepancy.

- **The case study (Figure 3) is qualitative and not strongly informative**: Showing that predicted subgoals are temporally offset by "approximately one timestep" is interesting but provides limited mechanistic insight into why the method works or when it might fail.

### Trivial

None beyond what the rules instruct me to ignore.

## Nice-to-Haves

- A comparison showing SPOT's benefit when applied on top of different reward model backbones (not just Preference Transformer) would significantly strengthen the generality claim.
- A more rigorous extrapolation error analysis, perhaps using environments where true rewards are available to measure actual OOD reward prediction accuracy without relying on human labels as proxy.
- Analysis of failure cases (e.g., lift-mh, drawer-open) to understand when the subgoal mechanism is harmful or unhelpful.

## Novel Insights

The paper's core insight—that attention weights from preference transformers can serve as subgoal identifiers, and that these subgoals can regularize offline PbRL training—is genuinely novel. The observation that higher attention-weight states (filtered by above-average reward) yield better policy performance than lower-weight states (Table 2) provides empirical evidence that attention patterns in preference learning encode meaningful temporal structure beyond simple credit assignment. The extrapolation error analysis in Figure 2, showing that states closer to subgoals exhibit lower reward prediction errors even in OOD settings, suggests a promising direction for understanding and controlling distributional shift in learned reward models.

## Suggestions

- The authors should temper the "consistent superiority" narrative and provide a more nuanced discussion of when the method excels versus when it falls short (e.g., discuss the lift-mh and drawer-open failures).
- Provide a formal or semi-formal argument (even in an appendix) connecting CVAE-regularized subgoal proximity to bounded extrapolation error.
- Test on at least one non-continuous-control domain (e.g., a discrete or high-dimensional observation task) to assess the generality of the cosine similarity reward shaping.
- Add error bars on the extrapolation error plots (Figure 2) to assess statistical significance of the differences.

MY FINAL SCORE: <score>4.0</score>
MY FINAL DECISION: <decision>Reject</decision>