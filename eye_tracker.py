import cv2
import mediapipe as mp
import pyautogui
import time
import keyboard
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# GLOBAL DEĞİŞKENLER

sensitivity = 7
smooth_factor = 10
pause_threshold = 3
tracking_enabled = False  
clicking_left = False
clicking_right = False
eye_closed_start_time = None
left_eye_closed_time = None
right_eye_closed_time = None
left_click_time = 0
double_click_threshold = 1
click_hold_threshold = 0.1
frame_counter = 0
eye_closure_thresh = 0.007
smile_width_thresh = 0.11
smile_open_thresh = 0.01
smiling = False

pyautogui.FAILSAFE = False
screen_w, screen_h = pyautogui.size()
current_x, current_y = pyautogui.position()
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

root = tk.Tk()
root.title("Göz Takip Sistemi")
root.geometry("900x750")
main_frame = tk.Frame(root)
main_frame.pack()
video_label = tk.Label(main_frame)
video_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# ARAYÜZ

def create_slider_with_label(parent, label_text, from_, to, initial_value, row, col):
    label = ttk.Label(parent, text=label_text)
    label.grid(row=row, column=col, sticky="w")
    value_var = tk.DoubleVar()
    value_var.set(initial_value)
    slider = ttk.Scale(parent, from_=from_, to=to, orient="horizontal", variable=value_var)
    slider.grid(row=row, column=col+1, padx=5)
    value_display = ttk.Label(parent, text=f"{initial_value:.3f}")
    value_display.grid(row=row, column=col+2, padx=5)
    slider.config(command=lambda val: value_display.config(text=f"{float(val):.3f}"))
    return slider, value_var

control_frame = tk.Frame(main_frame)
control_frame.grid(row=1, column=0, columnspan=3, pady=20)
sensitivity_slider, sensitivity_var = create_slider_with_label(control_frame, "Hassasiyet", 1, 10, sensitivity, 0, 0)
smooth_slider, smooth_var = create_slider_with_label(control_frame, "Yumuşaklık", 1, 100, smooth_factor, 1, 0)
threshold_slider, threshold_var = create_slider_with_label(control_frame, "Threshold (sn)", 1, 10, pause_threshold, 2, 0)
click_threshold_slider, click_threshold_var = create_slider_with_label(control_frame, "Sol Göz Tıklama Eşiği (sn)", 0.1, 1, click_hold_threshold, 3, 0)
double_click_slider, double_click_var = create_slider_with_label(control_frame, "Çift Tıklama Süresi (sn)", 0.1, 2, double_click_threshold, 4, 0)
eye_threshold_slider, eye_threshold_var = create_slider_with_label(control_frame, "Göz Kapanma Eşiği", 0.001, 0.01, eye_closure_thresh, 5, 0)
smile_width_slider, smile_width_var = create_slider_with_label(control_frame, "Gülümseme Ağız Genişliği", 0.03, 0.2, smile_width_thresh, 6, 0)
smile_open_slider, smile_open_var = create_slider_with_label(control_frame, "Gülümseme Ağız Açıklığı", 0.005, 0.07, smile_open_thresh, 7, 0)

def toggle_tracking():
    global tracking_enabled
    tracking_enabled = not tracking_enabled
    track_button.config(text=f"Takip Durumu: {'AÇIK' if tracking_enabled else 'KAPALI'}")

track_button = ttk.Button(control_frame, text="Takip Durumu: KAPALI", command=toggle_tracking)
track_button.grid(row=8, column=0, columnspan=3, pady=10)

# ANA FONKSİYON

