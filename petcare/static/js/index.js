const menuToggle = document.getElementById("nav-toggle");
const navDropdown = document.getElementById("menu");
menuToggle.addEventListener("click", () => {
  if (navDropdown.classList.contains("hidden"))
    navDropdown.classList.replace("hidden", "block");
  else navDropdown.classList.add("block", "hidden");
});

msg_sent_toast = document.getElementById("msg-sent");
if (msg_sent_toast){
  setTimeout(function () {
    msg_sent_toast.classList.add("hidden");
  }, 6000);
}

