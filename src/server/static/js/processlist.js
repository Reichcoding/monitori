
if(localStorage.getItem("green_process")== null){
    localStorage.setItem("green_process","Visual Studio Code,Firefox Developer Edition")
    localStorage.setItem("yellow_process","")
    localStorage.setItem("red_process","")
}
let good = localStorage.getItem("green_process").split(",")
let yellow = localStorage.getItem("yellow_process").split(",")
let red = localStorage.getItem("red_process").split(",")

function template(name,pcid){
    color = "secondary";
    if(good.includes(name)){
        color = "success";
    }else if(yellow.includes(name)){
        color = "warning";
    }else if(red.includes(name)){
        color = "danger"
    }
    to_kill_name = name.split(" ")[0]
    return `
    <div class="row mt-1">
    <div class=" btn btn-outline-${color} col-9 " onclick="navigator.clipboard.writeText(this.innerText)">
        ${name}
    </div>
    <form action="send_command_pc_${pcid}" method="post">
        <input type="hidden" name="cmd" value="taskkill /f /im ${to_kill_name}*">
        <input type="submit" class="btn btn-danger" value="Завершить">
    </form>
    </div>
    `;
}

function updateProcessList(this_pc_id){
    process = pcs[this_pc_id]['process']

    processbody = document.querySelector("#process_list");

    generate = ""
    process.forEach(process => {
        generate+=template(process,this_pc_id)
        // console.log(process)
    });
    processbody.innerHTML = generate;

}