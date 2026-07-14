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
          gap: 8px;
        "
      >
        <router-link
          to="/staff"
          :style="{
            color: 'white',
            backgroundColor: $route.path === '/staff' ? '#0d6efd' : 'transparent',
            textDecoration: 'none',
            padding: '9px 13px',
            borderRadius: '5px',
            fontSize: '14px'
          }"
        >
          My Dashboard
        </router-link>

       <router-link
          to="/staff/manage_treks"
          :style="{
            color: 'white',
            backgroundColor: $route.path === '/staff/manage_treks' ? '#0d6efd' : '#6c757d',
            textDecoration: 'none',
            padding: '9px 13px',
            borderRadius: '5px',
            fontSize: '14px'
          }"
        >
          Manage Treks
        </router-link>


        <span
          style="
            color: #d7d7df;
            font-size: 14px;
            margin-left: 10px;
          "
        >
          Welcome, {{ staffName }}
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
            margin-left: 5px;
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
      <!-- heading -->
      <div
        style="
          background-color: white;
          padding: 18px 22px;
          border-radius: 8px;
          margin-bottom: 22px;
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
            My Dashboard
          </h2>

          <p
            style="
              margin: 0;
              color: #777;
              font-size: 13px;
            "
          >
            View and manage your assigned trekking expeditions.
          </p>
        </div>

        <span
          style="
            background-color: #198754;
            color: white;
            padding: 7px 13px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
          "
        >
          Staff Member
        </span>
      </div>

      <!-- loading -->
      <div
        v-if="loading"
        style="
          background-color: white;
          border-radius: 8px;
          padding: 60px 20px;
          text-align: center;
          color: #0d6efd;
          font-size: 15px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        "
      >
        Loading dashboard data...
      </div>

      <div v-else>
        <!-- statistic cards -->
        <div
          style="
            display: flex;
            flex-wrap: wrap;
            gap: 18px;
            margin-bottom: 25px;
          "
        >
          <!-- assigned treks -->
          <div
            style="
              flex: 1;
              min-width: 250px;
              background-color: white;
              border-radius: 8px;
              padding: 20px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
              display: flex;
              justify-content: space-between;
              align-items: center;
              box-sizing: border-box;
            "
          >
            <div>
              <p
                style="
                  color: #777;
                  font-size: 13px;
                  margin: 0 0 8px 0;
                "
              >
                ASSIGNED TREKS
              </p>

              <h2
                style="
                  margin: 0;
                  color: #222;
                  font-size: 30px;
                "
              >
                {{ stats.assigned_treks_count }}
              </h2>
            </div>

            <div
              style="
                width: 52px;
                height: 52px;
                background-color: #dbeafe;
                color: #0d6efd;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 25px;
              "
            >
              ▲
            </div>
          </div>

          <!-- participants -->
          <div
            style="
              flex: 1;
              min-width: 250px;
              background-color: white;
              border-radius: 8px;
              padding: 20px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
              display: flex;
              justify-content: space-between;
              align-items: center;
              box-sizing: border-box;
            "
          >
            <div>
              <p
                style="
                  color: #777;
                  font-size: 13px;
                  margin: 0 0 8px 0;
                "
              >
                TOTAL PARTICIPANTS
              </p>

              <h2
                style="
                  margin: 0;
                  color: #222;
                  font-size: 30px;
                "
              >
                {{ stats.total_participants }}
              </h2>
            </div>

            <div
              style="
                width: 52px;
                height: 52px;
                background-color: #d1e7dd;
                color: #198754;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 24px;
              "
            >
              👥
            </div>
          </div>

          <!-- ongoing treks -->
          <div
            style="
              flex: 1;
              min-width: 250px;
              background-color: white;
              border-radius: 8px;
              padding: 20px;
              box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
              display: flex;
              justify-content: space-between;
              align-items: center;
              box-sizing: border-box;
            "
          >
            <div>
              <p
                style="
                  color: #777;
                  font-size: 13px;
                  margin: 0 0 8px 0;
                "
              >
                ONGOING TREKS
              </p>

              <h2
                style="
                  margin: 0;
                  color: #222;
                  font-size: 30px;
                "
              >
                {{ stats.ongoing_treks_count }}
              </h2>
            </div>

            <div
              style="
                width: 52px;
                height: 52px;
                background-color: #fff3cd;
                color: #b78103;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 24px;
              "
            >
              ↗
            </div>
          </div>
        </div>

        <!-- assigned treks table -->
        <div
          style="
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
            My Assigned Treks
          </h3>

          <!-- no treks -->
          <div
            v-if="assignedTreks.length == 0"
            style="
              background-color: #f8f9fa;
              color: #777;
              border-radius: 6px;
              padding: 40px 20px;
              text-align: center;
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
              ▲
            </div>

            You are not assigned to any trek. Please contact admin.
          </div>

          <!-- trek table -->
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
                min-width: 950px;
                border-collapse: collapse;
              "
            >
              <thead>
                <tr style="background-color: #f5f6f8;">
                  <th :style="headingStyle">Trek Name</th>
                  <th :style="headingStyle">Location</th>
                  <th :style="headingStyle">Difficulty</th>
                  <th :style="headingStyle">Trek Dates</th>
                  <th :style="headingStyle">Available Slots</th>
                  <th :style="headingStyle">Status</th>
                  <th :style="headingStyle">Action</th>
                </tr>
              </thead>

              <tbody>
                <tr
                  v-for="trek in assignedTreks"
                  :key="trek.id"
                  style="border-bottom: 1px solid #e8ebee;"
                >
                  <td :style="cellStyle">
                    <b style="color: #222;">
                      {{ trek.name }}
                    </b>
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
                    <div>
                      {{ trek.start_date }}
                    </div>

                    <small style="color: #777;">
                      to {{ trek.end_date }}
                    </small>
                  </td>

                  <td :style="cellStyle">
                    <b>{{ trek.available_slots }}</b>
                    /
                    {{ trek.total_slots }}
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
                    <router-link
                      :to="'/staff/manage_treks/' + trek.id"
                      style="
                        display: inline-block;
                        background-color: #0d6efd;
                        color: white;
                        text-decoration: none;
                        padding: 8px 13px;
                        border-radius: 5px;
                        font-size: 13px;
                        font-weight: bold;
                      "
                    >
                      Manage →
                    </router-link>
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
            <b>Info:</b> You can only manage treks assigned to your staff account.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import router from '../router';

export default {
  data() {
    return {
      staffName: '',

      stats: {
        assigned_treks_count: 0,
        total_participants: 0,
        ongoing_treks_count: 0
      },

      assignedTreks: [],
      loading: true,

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
    async fetchDashboardData() {
      this.loading = true

      try {
        let response = await window.apiFetch('/api/staff/dashboard')
        let data = await response.json()

        if (response.ok) {
          this.stats = data.stats
          this.assignedTreks = data.assigned_treks
        }
      } catch (error) {
        console.log(error)
      }

      this.loading = false
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

      if (status == 'Upcoming') {
        backgroundColor = '#17a2b8'
      } else if (status == 'Approved') {
        backgroundColor = '#20c997'
      } else if (status == 'Open') {
        backgroundColor = '#198754'
      } else if (status == 'Closed') {
        backgroundColor = '#dc3545'
      } else if (status == 'Pending') {
        backgroundColor = '#ffc107'
        color = '#222'
      } else if (status == 'Ongoing') {
        backgroundColor = '#6610f2'
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

  created() {
    let userData = localStorage.getItem('user')

    if (userData) {
      let user = JSON.parse(userData)
      this.staffName = user.full_name
    }

    this.fetchDashboardData()
  }
}
</script>