const chatForm = document.getElementById('chat-form');
const chatMessages = document.querySelector('.card-body');
const socket = io();
const user = prompt('What is your name?');

socket.on('message', message =>{
  outputMessage(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
});

chatForm.addEventListener('submit', (e) =>{
  e.preventDefault();

  const msg = e.target.elements.msg.value;

  socket.emit('chatMessage', [user, msg]);

  e.target.elements.msg.value = '';
  e.target.elements.msg.focus();
});

function outputMessage(message){
  const div = document.createElement('div');
  div.classList.add('message');
  div.innerHTML = `<p class ="meta">${message.info[0]}<span class="time"> ${message.time}</span></p>
  <p class="text">
  ${message.info[1]}
  </p>`;
  document.querySelector('.chat-messages').appendChild(div);
}