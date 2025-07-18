---
title:  LQR Control Using Factor Graphs
date:   2019-11-07
authors:
  - name: Gerry Chen
    url: https://gerry-chen.com
  - name: Yetong Zhang
    url: https://www.linkedin.com/in/yetong-zhang-9b810a105/
  - name: Frank Dellaert
    url: https://dellaert.github.io/
intro:  "Demonstrates how to frame Linear Quadratic Regulator (LQR) control problems as factor graphs, enabling efficient optimization techniques borrowed from SLAM and sensor fusion to solve classic control tasks."
---

# Introduction

```{figure} /_static/lqr_control/VE/fg_lqr.png
:label: Figure 1
:width: 75%
:align: center

Factor graph structure for an LQR problem with 3 time steps. The cost factors are marked with dashed lines and the dynamics constraint factors are marked with solid lines.
```

In this post we explain how optimal control problems can be formulated as factor graphs and solved
by performing variable elimination on the factor graph.

Specifically, we will show the factor graph formulation and solution for the
**Linear Quadratic Regulator (LQR)**.  LQR is *a state feedback controller which derives the optimal gains
for a linear system with quadratic costs on control effort and state error*.

We consider the [**finite-horizon, discrete LQR
problem**](https://stanford.edu/class/ee363/lectures/dlqr.pdf).
The task is to *find the optimal controls $u_k$ at time instances $t_k$
so that a total cost is minimized*.  Note that we will later see the optimal controls can be represented in the form $u^*_k = K_kx_k$ for some optimal gain matrices $K_k$.  The LQR problem can be represented as a constrained optimization
problem where the costs of control and state error are represented by the
minimization objective {eq}`eq:cost`, and the system dynamics are represented by the
constraints {eq}`eq:dyn_model`.

```{math}
\def\argmin{\mathop{\mathrm{argmin}}\limits}
\def\coloneqq{\mathrel{\mathop:}=}

\argmin\limits_{u_{1\sim N}} ~~x_N^T Q x_N + \sum\limits_{k=1}^{N-1} x_k^T Q x_k + u_k^T R u_k \label{eq:cost}
```

$$
s.t. ~~ x_{k+1}=Ax_k+Bu_k ~~\text{for } k=1 \text{ to } N-1 \label{eq:dyn_model}
$$

We can visualize the objective function and constraints in the form of a factor
graph as shown in **Figure 1**. This is a simple Markov chain, with the oldest
states and controls on the left, and the newest states and controls on the right. **The
ternary factors represent the dynamics model constraints and the unary
factors represent the state and control costs we seek to minimize via least-squares.**

# Variable Elimination
To optimize the factor graph, which represents minimizing the least squares objectives above, we can simply eliminate the factors from right
to left.  In this section we demonstrate the variable elimination graphically and algebraically, but the matrix elimination is also
provided in the [Appendix](#appendix-target).


::::{tab-set}

:::{tab-item} 2a
| ![fig2a](/_static/lqr_control/Elimination/cropped_Slide1.png) | 
| :---: |
| **Figure 2a** Elimination of state $x_2$ |
:::


:::{tab-item} 2b
| ![fig2b](/_static/lqr_control/Elimination/cropped_Slide2.png) | 
| :---: |
| **Figure 2b** Elimination of state $x_2$ |
:::

:::{tab-item} 3a
| ![fig3a](/_static/lqr_control/Elimination/cropped_Slide3.png) | 
| :---: |
| **Figure 3a** Elimination of state $u_1$ |
:::

:::{tab-item} 3b
| ![fig3b](/_static/lqr_control/Elimination/cropped_Slide4.png) | 
| :---: |
| **Figure 3b** Elimination of state $u_1$ |
:::

:::{tab-item} 3c
| ![fig3c](/_static/lqr_control/Elimination/cropped_Slide5.png) | 
| :---: |
| **Figure 3c** Cost-to-go at $x_1$ is the sum of the two unary factors on $x_1$ (green) |
:::

:::{tab-item} 4a
| ![fig4a](/_static/lqr_control/Elimination/cropped_Slide6.png) | 
| :---: |
| **Figure 4a** Repeat elimination until the graph is reduced to a Bayes net |
:::

:::{tab-item} 4b
| ![fig4b](/_static/lqr_control/Elimination/cropped_Slide7.png) | 
| :---: |
| **Figure 4b** Repeat elimination until the graph is reduced to a Bayes net |
:::

:::{tab-item} 4c
| ![fig4c](/_static/lqr_control/Elimination/cropped_Slide8.png) | 
| :---: |
| **Figure 4c** Repeat elimination until the graph is reduced to a Bayes net |
:::

:::{tab-item} 4d
| ![fig4d](/_static/lqr_control/Elimination/cropped_Slide9.png) | 
| :---: |
| **Figure 4d** Completed Bayes net |
:::
::::

::::{tab-set}

:::{tab-item} Eliminate a State

## Eliminate a State

Let us start at the last state, $x_2$. Gathering the two factors (marked in
red in **Figure 2a**), we have {eq}`eq:potential` the objective function $\phi_1$, and {eq}`eq:constrain` the constraint equation on $x_2$, $u_1$ and $x_1$:

$$\phi_1(x_2) = x_2^T Q x_2 \label{eq:potential}$$

\begin{equation} x_2 = Ax_1 + Bu_1 \label{eq:constrain} \end{equation}

By substituting $x_2$ from the dynamics constraint {eq}`eq:constrain` into the objective function
{eq}`eq:potential`, we create a new factor representing
the cost of state $x_2$ as a function of $x_1$ and $u_1$:

\begin{equation} \phi_2(x_1, u_1) = (Ax_1 + Bu_1)^T Q (Ax_1 + Bu_1)
\label{eq:potential_simplified} \end{equation}

The resulting factor graph is illustrated in **Figure 2b**.  Note that the 
dynamics constraint is now represented by the bayes net factors shown as gray arrows.

To summarize, we used the dynamics constraint to eliminate variable
$x_2$ and the two factors marked in red, and we replaced them with a new binary cost factor on $x_1$
and $u_1$, marked in blue.

:::

:::{tab-item} Eliminate a Control

## Eliminate a Control

To eliminate $u_1$, we seek to replace the two factors marked red in **Figure 3a**
with a new cost factor on $x_1$ and an equation for the optimal control $u_1^*(x_1)$.

Adding the control cost to {eq}`eq:potential_simplified`, the combined cost of the
two red factors in **Figure 3a** is given by:

$$\phi_3(x_1, u_1) = u_1^TRu_1 + (Ax_1 + Bu_1)^T Q (Ax_1 + Bu_1)
\label{eq:potential_u1}$$

$\phi_3$ is sometimes referred to as the *optimal action value function* and we seek to minimize it over $u_1$.
We do so by
setting the derivative of {eq}`eq:potential_u1` wrt $u_1$ to zero yielding the expression for the optimal control input $u_1^*$ as 

$$\begin{align} 
u_1^*(x_1) &= \argmin\limits_{u_1}\phi_3(x_1, u_1) \nonumber \\
&= -(R+B^TQB)^{-1}B^TQAx_1 \label{eq:control_law} \\
&= K_1x_1 \nonumber
\end{align}$$

where $K_1\coloneqq -(R+B^TQB)^{-1}B^TQA$.

Finally, we substitute the expression of our optimal control, $u_1^* = K_1x_1$,
into our potential {eq}`eq:potential_u1` to obtain a new unary cost factor on $x_1$:

\begin{align}
    \phi_4(x_1) &= \phi_3(x_1, u_1^*(x_1)) \nonumber \\
        &= (K_1x_1)^T RK_1x_1 + (Ax_1 + BKx_1)^T Q (Ax_1 + BKx_1) \nonumber \\
        &= x_1^T(A^TQA-K_1^TB^TQA)x_1 \label{eq:potential_x1}
\end{align}
Note that we simplified $K_1^TRK_1 + K_1^TB^TQBK_1 = -K_1^TB^TQA$ by substituting in for $K_1$ using
{eq}`eq:control_law`.

The resulting factor graph is illustrated in **Figure 3b**.

For convenience, we will also define $P_k$ where $x_k^TP_kx_k$ represents the aggregate of the two unary costs on $x_k$.  In the case of $P_1$,
\begin{align}
    x_1^TP_1x_1 &= x_1^TQx_1 + \phi_4(x_1) \nonumber
\end{align}
is the aggregation of the two unary factors labeled in green in **Figure 3c**.

:::

:::{tab-item} Turning into a Bayes Network

## Turning into a Bayes Network
By eliminating all the variables from right to left, we can get a Bayes network
as shown in **Figure 4d**. Each time we eliminate a state
and control, we simply repeat the steps in **Eliminate a state** and **Eliminate a control**: we express the state $x_{k+1}$ with the dynamics model, then find the optimal control $u_k$ as
a function of state $x_k$.

Eliminating a general state, $x_{k+1}$, and control $u_k$, we obtain the recurrence relations:

\begin{equation} \boxed{K_k = -(R+B^TP_{k+1}B)^{-1}B^TP_{k+1}A} \label{eq:control_update_k} \end{equation}

\begin{equation} \boxed{P_k = Q+A^TP_{k+1}A - K_k^TB^TP_{k+1}A} \label{eq:cost_update_k} \end{equation}

with $P_{N}=Q$ is the cost at the last time step.

The final Bayes net in **Figure 4d** shows graphically the optimal control law:
\begin{equation} \boxed{u^*_k = K_k x_k} \end{equation}

:::
::::

# Intuition

```{figure} /_static/lqr_control/LQR_FGvsRicatti.png
:alt: Comparison between LQR control as solved by factor graphs and by the Ricatti Equation. (they are the same)
:width: 75%

**Figure 5:** Example LQR control solutions as solved by factor graphs (middle) and the traditional Discrete Algebraic Ricatti Equations (right).  The optimal control gains and cost-to-go factors are compared (left).  All plots show exact agreement between factor graph and Ricatti equation solutions.
```

We introduce the **cost-to-go** (also known as *return cost*, *optimal state value function*, or simply *value function*) as $V_k(x) \coloneqq x^TP_kx$ which intuitively represents *the total cost that will be accrued from here on out, assuming optimal control*.

In our factor graph representation, it is becomes obvious that $V_k(x)$ corresponds to the total cost at and after the state $x_k$ assuming optimal control because we eliminate variables backwards in time with the objective of minimizing cost.
Eliminating a state just re-expresses the future cost in terms of prior states/controls.  Each time we eliminate a control, $u$, the future cost is recalculated assuming optimal control (i.e. $\phi_4(x) = \phi_3(x, u^*)$).

This "cost-to-go" is depicted as a heatmap in **Figure 5**.
The heat maps depict the $V_k$ showing that the cost is high when $x$ is far from 0, but also showing that after iterating sufficient far backwards in time, $V_k(x)$ begins to converge.  That is to say, the $V_0(x)$ is very similar for $N=30$ and $N=100$.
Similarly, the leftmost plot of **Figure 5** depicts $K_k$ and $P_k$ and shows that they (predictably) converge as well.

This convergence allows us to see that we can extend to the [infinite horizon LQR problem](https://en.wikipedia.org/wiki/Linear%E2%80%93quadratic_regulator#Infinite-horizon,_discrete-time_LQR) (continued in the next section).

<!-- The factor graph representation also gives us insight to the equation for the optimal gain matrix $K_k$ from
\eqref{eq:control_update_k}.
The optimal control, $K_k$, should attempt to balance (a) the unary factor $u_k^TRu_k$ representing the cost of executing a control action and (b) the binary factor $(Ax_k+Bu_k)^TP_{k+1}(Ax_k+Bu_k)$ representing the future cost of the control action.

The binary factor consists of two terms
represents a balance between achieving a small "cost-to-go" next time step ($B^TP_{k+1}B$) and exerting a small
amount of control this time step ($R$). -->

# Equivalence to the Ricatti Equation

In traditional descriptions of discrete, finite-horizon LQR (i.e. [Chow](https://www.amazon.com/Analysis-Control-Dynamic-Economic-Systems/dp/0898749697), [Kirk](https://pdfs.semanticscholar.org/9777/06d1dc022280f47a2c67c646e85f38d88fe2.pdf#page=86), [Stanford](https://stanford.edu/class/ee363/lectures/dlqr.pdf)), the control law and cost function are given by

$$ u_k = K_kx_k $$

$$K_k = -(R+B^TP_{k+1}B)^{-1}B^TP_{k+1}A \label{eq:control_update_k_ricatti}$$

\begin{equation} P_k = Q+A^TP_{k+1}A - K_k^TB^TP_{k+1}A \label{eq:cost_update_k_ricatti} \end{equation}

with $P_k$ commonly referred to as the solution to the **dynamic Ricatti equation** and $P_N=Q$ is the
value of the Ricatti function at the final time step.
{eq}`eq:control_update_k_ricatti` and {eq}`eq:cost_update_k_ricatti` correspond to
the same results as we derived in {eq}`eq:control_update_k` and {eq}`eq:cost_update_k`
respectively.

Recall that $P_0$ and $K_0$ appear to converge as the number of time steps grows.  They will approach a stationary solution to the equations

\begin{align}
K &= -(R+B^TPB)^{-1}B^TPA \nonumber \\ 
P &= Q+A^TPA - K^TB^TPA \nonumber
\end{align}

as $N\to\infty$.  This is the [Discrete Algebraic Ricatti Equations (DARE)](https://en.wikipedia.org/wiki/Algebraic_Riccati_equation) and $\lim_{N\to\infty}V_0(x)$ and $\lim_{N\to\infty}K_0$ are the cost-to-go and optimal control gain respectively for the [infinite horizon LQR problem](https://en.wikipedia.org/wiki/Linear%E2%80%93quadratic_regulator#Infinite-horizon,_discrete-time_LQR).  Indeed, one way to calculate the solution to the DARE is to iterate on the dynamic Ricatti equation.

# Implementation using GTSAM
**Edit (Apr 17, 2021): Code updated to new Python wrapper as of GTSAM 4.1.0.

You can view an example Jupyter notebook on [google colab](https://colab.research.google.com/drive/1pIUC6fQVMEaQ7QfJk8BvD0F60gShj3F4#sandboxMode=true) or
<a href="/assets/code_samples/lqr_control.zip" download>download</a> the modules/examples
that you can use in your
projects to:

* Calculate the closed loop gain matrix, `K`, using GTSAM
* Calculate the "cost-to-go" matrix, `P` (which is equivalent to the solutions to
  the dynamic Ricatti equation), using GTSAM
* Calculate the LQR solution for a non-zero, non-constant goal position, using GTSAM
* Visualize the cost-to-go and how it relates to factor graphs and the Ricatti
  equation
* and more!

A brief example of the open-loop finite horizon LQR problem using
factor graphs is shown below:

```python
def solve_lqr(A, B, Q, R, X0=np.array([0., 0.]), num_time_steps=500):
    '''Solves a discrete, finite horizon LQR problem given system dynamics in
    state space representation.
    Arguments:
        A, B: nxn state transition matrix and nxp control input matrix
        Q, R: nxn state cost matrix and pxp control cost matrix
        X0: initial state (n-vector)
        num_time_steps: number of time steps, T
    Returns:
        x_sol, u_sol: Txn array of states and Txp array of controls
    '''
    n = np.size(A, 0)
    p = np.size(B, 1)

    # noise models
    prior_noise = gtsam.noiseModel.Constrained.All(n)
    dynamics_noise = gtsam.noiseModel.Constrained.All(n)
    q_noise = gtsam.noiseModel.Gaussian.Information(Q)
    r_noise = gtsam.noiseModel.Gaussian.Information(R)

    # Create an empty Gaussian factor graph
    graph = gtsam.GaussianFactorGraph()

    # Create the keys corresponding to unknown variables in the factor graph
    X = []
    U = []
    for k in range(num_time_steps):
        X.append(gtsam.symbol('x', k))
        U.append(gtsam.symbol('u', k))

    # set initial state as prior
    graph.add(X[0], np.eye(n), X0, prior_noise)

    # Add dynamics constraint as ternary factor
    #   A.x1 + B.u1 - I.x2 = 0
    for k in range(num_time_steps-1):
        graph.add(X[k], A, U[k], B, X[k+1], -np.eye(n),
                  np.zeros((n)), dynamics_noise)

    # Add cost functions as unary factors
    for x in X:
        graph.add(x, np.eye(n), np.zeros(n), q_noise)
    for u in U:
        graph.add(u, np.eye(p), np.zeros(p), r_noise)

    # Solve
    result = graph.optimize()
    x_sol = np.zeros((num_time_steps, n))
    u_sol = np.zeros((num_time_steps, p))
    for k in range(num_time_steps):
        x_sol[k, :] = result.at(X[k])
        u_sol[k] = result.at(U[k])
    
    return x_sol, u_sol
```

# Future Work
The factor graph **Figure 1** for our finite horizon discrete LQR problem can be readily extended to LQG, iLQR, DDP, and reinforcement
learning using non-deterministic dynamics factors, nonlinear factors, discrete factor graphs, and other features of GTSAM (stay tuned for future posts).

<hr />

<!-- ********************************** APPENDIX ********************************** -->
(appendix-target)=
# Appendix

<!-- ### Marginalization Cost on $x_1$
By substituting \eqref{eq:control_law} into \eqref{eq:potential_simplified}, we have the updated
potential function as a function of only $x_1$:
\\[ \begin{aligned} 
    \phi_1(x_1) &= x_1^T Q x_1 + (K_1x_1)^T RK_1x_1 + (Ax_1 + BKx_1)^T Q (Ax_1 + BKx_1) \\ 
    &= x_1^T(Q+ K_1^TRK_1 + A^TQA + K_1^TB^TQB - K_1^TB^TQA - A^TQBK_1)x_1  \\ 
    &= x_1^T[Q + A^TQA + K_1^T(R+B^TQB)K_1 - K_1^TB^TQA - A^TQBK_1]x_1 \\ 
    &= x_1^T(Q + A^TQA + A^TQBK_1 - K_1^TB^TQA - A^TQBK_1)x_1 \\ 
    &= x_1^T(Q + A^TQA - K_1^TB^TQA)x_1 
\end{aligned} \\] -->

## Least Squares Implementation in GTSAM
GTSAM can be specified to use either of two methods for solving the least squares problems that
appear in eliminating factor graphs: Cholesky Factorization or QR Factorization.  Both arrive at the same result, but we will take a look at QR since it more immediately illustrates the elimination algorithm at work.

<!-- plain table for formatting purposes -->
<style>
table, caption, tbody, tfoot, thead, table tr, table th, table tr:nth-child(even), td {
    margin: 0;
    padding: 0;
    border: 0;
    outline: 0;
    font-size: 100%;
    font-weight: normal;
    vertical-align: baseline;
    background: transparent;
    background-color: transparent;
}
table th {
    padding: 3px;
}
</style>

### QR Factorization

::::{tab-set}

:::{tab-item} 6a
```{math}
\begin{array}{cc} 
    \text{NM} & \text{Elimination Matrix} \\ 
    \left[ \begin{array}{c} 
        \vphantom{Q^{1/2} | } I\\ 
        \vphantom{I       | } 0\\ 
        \vphantom{R^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I\\ 
        \vphantom{-A      | } 0\\ 
        \vphantom{R^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I 
    \end{array} \right]
    &
    \left[ \begin{array}{ccccc|c} 
        Q^{1/2} &   &       &       &       & 0\\ 
        I & -B      & -A    &       &       & 0\\ 
          & R^{1/2} &       &       &       & 0\\ 
          &         & Q^{1/2}&      &       & 0\\ 
          &         & I     & -B    & -A    & 0\\ 
          &         &       & R^{1/2}&      & 0\\ 
          &         &       &       & Q^{1/2}& 0 
    \end{array} \right]
\end{array}
```

```{figure} /_static/lqr_control/Elimination/cropped_Slide0.png
:alt: factor graph partially eliminated

**Figure 6a** Initial factor graph and elimination matrix
```
:::

:::{tab-item} 6b
```{math}
\begin{array}{cc} 
    \text{NM} & \text{Elimination Matrix} \\ 
    \begin{bmatrix} 
        \vphantom{Q^{1/2} | } I\\ 
        \vphantom{I       | } 0\\ 
        \vphantom{R^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I\\ 
        \vphantom{I       | } 0\\ 
        \vphantom{R^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I
    \end{bmatrix}
    & 
    \left[ \begin{array}{ccccc|c} 
        \textcolor{red}{Q^{1/2}} &   &       &       &       & 0\\ 
        \textcolor{red}{I} & \textcolor{red}{-B} & \textcolor{red}{-A} &       &       & 0\\ 
          & R^{1/2} &       &       &       & 0\\ 
          &         & Q^{1/2} &      &       & 0\\ 
          &         & I     & -B    & -A    & 0\\ 
          &         &       & R^{1/2} &      & 0\\ 
          &         &       &       & Q^{1/2} & 0 
    \end{array} \right]
\end{array}
```

```{figure} /_static/lqr_control/Elimination/cropped_Slide1.png
:alt: factor graph partially eliminated

**Figure 6b** Eliminate $x_2$: the two factors to replace are highlighted in red
```
:::

:::{tab-item} 6c
$$ \begin{array}{cc} 
    \text{NM} & \text{Elimination Matrix} \\ 
    \begin{bmatrix} 
        \vphantom{I       | } 0\\ 
        \vphantom{Q^{1/2} | } I\\ 
        \vphantom{R^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I\\ 
        \vphantom{I       | } 0\\ 
        \vphantom{R^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I\\ 
    \end{bmatrix} & 
    \left[ \begin{array}{c:cccc|c} 
        I & -B      & -A    &       &       & 0\\ 
        \hdashline 
          & \color{blue} {Q^{1/2}B} & \color{blue} {Q^{1/2}A} &      &       & 0\\ 
          & R^{1/2} &       &       &       & 0\\ 
          &                     & Q^{1/2}&      &       & 0\\ 
          &                     & I     & -B    & -A    & 0\\ 
          &                     &       & R^{1/2}&      & 0\\ 
          &                     &       &       & Q^{1/2}& 0 
    \end{array} \right]
    \end{array}
$$
```{figure} /_static/lqr_control/Elimination/cropped_Slide2.png
:alt: factor graph partially eliminated

**Figure 6c** Eliminated $x_2$: the resulting binary cost factor is highlighted in blue
```
:::

:::{tab-item} 6d
$$ \begin{array}{cc} 
    \text{NM} & \text{Elimination Matrix} \\ 
    \begin{bmatrix} 
        \vphantom{I       | } 0\\ 
        \vphantom{Q^{1/2} | } I\\ 
        \vphantom{R^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I\\ 
        \vphantom{I       | } 0\\ 
        \vphantom{R^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I\\ 
    \end{bmatrix} & 
    \left[ \begin{array}{c:cccc|c} 
        I & -B      & -A    &       &       & 0\\ 
        \hdashline 
          & \color{red} {Q^{1/2}B} & \color{red} {Q^{1/2}A} &      &       & 0\\ 
          & \color{red} {R^{1/2}} &       &       &       & 0\\ 
          &                     & {Q^{1/2}} &      &       & 0\\ 
          &                     & I     & -B    & -A    & 0\\ 
          &                     &       & R^{1/2}&      & 0\\ 
          &                     &       &       & Q^{1/2}& 0 
    \end{array} \right]
    \end{array} $$
```{figure} /_static/lqr_control/Elimination/cropped_Slide3.png
:alt: factor graph partially eliminated

**Figure 6d** Eliminate $u_1$: the two factors to replace are highlighted in red
```
:::

:::{tab-item} 6e
$$ \begin{array}{cc} 
    \text{NM} & \text{Elimination Matrix} \\ 
    \begin{bmatrix} 
        \vphantom{I       | } 0\\ 
        \vphantom{D_1^{1/2} | } I\\ 
        \vphantom{(P_1-Q)^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I\\ 
        \vphantom{I       | } 0\\ 
        \vphantom{R^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I\\ 
    \end{bmatrix} & 
    \left[ \begin{array}{cc:ccc|c} 
        I & -B      & -A    &       &       & 0\\ 
          & D_1^{1/2} & -D_1^{1/2}K_1 &      &       & 0\\ 
          \hdashline 
          &         & \color{blue} {(P_1-Q)^{1/2}} &      &       & 0\\ 
          &         & Q^{1/2} &      &       & 0\\ 
          &         & I     & -B    & -A    & 0\\ 
          &         &       & R^{1/2}&      & 0\\ 
          &         &       &       & Q^{1/2}& 0 
    \end{array} \right]
    \end{array} $$
```{figure} /_static/lqr_control/Elimination/cropped_Slide4.png
:alt: factor graph partially eliminated

**Figure 6e** Eliminated $u_1$: the resulting unary cost factor on $x_1$ is shown in blue
```
:::

:::{tab-item} 6f
$$ \begin{array}{cc} 
    \text{NM} & \text{Elimination Matrix} \\ 
    \begin{bmatrix} 
        \vphantom{I       | } 0\\ 
        \vphantom{D_1^{1/2} | } I\\ 
        \vphantom{(P_1-Q)^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I\\ 
        \vphantom{I       | } 0\\ 
        \vphantom{R^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I\\ 
    \end{bmatrix} & 
    \left[ \begin{array}{cc:ccc|c} 
        I & -B      & -A    &       &       & 0\\ 
          & D_1^{1/2} & -D_1^{1/2}K_1 &      &       & 0\\ 
          \hdashline 
          &         & \color{red} {(P_1-Q)^{1/2}} &      &       & 0\\ 
          &         & \color{red} {Q^{1/2}} &      &       & 0\\ 
          &         & \color{red} I     & \color{red} {-B}    & \color{red} {-A}    & 0\\ 
          &         &       & R^{1/2}&      & 0\\ 
          &         &       &       & Q^{1/2}& 0 
    \end{array} \right]
    \end{array} $$
```{figure} /_static/lqr_control/Elimination/cropped_Slide6.png
:alt: factor graph partially eliminated

**Figure 6f** Eliminate $x_1$: the three factors to replace are highlighted in red
```
:::

:::{tab-item} 6g
$$ \begin{array}{cc} 
    \text{NM} & \text{Elimination Matrix} \\ 
    \begin{bmatrix} 
        \vphantom{I       | } 0\\ 
        \vphantom{D_1^{1/2}K_1 | } I\\ 
        \vphantom{I       | } 0\\ 
        \vphantom{D_0^{1/2} | } I\\ 
        \vphantom{P^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I\\ 
    \end{bmatrix} & 
    \left[ \begin{array}{ccc:cc|c} 
        I & -B      & -A    &       &       & 0\\ 
          & D_1^{1/2} & -D_1^{1/2}K_1&      &       & 0\\ 
          &         & I     & -B    & -A    & 0\\ 
          \hdashline 
          &         &       &\color{blue} {P_1^{1/2}B} & \color{blue} {P_1^{1/2}A} & 0\\ 
          &         &       & R^{1/2}&      & 0\\ 
          &         &       &       & Q^{1/2}& 0 
    \end{array} \right]
    \end{array} $$
```{figure} /_static/lqr_control/Elimination/cropped_Slide7.png
:alt: factor graph partially eliminated

**Figure 6g** Eliminated $x_1$: the resulting binary cost factor is shown in blue
```
:::

:::{tab-item} 6h
$$ \begin{array}{cc} 
    \text{NM} & \text{Elimination Matrix} \\ 
    \begin{bmatrix} 
        \vphantom{I       | } 0\\ 
        \vphantom{D_1^{1/2}K_1 | } I\\ 
        \vphantom{I       | } 0\\ 
        \vphantom{D_0^{1/2} | } I\\ 
        \vphantom{P^{1/2} | } I\\ 
        \vphantom{Q^{1/2} | } I\\ 
    \end{bmatrix} & 
    \left[ \begin{array}{ccc:cc|c} 
        I & -B      & -A    &       &       & 0\\ 
          & D_1^{1/2} & -D_1^{1/2}K_1&      &       & 0\\ 
          &         & I     & -B    & -A    & 0\\ 
          \hdashline 
          &         &       &\color{red} {P_1^{1/2}B} &\color{red} {P_1^{1/2}A} & 0\\ 
          &         &       &\color{red} {R^{1/2}} &      & 0\\ 
          &         &       &       & Q^{1/2} & 0 
    \end{array} \right]
    \end{array} $$
```{figure} /_static/lqr_control/Elimination/cropped_Slide8.png
:alt: factor graph partially eliminated

**Figure 6h** Eliminate $u_0$: the two cost factors to replace are shown in red
```
:::

:::{tab-item} 6i
$$ \begin{array}{cc} 
    \text{NM} & \text{Elimination Matrix} \\ 
    \begin{bmatrix} 
        \vphantom{I       | } 0\\ 
        \vphantom{D_1^{1/2}K_1 | } I\\ 
        \vphantom{I       | } 0\\ 
        \vphantom{D_0^{1/2} | } I\\ 
        \vphantom{(P_0-Q)^{1/2} | } I\\ 
        \vphantom{P^{1/2} | } I\\ 
    \end{bmatrix} & 
    \left[ \begin{array}{cccc:c|c} 
        I & -B      & -A    &       &       & 0\\ 
          & D_1^{1/2} & -D_1^{1/2}K_1 &      &       & 0\\ 
          &         & I     & -B    & -A    & 0\\ 
          &         &       & D_0^{1/2}  & -D_0^{1/2}K_0 & 0\\ 
          \hdashline 
          &         &   &      & \color{blue} {(P_0-Q)^{1/2}} & 0\\ 
          &         &   &      & Q^{1/2}                    & 0\\ 
    \end{array} \right]
    \end{array} $$
```{figure} /_static/lqr_control/Elimination/cropped_Slide9.png
:alt: factor graph partially eliminated

**Figure 6i** Eliminated $u_0$: the resulting unary cost factor on $x_0$ is shown in blue.
```
:::

:::{tab-item} 6j
$$ \begin{array}{cc} 
    \text{NM} & \text{Elimination Matrix} \\ 
    \begin{bmatrix} 
        \vphantom{I       | } 0\\ 
        \vphantom{D_1^{1/2}K_1 | } I\\ 
        \vphantom{I       | } 0\\ 
        \vphantom{D_0^{1/2} | } I\\ 
        \vphantom{(P_0-Q)^{1/2} | } I\\ 
        \vphantom{P^{1/2} | } I\\ 
    \end{bmatrix} & 
    \left[ \begin{array}{cccc:c|c} 
        I & -B      & -A    &       &       & 0\\ 
          & D_1^{1/2} & -D_1^{1/2}K_1 &      &       & 0\\ 
          &         & I     & -B    & -A    & 0\\ 
          &         &       & D_0^{1/2}  & -D_0^{1/2}K_0 & 0\\ 
          \hdashline 
          &         &   &      & \color{red} {(P_0-Q)^{1/2}} & 0\\ 
          &         &   &      & \color{red} {Q^{1/2}}                    & 0\\ 
    \end{array} \right]
    \end{array} $$
```{figure} /_static/lqr_control/Elimination/cropped_Slide10.png
:alt: factor graph partially eliminated

**Figure 6j** Eliminate $x_0$: the final two factors to eliminate are shown in red.
```
:::

:::{tab-item} 6k
$$ \begin{array}{cc} 
    \text{NM} & \text{Elimination Matrix} \\ 
    \begin{bmatrix} 
        \vphantom{I       | } 0\\ 
        \vphantom{D_1^{1/2}K_1 | } I\\ 
        \vphantom{I       | } 0\\ 
        \vphantom{D_0^{1/2} | } I\\ 
        \vphantom{P_0^{1/2} | } I\\ 
    \end{bmatrix} & 
    \left[ \begin{array}{cccc:c|c} 
        I & -B      & -A    &       &       & 0\\ 
          & D_1^{1/2} & -D_1^{1/2}K_1 &      &       & 0\\ 
          &         & I     & -B    & -A    & 0\\ 
          &         &       & D_0^{1/2}  & -D_0^{1/2}K_0 & 0\\ 
          \hdashline 
          &         &   &      & \color{blue} {P_0^{1/2}} & 0\\ 
    \end{array} \right]
    \end{array} $$
```{figure} /_static/lqr_control/Elimination/cropped_Slide11.png
:alt: factor graph partially eliminated

**Figure 6k** Final result: after eliminating $x_0$, the elimination matrix is upper-triangular and we can read off the control laws.
```
:::

::::

```{math}
\begin{aligned}
    &\text{where} \quad P_k &=& Q + A^T P_{k+1} A - K_k^T B^T P_{k+1} A, \quad (P_2 = Q) \\
    &D_k &=& R + B^T P_{k+1} B \\
    &K_k &=& -D_k^{-1/2} (R + B^T P_{k+1} B)^{-T/2} B^T P_{k+1} A \\
    &&=& -(R + B^T P_{k+1} B)^{-1} B^T P_{k+1} A
\end{aligned}
```

<!-- ************************ end QR block elimination ************************ -->
  
<br />

The factorization process is illustrated in **Figure 6** for a 3-time step factor graph, where the noise matrices and elimination
matrices are shown with the corresponding states of the graph.  The noise matrix (NM) is $0$ for a
hard constraint and $I$ for a minimization objective.  The elimination matrix is formatted as an
augmented matrix $[A|b]$ for the linear least squares problem $\argmin\limits_x\|\|Ax-b\|\|_2^2$
with ${x=[x_2;u_1;x_1;u_0;x_0]}$ is the vertical concatenation of all state and control vectors.
The recursive expressions for $P$, $D$, and $K$ when eliminating control variables (i.e. $u_1$ in **Figure 6e**) are derived from block QR Factorization.

Note that all $b_i=0$ in the augmented matrix for the LQR problem of finding minimal control to
reach state $0$, but simply changing values of $b_i$ intuitively extends GTSAM to solve
LQR problems whose objectives are to reach different states or even follow trajectories.

<!-- ### Final Symbolic Expressions of Factor Graph Evaluation
In the above solution, we have
\\[ \begin{aligned} 
K_1 &= -(R+B^TQB)^{-1}B^TQA\\ 
P_1 &= Q+A^TQA + A^TQBK_1\\ 
K_0 &= -(R+B^TV_1B)^{-1}B^TV_1A\\ 
P_0 &= Q + A^T V_1 A + A^T V_1 B K_0
\end{aligned} \\]

In general, the above factor graph and solution method can be expanded for an arbitrary number of time steps, $T$, arising in the iterative equations
\\[ \begin{aligned} 
    V_T &= Q \\ 
    K_t &= -( R + B^T V_{t+1} B )^{-1} B^T V_{t+1} A \\ 
    P_t &= Q + A^T V_{t+1} A + A^T V_{t+1} B K_t 
\end{aligned} \\]
and
\\[ \begin{aligned} 
    u_t &= K_t x_t
\end{aligned} \\]
which match the traditional algorithm using the Ricatti Equation for solving the finite-horizon discrete-time LQR problem.  As the number
of time steps grows, the solution for $V_0$ approaches the stationary solution to the algebraic
Ricatti equation and the solution for $K_0$ approaches the solution to the infinite-horizon
discrete-time LQR problem. -->

<!-- **************** JAVASCRIPT FOR SLIDESHOWS **************** -->
<script>
    var slideIndex = [1,1];
    showSlides(slideIndex[0], 0);
    showSlides(slideIndex[1], 1);

    // Next/previous controls
    function plusSlides(n, which) {
        showSlides(slideIndex[which] += n, which);
    }

    // Thumbnail image controls
    function currentSlide(n, which) {
        showSlides(slideIndex[which] = n, which);
    }

    // change image/slide
    function showSlides(n, which, triggeredByScroll) {
        var i;
        var slides = document.getElementsByClassName("mySlides "+which);
        var dots = document.getElementsByClassName("dot "+which);
        if (n > slides.length) {slideIndex[which] = 1}
        if (n < 1) {slideIndex[which] = slides.length}
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }
        for (i = 0; i < dots.length; i++) {
            dots[i].className = dots[i].className.replace(" active", "");
        }
        slides[slideIndex[which]-1].style.display = "block";
        dots[slideIndex[which]-1].className += " active";

        if (which==1){
            return
        }

        // when image changes, also scroll to the correct subsection in "Variable Elimination"
        var scrollable = document.getElementById("sec:elim_scrollable");
        var scrollLoc_state = document.getElementById("sec:elim_state").offsetTop - scrollable.offsetTop;
        var scrollLoc_ctrl = document.getElementById("sec:elim_ctrl" ).offsetTop - scrollable.offsetTop;
        var scrollLoc_bayes = document.getElementById("sec:elim_bayes").offsetTop - scrollable.offsetTop;
        var scroll_cur = scrollable.scrollTop;
        var scrollLoc;
        var div_state = document.getElementById("sec:elim_state_div");
        var div_ctrl = document.getElementById("sec:elim_ctrl_div");
        var div_bayes = document.getElementById("sec:elim_bayes_div");
        switch(slideIndex[which]) {
            case 1:
            case 2:
                div_state.style.display = "block";
                div_ctrl.style.display = "none";
                div_bayes.style.display = "none";
                // fadeIn(div_state);
                // fadeOut(div_ctrl, div_state);
                // fadeOut(div_bayes, div_state);
                return;
            case 3:
            case 4:
            case 5:
                div_state.style.display = "none";
                div_ctrl.style.display = "block";
                div_bayes.style.display = "none";
                // fadeOut(div_state, div_ctrl);
                // div_state.classList.toggle('hide');
                // fadeIn(div_ctrl);
                // fadeOut(div_bayes, div_ctrl);
                return;
            case 6:
            case 7:
            case 8:
            case 9:
                div_state.style.display = "none";
                div_ctrl.style.display = "none";
                div_bayes.style.display = "block";
                // fadeOut(div_state, div_bayes);
                // fadeOut(div_ctrl, div_bayes);
                // fadeIn(div_bayes);
                return;
        }
    }

    // // when scrolling through subsections in "Variable Elimination", also change the image to correspond
    // document.getElementById("sec:elim_scrollable").addEventListener("scroll", function (event) {
    //     var scrollable = document.getElementById("sec:elim_scrollable");
    //     var scrollLoc_state = document.getElementById("sec:elim_state").offsetTop - scrollable.offsetTop;
    //     var scrollLoc_ctrl = document.getElementById("sec:elim_ctrl" ).offsetTop - scrollable.offsetTop;
    //     // var scrollLoc_value = document.getElementById("sec:elim_value").offsetTop - scrollable.offsetTop;
    //     var scrollLoc_bayes = document.getElementById("sec:elim_bayes").offsetTop - scrollable.offsetTop;
        
    //     var scroll = this.scrollTop;
    //     if (scroll < scrollLoc_ctrl) {
    //         if (slideIndex[0] > 2) {showSlides(slideIndex[0]=1, 0, true)}
    //     }
    //     // else if (scroll < scrollLoc_value) {
    //     //     if ((slideIndex[0] < 3) || (slideIndex[0] > 4)) {showSlides(slideIndex[0]=3, 0, true)}
    //     // }
    //     else if ((scroll < scrollLoc_bayes) && (scroll < (scrollable.scrollHeight - scrollable.offsetHeight))) {
    //         if ((slideIndex[0] < 3) || (slideIndex[0] > 3)) {showSlides(slideIndex[0]=3, 0, true)}
    //     }
    //     else {
    //         if ((slideIndex[0] < 6)) {showSlides(slideIndex[0]=6, 0, true)}
    //     }
    // });

    function fadeOut(element, nextElement) {
        if (element.style.display == "none") {
            return;
        }
        element.addEventListener('webkitTransitionEnd', function () {
            element.style.display = "none";
            nextElement.style.display = "block";
        }, {once: true});
        element.addEventListener('mozTransitionEnd', function () {
            element.style.display = "none";
            nextElement.style.display = "block";
        }, {once: true});
        element.addEventListener('oTransitionEnd', function () {
            element.style.display = "none";
            nextElement.style.display = "block";
        }, {once: true});
        element.addEventListener('transitionend', function () {
            element.style.display = "none";
            nextElement.style.display = "block";
        }, {once: true});
        element.style.webkitTransitionDuration = "0.1s";
        element.style.mozTransitionDuration = "0.1s";
        element.style.oTransitionDuration = "0.1s";
        element.style.transitionDuration = "0.1s";
        element.style.opacity = "0";
    }
    function fadeIn(element) {
        if (element.style.display == "block") {
            return;
        }
        element.addEventListener('webkitTransitionEnd', function () {
        }, {once: true});
        element.addEventListener('mozTransitionEnd', function () {
        }, {once: true});
        element.addEventListener('oTransitionEnd', function () {
        }, {once: true});
        element.addEventListener('transitionend', function () {
        }, {once: true});
        element.style.webkitTransitionDuration = "0.1s";
        element.style.mozTransitionDuration = "0.1s";
        element.style.oTransitionDuration = "0.1s";
        element.style.transitionDuration = "0.1s";
        element.style.webkitTransitionDelay = "0.1s";
        element.style.mozTransitionDelay = "0.1s";
        element.style.oTransitionDelay = "0.1s";
        element.style.transitionDelay = "0.1s";
        element.style.opacity = "1";
    }
</script>