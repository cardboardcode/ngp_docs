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

We provide a pre-built base image (`ros2_rust_base`) that bundles **all**
dependencies. Bring it up with `rocker`, `distrobox`, `podman`, or any other
OCI-compliant tool — the example below uses [`distrobox`](https://github.com/containers/distrobox):

```{code-block} bash
:caption: Create and enter the distrobox container

    distrobox create --image ghcr.io/open-rmf/ros2_rust_base:jazzy -n ros2_rust_base
    distrobox enter ros2_rust_base
```

:::{note}
From this point on, **all commands must be run inside the container** (or on
your local system, if you chose Method 1).
:::

## 2. Import workspace dependencies

Create a fresh ROS 2 workspace and clone the repository into it:

```{code-block} bash
:caption: Create the workspace and clone next_gen_prototype

    mkdir -p rmf_ws/src
    cd rmf_ws/src
    git clone https://github.com/open-rmf/next_gen_prototype.git
    cd ..
```

The workspace layout now looks like this:

```
rmf_ws/
├── build/        ← (created by colcon)
├── install/      ← (created by colcon)
└── src/
    └── next_gen_prototype/
```

## 3. Install ROS package dependencies

```{code-block} bash
:caption: Resolve and install all rosdep keys
:emphasize-lines: 1
:linenos:

    rosdep update
    rosdep install --from-paths src --ignore-src --rosdistro jazzy -yr
```

## 4. Build the workspace

Make sure you are at the **workspace root** (i.e. inside `rmf_ws/`), then build:

```{code-block} bash
:caption: Build all packages in the workspace

    source /opt/ros/jazzy/setup.bash
    colcon build
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
