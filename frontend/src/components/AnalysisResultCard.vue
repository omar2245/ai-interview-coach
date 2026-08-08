<script setup lang="ts">
import { ClipboardList, FileText, Sparkles } from "@lucide/vue";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import type { AnalysisSection, AnalyzeResponse } from "@/types/analysis";

defineProps<{
  analysis: AnalyzeResponse | null;
  sections: AnalysisSection[];
  hasResult: boolean;
}>();
</script>

<template>
  <Card class="rounded-lg border-app-border bg-app-panel text-app-text shadow-app">
    <CardHeader class="space-y-2">
      <div class="flex items-center gap-2 text-sm font-medium text-brand">
        <ClipboardList class="size-4" aria-hidden="true" />
        <span>分析結果</span>
      </div>
      <div class="flex items-start justify-between gap-4">
        <div>
          <CardTitle class="text-xl font-semibold tracking-normal text-app-text">
            {{ hasResult ? "匹配摘要" : "等待分析結果" }}
          </CardTitle>
          <CardDescription class="mt-1 text-app-muted">
            {{
              hasResult
                ? "AI 已根據履歷與職缺產生分析。"
                : "填寫履歷與職缺後開始分析，結果會顯示在這裡。"
            }}
          </CardDescription>
        </div>
        <div
          v-if="analysis"
          class="rounded-lg border border-brand-border bg-brand-soft px-4 py-3 text-right"
        >
          <p class="text-xs font-medium text-brand">匹配分數</p>
          <p class="text-3xl font-semibold text-app-text">
            {{ analysis.match_score }}
          </p>
        </div>
      </div>
    </CardHeader>

    <CardContent v-if="analysis" class="space-y-5">
      <p
        class="rounded-lg border border-app-border bg-app-panel-soft px-4 py-3 text-sm text-app-muted"
        aria-live="polite"
      >
        <template v-if="analysis.history_status === 'saved'">
          已儲存至本機分析紀錄（#{{ analysis.history_id }}）
        </template>
        <template v-else-if="analysis.history_status === 'failed'">
          分析完成，但無法儲存至本機紀錄。
        </template>
        <template v-else>
          分析完成；本機分析紀錄功能未啟用。
        </template>
      </p>
      <div>
        <Progress :model-value="analysis.match_score" class="h-2 bg-app-panel-soft" />
        <div class="mt-2 flex justify-between text-xs text-app-muted">
          <span>待補強</span>
          <span>高度匹配</span>
        </div>
      </div>

      <div class="rounded-lg border border-app-border bg-app-panel-soft p-4">
        <div class="mb-3 flex items-center gap-2 text-sm font-medium text-app-text">
          <FileText class="size-4 text-app-muted" aria-hidden="true" />
          <span>整體摘要</span>
        </div>
        <p class="text-sm leading-7 text-app-muted">
          {{ analysis.summary }}
        </p>
      </div>

      <div class="grid gap-3">
        <section
          v-for="section in sections"
          :key="section.title"
          class="rounded-lg border border-app-border bg-app-panel-soft p-4"
        >
          <div class="mb-3 flex items-center gap-2">
            <component :is="section.icon" class="size-4 text-brand" aria-hidden="true" />
            <h2 class="text-sm font-semibold text-app-text">
              {{ section.title }}
            </h2>
          </div>
          <ul class="space-y-2">
            <li
              v-for="item in section.items"
              :key="item"
              class="flex gap-2 text-sm leading-6 text-app-muted"
            >
              <span class="mt-2 size-1.5 shrink-0 rounded-full bg-success-dot" />
              <span>{{ item }}</span>
            </li>
          </ul>
        </section>
      </div>
    </CardContent>

    <CardContent v-else>
      <div
        class="flex min-h-80 flex-col items-center justify-center rounded-lg border border-dashed border-app-border bg-app-panel-soft px-6 py-10 text-center"
      >
        <div
          class="mb-4 flex size-12 items-center justify-center rounded-full bg-brand-soft text-brand"
        >
          <Sparkles class="size-5" aria-hidden="true" />
        </div>
        <p class="text-base font-semibold text-app-text">尚未產生分析</p>
        <p class="mt-2 max-w-md text-sm leading-6 text-app-muted">
          選擇履歷輸入方式並貼上職缺描述後，點擊開始分析即可取得 AI 匹配摘要。
        </p>
      </div>
    </CardContent>
  </Card>
</template>
