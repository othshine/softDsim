

data = {
  phases : [
    {
      name: "Requirements",
      predefined: 30,
      scheduled: 35,
    },
    {
      name: "Design",
      predefined: 10,
      scheduled: 12,
    },
    {
      name: "Implementation",
      predefined: 50,
      scheduled: 74,
    },
    {
      name: "Testing",
      predefined: 10,
      scheduled: 8,
    },
    {
      name: "Training",
      predefined: 10,
      scheduled: 8,
    }
  ],
  current: 39
}


function transformData(data){
  let predefined_counter = 0;
  let scheduled_counter = 0;

  for (let d of data.phases){
    d.predefinedStart = predefined_counter
    d.predefinedEnd = d.predefined + predefined_counter
    d.scheduledStart = scheduled_counter
    d.scheduledEnd = d.scheduled + scheduled_counter
    scheduled_counter = d.scheduledEnd
    predefined_counter = d.predefinedEnd
  }
  return data;
}

function getInfoObejct(data){
  const obj = {};
  obj.phaseCount = data.phases.length;
  const lastPhase = data.phases[data.phases.length - 1];
  obj.totalLenght = Math.max(lastPhase.scheduledEnd, lastPhase.predefinedEnd)
  return obj;
}

function transformDataToPercentage(data, maxLen){
  for (let d of data.phases){
    for (let value of ["predefined", "scheduled","predefinedStart", "scheduledStart","predefinedEnd", "scheduledEnd"]){
      d[value] = d[value] / maxLen
    }
  }
}

function renderGantt(id){
  const el = docoment.getElementById(id);
  el.innerHTML = '';

  const chart = document.createElement("div")



  el.appendChild( chart );
}
