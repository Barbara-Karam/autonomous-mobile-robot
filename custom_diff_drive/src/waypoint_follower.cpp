#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "nav2_msgs/action/NavigateToPose.hpp"
using std::placeholders::_1;

class WaypointFollower : public rclcpp::Node
{
public:
  WaypointFollower() : Node("waypoint_follower")
  {
    RCLCPP_INFO(this->get_logger(), "Waypoint Follower Node has been started.");
    subscription_ = this->create_subscription<geometry_msgs::msg::Twist>(