import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useCatalogStore = defineStore('catalog', () => {
  const clients = ref([])
  const equipment = ref([])

  async function fetchClients() {
    const res = await api.get('/clients/')
    clients.value = res.data
  }

  async function fetchEquipment() {
    const res = await api.get('/equipment/')
    equipment.value = res.data
  }

  async function createClient(data) {
    const res = await api.post('/clients/', data)
    await fetchClients()
    return res.data
  }

  async function createEquipment(data) {
    const res = await api.post('/equipment/', data)
    await fetchEquipment()
    return res.data
  }

  async function deleteClient(id) {
    await api.delete(`/clients/${id}`)
    await fetchClients()
  }

  async function deleteEquipment(id) {
    await api.delete(`/equipment/${id}`)
    await fetchEquipment()
  }

  return {
    clients, equipment,
    fetchClients, fetchEquipment,
    createClient, createEquipment,
    deleteClient, deleteEquipment,
  }
})