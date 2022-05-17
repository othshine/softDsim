// ToDo: This may be deleted!

const input = document.getElementById('name-input');
const btn = document.getElementById('add-sc-btn');

input.addEventListener('input', checkValidity)

//btn.addEventListener('click', openDialog)

/**
 * Checks if the input field is valid and adds/removes the css class for invalid fields.
 */
function checkValidity() {
    if (hasWhiteSpace(input.value)) {
        input.classList.add("invalid")
        document.getElementById('add-sc-btn').disabled = true;
        console.log(document.getElementById('add-sc-btn').disabled)
    } else {
        input.classList.remove("invalid");
        document.getElementById('add-sc-btn').disabled = false;
        console.log(btn.disabled)
    }
}

/**
 * Checks if the given String s contains a whitespace.
 * @param s
 * @returns {boolean}
 */
function hasWhiteSpace(s) {
    return s.indexOf(' ') >= 0;
}

function openDialog() {
    this.$root.$emit("bv::show::modal", "your-modal-id");
}

// register modal component
Vue.component("modal", {
    template: "#modal-template"
});

// start app
new Vue({
    el: "#app",
    data: {
        showModal: false,
    }
});