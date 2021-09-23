let x = new Vue({
    el: "#vue",
    delimiters: ['[[', ']]'],
    data: {
        blocks:
            [
                {
                    header: "Welcome to this Scenario",
                    text: "Start the simulation by pressing Start in the lower right corner."
                }
            ],
        tasks_total: 0,
        tasks_done: 0,
        continue_text: "Start",
        cost: 0,
        meetings: 0,
        button_rows: [],
        numeric_rows: [], // ToDo: Make sure values cant be below 0.

    },
    filters: {
        toCurrency(value) {
            return `${value.toLocaleString('de-DE', {style: 'currency', currency: 'EUR'})}`
        }

    },
    methods: {
        /**
         * Activates an answer of a button row. Sets the active attr of that answer to true.
         * @param row_index the index of the button row in vue data button_rows
         * @param answer_index the index of the answer in that row.
         */
        vuePickButton(row_index, answer_index) {
            const answers = this.button_rows[row_index]['answers']
            for (let k = 0; k < answers.length; k++) {
                answers[k].active = k === answer_index;
            }
        },
        getNumOfAnswers(arr) {
            return arr.length
        },
        /**
         * Returns a string with n dots • .
         * @param n Number of dots.
         * @returns {string}
         */
        dots(n) {
            let d = "";
            for (let i = 0; i < n; i++) {
                d += "•"
            }
            return d;
        },
        numericPicker(i, j, op) {
            let v = -1
            if (op === "add") {
                v = 1
            }
            let count = this.numeric_rows[i]['values'][j];
            if (!(count < 1 && v === -1)) {
                this.numeric_rows[i]['values'][j] += v;
            }


        }


    }
});


/* Load Continue */
let COUNTER = 0 // ToDo: Count on server side by having a flag at the current decision.

function readButton(elementId) {
    for (const button of document.getElementById(elementId).children) {
        if (button.classList.contains('active-button')) {
            return button.innerText;
        }
    }
    return null;
}


function countStaff(staffType) {
    return document.getElementById("staff-number-" + staffType).innerText.length;
}

async function cont() {
    const s = window.location.pathname.split('/').slice(-1)[0]
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
    const data = await response.json();

    if (data['done'] === true) {
        window.location.href = '/result/' + s
    } else {
        for (const dataKey in data) {
            x._data[dataKey] = data[dataKey]
        }
        if (costChart.data.datasets.length === 1) {
            initializeCharts(data['budget'], data['tasks_total'], data['scheduled_days']/5)
        }

        console.log(data['current_day'])
        console.log(costChart.data.datasets[0].data.length * 5)
        if ((costChart.data.datasets[0].data.length-1) * 5 < data['current_day']){
            console.log(data['current_day'])
            addWeek(costChart, data['actual_cost'])
            addWeek(taskChart, data['tasks_done'])
        }

    }

}
