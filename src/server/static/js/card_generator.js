
function remove_card(pc_id){
    document.querySelector(`#pc_${pc_id}`).remove();
    document.querySelector(`#pc_sidebar_${pc_id}`).remove()
}
function generate_pc_sidebar(pc_name,pc_id){

    if(document.querySelector(`#pc_sidebar_${pc_id}`)!=null){
        return
    }
    document.querySelector(".pc_sidebars").innerHTML += 
    `
    <li class="nav-item pc_sidebar" id="pc_sidebar_${pc_id}">
        <a class="nav-link" href="/pc_data_${pc_id}">
            <i class="fas fa-fw fa-desktop"></i>
        <span>${pc_name}</span></a>
    </li>
    `;
};
function generate_card(pc_name,pc_id,pc_ip,data=false){
    if(document.querySelector(`#pc_${pc_id}`)!=null){
        return
    }
    document.querySelector(".card-container").innerHTML += 
    `
    <div class="col-12 col-sm-12 col-md-6 col-lg-4 col-xl-3 pc_card" id="pc_${pc_id}">
        <a href="/pc_data_${pc_id}" class="text-gray-600 text-decoration-none">
        <div class="card shadow mb-4">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">${pc_name} <span class="float-right text-xs mt-1 text-gray-800">${pc_ip}</span></h6>
                
            </div>
            <div class="card-body">
                <h4 class="small font-weight-bold">Загрузка ЦП <span class="float-right cpu_usage_data_only">20%</span></h4>
                <div class="progress mb-4">
                    <div class="progress-bar cpu_usage" role="progressbar" style="width: 20%" aria-valuenow="20"
                        aria-valuemin="0" aria-valuemax="100"></div>
                </div>
                <h4 class="small font-weight-bold">Загрузка ОЗУ <span class="float-right"><span class="ram_used">0</span>GB / <span class="ram_total">0</span>GB</span></h4>
                <div class="progress mb-4">
                    <div class="progress-bar ram_usage " role="progressbar" style="width: 40%" aria-valuenow="40"
                        aria-valuemin="0" aria-valuemax="100"></div>
                </div>
                <h4 class="small font-weight-bold ">Загрузка диска <span class="float-right"><span class="disk_used">0</span>GB / <span class="disk_total">0</span>GB</span></h4>
                <div class="progress mb-4">
                    <div class="progress-bar disk_usage" role="progressbar" style="width: 60%" aria-valuenow="60" aria-valuemin="0"
                        aria-valuemax="100"></div>
                </div>
                <h4 class="small font-weight-bold">Батарея <span class="float-right battery_perc" >нет</span></h4>
                <div class="progress mb-4 battery_container" hidden>
                    <div class="progress-bar battery_perc_prog" role="progressbar" style="width: 80%" aria-valuenow="80"
                        aria-valuemin="0" aria-valuemax="100"></div>
                </div>
            </div>
        </div>
        </a>
    </div>
    `;
    if(data!=false){
        pc_data(pc_id,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7])
    }
};