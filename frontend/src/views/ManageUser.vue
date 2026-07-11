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
            color: #d7d7df;
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
            color: white;
            background-color: #0d6efd;
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
      <!-- heading -->
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
          Manage Users
        </h2>

        <p
          style="
            margin: 0;
            color: #777;
            font-size: 13px;
          "
        >
          View and manage registered trekkers.
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

      <!-- user card -->
      <div
        style="
          background-color: white;
          border-radius: 8px;
          padding: 22px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        "
      >
        <!-- heading and search -->
        <div
          style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 20px;
          "
        >
          <h3
            style="
              margin: 0;
              font-size: 19px;
              color: #222;
            "
          >
            Registered Trekkers
          </h3>

          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search users"
            @input="fetchUsers"
            style="
              width: 100%;
              max-width: 320px;
              height: 42px;
              padding: 0 12px;
              border: 1px solid #ced4da;
              border-radius: 5px;
              font-size: 14px;
              color: #222;
              background-color: #fafafa;
              box-sizing: border-box;
              outline: none;
            "
          >
        </div>

        <!-- loading -->
        <div
          v-if="loading"
          style="
            text-align: center;
            padding: 50px 20px;
            color: #0d6efd;
            font-size: 15px;
          "
        >
          Loading users...
        </div>

        <!-- no users -->
        <div
          v-else-if="usersList.length == 0"
          style="
            text-align: center;
            padding: 50px 20px;
            color: #777;
            font-size: 14px;
          "
        >
          No users found.
        </div>

        <!-- users table -->
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
                <th :style="headingStyle">User ID</th>
                <th :style="headingStyle">Username</th>
                <th :style="headingStyle">Full Name</th>
                <th :style="headingStyle">Email</th>
                <th :style="headingStyle">Contact</th>
                <th :style="headingStyle">Status</th>
                <th
                  :style="{
                    padding: '13px',
                    textAlign: 'center',
                    color: '#555',
                    fontSize: '13px',
                    borderBottom: '1px solid #dee2e6',
                    whiteSpace: 'nowrap'
                  }"
                >
                  Actions
                </th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="(user, index) in usersList"
                :key="user.id"
                style="border-bottom: 1px solid #e8ebee;"
              >
                <td :style="cellStyle">
                  <b>
                    #US{{ String(index + 1).padStart(4, '0') }}
                  </b>
                </td>

                <td :style="cellStyle">
                  {{ user.username }}
                </td>

                <td :style="cellStyle">
                  <b style="color: #222;">
                    {{ user.full_name }}
                  </b>
                </td>

                <td :style="cellStyle">
                  {{ user.email }}
                </td>

                <td :style="cellStyle">
                  {{ user.contact_number || 'N/A' }}
                </td>

                <td :style="cellStyle">
                  <span :style="getStatusStyle(user.status)">
                    {{ user.status }}
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
                    v-if="user.status == 'active'"
                    type="button"
                    @click="toggleUserStatus(user, 'blacklisted')"
                    style="
                      background-color: #dc3545;
                      color: white;
                      border: none;
                      padding: 7px 10px;
                      border-radius: 4px;
                      margin-right: 5px;
                      cursor: pointer;
                      font-size: 12px;
                    "
                  >
                    Blacklist
                  </button>

                  <button
                    v-else
                    type="button"
                    @click="toggleUserStatus(user, 'active')"
                    style="
                      background-color: #198754;
                      color: white;
                      border: none;
                      padding: 7px 10px;
                      border-radius: 4px;
                      margin-right: 5px;
                      cursor: pointer;
                      font-size: 12px;
                    "
                  >
                    Whitelist
                  </button>

                  <button
                    type="button"
                    @click="deleteUser(user.id)"
                    style="
                      background-color: white;
                      color: #dc3545;
                      border: 1px solid #dc3545;
                      padding: 7px 10px;
                      border-radius: 4px;
                      cursor: pointer;
                      font-size: 12px;
                    "
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- info message -->
        <div
          style="
            background-color: #cff4fc;
            color: #055160;
            border: 1px solid #b6effb;
            padding: 12px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 13px;
            line-height: 1.5;
          "
        >
          <b>Info:</b> Blacklisted users cannot log in or make bookings.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      usersList: [],
      searchQuery: '',
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
      }
    }
  },

  methods: {
    async fetchUsers() {
      this.loading = true

      try {
        let endpoint = '/api/admin/users'

        if (this.searchQuery.trim() != '') {
          endpoint =
            '/api/admin/search?type=user&q=' +
            encodeURIComponent(this.searchQuery)
        }

        let response = await window.apiFetch(endpoint)
        let data = await response.json()

        if (response.ok) {
          this.usersList = data
        } else {
          this.errorMessage = data.message || 'Failed to load users.'
        }
      } catch (error) {
        this.errorMessage = 'Failed to load users.'
      }

      this.loading = false
    },

    async toggleUserStatus(user, newStatus) {
      this.errorMessage = ''
      this.successMessage = ''

      try {
        let response = await window.apiFetch(
          '/api/admin/users/' + user.id + '/status',
          {
            method: 'PUT',
            body: {
              status: newStatus
            }
          }
        )

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message
          this.fetchUsers()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to change user status.'
      }
    },

    async deleteUser(userId) {
      let check = confirm(
        'Are you sure you want to delete this user?'
      )

      if (check == false) {
        return
      }

      this.errorMessage = ''
      this.successMessage = ''

      try {
        let response = await window.apiFetch(
          '/api/admin/users/' + userId,
          {
            method: 'DELETE'
          }
        )

        let data = await response.json()

        if (response.ok) {
          this.successMessage = data.message
          this.fetchUsers()
        } else {
          this.errorMessage = data.message
        }
      } catch (error) {
        this.errorMessage = 'Failed to delete user.'
      }
    },

    getStatusStyle(status) {
      let backgroundColor = '#dc3545'

      if (status == 'active') {
        backgroundColor = '#198754'
      }

      return {
        display: 'inline-block',
        backgroundColor: backgroundColor,
        color: 'white',
        padding: '6px 10px',
        borderRadius: '20px',
        fontSize: '12px',
        fontWeight: 'bold',
        textTransform: 'capitalize'
      }
    },

    handleLogout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  },

  created() {
    this.fetchUsers()
  }
}
</script>