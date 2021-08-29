let x = new Vue({
    el: "#vue",
    delimiters: ['[[', ']]'],
    data: {
        blocks:
            [
                {
                    header: "Story",
                    text: "You are the Engineer!"
                },
                {
                    header: "Time Line",
                    text: "You are at the throttle"
                }
            ],
        tasks: 0,
        continue_text: "Continue"
    }
});


/* Load Continue */
let COUNTER = 0 // ToDo: Count on server side by having a flag at the current decision.

function readButton(elementId) {
    for (const button of document.getElementById(elementId).children){
        console.log(button.classList)
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
        'staff': {
            'junior': countStaff('junior'),
            'senior': countStaff('senior'),
            'expert': countStaff('expert'),
            'consultant': countStaff('consultant')

        }
    };
}

async function cont() {
    const response = await fetch('continue/?counter=' + COUNTER,
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
    x._data.tasks = data.tasks;
    x._data.continue_text = data.continue_text
    COUNTER += 1;
}