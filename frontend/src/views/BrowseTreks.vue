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
        to="/user"
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
          to="/user"
          style="
            color: #d7d7df;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Home
        </router-link>

        <router-link
          to="/user/treks"
          style="
            color: white;
            background-color: #0d6efd;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Browse Treks
        </router-link>

        <router-link
          to="/user/trek_history"
          style="
            color: #d7d7df;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Trekking History
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
        "
      >
        <h2
          style="
            margin: 0 0 5px 0;
            font-size: 24px;
            color: #222;
          "
        >
          Browse Treks
        </h2>

        <p
          style="
            margin: 0;
            color: #777;
            font-size: 13px;
          "
        >
          Find and book your next trekking adventure.
        </p>
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
            background: none;
            border: none;
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
            background: none;
            border: none;
            color: #842029;
            font-size: 18px;
            cursor: pointer;
          "
        >
          ×
        </button>
      </div>

      <!-- filters -->
      <div
        style="
          background-color: white;
          border-radius: 8px;
          padding: 18px;
          margin-bottom: 22px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          display: flex;
          flex-wrap: wrap;
          gap: 15px;
          align-items: flex-end;
        "
      >
        <div
          style="
            flex: 2;
            min-width: 250px;
          "
        >
          <label :style="labelStyle">
            Search Trek
          </label>

          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by trek name"
            @input="filterTreks"
            :style="inputStyle"
          >
        </div>

        <div
          style="
            flex: 1;
            min-width: 180px;
          "
        >
          <label :style="labelStyle">
            Difficulty
          </label>

          <select
            v-model="difficultyFilter"
            @change="filterTreks"
            :style="inputStyle"
          >
            <option value="All">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Moderate">Moderate</option>
            <option value="Hard">Hard</option>
          </select>
        </div>

        <div
          style="
            flex: 1;
            min-width: 200px;
          "
        >
          <label :style="labelStyle">
            Location
          </label>

          <select
            v-model="locationFilter"
            @change="filterTreks"
            :style="inputStyle"
          >
            <option value="All">All Locations</option>

            <option
              v-for="location in uniqueLocations"
              :key="location"
              :value="location"
            >
              {{ location }}
            </option>
          </select>
        </div>
      </div>

      <!-- loading -->
      <div
        v-if="loading"
        style="
          background-color: white;
          border-radius: 8px;
          padding: 55px 20px;
          text-align: center;
          color: #0d6efd;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        "
      >
        Loading treks...
      </div>

      <!-- no treks -->
      <div
        v-else-if="paginatedTreks.length == 0"
        style="
          background-color: white;
          border-radius: 8px;
          padding: 55px 20px;
          text-align: center;
          color: #777;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        "
      >
        <div
          style="
            font-size: 45px;
            color: #aaa;
            margin-bottom: 10px;
          "
        >
          ▲
        </div>

        <p style="margin: 0;">
          No treks found.
        </p>
      </div>

      <!-- trek cards -->
      <div v-else>
        <div
          style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 22px;
          "
        >
          <div
            v-for="trek in paginatedTreks"
            :key="trek.id"
            style="
              background-color: white;
              border-radius: 8px;
              overflow: hidden;
              box-shadow: 0 2px 9px rgba(0, 0, 0, 0.1);
              display: flex;
              flex-direction: column;
            "
          >
            <img
              :src="trek.image_url || 'https://picsum.photos/400/220?random=' + (trek.id + 50)"
              @error="$event.target.src = 'https://picsum.photos/400/220?random=' + (trek.id + 50)"
              alt="Trek image"
              style="
                width: 100%;
                height: 180px;
                object-fit: cover;
                display: block;
              "
            >

            <div
              style="
                padding: 17px;
                flex: 1;
              "
            >
              <div
                style="
                  display: flex;
                  justify-content: space-between;
                  align-items: center;
                  gap: 10px;
                  margin-bottom: 10px;
                "
              >
                <span :style="getDifficultyStyle(trek.difficulty)">
                  {{ trek.difficulty }}
                </span>

                <span
                  style="
                    color: #777;
                    font-size: 13px;
                  "
                >
                  {{ trek.duration_days }} Days
                </span>
              </div>

              <h3
                style="
                  margin: 0 0 8px 0;
                  color: #222;
                  font-size: 19px;
                "
              >
                {{ trek.name }}
              </h3>

              <p
                style="
                  color: #dc3545;
                  font-size: 13px;
                  margin: 0 0 10px 0;
                "
              >
                Location:
                <span style="color: #666;">
                  {{ trek.location }}
                </span>
              </p>

              <p
                style="
                  color: #777;
                  font-size: 13px;
                  line-height: 1.6;
                  margin: 0;
                  height: 62px;
                  overflow: hidden;
                "
              >
                {{ trek.description || 'No description available.' }}
              </p>
            </div>

            <div
              style="
                border-top: 1px solid #eceff1;
                padding: 14px 17px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
              "
            >
              <span
                style="
                  color: #666;
                  font-size: 13px;
                "
              >
                <b style="color: #222;">
                  {{ trek.available_slots }}
                </b>
                slots left
              </span>

              <button
                type="button"
                @click="viewTrekDetails(trek)"
                style="
                  background-color: white;
                  color: #0d6efd;
                  border: 1px solid #0d6efd;
                  padding: 8px 13px;
                  border-radius: 5px;
                  font-size: 13px;
                  cursor: pointer;
                "
              >
                View Details
              </button>
            </div>
          </div>
        </div>

        <!-- pagination -->
        <div
          v-if="totalPages > 1"
          style="
            background-color: white;
            padding: 15px 18px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
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
              flex-wrap: wrap;
              gap: 5px;
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

    <!-- trek details modal -->
    <div
      v-if="showModal"
      style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.58);
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
        box-sizing: border-box;
        z-index: 1000;
      "
      @click.self="closeModal"
    >
      <div
        style="
          width: 100%;
          max-width: 850px;
          max-height: 90vh;
          overflow-y: auto;
          background-color: white;
          border-radius: 8px;
          box-shadow: 0 8px 28px rgba(0, 0, 0, 0.3);
        "
      >
        <!-- modal header -->
        <div
          style="
            background-color: #0d6efd;
            color: white;
            padding: 16px 20px;
            border-radius: 8px 8px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
          "
        >
          <h3
            style="
              margin: 0;
              color: white;
              font-size: 20px;
            "
          >
            {{ selectedTrek.name }}
          </h3>

          <button
            type="button"
            @click="closeModal"
            style="
              background: none;
              color: white;
              border: none;
              font-size: 23px;
              cursor: pointer;
            "
          >
            ×
          </button>
        </div>

        <!-- modal body -->
        <div
          style="
            padding: 22px;
            display: flex;
            flex-wrap: wrap;
            gap: 22px;
          "
        >
          <!-- left modal side -->
          <div
            style="
              flex: 1;
              min-width: 270px;
            "
          >

            <div
              style="
                background-color: #f6f7f8;
                padding: 15px;
                border-radius: 6px;
                font-size: 14px;
                line-height: 1.6;
              "
            >
              <p style="margin: 0 0 8px 0;">
                <b>Location:</b>
                {{ selectedTrek.location }}
              </p>

              <p style="margin: 0 0 8px 0;">
                <b>Difficulty:</b>

                <span :style="getDifficultyStyle(selectedTrek.difficulty)">
                  {{ selectedTrek.difficulty }}
                </span>
              </p>

              <p style="margin: 0 0 8px 0;">
                <b>Duration:</b>
                {{ selectedTrek.duration_days }} Days
              </p>

              <p style="margin: 0 0 8px 0;">
                <b>Available Slots:</b>
                {{ selectedTrek.available_slots }}
                /
                {{ selectedTrek.total_slots }}
              </p>

              <p style="margin: 0;">
                <b>Status:</b>

                <span
                  style="
                    display: inline-block;
                    background-color: #198754;
                    color: white;
                    padding: 5px 9px;
                    border-radius: 20px;
                    font-size: 11px;
                    font-weight: bold;
                  "
                >
                  Open
                </span>
              </p>
            </div>
          </div>

          <!-- right modal side -->
          <div
            style="
              flex: 1.4;
              min-width: 280px;
            "
          >
            <h4
              style="
                margin: 0 0 10px 0;
                color: #333;
                font-size: 16px;
              "
            >
              Expedition Dates
            </h4>

            <div
              style="
                background-color: #f6f7f8;
                padding: 14px;
                border-radius: 6px;
                margin-bottom: 20px;
              "
            >
              <p style="margin: 0 0 8px 0; font-size: 14px;">
                <b>Start Date:</b>
                {{ selectedTrek.start_date }}
              </p>

              <p style="margin: 0; font-size: 14px;">
                <b>End Date:</b>
                {{ selectedTrek.end_date }}
              </p>
            </div>

            <h4
              style="
                margin: 0 0 10px 0;
                color: #333;
                font-size: 16px;
              "
            >
              Trek Guide
            </h4>

            <div
              style="
                border: 1px solid #dfe3e6;
                padding: 14px;
                border-radius: 6px;
                margin-bottom: 20px;
                color: #333;
                font-size: 14px;
              "
            >
              {{ selectedTrek.assigned_staff_name || 'Coordinator' }}
            </div>

            <h4
              style="
                margin: 0 0 10px 0;
                color: #333;
                font-size: 16px;
              "
            >
              Description
            </h4>

            <p
              style="
                color: #666;
                font-size: 14px;
                line-height: 1.7;
                margin: 0;
              "
            >
              {{
                selectedTrek.description ||
                'No description available. Wear warm clothes, hiking shoes and carry water.'
              }}
            </p>
          </div>
        </div>

        <!-- modal footer -->
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
            v-if="selectedTrek.available_slots > 0"
            type="button"
            @click="confirmBooking(selectedTrek.id)"
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
            Book Trek
          </button>

          <button
            v-else
            type="button"
            disabled
            style="
              background-color: #888;
              color: white;
              border: none;
              padding: 9px 17px;
              border-radius: 5px;
              cursor: not-allowed;
            "
          >
            Fully Booked
          </button>
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
      showModal: false,

      loading: true,
      successMessage: '',
      errorMessage: '',

      labelStyle: {
        display: 'block',
        color: '#333',
        fontSize: '14px',
        fontWeight: 'bold',
        marginBottom: '6px'
      },

      inputStyle: {
        width: '100%',
        height: '42px',
        padding: '0 11px',
        border: '1px solid #ced4da',
        borderRadius: '5px',
        fontSize: '14px',
        color: '#222',
        backgroundColor: '#fafafa',
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
        let response = await window.apiFetch('/api/user/treks')
        let data = await response.json()

        if (response.ok) {
          this.treks = data

          let locations = data.map(function(trek) {
            return trek.location
          })

          this.uniqueLocations = [...new Set(locations)]

          this.filterTreks()
        } else {
          this.errorMessage = data.message || 'Failed to load treks.'
        }
      } catch (error) {
        this.errorMessage = 'Failed to load treks.'
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
      this.totalPages = Math.ceil(
        this.filteredTreks.length / this.itemsPerPage
      )
    },

    viewTrekDetails(trek) {
      this.selectedTrek = trek
      this.showModal = true
    },

    closeModal() {
      this.showModal = false
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
          this.closeModal()
          this.fetchTreks()
        } else {
          this.errorMessage = data.message
          this.closeModal()
        }
      } catch (error) {
        this.errorMessage = 'Failed to book trek.'
        this.closeModal()
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

    handleLogout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  },

  mounted() {
    this.fetchTreks()
  }
}
</script>