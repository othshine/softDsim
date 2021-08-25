

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
      d[value] = (d[value] / maxLen )*100
    }
  }
}

function generateGanttRow(phase, phaseCount){
  const row = generateDiv('gantt-row')
  row.style.height = '' +(100/phaseCount) + '%'

  const label = generateDiv('gantt-label')
  const btn = document.createElement('button')
  btn.innerHTML = phase.name;
  label.appendChild(btn)

  row.appendChild(label)

  const sep = generateDiv('gantt-seperator')
  row.appendChild(sep)

  const bar = generateDiv('gantt-bar')
  const innerContainer = generateDiv('gantt-inner-bar-container')

  const innerBar = generateDiv('gantt-inner-bar')
  const filler = generateDiv('gantt-filler')
  const segment = generateDiv('gantt-bar-segment')
  filler.style.width = "" + phase.scheduledStart + "%";
  segment.style.width = "" + phase.scheduled + "%";

  innerBar.appendChild(filler)
  innerBar.appendChild(segment)

  innerContainer.appendChild(innerBar)

  const innerBar2 = generateDiv('gantt-inner-bar')
  const filler2 = generateDiv('gantt-filler')
  const segment2 = generateDiv('gantt-bar-segment')
  filler2.style.width = "" + phase.predefinedStart + "%";
  segment2.style.width = "" + phase.predefined + "%";

  segment2.style.backgroundColor = 'lightblue';

  innerBar2.appendChild(filler2)
  innerBar2.appendChild(segment2)

  innerContainer.appendChild(innerBar2)

  bar.appendChild(innerContainer)

  row.appendChild(bar)

  return row;
}

function generateDiv(c){
  const div = document.createElement('div');
  if (c){
    div.setAttribute('class', c)
  }
  return div;
}

function renderGantt(id, data){
  const el = document.getElementById(id);
  el.innerHTML = '';
  const chart = generateDiv('chart')


  data = transformData(data)
  const infoObj = getInfoObejct(data)
  transformDataToPercentage(data, infoObj.totalLenght)
  for (phase of data.phases){
    chart.appendChild(generateGanttRow(phase, infoObj.phaseCount))
  }



  el.appendChild( chart );
}
