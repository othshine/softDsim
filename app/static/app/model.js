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
        staff: {
            junior: "",
            senior: "",
            expert: ""
        },
        cost: 0,
        meetings: 0
    },
    filters: {
    toCurrency (value) {
      return `${value.toLocaleString('de-DE', {style:'currency', currency:'EUR'})}`
    }
  }
});


/* Load Continue */
let COUNTER = 0 // ToDo: Count on server side by having a flag at the current decision.

function readButton(elementId) {
    for (const button of document.getElementById(elementId).children){
        if (button.classList.contains('active-button')){
            return button.innerText;
        }
    }
    return null;
}


function countStaff(staffType) {
    return document.getElementById("staff-number-"+staffType).innerText.length;
}

/**
 * Reads the current setting that the user as applied.
 * (Status of all buttons etc.)
 * @returns {*}
 */
function getSettings() {

    return {
        'model': readButton('model-picker-container'),
        'lifecycle': readButton('lifecycle-picker-container'),
        'meetings': x._data.meetings,
        'staff': {
            'junior': countStaff('junior'),
            'senior': countStaff('senior'),
            'expert': countStaff('expert'),
            'consultant': countStaff('consultant')

        }
    };
}

async function cont() {
    const s = window.location.pathname.split('/').slice(-1)[0]
    const response = await fetch('/continue/'+ s,
        {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify(getSettings())
        }
    );
    const data = await response.json();
    x._data.blocks = data.blocks;
    x._data.tasks_done = data.tasks_done;
    x._data.tasks_total = data.tasks_total;
    x._data.continue_text = data.continue_text
    x._data.staff.junior = data.staff.junior
    x._data.staff.senior = data.staff.senior
    x._data.staff.expert = data.staff.expert
    x._data.cost = data.cost
    addWeek(costChart, data.actual_cost, COUNTER)
    COUNTER += 1;
}
