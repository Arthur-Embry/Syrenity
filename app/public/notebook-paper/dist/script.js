console.log("ping");
// on click button with class "submit-button" run function
document.querySelector(".submit-button").addEventListener("click", async function() {


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

    //uses the guided message khi function to get the user response from the server
    res = await guided_message_khi({context: text,user_data:res})
    document.querySelector('.paper-1 .text').innerText+="\n\n"+res

    res= await health_analysis({context: text})
    document.querySelector('.paper-2 .text').innerHTML+="<h3>Sensitive data:</h3>"
    document.querySelector('.paper-2 .text').innerHTML+="<p>"+res+"</p>"

});