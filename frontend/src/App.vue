<script setup lang="ts">
import {
  AlertCircle,
  ArrowRight,
  BriefcaseBusiness,
  CheckCircle2,
  ClipboardList,
  Lightbulb,
  Sparkles,
  Target,
} from "@lucide/vue";
import { computed, ref } from "vue";

import { analyzeJobFit } from "@/api/analysis";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import AnalysisResultCard from "@/components/AnalysisResultCard.vue";
import ResumeInputCard from "@/components/ResumeInputCard.vue";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { previewAnalysis } from "@/data/previewAnalysis";
import type { AnalysisSection, AnalyzeResponse } from "@/types/analysis";

const appVersion = "v0.1.0";
const resumeInputMode = ref<"file" | "text">("file");
const jobDescription = ref("");
const resumeText = ref("");
const selectedFileName = ref("");
const isAnalyzing = ref(false);
const analysisResult = ref<AnalyzeResponse | null>(null);
const errorMessage = ref("");

const displayAnalysis = computed(() => analysisResult.value ?? previewAnalysis);
const displaySections = computed<AnalysisSection[]>(() => [
  {
    title: "履歷強項",
    icon: CheckCircle2,
    items: displayAnalysis.value.strengths,
  },
  {
    title: "命中需求",
    icon: Target,
    items: displayAnalysis.value.matched_requirements,
  },
  {
    title: "可能缺口",
    icon: AlertCircle,
    items: displayAnalysis.value.gaps,
  },
  {
    title: "建議補強",
    icon: Lightbulb,
    items: displayAnalysis.value.recommendations,
  },
  {
    title: "面試準備重點",
    icon: ClipboardList,
    items: displayAnalysis.value.interview_focus,
  },
]);

function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  selectedFileName.value = input.files?.[0]?.name ?? "";
}

async function handleAnalyzeJobFit() {
  isAnalyzing.value = true;
  errorMessage.value = "";
  analysisResult.value = null;

  try {
    analysisResult.value = await analyzeJobFit({
      jobDescription: jobDescription.value,
      resumeText: resumeText.value || "這是暫時的履歷文字",
    });
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : "無法連線到後端服務，請確認 FastAPI 是否已啟動。";
  } finally {
    isAnalyzing.value = false;
  }
}
</script>

<template>
  <main class="relative min-h-screen bg-app-canvas text-app-text">
    <div
      class="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8"
    >
      <header
        class="mb-6 flex flex-col gap-4 border-b border-app-border pb-5 lg:flex-row lg:items-end lg:justify-between"
      >
        <div class="max-w-3xl">
          <h1
            class="text-3xl font-semibold tracking-normal text-app-text sm:text-4xl"
          >
            JobFit Analyzer
          </h1>
          <p class="mt-2 max-w-2xl text-base leading-7 text-app-muted">
            面試職缺匹配分析器
          </p>
        </div>
        <div class="flex items-center gap-2 text-sm text-app-muted">
          <Sparkles class="size-4 text-brand" aria-hidden="true" />
          <span>履歷 × 職缺分析</span>
        </div>
      </header>

      <section class="space-y-5">
        <div class="grid gap-5 lg:grid-cols-2">
          <ResumeInputCard
            :resume-input-mode="resumeInputMode"
            :resume-text="resumeText"
            :selected-file-name="selectedFileName"
            @update:resume-input-mode="resumeInputMode = $event"
            @update:resume-text="resumeText = $event"
            @file-change="handleFileChange"
          />

          <Card
            class="rounded-lg border-app-border bg-app-panel text-app-text shadow-app"
          >
            <CardHeader class="space-y-2">
              <div
                class="flex items-center gap-2 text-sm font-medium text-brand"
              >
                <BriefcaseBusiness class="size-4" aria-hidden="true" />
                <span>職缺</span>
              </div>
              <CardTitle
                class="text-xl font-semibold tracking-normal text-app-text"
              >
                職缺描述
              </CardTitle>
              <CardDescription class="text-app-muted">
                貼上工作內容、必要條件、加分項與公司說明。
              </CardDescription>
            </CardHeader>

            <CardContent>
              <Textarea
                id="job-description"
                v-model="jobDescription"
                class="min-h-72 resize-none border-app-border bg-app-field text-base leading-6 text-app-text placeholder:text-app-subtle focus-visible:ring-brand"
                placeholder="貼上工作內容、必要條件、加分項與公司說明..."
              />
            </CardContent>
          </Card>
        </div>

        <div class="grid gap-4 lg:grid-cols-[1fr_auto] lg:items-center">
          <Alert
            class="border-warning-border bg-warning-surface text-warning-text"
          >
            <AlertCircle class="size-4" aria-hidden="true" />
            <AlertTitle class="font-semibold"> 已接上 FastAPI 假資料 </AlertTitle>
            <AlertDescription class="text-warning-text/80">
              目前後端會先回傳固定分析結果，之後再替換成 AI 產生內容。
            </AlertDescription>
          </Alert>

          <Alert
            v-if="errorMessage"
            class="border-destructive/40 bg-destructive/10 text-destructive"
          >
            <AlertCircle class="size-4" aria-hidden="true" />
            <AlertTitle class="font-semibold"> 分析失敗 </AlertTitle>
            <AlertDescription>
              {{ errorMessage }}
            </AlertDescription>
          </Alert>

          <Button
            class="h-11 cursor-pointer bg-cta-gradient px-8 text-base font-bold text-white shadow-cta hover:opacity-95 disabled:cursor-not-allowed disabled:opacity-60"
            :disabled="isAnalyzing"
            @click="handleAnalyzeJobFit"
          >
            {{ isAnalyzing ? "分析中..." : "開始分析" }}
            <ArrowRight class="ml-2 size-4" aria-hidden="true" />
          </Button>
        </div>

        <AnalysisResultCard
          :analysis="displayAnalysis"
          :sections="displaySections"
          :has-result="Boolean(analysisResult)"
        />
      </section>

      <footer
        class="mt-5 flex flex-wrap justify-end gap-2 border-t border-app-border pt-4 text-xs font-medium text-app-subtle"
      >
        <Badge
          class="border border-app-border bg-app-panel-soft text-app-muted"
        >
          MVP 階段 1
        </Badge>
        <Badge
          variant="outline"
          class="border-app-border bg-app-panel text-app-muted"
        >
          Vue 3 + FastAPI
        </Badge>
        <span
          class="rounded-md border border-app-border bg-app-panel px-2.5 py-0.5 leading-5"
        >
          {{ appVersion }}
        </span>
      </footer>
    </div>
  </main>
</template>
