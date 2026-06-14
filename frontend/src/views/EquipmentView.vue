<template>
  <div>
    <div class="toolbar">
      <span class="toolbar-title">🚜 Спецтехника</span>
      <button class="btn btn-primary" @click="showCreate = true">＋ Добавить технику</button>
    </div>

    <div class="card">
      <div v-if="catalog.equipment.length === 0" class="empty">
        <div class="empty-icon">🏗️</div>
        <p>Техника не добавлена</p>
      </div>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Наименование</th>
              <th>Категория</th>
              <th>Описание</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in catalog.equipment" :key="e.id">
              <td>{{ e.id }}</td>
              <td><strong>{{ e.name }}</strong></td>
              <td>
                <span v-if="e.category" class="badge badge-new">{{ e.category }}</span>
                <span v-else style="color:#9ca3af">—</span>
              </td>
              <td style="color:#6b7280;max-width:250px">{{ e.description || '—' }}</td>
              <td>
                <button class="btn btn-danger btn-sm" @click="deleteTarget = e">🗑️</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create modal -->
    <div v-if="showCreate" class="modal-overlay" @click.self="showCreate = false">
      <div class="modal">
        <div class="modal-title">🚜 Новая техника</div>
        <form @submit.prevent="handleCreate">
          <div class="form-group">
            <label>Наименование *</label>
            <input class="form-control" v-model="form.name" required placeholder="Экскаватор KOMATSU PC200" />
          </div>
          <div class="form-group">
            <label>Категория</label>
            <input class="form-control" v-model="form.category" placeholder="Земляные работы" />
          </div>
          <div class="form-group">
            <label>Описание</label>
            <textarea class="form-control" v-model="form.description" rows="3" placeholder="Краткое описание техники…"></textarea>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-ghost" @click="showCreate = false">Отмена</button>
            <button type="submit" class="btn btn-primary">Добавить</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete confirm -->
    <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget = null">
      <div class="modal">
        <div class="modal-title">🗑️ Удалить технику?</div>
        <p class="confirm-text">Удалить <strong>{{ deleteTarget.name }}</strong>?</p>
        <div class="modal-footer">
          <button class="btn btn-ghost" @click="deleteTarget = null">Отмена</button>
          <button class="btn btn-danger" @click="handleDelete">Удалить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { useCatalogStore } from '../stores/catalogStore'

const catalog = useCatalogStore()
const toast = useToast()

const showCreate = ref(false)
const deleteTarget = ref(null)
const form = reactive({ name: '', category: '', description: '' })

onMounted(() => catalog.fetchEquipment())

async function handleCreate() {
  try {
    await catalog.createEquipment({ ...form })
    Object.assign(form, { name: '', category: '', description: '' })
    showCreate.value = false
    toast.success('✅ Техника добавлена!')
  } catch {
    toast.error('❌ Ошибка при добавлении')
  }
}

async function handleDelete() {
  try {
    await catalog.deleteEquipment(deleteTarget.value.id)
    deleteTarget.value = null
    toast.success('🗑️ Техника удалена')
  } catch {
    toast.error('❌ Невозможно удалить — есть связанные заявки')
  }
}
</script>