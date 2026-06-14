<template>
  <div class="app">
    <header class="header">
      <div class="header-inner">
        <div class="logo">
          <span class="logo-icon">🏗️</span>
          <span class="logo-text">CRM <strong>Спецтехника</strong></span>
        </div>
        <nav class="nav">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            class="nav-btn"
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            {{ tab.icon }} {{ tab.label }}
          </button>
        </nav>
      </div>
    </header>

    <main class="main">
      <OrdersView v-if="activeTab === 'orders'" />
      <ClientsView v-if="activeTab === 'clients'" />
      <EquipmentView v-if="activeTab === 'equipment'" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import OrdersView from './views/OrdersView.vue'
import ClientsView from './views/ClientsView.vue'
import EquipmentView from './views/EquipmentView.vue'

const activeTab = ref('orders')
const tabs = [
  { id: 'orders', label: 'Заявки', icon: '📋' },
  { id: 'clients', label: 'Клиенты', icon: '👤' },
  { id: 'equipment', label: 'Спецтехника', icon: '🚜' },
]
</script>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Segoe UI', system-ui, sans-serif;
  background: #f0f2f5;
  color: #1a1d23;
  min-height: 100vh;
}

.app { min-height: 100vh; display: flex; flex-direction: column; }

.header {
  background: #1a1d23;
  color: #fff;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,.25);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  gap: 24px;
}

.logo { display: flex; align-items: center; gap: 10px; font-size: 18px; white-space: nowrap; }
.logo-icon { font-size: 24px; }
.logo-text strong { color: #f5a623; }

.nav { display: flex; gap: 4px; }

.nav-btn {
  background: transparent;
  border: none;
  color: #9ca3af;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background .15s, color .15s;
}
.nav-btn:hover { background: #2d3139; color: #fff; }
.nav-btn.active { background: #f5a623; color: #1a1d23; font-weight: 700; }

.main { flex: 1; max-width: 1280px; margin: 0 auto; padding: 24px; width: 100%; }

/* Shared card */
.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0,0,0,.08);
  padding: 24px;
}

/* Status badges */
.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: .3px;
}
.badge-new { background: #dbeafe; color: #1d4ed8; }
.badge-in_progress { background: #fef3c7; color: #92400e; }
.badge-completed { background: #d1fae5; color: #065f46; }

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: opacity .15s, transform .1s;
}
.btn:hover { opacity: .88; }
.btn:active { transform: scale(.97); }
.btn-primary { background: #f5a623; color: #1a1d23; }
.btn-danger { background: #fee2e2; color: #dc2626; }
.btn-ghost { background: #f3f4f6; color: #374151; }
.btn-sm { padding: 5px 10px; font-size: 13px; }

/* Form */
.form-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 16px; }
.form-group label { font-size: 13px; font-weight: 600; color: #6b7280; }
.form-control {
  padding: 9px 12px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color .15s;
  width: 100%;
}
.form-control:focus { border-color: #f5a623; }

/* Modal */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,.45);
  display: flex; align-items: center; justify-content: center;
  z-index: 200;
  padding: 16px;
}
.modal {
  background: #fff;
  border-radius: 16px;
  padding: 28px;
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
}
.modal-title { font-size: 18px; font-weight: 700; margin-bottom: 20px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }

/* Table */
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th { text-align: left; padding: 10px 14px; background: #f9fafb; color: #6b7280; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .5px; border-bottom: 1px solid #e5e7eb; }
td { padding: 12px 14px; border-bottom: 1px solid #f3f4f6; vertical-align: middle; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: #fafafa; }

/* Pagination */
.pagination { display: flex; align-items: center; gap: 8px; justify-content: center; margin-top: 20px; flex-wrap: wrap; }
.page-btn {
  width: 34px; height: 34px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  display: flex; align-items: center; justify-content: center;
  transition: all .15s;
}
.page-btn:hover:not(:disabled) { border-color: #f5a623; color: #f5a623; }
.page-btn.active { background: #f5a623; border-color: #f5a623; color: #1a1d23; }
.page-btn:disabled { opacity: .4; cursor: not-allowed; }

/* Toolbar */
.toolbar { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.toolbar-title { font-size: 20px; font-weight: 700; flex: 1; }

/* Empty state */
.empty { text-align: center; padding: 60px 24px; color: #9ca3af; }
.empty-icon { font-size: 48px; margin-bottom: 12px; }
.empty p { font-size: 15px; }

/* Confirm dialog */
.confirm-text { color: #374151; line-height: 1.6; margin-bottom: 8px; }
</style>