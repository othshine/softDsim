


/* Load Continue */

/**
 * Function is called when user clicks on the continue button while playing a scenario. Everything that has to do with
 * fetching updating the data happens here.
 * @returns {Promise<void>}
 */
async function cont() {
    const s = window.location.pathname.split('/').slice(-1)[0]
    x.$data.advance = document.getElementById('continue-button').innerText.toLowerCase() !== "start"
    const response = await fetch('/continue/' + s,
        {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(x._data)
        }
    );

    if (response.status === 403){
        alert("This is not a valid scenario id")
    }
    const data = await response.json();
    if (data['done'] === true) {
        window.location.href = '/result/' + s
    } else {
        for (const dataKey in data) {
            x._data[dataKey] = data[dataKey]
        }
        if (costChart.data.datasets.length === 1) {
            initializeCharts(data['budget'], data['tasks_total'], data['scheduled_days'] / 5)
        }
        if ((costChart.data.datasets[0].data.length - 1) * 5 < data['current_day']) {
            addWeek(costChart, data['actual_cost'])
            addWeek(taskChart, data['tasks_done'], 'Tasks Done')
            addWeek(taskChart, data['tasks']['tested'], 'Tasks Tested')
        }
    }
    set_continue_button()
}

async function endScenario(){

}
