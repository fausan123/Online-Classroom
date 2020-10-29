document.addEventListener('DOMContentLoaded', () => {

    var sub_id = Number(location.pathname.split('/subject/')[1]);

    var fac_btn = document.getElementById('facbtn');
    var std_btn = document.getElementById('stdbtn');
    var fac_div = document.querySelector('.faculties');
    var std_div = document.querySelector('.students');

    fac_btn.onclick = () => {
        if (fac_div.style.display == 'none') {
            fac_div.style.display = 'block';
            document.querySelector('#facbtn img').src = '/media/expandless.svg';
        } else {
            fac_div.style.display = 'none'
            document.querySelector('#facbtn img').src = '/media/expandmore.svg';
        }
    }

    std_btn.onclick = () => {
        if (std_div.style.display == 'none') {
            std_div.style.display = 'block';
            document.querySelector('#stdbtn img').src = '/media/expandless.svg';
        } else {
            std_div.style.display = 'none'
            document.querySelector('#stdbtn img').src = '/media/expandmore.svg';
        }
    }

    // GET request to fetch all posts related to subject
    fetch(`/subject/${sub_id}/posts`)
        .then(response => response.json())
        .then(posts => {
            posts.forEach((post) => {
                var post_id = post.id;
                var username = document.getElementById('userName').value;
                var com_submit = document.getElementById(`${post_id}postcomsubmit`);
                var com_link = document.getElementById(`${post_id}postcomlink`);
                var comments = document.getElementById(`${post_id}postcomments`);

                com_submit.onclick = () => {
                    var com_input = document.getElementById(`${post_id}postcominput`).value;

                    // POST request to post comments
                    fetch(`/posts/${post_id}`, {
                        'method': 'POST',
                        'body': JSON.stringify({
                            content: com_input
                        })
                    })
                        .then(response => response.json())
                        .then(result => {
                            console.log(result)
                            if (result.status == 201) {
                                document.getElementById(`${post_id}postcominput`).value = '';
                                var postdiv = document.createElement('div');
                                postdiv.className = 'post';
                                postdiv.innerHTML = `<strong>${username} :</strong> ${com_input}`;
                                comments.prepend(postdiv);

                                if (comments.style.display == 'none') {
                                    show_comments(post_id);
                                }
                            }
                        })
                    return false;
                };

                com_link.onclick = () => {
                    show_comments(post_id);
                }
            })
        })
})

// Function to show comments
function show_comments(post_id) {
    var comments = document.getElementById(`${post_id}postcomments`);
    var com_link = document.getElementById(`${post_id}postcomlink`);

    console.log(comments);
    if (comments.style.display == 'none') {
        comments.style.display = 'block';
        com_link.innerHTML = 'Hide all comments'
    } else {
        comments.style.display = 'none';
        com_link.innerHTML = 'Click here to view all comments'
    }
}