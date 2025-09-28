<template>
    <div>
        <v-row align="center" justify="center" class="mt-1 mb-0">
            <h3>Overview of {{ $props.selectedCategory }} Companies</h3>
        </v-row>
        <div style="height: 90vh">
            <div id='myScatterPlot' style="height: inherit"></div>
        </div>
    </div>
</template>

<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
    name: "ScatterPlot",
    props: ['selectedCategory'],
    watch: {
        selectedCategory: function () {
            this.ScatterPlotData.x = [];
            this.ScatterPlotData.y = [];
            this.ScatterPlotData.name = [];
            this.ScatterPlotData.category = [];

            this.fetchData();
        }
    },
    data: () => ({
        ScatterPlotData: { x: [], y: [], name: [], category: [] },
    }),
    mounted() {
        this.fetchData()
    },
    methods: {
        async fetchData() {
            // req URL to retrieve companies from backend
            var reqUrl = 'http://127.0.0.1:5000/companies?category=' + this.$props.selectedCategory
            console.log('ReqURL ' + reqUrl)
            // await response and data
            const response = await fetch(reqUrl)
            const responseData = await response.json();

            // transform data to usable by scatterplot
            responseData.forEach((company) => {
                this.ScatterPlotData.name.push(company.name)
                this.ScatterPlotData.x.push(company.founding_year)
                this.ScatterPlotData.y.push(company.employees)
                this.ScatterPlotData.category.push(company.category || 'unknown')
            })
            // after the data is loaded, draw the plot
            this.drawScatterPlot()
        },
        drawScatterPlot() {
            let data = [];

            if (this.selectedCategory === 'All') {
                // Create separate traces for each category when "All" is selected
                data = this.createCategoryTraces();
            } else {
                // Create single trace for selected category
                data = this.createSingleTrace();
            }

            var layout = {
                hovermode: 'closest',
                margin: { l: 80, r: 40, b: 80, t: 40 },
                xaxis: {
                    title: {
                        text: 'Founding Year',
                        font: { size: 14, color: '#333' }
                    },
                    showgrid: true,
                    gridcolor: '#eee'
                },
                yaxis: {
                    title: {
                        text: 'Number of Employees',
                        font: { size: 14, color: '#333' }
                    },
                    showgrid: true,
                    gridcolor: '#eee'
                },
                showlegend: this.selectedCategory === 'All',
                legend: {
                    x: 1,
                    y: 1,
                    bgcolor: 'rgba(255,255,255,0.8)',
                    bordercolor: '#ccc',
                    borderwidth: 1
                }
            }
            var config = { responsive: true, displayModeBar: false }
            Plotly.newPlot('myScatterPlot', data, layout, config);

            this.clickScatterPlot()
        },
        getCategoryColors() {
            // Define meaningful colors for each category
            return {
                'tech': '#2196F3',      // Blue - represents innovation and technology
                'health': '#4CAF50',    // Green - represents health and life
                'bank': '#FF9800',      // Orange - represents finance and stability
                'unknown': '#757575'    // Grey - for undefined categories
            };
        },
        getMarkerColors() {
            const categoryColors = this.getCategoryColors();
            return this.ScatterPlotData.category.map(category =>
                categoryColors[category] || categoryColors['unknown']
            );
        },
        getHoverText() {
            return this.ScatterPlotData.name.map((name, index) => {
                const category = this.ScatterPlotData.category[index];
                return `${name} (${category})`;
            });
        },
        createCategoryTraces() {
            const categoryColors = this.getCategoryColors();
            const categories = ['tech', 'health', 'bank'];
            const traces = [];

            categories.forEach(category => {
                // Filter data for this specific category
                const categoryData = this.getDataForCategory(category);

                if (categoryData.x.length > 0) {
                    traces.push({
                        x: categoryData.x,
                        y: categoryData.y,
                        mode: 'markers',
                        type: 'scatter',
                        name: category.charAt(0).toUpperCase() + category.slice(1),
                        text: categoryData.hoverText,
                        hovertemplate: '<b>%{text}</b><br>' +
                            'Founded: %{x}<br>' +
                            'Employees: %{y}<br>' +
                            '<extra></extra>',
                        marker: {
                            color: categoryColors[category],
                            size: 12,
                            line: {
                                width: 2,
                                color: 'white'
                            }
                        },
                        showlegend: true
                    });
                }
            });

            return traces;
        },
        createSingleTrace() {
            const colors = this.getMarkerColors();
            const hoverText = this.getHoverText();

            return [{
                x: this.ScatterPlotData.x,
                y: this.ScatterPlotData.y,
                mode: 'markers',
                type: 'scatter',
                text: hoverText,
                hovertemplate: '<b>%{text}</b><br>' +
                    'Founded: %{x}<br>' +
                    'Employees: %{y}<br>' +
                    '<extra></extra>',
                marker: {
                    color: colors,
                    size: 12,
                    line: {
                        width: 2,
                        color: 'white'
                    }
                },
                showlegend: false
            }];
        },
        getDataForCategory(targetCategory) {
            const categoryData = {
                x: [],
                y: [],
                names: [],
                hoverText: []
            };

            this.ScatterPlotData.category.forEach((category, index) => {
                if (category === targetCategory) {
                    categoryData.x.push(this.ScatterPlotData.x[index]);
                    categoryData.y.push(this.ScatterPlotData.y[index]);
                    categoryData.names.push(this.ScatterPlotData.name[index]);
                    categoryData.hoverText.push(`${this.ScatterPlotData.name[index]} (${category})`);
                }
            });

            return categoryData;
        },
        clickScatterPlot() {
            var that = this
            var myPlot = document.getElementById('myScatterPlot')
            myPlot.on('plotly_click', function (data) {
                for (var i = 0; i < data.points.length; i++) {
                    let clickedPoint = data.points[i];
                    let traceIndex = clickedPoint.curveNumber;
                    let pointIndex = clickedPoint.pointNumber;

                    // Calculate the global company index based on the data structure
                    let companyIndex = that.getGlobalCompanyIndex(traceIndex, pointIndex);

                    // emit event to change the currently selected company
                    that.$emit('changeCurrentlySelectedCompany', companyIndex);

                    // Reset all traces to normal appearance
                    that.resetAllTraces();

                    // Highlight the selected point
                    that.highlightSelectedPoint(traceIndex, pointIndex);
                }
            });
        },
        getGlobalCompanyIndex(traceIndex, pointIndex) {
            if (this.selectedCategory === 'All') {
                // For "All" view, we need to map back to the original data index
                const categories = ['tech', 'health', 'bank'];
                const selectedCategory = categories[traceIndex];

                // Find the pointIndex-th occurrence of selectedCategory in our data
                let categoryCount = 0;
                for (let i = 0; i < this.ScatterPlotData.category.length; i++) {
                    if (this.ScatterPlotData.category[i] === selectedCategory) {
                        if (categoryCount === pointIndex) {
                            return i + 1; // +1 because company IDs are 1-based
                        }
                        categoryCount++;
                    }
                }
            } else {
                // For single category view, direct mapping
                return pointIndex + 1;
            }
            return 1; // fallback
        },
        resetAllTraces() {
            const plotDiv = document.getElementById('myScatterPlot');
            const numTraces = plotDiv.data.length;

            for (let i = 0; i < numTraces; i++) {
                const traceData = plotDiv.data[i];
                if (traceData.marker && traceData.marker.color) {
                    const resetUpdate = {
                        'marker.size': Array(traceData.x.length).fill(12),
                        'marker.line.width': Array(traceData.x.length).fill(2),
                        'marker.opacity': Array(traceData.x.length).fill(1)
                    };
                    Plotly.restyle('myScatterPlot', resetUpdate, [i]);
                }
            }
        },
        highlightSelectedPoint(traceIndex, pointIndex) {
            const plotDiv = document.getElementById('myScatterPlot');
            const traceData = plotDiv.data[traceIndex];

            // Create arrays for highlighting
            const sizes = Array(traceData.x.length).fill(12);
            const lineWidths = Array(traceData.x.length).fill(2);
            const opacities = Array(traceData.x.length).fill(0.5); // Make other points semi-transparent

            // Highlight the selected point
            sizes[pointIndex] = 16;
            lineWidths[pointIndex] = 3;
            opacities[pointIndex] = 1;

            const highlightUpdate = {
                'marker.size': sizes,
                'marker.line.width': lineWidths,
                'marker.opacity': opacities
            };

            Plotly.restyle('myScatterPlot', highlightUpdate, [traceIndex]);
        }
    }
}
</script>
