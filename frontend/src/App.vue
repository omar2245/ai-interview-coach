<script setup lang="ts">
import {
  AlertCircle,
  ArrowRight,
  BriefcaseBusiness,
  CheckCircle2,
  ClipboardList,
  FileText,
  Lightbulb,
  Sparkles,
  Target,
  Upload,
} from '@lucide/vue'
import { ref } from 'vue'

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { Textarea } from '@/components/ui/textarea'

type AnalysisSection = {
  title: string
  icon: typeof CheckCircle2
  items: string[]
}

const appVersion = 'v0.1.0'
const resumeInputMode = ref<'file' | 'text'>('file')
const jobDescription = ref('')
const resumeText = ref('')
const selectedFileName = ref('')
const resumeFileInput = ref<HTMLInputElement | null>(null)

const matchScore = 78

const analysisSections: AnalysisSection[] = [
  {
    title: '履歷強項',
    icon: CheckCircle2,
    items: ['前端框架與元件化開發經驗明確', '有 API 串接與狀態管理相關描述'],
  },
  {
    title: '命中需求',
    icon: Target,
    items: ['符合 JavaScript / TypeScript 經驗需求', '具備跨部門合作與產品迭代經驗'],
  },
  {
    title: '可能缺口',
    icon: AlertCircle,
    items: ['履歷中尚未明確呈現 CI/CD 經驗', '缺少雲端部署或監控相關成果'],
  },
  {
    title: '建議補強',
    icon: Lightbulb,
    items: ['補上專案成果的量化指標', '把部署、測試、效能優化經驗寫得更具體'],
  },
]

function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  selectedFileName.value = input.files?.[0]?.name ?? ''
}

function openResumeFilePicker() {
  resumeFileInput.value?.click()
}
</script>

