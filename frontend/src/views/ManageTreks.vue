<template>
  <div
    style="
      min-height: 100vh;
      background-color: #f2f4f7;
      font-family: Arial, Helvetica, sans-serif;
      color: #222;
    "
  >
    <!-- navbar -->
    <nav
      style="
        min-height: 65px;
        background-color: #1a1a2e;
        padding: 0 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        box-sizing: border-box;
      "
    >
      <router-link
        to="/admin"
        style="
          color: white;
          text-decoration: none;
          font-size: 21px;
          font-weight: bold;
          padding: 18px 0;
        "
      >
        <span style="color: #ffc107; margin-right: 7px;">▲</span>
        Trek Journey
      </router-link>

      <div
        style="
          display: flex;
          align-items: center;
          flex-wrap: wrap;
          gap: 5px;
        "
      >
        <router-link
          to="/admin"
          style="
            color: #d7d7df;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Dashboard
        </router-link>

        <router-link
          to="/admin/manage_treks"
          style="
            color: white;
            background-color: #0d6efd;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Treks
        </router-link>

        <router-link
          to="/admin/manage_staff"
          style="
            color: #d7d7df;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Trekking Staff
        </router-link>

        <router-link
          to="/admin/manage_users"
          style="
            color: #d7d7df;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Users
        </router-link>

        <button
          type="button"
          @click="handleLogout"
          style="
            background-color: transparent;
            color: #ff6b75;
            border: 1px solid #dc3545;
            padding: 8px 13px;
            border-radius: 5px;
            font-size: 14px;
            cursor: pointer;
            margin-left: 8px;
          "
        >
          Logout
        </button>
      </div>
    </nav>

    <!-- main content -->
    <div
      style="
        width: 100%;
        max-width: 1450px;
        margin: auto;
        padding: 25px;
        box-sizing: border-box;
      "
    >
      <!-- page heading -->
      <div
        style="
          background-color: white;
          padding: 18px 22px;
          border-radius: 8px;
          margin-bottom: 20px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 12px;
        "
      >
        <div>
          <h2
            style="
              margin: 0 0 5px 0;
              font-size: 24px;
              color: #222;
            "
          >
            Manage Treks
          </h2>

          <p
            style="
              margin: 0;
              color: #777;
              font-size: 13px;
            "
          >
            Add, update and manage trekking expeditions.
          </p>
        </div>

        <button
          type="button"
          @click="openCreateModal"
          style="
            background-color: #0d6efd;
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
          "
        >
          + Add New Trek
        </button>
      </div>

      <!-- search and filter -->
      <div
        style="
          background-color: white;
          border-radius: 8px;
          padding: 16px;
          margin-bottom: 20px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          display: flex;
          gap: 12px;
          flex-wrap: wrap;
        "
      >
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search treks by name or location"
          @input="handleSearch"
          style="
            flex: 1;
            min-width: 250px;
            height: 42px;
            padding: 0 12px;
            border: 1px solid #ced4da;
            border-radius: 5px;
            font-size: 14px;
            color: #222;
            background-color: #fafafa;
            outline: none;
            box-sizing: border-box;
          "
        >

        <select
          v-model="difficultyFilter"
          @change="filterTreks"
          style="
            width: 220px;
            height: 42px;
            padding: 0 10px;
            border: 1px solid #ced4da;
            border-radius: 5px;
            font-size: 14px;
            color: #333;
            background-color: #fafafa;
            outline: none;
          "
        >
          <option value="All">All Difficulties</option>
          <option value="Easy">Easy</option>
          <option value="Moderate">Moderate</option>
          <option value="Hard">Hard</option>
        </select>
      </div>

      <!-- success message -->
      <div
        v-if="successMessage"
        style="
          background-color: #d1e7dd;
          color: #0f5132;
          border: 1px solid #badbcc;
          padding: 12px;
          border-radius: 5px;
          margin-bottom: 18px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 14px;
        "
      >
        <span>{{ successMessage }}</span>

        <button
          type="button"
          @click="successMessage = ''"
          style="
            border: none;
            background: none;
            color: #0f5132;
            font-size: 18px;
            cursor: pointer;
          "
        >
          ×
        </button>
      </div>

      <!-- error message -->
      <div
        v-if="errorMessage"
        style="
          background-color: #f8d7da;
          color: #842029;
          border: 1px solid #f5c2c7;
          padding: 12px;
          border-radius: 5px;
          margin-bottom: 18px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 14px;
        "
      >
        <span>{{ errorMessage }}</span>

        <button
          type="button"
          @click="errorMessage = ''"
          style="
            border: none;
            background: none;
            color: #842029;
            font-size: 18px;
            cursor: pointer;
          "
        >
          ×
        </button>
      </div>

      <!-- trek list -->
      <div
        style="
          background-color: white;
          border-radius: 8px;
          padding: 22px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        "
      >
        <div
          v-if="loading"
          style="
            text-align: center;
            padding: 50px;
            color: #0d6efd;
            font-size: 15px;
          "
        >
          Loading treks...
        </div>

        <div
          v-else-if="paginatedTreks.length == 0"
          style="
            text-align: center;
            padding: 50px;
            color: #777;
            font-size: 14px;
          "
        >
          No treks found.
        </div>

        <div
          v-else
          style="
            width: 100%;
            overflow-x: auto;
          "
        >
          <table
            style="
              width: 100%;
              min-width: 1050px;
              border-collapse: collapse;
            "
          >
            <thead>
              <tr style="background-color: #f5f6f8;">
                <th :style="headingStyle">ID</th>
                <th :style="headingStyle">Trek Name</th>
                <th :style="headingStyle">Location</th>
                <th :style="headingStyle">Difficulty</th>
                <th :style="headingStyle">Duration</th>
                <th :style="headingStyle">Slots</th>
                <th :style="headingStyle">Staff</th>
                <th :style="headingStyle">Status</th>
                <th :style="headingStyle">Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="trek in paginatedTreks"
                :key="trek.id"
                style="border-bottom: 1px solid #e8ebee;"
              >
                <td :style="cellStyle">
                  <b>#{{ trek.id }}</b>
                </td>

                <td :style="cellStyle">
                  <b>{{ trek.name }}</b>
                </td>

                <td :style="cellStyle">
                  {{ trek.location }}
                </td>

                <td :style="cellStyle">
                  <span :style="getDifficultyStyle(trek.difficulty)">
                    {{ trek.difficulty }}
                  </span>
                </td>

                <td :style="cellStyle">
                  {{ trek.duration_days }} Days
                </td>

                <td :style="cellStyle">
                  <b>{{ trek.available_slots }}</b>
                  /
                  {{ trek.total_slots }}
                </td>

                <td :style="cellStyle">
                  {{ trek.assigned_staff_name || 'Unassigned' }}
                </td>

                <td :style="cellStyle">
                  <span :style="getStatusStyle(trek.status)">
                    {{ trek.status }}
                  </span>
                </td>

                <td
                  style="
                    padding: 13px;
                    text-align: center;
                    white-space: nowrap;
                  "
                >
                  <button
                    type="button"
                    @click="openEditModal(trek)"
                    style="
                      background-color: white;
                      color: #555;
                      border: 1px solid #777;
                      padding: 7px 10px;
                      border-radius: 4px;
                      margin-right: 5px;
                      cursor: pointer;
                    "
                  >
                    Edit
                  </button>

                  <button
                    type="button"
                    @click="confirmDelete(trek)"
                    style="
                      background-color: white;
                      color: #dc3545;
                      border: 1px solid #dc3545;
                      padding: 7px 10px;
                      border-radius: 4px;
                      cursor: pointer;
                    "
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- pagination -->
        <div
          v-if="totalPages > 1"
          style="
            margin-top: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
          "
        >
          <span
            style="
              color: #777;
              font-size: 13px;
            "
          >
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }}
            to
            {{ Math.min(currentPage * itemsPerPage, filteredTreks.length) }}
            of {{ filteredTreks.length }} treks
          </span>

          <div
            style="
              display: flex;
              gap: 5px;
              flex-wrap: wrap;
            "
          >
            <button
              type="button"
              @click="previousPage"
              :disabled="currentPage == 1"
              :style="pageButtonStyle(currentPage == 1)"
            >
              Previous
            </button>

            <button
              v-for="page in totalPages"
              :key="page"
              type="button"
              @click="currentPage = page"
              :style="numberButtonStyle(page)"
            >
              {{ page }}
            </button>

            <button
              type="button"
              @click="nextPage"
              :disabled="currentPage == totalPages"
              :style="pageButtonStyle(currentPage == totalPages)"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- custom add/edit modal -->
    <div
      v-if="showModal"
      style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.55);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        padding: 20px;
        box-sizing: border-box;
      "
      @click.self="closeModal"
    >
      <div
        style="
          width: 100%;
          max-width: 800px;
          max-height: 90vh;
          overflow-y: auto;
          background-color: white;
          border-radius: 8px;
          box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
        "
      >
        <!-- modal header -->
        <div
          style="
            background-color: #0d6efd;
            color: white;
            padding: 16px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 8px 8px 0 0;
          "
        >
          <h3
            style="
              margin: 0;
              font-size: 19px;
              color: white;
            "
          >
            {{ isEditing ? 'Edit Trek' : 'Add New Trek' }}
          </h3>

          <button
            type="button"
            @click="closeModal"
            style="
              border: none;
              background: none;
              color: white;
              font-size: 23px;
              cursor: pointer;
            "
          >
            ×
          </button>
        </div>

        <form @submit.prevent="saveTrek">
          <div style="padding: 22px;">
            <div
              style="
                display: flex;
                flex-wrap: wrap;
                gap: 16px;
              "
            >
              <div style="flex: 1; min-width: 250px;">
                <label :style="labelStyle">Trek Name</label>

                <input
                  v-model="form.name"
                  type="text"
                  placeholder="Everest Base Camp"
                  required
                  :style="inputStyle"
                >
              </div>

              <div style="flex: 1; min-width: 250px;">
                <label :style="labelStyle">Location</label>

                <input
                  v-model="form.location"
                  type="text"
                  placeholder="Nepal"
                  required
                  :style="inputStyle"
                >
              </div>

              <div style="flex: 1; min-width: 180px;">
                <label :style="labelStyle">Difficulty</label>

                <select
                  v-model="form.difficulty"
                  required
                  :style="inputStyle"
                >
                  <option value="Easy">Easy</option>
                  <option value="Moderate">Moderate</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>

              <div style="flex: 1; min-width: 180px;">
                <label :style="labelStyle">Duration Days</label>

                <input
                  v-model.number="form.duration_days"
                  type="number"
                  min="1"
                  required
                  :style="inputStyle"
                >
              </div>

              <div style="flex: 1; min-width: 180px;">
                <label :style="labelStyle">Total Slots</label>

                <input
                  v-model.number="form.total_slots"
                  type="number"
                  min="1"
                  required
                  :style="inputStyle"
                >
              </div>

              <div style="flex: 1; min-width: 250px;">
                <label :style="labelStyle">Start Date</label>

                <input
                  v-model="form.start_date"
                  type="date"
                  required
                  :style="inputStyle"
                >
              </div>

              <div style="flex: 1; min-width: 250px;">
                <label :style="labelStyle">End Date</label>

                <input
                  v-model="form.end_date"
                  type="date"
                  required
                  :style="inputStyle"
                >
              </div>

              <div style="flex: 1; min-width: 250px;">
                <label :style="labelStyle">Assigned Staff</label>

                <select
                  v-model="form.assigned_staff_id"
                  :style="inputStyle"
                >
                  <option :value="null">Select Staff</option>

                  <option
                    v-for="staff in staffList"
                    :key="staff.id"
                    :value="staff.id"
                  >
                    {{ staff.full_name }}
                    (Exp: {{ staff.experience || 'N/A' }})
                  </option>
                </select>
              </div>

              <div style="flex: 1; min-width: 250px;">
                <label :style="labelStyle">Status</label>

                <select
                  v-model="form.status"
                  required
                  :style="inputStyle"
                >
                  <option value="Open">Open</option>
                  <option value="Closed">Closed</option>
                  <option value="Pending">Pending</option>
                  <option value="Completed">Completed</option>
                </select>
              </div>

              <div style="width: 100%;">
                <label :style="labelStyle">Description</label>

                <textarea
                  v-model="form.description"
                  rows="3"
                  placeholder="Enter trek details"
                  style="
                    width: 100%;
                    min-height: 90px;
                    padding: 10px 12px;
                    border: 1px solid #ced4da;
                    border-radius: 5px;
                    font-size: 14px;
                    font-family: Arial, Helvetica, sans-serif;
                    box-sizing: border-box;
                    outline: none;
                    resize: vertical;
                  "
                ></textarea>
              </div>
            </div>
          </div>

          <!-- modal buttons -->
          <div
            style="
              padding: 15px 22px;
              background-color: #f6f7f8;
              display: flex;
              justify-content: flex-end;
              gap: 10px;
              border-radius: 0 0 8px 8px;
            "
          >
            <button
              type="button"
              @click="closeModal"
              style="
                background-color: white;
                color: #555;
                border: 1px solid #777;
                padding: 9px 15px;
                border-radius: 5px;
                cursor: pointer;
              "
            >
              Cancel
            </button>

            <button
              type="submit"
              style="
                background-color: #0d6efd;
                color: white;
                border: none;
                padding: 9px 17px;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
              "
            >
              {{ isEditing ? 'Update Trek' : 'Create Trek' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      treks: [],
      filteredTreks: [],
      staffList: [],

      searchQuery: '',
      difficultyFilter: 'All',

      currentPage: 1,
      itemsPerPage: 5,
      totalPages: 1,

      isEditing: false,
      editingTrekId: null,
      showModal: false,

      form: {
        name: '',
        location: '',
        difficulty: 'Easy',
        duration_days: 5,
        total_slots: 20,
        start_date: '',
        end_date: '',
        assigned_staff_id: null,
        status: 'Open',
        description: '',
        image_url: ''
      },

      loading: true,
      successMessage: '',
      errorMessage: '',

      headingStyle: {
        padding: '13px',
        textAlign: 'left',
        color: '#555',
        fontSize: '13px',
        borderBottom: '1px solid #dee2e6',
        whiteSpace: 'nowrap'
      },

      cellStyle: {
        padding: '13px',
        color: '#333',
        fontSize: '14px',
        verticalAlign: 'middle'
      },

      labelStyle: {
        display: 'block',
        color: '#333',
        fontSize: '14px',
        fontWeight: 'bold',
        marginBottom: '6px'
      },

      inputStyle: {
        width: '100%',
        height: '41px',
        padding: '0 11px',
        border: '1px solid #ced4da',
        borderRadius: '5px',
        fontSize: '14px',
        color: '#222',
        backgroundColor: 'white',
        boxSizing: 'border-box',
        outline: 'none'
      }
    }
  },

  computed: {
    paginatedTreks() {
      let start = (this.currentPage - 1) * this.itemsPerPage
      let end = start + this.itemsPerPage

      return this.filteredTreks.slice(start, end)
    }
  },

  methods: {
    async fetchTreks() {
      this.loading = true

      try {
        let response = await window.apiFetch('/api/admin/treks')
        let data = await response.json()

        if (response.ok) {
          this.treks = data
          this.filterTreks()
        } else {
          this.errorMessage = data.message || 'Failed to load treks.'
        }
      } catch (error) {
        this.errorMessage = 'Failed to load treks.'
      }

      this.loading = false
    },

    async fetchStaff() {
      try {
        let response = await window.apiFetch('/api/admin/staff')
        let data = await response.json()

        if (response.ok) {
          this.staffList = data.filter((staff) => {
            return staff.status == 'active'
          })
        }
      } catch (error) {
        console.log(error)
      }
    },

    filterTreks() {
      let result = this.treks

      if (this.difficultyFilter != 'All') {
        result = result.filter((trek) => {
          return trek.difficulty == this.difficultyFilter
        })
      }

      if (this.searchQuery.trim() != '') {
        let searchText = this.searchQuery.toLowerCase()

        result = result.filter((trek) => {
          return (
            trek.name.toLowerCase().includes(searchText) ||
            trek.location.toLowerCase().includes(searchText)
          )
        })
      }

      this.filteredTreks = result
      this.currentPage = 1
      this.totalPages = Math.ceil(
        this.filteredTreks.length / this.itemsPerPage
      )
    },

    handleSearch() {
      this.filterTreks()
    },

    openCreateModal() {
      this.isEditing = false
      this.editingTrekId = null

      this.form = {
        name: '',
        location: '',
        difficulty: 'Easy',
        duration_days: 5,
        total_slots: 20,
        start_date: '',
        end_date: '',
        assigned_staff_id: null,
        status: 'Open',
        description: '',
        image_url: ''
      }

      this.showModal = true
    },

    openEditModal(trek) {
      this.isEditing = true
      this.editingTrekId = trek.id

      this.form = {
        name: trek.name,
        location: trek.location,
        difficulty: trek.difficulty,
        duration_days: trek.duration_days,
        total_slots: trek.total_slots,
        start_date: trek.start_date,
        end_date: trek.end_date,
        assigned_staff_id: trek.assigned_staff_id,
        status: trek.status,
        description: trek.description || '',
        image_url: trek.image_url || ''
      }

      this.showModal = true
    },

    closeModal() {
      this.showModal = false
    },

    async saveTrek() {
      this.errorMessage = ''
      this.successMessage = ''

      let method = 'POST'
      let endpoint = '/api/admin/treks'

      if (this.isEditing == true) {
        method = 'PUT'
        endpoint = '/api/admin/treks/' + this.editingTrekId
      }

      try {
        let response = await window.apiFetch(endpoint, {
          method: method,
          body: this.form
        })

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message
          this.closeModal()
          this.fetchTreks()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to save trek details.'
      }
    },

    async confirmDelete(trek) {
      let check = confirm(
        'Are you sure you want to delete trek "' + trek.name + '"?'
      )

      if (check == false) {
        return
      }

      this.errorMessage = ''
      this.successMessage = ''

      try {
        let response = await window.apiFetch(
          '/api/admin/treks/' + trek.id,
          {
            method: 'DELETE'
          }
        )

        let data = await response.json()

        if (response.ok) {
          this.successMessage = 'Trek deleted successfully.'
          this.fetchTreks()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to delete trek.'
      }
    },

    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage = this.currentPage - 1
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage = this.currentPage + 1
      }
    },

    pageButtonStyle(disabled) {
      return {
        backgroundColor: disabled ? '#eeeeee' : 'white',
        color: disabled ? '#999' : '#0d6efd',
        border: '1px solid #ced4da',
        padding: '7px 11px',
        borderRadius: '4px',
        cursor: disabled ? 'not-allowed' : 'pointer'
      }
    },

    numberButtonStyle(page) {
      return {
        backgroundColor: this.currentPage == page ? '#0d6efd' : 'white',
        color: this.currentPage == page ? 'white' : '#0d6efd',
        border: '1px solid #0d6efd',
        padding: '7px 11px',
        borderRadius: '4px',
        cursor: 'pointer'
      }
    },

    getDifficultyStyle(diff) {
      let backgroundColor = '#6c757d'
      let color = 'white'

      if (diff == 'Easy') {
        backgroundColor = '#198754'
      } else if (diff == 'Moderate') {
        backgroundColor = '#ffc107'
        color = '#222'
      } else if (diff == 'Hard') {
        backgroundColor = '#dc3545'
      }

      return {
        display: 'inline-block',
        backgroundColor: backgroundColor,
        color: color,
        padding: '6px 10px',
        borderRadius: '20px',
        fontSize: '12px',
        fontWeight: 'bold'
      }
    },

    getStatusStyle(status) {
      let backgroundColor = '#6c757d'
      let color = 'white'

      if (status == 'Open') {
        backgroundColor = '#198754'
      } else if (status == 'Closed') {
        backgroundColor = '#dc3545'
      } else if (status == 'Pending') {
        backgroundColor = '#ffc107'
        color = '#222'
      } else if (status == 'Completed') {
        backgroundColor = '#0d6efd'
      }

      return {
        display: 'inline-block',
        backgroundColor: backgroundColor,
        color: color,
        padding: '6px 10px',
        borderRadius: '20px',
        fontSize: '12px',
        fontWeight: 'bold'
      }
    },

    handleLogout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  },

  mounted() {
    this.fetchTreks()
    this.fetchStaff()
  }
}
</script>