/**
 * This file contains the Chart Elements that are used to represent the two line charts: Cost and Task Chart. All
 * functions that CRUD these charts are also contained in this file.
 */

/* ======== INITIALIZE CHARTS ======== */
const chartLabels = ["Week 0", "Week 1", "Week 2", "Week 3", "Week 4", "Week 5"]
/* TASK CHART */
const ctxTasks = document.getElementById("tasks-chart").getContext("2d");
const taskChart = new Chart(ctxTasks, {
    type: 'line',
    data: {
        labels: chartLabels,
        datasets: [{
            data: [0],
            label: "Done",
            borderColor: "#FF55AA",
            fill: false
        }, {
            data: [0],
            label: "Unit Tested",
            borderColor: "#55FF55",
            fill: true
        },
        {
            data: [0],
            label: "Integration Tested",
            borderColor: "#5555AA",
            fill: true
        },
        {
            data: [0],
            label: "Bugs",
            borderColor: "#AA55AA",
            fill: false
        },
        ]
    },
    options: {
        title: {
            display: true,
            text: 'Cost'
        },
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    boxWidth: 3,
                    boxHeight: 3,
                }
            }
        }
    

    }
});

/* COST CHART */
const ctxCost = document.getElementById("cost-chart").getContext("2d");

const costChart = new Chart(ctxCost, {
    type: 'line',
    data: {
        labels: chartLabels,
        datasets: [{
            data: [0],
            label: "Actual",
            borderColor: "#FF55AA",
            fill: false
        }
        ]
    },
    options: {
        title: {
            display: true,
            text: 'Cost'
        },
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    boxWidth: 3,
                    boxHeight: 3
                }
            }
        }
    }
});

/* ======= CRUD FUNCTIONS ======= */


/**
 * Adds data to a chart that represents a week.
 * A week is described by the following data:
 * @param chart The chart
 * @param value The value of the week to add
 * @param label The label of the data row where that value is to be added
 */
function addWeek(chart, value, label = "Actual") {
    let weeks = 0;
    chart.data.datasets.forEach((dataset) => {
        if (dataset.label === label) {
            dataset.data.push(value)
            weeks = dataset.data.length
        }
    })
    adjustWeekLabel(chart, weeks)
    chart.update()
}

function addChartDataRow(chart, dataArr, label, color = "#55AAFF") {
    chart.data.datasets.push(
        {
            data: dataArr,
            label: label,
            borderColor: color,
            fill: false
        })
    chart.update()
}

function initializeCharts(budget, tasks, weeks) {
    const weekly_budget = budget / weeks
    const cost_data = []
    for (let i = 0; i <= weeks; i++) {
        cost_data.push(i * weekly_budget)
    }

    const weekly_tasks = tasks / weeks
    const task_data = []
    for (let i = 0; i <= weeks; i++) {
        task_data.push(i * weekly_tasks)
    }

    /*Add null values for weeks that have passed (if a scenario is loaded that already is half way through)*/
    if (x.$data.current_day > 0) {
        for (let i = 0; i < x.$data.current_day / 5; i++) {
            addWeek(costChart, null)
            addWeek(taskChart, null)
        }
    }

    adjustWeekLabel(costChart, weeks)
    adjustWeekLabel(taskChart, weeks)
    addChartDataRow(costChart, cost_data, "Management Goal")
    addChartDataRow(taskChart, task_data, "Management Goal")
}

function adjustWeekLabel(chart, week) {
    if (chart.data.labels.length <= week) {
        for (let i = chart.data.labels.length; i <= week; i++) {
            chart.data.labels.push("Week " + i);
        }
    }
}