---
orphan: true
---

# Running the Interactive Web Demonstration

<video src="https://github.com/user-attachments/assets/d5793eee-515d-49a9-a92c-9926617b48ed" controls width="100%"></video>

Launch the fully standalone path server dashboard:

```bash
ros2 launch rmf_path_server_demo demo.launch.py
```

1. Open `http://localhost:8080` in your web browser.
2. Click **Add Robot** to drop active participants onto the canvas.
3. Select a robot and click a cell to place its goal.
4. Click **Send Scenario** to observe multi-agent trajectory generation and live execution progress.

:::{seealso}
Part of the **For Users** guide.
:::
