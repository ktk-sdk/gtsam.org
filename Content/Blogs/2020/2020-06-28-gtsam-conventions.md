---
title:  Geometry and Variable Naming Conventions
date:   2020-06-28
authors:
  - name: Samarth Brahmbhatt
    url: https://samarth-robo.github.io
intro:  "A practical guide to naming geometric variables in GTSAM code. \n\n*(Aligning naming conventions like `wTc` and `cX` with textbook notation makes coordinate transforms and pose compositions easier to read and less error‑prone.)*"
---

I am a post-doc at [Intel ISL](https://vladlen.info). In my
[PhD work](https://contactpose.cc.gatech.edu), I used GTSAM for object pose
estimation and 3D reconstruction of hand joints to study hand-object interaction.
I love GTSAM for its ability to optimize geometric quantities and deal with
uncertainty in observations. However, it is easy to get lost in the web of
inverse transformations while optimizing complex geometric systems. I've found 
that naming code variables consistently with textbook notation conventions can
help mitigate this. This post describes some suggestions for doing that.

# Points
- Always name your 3D points like how you would on paper. A point $^{c}X$ in the
camera coordinate system $c$ is named `cX`.
- 3D points use uppercase letters, 2D points use lowercase letters.

# Pose
Name your pose variables like how you would write them on paper.
The pose $^wT_c$ of camera coordinate frame $c$ in the world coordinate frame
$w$ is named `wTc`. In GTSAM jargon, `c` is the **pose coordinate** frame,
and `w` is the **world coordinate** frame.

# Composing Poses
Math: $^oT_c =~^oT_w~\cdot~^wT_c$.

```{code}cpp
:caption: GTSAM code
Pose3 oTw = Pose3(...);
Pose3 wTc = Pose3(...);
Pose3 oTc = oTw * wTc;
// same as Pose3 oTc = oTw.compose(wTc);
```

# Transforming Points *from* Pose Coordinates
This operation uses the camera pose in the world coordinate frame
($^wT_c$) to bring points from the camera coordinate frame ($^c\tilde{\mathbf{X}}$) to
the world coordinate frame ($^w\tilde{\mathbf{X}}$).

Math: $^w\tilde{\mathbf{X}} =~^wT_c~\cdot~^c\tilde{\mathbf{X}}$

```{code}cpp
:caption: GTSAM code
Point3 wX = wTc.transformFrom(cX);
// same as Point3 wX = wTc * cX;
```

# Transforming Points *to* Pose Coordinates
This operation uses the inverse of the camera pose $\left(^wT_c\right)^{-1}$
to bring points from the world coordinate frame ($^w\tilde{\mathbf{X}}$) to
the camera coordinate frame ($^c\tilde{\mathbf{X}}$).

Math: $^c\tilde{\mathbf{X}} =~\left(^wT_c\right)^{-1}~\cdot~^w\tilde{\mathbf{X}}$

```{code}cpp
:caption: GTSAM code
Point3 cX = wTc.transformTo(wX);
```

# Cameras
The GTSAM pinhole camera classes
(e.g. [`PinholeBase`](https://github.com/borglab/gtsam/blob/develop/gtsam/geometry/CalibratedCamera.cpp))
internally use `transformTo()` to transform 3D points into the camera
coordinates, so you should use the pose of the camera w.r.t. world while
constructing the object:

```cpp
Pose3 wTc = Pose3(...);
SimpleCamera cam(wTc, K);
```
now you can use `cam` in the `TriangulationFactor` for example. Other factors
like the
[`GenericProjectionFactor`](https://github.com/borglab/gtsam/blob/develop/gtsam/slam/ProjectionFactor.h)
also use the same convention:

$$
\begin{align*}
^{sensor}\tilde{\mathbf{X}}
&=~^{sensor}T_{world}~\cdot~^{world}\tilde{\mathbf{X}}\\
&=~^{sensor}T_{body}~\cdot~^{body}T_{world}~\cdot~^{world}\tilde{\mathbf{X}}\\
&= \left(^{world}T_{body}~\cdot~^{body}T_{sensor}\right)^{-1}~\cdot~^{world}\tilde{\mathbf{X}}
\end{align*}
$$

**Example**: In a mobile robot SLAM scenario, wheel odometry might tell you where
the robot body is in the world ($^{world}T_{body}$), and the robot URDF spec
might tell you where the camera is on the robot body ($^{body}T_{sensor}$).
Together, these allow you to situate camera observations in the world coordinate
frame.

```{code}cpp
:caption: GTSAM code
Pose3 body_T_sensor = ...
Point2 sensor_p = ...  // 2D point in the image
// in the following factor,
// Symbol('T', i) is world_T_body for the i'th frame
// Symbol('X', j) is the j'th 3D point in world coordinates i.e. world_Xj
auto f = GenericProjectionFactor<Pose3, Point3, Cal3_S2>(sensor_p, noise, Symbol('T', i), Symbol('X', j), K, body_T_sensor);
```
It will project the world 3D point $^{world}\tilde{\mathbf{X}}$ into the sensor coordinates like so:
```cpp
Pose3 world_T_sensor = world_T_body * body_T_sensor;
Point3 sensor_X = world_T_sensor.transformTo(world_X);
```
and then project it to the image using instrinsics and then compare it to the detection `sensor_p`.