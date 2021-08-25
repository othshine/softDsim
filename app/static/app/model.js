let x = new Vue({
        el: "#scenario",
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
         }
      });


/* Load Continue */
let COUNTER = 0
async function cont(){
    const response = await fetch('continue?counter=' + COUNTER);
    const j = await response.json();
    x._data.blocks = j;
    COUNTER += 1;
}