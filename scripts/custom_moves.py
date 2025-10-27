#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from mors.srv import QuadrupedCmd

# --- Сервисные клиенты (остаются без изменений) ---
def set_mode_client(mode):
    rospy.wait_for_service('robot_mode')
    try:
        set_mode = rospy.ServiceProxy('robot_mode', QuadrupedCmd)
        resp = set_mode(mode)
        return resp.result
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

def set_action_client(action):
    rospy.wait_for_service('robot_action')
    try:
        set_action = rospy.ServiceProxy('robot_action', QuadrupedCmd)
        resp = set_action(action)
        return resp.result
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

# --- Функции для танцевальных движений ---

def body_shake(pub, status_pub, duration, rate):
    """Движение: тряска корпусом из стороны в сторону (крен)."""
    rospy.loginfo("Dance move: Body Shake")
    start_time = rospy.get_time()
    cmd_pose_msg = Twist()
    
    while rospy.get_time() - start_time < duration and not rospy.is_shutdown():
        t = rospy.get_time() - start_time
        cmd_pose_msg.angular.x = 0.4 * np.sin(4 * 2 * np.pi * t) # Быстрые колебания по крену
        pub.publish(cmd_pose_msg)
        status_pub.publish(True)
        rate.sleep()

def vertical_hop(pub, status_pub, duration, rate):
    """Движение: имитация прыжков на месте."""
    rospy.loginfo("Dance move: Vertical Hop")
    start_time = rospy.get_time()
    cmd_pose_msg = Twist()

    while rospy.get_time() - start_time < duration and not rospy.is_shutdown():
        t = rospy.get_time() - start_time
        cmd_pose_msg.linear.z = 0.06 * abs(np.sin(2 * 2 * np.pi * t)) # Используем abs для "подпрыгивания"
        pub.publish(cmd_pose_msg)
        status_pub.publish(True)
        rate.sleep()

def body_twist(pub, status_pub, duration, rate):
    """Движение: повороты корпуса (рысканье)."""
    rospy.loginfo("Dance move: Body Twist")
    start_time = rospy.get_time()
    cmd_pose_msg = Twist()

    while rospy.get_time() - start_time < duration and not rospy.is_shutdown():
        t = rospy.get_time() - start_time
        cmd_pose_msg.angular.z = 0.5 * np.sin(0.5 * 2 * np.pi * t) # Плавные повороты
        pub.publish(cmd_pose_msg)
        status_pub.publish(True)
        rate.sleep()

# --- Обычные движения ---

def forward_back(pub, status_pub, duration, rate):
    """Движение: вперед-назад по X."""
    rospy.loginfo("Dance move: Forward and Backward")
    start_time = rospy.get_time()
    msg = Twist()
    while rospy.get_time() - start_time < duration and not rospy.is_shutdown():
        t = rospy.get_time() - start_time
        msg.linear.x = 0.05 * np.sin(2 * np.pi * t)   # 1 Гц
        pub.publish(msg)
        status_pub.publish(True)
        rate.sleep()

def side_step(pub, status_pub, duration, rate, direction=1):
    """Движение: боковые шаги по Y. direction=1 вправо, -1 влево."""
    rospy.loginfo("Dance move: Side Step %s" % ("Right" if direction > 0 else "Left"))
    start_time = rospy.get_time()
    msg = Twist()
    while rospy.get_time() - start_time < duration and not rospy.is_shutdown():
        t = rospy.get_time() - start_time
        msg.linear.y = direction * 0.04 * np.sin(2 * np.pi * t)  # 1 Гц
        pub.publish(msg)
        status_pub.publish(True)
        rate.sleep()

def running_hop(pub, status_pub, duration, rate):
    """Бег вперед в припрыжку: поступательно по X + быстрые подпрыгивания по Z."""
    rospy.loginfo("Dance move: Running Hop")
    start_time = rospy.get_time()
    msg = Twist()
    base_speed = 0.08           # м/с эквивалент для визуального “бега”
    hop_amp = 0.06              # амплитуда прыжка по Z
    hop_freq = 6.0              # Гц подпрыгивания
    while rospy.get_time() - start_time < duration and not rospy.is_shutdown():
        t = rospy.get_time() - start_time
        msg.linear.x = base_speed  # постоянное поступательное движение
        msg.linear.z = hop_amp * abs(np.sin(2 * np.pi * hop_freq * t))
        pub.publish(msg)
        status_pub.publish(True)
        rate.sleep()

