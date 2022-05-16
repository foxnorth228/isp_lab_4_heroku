const filterTags = document.getElementById("butt_add_tags");
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
filterTags.addEventListener("click", function(){
    const elFilt = document.getElementById("input_add_tags");
    let tag = elFilt.value;
    const url = document.location.origin;
    fetch(`${url}/blog/tag/create`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body: JSON.stringify({'message': tag}),
    })
    .then((res) => res.json())
    .then((data) => { 
        console.log(data); 
        elFilt.value = ""; 
        let option = document.createElement("option");
        option.text = data['message'];
        if(data['message'] !== null)
            document.getElementById("id_tags").add(option);
    })
    .catch((err) => { console.log(err); })
    console.log(url);
});

const form = document.getElementById("post_editing");
form.addEventListener("submit", function(e) {
    e.preventDefault();
    e.stopPropagation();
    const title = form.querySelector("#id_title");
    const text = form.querySelector("#id_text");
    const tags = form.querySelector("#id_tags");
    let arrTags = [];
    for(let el of tags.options) {
        if (el.selected) {
            arrTags.push(el.innerHTML);
        }
    }
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body: JSON.stringify({
            'title': title.value,
            'text': text.value,
            'tags': arrTags,
        }),
    })
    .then(data => {
        window.location.href = data['url'];
    })
    .catch((err) => { console.log(err); })
    return false;
})