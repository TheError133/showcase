//localStorage.clear()

// Внесение информации по товарам на страницу пользователя.
if (document.querySelectorAll('.user-detail-page').length > 0) {
  let cartDiv = document.querySelector('.user-cart');
  let userId = user_id.textContent;
  let currentStorageValue = localStorage.getItem('cart');
  let cartProducts;

  if (currentStorageValue == null) {
    cartProducts = null;
  } else {
    cartProducts = JSON.parse(currentStorageValue);
  }

  if (cartProducts != null) { // В корзине есть товары.
    let currentUserCart = cartProducts.find(a => a.userId === userId); // Получаем корзину текущего пользователя.

    if (currentUserCart !== undefined && currentUserCart.products.length > 0) { // Корзина текущего пользователя существует и в ней есть товары.
      let table = document.createElement('table');
      table.className = 'cart-table';
      
      // Заголовок таблицы.
      let thead = document.createElement('thead');
      let thName = document.createElement('th');
      thName.textContent = 'Наименование';
      thead.appendChild(thName);
      let thCount = document.createElement('th');
      thCount.textContent = 'Кол-во';
      thCount.setAttribute('colspan', 3);
      thead.appendChild(thCount);
      let thPrice = document.createElement('th');
      thPrice.textContent = 'Стоимость';
      thead.appendChild(thPrice);
      table.appendChild(thead);
      
      // Основное тело таблицы.
      let tbody = document.createElement('tbody');
      let totalCostValue = 0.0;

      currentUserCart.products.forEach(element => {
        let tr = document.createElement('tr');
        let tdName = document.createElement('td');
        tdName.textContent = element.name;
        tdName.id = 'user-cart-product';
        tr.appendChild(tdName);
        let tdMinus = document.createElement('td');
        let tdPlus = document.createElement('td');
        tdMinus.textContent = '-';
        tdMinus.id = 'count-decrease'
        tdPlus.textContent = '+';
        tdPlus.id = 'count-increase'
        let tdCount = document.createElement('td');
        tdCount.textContent = element.count;
        tdCount.id = 'count-value';
        tr.appendChild(tdMinus);
        tr.appendChild(tdCount);
        tr.appendChild(tdPlus);
        let tdCost = document.createElement('td');
        tdCost.textContent = element.cost;
        tdCost.id = 'user-cart-cost';
        tr.appendChild(tdCost);
        totalCostValue += parseFloat(tdCost.textContent);
        tbody.appendChild(tr);
      });

      // Итого.
      let totalRow = document.createElement('tr');
      let totalName = document.createElement('td');
      totalName.textContent = 'ИТОГО';
      totalName.id = 'total-name';
      totalRow.appendChild(totalName);
      let totalCost = document.createElement('td');
      totalCost.textContent = totalCostValue;
      totalCost.id = 'total-cost-value';
      totalCost.setAttribute('colspan', 4);
      totalRow.appendChild(totalCost);
      tbody.appendChild(totalRow);
      table.appendChild(tbody);

      // Добавление таблицы на страницу.
      cartDiv.appendChild(table);
    } else { // Если корзина пуста.
      let emptyMessage = document.createElement('span');
      emptyMessage.textContent = 'Корзина пуста'
      cartDiv.appendChild(emptyMessage);
    }
  } else { // Если корзины не существует.
    let emptyMessage = document.createElement('span');
    emptyMessage.textContent = 'Корзина пуста'
    cartDiv.appendChild(emptyMessage);
  }
}

// Отображение информации во всплывающем окне.
function showPopUp(messageText, borderColor='black') {
  let message = document.createElement('span');
  message.className = 'pop-up';
  message.textContent = messageText;
  message.style.cssText = `border: 2px solid ${borderColor}`;
  document.body.appendChild(message);
  let animation = message.animate(
    [
      {
        top: '0',
        opacity: '0'
      },
      {
        top: '30px',
        opacity: '100%'
      },
      {
        top: '30px',
        opacity: '100%'
      },
      {
        top: '0',
        opacity: '0'
      },
     ],
    3000
  )
  animation.addEventListener('finish', function() {
    document.body.removeChild(message);
  })
}

// Добавление товара в корзину.
// На странице товаров.
let buttonAddToCart = document.querySelectorAll('#product-button-add');
buttonAddToCart.forEach(element => {
  element.addEventListener('click', event => {
    addToCart(event.target, 'products');
  })
});
// На странице пользователя.
let buttonIncreaseCount = document.querySelectorAll('#count-increase');
buttonIncreaseCount.forEach(element => {
  element.addEventListener('click', event => {
    addToCart(event.target, 'user-detail');
  })
});

