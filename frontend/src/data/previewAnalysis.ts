import type { AnalyzeResponse } from "@/types/analysis";

export const previewAnalysis: AnalyzeResponse = {
  match_score: 78,
  summary:
    "你的履歷與這份前端職缺有不錯的匹配度，已清楚呈現前端開發與跨部門協作經驗。接下來可以補強部署流程、測試與量化成果，讓履歷更貼近職缺需求。",
  strengths: ["前端框架與元件化開發經驗明確", "有 API 串接與狀態管理相關描述"],
  matched_requirements: [
    "符合 JavaScript / TypeScript 經驗需求",
    "具備跨部門合作與產品迭代經驗",
  ],
  gaps: ["履歷中尚未明確呈現 CI/CD 經驗", "缺少雲端部署或監控相關成果"],
  recommendations: [
    "補上專案成果的量化指標",
    "把部署、測試、效能優化經驗寫得更具體",
  ],
  interview_focus: [
    "準備說明代表性專案的技術選擇",
    "準備回答遇到問題時如何排查與溝通",
  ],
};
