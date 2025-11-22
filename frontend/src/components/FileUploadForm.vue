<script setup lang="ts">
  import { ref } from 'vue'

  defineProps<{ msg: string }>()

  const count = ref(0)
  const resultMessage = ref<string>('')

  const fileInput = ref<File | null>(null)

  function handleFileChange(event: Event) {
    const target = event.target as HTMLInputElement
    const file = target.files?.[0] ?? null
    fileInput.value = file as File | null
  }

  async function submitFile() {
    if (!fileInput.value) {
      resultMessage.value = 'No file selected'
      return
    }

    const formData = new FormData()
    formData.append('file', fileInput.value as File)

    try {
      const response = await fetch('http://127.0.0.1:8000/parse-gp/', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      resultMessage.value = `File processed! Download available.`

      const a = document.createElement('a')
      a.href = url
      a.download = fileInput.value.name.replace(/\.[^/.]+$/, '.bh1')
      a.click()
    } catch (err: any) {
      resultMessage.value = `Error: ${err.message}`
    }
  }
</script>

<template>
  <h1>This program does {{ msg }} conversion.</h1>
  <div class="card">
    <div style="margin-top: 20px; display: flex; flex-direction: column;">
      <input type="file" @change="handleFileChange" />
      <button @click="submitFile">Upload & Convert</button>
    </div>

    <p v-if="resultMessage">{{ resultMessage }}</p>
  </div>
</template>

<style scoped>
  .read-the-docs {
    color: #888;
  }
</style>
