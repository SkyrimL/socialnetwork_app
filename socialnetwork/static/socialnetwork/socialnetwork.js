
// Sends a new request to update the to-do list
function getList() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("GET", "socialnetwork/get-global", true)
    xhr.send()
}


function getList2() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("GET", "socialnetwork/get-follower", true)
    xhr.send()
}

function updatePage(xhr) {
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        updateList(response)
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function updateList(items) {
    // Removes the old to-do list items
    let list = document.getElementById("my-posts-go-here")

    // Adds each new todo-list item to the list
    for (let i = 0; i < items.length; i++) {
        
        let item = items[i]


        if (document.getElementById("id_post_profile_" + item.id) === null) {

            let stream= "<div id='id_post_div_"+item.id+"\' class=topheader>Post by"+ 
            "<a href=\"/otherProfile/" +item.user_id+ "\" id=\"id_post_profile_"+item.id+"\" >"+item.first_name+" "+ item.last_name+ "</a>"+ 
            "<span id=\"id_post_text_"+item.id+"\">"+sanitize(item.post_text)+"</span> " +
            "<span id=\"id_post_date_time_"+item.id+"\" class='span'>"+item.post_time+"</span>"+
        "</div>"+



        "<from>"+
            "<label for=\"id_comment_input_text_"+
            item.id+
            "\">Comment:</label>"+
            "<input id=\"id_comment_input_text_"+
            item.id+
            "\">"+
            "<button id=\"id_comment_button_"+
            item.id+"\"onclick=addComment("+item.id+")"+
            " >Submit</button>"+
        "</from>"
            let element = document.createElement("li")
            element.innerHTML = stream

            // Adds the todo-list item to the HTML list
            list.prepend(element)
        }

        let list1 = document.getElementById("id_post_div_"+item.id)

        
        for (let j = item.comments.length-1; j>=0; j--) {

            let item1 = item.comments[j]



            if (document.getElementById("id_comment_profile_" + item1.id) === null) {
               
                let stream1 = "<div id='id_comment_div_"+item1.id+"\' class=comment1>comment by"+ 
        "<a href=\"/otherProfile/" +item1.id+ "\" id=\"id_comment_profile_"+item1.id+"\" >"+item1.first_name+" "+ item1.last_name+ "</a>"+ 
        "<span id=\"id_comment_text_"+item1.id+"\">"+sanitize(item1.comment_text)+"</span> " +
        "<span id=\"id_comment_date_time_"+item1.id+"\" class='span'>"+item1.comment_time+"</span>"+
        "</div>"


                let element1 = document.createElement("li")

                element1.innerHTML = stream1 

                list1.append(element1)       

            }

        }

    }
}






function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}


function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}



function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function addComment(post_id) {

    let itemTextElement = document.getElementById("id_comment_input_text_" + post_id)
    let itemTextValue   = itemTextElement.value
    // Clear input box and old error message (if any)
    itemTextElement.value = ''
    

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }



    xhr.open("POST", "socialnetwork/add-comment", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("post_id="+post_id+"&comment_text="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());
}