<template>
  <main class="relative min-h-screen bg-app-canvas text-app-text">
    <div class="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8">
      <header class="mb-6 flex flex-col gap-4 border-b border-app-border pb-5 lg:flex-row lg:items-end lg:justify-between">
        <div class="max-w-3xl">
          <h1 class="text-3xl font-semibold tracking-normal text-app-text sm:text-4xl">
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
          <Card class="rounded-lg border-app-border bg-app-panel text-app-text shadow-app">
            <CardHeader class="space-y-2">
              <div class="flex items-center gap-2 text-sm font-medium text-brand">
                <FileText class="size-4" aria-hidden="true" />
                <span>履歷</span>
              </div>
              <CardTitle class="text-xl font-semibold tracking-normal text-app-text">
                履歷輸入
              </CardTitle>
              <CardDescription class="text-app-muted">
                預設使用檔案上傳，也可以切換成直接貼上履歷文字。
              </CardDescription>
            </CardHeader>

            <CardContent class="space-y-4">
              <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <Label class="text-sm font-medium text-app-text">
                  輸入方式
                </Label>
                <div class="grid grid-cols-2 rounded-lg border border-app-border bg-app-field p-1">
                  <button
                    type="button"
                    class="rounded-md px-3 py-1.5 text-sm font-medium transition"
                    :class="resumeInputMode === 'file' ? 'bg-brand-strong text-white' : 'text-app-muted hover:text-app-text'"
                    @click="resumeInputMode = 'file'"
                  >
                    上傳履歷
                  </button>
                  <button
                    type="button"
                    class="rounded-md px-3 py-1.5 text-sm font-medium transition"
                    :class="resumeInputMode === 'text' ? 'bg-brand-strong text-white' : 'text-app-muted hover:text-app-text'"
                    @click="resumeInputMode = 'text'"
                  >
                    貼上文字
                  </button>
                </div>
              </div>

              <div v-if="resumeInputMode === 'file'" class="space-y-2">
                <input
                  id="resume-file"
                  ref="resumeFileInput"
                  type="file"
                  accept=".pdf,.docx,.txt"
                  class="sr-only"
                  @change="handleFileChange"
                />

                <button
                  type="button"
                  class="group w-full rounded-lg border border-dashed border-app-border bg-app-panel-soft p-5 text-center transition hover:border-brand-border hover:bg-app-field"
                  @click="openResumeFilePicker"
                >
                  <span class="mx-auto mb-4 flex size-12 items-center justify-center rounded-full bg-brand-soft text-brand transition group-hover:bg-brand-strong group-hover:text-white">
                    <Upload class="size-5" aria-hidden="true" />
                  </span>
                  <span class="block text-base font-semibold text-app-text">
                    上傳履歷檔案
                  </span>
                  <span class="mt-1 block text-sm leading-6 text-app-muted">
                    點擊選擇 PDF、DOCX 或 TXT
                  </span>
                  <span class="mt-4 flex items-center justify-center gap-2 text-xs text-app-subtle">
                    <span>檔案上限 5MB</span>
                    <span class="size-1 rounded-full bg-app-subtle" />
                    <span>不會儲存原始檔案</span>
                  </span>
                  <span v-if="selectedFileName" class="mx-auto mt-4 block max-w-full truncate rounded-md border border-brand-border bg-brand-soft px-3 py-2 text-xs font-medium text-brand">
                    已選擇：{{ selectedFileName }}
                  </span>
                </button>
              </div>

              <div v-else class="space-y-2">
                <Textarea
                  id="resume-text"
                  v-model="resumeText"
                  class="min-h-56 resize-none border-app-border bg-app-field text-base leading-6 text-app-text placeholder:text-app-subtle focus-visible:ring-brand"
                  placeholder="貼上履歷內容，例如工作經歷、專案、技能與學歷..."
                />
              </div>
            </CardContent>
          </Card>

          <Card class="rounded-lg border-app-border bg-app-panel text-app-text shadow-app">
            <CardHeader class="space-y-2">
              <div class="flex items-center gap-2 text-sm font-medium text-brand">
                <BriefcaseBusiness class="size-4" aria-hidden="true" />
                <span>職缺</span>
              </div>
              <CardTitle class="text-xl font-semibold tracking-normal text-app-text">
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
          <Alert class="border-warning-border bg-warning-surface text-warning-text">
            <AlertCircle class="size-4" aria-hidden="true" />
            <AlertTitle class="font-semibold">
              今天先使用假資料
            </AlertTitle>
            <AlertDescription class="text-warning-text/80">
              目前按鈕還不會呼叫 API；下一步會把表單接到 FastAPI。
            </AlertDescription>
          </Alert>

          <Button class="h-11 cursor-pointer bg-cta-gradient px-8 text-base font-bold text-white shadow-cta hover:opacity-95">
            開始分析
            <ArrowRight class="ml-2 size-4" aria-hidden="true" />
          </Button>
        </div>

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
                  之後會改成 AI 回傳的正式結果。
                </CardDescription>
              </div>
              <div class="rounded-lg border border-brand-border bg-brand-soft px-4 py-3 text-right">
                <p class="text-xs font-medium text-brand">匹配分數</p>
                <p class="text-3xl font-semibold text-app-text">{{ matchScore }}</p>
              </div>
            </div>
          </CardHeader>

          <CardContent class="space-y-5">
            <div>
              <Progress :model-value="matchScore" class="h-2 bg-app-panel-soft" />
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
                你的履歷與這份前端職缺有不錯的匹配度，已清楚呈現前端開發與跨部門協作經驗。接下來可以補強部署流程、測試與量化成果，讓履歷更貼近職缺需求。
              </p>
            </div>

            <div class="grid gap-3">
              <section
                v-for="section in analysisSections"
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
      </section>

      <footer class="mt-5 flex flex-wrap justify-end gap-2 border-t border-app-border pt-4 text-xs font-medium text-app-subtle">
        <Badge class="border border-app-border bg-app-panel-soft text-app-muted">
          MVP 階段 1
        </Badge>
        <Badge variant="outline" class="border-app-border bg-app-panel text-app-muted">
          Vue 3 + FastAPI
        </Badge>
        <span class="rounded-md border border-app-border bg-app-panel px-2.5 py-0.5 leading-5">
          {{ appVersion }}
        </span>
      </footer>
    </div>
  </main>
</template>
