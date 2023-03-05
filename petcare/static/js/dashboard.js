const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']");
const latestTickets = document.getElementById("latestTickets");

function updateStatus(id) {
  const updatedRow = document.getElementById(id);
  const statusElement = updatedRow.querySelector("td:nth-child(4)");
  const dropDownElement = updatedRow.querySelector("td:nth-child(5) select");
  let formData = new FormData();
  formData.append("id", id);
  formData.append("csrfmiddlewaretoken", csrfToken.value);
  formData.append("status", dropDownElement.value);
  fetch("/dashboard/", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data.submitted) return alert("Data updation failed!");
      if (dropDownElement.value == "RESCUED")
        statusElement.innerHTML =
          '<span class="bg-green-100 text-green-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full dark:bg-green-900 dark:text-green-300">Rescued</span>';
      else
        statusElement.innerHTML =
          '<span class="bg-gray-100 text-gray-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full dark:bg-gray-700 dark:text-gray-300">Not Rescued</span>';
    })
    .catch((err) => console.log(err));
}

function handleAcceptReject(status, id){
    const formData = new FormData();
    formData.append("id", id);
    formData.append("status", status);
    formData.append("csrfmiddlewaretoken", csrfToken.value);
    fetch("/api/", {
      method: "POST",
      body: formData,
    }).then((res)=>res.json())
    .then((data)=>{
        if(!data.submitted) alert("Some error occurred!");
        
    })
}

function updateLatestTickets(data) {
  let element = `
    <div class="flex gap-y-2 gap-x-3">
            <img width="200px" class="object-cover rounded-md" src="http://127.0.0.1:8000${data.image}" alt="Image">
            <div class="space-y-1">
                <div class="flex gap-x-2">
                    <i class="fa-solid fa-image"></i>
                    <a href="${data.image}">http://localhost:8000${data.image}</a>
                </div>
                <div class="flex gap-x-2">
                    <i class="fa-solid fa-location-dot"></i>
                    <a href="${data.mapurl}">${data.mapurl}</a>
                </div>
                <div class="text-justify">${data.address}</div>
                <div class="flex gap-2">
                    <button class="bg-green-600 hover:bg-green-700 p-1.5 rounded-xl border-none">Accept</button>
                    <button class="bg-red-600 hover:bg-red-700 p-1.5 rounded-xl border-none">Reject</button>
                </div>
            </div>
        </div>
    `;
}

async function getLatestTickets() {
  fetch("/api/")
    .then((data) => data.json())
    .then((data) => data.forEach((ticket) => updateLatestTickets(data)))
    .catch((err) => console.log(err));
}

setInterval(() => {
  getLatestTickets();
}, 60000);
