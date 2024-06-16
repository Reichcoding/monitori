

var pcs = {}

function get_pcs(){
    axios.post('/get_pcs')
    .then(function (response) {
        pcs = response.data
        update_cards()
    })
    .catch(function (error) {
        console.log(error);
    });
}

if(localStorage.getItem("data_update_speed")== null){
    localStorage.setItem("data_update_speed",5)
}

setInterval(get_pcs,parseInt(localStorage.getItem("data_update_speed"))*1000);
get_pcs()
function update_cards(){

    
    cards = document.querySelectorAll(".pc_card");
    cards.forEach(card => {
        id = card.id.split("_")[1];
        // Удаление просроченных карточек
        if(!pcs[id]){
            remove_card(id)
        }
        // Если подключение имеется, обновляется карточка
        else{   
            pc_data(id,pcs[id]["cpu_use_perc"],pcs[id]["ram_use_perc"],pcs[id]["disk_use_perc"],pcs[id]["ram_use_gb"],pcs[id]["ram_total"],pcs[id]["disk_use_gb"],pcs[id]["disk_total"],pcs[id]["battery"])
        }
    });
    // Добавление карточек при появлении нового пк
    Object.keys(pcs).forEach(key => {
        if(!card_is_alive(key)){
            data = [pcs[key]["cpu_use_perc"],pcs[key]["ram_use_perc"],pcs[key]["disk_use_perc"],pcs[key]["ram_use_gb"],pcs[key]["ram_total"],pcs[key]["disk_use_gb"],pcs[key]["disk_total"],pcs[key]["battery"]]
            if(document.querySelector(".card-container")){
                generate_card(pcs[key]["pc_name"],key,pcs[key]["ip"],data)
            }
            generate_pc_sidebar(pcs[key]["pc_name"],key,pcs[key]["ip"])
           
        }
    });

}

var pc_online = 1
setInterval(function() {
    pc_online = Object.keys(pcs).length
    document.querySelector("#online").innerText = pc_online
},1000);

// function pc_stop(pc_id){
//     console.log("pc_stop",pc_id)
// }
// function pc_reboot(pc_id){
//     console.log("pc_reboot",pc_id)
// }
function card_is_alive(pc_id){
    if(document.querySelector(`#pc_${pc_id}`)){
        return true
    }
    return false
}

function progress_change(pc_id,selector,data,abbr){

    document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).innerText = data + abbr;
    document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).style.width=data + "%";
    
    if(data<10){
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.add("bg-success")
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.remove("bg-primary")
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.remove("bg-warning")
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.remove("bg-danger")
    }
    else if(data<50){
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.remove("bg-success")
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.add("bg-primary")
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.remove("bg-warning")
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.remove("bg-danger")
    }
    else if(data<75){
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.remove("bg-success")
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.remove("bg-primary")
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.add("bg-warning")
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.remove("bg-danger")
    }
    else{
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.remove("bg-success")
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.remove("bg-primary")
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.remove("bg-warning")
        document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).classList.add("bg-danger")
    }
}
function data_change(pc_id,selector,data){

    document.querySelector(`#pc_${pc_id}`).querySelector(`${selector}`).innerText = data;
}

function pc_data(pc_id,cpu_usage,ram_usage,disk_usage,ram_used,ram_total,disk_used,disk_total,battery){
    
    progress_change(pc_id,".cpu_usage",cpu_usage,"%");
    progress_change(pc_id,".ram_usage",ram_usage,"%");
    progress_change(pc_id,".disk_usage",disk_usage,"%");
    data_change(pc_id,".cpu_usage_data_only",`${cpu_usage}%`)
    data_change(pc_id,".ram_used",ram_used)
    data_change(pc_id,".ram_total",ram_total)
    data_change(pc_id,".disk_used",disk_used)
    data_change(pc_id,".disk_total",disk_total)
    if(battery!=false){
        document.querySelector(`#pc_${pc_id}`).querySelector(`.battery_container`).hidden=false;
        data_change(pc_id,".battery_perc",`${battery}%`)
        progress_change(pc_id,".battery_perc_prog",battery,"%");
    }else{
        document.querySelector(`#pc_${pc_id}`).querySelector(`.battery_container`).hidden=true;
    }


}




