console.log("ping");
// on click button with class "submit-button" run function
document.querySelector(".submit-button").addEventListener("click", async function() {
    //get the innertext of class text in class paper 1
    var text = document.querySelector('.paper-1 .text').innerText;
    res = await extract_info({context: text})
    document.querySelector('.paper-2 .text').innerText=res
    // get the value of the input with class "submit-bias"
    var bias = document.querySelector('.submit-bias').value;
    console.log(bias);
    res = await guide_message({guidance: bias,chat_log: ["User 1: "+text],current_user:"User 2:"})
    document.querySelector('.paper-1 .text').innerText+="\n\n"+res
});