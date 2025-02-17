<template>
  <div class="dashboard">
    <h1>Dashboard</h1>

    <!-- If user is not logged in, show a message -->
    <div v-if="!token">
      <p>You are not logged in!</p>
      <p><a href="/login">Go to Login</a></p>
    </div>

    <!-- Otherwise show the calculator settings -->
    <div v-else>
      <h2>Select your Years</h2>

      <table class="years-table">
        <thead>
        <tr>
          <th>Active</th>
          <th>Year</th>
          <th># Credits</th>
          <th>% Weight</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(y, index) in calculatorConfig.years" :key="index">
          <td>
            <input type="checkbox" v-model="y.active" />
          </td>
          <td>{{ y.year }}</td>
          <td>
            <input
                type="number"
                v-model.number="y.credits"
                min="0"
                @input="onCreditsChange(index)"
            />
          </td>
          <td>
            <input
                type="number"
                v-model.number="y.weight"
                min="0"
                max="100"
                @input="onWeightChange(index)"
            />
          </td>
        </tr>
        </tbody>
      </table>

      <button class="save-button" @click="saveYears">
        Save Years
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Dashboard',
  data() {
    return {
      token: null,
      // Some default year configuration if none is found
      calculatorConfig: {
        years: [
          { year: 'Year 1', active: false, credits: 120, weight: 0 },
          { year: 'Year 2', active: false, credits: 120, weight: 0 },
          { year: 'Year 3', active: false, credits: 120, weight: 0 },
          { year: 'Year 4', active: false, credits: 120, weight: 0 },
          { year: 'Masters', active: false, credits: 180, weight: 0 },
        ],
      },
    };
  },
  mounted() {
    // 1. Get token from URL or localStorage
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    if (token) {
      this.token = token;
      localStorage.setItem('authToken', token);
      // Remove token from the URL
      this.$router.replace({ path: '/dashboard' });
    } else {
      // If there's already a token in localStorage, use that
      const storedToken = localStorage.getItem('authToken');
      if (storedToken) {
        this.token = storedToken;
      }
    }

    // 2. Fetch existing calculator config if we have a token
    if (this.token) {
      this.getCalculatorConfig();
    }
  },
  methods: {
    async getCalculatorConfig() {
      try {
        const response = await axios.get('http://localhost:7071/api/calculator', {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        });
        // If user has a saved config, load it. If empty, keep defaults.
        if (response.data && response.data.years) {
          this.calculatorConfig = response.data;
        }
      } catch (error) {
        console.error('Error fetching calculator config:', error);
        // If 404 or no config, we just keep the default
      }
    },
    async saveYears() {
      try {
        const response = await axios.put(
            'http://localhost:7071/api/calculator',
            this.calculatorConfig,
            {
              headers: {
                Authorization: `Bearer ${this.token}`,
              },
            }
        );
        alert('Calculator configuration saved successfully!');
      } catch (error) {
        console.error('Error saving calculator config:', error);
        alert('Failed to save calculator configuration.');
      }
    },
    onCreditsChange(index) {
      // Optionally do any validations or transformations here
      // e.g. disallow negative numbers, clamp to a certain max, etc.
      if (this.calculatorConfig.years[index].credits < 0) {
        this.calculatorConfig.years[index].credits = 0;
      }
    },
    onWeightChange(index) {
      if (this.calculatorConfig.years[index].weight < 0) {
        this.calculatorConfig.years[index].weight = 0;
      }
      if (this.calculatorConfig.years[index].weight > 100) {
        this.calculatorConfig.years[index].weight = 100;
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  text-align: center;
}

/* Example table styling */
.years-table {
  margin: 2rem auto;
  border-collapse: collapse;
  width: 80%;
  max-width: 600px;
}
.years-table th,
.years-table td {
  border: 1px solid #ccc;
  padding: 0.75rem;
  text-align: left;
}
.years-table th {
  background-color: #f2f2f2;
}

.save-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  font-weight: bold;
  background-color: #512da8;
  color: #fff;
  border: none;
  border-radius: 24px;
  cursor: pointer;
  transition: 0.3s;
}
.save-button:hover {
  background-color: #3f1e8c;
  transform: scale(1.02);
}
</style>
