window.addEventListener("DOMContentLoaded", (event) => {
    var input = document.getElementById('task_input');
    const add_button = document.getElementById('i_add');
    const el = document.querySelector('button.add_task_button')

    input.addEventListener('input', function() {
        var newValue = input.value;
        if (newValue.length){
            add_button.className = 'active_button';
            el.setAttribute('type', 'submit')
        } else{
            add_button.className = 'add_task_button';
            el.setAttribute('type', 'button')
        }
    });
});