def body_sway(pub, status_pub, duration, rate):
    """НОВОЕ ДВИЖЕНИЕ: Плавное покачивание корпусом в плоскости XY."""
    rospy.loginfo("Dance move: Body Sway")
    start_time = rospy.get_time()
    cmd_pose_msg = Twist()

    while rospy.get_time() - start_time < duration and not rospy.is_shutdown():
        t = rospy.get_time() - start_time
        # Движение по эллипсу
        cmd_pose_msg.linear.x = 0.04 * np.sin(1 * 2 * np.pi * t)
        cmd_pose_msg.linear.y = 0.03 * np.cos(1 * 2 * np.pi * t)
        pub.publish(cmd_pose_msg)
        status_pub.publish(True)
        rate.sleep()

def body_nod(pub, status_pub, duration, rate):
    """НОВОЕ ДВИЖЕНИЕ: Кивки корпусом (тангаж)."""
    rospy.loginfo("Dance move: Body Nod")
    start_time = rospy.get_time()
    cmd_pose_msg = Twist()

    while rospy.get_time() - start_time < duration and not rospy.is_shutdown():
        t = rospy.get_time() - start_time
        # Колебания по тангажу (ось Y)
        cmd_pose_msg.angular.y = 0.35 * np.sin(2 * 2 * np.pi * t)
        pub.publish(cmd_pose_msg)
        status_pub.publish(True)
        rate.sleep()

def circle_move(pub, status_pub, duration, rate):
    """НОВОЕ ДВИЖЕНИЕ: Кружение на месте."""
    rospy.loginfo("Dance move: Circle Move")
    start_time = rospy.get_time()
    cmd_pose_msg = Twist()

    while rospy.get_time() - start_time < duration and not rospy.is_shutdown():
        # Постоянный поворот и небольшое смещение для имитации шага в сторону
        cmd_pose_msg.angular.z = 0.6  # Постоянная скорость поворота
        cmd_pose_msg.linear.y = 0.02 # Небольшое боковое смещение
        pub.publish(cmd_pose_msg)
        status_pub.publish(True)
        rate.sleep()

def main():
    try:
        rospy.init_node("mors_dance_script")
        rate = rospy.Rate(100)

        cmd_pose_pub = rospy.Publisher("/head/cmd_pose", Twist, queue_size=10)
        status_pub = rospy.Publisher("/head/status", Bool, queue_size=10)

        # Подготовка: встаем и переходим в нужный режим
        set_action_client(1)
        set_mode_client(2)
        rospy.sleep(2.0) # Пауза для стабилизации
        
        # Начало: легкие подпрыгивания и кивки
        vertical_hop(cmd_pose_pub, status_pub, duration=3.0, rate=rate)
        body_nod(cmd_pose_pub, status_pub, duration=2.0, rate=rate)
        
        # Развитие: покачивания и повороты
        body_sway(cmd_pose_pub, status_pub, duration=4.0, rate=rate)
        body_twist(cmd_pose_pub, status_pub, duration=4.0, rate=rate)
        
        # Кульминация: быстрая тряска и кружение
        body_shake(cmd_pose_pub, status_pub, duration=3.0, rate=rate)
        circle_move(cmd_pose_pub, status_pub, duration=4.0, rate=rate)
        
        # Начало: легкие подпрыгивания и кивки
        vertical_hop(cmd_pose_pub, status_pub, duration=3.0, rate=rate)
        body_nod(cmd_pose_pub, status_pub, duration=2.0, rate=rate)

        # Развитие: покачивания и повороты
        body_sway(cmd_pose_pub, status_pub, duration=4.0, rate=rate)
        body_twist(cmd_pose_pub, status_pub, duration=4.0, rate=rate)

        # Вперед-назад несколько секунд
        forward_back(cmd_pose_pub, status_pub, duration=4.0, rate=rate)

        # Боком вправо, затем влево
        side_step(cmd_pose_pub, status_pub, duration=3.0, rate=rate, direction=1)
        side_step(cmd_pose_pub, status_pub, duration=3.0, rate=rate, direction=-1)

        # Кульминация: быстрая тряска и кружение
        body_shake(cmd_pose_pub, status_pub, duration=3.0, rate=rate)
        circle_move(cmd_pose_pub, status_pub, duration=4.0, rate=rate)

        # Бег вперед в припрыжку
        running_hop(cmd_pose_pub, status_pub, duration=5.0, rate=rate)
        
        # Завершение
        rospy.loginfo("--- Dance Finished! ---")
    except rospy.ROSInterruptException:
        print("Program interrupted before completion.")
    finally:
        # 3. Возвращаемся в нейтральное положение и ложимся
        # Убедимся, что паблишеры были созданы, прежде чем их использовать
        if 'status_pub' in locals():
            status_pub.publish(False)
        if 'cmd_pose_pub' in locals():
            cmd_pose_pub.publish(Twist()) # Сброс позы
        
        rospy.sleep(1.0)
        set_action_client(2)
        rospy.loginfo("Script finished.")

if __name__ == '__main__':
    main()
