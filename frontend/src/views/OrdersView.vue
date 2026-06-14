<template>
  <div>
    <!-- Toolbar -->
    <div class="toolbar">
      <span class="toolbar-title">📋 Заявки <span class="total-badge">{{ store.total }}</span></span>

      <select class="form-control" style="width:170px" v-model="store.filterStatus" @change="applyFilter">
        <option value="">Все статусы</option>
        <option value="new">🔵 Новая</option>
        <option value="in_progress">🟡 В работе</option>
        <option value="completed">🟢 Завершена</option>
      </select>

      <select class="form-control" style="width:180px" v-model="store.sortOrder" @change="applyFilter">
        <option value="desc">Сначала новые</option>
        <option value="asc">Сначала старые</option>
      </select>

      <button class="btn btn-primary" @click="showCreate = true">＋ Создать заявку</button>
    </div>

    <!-- Table -->
    <div class="card">
      <div v-if="store.loading" class="empty">
        <div class="empty-icon">⏳</div>
        <p>Загружаем данные…</p>
      </div>

      <div v-else-if="store.orders.length === 0" class="empty">
        <div class="empty-icon">📭</div>
        <p>Заявок пока нет. Создайте первую!</p>
      </div>

      <div v-else class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Клиент</th>
              <th>Телефон</th>
              <th>Техника</th>
              <th>Комментарий</th>
              <th>Статус</th>
              <th>Дата</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in store.orders" :key="order.id">
              <td><strong>#{{ order.id }}</strong></td>
              <td>{{ order.client.name }}</td>
              <td>{{ order.client.phone }}</td>
              <td>{{ order.equipment.name }}</td>
              <td style="max-width:200px; color:#6b7280">{{ order.comment || '—' }}</td>
              <td>
                <select
                  class="badge"
                  :class="'badge-' + order.status"
                  :value="order.status"
                  @change="changeStatus(order, $event.target.value)"
                  style="cursor:pointer; border:none; outline:none; background:inherit"
                >
                  <option value="new">🔵 Новая</option>
                  <option value="in_progress">🟡 В работе</option>
                  <option value="completed">🟢 Завершена</option>
                </select>
              </td>
              <td style="white-space:nowrap; color:#9ca3af; font-size:13px">
                {{ formatDate(order.created_at) }}
              </td>
              <td>
                <div style="display:flex;gap:6px">
                  <button class="btn btn-ghost btn-sm" @click="openEdit(order)">✏️</button>
                  <button class="btn btn-danger btn-sm" @click="confirmDelete(order)">🗑️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="store.pages > 1" class="pagination">
        <button class="page-btn" :disabled="store.currentPage === 1" @click="goPage(1)">«</button>
        <button class="page-btn" :disabled="store.currentPage === 1" @click="goPage(store.currentPage - 1)">‹</button>
        <button
          v-for="p in visiblePages"
          :key="p"
          class="page-btn"
          :class="{ active: p === store.currentPage }"
          @click="goPage(p)"
        >{{ p }}</button>
        <button class="page-btn" :disabled="store.currentPage === store.pages" @click="goPage(store.currentPage + 1)">›</button>
        <button class="page-btn" :disabled="store.currentPage === store.pages" @click="goPage(store.pages)">»</button>
      </div>
    </div>

    <!-- Create modal -->
    <div v-if="showCreate" class="modal-overlay" @click.self="showCreate = false">
      <div class="modal">
        <div class="modal-title">➕ Новая заявка</div>
        <OrderForm :clients="catalog.clients" :equipment="catalog.equipment" @submit="handleCreate" @cancel="showCreate = false" />
      </div>
    </div>

    <!-- Edit modal -->
    <div v-if="editOrder" class="modal-overlay" @click.self="editOrder = null">
      <div class="modal">
        <div class="modal-title">✏️ Редактировать заявку #{{ editOrder.id }}</div>
        <OrderForm
          :clients="catalog.clients"
          :equipment="catalog.equipment"
          :initial="editOrder"
          @submit="handleUpdate"
          @cancel="editOrder = null"
        />
      </div>
    </div>

    <!-- Delete confirm modal -->
    <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget = null">
      <div class="modal">
        <div class="modal-title">🗑️ Подтверждение удаления</div>
        <p class="confirm-text">
          Вы уверены, что хотите удалить заявку <strong>#{{ deleteTarget.id }}</strong>
          от клиента <strong>{{ deleteTarget.client.name }}</strong>?
        </p>
        <p class="confirm-text" style="color:#dc2626; font-size:13px">Это действие необратимо.</p>
        <div class="modal-footer">
          <button class="btn btn-ghost" @click="deleteTarget = null">Отмена</button>
          <button class="btn btn-danger" @click="handleDelete">Удалить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { useOrdersStore } from '../stores/ordersStore'
import { useCatalogStore } from '../stores/catalogStore'
import OrderForm from '../components/OrderForm.vue'

const store = useOrdersStore()
const catalog = useCatalogStore()
const toast = useToast()

const showCreate = ref(false)
const editOrder = ref(null)
const deleteTarget = ref(null)

onMounted(async () => {
  await Promise.all([store.fetchOrders(), catalog.fetchClients(), catalog.fetchEquipment()])
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, store.currentPage - 2)
  const end = Math.min(store.pages, store.currentPage + 2)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

function applyFilter() {
  store.currentPage = 1
  store.fetchOrders()
}

function goPage(p) {
  store.currentPage = p
  store.fetchOrders()
}

function openEdit(order) {
  editOrder.value = order
}

function confirmDelete(order) {
  deleteTarget.value = order
}

async function handleCreate(data) {
  try {
    await store.createOrder(data)
    showCreate.value = false
    toast.success('✅ Заявка успешно создана!')
  } catch (e) {
    toast.error('❌ Ошибка при создании заявки')
  }
}

async function handleUpdate(data) {
  try {
    await store.updateOrder(editOrder.value.id, data)
    editOrder.value = null
    toast.success('✅ Заявка обновлена!')
  } catch (e) {
    toast.error('❌ Ошибка при обновлении')
  }
}

async function handleDelete() {
  try {
    await store.deleteOrder(deleteTarget.value.id)
    deleteTarget.value = null
    toast.success('🗑️ Заявка удалена')
  } catch (e) {
    toast.error('❌ Ошибка при удалении')
  }
}

async function changeStatus(order, newStatus) {
  try {
    await store.updateOrder(order.id, { status: newStatus })
    toast.success('✅ Статус обновлён')
  } catch (e) {
    toast.error('❌ Ошибка обновления статуса')
  }
}

function formatDate(dt) {
  return new Date(dt).toLocaleString('ru-RU', { day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit' })
}
</script>

<style scoped>
.total-badge {
  background: #f5a623;
  color: #1a1d23;
  border-radius: 20px;
  padding: 1px 8px;
  font-size: 13px;
  font-weight: 700;
  margin-left: 6px;
}
</style>