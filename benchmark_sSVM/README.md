## Benchmark repository for smoothed SVMs

Smoothed SVMs solve the following optimization problem:
```math
  \min_{\mathbf{\beta} \in \mathbb{R}^d} \frac{C}{n} \sum_{i=1}^n V( y_i \mathbf{\beta}^\intercal \mathbf{x}_i ) + \frac{1}{2} \| \mathbf{\beta} \|_2^2
```
where $\mathbf{x}_i \in \mathbb{R}^d$ is a feature vector, and $y_i \in \{-1, 1\}$ is a binary label, and $V(\cdot)$ is the modified Huber loss or the smoothed hinge loss:
```math
\begin{equation*}
  V(z) =
  \begin{cases}
  \ 0, & z \geq 1, \\
  \ (1-z)^2/2,                  & 0 < z \leq 1, \\
  \ (1/2 - z ),   & z < 0.
  \end{cases}
\end{equation*}
```


Smoothed SVM can be rewritten as a ReHLine optimization with
```math
\mathbf{S} \leftarrow -\sqrt{C/n} \mathbf{y}^\intercal, \quad
\mathbf{T} \leftarrow \sqrt{C/n} \mathbf{1}^\intercal_n, \quad
\mathbf{\tau} \leftarrow \sqrt{C/n} \mathbf{1}^\intercal_n.
```
where $\mathbf{1}_n = (1, \cdots, 1)^\intercal$ is the $n$-length one vector, $\mathbf{X} \in \mathbb{R}^{n \times d}$ is the feature matrix, and $\mathbf{y} = (y_1, \cdots, y_n)^\intercal$ is the response vector.
### Benchmarking solvers

The solvers can be benchmarked using the command below:

```bash
benchopt run . -d classification_data
```
