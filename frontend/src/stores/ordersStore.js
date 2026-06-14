import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useOrdersStore = defineStore('orders', () => {
  const orders = ref([])
  const total = ref(0)
  const pages = ref(1)
  const loading = ref(false)
  const currentPage = ref(1)
  const pageSize = ref(10)
  const filterStatus = ref('')
  const sortOrder = ref('desc')

  async function fetchOrders() {
    loading.value = true
    try {
      const params = {
        page: currentPage.value,
        page_size: pageSize.value,
        sort_order: sortOrder.value,
      }
      if (filterStatus.value) params.status = filterStatus.value
      const res = await api.get('/orders/', { params })
      orders.value = res.data.items
      total.value = res.data.total
      pages.value = res.data.pages
    } finally {
      loading.value = false
    }
  }

  async function createOrder(data) {
    const res = await api.post('/orders/', data)
    await fetchOrders()
    return res.data
  }

  async function updateOrder(id, data) {
    const res = await api.put(`/orders/${id}`, data)
    await fetchOrders()
    return res.data
  }

  async function deleteOrder(id) {
    await api.delete(`/orders/${id}`)
    await fetchOrders()
  }

  return {
    orders, total, pages, loading,
    currentPage, pageSize, filterStatus, sortOrder,
    fetchOrders, createOrder, updateOrder, deleteOrder,
  }
})