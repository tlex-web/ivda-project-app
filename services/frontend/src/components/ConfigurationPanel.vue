<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col cols="12" md="2" class="sidebar">
          <!-- Company Overview Section -->
          <v-card class="mb-4" elevation="2">
            <v-card-title class="section-header">
              <v-icon left color="primary" class="mr-2">mdi-office-building</v-icon>
              Company Overview
            </v-card-title>
            <v-card-text class="card-content">
              <v-select :items="categories.values" label="Select a category" variant="outlined" density="compact"
                v-model="categories.selectedValue" @update:modelValue="changeCategory"
                prepend-inner-icon="mdi-tag-outline" color="primary" class="select-field"></v-select>
              <v-chip :color="getCategoryColor(categories.selectedValue)" small class="category-chip">
                {{ categories.selectedValue }}
              </v-chip>
            </v-card-text>
          </v-card>

          <!-- Profit Analysis Section -->
          <v-card class="mb-4" elevation="2">
            <v-card-title class="section-header">
              <v-icon left color="success" class="mr-2">mdi-chart-line</v-icon>
              Profit Analysis
            </v-card-title>
            <v-card-text class="card-content">
              <v-select :items="companyOptions" label="Select a company" variant="outlined" density="compact"
                v-model="companies.selectedValue" @update:modelValue="changeCompany" prepend-inner-icon="mdi-domain"
                color="primary" class="select-field"></v-select>

              <v-select :items="algorithmOptions" label="Prediction algorithm" variant="outlined" density="compact"
                v-model="algorithm.selectedValue" @update:modelValue="changeAlgorithm" prepend-inner-icon="mdi-brain"
                color="primary" class="select-field"></v-select>

              <v-chip :color="getAlgorithmColor(algorithm.selectedValue)" small class="algorithm-chip">
                <v-icon left small>{{ getAlgorithmIcon(algorithm.selectedValue) }}</v-icon>
                {{ algorithm.selectedValue }}
              </v-chip>
            </v-card-text>
          </v-card>

          <!-- Status Section -->
          <v-card class="mb-4" elevation="2">
            <v-card-title class="section-header">
              <v-icon left color="info" class="mr-2">mdi-information</v-icon>
              Status
            </v-card-title>
            <v-card-text class="status-card">
              <div class="status-item">
                <v-icon color="success" small class="mr-2">mdi-check-circle</v-icon>
                <span class="status-text">Data loaded</span>
              </div>
              <div class="status-item">
                <v-icon color="primary" small class="mr-2">mdi-chart-scatter-plot</v-icon>
                <span class="status-text">{{ categories.selectedValue }} category</span>
              </div>
              <div class="status-item">
                <v-icon color="warning" small class="mr-2">mdi-cog</v-icon>
                <span class="status-text">{{ getSelectedCompanyName() }}</span>
              </div>
            </v-card-text>
          </v-card>

          <!-- Poem Section -->
          <v-card class="mb-4" elevation="2">
            <v-card-title class="section-header">
              <v-icon left color="purple" class="mr-2">mdi-book-open-page-variant</v-icon>
              Company Poem
            </v-card-title>
            <v-card-text class="poem-content">
              <div v-if="isLoadingPoem" class="text-center">
                <v-progress-circular indeterminate color="primary" size="24"></v-progress-circular>
                <span class="ml-2">Generating poem...</span>
              </div>
              <div v-else-if="poem" class="poem-text">
                {{ poem }}
              </div>
              <div v-else class="text-muted">
                Select a company to generate a poem
              </div>
              <v-btn v-if="companies.selectedValue && !isLoadingPoem" @click="fetchPoem(companies.selectedValue)"
                color="purple" variant="outlined" size="small" class="mt-2" prepend-icon="mdi-refresh">
                Generate New Poem
              </v-btn>
            </v-card-text>
          </v-card>

          <!-- Company Information Section -->
          <v-card v-if="companies.selectedValue" class="mb-4" elevation="2">
            <v-card-title class="section-header">
              <v-icon left color="cyan" class="mr-2">mdi-information-outline</v-icon>
              Company Information
            </v-card-title>
            <v-card-text class="company-info-content">
              <div v-if="isLoadingCompanyInfo" class="text-center">
                <v-progress-circular indeterminate color="primary" size="24"></v-progress-circular>
                <span class="ml-2">Fetching company information...</span>
              </div>
              <div v-else-if="companyInfo" class="company-info-text">
                {{ companyInfo }}
              </div>
              <div v-else class="text-muted">
                Select a company to view information
              </div>
              <v-btn v-if="companies.selectedValue && !isLoadingCompanyInfo"
                @click="fetchCompanyInfo(companies.selectedValue)" color="cyan" variant="outlined" size="small"
                class="mt-2" prepend-icon="mdi-refresh">
                Refresh Information
              </v-btn>
            </v-card-text>
          </v-card>

          <!-- Groq API Parameters Section -->
          <v-card v-if="companies.selectedValue" class="mb-4" elevation="2">
            <v-card-title class="section-header">
              <v-icon left color="orange" class="mr-2">mdi-api</v-icon>
              Groq API Parameters
            </v-card-title>
            <v-card-text class="api-params-content">
              <v-chip color="primary" variant="outlined" size="small" class="ma-1">
                <v-icon left size="small">mdi-brain</v-icon>
                Model: llama-3.1-8b-instant
              </v-chip>
              <v-chip color="success" variant="outlined" size="small" class="ma-1">
                <v-icon left size="small">mdi-thermometer</v-icon>
                Temperature: 0.7
              </v-chip>
              <v-chip color="info" variant="outlined" size="small" class="ma-1">
                <v-icon left size="small">mdi-counter</v-icon>
                Max Tokens: 150
              </v-chip>
              <v-chip color="warning" variant="outlined" size="small" class="ma-1">
                <v-icon left size="small">mdi-account</v-icon>
                Company: {{ getSelectedCompanyName() }}
              </v-chip>
              <v-chip color="purple" variant="outlined" size="small" class="ma-1">
                <v-icon left size="small">mdi-cloud</v-icon>
                API: Groq OpenAI Compatible
              </v-chip>
              <v-chip color="teal" variant="outlined" size="small" class="ma-1">
                <v-icon left size="small">mdi-format-text</v-icon>
                Task: Poetry Generation
              </v-chip>
              <v-chip color="cyan" variant="outlined" size="small" class="ma-1">
                <v-icon left size="small">mdi-information-outline</v-icon>
                Task: Company Information
              </v-chip>
              <v-chip color="deep-orange" variant="outlined" size="small" class="ma-1">
                <v-icon left size="small">mdi-tune</v-icon>
                Temp: 0.3 (Info) / 0.7 (Poetry)
              </v-chip>
              <v-chip color="indigo" variant="outlined" size="small" class="ma-1">
                <v-icon left size="small">mdi-text-box-outline</v-icon>
                Tokens: 200 (Info) / 150 (Poetry)
              </v-chip>
            </v-card-text>
          </v-card>
        </v-col>
        <!-- Plots Section -->
        <v-col cols="12" md="5">
          <ScatterPlot :key="scatterPlotId" :selectedCategory="categories.selectedValue"
            @changeCurrentlySelectedCompany="changeCurrentlySelectedCompany" />
        </v-col>
        <v-col cols="12" md="5">
          <LinePlot :key="linePlotId" :selectedCompany="companies.selectedValue"
            :selectedAlgorithm="algorithm.selectedValue" />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="12">
          <CompanySize :key="companySizePlotId" :selectedCompany="companies.selectedValue"
            :selectedCategory="categories.selectedValue" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<style scoped>
