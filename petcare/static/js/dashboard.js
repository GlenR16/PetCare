const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']");
const latestTickets = document.getElementById("latestTickets");
let domparse = new DOMParser();

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
    let error = `
    <div id="toast-error" class="flex items-center w-full m-2 max-w-xs p-4 text-gray-500 bg-white rounded-lg shadow dark:text-gray-400 dark:bg-gray-800" role="alert">
      <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-orange-500 bg-orange-100 rounded-lg dark:bg-orange-700 dark:text-orange-200">
          <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>
          <span class="sr-only">Warning icon</span>
      </div>
      <div class="ml-3 text-sm font-normal">Mission was Rejected.</div>
      <button type="button" onclick="document.getElementById('toast-error').remove();" class="ml-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700" data-dismiss-target="#toast-error" aria-label="Close">
          <span class="sr-only">Close</span>
          <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
      </button>
    </div>
                `
    fetch("/api/", {
      method: "POST",
      body: formData,
    }).then((res)=>res.json())
    .then((data)=>{
        if(!data.submitted) document.getElementById("upperElement").prepend(domparse.parseFromString(error,"text/html").body.querySelector("div"));
        document.getElementById(id).remove();
    })
    
}

function updateLatestTickets(data) {
  let element = `
  <div class="p-2 w-1/2 " id="${data.id}">
    <div class=" bg-white rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 w-full flex h-[300px]">
      <a href="http://127.0.0.1:8000${data.image}" class="w-full h-full" target="_blank">
        <img class="rounded-l-lg w-full h-full" src="http://127.0.0.1:8000${data.image}" alt="Uploaded Image" height="100" />
      </a>
      <div class="flex flex-col p-2 w-full text-center">
        <a href="#">
          <h5 class="mb-1 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">${data.date_reported}</h5>
        </a>
        <p class="mb-2 font-normal text-gray-700 dark:text-gray-400 grow">${data.address}</p>
        <div class="flex align-center justify-center">
          <i class="fa-solid fa-location-dot"></i>
          <a href="${data.map_url}" target="_blank"> &nbsp;Google Maps</a>
        </div>
        <div class="inline-flex items-center px-2 w-full justify-center py-1 text-sm font-medium text-center text-white">
          <button class="bg-green-600 hover:bg-green-700 p-2 text-lg font-bold rounded-xl border-none mx-2" onclick='handleAcceptReject("ACCEPT",${data.id});'>Accept</button>
          <button class="bg-red-600 hover:bg-red-700 p-2 text-lg font-bold rounded-xl border-none mx-2" onclick='handleAcceptReject("REJECT",${data.id});'>Reject</button>
        </div>
      </div>
    </div>
  </div>
    `;
    let result = domparse.parseFromString(element,"text/html").body.querySelector("div");
    latestTickets.append(result);
}

async function getLatestTickets() {
  fetch("/api/")
    .then((data) => data.json())
    .then((data) => {
      if (data.length == 0) {document.getElementById("init_alert").classList.remove("hidden");} 
      data.forEach((ticket)=> {if (!document.getElementById(`${ticket.id}`)) updateLatestTickets(ticket);})
    })
    .catch((err) => console.log(err));
  document.getElementById("loadingsym").remove();
}

setInterval(() => {
  if (!document.getElementById("init_alert").classList.contains("hidden")) {
    document.getElementById("init_alert").classList.add("hidden");
  }
  loading = `
    <div role="status" id="loadingsym">
      <svg aria-hidden="true" class="w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/><path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/></svg>
      <span class="sr-only">Loading...</span>
    </div>
    `
  latestTickets.append(domparse.parseFromString(loading,"text/html").body.querySelector("div"));
  getLatestTickets();
}, 6000);

