const STORAGE_KEY = 'todo_app_tasks';
const form = document.getElementById('todo-form');
const input = document.getElementById('todo-input');
const list = document.getElementById('todo-list');
const taskCount = document.getElementById('task-count');
const emptyState = document.getElementById('empty-state');
const clearCompleted = document.getElementById('clear-completed');
let todos = [];

try {
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    if (Array.isArray(stored)) {
        todos = stored.filter(task => task && typeof task.text === 'string');
    }
} catch (error) {
    todos = [];
}

function saveTodos() {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
    } catch (error) {
        console.error('Could not save tasks:', error);
    }
}

function renderTodos() {
    list.replaceChildren();

    todos.forEach(todo => {
        const item = document.createElement('li');
        item.className = 'todo-item' + (todo.done ? ' completed' : '');

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = Boolean(todo.done);
        checkbox.setAttribute('aria-label', 'Mark ' + todo.text + ' as completed');
        checkbox.addEventListener('change', () => {
            todo.done = checkbox.checked;
            saveTodos();
            renderTodos();
        });

        const text = document.createElement('span');
        text.className = 'todo-text';
        text.textContent = todo.text;

        const removeButton = document.createElement('button');
        removeButton.className = 'delete-btn';
        removeButton.type = 'button';
        removeButton.textContent = 'Delete';
        removeButton.setAttribute('aria-label', 'Delete ' + todo.text);
        removeButton.addEventListener('click', () => {
            todos = todos.filter(item => item.id !== todo.id);
            saveTodos();
            renderTodos();
        });

        item.append(checkbox, text, removeButton);
        list.appendChild(item);
    });

    const remaining = todos.filter(todo => !todo.done).length;
    taskCount.textContent = `${remaining} ${remaining === 1 ? 'task' : 'tasks'} remaining`;
    emptyState.hidden = todos.length > 0;
    clearCompleted.disabled = !todos.some(todo => todo.done);
}

form.addEventListener('submit', event => {
    event.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    todos.push({
        id: `${Date.now()}-${Math.random().toString(36).slice(2)}`,
        text,
        done: false
    });
    input.value = '';
    saveTodos();
    renderTodos();
    input.focus();
});

clearCompleted.addEventListener('click', () => {
    todos = todos.filter(todo => !todo.done);
    saveTodos();
    renderTodos();
});

renderTodos();