.sidebar {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 16px;
  height: calc(100vh - 50px);
  overflow-y: auto;
}

.section-header {
  font-size: 14px !important;
  font-weight: 600 !important;
  padding: 12px 16px 8px 16px !important;
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white !important;
}

.section-header .v-icon {
  color: white !important;
}

.card-content {
  padding: 16px !important;
}

.select-field {
  margin-bottom: 0px !important;
}

.category-chip {
  width: 100%;
  justify-content: center;
  font-weight: 500;
  margin-top: 0px;
}

.algorithm-chip {
  width: 100%;
  justify-content: center;
  font-weight: 500;
  margin-top: 0px;
}

.status-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  padding: 4px 0;
}

.status-text {
  font-size: 13px;
  font-weight: 500;
  color: #555;
}

.status-card {
  padding-top: 8px !important;
  padding-bottom: 0px !important;

}

.api-params-content {
  padding: 12px !important;
}

.api-params-content .v-chip {
  margin: 2px !important;
  font-size: 11px !important;
  height: 28px !important;
}

.api-params-content .v-chip .v-icon {
  font-size: 14px !important;
}

.company-info-content {
  padding: 16px !important;
}

.company-info-text {
  font-size: 14px;
  line-height: 1.6;
  color: #444;
  text-align: justify;
  background: rgba(0, 188, 212, 0.05);
  padding: 12px;
  border-radius: 8px;
  border-left: 4px solid #00bcd4;
}

