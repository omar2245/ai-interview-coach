<script setup lang="ts">
import { BriefcaseBusiness } from "@lucide/vue";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";

defineProps<{
  jobDescription: string;
}>();

const emit = defineEmits<{
  "update:jobDescription": [value: string];
}>();
</script>

<template>
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
        :model-value="jobDescription"
        class="min-h-72 resize-none border-app-border bg-app-field text-base leading-6 text-app-text placeholder:text-app-subtle focus-visible:ring-brand"
        placeholder="貼上工作內容、必要條件、加分項與公司說明..."
        @update:model-value="emit('update:jobDescription', String($event))"
      />
    </CardContent>
  </Card>
</template>
