// Configuracao da API
const API_URL = 'http://localhost:5001/api';

// Funcao para verificar se o usuario esta autenticado
function checkAuth() {
    const token = localStorage.getItem('token');
    const currentPage = window.location.pathname.split('/').pop();

    if (!token && currentPage !== 'login.html' && currentPage !== '') {
        // Nao autenticado e nao esta na pagina de login
        window.location.href = 'login.html';
        return false;
    }

    if (token && (currentPage === 'login.html' || currentPage === '')) {
        // Ja autenticado, redireciona para dashboard
        window.location.href = 'dashboard.html';
        return false;
    }

    return true;
}

// Funcao de login
async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Salva o token e dados do usuario no localStorage
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));

            // Redireciona para o dashboard
            window.location.href = 'dashboard.html';
        } else {
            // Mostra mensagem de erro
            errorMessage.textContent = data.error || 'Erro ao fazer login';
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        errorMessage.textContent = 'Erro de conexao com o servidor';
        errorMessage.style.display = 'block';
        console.error('Erro:', error);
    }
}

// Funcao de logout
async function logout() {
    const token = localStorage.getItem('token');

    try {
        // Chama endpoint de logout (opcional, apenas para validar o token)
        await fetch(`${API_URL}/auth/logout`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
    } catch (error) {
        console.error('Erro ao fazer logout:', error);
    }

    // Remove dados do localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('user');

    // Redireciona para login
    window.location.href = 'login.html';
}

// Funcao para obter o token
function getToken() {
    return localStorage.getItem('token');
}

// Funcao para obter dados do usuario
function getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

// Inicializa a pagina de login
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
}

// Inicializa a pagina do dashboard
if (document.getElementById('userName')) {
    const user = getUser();
    if (user) {
        document.getElementById('userName').textContent = user.username;
    }
}

// Verifica autenticacao ao carregar a pagina
checkAuth();
