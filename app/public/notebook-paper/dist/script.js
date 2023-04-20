text_log=[]


// function that given a value between 0 and 1 returns a circular div between red and green
function getColor(value) {
    //make sure the value is between 0 and 1
    value*=2
    if (value > 1) {
        value = 1;
    }

    var hue = ((1 - value) * 120).toString(10);
    color = ["hsl(", hue, ",100%,40%)"].join("");
    //create a div with the color
    var div = document.createElement('div');
    div.style.backgroundColor = color;

    //get a width between 0 and 500 inversely proportional to the value
    var width = (1-value)*300
    //subtract 200 from the width, and check to make sure it is not negative
    if(width<50){
        width=50
    }
    div.style.width = width+"px";
    div.style.height = "20px";
    div.style.borderRadius = "5px";
    return div;
}
// on click button with class "submit-button" run function
document.querySelector(".submit-button").addEventListener("click", async function() {
    
    var text = document.querySelector('.paper-1 .text').innerText;

    text_log.push(text)

    //find the difference between the last and second last text if it exists
    if(text_log.length>1){
        var last_text = text_log[text_log.length-1]
    } else {
        var last_text = text_log[0]
    }

    user_end_bias =  await end_classification({chat_history: [last_text]})
    sentiment_div=getColor(user_end_bias)
    document.querySelector('.paper-1 .text').appendChild(sentiment_div)

        
    res = await extract_info({context: text})
    document.querySelector('.paper-2 .text').innerHTML=""
    document.querySelector('.paper-2 .text').innerHTML+="<h2>Overview:</h2>"
    document.querySelector('.paper-2 .text').innerHTML+="<p>"+res+"</p>"

    var extract_bias = document.querySelector('.extraction-bias').value
    console.log(extract_bias)
    res= await biased_extract({context: text, bias: extract_bias})
    document.querySelector('.paper-2 .text').innerHTML+="<h3>"+extract_bias+":</h3>"
    document.querySelector('.paper-2 .text').innerHTML+="<p>"+res+"</p>"


    var slider_value = document.querySelector('.switch input').checked
    if(slider_value||user_end_bias>0.5){
        //uses the guided message khi function to get the user response from the server
        res = await end_message({context: text})
        document.querySelector('.paper-1 .text').innerHTML+="\n\n"+res
    }else{
        //uses the guided message khi function to get the user response from the server
        res = await guided_message_khi({context: text,user_data:res,KHI:extract_bias})
        document.querySelector('.paper-1 .text').innerHTML+="\n\n"+res
    }

    
    msg_cache=res
    res =  await end_classification({chat_history: [msg_cache]})
    console.log("bot termination bias: "+res)

    sentiment_div=getColor(res)
    document.querySelector('.paper-1 .text').appendChild(sentiment_div)
    document.querySelector('.paper-1 .text').innerHTML+="<br>"
    
    res= await health_analysis({context: text})
    document.querySelector('.paper-2 .text').innerHTML+="<h3>Sensitive data:</h3>"
    document.querySelector('.paper-2 .text').innerHTML+="<p>"+res+"</p>"

});