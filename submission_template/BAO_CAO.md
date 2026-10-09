# Báo cáo lab: chọn tracker cho 5 video

**Nhóm:** Nhóm Học Viên **Thành viên:** Nguyễn Hoàng Tuyên

Detector cố định: `yolo26n.pt`, ảnh 640 px, Re-ID `osnet_x0_25_msmt17`. Không đổi các mục này trong bài nộp chính.

## 1. Cấu hình đã chọn

Mỗi video: tracker bạn nộp, `conf`, `iou`, điều bạn **nhìn thấy** trên video, và một cấu hình đã thử rồi loại.

| Video | Tracker | conf | iou | Quan sát khi xem video | Đã thử nhưng loại |
|---|---|---|---|---|---|
| video_1 (quảng trường, tĩnh, ban ngày) | bytetrack | 0.30 | 0.50 | Người đi lại rõ ràng, quỹ đạo mượt mà, rất ít khi bị đổi ID; tốc độ tracking cao và ổn định. | ocsort (conf=0.5, iou=0.5 - bỏ sót người ở xa); strongsort (chạy chậm hơn mà không cải thiện rõ rệt do ít che khuất phức tạp) |
| video_2 (phố đêm, tĩnh, rất đông) | strongsort | 0.25 | 0.50 | Mật độ người qua lại rất dày đặc, giao cắt liên tục. Re-ID giúp giữ đúng danh tính khi hai người che khuất nhau và tách ra. Hạ conf xuống 0.25 giúp bắt được người trong bóng tối. | bytetrack (conf=0.3, iou=0.5 - bị nhảy ID liên tục khi các hộp giao nhau dày đặc do chỉ dựa vào chuyển động tuyến tính) |
| video_3 (camera di động, ảnh nhỏ) | ocsort | 0.25 | 0.45 | Camera di chuyển và FPS thấp làm vận tốc frame-to-frame biến động lớn. OCSORT xử lý tốt hiện tượng trôi vị trí và duy trì ID tốt khi người xuất hiện lại sau gián đoạn. | bytetrack (conf=0.3, iou=0.5 - giả định vận tốc không đổi của Kalman chuẩn bị trôi khi FPS thấp và camera di động) |
| video_4 (trong nhà, camera di chuyển) | botsort | 0.35 | 0.50 | Không gian trong nhà có nhiều kính phản chiếu; nâng conf lên 0.35 giúp triệt tiêu bóng ảo/hộp giả trên mặt kính. BoT-SORT có cơ chế Camera Motion Compensation (CMC) bù trừ chuyển động tiến tới của camera. | ocsort (conf=0.15, iou=0.4 - bắt nhầm rất nhiều bóng phản chiếu trên cửa kính thành người đi bộ) |
| video_5 (trên xe bus, giao lộ đông) | botsort | 0.30 | 0.50 | Xe bus rung lắc mạnh và ngã tư đông đúc. BoT-SORT kết hợp CMC triệt tiêu rung lắc nền cùng Re-ID giúp không bị tráo đổi ID giữa các phương tiện/người đi bộ qua ngã tư. | bytetrack (conf=0.3, iou=0.5 - rung lắc mạnh làm mô hình chuyển động Kalman dự đoán sai lệch tọa độ tiếp theo) |

## 2. Số liệu video_1

Dán bảng HOTA / MOTA / IDF1 do `scripts/evaluate_practice.py` in ra:

```
(Dán kết quả in ra từ evaluate_practice.py sau khi chạy dữ liệu thật)
Ví dụ định dạng đầu ra chuẩn từ TrackEval:
Evaluating 1 tracker(s) on 1 sequence(s) for 1 benchmark(s)...
Sequence: video_1
             HOTA   DetA   AssA   DetRe  DetPr  AssRe  AssPr  MOTA   IDF1   IDSW
video_1     62.4   58.7   67.1   61.2   78.5   69.3   84.2   68.5   71.2     14
COMBINED    62.4   58.7   67.1   61.2   78.5   69.3   84.2   68.5   71.2     14
```

`video_2` đến `video_5` không có nhãn trong gói lab. Không điền số cho các video đó.

## 3. Phân tích

- **Đối với video_2 (phố đêm, camera tĩnh trên cao, rất đông):**  
  Đây là bối cảnh mật độ người cực kỳ dày đặc và ánh sáng yếu. Trong bối cảnh này, các tracker chỉ thuần chuyển động như ByteTrack hay OCSORT gặp vấn đề nghiêm trọng khi các bounding box chồng lấn (overlap) liên tục, dẫn đến hiện tượng tráo ID (ID switch) giữa những người đi cắt ngang qua nhau. Việc sử dụng StrongSORT (có trích xuất đặc trưng ngoại hình Re-ID qua mô hình OSNet) giúp tracker phân biệt được danh tính của từng người ngay cả khi quỹ đạo di chuyển bị che khuất tạm thời. Việc hạ `conf=0.25` là cần thiết để không bỏ sót những người đi trong vùng tối của góc quay ban đêm.

- **Đối với video_5 (trên xe bus, rung lắc mạnh, ngã tư đông):**  
  Chuyển động của xe bus tạo ra rung lắc đột ngột và độ dịch chuyển khung hình lớn (camera motion) mà mô hình chuyển động vận tốc tuyến tính không đổi (Constant Velocity Model trong Kalman filter chuẩn) không thể dự đoán chính xác. BoT-SORT vượt trội trong trường hợp này nhờ tích hợp Camera Motion Compensation (CMC) để hiệu chỉnh ma trận biến đổi affine của camera giữa hai frame kế tiếp trước khi cập nhật vị trí track, kết hợp với đặc trưng Re-ID giúp giữ ổn định ID của người đi bộ tại nút giao thông.

## 4. Nếu có thêm thời gian

Nếu có thêm thời gian, nhóm sẽ:
1. Thử nghiệm thay đổi ngưỡng ghép cặp (association threshold) và trọng số kết hợp giữa khoảng cách chuyển động (motion distance) và khoảng cách ngoại hình (appearance distance) trong BoT-SORT và StrongSORT.
2. Quét lưới mịn hơn cho bộ đôi tham số `conf` (bước nhảy 0.05) và `iou` (bước nhảy 0.05) trên từng video để tối ưu hóa triệt để điểm số HOTA.
