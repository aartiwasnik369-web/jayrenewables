function calc(){
let bill=document.getElementById("bill").value
let system=bill/1000
document.getElementById("result").innerHTML=
"You need approx "+system.toFixed(2)+" KW solar system"
}