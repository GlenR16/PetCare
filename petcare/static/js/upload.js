const fileInput = document.getElementById("dropzone-file");
fileInput.addEventListener("change", getLocation);

function getLocation() {
  if (!navigator.geolocation) return alert("Please provide location access!");
  navigator.geolocation.getCurrentPosition(handleUpload, (err) =>
    alert("Some error occured!")
  );
}

function handleUpload(position) {
  const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']");
  let file = fileInput.files[0];
  if (!file) return alert("Please select an image to upload!");
  let formData = new FormData();
  formData.append("csrfmiddlewaretoken", csrfToken.value);
  formData.append("latitude", position.coords.latitude);
  formData.append("longitude", position.coords.longitude);
  formData.append("image", fileInput.files[0]);
  fetch("/upload/", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data.submitted) alert("Some error occured!\nPlease try again.");
      else alert("Image uploaded successfully.");
    })
    .catch((err) => {
      console.log(err);
    });
}
