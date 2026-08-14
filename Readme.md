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

## 產品完整路線圖

完整產品以 4 個主要階段開發，並在階段 1 和階段 2 之間加入階段 1.5。

### 階段 1：履歷 × 職缺分析

這是目前 MVP 要先完成的核心功能。

- 上傳履歷，或貼上履歷文字
- 貼上職缺內容
- AI 分析履歷與職缺的匹配度
- 產生摘要、強項、缺口、建議補強方向
- 顯示面試前應優先準備的重點

### 階段 1.5：登入 × 分析紀錄

完成核心分析後，加入使用者登入與個人分析紀錄，讓分析結果不會在重新整理後消失。

- 使用者註冊、登入與登出
- 每筆分析紀錄只屬於建立它的使用者
- 成功分析後自動保存職稱、公司、履歷文字、職缺內容與完整分析結果
- 顯示最新到最舊的分析紀錄，並支援分頁
- 查看單筆分析紀錄完整內容
- 將歷史輸入載回分析頁面，讓使用者修改後重新分析
- 刪除單筆分析紀錄
- 經過明確確認後清空自己的全部分析紀錄
- 不保存原始 PDF 或 DOCX binary，只保存解析後文字與來源資訊

階段 1.5 會使用 FastAPI、SQLite、SQLAlchemy 2.0 與 Alembic，逐步建立 authentication、資料所有權與 History CRUD API。

### 階段 2：面試題產生

在履歷與職缺分析完成後，進一步產生可能被問到的面試題。

- 根據履歷與職缺產生可能面試題
- 題目分類：
  - 履歷追問題
  - 技術 / 專業題
  - 行為題
  - 公司 / 職位動機題
- 每題附上建議回答方向
- 幫助使用者知道該先準備哪些回答

### 階段 3：模擬面試

把面試題變成一題一題的互動練習。

- AI 一題一題提問
- 使用者輸入回答
- AI 針對回答給回饋
- 下一題可以根據使用者回答追問
- 面試結束後產生整體表現總結

### 階段 4：個人面試準備中心

在登入與基本分析紀錄完成後，擴充成更完整的個人面試準備中心。

- 履歷版本管理
- 面試練習紀錄
- 常見弱點追蹤
- 回答範本整理
- 跨裝置同步與更完整的個人化設定

目前階段 1 的核心分析流程已完成，接下來的開發重點是階段 1.5。階段 2 到階段 4 先保留為後續方向。

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
job_title: string optional
company_name: string optional
role_type: string optional
language: string default zh-TW
```

規則：

- `job_description` 必填。
- `resume_file` 和 `resume_text` 至少要有一個。
- 如果有 `resume_file`，優先解析檔案內容。
- 如果沒有檔案，就使用 `resume_text`。
- `job_title` 和 `company_name` 是方便辨識分析紀錄的選填資訊。
- `language` 預設使用 `zh-TW`，也就是繁體中文。

回傳格式範例：

```json
{
  "match_score": 78,
  "summary": "你的履歷與這份前端職缺有不錯的匹配度...",
  "strengths": ["有 Vue / React 前端開發經驗", "有 API 串接與狀態管理經驗"],
  "matched_requirements": [
    "符合 JavaScript / TypeScript 經驗需求",
    "符合前後端串接經驗"
  ],
  "gaps": ["職缺提到 CI/CD，但履歷中沒有明確呈現", "缺少雲端部署經驗描述"],
  "recommendations": ["補上專案部署經驗", "把專案成果改成可量化描述"],
  "interview_focus": [
    "準備說明你如何設計前端架構",
    "準備回答 API 錯誤處理與 loading 狀態"
  ],
  "history_id": 42,
  "history_status": "saved"
}
```

### 階段 1.5 API 樣子（規劃中）

以下 API 是階段 1.5 的目標 contract，實作時仍會透過 tickets 逐步確認細節。

註冊：

```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "learner@example.com",
  "password": "example-password"
}
```

登入：

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "learner@example.com",
  "password": "example-password"
}
```

登入成功後回傳 access token：

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

取得自己的分析紀錄列表：

```http
GET /api/history?limit=20&offset=0
Authorization: Bearer <token>
```

```json
{
  "items": [
    {
      "id": 42,
      "display_title": "Frontend Engineer",
      "company_name": "Example Corp",
      "match_score": 78,
      "resume_source": "text",
      "created_at": "2026-08-14T12:00:00+00:00"
    }
  ],
  "total": 1
}
```

取得單筆完整紀錄：

```http
GET /api/history/42
Authorization: Bearer <token>
```

刪除單筆紀錄：

```http
DELETE /api/history/42
Authorization: Bearer <token>
```

成功時回傳：

```http
204 No Content
```

清空自己的全部紀錄：

```http
DELETE /api/history?confirm=true
Authorization: Bearer <token>
```

```json
{
  "deleted_count": 12
}
```

所有 History API 都只能存取目前登入使用者自己的資料；未知或不屬於該使用者的 ID 統一回傳 `404 Not Found`。

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
- Tailwind CSS：負責版面、間距、RWD 與整體樣式
- shadcn-vue：提供可客製化的 UI 元件基礎
- @lucide/vue：提供乾淨一致的 icon
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
- 初始化 Tailwind CSS + shadcn-vue UI 基礎
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
