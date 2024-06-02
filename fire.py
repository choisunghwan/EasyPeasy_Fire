import cv2
import numpy as np
import requests

# 불 인식을 위한 컬러 범위 설정 (HSV 색상 공간에서)
lower_bound = np.array([18, 50, 50], dtype=np.uint8)
upper_bound = np.array([35, 255, 255], dtype=np.uint8)

def detect_fire(frame):
    # BGR 이미지를 HSV 이미지로 변환
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 지정된 컬러 범위에 해당하는 부분만 마스크 생성
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    # 마스크된 이미지에서 화재가 감지되었는지 확인
    fire_detected = cv2.countNonZero(mask) > 0
    return fire_detected

def send_fire_alert():
    url = "http://localhost:8080/api/fire-alert"  # 올바른 URL 형식으로 수정
    data = {"fire_detected": True}
    try:
        response = requests.post(url, json=data)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error sending fire alert: {e}")
        return None

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        fire_detected = detect_fire(frame)
        if fire_detected:
            print("Fire detected!")
            response_code = send_fire_alert()
            if response_code:
                print(f"Alert sent with response code: {response_code}")
            else:
                print("Failed to send alert")

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
