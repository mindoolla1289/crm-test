<template>
  <form @submit.prevent="handleSubmit">
    <div class="form-group">
      <label>Клиент *</label>
      <select class="form-control" v-model="form.client_id" required>
        <option value="" disabled>Выберите клиента</option>
        <option v-for="c in clients" :key="c.id" :value="c.id">
          {{ c.name }} — {{ c.phone }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label>Спецтехника *</label>
      <select class="form-control" v-model="form.equipment_id" required>
        <option value="" disabled>Выберите технику</option>
        <option v-for="e in equipment" :key="e.id" :value="e.id">
          {{ e.name }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label>Статус</label>
      <select class="form-control" v-model="form.status">
        <option value="new">🔵 Новая</option>
        <option value="in_progress">🟡 В работе</option>
        <option value="completed">🟢 Завершена</option>
      </select>
    </div>

    <div class="form-group">
      <label>Комментарий</label>
      <textarea class="form-control" v-model="form.comment" rows="3" placeholder="Описание задачи, объём работ…"></textarea>
    </div>

    <div class="modal-footer">
      <button type="button" class="btn btn-ghost" @click="$emit('cancel')">Отмена</button>
      <button type="submit" class="btn btn-primary">Сохранить</button>
    </div>
  </form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  clients: Array,
  equipment: Array,
  initial: Object,
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({
  client_id: '',
  equipment_id: '',
  status: 'new',
  comment: '',
})

watch(() => props.initial, (val) => {
  if (val) {
    form.client_id = val.client?.id ?? ''
    form.equipment_id = val.equipment?.id ?? ''
    form.status = val.status
    form.comment = val.comment || ''
  }
}, { immediate: true })

function handleSubmit() {
  emit('submit', { ...form })
}
</script>