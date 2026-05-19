#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "std_msgs/msg/float64.hpp"

using std::placeholders::_1;

class CustomDiffDriveNode : public rclcpp::Node
{
public:
  CustomDiffDriveNode(): Node("custom_diff_drive_node")
  {
    RCLCPP_INFO(this->get_logger(), "Custom Diff Drive Node has been started.");
    subscription_ = this->create_subscription<geometry_msgs::msg::Twist>(
      "cmd_vel", 10, std::bind(&CustomDiffDriveNode::topic_callback, this, _1));
    
    publisher_left_ = this->create_publisher<std_msgs::msg::Float64>("/left_wheel_speed", 10);
    publisher_right_ = this->create_publisher<std_msgs::msg::Float64>("/right_wheel_speed", 10);
    publisher_ign_cmd_vel_ = this->create_publisher<geometry_msgs::msg::Twist>("/model/mobile_robot/cmd_vel", 10);
    timer_ = this->create_wall_timer(
      std::chrono::milliseconds(100),
      [this]() {
        auto left_msg = std_msgs::msg::Float64();
        left_msg.data = left_wheel_speed_;
        publisher_left_->publish(left_msg);

        auto right_msg = std_msgs::msg::Float64();
        right_msg.data = right_wheel_speed_;
        publisher_right_->publish(right_msg);
      });
  }
  private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_ign_cmd_vel_;
    rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr subscription_;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr publisher_left_;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr publisher_right_;
    rclcpp::TimerBase::SharedPtr timer_;

    double left_wheel_speed_ = 0.0;
    double right_wheel_speed_ = 0.0;
    const double wheel_base_ = 1.2;
    const double wheel_radius_ = 0.3;

    void topic_callback(const geometry_msgs::msg::Twist & msg)
    {
        double current_speed = msg.linear.x;
        RCLCPP_INFO(this->get_logger(), "Current speed: %f m/s", current_speed);
        double current_angular_velocity = msg.angular.z;
        RCLCPP_INFO(this->get_logger(), "Current angular velocity: %f rad/s", current_angular_velocity);
        left_wheel_speed_ = (current_speed - current_angular_velocity * wheel_base_ / 2.0) / wheel_radius_;
        right_wheel_speed_ = (current_speed + current_angular_velocity * wheel_base_ / 2.0) / wheel_radius_;
        RCLCPP_INFO(this->get_logger(), "Calculated left wheel speed: %f rad/s", left_wheel_speed_);
        RCLCPP_INFO(this->get_logger(), "Calculated right wheel speed: %f rad/s", right_wheel_speed_);
        publisher_ign_cmd_vel_->publish(msg);
    }


};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<CustomDiffDriveNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}