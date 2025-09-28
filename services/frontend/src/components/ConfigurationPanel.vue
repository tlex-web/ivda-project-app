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
              <v-select :items="companies.values" label="Select a company" variant="outlined" density="compact"
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
          <v-card elevation="2">
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
                <span class="status-text">Company {{ companies.selectedValue }}</span>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="5">
          <ScatterPlot :key="scatterPlotId" :selectedCategory="categories.selectedValue"
            @changeCurrentlySelectedCompany="changeCurrentlySelectedCompany" />
        </v-col>
        <v-col cols="12" md="5">
          <LinePlot :key="linePlotId" :selectedCompany="companies.selectedValue"
            :selectedAlgorithm="algorithm.selectedValue" />
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
</style>

<script>
import ScatterPlot from "./ScatterPlot";
import LinePlot from "./LinePlot";
export default {
  components: { ScatterPlot, LinePlot },
  data: () => ({
    scatterPlotId: 0,
    linePlotId: 0,
    categories: {
      values: ['All', 'tech', 'health', 'bank'],
      selectedValue: 'All'
    },
    companies: {
      values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
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
    }
  },
  methods: {
    changeCategory() {
      this.scatterPlotId += 1
    },
    changeCompany() {
      this.linePlotId += 1
    },
    changeAlgorithm() {
      this.linePlotId += 1
    },
    changeCurrentlySelectedCompany(companyId) {
      this.companies.selectedValue = companyId
      this.changeCompany()
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