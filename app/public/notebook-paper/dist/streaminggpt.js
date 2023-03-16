fetch("/openapi.json")
  .then((response) => response.json())
  .then((data) => {
  for (const endpoint in data.paths) {
     if(data.paths[endpoint].hasOwnProperty('post')){
        window[endpoint.substring(1)] = async function(body) {
        res = await autocomplete_stream(body,endpoint.substring(1))
        const reader = res.getReader();
        let result;
        output=""
        while (!(result = await reader.read()).done) {
          output+= new TextDecoder().decode(result.value)
        }
        return output;
      };
     }
  }

});
  


//streaming driver function (posted endpoints)
async function autocomplete_stream(body_test,endpoint){
  //add any undefined global_ var values if not explicitly defined
    Object.keys(window).forEach(function(name) {
    if (name.startsWith("global_")) {
      if(body_test[name.substring(7)]==undefined){
        body_test[name.substring(7)] = window[name]; 
      }
    }
  });
  //post to the endpoint
 res= await fetch("/"+endpoint, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(body_test) // body data type must match "Content-Type" header
  })
        contents=":"
        const reader = res.body.getReader();
        return new ReadableStream({
            start(controller) {
                return pump();
                function pump() {
                    return reader.read().then(({ done, value }) => {
                      var string = new TextDecoder().decode(value)
                      //console.log(string)
                        // When no more data needs to be consumed, close the stream
                        if (done) {
                            controller.close();
                            return ;
                        }
                        // Enqueue the next data chunk into our target stream
                        controller.enqueue(value);
                        return pump();
                    });
                }
            }
        });
}

