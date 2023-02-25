const menuToggle = document.getElementById("nav-toggle");
const navDropdown = document.getElementById("menu");
menuToggle.addEventListener("click", () => {
  if (navDropdown.classList.contains("hidden"))
    navDropdown.classList.replace("hidden", "block");
  else navDropdown.classList.add("block", "hidden");
});
