<template>
  <div>
    <!-- navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
      <router-link class="navbar-brand" to="/staff">
        <i class="fa-solid fa-mountain-sun text-warning me-2"></i>
        Trek Journey
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#staffNavbar"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="staffNavbar">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/staff">
              <i class="fa-solid fa-table-columns me-1"></i>
              My Dashboard
            </router-link>
          </li>

          <li class="nav-item">
            <span class="nav-link active">
              <i class="fa-solid fa-mountain me-1"></i>
              Manage Trek
            </span>
          </li>
        </ul>

        <button class="btn btn-outline-danger btn-sm" @click="handleLogout">
          <i class="fa-solid fa-right-from-bracket me-1"></i>
          Logout
        </button>
      </div>
    </nav>

    <!-- main content -->
    <div class="container-fluid p-4">
      <!-- page heading -->
      <div class="bg-white shadow-sm p-3 mb-4">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <router-link
              to="/staff"
              class="text-decoration-none text-muted small"
            >
              <i class="fa-solid fa-arrow-left me-1"></i>
              Back to Dashboard
            </router-link>

            <h4 class="mt-2 mb-0">
              Manage Trek: {{ trek.name }}
            </h4>
          </div>

          <span class="badge bg-secondary">
            Trek ID: #{{ trek.id }}
          </span>
        </div>
      </div>

      <!-- success message -->
      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}

        <button
          class="btn-close float-end"
          @click="successMessage = ''"
        ></button>
      </div>

      <!-- error message -->
      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}

        <button
          class="btn-close float-end"
          @click="errorMessage = ''"
        ></button>
      </div>

      <!-- loading -->
      <div v-if="loading" class="text-center p-5">
        <div class="spinner-border text-primary"></div>
      </div>

      <div v-else class="row g-4">
        <!-- trek details -->
        <div class="col-lg-5">
          <div class="card shadow-sm p-4">
            <h5 class="border-bottom pb-2 mb-4">
              <i class="fa-solid fa-mountain text-primary me-2"></i>
              Trek Details
            </h5>

            <div class="mb-3">
              <label class="text-muted small">Location</label>
              <p class="mb-0">
                {{ trek.location }}
              </p>
            </div>

            <div class="row mb-3">
              <div class="col-6">
                <label class="text-muted small">Difficulty</label>
                <br>

                <span
                  class="badge"
                  :class="getDifficultyClass(trek.difficulty)"
                >
                  {{ trek.difficulty }}
                </span>
              </div>

              <div class="col-6">
                <label class="text-muted small">Duration</label>
                <p class="mb-0">
                  {{ trek.duration_days }} Days
                </p>
              </div>
            </div>

            <div class="row mb-3">
              <div class="col-6">
                <label class="text-muted small">Start Date</label>
                <p class="mb-0">
                  {{ trek.start_date }}
                </p>
              </div>

              <div class="col-6">
                <label class="text-muted small">End Date</label>
                <p class="mb-0">
                  {{ trek.end_date }}
                </p>
              </div>
            </div>

            <div class="mb-4">
              <label class="text-muted small">Description</label>

              <p class="text-muted small mb-0">
                {{ trek.description || 'No description provided.' }}
              </p>
            </div>

            <!-- update form -->
            <h5 class="border-top pt-3 mb-3">
              <i class="fa-solid fa-pen-to-square text-primary me-2"></i>
              Update Trek
            </h5>

            <form @submit.prevent="updateTrek">
              <div class="mb-3">
                <label class="form-label">
                  Available Slots
                </label>

                <div class="input-group">
                  <input
                    type="number"
                    class="form-control"
                    v-model.number="form.available_slots"
                    min="0"
                    :max="trek.total_slots"
                    required
                  >

                  <span class="input-group-text">
                    / {{ trek.total_slots }}
                  </span>
                </div>
              </div>

              <div class="mb-4">
                <label class="form-label">
                  Trek Status
                </label>

                <select
                  class="form-select"
                  v-model="form.status"
                  required
                >
                  <option value="Open">Open</option>
                  <option value="Closed">Closed</option>
                  <option value="Pending">Pending</option>
                  <option value="Completed">Completed</option>
                </select>
              </div>

              <div class="d-flex gap-2">
                <button
                  type="submit"
                  class="btn btn-primary w-100"
                  :disabled="updating"
                >
                  <span
                    v-if="updating"
                    class="spinner-border spinner-border-sm me-2"
                  ></span>

                  Update Trek
                </button>

                <button
                  v-if="trek.status != 'Completed'"
                  type="button"
                  class="btn btn-success w-100"
                  @click="markCompleted"
                >
                  Mark Completed
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- participant list -->
        <div class="col-lg-7">
          <div class="card shadow-sm p-4 h-100">
            <h5 class="border-bottom pb-2 mb-3">
              <i class="fa-solid fa-users text-primary me-2"></i>
              Participants ({{ participants.length }})
            </h5>

            <div
              v-if="participants.length == 0"
              class="text-center p-5"
            >
              <i class="fa-solid fa-users-slash text-muted fa-3x mb-3"></i>

              <p class="text-muted">
                No participants have booked this trek.
              </p>
            </div>

            <div v-else class="table-responsive">
              <table class="table table-hover">
                <thead class="table-light">
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Contact</th>
                    <th>Booking Date</th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="participant in participants"
                    :key="participant.booking_id"
                  >
                    <td>
                      {{ participant.full_name }}
                    </td>

                    <td>
                      {{ participant.email }}
                    </td>

                    <td>
                      {{ participant.contact_number || 'N/A' }}
                    </td>

                    <td>
                      {{ participant.booking_date }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },

  data() {
    return {
      trek: {},
      participants: [],

      loading: true,
      updating: false,

      successMessage: '',
      errorMessage: '',

      form: {
        available_slots: 0,
        status: 'Open'
      }
    }
  },

  methods: {
    async fetchTrekData() {
      this.loading = true

      try {
        let trekResponse = await window.apiFetch(
          '/api/staff/treks/' + this.id
        )

        let trekData = await trekResponse.json()

        if (trekResponse.ok) {
          this.trek = trekData

          this.form.available_slots = trekData.available_slots
          this.form.status = trekData.status

          let participantResponse = await window.apiFetch(
            '/api/staff/treks/' + this.id + '/participants'
          )

          let participantData = await participantResponse.json()

          if (participantResponse.ok) {
            this.participants = participantData
          }
        } else {
          this.errorMessage = trekData.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to load trek details.'
      }

      this.loading = false
    },

    async updateTrek() {
      this.updating = true
      this.errorMessage = ''
      this.successMessage = ''

      try {
        let response = await window.apiFetch(
          '/api/staff/treks/' + this.id,
          {
            method: 'PUT',
            body: this.form
          }
        )

        let data = await response.json()

        if (response.ok) {
          this.successMessage = 'Trek updated successfully.'
          this.fetchTrekData()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to update trek.'
      }

      this.updating = false
    },

    async markCompleted() {
      let check = confirm(
        'Are you sure you want to mark this trek as completed?'
      )

      if (check == false) {
        return
      }

      this.errorMessage = ''
      this.successMessage = ''

      try {
        let response = await window.apiFetch(
          '/api/staff/treks/' + this.id + '/complete',
          {
            method: 'PUT'
          }
        )

        let data = await response.json()

        if (response.ok) {
          this.successMessage = 'Trek marked as completed.'
          this.fetchTrekData()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to mark trek as completed.'
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

  created() {
    this.fetchTrekData()
  }
}
</script>