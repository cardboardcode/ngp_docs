---
orphan: true
---

# Layered Map Server Demos

This tutorial walks through three progressive demonstrations in `rmf_layered_map_server_demo`, covering synthetic TTL expiration, multi-robot laser scan composition, and end-to-end obstacle-triggered replanning with Nav2.

---

## 1. TTL Smoke Test

This quick smoke test verifies that the layered map server composes a static base grid with temporary regional patches that expire after their time-to-live (TTL).

### Steps

1. Launch the synthetic TTL demo:
   ```bash
   ros2 launch rmf_layered_map_server_demo demo.launch.py
   ```
2. Observe the RViz window: a synthetic static grid is published alongside a temporary occupied rectangle with a **5-second TTL**.
3. Confirm that the temporary rectangle automatically clears from `/map` once the 5-second TTL expires.

:::{tip}
Pass `use_rviz:=False` for a headless run:
```bash
ros2 launch rmf_layered_map_server_demo demo.launch.py use_rviz:=False
```
:::

---

## 2. Three-Robot Nav2 Observation Demo

This demo combines live laser observations from three moving Nav2 robots into the shared global `/map`, demonstrating per-source rasterization, free-space ray clearing, and TTL-based expiration.

<video src="https://github.com/user-attachments/assets/42f35ede-cf89-485b-bcc3-e245ebe79941" controls width="100%"></video>

![Three robot laser observations in the combined global map](https://raw.githubusercontent.com/open-rmf/next_gen_prototype/main/map_server/rmf_layered_map_server_demo/docs/images/nav2_observations.png)

### Steps

1. Launch the three-robot observation simulation:
   ```bash
   ros2 launch rmf_layered_map_server_demo nav2_observations.launch.py
   ```
2. Inspect the four RViz windows that open by default (three robot-local Nav2 views and one combined global map view) as the robots navigate between fixed goals around spawned demo obstacles.
3. Observe how sensor observations behave in the global RViz view:
   - **Per-Source Rasterization & Visualization**: Incoming sensor observations are rasterized into per-source map layers ([SamuelFoo/next_gen_prototype#4](https://github.com/SamuelFoo/next_gen_prototype/pull/4)). RViz color-codes retained obstacle contributions from each robot (`/map/source_contributions`) while separately displaying each robot's latest free-space scan sectors.
   - **Same-Source Free-Space Clearing**: Free-space rays clear stale obstacle cells previously reported by the same source without affecting other sources. For example, when the blue robot passes through the orange robot's sensor field of view, subsequent clear rays from the orange robot remove the transient trail rather than leaving lingering obstacle cells.
   - **TTL Expiry**: Obstacles outside a robot's current field of view remain active in the layered map until their TTL expires (`10.0 s` by default).

### Optional Launch Arguments

* Set `use_nav2_rviz:=False` or `use_global_rviz:=False` to disable either RViz view.
* Set `move_robots:=False` to disable robot movement.
* Set `spawn_clutter:=False` to use the unmodified warehouse world.
* Use `map` and `params_file` to override the warehouse map and shared Nav2 parameters.
* `beam_stride:=1` and `publish_period_sec:=0.5` control scan sampling.
* `max_observation_range:=2.5` and `ttl_sec:=10.0` control observation range and retention.

---

## 3. Two-Robot Obstacle Replanning Demo

This end-to-end demo connects the layered map server to the path server, plan executor, and Nav2 traffic bridge ([SamuelFoo/next_gen_prototype#3](https://github.com/SamuelFoo/next_gen_prototype/pull/3)), exercising the `CODE_PATH_BLOCKED` replanning flow ([open-rmf/next_gen_prototype#39](https://github.com/open-rmf/next_gen_prototype/pull/39)).

:::{warning}
Run only one scenario per ROS/Gazebo domain because both scenarios share the same robot and map topic names. For concurrent runs, set distinct `ROS_DOMAIN_ID` and `GZ_PARTITION` environment variables.
:::

### Step 1: Run the Simple-Room Scenario (Default)

1. Launch the default simple-room scenario (a room with no aisles):
   ```bash
   ros2 launch rmf_layered_map_server_demo replan_obstacle.launch.py
   ```

<video src="https://github.com/user-attachments/assets/977162a2-1506-4473-a169-7156a47e06a7" controls width="100%"></video>

2. Watch the expected sequence unfold in the global RViz window:
   1. **Initial Plans**: Two robots start with non-overlapping scan regions and separate goals; both initial green RMF plans appear on the static map alongside the robot poses, goals, and Nav2 paths.
   2. **Dynamic Obstacle Spawn**: Once the initial plans are active, the demo spawns a red bar across both scan regions that meets the right wall to form a dead end while leaving a detour around its left end. Detected portions of the bar enter the combined `/map`.
   3. **Blockage Detection**: After a `300 ms` debounce, the plan executor publishes `PlanError.CODE_PATH_BLOCKED` for the blocked route.
   4. **Multi-Agent Replanning**: The path server downsamples the updated map and publishes a new conflict-free plan routing around the left end of the obstacle.

### Step 2: Run the Warehouse Scenario

1. Stop the previous launch, then run the two-aisle warehouse scenario (which preserves the original robot poses and a `15 m` shelf-connected bar):
   ```bash
   ros2 launch rmf_layered_map_server_demo replan_obstacle.launch.py \
     scenario:=warehouse
   ```

<video src="https://github.com/user-attachments/assets/ee6c360b-a3c4-4e65-a396-4f2655a72e2d" controls width="100%"></video>

2. Observe both robots detect the `15 m` barrier blocking their aisles, report `CODE_PATH_BLOCKED`, and execute newly generated detour trajectories.

### How Layered Map & Nav2 Replanning Work Under the Hood

* **Single Source of Truth**: The layered-map backend manages all observation persistence, clearing, and TTL expiry; the demo node itself does not maintain separate obstacle memory or reset a source on every scan.
* **Source Contribution Snapshots**: `/map/source_contributions` publishes complete snapshots of active obstacle cells grouped by source (omitting clear cells because each snapshot replaces the previous one). Scan overlay markers in RViz replace earlier markers immediately, affecting visualization only rather than map state.
* **Conservative Downsampling & Cooldown**: The path server conservatively downsamples the `0.1 m` simple-room map and `0.03 m` warehouse map to its `1.0 m` PiBT planning resolution—any planning cell containing an occupied source cell remains occupied. Replan reports enforce a **2-second cooldown** to prevent oscillation.
* **PlanId Target Resending & Goal Superseding**:
  * When a new plan is issued, an unchanged incremental target is resent whenever its `PlanId` changes, ensuring Nav2 receives the target under the new plan.
  * Replaced Nav2 goals are marked as superseded so delayed aborts or cleanup events from older goals cannot trigger duplicate `CODE_PATH_BLOCKED` replan requests.

### Optional Launch Arguments

* `use_nav2_rviz:=True` opens the robot-local Nav2 views.
* `use_global_rviz:=False` runs without the combined RViz view.
* `spawn_delay_sec:=1.0` controls the delay after initial plans are received before spawning the obstacle bar.
* `scenario_timeout_sec:=180.0` controls how long the demo waits for replanning.
* `ttl_sec` controls how long observations outside the current scan remain in the layered map (`60 s` by default for the simple-room scenario and `210 s` for the warehouse scenario). New clear rays remove stale same-source obstacles before the TTL expires.
* `self_filter_radius:=0.22` excludes scan returns inside the robot body.

:::{seealso}
Part of the **For Users** guide.
:::
