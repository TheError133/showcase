// Добавление комментариев.
let addCommentButtons = document.querySelectorAll('#comment-add');
addCommentButtons.forEach(elem => {
    elem.addEventListener('click', evt => {
        popupFormShow(evt, 'comment');
    })
})

// Скрытие отображающейся формы добавления информации.
popupHide();

function popupFormShow(evt, mode) {
    // Отображение формы добавления информации.
    let textAreaBlock = document.querySelector('.popup-block');
	let textAreaForm = document.querySelector('#popup-form');
	let textArea = document.createElement('textarea');
	let submitButton = document.createElement('input');
	let closeButton = document.createElement('button');
	let textAreaName;
	let submitButtonValue;

	if (document.querySelectorAll('#popup-textarea').length < 1) {
	    // Если форма еще не выведена, то выводим ее.
	    textAreaBlock.hidden = false;
	    textAreaBlock.appendChild(textAreaForm);
	} else {
	    // Если форма уже выведена, то обновляем ее положение, удаляя потомков.
	    let tmpTextArea = document.querySelector('#popup-textarea');
	    let tmpInput = document.querySelector('#popup-submit');
	    let tmpCloseButton = document.querySelector('#popup-close');

	    textAreaBlock.removeAttribute('hidden'); // Для случая, если форма уже была скрыта.
	    textAreaForm.removeChild(tmpTextArea);
	    textAreaForm.removeChild(tmpInput);
	    textAreaForm.removeChild(tmpCloseButton);
	}

	switch(mode) {
        case 'comment':
            textAreaName = 'comment_string';
            submitButtonValue = 'Добавить комментарий';
            break;
        case 'rating':
            textAreaName = 'rating_value';
            submitButtonValue = 'Добавить оценку';
            break;
    }

	textAreaBlock.style.cssText = `top: ${evt.pageY - 30}px; left: ${evt.pageX}px; position: absolute;`;
	textArea.id = 'popup-textarea';
	textArea.name = textAreaName;
	submitButton.type = 'submit';
	submitButton.id = 'popup-submit';
	submitButton.value = submitButtonValue;
	closeButton.textContent = 'x';
	closeButton.id = 'popup-close';

	textAreaForm.appendChild(closeButton);
	textAreaForm.appendChild(textArea);
	textAreaForm.appendChild(submitButton);
}

function popupHide() {
    // Скрытие формы добавления информации.
    document.addEventListener('click', evt => {
        let popupCloseButton = document.querySelector('#popup-close');
        let clickTarget = evt.target;

        if (popupCloseButton === clickTarget) {
            evt.preventDefault();
            document.querySelector('.popup-block').hidden = true;
        }
    })
}