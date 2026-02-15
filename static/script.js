document.getElementById('addForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const data = {
        subject: document.getElementById('subject').value,
        time: document.getElementById('time').value,
        day: document.getElementById('day').value,
        room: document.getElementById('room').value,
        instructor: document.getElementById('instructor').value
    };
    fetch('/api/classes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(response => response.json()).then(() => {
        alert('Class added!');
        loadClasses();
        document.getElementById('addForm').reset();
    });
});

function loadClasses() {
    const day = document.getElementById('filterDay').value;
    fetch(`/api/classes?day=${day}`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#classesTable tbody');
            tbody.innerHTML = '';
            data.forEach(cls => {
                const row = `<tr>
                    <td>${cls.id}</td>
                    <td>${cls.subject}</td>
                    <td>${cls.time}</td>
                    <td>${cls.day}</td>
                    <td>${cls.room}</td>
                    <td>${cls.instructor}</td>
                    <td>
                        <button class="btn btn-warning btn-sm" onclick="editClass(${cls.id})">Edit</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteClass(${cls.id})">Delete</button>
                    </td>
                </tr>`;
                tbody.innerHTML += row;
            });
        });
}

function editClass(id) {
    fetch(`/api/classes?day=`)
        .then(response => response.json())
        .then(data => {
            const cls = data.find(c => c.id === id);
            if (cls) {
                document.getElementById('updateId').value = cls.id;
                document.getElementById('updateSubject').value = cls.subject;
                document.getElementById('updateTime').value = cls.time;
                document.getElementById('updateDay').value = cls.day;
                document.getElementById('updateRoom').value = cls.room;
                document.getElementById('updateInstructor').value = cls.instructor;
                new bootstrap.Modal(document.getElementById('updateModal')).show();
            }
        });
}

document.getElementById('updateForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const id = document.getElementById('updateId').value;
    const data = {
        subject: document.getElementById('updateSubject').value,
        time: document.getElementById('updateTime').value,
        day: document.getElementById('updateDay').value,
        room: document.getElementById('updateRoom').value,
        instructor: document.getElementById('updateInstructor').value
    };
    fetch(`/api/classes/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(response => response.json()).then(() => {
        alert('Class updated!');
        loadClasses();
        bootstrap.Modal.getInstance(document.getElementById('updateModal')).hide();
    });
});

function deleteClass(id) {
    if (confirm('Are you sure?')) {
        fetch(`/api/classes/${id}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(() => {
                alert('Class deleted!');
                loadClasses();
            });
    }
}

// Load classes on page load
loadClasses();