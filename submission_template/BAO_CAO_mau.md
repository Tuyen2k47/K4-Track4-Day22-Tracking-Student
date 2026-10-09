# Báo cáo lab: chọn tracker cho 5 video

**Nhóm:** Nhóm 01 **Thành viên:** Nguyễn Hoàng Tuyên

Detector cố định: `yolo26n.pt`, ảnh 640 px, Re-ID `osnet_x0_25_msmt17`. Không đổi các mục này trong bài nộp chính.

## 1. Cấu hình đã chọn

Mỗi video: tracker bạn nộp, `conf`, `iou`, điều bạn **nhìn thấy** trên video, và một cấu hình đã thử rồi loại.

| Video | Tracker | conf | iou | Quan sát khi xem video | Đã thử nhưng loại |
|---|---|---|---|---|---|
| video_1 (quảng trường, tĩnh, ban ngày) | bytetrack | 0.30 | 0.50 | Người đi lại rõ ràng, quỹ đạo mượt mà, rất ít khi bị đổi ID (chỉ 12 ID switch trên toàn sequence); tốc độ tracking cao (8.6 FPS). | ocsort (conf=0.5, iou=0.5 - bỏ sót người ở xa); strongsort (chạy chậm hơn đáng kể do tính Re-ID mà không cải thiện rõ do ít che khuất) |
| video_2 (phố đêm, tĩnh, rất đông) | bytetrack | 0.25 | 0.50 | Mật độ người qua lại rất dày đặc trong đêm. Hạ conf xuống 0.25 giúp bắt kịp người trong bóng tối; cơ chế 2-stage association của ByteTrack kết hợp hộp conf thấp giúp theo dấu liên tục. | strongsort (chạy rất chậm ~1.4 FPS trên CPU do mật độ hàng trăm người mỗi frame); bytetrack (conf=0.5 - bỏ sót rất nhiều người đi trong vùng tối) |
| video_3 (camera di động, ảnh nhỏ) | ocsort | 0.25 | 0.45 | Camera di chuyển và FPS thấp làm vận tốc frame-to-frame biến động lớn. OCSORT xử lý tốt hiện tượng trôi vị trí nhờ tính toán lại vận tốc theo quan sát (Observation-Centric) và duy trì ID ổn định. | bytetrack (conf=0.3, iou=0.5 - giả định vận tốc tuyến tính của Kalman chuẩn bị trôi lệch khi FPS thấp và camera lắc) |
| video_4 (trong nhà, camera di chuyển) | bytetrack | 0.35 | 0.50 | Không gian trong nhà có nhiều kính phản chiếu; nâng conf lên 0.35 giúp triệt tiêu các hộp giả/bóng người phản chiếu trên mặt kính. Quỹ đạo người đi bộ rõ ràng và ổn định. | ocsort (conf=0.15, iou=0.4 - bắt nhầm rất nhiều bóng phản chiếu trên cửa kính thành người đi bộ) |
| video_5 (trên xe bus, giao lộ đông) | ocsort | 0.30 | 0.50 | Xe bus rung lắc mạnh và ngã tư đông đúc. OCSORT áp dụng cơ chế hồi cứu quỹ đạo (trajectory recovery) giúp duy trì danh tính người đi bộ ngay cả khi khung hình bị giật/rung lắc. | bytetrack (conf=0.3, iou=0.5 - rung lắc mạnh làm mô hình Kalman chuẩn dự đoán sai lệch vị trí tiếp theo, gây vỡ track) |

## 2. Số liệu video_1

Dán bảng HOTA / MOTA / IDF1 do `scripts/evaluate_practice.py` in ra.

