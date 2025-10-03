// Variavel global para armazenar o ID do produto em edicao
let editingProductId = null;

// Carrega os produtos ao carregar a pagina
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('productForm')) {
        loadProducts();
        document.getElementById('productForm').addEventListener('submit', handleSubmit);
    }
});

// Funcao para carregar produtos
async function loadProducts() {
    const token = getToken();
    const loadingMessage = document.getElementById('loadingMessage');
    const productsBody = document.getElementById('productsBody');
    const emptyMessage = document.getElementById('emptyMessage');

    loadingMessage.style.display = 'block';

    try {
        const response = await fetch(`${API_URL}/products/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const products = await response.json();

            productsBody.innerHTML = '';

            if (products.length === 0) {
                emptyMessage.style.display = 'block';
                document.getElementById('productsTable').style.display = 'none';
            } else {
                emptyMessage.style.display = 'none';
                document.getElementById('productsTable').style.display = 'block';

                products.forEach(product => {
                    const row = createProductRow(product);
                    productsBody.appendChild(row);
                });
            }
        } else if (response.status === 401) {
            // Token expirado, faz logout
            logout();
        } else {
            showMessage('Erro ao carregar produtos', 'error');
        }
    } catch (error) {
        showMessage('Erro de conexao com o servidor', 'error');
        console.error('Erro:', error);
    } finally {
        loadingMessage.style.display = 'none';
    }
}

// Cria uma linha da tabela para um produto
function createProductRow(product) {
    const row = document.createElement('tr');

    row.innerHTML = `
        <td>${product.id}</td>
        <td>${product.nome}</td>
        <td>${product.marca}</td>
        <td>R$ ${parseFloat(product.valor).toFixed(2)}</td>
        <td class="actions">
            <button onclick="editProduct(${product.id})" class="btn btn-sm btn-primary">Editar</button>
            <button onclick="deleteProduct(${product.id})" class="btn btn-sm btn-danger">Excluir</button>
        </td>
    `;

    return row;
}

// Funcao para cadastrar ou editar produto
async function handleSubmit(event) {
    event.preventDefault();

    const token = getToken();
    const nome = document.getElementById('nome').value;
    const marca = document.getElementById('marca').value;
    const valor = parseFloat(document.getElementById('valor').value);

    const productData = { nome, marca, valor };

    try {
        let response;

        if (editingProductId) {
            // Atualizacao (PUT)
            response = await fetch(`${API_URL}/products/${editingProductId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(productData)
            });
        } else {
            // Criacao (POST)
            response = await fetch(`${API_URL}/products/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(productData)
            });
        }

        if (response.ok) {
            showMessage(editingProductId ? 'Produto atualizado com sucesso!' : 'Produto cadastrado com sucesso!', 'success');
            resetForm();
            loadProducts();
        } else {
            const data = await response.json();
            showMessage(data.error || 'Erro ao salvar produto', 'error');
        }
    } catch (error) {
        showMessage('Erro de conexao com o servidor', 'error');
        console.error('Erro:', error);
    }
}

// Funcao para editar produto
async function editProduct(id) {
    const token = getToken();

    try {
        const response = await fetch(`${API_URL}/products/${id}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const product = await response.json();

            // Preenche o formulario
            document.getElementById('nome').value = product.nome;
            document.getElementById('marca').value = product.marca;
            document.getElementById('valor').value = product.valor;

            // Atualiza o estado
            editingProductId = id;
            document.getElementById('formTitle').textContent = 'Editar Produto';
            document.getElementById('submitBtn').textContent = 'Atualizar';
            document.getElementById('cancelBtn').style.display = 'inline-block';

            // Scroll para o formulario
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            showMessage('Erro ao carregar produto', 'error');
        }
    } catch (error) {
        showMessage('Erro de conexao com o servidor', 'error');
        console.error('Erro:', error);
    }
}

// Funcao para excluir produto
async function deleteProduct(id) {
    if (!confirm('Tem certeza que deseja excluir este produto?')) {
        return;
    }

    const token = getToken();

    try {
        const response = await fetch(`${API_URL}/products/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            showMessage('Produto excluido com sucesso!', 'success');
            loadProducts();
        } else {
            const data = await response.json();
            showMessage(data.error || 'Erro ao excluir produto', 'error');
        }
    } catch (error) {
        showMessage('Erro de conexao com o servidor', 'error');
        console.error('Erro:', error);
    }
}

// Cancela a edicao
function cancelEdit() {
    resetForm();
}

// Reseta o formulario
function resetForm() {
    document.getElementById('productForm').reset();
    editingProductId = null;
    document.getElementById('formTitle').textContent = 'Cadastrar Produto';
    document.getElementById('submitBtn').textContent = 'Salvar';
    document.getElementById('cancelBtn').style.display = 'none';
    document.getElementById('formMessage').style.display = 'none';
}

// Mostra mensagem de feedback
function showMessage(text, type) {
    const messageEl = document.getElementById('formMessage');
    messageEl.textContent = text;
    messageEl.className = `message ${type === 'error' ? 'error-message' : 'success-message'}`;
    messageEl.style.display = 'block';

    // Esconde a mensagem apos 5 segundos
    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 5000);
}