def update_camera():
    global sensitivity, smooth_factor, pause_threshold, tracking_enabled
    global clicking_left, clicking_right, current_x, current_y
    global eye_closed_start_time, left_eye_closed_time, right_eye_closed_time
    global left_click_time, frame_counter, smiling
    if keyboard.is_pressed('ctrl+shift+l'):
        toggle_tracking()
    sensitivity = sensitivity_var.get()
    smooth_factor = smooth_var.get() / 100
    pause_threshold = threshold_var.get()
    click_hold_threshold = click_threshold_var.get()
    double_click_threshold = double_click_var.get()
    eye_closure_thresh = eye_threshold_var.get()
    smile_width_thresh = smile_width_var.get()
    smile_open_thresh = smile_open_var.get()

    ret, frame = cam.read()
    if not ret:
        root.after(10, update_camera)
        return
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    if not output.multi_face_landmarks:
        show_frame(frame)
        root.after(10, update_camera)
        return
    display_frame = cv2.resize(frame, (640, 360))
    landmarks = output.multi_face_landmarks[0].landmark
    left_eye = [landmarks[145], landmarks[159]]
    right_eye = [landmarks[386], landmarks[374]]
    left_closed = abs(left_eye[0].y - left_eye[1].y) < eye_closure_thresh
    right_closed = abs(right_eye[0].y - right_eye[1].y) < eye_closure_thresh
    both_closed = left_closed and right_closed
    only_left_closed = left_closed and not right_closed
    only_right_closed = right_closed and not left_closed   
    center = landmarks[9]
    left_eye_open = abs(left_eye[0].y - left_eye[1].y)
    right_eye_open = abs(right_eye[0].y - right_eye[1].y)
    mouth_width = abs(landmarks[61].x - landmarks[291].x)
    mouth_open = abs(landmarks[13].y - landmarks[14].y)
    if mouth_width > smile_width_thresh or mouth_open > smile_open_thresh:
        smiling = True
    else:
        smiling = False 
    cv2.putText(display_frame, f"Sol Goz: {left_eye_open:.4f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 255, 255), 1)
    cv2.putText(display_frame, f"Sag Goz: {right_eye_open:.4f}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 255, 255), 1)
    cv2.putText(display_frame, f"Agiz Genislik: {mouth_width:.4f}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 255, 255), 1)
    cv2.putText(display_frame, f"Agiz Yukseklik: {mouth_open:.4f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 255, 255), 1)
    cv2.putText(display_frame, f"L9 Poz: ({center.x:.2f}, {center.y:.2f})", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 255), 1)
    for eye in [left_eye, right_eye]:
            for landmark in eye:
                lx = int(landmark.x * 640)
                ly = int(landmark.y * 360)
                cv2.circle(display_frame, (lx, ly), 3, (0, 255, 255), -1)
    center_x = int(center.x * 640)
    center_y = int(center.y * 360)
    cv2.circle(display_frame, (int(landmarks[61].x * 640), int(landmarks[61].y * 360)), 3, (0, 255, 255), -1)
    cv2.circle(display_frame, (int(landmarks[291].x * 640), int(landmarks[291].y * 360)), 3, (0, 255, 255), -1)
    cv2.circle(display_frame, (int(landmarks[13].x * 640), int(landmarks[13].y * 360)), 3, (0, 255, 255), -1)
    cv2.circle(display_frame, (int(landmarks[14].x * 640), int(landmarks[14].y * 360)), 3, (0, 255, 255), -1)
    cv2.circle(display_frame, (center_x, center_y), 6, (255, 0, 0), -1)
    now = time.time()
    if both_closed:
        if eye_closed_start_time is None:
            eye_closed_start_time = now
        elif now - eye_closed_start_time >= pause_threshold:
            toggle_tracking()
            eye_closed_start_time = None
            time.sleep(1.5)
    else:
        eye_closed_start_time = None

    if tracking_enabled:
        delta_x = (center.x - 0.5) * sensitivity
        delta_y = (center.y - 0.5) * sensitivity
        target_x = screen_w / 2 + screen_w * delta_x
        target_y = screen_h / 2 + screen_h * delta_y
        current_x += (target_x - current_x) * smooth_factor
        current_y += (target_y - current_y) * smooth_factor
        frame_counter += 1
        if frame_counter % 2 == 0:
            pyautogui.moveTo(current_x, current_y)

        margin = 5
        mouse_near_edge = (
            current_x <= margin or current_x >= screen_w - margin or
            current_y <= margin or current_y >= screen_h - margin
        )

        if only_left_closed and not mouse_near_edge and not smiling:
            if left_eye_closed_time is None:
                left_eye_closed_time = now
            elif now - left_eye_closed_time >= click_hold_threshold:
                if not clicking_left:
                    pyautogui.mouseDown(button='left')
                    clicking_left = True
        else:
            if clicking_left:
                pyautogui.mouseUp(button='left')
                if now - left_click_time <= double_click_threshold:
                    pyautogui.doubleClick(button='left')
                    left_click_time = 0
                else:
                    left_click_time = now
                clicking_left = False
            left_eye_closed_time = None

        if only_right_closed and not mouse_near_edge and not smiling:
            if right_eye_closed_time is None:
                right_eye_closed_time = now
            elif now - right_eye_closed_time >= click_hold_threshold and not clicking_right:
                pyautogui.mouseDown(button='right')
                pyautogui.mouseUp(button='right')
                clicking_right = True
        else:
            right_eye_closed_time = None
            clicking_right = False        
    else:
        if clicking_left:
            pyautogui.mouseUp(button='left')
            clicking_left = False
        if clicking_right:
            pyautogui.mouseUp(button='right')
            clicking_right = False

    status_text = "AKTIF" if tracking_enabled else "DURAKLATILDI"
    color = (0, 255, 0) if tracking_enabled else (0, 0, 255)
    cv2.putText(display_frame, f"Durum: {status_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    show_frame(display_frame)
    root.after(1, update_camera)

def show_frame(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

update_camera()
root.mainloop()