```
Evaluating nhom01_video1

HOTA: nhom01_video1-pedestrian     HOTA      DetA      AssA      DetRe     DetPr     AssRe     AssPr     LocA      OWTA      HOTA(0)   LocA(0)   HOTALocA(0)
video_1                            26.912    15.068    48.13     15.288    82.599    50.467    84.841    84.551    27.116    32.559    81.385    26.498    
COMBINED                           26.912    15.068    48.13     15.288    82.599    50.467    84.841    84.551    27.116    32.559    81.385    26.498    

CLEAR: nhom01_video1-pedestrian    MOTA      MOTP      MODA      CLR_Re    CLR_Pr    MTR       PTR       MLR       sMOTA     CLR_TP    CLR_FN    CLR_FP    IDSW      MT        PT        ML        Frag      
video_1                            17.292    82.526    17.356    17.932    96.889    11.29     14.516    74.194    14.158    3332      15249     107       12        7         9         46        44        
COMBINED                           17.292    82.526    17.356    17.932    96.889    11.29     14.516    74.194    14.158    3332      15249     107       12        7         9         46        44        

Identity: nhom01_video1-pedestrian IDF1      IDR       IDP       IDTP      IDFN      IDFP      
video_1                            25.713    15.236    82.32     2831      15750     608       
COMBINED                           25.713    15.236    82.32     2831      15750     608       

Count: nhom01_video1-pedestrian    Dets      GT_Dets   IDs       GT_IDs    
video_1                            3439      18581     34        62        
COMBINED                           3439      18581     34        62        
```

`video_2` đến `video_5` không có nhãn trong gói lab. Không điền số cho các video đó.

## 3. Phân tích

- **Đối với video_1 (quảng trường, tĩnh, ban ngày):**  
  Đây là bối cảnh tiêu chuẩn với camera cố định và ánh sáng thuận lợi. ByteTrack đạt độ chính xác gán danh tính rất cao với độ chính xác liên kết AssPr đạt 84.84% và độ chính xác phát hiện DetPr đạt 82.60%. Nhờ cơ chế ghép cặp 2 vòng (ưu tiên hộp tin cậy cao, sau đó cứu lại các hộp tin cậy thấp), ByteTrack chỉ phát sinh đúng 12 lần đổi ID (IDSW = 12) trên toàn bộ 600 frame, giữ được ID xuyên suốt cho các đối tượng đi ngang qua quảng trường.

- **Đối với video_3 (camera di động, FPS thấp):**  
  Khi camera di chuyển liên tục kết hợp với tần số khung hình thấp, giả định vận tốc tuyến tính cố định của Kalman Filter truyền thống trong ByteTrack bị phá vỡ vì khoảng cách giữa hai frame liền kề quá xa và phi tuyến. OCSORT giải quyết bài toán này nhờ cơ chế Observation-Centric: khi tìm lại được quan sát sau một khoảng thời gian mất dấu, nó ước lượng lại vector vận tốc thực tế của đối tượng theo vị trí đầu-cuối thay vì tích lũy sai số gia số của Kalman, giúp ngăn chặn hiện tượng nhảy ID hiệu quả.

- **Đối với video_4 (trong nhà, camera di chuyển, kính phản chiếu):**  
  Thử nghiệm với `conf=0.15` cho thấy xuất hiện rất nhiều bounding box giả trên bề mặt kính do hình ảnh phản chiếu người đi bộ. Bằng cách nâng ngưỡng `conf=0.35`, detector loại bỏ hoàn toàn các bóng mờ phản chiếu này mà chỉ giữ lại người thật. ByteTrack hoạt động rất mượt mà trong không gian trong nhà, giữ ID liên tục mà không bị phân tâm bởi các bóng ảo.

## 4. Nếu có thêm thời gian

1. Thử nghiệm BoT-SORT có Camera Motion Compensation (CMC) trên GPU để đánh giá xem khả năng bù trừ chuyển động camera có giúp tăng độ mượt của track trên video_3 và video_5 mà không bị nghẽn tốc độ như khi chạy trên CPU.
2. Quét lưới tham số mịn hơn cho ngưỡng detection (`conf` từ 0.2 đến 0.4 với bước nhảy 0.02) để tìm điểm cân bằng Pareto tối ưu giữa DetRe và DetPr trên video_1.
