


/* Staff Picker */


function pickerAdd(n){
  x._data.staff[n] += "•";
}

function pickerSub(n){
  const str = x._data.staff[n];
  x._data.staff[n] = str.substring(0, str.length - 1)
}


/* Model Picker */

function pickButton(n, element, m){
  for (let i of Array(m).keys()){
    const x = (n+i) % m
    document.getElementById(element).children[x].classList.remove("active-button");
  }

  document.getElementById(element).children[n].classList.add("active-button");
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

new Chart(ctxCost, {
  type: 'line',
  data: {
    labels: labels,
    datasets: [{ 
        data: [0, 20, 40, 60, 80, 100],
        label: "Management Goals",
        borderColor: "#55AAFF",
        fill: false
      }, { 
        data: [0, 10, 40, 65, 95, 128],
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
        data: [0, 5, 15, 40, 75, 100],
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