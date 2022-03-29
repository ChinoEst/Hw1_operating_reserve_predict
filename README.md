# Hw1_operating_reserve_predict

目標: 預測2022/03/30 to 2022/04/13的備轉容量

使用資料:https://data.gov.tw/dataset/19995

用今日備轉容量 預測明日備轉容量

先把將資料透過MinMaxScaler前處理，使得數據會縮放到到[0,1]之間

放入RNN模型進行訓練

將2/28的備轉容量輸入模型，預測3/1備轉容量，再放入模型備轉容量
直到4/10
