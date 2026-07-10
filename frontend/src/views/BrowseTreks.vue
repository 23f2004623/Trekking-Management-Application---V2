<template>
  <div>
    <!-- navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
      <router-link class="navbar-brand" to="/admin">
        <i class="fa-solid fa-mountain-sun text-warning me-2"></i>
        Trek Journey
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#adminNavbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="adminNavbar">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/admin">
              <i class="fa-solid fa-chart-line"></i>
              Dashboard
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link" to="/admin/manage_treks">
              <i class="fa-solid fa-mountain"></i>
              Treks
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link active" to="/admin/manage_staff">
              <i class="fa-solid fa-person-hiking"></i>
              Trekking Staff
            </router-link>
          </li>

          <li class="nav-item">
            <router-link class="nav-link" to="/admin/manage_users">
              <i class="fa-solid fa-users"></i>
              Users
            </router-link>
          </li>
        </ul>

        <button class="btn btn-outline-danger btn-sm" @click="handleLogout">
          <i class="fa-solid fa-right-from-bracket me-1"></i>
          Logout
        </button>
      </div>
    </nav>

    <!-- main area -->
    <div class="main-wrapper">
      <nav class="navbar navbar-light bg-white shadow-sm mb-4 px-4 py-3">
        <div class="container-fluid p-0">
          <h4 class="m-0">Browse Treks</h4>
          <span class="text-muted small">Find and book your next trek</span>
        </div>
      </nav>

      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
        <button class="btn-close float-end" @click="successMessage = ''"></button>
      </div>

      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
        <button class="btn-close float-end" @click="errorMessage = ''"></button>
      </div>

      <!-- filters -->
      <div class="card shadow-sm p-4 mb-4">
        <div class="row g-3">
          <div class="col-md-5">
            <label class="form-label">Search Trek</label>
            <input
              type="text"
              class="form-control"
              v-model="searchQuery"
              placeholder="Search by trek name"
              @input="filterTreks"
            >
          </div>

          <div class="col-md-3">
            <label class="form-label">Difficulty</label>
            <select
              class="form-select"
              v-model="difficultyFilter"
              @change="filterTreks"
            >
              <option value="All">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Moderate">Moderate</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          <div class="col-md-4">
            <label class="form-label">Location</label>
            <select
              class="form-select"
              v-model="locationFilter"
              @change="filterTreks"
            >
              <option value="All">All Locations</option>
              <option v-for="loc in uniqueLocations" :key="loc" :value="loc">
                {{ loc }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- loading -->
      <div v-if="loading" class="text-center p-5">
        <div class="spinner-border text-primary"></div>
      </div>

      <!-- no treks -->
      <div v-else-if="paginatedTreks.length == 0" class="card shadow-sm text-center p-5">
        <i class="fa-solid fa-mountain-sun text-muted fa-3x mb-3"></i>
        <p class="text-muted">No treks found.</p>
      </div>

      <!-- treks -->
      <div v-else>
        <div class="row g-4 mb-4">
          <div
            v-for="trek in paginatedTreks"
            :key="trek.id"
            class="col-md-4"
          >
            <div class="card shadow-sm h-100">
              <img
                :src="trek.image_url || 'https://picsum.photos/400/220?random=' + (trek.id + 50)"
                @error="$event.target.src='https://picsum.photos/400/220?random=' + (trek.id + 50)"
                class="card-img-top"
                style="height: 180px; object-fit: cover;"
              >

              <div class="card-body">
                <div class="d-flex justify-content-between mb-2">
                  <span class="badge" :class="getDifficultyClass(trek.difficulty)">
                    {{ trek.difficulty }}
                  </span>

                  <small class="text-muted">
                    {{ trek.duration_days }} Days
                  </small>
                </div>

                <h5>{{ trek.name }}</h5>

                <p class="text-muted small">
                  <i class="fa-solid fa-location-dot text-danger me-1"></i>
                  {{ trek.location }}
                </p>

                <p class="text-muted small line-clamp">
                  {{ trek.description || 'No description available.' }}
                </p>
              </div>

              <div class="card-footer bg-white">
                <div class="d-flex justify-content-between align-items-center">
                  <small>
                    <b>{{ trek.available_slots }}</b> slots left
                  </small>

                  <button
                    class="btn btn-outline-primary btn-sm"
                    @click="viewTrekDetails(trek)"
                  >
                    View Details
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- pagination -->
        <nav
          v-if="totalPages > 1"
          class="d-flex justify-content-between align-items-center bg-white p-3 shadow-sm"
        >
          <span class="text-muted small">
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }}
            to {{ Math.min(currentPage * itemsPerPage, filteredTreks.length) }}
            of {{ filteredTreks.length }} treks
          </span>

          <ul class="pagination pagination-sm m-0">
            <li class="page-item" :class="{ disabled: currentPage == 1 }">
              <button class="page-link" @click="currentPage--">
                Previous
              </button>
            </li>

            <li
              v-for="page in totalPages"
              :key="page"
              class="page-item"
              :class="{ active: currentPage == page }"
            >
              <button class="page-link" @click="currentPage = page">
                {{ page }}
              </button>
            </li>

            <li class="page-item" :class="{ disabled: currentPage == totalPages }">
              <button class="page-link" @click="currentPage++">
                Next
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- details modal -->
    <div
      class="modal fade"
      id="detailsModal"
      tabindex="-1"
      ref="detailsModal"
    >
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">
              {{ selectedTrek.name }}
            </h5>

            <button
              type="button"
              class="btn-close btn-close-white"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <div class="modal-body">
            <div class="row g-4">
              <div class="col-md-5">
                <img
                  :src="selectedTrek.image_url || 'https://picsum.photos/400/300?random=' + (selectedTrek.id + 100)"
                  @error="$event.target.src='https://picsum.photos/400/300?random=' + (selectedTrek.id + 100)"
                  class="img-fluid rounded mb-3"
                >

                <div class="bg-light p-3 rounded">
                  <p><b>Location:</b> {{ selectedTrek.location }}</p>

                  <p>
                    <b>Difficulty:</b>
                    <span class="badge" :class="getDifficultyClass(selectedTrek.difficulty)">
                      {{ selectedTrek.difficulty }}
                    </span>
                  </p>

                  <p><b>Duration:</b> {{ selectedTrek.duration_days }} Days</p>

                  <p>
                    <b>Available Slots:</b>
                    {{ selectedTrek.available_slots }} / {{ selectedTrek.total_slots }}
                  </p>

                  <p>
                    <b>Status:</b>
                    <span class="badge bg-success">Open</span>
                  </p>
                </div>
              </div>

              <div class="col-md-7">
                <h6>Expedition Dates</h6>

                <div class="bg-light p-3 rounded mb-4">
                  <p>
                    <b>Start Date:</b> {{ selectedTrek.start_date }}
                  </p>
                  <p class="mb-0">
                    <b>End Date:</b> {{ selectedTrek.end_date }}
                  </p>
                </div>

                <h6>Trek Guide / Staff</h6>

                <div class="border p-3 rounded mb-4">
                  <i class="fa-solid fa-user-tie text-primary me-2"></i>
                  {{ selectedTrek.assigned_staff_name || 'Coordinator' }}
                </div>

                <h6>Description</h6>

                <p class="text-muted small">
                  {{ selectedTrek.description || 'No description available. Wear warm clothes, hiking shoes and carry water.' }}
                </p>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-outline-secondary"
              data-bs-dismiss="modal"
            >
              Cancel
            </button>

            <button
              v-if="selectedTrek.available_slots > 0"
              type="button"
              class="btn btn-primary"
              @click="confirmBooking(selectedTrek.id)"
            >
              Book Trek
            </button>

            <button
              v-else
              type="button"
              class="btn btn-secondary"
              disabled
            >
              Fully Booked
            </button>
          </div>
        </div>
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
      uniqueLocations: [],

      searchQuery: '',
      difficultyFilter: 'All',
      locationFilter: 'All',

      currentPage: 1,
      itemsPerPage: 6,
      totalPages: 1,

      selectedTrek: {},
      bsModal: null,

      loading: true,
      successMessage: '',
      errorMessage: ''
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
        let response = await window.apiFetch('/api/user/treks')
        let data = await response.json()

        if (response.ok) {
          this.treks = data

          let locations = data.map(function(trek) {
            return trek.location
          })

          this.uniqueLocations = [...new Set(locations)]

          this.filterTreks()
        }
      } catch (error) {
        console.log(error)
      }

      this.loading = false
    },

    filterTreks() {
      let result = this.treks

      if (this.difficultyFilter != 'All') {
        result = result.filter((trek) => {
          return trek.difficulty == this.difficultyFilter
        })
      }

      if (this.locationFilter != 'All') {
        result = result.filter((trek) => {
          return trek.location == this.locationFilter
        })
      }

      if (this.searchQuery.trim() != '') {
        let searchText = this.searchQuery.toLowerCase()

        result = result.filter((trek) => {
          return trek.name.toLowerCase().includes(searchText)
        })
      }

      this.filteredTreks = result
      this.currentPage = 1
      this.totalPages = Math.ceil(this.filteredTreks.length / this.itemsPerPage)
    },

    viewTrekDetails(trek) {
      this.selectedTrek = trek
      this.bsModal.show()
    },

    async confirmBooking(trekId) {
      this.successMessage = ''
      this.errorMessage = ''

      try {
        let response = await window.apiFetch('/api/user/bookings', {
          method: 'POST',
          body: {
            trek_id: trekId
          }
        })

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message
          this.bsModal.hide()
          this.fetchTreks()
        } else {
          this.errorMessage = data.message
          this.bsModal.hide()
        }
      } catch (error) {
        this.errorMessage = 'Failed to book trek.'
        this.bsModal.hide()
      }
    },

    getDifficultyClass(diff) {
      if (diff == 'Easy') {
        return 'badge-easy'
      } else if (diff == 'Moderate') {
        return 'badge-moderate'
      } else if (diff == 'Hard') {
        return 'badge-hard'
      } else {
        return 'bg-secondary'
      }
    },

    handleLogout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  },

  mounted() {
    this.bsModal = new bootstrap.Modal(this.$refs.detailsModal)
    this.fetchTreks()
  }
}
</script>

<style scoped>
.line-clamp {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>