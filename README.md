# 將剪映生成的簡體字幕轉成正體中文

**剪映影片檔路徑 (Mac):** <家目錄>/Movies/JianyingPro/videocut/<影片 ID>
**影片縮圖:** <家目錄>/Movies/JianyingPro/videocut/<影片 ID>/cover.png

### 使用說明:
0. 照上述路徑說明，找到你要轉換的 **_影片 ID_**
1. 關閉剪映 App
2. 安裝 python3 及 pip
3. 執行 pip install -r requirements.txt
4. 找到你要轉換的 _**影片 ID**_
5. 執行 python3 src/JyCnTwTranslator.py
6. 等待...依字幕的多寡，時間會有所不同
7. 完成！重新打開剪映 App，檢視轉換後的字幕