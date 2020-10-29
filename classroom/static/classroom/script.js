document.addEventListener('DOMContentLoaded', () => {
    var modal = document.getElementById('sub_modal');
    var sub_btn = document.querySelector('.sub-btn');
    var course_btn = document.getElementById('course_btn');
    var course_modal = document.getElementById('course_modal');
    var createclose = document.getElementById('createclose');
    var joinclose = document.getElementById('joinclose');


    if (sub_btn != null) {
        sub_btn.onclick = () => {
            modal.style.display = 'block';
        }
    }

    if (course_btn != null) {
        course_btn.onclick = () => {
            course_modal.style.display = 'block';
        }
    }

    if (createclose != null) {
        createclose.onclick = () => {
            modal.style.display = 'none';
        }
    }

    if (joinclose != null) {
        joinclose.onclick = () => {
            course_modal.style.display = 'none';
        }
    }

    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
        else if (event.target == course_modal) {
            course_modal.style.display = 'none';
        }
    }

    document.querySelectorAll('.subs').forEach((div) => {
        div.onclick = () => {
            var id = div.dataset.subid;
            var origin = location.origin;
            location.assign(`${origin}/subject/${id}`);
        }
    })

    document.querySelectorAll('.assign').forEach((div) => {
        div.onclick = () => {
            var id = div.dataset.assignid;
            var origin = location.origin;
            location.assign(`${origin}/assignments/${id}`);
        }
    })
})


function resNavbar() {
    var x = document.querySelector('nav');
    var icon = document.querySelector('.icon');
    var i = document.createElement('i')
    if (x.className == "") {
        x.className = "responsive";
        icon.children[0].remove();
        i.className = "fa fa-times";
        icon.append(i);
    } else {
        x.className = "";
        icon.children[0].remove();
        i.className = "fa fa-bars";
        icon.append(i);
    }
}