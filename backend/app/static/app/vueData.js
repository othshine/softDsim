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
        salaries: 0,
        meetings: 0,
        button_rows: [],
        numeric_rows: [], // ToDo: Make sure values cant be below 0.
        motivation: 0,
        familiarity: 0,
        stress: 0,
        scrum: false,
        current_workday: false,
        advance: false,
        tasks: {}

    },
    filters: {
        toCurrency(value) {
            return `${value.toLocaleString('de-DE', {style: 'currency', currency: 'EUR'})}`
        },
        orEmpty(value) {
            if (value){
                return value;
            } return "-";
        },
        uppercase(value) {
            if (!value) {
                return '';
            }

            return value.toString().charAt(0).toUpperCase() + value.toString().slice(1);
        },
        percentage(value){
            return "" + Math.round(value*100) + "%"
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


        },
        /**
         * Removes the ith numeric row i the vue data object numeric rows array.
         * @param i
         * @returns {undefined}
         */
        remove_numeric_row(i){
            this.numeric_rows.splice(i, 1)
        },
        isScrumTeam(row){
            return row.title === "Scrum Team";
        }


    }
});