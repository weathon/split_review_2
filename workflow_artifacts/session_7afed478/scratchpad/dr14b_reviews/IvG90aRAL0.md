### Summary

This paper studies the Frank-Wolfe algorithm in the quantum setting, which is a classical projection-free optimization method. The authors propose two quantum algorithms for sparse constraints that find a $\varepsilon$-optimal solution with the query complexity of $O(\sqrt{d/\varepsilon})$ and $O(1/\varepsilon)$ by using the function value oracle, reducing a factor of $O(\sqrt{d})$ and $O(d)$ over the best classical algorithm, respectively, where $d$ is the dimension. For the matrix domain, the authors propose two quantum algorithms for nuclear norm constraints that improve the time complexity to $\tilde{O}(rd/\varepsilon^2)$ and $\tilde{O}(\sqrt{rd}/\varepsilon^3)$ for computing the update step, reducing at least a factor of $O(\sqrt{d})$ over the best classical algorithm, where $r$ is the rank of the gradient matrix.

### Soundness

3

### Presentation

3

### Contribution

3

### Strengths

1. The authors propose the quantum Frank-Wolfe algorithm for the projection-free sparse convex optimization problem under $\ell_1$ norm constraints and the $d$-dimensional simplex $\Delta_d$. They achieve a query complexity of $\tilde{O}(\sqrt{d}/\epsilon)$ in finding an $\epsilon$-optimal solution using the function value oracle, reducing a factor of $O(\sqrt{d})$ over the optimal classical algorithm. Furthermore, if the objective function is a Lipschitz continuous function, they prove that the query complexity can be reduced to $O(1/\epsilon)$ by employing the bounded-error Jordan quantum gradient estimation algorithm, at the cost of more qubits and additional gates.

2. The authors propose two complementary quantum Frank-Wolfe algorithms tailored to high-rank and low-rank gradient matrices, respectively. For finding an $\epsilon$-optimal solution, they achieve a time complexity of $\tilde{O}(rd/\epsilon^2)$ and $\tilde{O}(\sqrt{rd}/\epsilon^3)$ in computing the update direction, representing an at least $O(\sqrt{d})$ speedup over state-of-the-art classical algorithm, where $r$ is the rank of the gradient matrix.

### Weaknesses

#### Some Related Works


#### comment

1. The authors propose the quantum Frank-Wolfe algorithm for the projection-free sparse convex optimization problem under $\ell_1$ norm constraints and the $d$-dimensional simplex $\Delta_d$. They achieve a query complexity of $\tilde{O}(\sqrt{d}/\epsilon)$ in finding an $\epsilon$-optimal solution using the function value oracle, reducing a factor of $O(\sqrt{d})$ over the optimal classical algorithm. Furthermore, if the objective function is a Lipschitz continuous function, they prove that the query complexity can be reduced to $O(1/\epsilon)$ by employing the bounded-error Jordan quantum gradient estimation algorithm, at the cost of more qubits and additional gates.

2. The authors propose two complementary quantum Frank-Wolfe algorithms tailored to high-rank and low-rank gradient matrices, respectively. For finding an $\epsilon$-optimal solution, they achieve a time complexity of $\tilde{O}(rd/\epsilon^2)$ and $\tilde{O}(\sqrt{rd}/\epsilon^3)$ in computing the update direction, representing an at least $O(\sqrt{d})$ speedup over state-of-the-art classical algorithm, where $r$ is the rank of the gradient matrix.

### Suggestions

The paper introduces quantum algorithms for sparse convex optimization, which is a valuable contribution. However, the practical implications of these algorithms need further clarification. While the theoretical speedups are significant, the constant factors hidden within the $\tilde{O}$ notation could be substantial, potentially limiting the practical advantage of these quantum algorithms. For instance, the quantum gradient estimation algorithm, while achieving a better asymptotic complexity, requires a significant number of qubits and quantum gates, which might be challenging to implement on current and near-term quantum hardware. A more detailed analysis of the constant factors and a discussion of the hardware requirements would be beneficial to assess the practical feasibility of these algorithms. Furthermore, it would be helpful to provide a comparison of the resource requirements (e.g., number of qubits, gate count, coherence time) of the proposed quantum algorithms with those of classical algorithms for specific problem instances. This would allow for a more concrete understanding of the potential advantages and limitations of the proposed quantum approaches.

Additionally, the paper could benefit from a more thorough discussion of the assumptions made about the quantum computer. While the authors mention the use of quantum oracles and quantum gradient estimation, a more detailed explanation of the specific quantum subroutines used and their implementation details would be valuable. For example, the paper could elaborate on the specific quantum circuits used for gradient estimation and how they are adapted for the Frank-Wolfe algorithm. Furthermore, it would be beneficial to discuss the potential impact of noise and decoherence on the performance of the proposed quantum algorithms. A discussion of error mitigation techniques and their impact on the overall performance would also be valuable. This would help to clarify the robustness of the proposed algorithms and their potential for practical implementation.

Finally, while the paper focuses on the theoretical aspects of the proposed quantum algorithms, it would be beneficial to include some numerical experiments to demonstrate their performance on specific problem instances. This would provide a more concrete understanding of the practical behavior of the algorithms and their potential advantages over classical methods. The experiments could include a comparison of the convergence rate and the solution quality of the quantum algorithms with those of classical algorithms for different problem sizes and parameter settings. This would help to validate the theoretical results and provide a more comprehensive evaluation of the proposed quantum approaches. Furthermore, it would be useful to explore the sensitivity of the algorithms to different problem parameters and to investigate the impact of different quantum hardware architectures on their performance.

### Questions

1. What are the assumptions about the quantum computer? Can you explain more about the quantum subroutines used in the algorithms?

### Rating

6

### Confidence

3

**********