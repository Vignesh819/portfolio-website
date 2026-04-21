document.addEventListener("DOMContentLoaded", function(){

    // ----------- TABS FUNCTION -----------
    const tablinks = document.getElementsByClassName("tab-links");
    const tabcontents = document.getElementsByClassName("tab-contents");

    window.opentab = function(tabname, event){

        // remove all active classes
        for (let tablink of tablinks){
            tablink.classList.remove("active-link");
        }

        for (let tabcontent of tabcontents){
            tabcontent.classList.remove("active-tab");
        }

        // add active to clicked tab
        if (event && event.currentTarget){
            event.currentTarget.classList.add("active-link");
        }

        // show selected content
        const tab = document.getElementById(tabname);
        if (tab){
            tab.classList.add("active-tab");
        }
    };

    // ----------- SIDEMENU -----------
    const sidemenu = document.getElementById("sidemenu");

    window.openmenu = function(){
        if (sidemenu) sidemenu.style.right = "0";
    };

    window.closemenu = function(){
        if (sidemenu) sidemenu.style.right = "-200px";
    };

    // ----------- DELETE MESSAGE -----------
    window.deleteMsg = function(id){
        fetch(`/delete/${id}`, { method: "POST" })
        .then(() => location.reload())
        .catch(error => console.log("Delete error:", error));
    };

    // ----------- LOAD ADMIN DATA -----------
    let table = document.getElementById("table-data");

    if (table){
        fetch("/api/messages")
        .then(res => res.json())
        .then(data => {
            let html = "";

            data.forEach(msg => {
                html += `
                <tr>
                    <td>${msg.id}</td>
                    <td>${msg.name}</td>
                    <td>${msg.email}</td>
                    <td>${msg.message}</td>
                    <td><button onclick="deleteMsg(${msg.id})">Delete</button></td>
                </tr>`;
            });

            table.innerHTML = html;
        })
        .catch(error => console.log("Error loading data:", error));
    }

});