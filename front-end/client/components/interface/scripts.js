/*
  --------------------------------------------------------------------------------------
  Função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/

const getList = async () => {
    let url = 'http://127.0.0.1:5000/produtos'
    fetch(url, {
        method: 'get',
    })
        .then((res) => res.json())
        .then((data) => {
            data.produtos.forEach(item => insertList(item.nome, item.categoria, item.quantidade, item.valor))
        })
        .catch((error) => {
            console.error('Error:', error)
        })

}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/

getList()

/*
--------------------------------------------------------------------------------------
Função para adicionar um novo item com nome, categoria, quantidade e valor 
--------------------------------------------------------------------------------------
*/

const newItem = () => {
  let inputProduct = document.getElementById("newProduct").value;
  let inputCategory = document.getElementById("newCategory").value;
  let inputQuantity = document.getElementById("newQuantity").value;
  let inputPrice = document.getElementById("newPrice").value;

  if (inputProduct === '') {
      alert("Escreva o nome de um item!");
  } else if (isNaN(inputQuantity) || isNaN(inputPrice)) {
      alert("Quantidade e valor precisam ser números!");
  } else {
      insertList(inputProduct, inputCategory, inputQuantity, inputPrice)
      postItem(inputProduct, inputCategory, inputQuantity, inputPrice)
      alert("Item adicionado!")
  }
}

/*
--------------------------------------------------------------------------------------
Função para colocar um item na lista do servidor via requisição POST
--------------------------------------------------------------------------------------
*/

const postItem = async (inputProduct, inputCategory, inputQuantity, inputPrice) => {
    const formData = new FormData();
    formData.append('nome', inputProduct);
    formData.append('categoria', inputCategory);
    formData.append('quantidade', inputQuantity);
    formData.append('valor', inputPrice);

    let url = 'http://127.0.0.1:5000/produto'
    fetch(url, {
        method: 'post',
        body: formData
    })
    .then((res) => res.json())
    .catch((error) => {
        console.error('Error:', error)
    })
}

/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/

const insertButton = (parent) => {
    let span = document.createElement("span");
    let txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    parent.appendChild(span);
}

/*
--------------------------------------------------------------------------------------
Função para remover um item da lista com um click no botão close
--------------------------------------------------------------------------------------
*/

const removeElement = () => {
    let close = document.getElementsByClassName("close");
    let i;
    for (i = 0; i < close.length; i++) {
        close[i].onclick = function () {
            let div = this.parentElement.parentElement;
            const nomeItem = div.getElementsByTagName('td')[0].innerHTML
            if (confirm("Você tem certeza?")) {
                div.remove()
                deleteItem(nomeItem)
                alert("Removido!")
            }
        }
    }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/

const deleteItem = (item) => {
    console.log(item)
    let url = 'http://127.0.0.1:5000/produto?nome=' + item;
    fetch(url, {
      method: 'delete'
    })
      .then((res) => res.json())
      .catch((error) => {
        console.error('Error:', error);
      });
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/

const insertList = (nameProduct, category, quantity, price) => {
    var item = [nameProduct, category, quantity, price]
    var table = document.getElementById('myTable');
    var row = table.insertRow();
  
    for (var i = 0; i < item.length; i++) {
      var cel = row.insertCell(i);
      cel.textContent = item[i];
    }
    insertButton(row.insertCell(-1))
    document.getElementById("newProduct").value = "";
    document.getElementById("newCategory").value = "";
    document.getElementById("newQuantity").value = "";
    document.getElementById("newPrice").value = "";
  
    removeElement()
}

/*
  --------------------------------------------------------------------------------------
  Função para buscar produtos por categoria
  --------------------------------------------------------------------------------------
*/
const buscarCategoria = () => {
    var busca_categoria = document.getElementById('buscaCategoria').value

    let url = `http://127.0.0.1:5000/buscar_produto_categoria?categoria=${busca_categoria}`

    fetch(url, {
        method: 'get',
    })
        .then((res) => res.json())
        .then((data) => {
          // Obter a referência para a tabela e seu corpo
          const resultadoTable = document.getElementById('resultado');
          const resultadoBody = resultadoTable.getElementsByTagName('tbody')[0];
          
          resultadoBody.innerHTML = ''; // Limpar resultados anteriores
  
          if (data.produtos.length === 0) {
            resultadoTable.classList.add('hidden'); // Esconder a tabela se não houver resultados
            return;
          }

          resultadoTable.classList.remove('hidden');
  
          // Criar uma linha para cada produto e adicionar ao corpo da tabela
          data.produtos.forEach((produto) => {
              const row = document.createElement('tr');
              row.appendChild(criarCelula(produto.nome));
              row.appendChild(criarCelula(produto.categoria));
              row.appendChild(criarCelula(produto.quantidade));
              row.appendChild(criarCelula(produto.valor));
              resultadoBody.appendChild(row);
          });
      })
      .catch((erro) => {
          console.error(erro); // Registrar o erro no console
          alert('Ocorreu um erro ao buscar a categoria.'); // Alertar o usuário em caso de erro
      });
  };
  
  // Função auxiliar para criar células de tabela
  const criarCelula = (conteudo) => {
      const cell = document.createElement('td');
      cell.innerText = conteudo;
      return cell;
  };