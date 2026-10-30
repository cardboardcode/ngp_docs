# Getting Started 🚀

This guide walks you through setting up a development environment, building the
`next_gen_prototype` workspace, running its automated integration tests, and
launching the interactive web demonstration.

:::{warning}
`next_gen_prototype` is a project under construction — these instructions are
likely to **change rapidly**.
:::

## Prerequisites

| Dependency        | Notes                                                            |
|:----------------- |:-----------------------------------------------------------------|
| **ROS 2 Jazzy Jalisco**   | [Ubuntu install (debs)](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html), including the [development tools](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html#install-development-tools-optional) |
| **Rust**          | The latest stable toolchain (managed by `rustup`)                |
| **colcon + Cargo** | `python3-colcon-cargo`, `colcon-ros-cargo`, `cargo-ament-build`  |

## Instructions 📘

```{code-block} bash
:caption: Create and enter the distrobox container

    distrobox create --image ghcr.io/open-rmf/ros2_rust_base:jazzy -n ros2_rust_base
    distrobox enter ros2_rust_base
```

:::{danger}
If `colcon build` fails with a missing Cargo toolchain error, double-check that
`rustc` and `cargo` are on your `PATH` (`rustup show`), and that the
colcon ↔ Cargo bridge packages from Step 1 were installed successfully.
:::

:::{seealso}
Stuck somewhere? Please open an
[issue on the repository](https://github.com/open-rmf/next_gen_prototype/issues)
or post to the
[Open-RMF ideas board](https://discourse.ros.org/c/open-rmf/open-rmf-ideas/105)
on Discourse.
:::
