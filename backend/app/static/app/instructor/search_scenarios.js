
let slist = new Vue({
    el: "#vue",
    delimiters: ['[[', ']]'],
    data: {
        scenarios: [],
    }
});

async function load_scenarios() {
    const res = await fetch('http://127.0.0.1:8000/scenarios/');
    const data = await res.json();
    console.log(data)
    slist._data.scenarios = data.scenarios;
}