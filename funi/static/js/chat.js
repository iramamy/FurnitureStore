// Large scree activation

document.getElementById('chatToggleIcon').addEventListener('click', function (e) {
	e.preventDefault();
	const chat = document.getElementById('chat');
	chat.style.display = chat.style.display === 'none' || chat.style.display === '' ? 'block' : 'none';
  });

document.getElementById('closeChat').addEventListener('click', function (e) {
	e.preventDefault();
	console.log('Clicked');
	document.getElementById('chat').style.display = 'none';
  });

