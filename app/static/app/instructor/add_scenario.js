

const input = document.getElementById('name-input');
const btn = document.getElementById('add-sc-btn');

function checkValidity() {
  if (hasWhiteSpace(input.value)){
    input.classList.add("invalid")
    btn.disabled = true;
  } else {
    input.classList.remove("invalid")
    btn.disabled = false;
  }
}

input.addEventListener('input', checkValidity)




function hasWhiteSpace(s) {
  return s.indexOf(' ') >= 0;
}