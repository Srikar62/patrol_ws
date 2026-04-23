# 🚓 NIGHT PATROL ROBOT

## 1. Project Title & Overview
**Night Patrol Robot** is an autonomous surveillance system designed for night-time patrolling, obstacle detection, and environmental monitoring. Developed as part of the "Mobile and Autonomous Robots (UE23CS343BB7)" course, this project leverages ROS 2, computer vision, and simulation tools to create a reliable robotic guard.

In real-world applications, such a system significantly enhances security, surveillance, and automation by reducing the need for human guards in hazardous or monotonous night-watch duties.

## 2. Features
- **Autonomous Navigation**: Waypoint-based patrolling using a Finite State Machine (FSM).
- **Obstacle Detection and Avoidance**: Safely navigates around obstacles in its path.
- **Night Surveillance Capability**: Low-light image enhancement using CLAHE to improve visibility in dark environments.
- **Real-time Monitoring & Alerting**: Motion-based intruder detection that triggers automated logging and alert broadcasting.

## 3. Tech Stack
- **Programming Languages**: Python
- **Frameworks/Tools**: ROS 2 (Robot Operating System), OpenCV
- **Simulation**: Gazebo, RViz
- **Libraries**: NumPy, `cv_bridge`, `nav2_simple_commander`, standard ROS message packages

## 4. System Architecture / Workflow
The system follows a sequential pipeline to ensure safe and effective patrolling:
1. **Sensor Input**: The camera captures raw image frames from the environment (`/camera/image_raw`).
2. **Processing (Sensing Node)**: Images undergo low-light enhancement (CLAHE). OpenCV's MOG2 background subtractor detects motion.
3. **Decision (FSM & Alert Node)**:
   - If motion is detected, an intruder alert is published (`/intruder_detected`).
   - The alert system logs the event and broadcasts a status update.
   - The navigation FSM halts the robot and switches to an `ALERT` state.
4. **Movement (Navigation FSM)**: If no intruder is present and battery levels are sufficient, the robot continues its autonomous waypoint navigation. When the battery runs low, it automatically triggers a `RETURN_TO_BASE` behavior to dock.

## 5. Installation & Setup
Follow these steps to set up the project on your local machine.

### Prerequisites
- Ubuntu 22.04 (recommended)
- ROS 2 (e.g., Humble or Foxy)
- Gazebo and RViz2

### Steps
1. **Clone the repository** (or download the workspace):
   ```bash
   git clone https://github.com/Srikar62/patrol_ws.git
   cd patrol_ws
   ```
2. **Install dependencies**:
   Ensure you have the required ROS 2 packages and Python libraries.
   ```bash
   rosdep install --from-paths src --ignore-src -r -y
   pip install opencv-python numpy
   ```
3. **Build the workspace**:
   ```bash
   colcon build
   ```
4. **Source the setup file**:
   ```bash
   source install/setup.bash
   ```

## 6. Usage
To launch the complete simulation and software stack, open separate terminals and run the following commands:

1. **Launch the Simulation Environment (Gazebo)**:
   ```bash
   cd ~/patrol_ws
   ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
   ```

2. **Launch Nav2 Bringup (with map)**:
   ```bash
    cd ~/patrol_ws
   ros2 launch nav2_bringup bringup_launch.py map:=$HOME/patrol_ws/maps/patrol_map.yaml use_sim_time:=True
   ```

3. **Launch RViz for Visualization**:
   ```bash
   cd ~/patrol_ws
   ros2 launch nav2_bringup rviz_launch.py
   ```

4. **Launch the Full Patrol System**:
   ```bash
   cd ~/patrol_ws
   source install/setup.bash
   ros2 launch alert_system full_patrol.launch.py
   ```

5. **Manual Teleoperation**:
   ```bash
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```

## 7. Results
The robot successfully navigates through predefined waypoints in the simulated environment. When low-light conditions are encountered, the camera feed is enhanced, and moving objects (intruders) are reliably detected, prompting the robot to halt and log the security event.


## 9. Project Structure
```text
patrol_ws/
├── src/
│   ├── alert_system/       # Handles security alerts and logging
│   ├── navigation_fsm/     # Waypoint navigation and state management
│   ├── sensing_node/       # Low-light vision and motion detection
│   └── slam_perception/    # SLAM and advanced perception
├── build/                  # Compiled workspace files
├── install/                # Installation targets and setup scripts
└── log/                    # ROS 2 execution logs
```


## 12. Contributors
- **Srikar Sunku** (PES2UG23CS629)
- **Sugavasi Mithil** (PES2UG23CS611)
- **T. Sai Rushil** (PES2UG23CS655)
- **Suhas T** (PES2UG23CS616)

**Instructor**: Dr. Ruby Dinakar

