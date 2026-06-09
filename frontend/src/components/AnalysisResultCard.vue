<script setup lang="ts">
import { ClipboardList, FileText } from "@lucide/vue";

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
  analysis: AnalyzeResponse;
  sections: AnalysisSection[];
  hasResult: boolean;
}>();
</script>

<template>
  <Card class="rounded-lg border-app-border bg-app-panel text-app-text shadow-app">
    <CardHeader class="space-y-2">
      <div class="flex items-center gap-2 text-sm font-medium text-brand">
        <ClipboardList class="size-4" aria-hidden="true" />
        <span>分析結果預覽</span>
      </div>
      <div class="flex items-start justify-between gap-4">
        <div>
          <CardTitle class="text-xl font-semibold tracking-normal text-app-text">
            匹配摘要
          </CardTitle>
          <CardDescription class="mt-1 text-app-muted">
            {{ hasResult ? "來自 FastAPI 的分析結果。" : "目前顯示預覽結果，送出後會更新。" }}
          </CardDescription>
        </div>
        <div class="rounded-lg border border-brand-border bg-brand-soft px-4 py-3 text-right">
          <p class="text-xs font-medium text-brand">匹配分數</p>
          <p class="text-3xl font-semibold text-app-text">
            {{ analysis.match_score }}
          </p>
        </div>
      </div>
    </CardHeader>

    <CardContent class="space-y-5">
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
  </Card>
</template>
