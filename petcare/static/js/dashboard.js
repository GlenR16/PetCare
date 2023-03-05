const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']");
const latestTickets = document.getElementById("latestTickets");

function updateStatus(id){
    const updatedRow = document.getElementById(id);
    const statusElement = updatedRow.querySelector("td:nth-child(4)")
    const dropDownElement = updatedRow.querySelector("td:nth-child(5) select")
    let formData = new FormData();
    formData.append("id", id);
    formData.append("csrfmiddlewaretoken", csrfToken.value);
    formData.append("status", dropDownElement.value);
    fetch("/dashboard/", {
        method: "POST",
        body: formData,
    } ).then((response)=>response.json())
    .then((data)=>{
        if (!data.submitted) return alert("Data updation failed!");
        if(dropDownElement.value == "RESCUED")
        statusElement.innerHTML = '<span class="bg-green-100 text-green-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full dark:bg-green-900 dark:text-green-300">Rescued</span>';
        else
        statusElement.innerHTML = '<span class="bg-gray-100 text-gray-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded-full dark:bg-gray-700 dark:text-gray-300">Not Rescued</span>'
    })
    .catch((err) => {
        console.log(err);
      });
}

function updateLatestTickets(data){


}

async function getLatestTickets(){
    fetch("/api/")
    .then((data)=>data.json())
    .then((data)=>data.forEach((ticket)=>updateLatestTickets(data)))
    .catch((err)=>console.log(err))
}

setInterval(() => {
    getLatestTickets();
}, 60000);