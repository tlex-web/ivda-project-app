<template>
    <div>
        <v-row align="center" justify="center" class="mt-1 mb-0">
            <h3>Company Size Comparison: {{ getSelectedCompanyName() }} vs {{ selectedCategory }} Category</h3>
        </v-row>
        <div style="height: 90vh">
            <div id='companySizePlot' style="height: inherit"></div>
        </div>
    </div>
</template>

<script>
import Plotly from 'plotly.js/dist/plotly';

export default {
    name: "CompanySize",
    props: ['selectedCompany', 'selectedCategory'],
    watch: {
        selectedCompany() {
            this.fetchData();
        },
        selectedCategory() {
            this.fetchData();
        }
    },
    data: () => ({
        companiesData: [],
        selectedCompanyData: null
    }),
    mounted() {
        this.fetchData();
    },
    methods: {
        async fetchData() {
            try {
                // Fetch all companies in the selected category
                let reqUrl = 'http://127.0.0.1:5000/companies';
                if (this.selectedCategory && this.selectedCategory !== 'All') {
                    reqUrl += `?category=${this.selectedCategory}`;
                }

                console.log("Fetching company size data from:", reqUrl);
                const response = await fetch(reqUrl);
                const responseData = await response.json();

                this.companiesData = responseData;
                this.selectedCompanyData = responseData.find(company => company.id === this.selectedCompany);

                this.drawCompanySizePlot();
            } catch (error) {
                console.error('Error fetching company size data:', error);
            }
        },

        drawCompanySizePlot() {
            if (!this.companiesData.length) return;

            // Prepare data for the bar chart
            const companyNames = this.companiesData.map(company => company.name);
            const employeeCounts = this.companiesData.map(company => company.employees);

            // Create colors array - highlight selected company
            const colors = this.companiesData.map(company => {
                if (company.id === this.selectedCompany) {
                    return '#FF4081'; // Pink for selected company
                } else {
                    return this.getCategoryColor(company.category);
                }
            });

            // Calculate average for the category
            const averageEmployees = employeeCounts.reduce((sum, count) => sum + count, 0) / employeeCounts.length;

            // Main bar trace
            const barTrace = {
                x: companyNames,
                y: employeeCounts,
                type: 'bar',
                name: 'Employee Count',
                marker: {
                    color: colors,
                    line: {
                        color: '#333',
                        width: 1
                    }
                },
                text: employeeCounts.map(count => count.toLocaleString()),
                textposition: 'outside',
                hovertemplate: '<b>%{x}</b><br>' +
                    'Employees: %{y:,.0f}<br>' +
                    '<extra></extra>'
            };

            // Average line trace
            const averageLine = {
                x: companyNames,
                y: Array(companyNames.length).fill(averageEmployees),
                type: 'scatter',
                mode: 'lines',
                name: `Category Average (${Math.round(averageEmployees).toLocaleString()})`,
                line: {
                    color: '#666',
                    width: 2,
                    dash: 'dash'
                },
                hovertemplate: 'Average: %{y:,.0f}<extra></extra>'
            };

            const data = [barTrace, averageLine];

            const layout = {
                title: {
                    text: `Employee Count Comparison - ${this.selectedCategory} Category`,
                    font: { size: 16, color: '#333' }
                },
                xaxis: {
                    title: {
                        text: 'Companies',
                        font: { size: 14, color: '#333' }
                    },
                    tickangle: -45,
                    showgrid: false
                },
                yaxis: {
                    title: {
                        text: 'Number of Employees',
                        font: { size: 14, color: '#333' }
                    },
                    showgrid: true,
                    gridcolor: '#eee'
                },
                showlegend: true,
                legend: {
                    x: 0.02,
                    y: 0.98,
                    bgcolor: 'rgba(255, 255, 255, 0.8)',
                    bordercolor: '#ccc',
                    borderwidth: 1
                },
                margin: { l: 80, r: 40, b: 120, t: 80 },
                hovermode: 'closest'
            };

            const config = {
                responsive: true,
                displayModeBar: false
            };

            Plotly.newPlot('companySizePlot', data, layout, config);
        },

        getCategoryColor(category) {
            // Use consistent colors across the application
            const colors = {
                'tech': '#2196F3',      // Blue for technology
                'health': '#4CAF50',    // Green for health
                'bank': '#FF9800'       // Orange for banking
            };
            return colors[category] || '#9E9E9E'; // Grey as fallback
        },

        getSelectedCompanyName() {
            if (this.selectedCompanyData) {
                return this.selectedCompanyData.name;
            }
            return `Company ID: ${this.selectedCompany}`;
        }
    }
}
</script>

<style scoped>
h3 {
    color: #333;
    font-weight: 500;
    text-align: center;
}
</style>