function addToCart(element, mode) {
  let userId = user_id.textContent;
  let productName;
  let productPrice;
  let currentStorageValue = localStorage.getItem('cart');
  let cartProducts;

  if (currentStorageValue == null) {
    cartProducts = [];
  } else {
    cartProducts = JSON.parse(currentStorageValue);
  }

  switch (mode) {
    case 'products':
      productName = element.parentNode.querySelector('#product-name').textContent;
      productPrice = parseFloat(element.parentNode.querySelector('#product-price strong').textContent.split(' ')[0])
      break;
    case 'user-detail':
      productName = element.parentNode.querySelector('#user-cart-product').textContent;
      productPrice = parseFloat(element.parentNode.querySelector('#user-cart-cost').textContent)
        / parseFloat(element.parentNode.querySelector('#count-value').textContent);
      break;
    default:
      break;
  }

  let currentUserCart = cartProducts.find(a => a.userId === userId); // Сохраняем текущую корзину пользователя.
  if (currentUserCart === undefined) { // Корзины пользователя пока не существует.
    cartProducts.push(
    {
      userId: userId,
      products: [
        {
          name: productName,
          cost: productPrice,
          count: 1
        }
      ]
    }
    );
  } else { // Корзина пользователя существует.
    let currentUserCartProducts = currentUserCart.products; // Сохраняем текущие товары в корзине.

    if (currentUserCartProducts.map(a => a.name).includes(productName)) { // Находим указанный товар в корзине.
      currentUserCartProducts.find(a => a.name === productName).cost += productPrice;
      currentUserCartProducts.find(a => a.name === productName).count++;

      // Если мы на странице пользователя, то обновляем значения в таблице.
      if (mode == 'user-detail') {
        let currentCount = element.parentNode.querySelector('#count-value');
        let currentCost = element.parentNode.querySelector('#user-cart-cost');
        let totalCostValue = document.querySelector('#total-cost-value');
        const reducer = (accumulator, currentValue) => accumulator + currentValue;
        currentCount.textContent = parseInt(currentCount.textContent) + 1;
        currentCost.textContent = parseFloat(currentCost.textContent) + productPrice;
        totalCostValue.textContent = currentUserCartProducts.map(a => a.cost).reduce(reducer);
      }
    } else { // Не находим указанный товар в корзине.
      currentUserCartProducts.push(
        {
        name: productName,
        cost: productPrice,
        count: 1
        }
      )
    }
  }

  // Уведомление о добавленном товаре.
  if (mode == 'products') {
    showPopUp(`${productName} добавлен в корзину`)
  }

  localStorage.setItem('cart', JSON.stringify(cartProducts));
}

// Удаление товара из корзины.
// На странице товаров.
let buttonRemoveFromCart = document.querySelectorAll('#product-button-remove');
buttonRemoveFromCart.forEach(element => {
  element.addEventListener('click', event => {
    removeFromCart(event.target, 'products');
  })
})
// На странице пользователя.
let buttonDecreaseCount = document.querySelectorAll('#count-decrease');
buttonDecreaseCount.forEach(element => {
  element.addEventListener('click', event => {
    removeFromCart(event.target, 'user-detail');
  })
});

function removeFromCart(element, mode) {
  let userId = user_id.textContent;
  let productName;
  let productPrice;
  let currentStorageValue = localStorage.getItem('cart');
  let cartProducts;

  if (currentStorageValue == null) {
    cartProducts = null;
  } else {
    cartProducts = JSON.parse(currentStorageValue);
  }

  switch (mode) {
    case 'products':
      productName = element.parentNode.querySelector('#product-name').textContent;
      productPrice = parseFloat(element.parentNode.querySelector('#product-price strong').textContent.split(' ')[0])
      break;
    case 'user-detail':
      productName = element.parentNode.querySelector('#user-cart-product').textContent;
      productPrice = parseFloat(element.parentNode.querySelector('#user-cart-cost').textContent)
        / parseFloat(element.parentNode.querySelector('#count-value').textContent);
      break;
    default:
      break;
  }

  if (cartProducts != null) { // Корзина товаров не пуста.
    if (cartProducts.find(a => a.userId === userId) !== undefined) { // Корзина пользователя существует.
      let currentUserCartProducts = cartProducts.find(a => a.userId === userId).products; // Сохраняем текущие товары в корзине.
      
      if (currentUserCartProducts.map(a => a.name).includes(productName)) { // В корзине есть указанный товар.
        currentUserCartProducts.find(a => a.name === productName).cost -= productPrice;
        currentUserCartProducts.find(a => a.name === productName).count--;

        // Если мы на странице пользователя, то обновляем значения в таблице.
        if (mode == 'user-detail') {
          let currentCount = element.parentNode.querySelector('#count-value');
          let currentCost = element.parentNode.querySelector('#user-cart-cost');
          let totalCostValue = document.querySelector('#total-cost-value');
          const reducer = (accumulator, currentValue) => accumulator + currentValue;
          currentCount.textContent = parseInt(currentCount.textContent) - 1;
          currentCost.textContent = parseFloat(currentCost.textContent) - productPrice;
          totalCostValue.textContent = currentUserCartProducts.map(a => a.cost).reduce(reducer);
        }

        if (currentUserCartProducts.find(a => a.name === productName).count == 0) { // Удаляем товары, количество которых 0.
          cartProducts.find(a => a.userId === userId).products = currentUserCartProducts.filter(a => a.count != 0);

          // Если мы на странице пользователя, то удаляем строку с нулевыми данными.
          if (mode == 'user-detail') {
            let tableRow = element.parentNode;
            let tableBody = element.parentNode.parentNode;
            tableBody.removeChild(tableRow);

            // Если корзина пуста, то выводим соответствующее сообщение.
            if (document.querySelector('.cart-table tbody').children.length <= 1) {
              let cartDiv = document.querySelector('.user-cart');
              let table = document.querySelector('.cart-table');
              let emptyMessage = document.createElement('span');
              
              cartDiv.removeChild(table);
              emptyMessage.textContent = 'Корзина пуста'
              cartDiv.appendChild(emptyMessage);
            }
          }
        }
      }
    }
  }

  // Уведомление об удаленном товаре.
  if (mode == 'products') {
    showPopUp(`${productName} удален из корзины`, 'red')
  }

  localStorage.setItem('cart', JSON.stringify(cartProducts));
}