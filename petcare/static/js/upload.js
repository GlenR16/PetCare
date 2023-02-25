const fileInput = document.getElementById("dropzone-file");

function handleUpload() {
  let file = fileInput.files[0];
  if (!file) return alert("No Image selected to upload.");
  if (!navigator.geolocation) return alert("Please provide location access!");
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const csrfToken = document.querySelector(
        "input[name='csrfmiddlewaretoken']"
      );
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
          if (!data.submitted) alert("Some error occured");
          else alert("Image uploaded successfully.");
        })
        .catch((err) => {
          console.log(err);
        });
    },
    (err) => {
      alert("Some error occured.");
    }
  );
}
