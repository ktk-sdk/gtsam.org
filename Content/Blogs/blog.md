# Blogs

## 2023
::::{grid} 1 1 2 2

:::{card}
:link: .//2023/2023-02-04-lost-triangulation.ipynb
:header: February 4
:footer: Akshay Krishnan, Sebastien Henry, Frank Dellaert, John Christian

[**LOST in Triangulation**](.//2023/2023-02-04-lost-triangulation.ipynb)

Introduces the triangulation problem and some commonly used solutions (both optimal and sub-optimal), along with GTSAM code examples.

Reviews the recently proposed **linear optimal sine triangulation method (LOST)**, comparing its performance to other methods.
:::


::::

<br><br>

## 2021
::::{grid} 1 1 2 2

:::{card}
:link: .//2021/2021-02-23(3)-uncertainties-part3.md
:header: February 23
:footer: Matias Mattamala

[**Reducing the uncertainty about the uncertainties, part 3: Adjoints and covariances**](.//2021/2021-02-23(3)-uncertainties-part3.md)

Presents methods for transforming covariances on Lie groups using **adjoint mappings**.

Explains how to consistently propagate uncertainty through **nonlinear transformations**, with a focus on pose estimation in $SE(3)$.
:::


:::{card}
:link: .//2021/2021-02-23(2)-uncertainties-part2.md
:header: February 23
:footer: Matias Mattamala

[**Reducing the uncertainty about the uncertainties, part 2: Frames and manifolds**](.//2021/2021-02-23(2)-uncertainties-part2.md)

Extends uncertainty modeling from vector spaces to **manifold-valued variables** such as rotations and poses.

Discusses the importance of **reference frames**, **retraction maps**, and how to define and interpret covariances on nonlinear spaces.
:::


:::{card}
:link: .//2021/2021-02-23(1)-uncertainties-part1.md
:header: February 23
:footer: Matias Mattamala

[**Reducing the uncertainty about the uncertainties, part 1: Linear and nonlinear**](.//2021/2021-02-23(1)-uncertainties-part1.md)

An in-depth look at how we handle uncertainty in optimization-based state estimation, starting from linear models then progressing into the nonlinear world.

Explores how factor graphs encode uncertainty through **covariance matrices** and what it *really* means to solve them—not just for the best estimate, but also for a measure of confidence.
:::


::::

<br><br>

## 2020
::::{grid} 1 1 2 2

:::{card}
:link: .//2020/2020-08-30-Laplacian.md
:header: August 30
:footer: Frank Dellaert

[**Mount Rainier's Eigenvectors**](.//2020/2020-08-30-Laplacian.md)

This post reconstructs Mount Rainier’s elevation from a top-down photo using relative measurements!

It connects the Hessian of the estimation problem with the **Graph Laplacian**, revealing how eigen decomposition provides insight into global structure and uncertainty.
:::


:::{card}
:link: .//2020/2020-07-16-new-release-gtsam.md
:header: July 16
:footer: Fan Jiang

[**Releasing GTSAM 4.0.3**](.//2020/2020-07-16-new-release-gtsam.md)

**GTSAM 4.0.3** introduces key improvements, including a switch to the $SE(3)$ exponential map for `Pose3` retraction—boosting convergence for poorly initialized problems.

This release also includes robust noise models, Python and Windows enhancements, bug fixes, and performance gains.
:::


:::{card}
:link: .//2020/2020-06-28-gtsam-conventions.md
:header: June 28
:footer: Samarth Brahmbhatt

[**Geometry and Variable Naming Conventions**](.//2020/2020-06-28-gtsam-conventions.md)

A practical guide to naming geometric variables in GTSAM code. 

*(Aligning naming conventions like `wTc` and `cX` with textbook notation makes coordinate transforms and pose compositions easier to read and less error‑prone.)*
:::


:::{card}
:link: .//2020/2020-06-01-factor-graphs.md
:header: June 1
:footer: Frank Dellaert

[**What are Factor Graphs?**](.//2020/2020-06-01-factor-graphs.md)

**Factor graphs** are powerful graphical models representing variables and constraints in estimation problems, and are the foundation of GTSAM's optimization.

Here we explain their structure and follow some of their applications in the robotics domain.
:::


::::

<br><br>

## 2019
::::{grid} 1 1 2 2

:::{card}
:link: .//2019/2019-11-07-lqr-control.md
:header: November 7
:footer: Gerry Chen, Yetong Zhang, Frank Dellaert

[**LQR Control Using Factor Graphs**](.//2019/2019-11-07-lqr-control.md)

Demonstrates how to frame Linear Quadratic Regulator (LQR) control problems as factor graphs, enabling efficient optimization techniques borrowed from SLAM and sensor fusion to solve classic control tasks.
:::


:::{card}
:link: .//2019/2019-09-20-robust-noise-model.md
:header: September 20
:footer: Varun Agrawal

[**Look Ma, No RANSAC**](.//2019/2019-09-20-robust-noise-model.md)

Discover how robust error models can reduce the need for RANSAC in parameter estimation by down-weighting outliers directly—yielding estimates that match or exceed RANSAC results (even with 2:1 outlier ratios!)
:::


:::{card}
:link: .//2019/2019-09-18_legged-robot-factors-part-I.md
:header: September 18
:footer: Ross Harley

[**Legged Robot Factors**](.//2019/2019-09-18_legged-robot-factors-part-I.md)

Outlines how GTSAM can be extended with custom factors tailored for **legged robot dynamics**, laying the groundwork for efficient state estimation in bipedal or quadrupedal locomotion.
:::


:::{card}
:link: .//2019/2019-05-20_gtsam-org.md
:header: May 20

[**Launching gtsam.org**](.//2019/2019-05-20_gtsam-org.md)

Announcing GTSAM’s official website built on GitHub Pages with **Jekyll**!
:::


:::{card}
:link: .//2019/2019-05-18_moving-to-github.md
:header: May 18

[**Moving to Github!**](.//2019/2019-05-18_moving-to-github.md)

GTSAM transitions from Bitbucket to GitHub, embracing open-source collaboration with free CI, enhanced community tools, and broader visibility—ushering in a new era of development and engagement.
:::


::::

<br><br>

