# JobFit Analyzer

JobFit Analyzer 是一個 AI 履歷與職缺匹配分析工具。

第一版 MVP 會先聚焦在一個很小、但完整可用的流程：

1. 使用者上傳履歷，或直接貼上履歷文字。
2. 使用者貼上職缺描述。
3. 系統使用 AI 分析履歷與職缺的匹配程度。
4. 前端顯示清楚的結構化分析結果。

中文產品名稱可以先叫：

> 面試職缺匹配分析器

## MVP 目標

幫助求職者快速理解：

- 自己的履歷和這份職缺有多匹配
- 履歷中已經呈現出哪些強項
- 哪些職缺需求已經被履歷命中
- 哪些地方可能是缺口
- 面試前應該優先準備什麼

第一版的重點不是把所有功能一次做完，而是先做出一個可以真的使用、可以展示、可以部署的核心產品。

## MVP 功能範圍

第一版會包含以下功能。

履歷輸入：

- 支援上傳 PDF、DOCX、TXT
- 支援直接貼上履歷文字，作為備用方式
- 第一版檔案大小限制為 5MB
- 第一版不儲存履歷檔案

職缺輸入：

- 使用 textarea 貼上職缺描述
- 內容可以包含工作內容、必要條件、加分條件、公司說明等

AI 分析結果：

- 整體匹配摘要
- 匹配分數
- 履歷強項
- 職缺需求命中點
- 可能缺口
- 建議補強方向
- 面試前準備重點

基本錯誤處理：

- 沒有提供履歷
- 沒有提供職缺描述
- 檔案格式不支援
- 檔案超過大小限制
- 履歷解析失敗
- AI 分析失敗

## MVP 暫時不做

以下功能先不要放進第一版，避免範圍變太大：

- 登入
- 資料庫
- 歷史紀錄
- 儲存履歷檔案
- 模擬面試
- 面試題一題一答
- 語音功能
- WebSocket
- 付款
- 多履歷管理

先把核心流程做完，之後再自然接到第二階段的「面試題產生」與「模擬面試」。

## API 草稿

第一版後端只需要一個主要 API：

```http
POST /api/analyze
```

請求欄位：

```txt
job_description: string
resume_file: file optional
resume_text: string optional
role_type: string optional
language: string default zh-TW
```

規則：

- `job_description` 必填。
- `resume_file` 和 `resume_text` 至少要有一個。
- 如果有 `resume_file`，優先解析檔案內容。
- 如果沒有檔案，就使用 `resume_text`。
- `language` 預設使用 `zh-TW`，也就是繁體中文。

回傳格式範例：

```json
{
  "match_score": 78,
  "summary": "你的履歷與這份前端職缺有不錯的匹配度...",
  "strengths": [
    "有 Vue / React 前端開發經驗",
    "有 API 串接與狀態管理經驗"
  ],
  "matched_requirements": [
    "符合 JavaScript / TypeScript 經驗需求",
    "符合前後端串接經驗"
  ],
  "gaps": [
    "職缺提到 CI/CD，但履歷中沒有明確呈現",
    "缺少雲端部署經驗描述"
  ],
  "recommendations": [
    "補上專案部署經驗",
    "把專案成果改成可量化描述"
  ],
  "interview_focus": [
    "準備說明你如何設計前端架構",
    "準備回答 API 錯誤處理與 loading 狀態"
  ]
}
```

## 前端頁面規劃

第一版只需要一頁。

輸入區：

- 職缺描述
- 履歷檔案上傳
- 履歷文字貼上區
- 開始分析按鈕

結果區：

- 匹配分數
- 整體摘要
- 履歷強項
- 命中需求
- 可能缺口
- 建議補強
- 面試準備重點

版面規劃：

- 桌機版可以使用左右分欄
- 手機版改成上下排列
- 表單要清楚、簡單，不要做得像複雜後台
- 結果區要容易掃讀，讓求職者一眼看懂重點

## 建議技術方向

目前先預設使用：

- Vue 3：建立前端單頁應用
- TypeScript：讓前端資料結構更安全
- FastAPI：建立後端 API
- OpenAI API：產生履歷與職缺分析
- 不使用資料庫：第一版不保存資料
- 不使用登入：降低 MVP 複雜度

前端與後端會先分成兩個資料夾：

- `frontend`：Vue 3 前端
- `backend`：FastAPI 後端

## 開發學習路線

我們會一步一步慢慢做：

1. 初始化文件與專案規劃。
2. 選定技術架構。
3. 建立 Vue 3 前端專案。
4. 做出第一版單頁 UI。
5. 加上表單狀態與基本驗證。
6. 建立 FastAPI 後端。
7. 先用假資料測試前後端流程。
8. 加上履歷檔案上傳。
9. 加上 PDF / DOCX / TXT 解析。
10. 接上 AI 分析。
11. 顯示真正的分析結果。
12. 補上 loading 與錯誤狀態。
13. 準備部署。

每一步都會盡量保持小而清楚，做完一段再往下一段走。

## 目前狀態

目前已完成：

- 建立 README
- 建立 agent 協作筆記
- 定義 MVP 功能範圍
- 定義第一版 API 草稿
- 決定使用 Vue 3 + FastAPI
- 初始化 Vue 3 前端專案
- 初始化 FastAPI 後端專案
- 建立根目錄 `.gitignore`

尚未開始：

- 建立正式頁面
- 建立 `/api/analyze`
- 串接 AI
- 部署

## 本機開發指令

啟動前端：

```powershell
cd frontend
npm run dev
```

啟動後端：

```powershell
cd backend
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

後端健康檢查：

```http
GET http://localhost:8000/health
```
