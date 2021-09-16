


/* Staff Picker */


function pickerAdd(n){
  x._data.staff[n] += "•";
}

function pickerSub(n){
  const str = x._data.staff[n];
  x._data.staff[n] = str.substring(0, str.length - 1)
}

/* Meetings */
function addMeeting(){
  if (x._data.meetings < 8){
    x._data.meetings += 1
  }
}

function subMeeting(){
  if (x._data.meetings > 0){
    x._data.meetings -= 1
  }

}


/* Activity Distribution Chart */

function calculateActivityLength(meetings, trainings){
  let m = (meetings / 40)*100;
  let t = (trainings / 40) * 100;
  let d = 100 - m - t;
  return [d, m, t]
}


function makeActivityChart(length) {
  const children = document.getElementById("activity-distribution-container").children;
  const colors = ['#55AAFF', '#AAFF55', '#FF55AA']
  for (let i of [0,1,2]){
    children[i].style.backgroundColor = colors[i]
    children[i].style.width = "" + length[i] + "%"
  }
}



/* Graphs */
const ctxCost = document.getElementById("cost-chart").getContext("2d");
const labels = ["Week 0", "Week 1", "Week 2", "Week 3", "Week 4", "Week 5"]

const costChart = new Chart(ctxCost, {
  type: 'line',
  data: {
    labels: labels,
    datasets: [{ 
        data: [0, 20000, 40000, 60000, 80000, 100000],
        label: "Management Goals",
        borderColor: "#55AAFF",
        fill: false
      }, { 
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
    }
  }
});

function addWeek(chart, value, week, label="Actual"){
  if (chart.data.labels.length <= week){
    chart.data.labels.push("Week " + week);
  }
  chart.data.datasets.forEach((dataset) => {
    if (dataset.label === label){
      dataset.data.push(value)
    }
  })
  chart.update()
}

const ctxTasks = document.getElementById("tasks-chart").getContext("2d");
new Chart(ctxTasks, {
  type: 'line',
  data: {
    labels: labels,
    datasets: [{ 
        data: [0, 20, 40, 60, 80, 100],
        label: "Management Goals",
        borderColor: "#55AAFF",
        fill: false
      }, { 
        data: [],
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
    }
  }
});