.v-card {
  border-radius: 12px !important;
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
}

.v-select {
  border-radius: 8px;
}

/* Custom scrollbar for sidebar */
.sidebar::-webkit-scrollbar {
  width: 6px;
}

.sidebar::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.sidebar::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 3px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.5);
}

.poem-content {
  padding: 16px !important;
}

.poem-text {
  font-style: italic;
  line-height: 1.6;
  color: #555;
  white-space: pre-line;
}

.text-muted {
  color: #999;
  font-style: italic;
}
</style>

<script>
import ScatterPlot from "./ScatterPlot";
import LinePlot from "./LinePlot";
import CompanySize from "./CompanySize";
export default {
  components: { ScatterPlot, LinePlot, CompanySize },
  data: () => ({
    scatterPlotId: 0,
    linePlotId: 0,
    companySizePlotId: 0,
    poem: '',
    isLoadingPoem: false,
    companyInfo: '',
    isLoadingCompanyInfo: false,
    categories: {
      values: ['All', 'tech', 'health', 'bank'],
      selectedValue: 'All'
    },
    companies: {
      list: [], // Will store company objects with id and name
      selectedValue: 1
    },
    algorithm: {
      values: ['none', 'random', 'regression'],
      selectedValue: 'none'
    }
  }),
  computed: {
    algorithmOptions() {
      return this.algorithm.values.map(value => ({
        title: this.getAlgorithmDisplayName(value),
        value: value
      }))
    },
    companyOptions() {
      return this.companies.list.map(company => ({
        title: company.name,
        value: company.id
      }))
    }
  },
  mounted() {
    this.fetchCompanies()
  },
  methods: {
    async fetchPoem(companyId) {
      try {
        this.isLoadingPoem = true;
        const companyName = this.getSelectedCompanyName();

        console.log(`🚀 GROQ API CALL INITIATED`);
        console.log(`📋 Company ID: ${companyId}`);
        console.log(`🏢 Company Name: ${companyName}`);

        // Log Groq API Parameters
        console.log(`🤖 GROQ API PARAMETERS:`);
        console.log(`   🧠 Model: llama-3.1-8b-instant`);
        console.log(`   🌡️  Temperature: 0.7`);
        console.log(`   🔢 Max Tokens: 150`);
        console.log(`   ⚡ Task: Poetry Generation`);
        console.log(`   🔗 API: Groq OpenAI Compatible`);

        // First test the test endpoint
        try {
          const testResponse = await fetch('http://127.0.0.1:5000/test/poem');
          console.log('✅ Test endpoint status:', testResponse.status);
        } catch (testError) {
          console.log('❌ Test endpoint failed:', testError.message);
        }

        const poemUrl = `http://127.0.0.1:5000/companies/${companyId}/poem`;
        console.log(`🌐 Making request to: ${poemUrl}`);

        const response = await fetch(poemUrl);
        console.log(`📡 Response status: ${response.status}`);
        console.log(`✅ Response ok: ${response.ok}`);

        if (response.status === 404) {
          throw new Error(`API endpoint not found (404). Check if backend is running and endpoint is registered.`);
        }

        if (response.status >= 500) {
          const errorText = await response.text();
          throw new Error(`Server error (${response.status}): ${errorText}`);
        }

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`HTTP ${response.status}: ${errorText || response.statusText}`);
        }

        const result = await response.json();
        console.log('🎭 GROQ API RESPONSE:');
        console.log('📝 Generated Poem:', result.poem ? result.poem.substring(0, 100) + '...' : 'No poem');
        console.log('✨ Full Response:', result);

        if (result.poem) {
          this.poem = result.poem;
        } else if (result.error) {
          this.poem = `Error: ${result.error}`;
        } else {
          this.poem = "No poem received from server.";
        }
      } catch (error) {
        console.error("Error fetching the poem:", error);
        this.poem = `Failed to generate poem: ${error.message}`;
      } finally {
        this.isLoadingPoem = false;
      }
    },

    async fetchCompanyInfo(companyId) {
      try {
        this.isLoadingCompanyInfo = true;
        const companyName = this.getSelectedCompanyName();

        console.log(`📊 COMPANY INFO API CALL INITIATED`);
        console.log(`📋 Company ID: ${companyId}`);
        console.log(`🏢 Company Name: ${companyName}`);

        // Log Groq API Parameters for company info
        console.log(`🤖 GROQ API PARAMETERS (Company Info):`);
        console.log(`   🧠 Model: llama-3.1-8b-instant`);
        console.log(`   🌡️  Temperature: 0.3`);
        console.log(`   🔢 Max Tokens: 200`);
        console.log(`   ⚡ Task: Company Information Generation`);
        console.log(`   🔗 API: Groq OpenAI Compatible`);

        const infoUrl = `http://127.0.0.1:5000/companies/${companyId}/info`;
        console.log(`🌐 Making request to: ${infoUrl}`);

        const response = await fetch(infoUrl);
        console.log(`📡 Response status: ${response.status}`);
        console.log(`✅ Response ok: ${response.ok}`);

        if (response.status === 404) {
          throw new Error(`API endpoint not found (404). Check if backend is running and endpoint is registered.`);
        }

        if (response.status >= 500) {
          const errorText = await response.text();
          throw new Error(`Server error (${response.status}): ${errorText}`);
        }

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`HTTP ${response.status}: ${errorText || response.statusText}`);
        }

        const result = await response.json();
        console.log('📊 COMPANY INFO API RESPONSE:');
        console.log('📝 Generated Info:', result.company_info ? result.company_info.substring(0, 100) + '...' : 'No info');
        console.log('✨ Full Response:', result);

        if (result.company_info) {
          this.companyInfo = result.company_info;
        } else if (result.error) {
          this.companyInfo = `Error: ${result.error}`;
        } else {
          this.companyInfo = "No company information received from server.";
        }
      } catch (error) {
        console.error("Error fetching company info:", error);
        this.companyInfo = `Failed to fetch company information: ${error.message}`;
      } finally {
        this.isLoadingCompanyInfo = false;
      }
    },

    async fetchCompanies() {
      try {
        const response = await fetch('http://127.0.0.1:5000/companies')
        const companiesData = await response.json()
        this.companies.list = companiesData.map(company => ({
          id: company.id,
          name: company.name
        }))
        // Set the first company as default if available
        if (this.companies.list.length > 0) {
          this.companies.selectedValue = this.companies.list[0].id
          // Fetch poem and company info for the initial company
          this.fetchPoem(this.companies.selectedValue);
          this.fetchCompanyInfo(this.companies.selectedValue);
        }
      } catch (error) {
        console.error('Error fetching companies:', error)
        // Fallback to original behavior if API fails
        this.companies.list = Array.from({ length: 15 }, (_, i) => ({
          id: i + 1,
          name: `Company ${i + 1}`
        }))
      }
    },
    getSelectedCompanyName() {
      const selectedCompany = this.companies.list.find(company => company.id === this.companies.selectedValue)
      return selectedCompany ? selectedCompany.name : `Company ID: ${this.companies.selectedValue}`
    },
    changeCategory() {
      this.scatterPlotId += 1
      this.companySizePlotId += 1
    },
    changeCompany() {
      this.linePlotId += 1
      this.companySizePlotId += 1
      // Fetch poem and company info for the selected company
      if (this.companies.selectedValue) {
        this.fetchPoem(this.companies.selectedValue);
        this.fetchCompanyInfo(this.companies.selectedValue);
      }
    },
    changeAlgorithm() {
      this.linePlotId += 1
    },
    changeCurrentlySelectedCompany(companyId) {
      this.companies.selectedValue = companyId
      this.changeCompany()
      // Fetch poem and company info for the newly selected company
      this.fetchPoem(companyId);
      this.fetchCompanyInfo(companyId);
    },
    getCategoryColor(category) {
      // Use the same colors as the scatter plot for consistency
      const colors = {
        'All': 'primary',
        'tech': 'blue',        // #2196F3 - Blue for technology/innovation
        'health': 'green',     // #4CAF50 - Green for health/life
        'bank': 'orange'       // #FF9800 - Orange for finance/stability
      }
      return colors[category] || 'grey'
    },
    getAlgorithmColor(algorithm) {
      const colors = {
        'none': 'grey',
        'random': 'orange',
        'regression': 'purple'
      }
      return colors[algorithm] || 'grey'
    },
    getAlgorithmIcon(algorithm) {
      const icons = {
        'none': 'mdi-minus-circle',
        'random': 'mdi-dice-multiple',
        'regression': 'mdi-chart-timeline-variant'
      }
      return icons[algorithm] || 'mdi-help-circle'
    },
    getAlgorithmDisplayName(algorithm) {
      const names = {
        'none': 'No Prediction',
        'random': 'Random',
        'regression': 'Linear Regression'
      }
      return names[algorithm] || algorithm
    }
  }
}
</script>