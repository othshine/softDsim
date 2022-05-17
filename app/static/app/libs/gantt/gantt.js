

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

/**
 * Transforms data that only consists of phases with predefined/scheduled times to have a start and end time for each
 * time. It does it in a manner so that all phases are consecutive. Scheduled and Predefined are both separate from
 * another.
 * The phases are scheduled in the order as they appear in the phases array.
 * data = {phases : [ {name: 'xy', predefined: 20, scheduled: 22},... ], current: 5 }
 * @param data
 * @returns data object including the calculated start and end times for each phase and each time type.
 */
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

/**
 * Calculates the info object for a data object. The info object contains two values:
 * phasesCount (number of phases of the data object)
 * totalLength (The total length of all phases, which equals the end time of the last phase [notice that 100% can either
 * be the predefined or scheduled end, which ever is larger])
 * @param data
 * @returns {{phasesCount, totalLength}}
 */
function getInfoObject(data){
  const obj = {};
  obj.phaseCount = data.phases.length;
  const lastPhase = data.phases[data.phases.length - 1];
  obj.totalLenght = Math.max(lastPhase.scheduledEnd, lastPhase.predefinedEnd)
  return obj;
}

/**
 * Transforms all the time values of the data object from absolute values into percentages (0,...,100) (100% being the
 * total length of the project)
 *
 * @param data
 * @param maxLen The total length of the project (Number by that every value will be divided by)
 */
function transformDataToPercentage(data, maxLen){
  for (let d of data.phases){
    for (let value of ["predefined", "scheduled","predefinedStart", "scheduledStart","predefinedEnd", "scheduledEnd"]){
      d[value] = (d[value] / maxLen )*100
    }
  }
}

/**
 * Creates a html element that represents a row in the gantt chart.
 *
 * @param phase a to percentages transformed phase object as they appear in the data.phases array
 * @param phaseCount the number of total phases (to calculate the height of each row)
 * @returns {HTMLDivElement}
 */
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

  segment.style.backgroundColor = '#FF55AA';

  innerBar.appendChild(filler)
  innerBar.appendChild(segment)

  innerContainer.appendChild(innerBar)

  const innerBar2 = generateDiv('gantt-inner-bar')
  const filler2 = generateDiv('gantt-filler')
  const segment2 = generateDiv('gantt-bar-segment')
  filler2.style.width = "" + phase.predefinedStart + "%";
  segment2.style.width = "" + phase.predefined + "%";

  segment2.style.backgroundColor = '#54AAFF';

  innerBar2.appendChild(filler2)
  innerBar2.appendChild(segment2)

  innerContainer.appendChild(innerBar2)

  bar.appendChild(innerContainer)

  row.appendChild(bar)

  return row;
}

/**
 * Helper Function: generates and returns a div with given class c.
 * @param c String that will be the css class of the returned div, or null if element should not have a class.
 * @returns {HTMLDivElement}
 */
function generateDiv(c){
  const div = document.createElement('div');
  if (c){
    div.setAttribute('class', c)
  }
  return div;
}

/**
 * Renders a gantt chart on html element with id 'id'. The element needs to have a size that is recommended to be at
 * least 300x300px.
 *
 * The data object needs to be in the following format:
 * data = {
 *     phases : [
 *    {
 *      name: "Requirements",
 *      predefined: 30,
 *      scheduled: 35,
 *    },
 *    {
 *      name: "Design",
 *      predefined: 10,
 *      scheduled: 12,
 *    },
 *    ...
 *  ],
 *  current: 39
 * }
 *
 * Each phase will be represented as one row in the gantt chart. Each phase has two bars with one being the predefined
 * time the other one being the scheduled time. The phases are planned in consecutive manner as they appear in the
 * array. Each predefined bar follows directly on the predecessor, and each scheduled bar follows on its predecessor.
 * The count can be set to a absolute value. A vertical line will appear in the gantt chart indicating, that this is the
 * current time/progress.
 *
 * @param id
 * @param data
 */
function renderGantt(id, data){
  const el = document.getElementById(id);
  el.innerHTML = '';
  const chart = generateDiv('chart')
  data = transformData(data)
  const infoObj = getInfoObject(data)
  transformDataToPercentage(data, infoObj.totalLenght)
  for (phase of data.phases){
    chart.appendChild(generateGanttRow(phase, infoObj.phaseCount))
  }
  el.appendChild( chart );
}
