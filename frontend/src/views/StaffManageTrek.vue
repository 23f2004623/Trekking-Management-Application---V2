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
        to="/staff"
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
          gap: 7px;
        "
      >
        <router-link
          to="/staff"
          style="
            color: #d7d7df;
            text-decoration: none;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          My Dashboard
        </router-link>

        <span
          style="
            color: white;
            background-color: #0d6efd;
            padding: 9px 13px;
            border-radius: 5px;
            font-size: 14px;
          "
        >
          Manage Trek
        </span>

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
          <router-link
            to="/staff"
            style="
              color: #6c757d;
              text-decoration: none;
              font-size: 13px;
            "
          >
            ← Back to Dashboard
          </router-link>

          <h2
            style="
              margin: 8px 0 0 0;
              font-size: 24px;
              color: #222;
            "
          >
            Manage Trek: {{ trek.name }}
          </h2>
        </div>

        <span
          style="
            background-color: #6c757d;
            color: white;
            padding: 7px 13px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
          "
        >
          Trek ID: #{{ trek.id }}
        </span>
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

      <!-- loading -->
      <div
        v-if="loading"
        style="
          background-color: white;
          padding: 60px 20px;
          border-radius: 8px;
          text-align: center;
          color: #0d6efd;
          font-size: 15px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        "
      >
        Loading trek details...
      </div>

      <div
        v-else
        style="
          display: flex;
          gap: 22px;
          align-items: flex-start;
          flex-wrap: wrap;
        "
      >
        <!-- trek details and update form -->
        <div
          style="
            flex: 1;
            min-width: 340px;
            background-color: white;
            border-radius: 8px;
            padding: 22px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            box-sizing: border-box;
          "
        >
          <h3
            style="
              margin: 0 0 20px 0;
              font-size: 19px;
              color: #222;
              border-bottom: 1px solid #e6e8eb;
              padding-bottom: 12px;
            "
          >
            Trek Details
          </h3>

          <div style="margin-bottom: 16px;">
            <p :style="smallHeadingStyle">Location</p>

            <p
              style="
                margin: 0;
                font-size: 15px;
                color: #333;
              "
            >
              {{ trek.location }}
            </p>
          </div>

          <div
            style="
              display: flex;
              gap: 20px;
              flex-wrap: wrap;
              margin-bottom: 16px;
            "
          >
            <div style="flex: 1; min-width: 130px;">
              <p :style="smallHeadingStyle">Difficulty</p>

              <span :style="getDifficultyStyle(trek.difficulty)">
                {{ trek.difficulty }}
              </span>
            </div>

            <div style="flex: 1; min-width: 130px;">
              <p :style="smallHeadingStyle">Duration</p>

              <p
                style="
                  margin: 0;
                  font-size: 15px;
                  color: #333;
                "
              >
                {{ trek.duration_days }} Days
              </p>
            </div>
          </div>

          <div
            style="
              display: flex;
              gap: 20px;
              flex-wrap: wrap;
              margin-bottom: 16px;
            "
          >
            <div style="flex: 1; min-width: 130px;">
              <p :style="smallHeadingStyle">Start Date</p>

              <p
                style="
                  margin: 0;
                  font-size: 15px;
                  color: #333;
                "
              >
                {{ trek.start_date }}
              </p>
            </div>

            <div style="flex: 1; min-width: 130px;">
              <p :style="smallHeadingStyle">End Date</p>

              <p
                style="
                  margin: 0;
                  font-size: 15px;
                  color: #333;
                "
              >
                {{ trek.end_date }}
              </p>
            </div>
          </div>

          <div style="margin-bottom: 22px;">
            <p :style="smallHeadingStyle">Description</p>

            <p
              style="
                margin: 0;
                color: #777;
                font-size: 13px;
                line-height: 1.6;
              "
            >
              {{ trek.description || 'No description provided.' }}
            </p>
          </div>

          <!-- update section -->
          <h3
            style="
              margin: 0 0 18px 0;
              font-size: 19px;
              color: #222;
              border-top: 1px solid #e6e8eb;
              padding-top: 18px;
            "
          >
            Update Trek
          </h3>

          <form @submit.prevent="updateTrek">
            <div style="margin-bottom: 16px;">
              <label :style="labelStyle">
                Available Slots
              </label>

              <div
                style="
                  display: flex;
                  align-items: stretch;
                "
              >
                <input
                  v-model.number="form.available_slots"
                  type="number"
                  min="0"
                  :max="trek.total_slots"
                  required
                  style="
                    flex: 1;
                    min-width: 0;
                    height: 42px;
                    border: 1px solid #ced4da;
                    border-right: none;
                    border-radius: 5px 0 0 5px;
                    padding: 0 11px;
                    font-size: 14px;
                    color: #222;
                    outline: none;
                    box-sizing: border-box;
                  "
                >

                <span
                  style="
                    background-color: #f1f3f5;
                    border: 1px solid #ced4da;
                    color: #555;
                    display: flex;
                    align-items: center;
                    padding: 0 12px;
                    border-radius: 0 5px 5px 0;
                    font-size: 13px;
                    white-space: nowrap;
                  "
                >
                  / {{ trek.total_slots }} Total
                </span>
              </div>
            </div>

            <div style="margin-bottom: 20px;">
              <label :style="labelStyle">
                Trek Status
              </label>

              <select
                v-model="form.status"
                required
                :style="inputStyle"
              >
                <option value="Open">Open</option>
                <option value="Closed">Closed</option>
                <option value="Pending">Pending</option>
                <option value="Ongoing">Ongoing</option>
                <option value="Completed">Completed</option>
              </select>
            </div>

            <div
              style="
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
              "
            >
              <button
                type="submit"
                :disabled="updating"
                :style="{
                  flex: '1',
                  minWidth: '150px',
                  backgroundColor: updating ? '#7baaf7' : '#0d6efd',
                  color: 'white',
                  border: 'none',
                  padding: '10px 14px',
                  borderRadius: '5px',
                  cursor: updating ? 'not-allowed' : 'pointer',
                  fontWeight: 'bold'
                }"
              >
                {{ updating ? 'Updating...' : 'Update Trek' }}
              </button>

              <button
                v-if="trek.status != 'Completed'"
                type="button"
                @click="markCompleted"
                style="
                  flex: 1;
                  min-width: 150px;
                  background-color: #198754;
                  color: white;
                  border: none;
                  padding: 10px 14px;
                  border-radius: 5px;
                  cursor: pointer;
                  font-weight: bold;
                "
              >
                Mark Completed
              </button>
            </div>
          </form>
        </div>

        <!-- participants -->
        <div
          style="
            flex: 1.5;
            min-width: 450px;
            background-color: white;
            border-radius: 8px;
            padding: 22px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            box-sizing: border-box;
          "
        >
          <h3
            style="
              margin: 0 0 20px 0;
              font-size: 19px;
              color: #222;
              border-bottom: 1px solid #e6e8eb;
              padding-bottom: 12px;
            "
          >
            Participants ({{ participants.length }})
          </h3>

          <div
            v-if="participants.length == 0"
            style="
              text-align: center;
              padding: 60px 20px;
              color: #777;
              font-size: 14px;
            "
          >
            <div
              style="
                font-size: 35px;
                color: #aaa;
                margin-bottom: 12px;
              "
            >
              👥
            </div>

            No participants have booked this trek.
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
                min-width: 700px;
                border-collapse: collapse;
              "
            >
              <thead>
                <tr style="background-color: #f5f6f8;">
                  <th :style="headingStyle">Name</th>
                  <th :style="headingStyle">Email</th>
                  <th :style="headingStyle">Contact</th>
                  <th :style="headingStyle">Booking Date</th>
                </tr>
              </thead>

              <tbody>
                <tr
                  v-for="participant in participants"
                  :key="participant.booking_id"
                  style="border-bottom: 1px solid #e8ebee;"
                >
                  <td :style="cellStyle">
                    <b style="color: #222;">
                      {{ participant.full_name }}
                    </b>
                  </td>

                  <td :style="cellStyle">
                    {{ participant.email }}
                  </td>

                  <td :style="cellStyle">
                    {{ participant.contact_number || 'N/A' }}
                  </td>

                  <td :style="cellStyle">
                    {{ participant.booking_date }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div
            style="
              margin-top: 20px;
              background-color: #cff4fc;
              color: #055160;
              border: 1px solid #b6effb;
              padding: 12px;
              border-radius: 5px;
              font-size: 13px;
              line-height: 1.5;
            "
          >
            <b>Info:</b> This list shows all users who have booked this trek.
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
      },

      smallHeadingStyle: {
        margin: '0 0 6px 0',
        color: '#777',
        fontSize: '12px',
        fontWeight: 'bold',
        textTransform: 'uppercase'
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
        height: '42px',
        padding: '0 11px',
        border: '1px solid #ced4da',
        borderRadius: '5px',
        fontSize: '14px',
        color: '#222',
        backgroundColor: 'white',
        boxSizing: 'border-box',
        outline: 'none'
      },

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
          } else {
            this.errorMessage =
              participantData.message || 'Failed to load participants.'
          }
        } else {
          this.errorMessage =
            trekData.message || 'Failed to load trek details.'
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

  created() {
    this.fetchTrekData()
  }
}
</script>