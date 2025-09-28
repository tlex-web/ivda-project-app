<template>
    <div>
        <v-row align="center" justify="center" class="mt-1 mb-0">
            <h3>Profit View of Company: {{ companyName || $props.selectedCompany }}</h3>
        </v-row>
        <div style="height: 90vh">
            <div id='myLinePlot' style="height: inherit"></div>
        </div>
    </div>
</template>


<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
    name: "LinePlot",
    props: ['selectedCompany', 'selectedAlgorithm'],
    watch: {
        selectedCompany() {
            this.LinePlotData.x = [];
            this.LinePlotData.y = [];
            this.predictedData.x = [];
            this.predictedData.y = [];
            this.companyName = '';

            this.fetchData();
        },
        selectedAlgorithm() {
            this.LinePlotData.x = [];
            this.LinePlotData.y = [];
            this.predictedData.x = [];
            this.predictedData.y = [];
            this.companyName = '';

            this.fetchData();
        }
    },
    data: () => ({
        LinePlotData: { x: [], y: [] },
        predictedData: { x: [], y: [] },
        companyName: ''
    }),
    mounted() {
        this.fetchData()
    },
    methods: {
        async fetchData() {
            var reqUrl = 'http://127.0.0.1:5000/companies/' + this.$props.selectedCompany +
                '?algorithm=' + this.$props.selectedAlgorithm
            console.log("ReqURL " + reqUrl)
            // await response and data
            const response = await fetch(reqUrl)
            const responseData = await response.json();

            // Store the company name for display in title
            this.companyName = responseData.name;

            // Check if we have predicted data (algorithm is 'random' or 'regression')
            const hasPrediction = this.$props.selectedAlgorithm === 'random' || this.$props.selectedAlgorithm === 'regression';

            // transform data to usable by lineplot
            responseData.profit.forEach((profit, index) => {
                // If we have prediction and this is the first item (index 0), it's the predicted value for 2022
                if (hasPrediction && index === 0) {
                    this.predictedData.x.push(profit.year);
                    this.predictedData.y.push(profit.value);
                } else {
                    this.LinePlotData.x.push(profit.year);
                    this.LinePlotData.y.push(profit.value);
                }
            })
            // draw the lineplot after the data is transformed
            this.drawLinePlot()
        },
        drawLinePlot() {
            // Main trace for real/historical data
            var trace1 = {
                x: this.LinePlotData.x,
                y: this.LinePlotData.y,
                type: 'scatter',
                mode: 'lines+markers',
                line: { color: '#1976D2', width: 2 },
                marker: { color: '#1976D2', size: 6 },
                name: 'Historical Data'
            };

            var data = [trace1];

            // Add predicted data trace if we have predicted values
            if (this.predictedData.x.length > 0) {
                // Connect the last historical point to the predicted point
                const lastHistoricalX = this.LinePlotData.x[this.LinePlotData.x.length - 1];
                const lastHistoricalY = this.LinePlotData.y[this.LinePlotData.y.length - 1];

                var predictedTrace = {
                    x: [lastHistoricalX, ...this.predictedData.x],
                    y: [lastHistoricalY, ...this.predictedData.y],
                    type: 'scatter',
                    mode: 'lines+markers',
                    line: {
                        color: '#FF5722',
                        width: 2,
                        dash: 'dash' // Dashed line for prediction
                    },
                    marker: {
                        color: '#FF5722',
                        size: 8,
                        symbol: 'diamond' // Different marker shape for prediction
                    },
                    name: 'Predicted Data'
                };
                data.push(predictedTrace);
            }

            var layout = {
                hovermode: 'closest',
                margin: { l: 100, r: 40, b: 80, t: 40 },
                showlegend: this.predictedData.x.length > 0, // Show legend only when we have predictions
                legend: {
                    x: 0.02,
                    y: 0.98,
                    bgcolor: 'rgba(255, 255, 255, 0.8)',
                    bordercolor: '#ccc',
                    borderwidth: 1
                },
                xaxis: {
                    title: {
                        text: 'Year',
                        font: { size: 14, color: '#333' }
                    },
                    showgrid: true,
                    gridcolor: '#eee'
                },
                yaxis: {
                    title: {
                        text: 'Profit (in million USD)',
                        font: { size: 14, color: '#333' }
                    },
                    showgrid: true,
                    gridcolor: '#eee'
                }
            }
            var config = { responsive: true, displayModeBar: false }
            Plotly.newPlot('myLinePlot', data, layout, config);
        }
    }
}
</script>