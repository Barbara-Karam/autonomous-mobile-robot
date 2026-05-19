# Autonomous Mobile Robot using ROS 2 & Gazebo

A complete autonomous navigation project for a differential drive mobile robot using ROS 2, Gazebo Ignition, Nav2, SLAM, and sensor fusion.

---

## Project Overview

This project demonstrates the implementation of a fully autonomous mobile robot in simulation using the ROS 2 ecosystem.

The robot is capable of:

* Simultaneous Localization and Mapping (SLAM)
* Autonomous navigation using Nav2
* Obstacle avoidance
* Sensor fusion using EKF
* Localization inside a prebuilt map
* Path planning and replanning in complex environments

The system was developed as part of the Robotics for Professionals Diploma graduation project.

---

# Features

## Robot Platform

The robot is modeled as a differential drive mobile robot including:

* Two actuated wheels
* Passive caster wheel
* Simulated IMU
* Simulated 2D LiDAR
* RGB camera

The robot description is implemented using:

* URDF/XACRO
* ros2_control
* Gazebo Ignition plugins

---

## Simulation Environment

A custom Gazebo world was designed to evaluate navigation robustness.

The environment includes:

* Long corridors
* Symmetric sections
* Narrow passages
* Static and dynamic obstacles
* Different floor textures

---

## Navigation Stack

The project integrates the complete ROS 2 autonomous navigation pipeline:

### SLAM

* Online map generation using SLAM Toolbox

### Localization

* AMCL localization using the saved map

### Sensor Fusion

* EKF using `robot_localization`
* Fusion of:

  * Wheel odometry
  * IMU measurements

### Navigation

* Nav2 stack
* Global planner
* Local planner
* Recovery behaviors
* Dynamic replanning

---

# Technologies Used

* ROS 2
* Gazebo Ignition
* Nav2
* SLAM Toolbox
* robot_localization
* RViz2
* ros2_control
* URDF/XACRO
* YAML configuration files

---

# Project Structure

```bash
src/
├── robot_description/
│   ├── urdf/
│   ├── meshes/
│   ├── config/
│   └── launch/
│
├── robot_bringup/
│   ├── launch/
│   └── config/
│
├── navigation/
│   ├── maps/
│   ├── params/
│   └── launch/
│
├── custom_world/
│   ├── worlds/
│   └── models/
│
└── localization/
    ├── config/
    └── launch/
```

---

# Installation

## Requirements

* Ubuntu 22.04
* ROS 2 Humble
* Gazebo Ignition Fortress

Install dependencies:

```bash
sudo apt update
sudo apt install ros-humble-navigation2 \
ros-humble-nav2-bringup \
ros-humble-slam-toolbox \
ros-humble-robot-localization \
ros-humble-xacro \
ros-humble-joint-state-publisher \
ros-humble-ros2-control \
ros-humble-gazebo-ros-pkgs
```

---

# Build the Workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Clone repository
git clone https://github.com/Barbara-Karam/autonomous-mobile-robot/ src/

# Build
colcon build --symlink-install

# Source workspace
source install/setup.bash
```

---

# Running the Project

## 1. Launch Gazebo Simulation

```bash
ros2 launch robot_bringup simulation.launch.py
```

This launches:

* Gazebo Ignition
* Robot model
* ros2_control
* Sensors

---

## 2. Run SLAM

```bash
ros2 launch navigation slam.launch.py
```

Drive the robot manually to generate the map.

Save the generated map:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/map
```

---

## 3. Localization

```bash
ros2 launch localization localization.launch.py
```

This launches:

* EKF node
* AMCL localization
* Map server

---

## 4. Autonomous Navigation

```bash
ros2 launch navigation nav2.launch.py
```

Open RViz2 and set a navigation goal using the “Nav2 Goal” tool.

The robot will:

* Plan a path
* Avoid obstacles
* Replan dynamically if needed

---

# Sensor Fusion

The robot uses an Extended Kalman Filter (EKF) to improve localization accuracy.

Fused sensors:

* Wheel encoder odometry
* IMU data

The EKF publishes a stable:

```bash
odom → base_link
```

transform for the navigation stack.

---

# Demonstration

The project demonstration includes:

* Robot spawning in Gazebo
* SLAM map generation
* Map saving
* AMCL localization
* Autonomous navigation to goal points
* Obstacle avoidance

---

# Demo Video is included in the repo
