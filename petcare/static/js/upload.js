const fileInput = document.getElementById("fileInput");

function handleUpload(e) {
  e.preventDefault();
  let [file, location] = [fileInput.files[0], undefined];
  if (!file) return alert("No Image selected to upload.");
  if (!navigator.geolocation) return alert("Please provide location access!");
  navigator.geolocation.getCurrentPosition((location, err) => {
    if (err) return alert("Some error occured.");
    location.latitude = location.coords.latitude;
    location.longitude = location.coords.longitude;
  });
  fetch("/upload/", {
    method: "POST",
    body: {
      file,
      latitude: location.latitude,
      longitude: location.longitude,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data.submitted) alert("Some error occured");
      else alert("Image uploaded successfully.");
    })
    .catch((err) => {
      console.log(err);
    });
}
