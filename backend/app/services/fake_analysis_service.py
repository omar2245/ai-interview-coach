from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse


def generate_fake_analysis(request: AnalyzeRequest) -> AnalyzeResponse:
    return AnalyzeResponse(
        match_score=78,
        summary="這是一筆假資料分析結果，之後會改成 AI 產生的內容。",
        strengths=[
            "履歷中有清楚的專案經驗描述",
            "具備與職缺相關的技能基礎",
        ],
        matched_requirements=[
            "符合職缺中提到的基礎技能需求",
            "具備團隊協作與產品開發經驗",
        ],
        gaps=[
            "目前尚未看到明確的部署或 CI/CD 經驗",
            "部分專案成果可以再補上量化指標",
        ],
        recommendations=[
            "補充專案成果，例如效能提升、使用者成長或交付時程",
            "把技能經驗對應到職缺需求，讓履歷更容易被理解",
        ],
        interview_focus=[
            "準備說明代表性專案的技術選擇",
            "準備回答遇到問題時如何排查與溝通",
        ],
    )
