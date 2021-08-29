let x = new Vue({
        el: "#vue",
        delimiters: ['[[', ']]'],
        data:{
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
let COUNTER = 0
async function cont(){
    const response = await fetch('continue?counter=' + COUNTER);
    const data = await response.json();
    x._data.blocks = data.blocks;
    x._data.tasks = data.tasks;
    x._data.continue_text = data.continue_text
    COUNTER += 1;
}