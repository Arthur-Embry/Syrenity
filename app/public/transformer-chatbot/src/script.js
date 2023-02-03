function removeClones(str) {
  try{
    for(i = 0; i< str.length-15; i++){
        sub = str.substring(i,i+15)
        let regex = new RegExp(`${sub}`, "g");
        count = (str.match(regex) || []).length;
        if(count>3){
            presplit=str.split(sub)[0]+sub+str.split(sub)[1]
            if(presplit.includes(".")){
                res=presplit.split(".").slice(0,-1).join(".")+"."
            } else if(presplit.includes("?")){
                res=presplit.split("?").slice(0,-1).join("?")+"?"
            } else if(presplit.includes("!")){
                res=presplit.split("!").slice(0,-1).join("!")+"!"
            } else {
                res=presplit
            }
            return res;
        }
    }    
  } catch(e){
    return "";
  }

    return "";
}
const delay = (ms) => new Promise(res => setTimeout(res, ms));	
async function link_query(subject, url) {
	while(document.querySelectorAll('[name="search"]').length==0||document.querySelectorAll(".gsc-search-button.gsc-search-button-v2").length==0){
		await delay(50);
	}
	search_in=document.querySelector('[name="search"]')
	execute_search=document.querySelector(".gsc-search-button.gsc-search-button-v2")
	//console.log(search_in)
	//console.log(execute_search)
	search_in.value=subject+" site:"+url
	execute_search.click()
	while(document.querySelectorAll('.gsc-resultsRoot.gsc-tabData.gsc-tabdActive').length==0){
		await delay(50);
	}
	search_res=document.querySelector('.gsc-resultsRoot.gsc-tabData.gsc-tabdActive')
	while(search_res.querySelectorAll('a').length==0){
		await delay(50);
	}
	anchors=search_res.querySelectorAll('a')
	//console.log(anchors)
	links=[]
	anchors.forEach(a=>{
		if(!a.href.includes("code.google")){
			console.log(a.href)
			links.push(a.href)
		}
	})
	//console.log(links)
	return links
	
};

//console.log(link_query("telehealth","https://syrahealth.com/"));



document.querySelectorAll("fieldset input, fieldset textarea").forEach((el)=>{
  console.log(el)
  el.addEventListener('change',function(){
    console.log(el.value)
  });
})

function expand(state){
if(state==0){
  document.querySelector(".r-nav").style.visibility="hidden"
  document.querySelector(".chat").style.width="45px"
  document.querySelector(".chat").style.height="45px"
} else if (state==1){
  document.querySelector(".r-nav").style.visibility="visible"
  document.querySelector(".chat").style.width="400px"
  document.querySelector(".chat").style.height="165px"
} else if (state==2){
  document.querySelector(".r-nav").style.visibility="visible"
  document.querySelector(".chat").style.width="400px"
  document.querySelector(".chat").style.height="60vh"
}
}
expand(2);
expansion_state=0
document.querySelector(".chat-title .avatar img").onclick=function(){
  expansion_state+=1
  expansion_state%=3
  expand(expansion_state)
}
document.querySelector(".r-nav li a").onclick=function(){
  expansion_state=0
  expand(expansion_state)
}

var msg_log = ['Person 1:','MHSIndiana at your service, how may we help you?']

async function query(data) {
	const response = await fetch(
		"https://api-inference.huggingface.co/models/bigscience/bloom",
		{
			headers: { Authorization: "Bearer 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" },
			method: "POST",
			body: JSON.stringify(data),
		}
	);
	const result = await response.json();
  console.log(result[0].generated_text)
	return result;
}
async function classify(data) {
    const response = await fetch(
        "https://api-inference.huggingface.co/models/facebook/bart-large-mnli",
        {
            headers: { Authorization: `Bearer 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` },
            method: "POST",
            body: JSON.stringify(data),
        }
    );
    const result = await response.json();
    return result;
}

var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    botMessage(msg_log[1]);
  }, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

async function insertMessage() {
  msg = $('.message-input').val();

  msg_log.push("Person 2:")
  msg_log.push(msg)
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  await new Promise(resolve => setTimeout(resolve, 1000 + (Math.random() * 20) * 100));
  stem="The following is a good example of a chat between two people. \nperson 1 is friendly, helpfull, and kind\n"
  for(i=0;i<msg_log.length;i++){
    stem+=msg_log[i]+"\n"
  }
  res = await query({"inputs": stem});
  out=res[0].generated_text.split(stem)[1]
  stem+=out;
  temp_chain=out
  while(!out.includes("Person 2:")){
    res = await query({"inputs": stem});
    out=res[0].generated_text.split(stem)[1]
    //console.log(removeClones(out));
    
    stem+=out;
    temp_chain+=out
    rc=removeClones(temp_chain)
    if(rc!=""){
      temp_chain=rc+"Person 2:";
      out+="Person 2:"
    }
    console.log(174,temp_chain)
  }
  console.log(temp_chain)
  console.log(out)
  out=temp_chain
  out=out.split("Person 1:")[1].split("Person 2:")[0]
  console.log(out)

  msg_log.push("Person 1:")
  msg_log.push(out)
  console.log(msg_log)
  
  botMessage(out);
  stem=""
  for(i=0;i<msg_log.length;i++){
    stem+=msg_log[i]+"\n"
  }
  
  link_state = await classify({inputs: out.trim(), parameters: {candidate_labels: ["medical", "control"]}})
  
 
 
  if(link_state.labels[0]=="medical"){
    stem="Prompt:\""+out+"\"\n\nSearch word:\""
      res = await query({"inputs": stem});
    word=res[0].generated_text.split(stem)[1].split("\"")[0]
  console.log(res[0].generated_text.split(stem)[1].split("\"")[0])
    links = await link_query("telehealth","https://www.mhsindiana.com/")
    await delay(500);
    try{
      msg_log.push("Person 1:")
      msg_log.push(`<a href="`+links[0]+`" target="_blank">${links[0]}</a>`)
      botMessage(`<a href="`+links[0]+`" target="_blank">${links[0]}</a>`);
    } catch (e){console.log(e)}
    
  }
    
  
  
  
}

$('.message-submit').click(function() {
  insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})


function botMessage(msg) {
  //i+=n
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="https://i.ibb.co/6mb7j1K/output-onlinepngtools.jpg" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();
  setTimeout(function() {
    $('.message.loading').remove();
    $('<div class="message new"><figure class="avatar"><img src="https://i.ibb.co/6mb7j1K/output-onlinepngtools.jpg" /></figure>' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
    //i++;
  }, 1000 + (Math.random() * 20) * 100);

}
