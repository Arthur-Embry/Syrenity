console.log("ping");
// on click button with class "submit-button" run function
document.querySelector(".submit-button").addEventListener("click", async function() {
    //get the innertext of class text in class paper 1
    var text = document.querySelector('.paper-1 .text').innerText;
    res = await extract_info({context: text})
    document.querySelector('.paper-2 .text').innerHTML=""
    document.querySelector('.paper-2 .text').innerHTML+="<h2>Overview:</h2>"
    document.querySelector('.paper-2 .text').innerHTML+="<p>"+res+"</p>"

    var extract_bias = document.querySelector('.extraction-bias').value
    console.log(extract_bias)
    res= await biased_extract({context: text, bias: extract_bias})
    document.querySelector('.paper-2 .text').innerHTML+="<h3>"+extract_bias+":</h3>"
    document.querySelector('.paper-2 .text').innerHTML+="<p>"+res+"</p>"
    // get the value of the input with class "submit-bias"
    var bias = document.querySelector('.submit-bias').value;
    console.log(bias);
    res = await guide_message({guidance: bias,chat_log: ["User 1: "+text],current_user:"User 2:"})
    document.querySelector('.paper-1 .text').innerText+="\n\n"+res
});