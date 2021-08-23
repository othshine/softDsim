


/* Staff Picker */


function pickerAdd(n){
  document.getElementById("staff-number-container").children[n].innerText += "•"
}

function pickerSub(n){
  const str = document.getElementById("staff-number-container").children[n].innerText;
  document.getElementById("staff-number-container").children[n].innerText = str.substring(0, str.length - 1)
}


/* Model Picker */

function pickModel(n){
  document.getElementById("model-picker-container").children[n].style.backgroundColor = '#5863f8ff';
  document.getElementById("model-picker-container").children[n].style.color = '#FFFFFF';
  
  for (i of [1,2]){
    const x = (n+i) % 3
    document.getElementById("model-picker-container").children[x].style.backgroundColor = "#F0F0F0"
    document.getElementById("model-picker-container").children[n].style.color = "#22181cff";
  }
  

}


/* Activity Distribution Chart */

function calculateActivityLenght(meetings, trainings){
  let m = (meetings / 40)*100;
  let t = (trainings / 40) * 100;
  let d = 100 - m - t;
  return [d, m, t]
}


function makeActivityChart(lenghts) {
  const childs = document.getElementById("activity-distribution-container").children;
  const colors = ['#55AAFF', '#AAFF55', '#FF55AA']
  for (i of [0,1,2]){
    childs[i].style.backgroundColor = colors[i]
    childs[i].style.width = "" + lenghts[i] + "%"
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