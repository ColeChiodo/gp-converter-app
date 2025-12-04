<script setup lang="ts">
import JSZip from "jszip";
import { ref } from 'vue'

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
		resultMessage.value = 'No file selected';
		return;
	}
	
	const file = fileInput.value as File;
	const formData = new FormData();
	formData.append('file', file);
	
	try {
		const response = await fetch('http://127.0.0.1:8000/parse-gp/', {
			method: 'POST',
			body: formData,
		});
	
		if (!response.ok) {
			throw new Error(`Server error: ${response.status}`);
		}
	
		// Get the zip blob
		const zipBlob = await response.blob();
		resultMessage.value = 'File processed!';
	
		// Download full zip directly
		const url = URL.createObjectURL(zipBlob);
		const a = document.createElement('a');
		a.href = url;
		a.download = file.name.replace(/\.[^/.]+$/, '_binary.zip');
		a.click();
		URL.revokeObjectURL(url);
	} catch (err: any) {
		resultMessage.value = `Error: ${err.message}`;
	}
}
</script>

<template>
  <div class="card">
    <div style="margin-top: 20px; display: flex; flex-direction: column;">
      <input type="file" @change="handleFileChange" />
      <button @click="submitFile">Upload & Convert</button>
    </div>

    <p v-if="resultMessage">{{ resultMessage }}</p>
  </div>
</template>

<style scoped>

</style>
