document.addEventListener('DOMContentLoaded', () => {

    fetch('/getnotes/')
        .then(response => response.json())
        .then(notes => {
            notes.forEach((note) => {
                var note_id = note.id;
                var starred = note.starred;
                var star_btn = document.getElementById(`${note_id}notestarbtn`);
                var delete_btn = document.getElementById(`${note_id}notedeletebtn`);
                var notediv = document.getElementById(`${note_id}notediv`);


                star_btn.addEventListener('click', () => {

                    if (starred) {
                        starred = false;
                    } else {
                        starred = true;
                    }

                    fetch(`/notes/${note_id}`, {
                        'method': 'PUT',
                        'body': JSON.stringify({
                            'star': starred
                        })
                    })

                    if (starred) {
                        notediv.style.backgroundColor = "rgb(253, 253, 135)";
                        star_btn.value = "Unstar";
                        star_btn.className = "btn btn-danger";
                    } else {
                        notediv.style.backgroundColor = "#fff";
                        star_btn.value = "Star";
                        star_btn.className = "btn btn-warning";
                    }

                    return false;
                })

                delete_btn.addEventListener('click', () => {

                    fetch(`/notes/${note_id}`, {
                        'method': 'PUT',
                        'body': JSON.stringify({
                            'delete': true
                        })
                    })

                    notediv.remove();

                    return false
                })
            })
        })
})
