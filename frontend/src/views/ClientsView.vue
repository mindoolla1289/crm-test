<template>
  <div>
    <div class="toolbar">
      <span class="toolbar-title">👤 Клиенты</span>
      <button class="btn btn-primary" @click="showCreate = true">＋ Добавить клиента</button>
    </div>

    <div class="card">
      <div v-if="catalog.clients.length === 0" class="empty">
        <div class="empty-icon">👥</div>
        <p>Клиентов пока нет</p>
      </div>
      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Имя / Организация</th>
              <th>Телефон</th>
              <th>Email</th>
              <th>Дата регистрации</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in catalog.clients" :key="c.id">
              <td>{{ c.id }}</td>
              <td><strong>{{ c.name }}</strong></td>
              <td>{{ c.phone }}</td>
              <td>{{ c.email || '—' }}</td>
              <td style="color:#9ca3af;font-size:13px">{{ formatDate(c.created_at) }}</td>
              <td>
                <button class="btn btn-danger btn-sm" @click="deleteTarget = c">🗑️</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create modal -->
    <div v-if="showCreate" class="modal-overlay" @click.self="showCreate = false">
      <div class="modal">
        <div class="modal-title">👤 Новый клиент</div>
        <form @submit.prevent="handleCreate">
          <div class="form-group">
            <label>ФИО / Название организации *</label>
            <input class="form-control" v-model="form.name" required placeholder="Иванов Иван Иванович" />
          </div>
          <div class="form-group">
            <label>Телефон *</label>
            <input class="form-control" v-model="form.phone" required placeholder="+7 701 000 00 00" />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input class="form-control" v-model="form.email" placeholder="email@example.com" type="email" />
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
        <div class="modal-title">🗑️ Удалить клиента?</div>
        <p class="confirm-text">Удалить клиента <strong>{{ deleteTarget.name }}</strong>?</p>
        <p class="confirm-text" style="color:#dc2626;font-size:13px">Все заявки этого клиента также будут удалены.</p>
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
const form = reactive({ name: '', phone: '', email: '' })

onMounted(() => catalog.fetchClients())

async function handleCreate() {
  try {
    await catalog.createClient({ ...form })
    Object.assign(form, { name: '', phone: '', email: '' })
    showCreate.value = false
    toast.success('✅ Клиент добавлен!')
  } catch {
    toast.error('❌ Ошибка при добавлении клиента')
  }
}

async function handleDelete() {
  try {
    await catalog.deleteClient(deleteTarget.value.id)
    deleteTarget.value = null
    toast.success('🗑️ Клиент удалён')
  } catch {
    toast.error('❌ Невозможно удалить — есть связанные заявки')
  }
}

function formatDate(dt) {
  return new Date(dt).toLocaleDateString('ru-RU')
}
</script>