Aqui está um **README.md limpo e profissional** pronto para subir no Git:

```markdown
# 📍 Valence Services

> Plataforma de conexão local — Encontre profissionais verificados perto de você em Valence e região.

[![Status](https://img.shields.io/badge/status-MVP-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Conformidade](https://img.shields.io/badge/RGPD-Conforme-blueviolet)]()

---

## 🎯 Sobre o Projeto

**Valence Services** é uma plataforma que conecta usuários a profissionais locais verificados na região de Valence, França. Com foco em conformidade RGPD e busca geolocalizada inteligente.

### ✨ Funcionalidades Principais
- 🔍 **Busca Geolocalizada** - Encontre profissionais em um raio de 500m a 50km
-  **Filtros por Serviço** - Limpeza, eletricidade, encanamento, cuidados, educação, etc.
- ✅ **Profissionais Verificados** - Sistema de validação e badges de confiança
- 🛡️ **100% RGPD** - Consentimento explícito, exportação/eliminação de dados, logs de auditoria

---

## 🏗️ Stack Tecnológica

| Camada | Tecnologia | Hospedagem |
|--------|------------|------------|
| **Frontend** | Next.js 16 + TypeScript + Tailwind CSS | Vercel |
| **Backend** | FastAPI + SQLAlchemy | Render |
| **Banco de Dados** | PostgreSQL 15 + Neon | Neon (Cloud) |
| **Cache** | Memória local (MVP) | - |

---

## 🚀 Instalação Local

### Pré-requisitos
- Python 3.10+
- Node.js 18+
- Conta [Neon](https://neon.tech) (gratuita)

### 1. Clonar Repositório
```bash
git clone https://github.com/Rikoborges/valence-services.git
cd valence-services
```

### 2. Configurar Backend
```bash
cd backend

# Criar ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
# Crie backend/.env com:
# DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require

# Iniciar servidor
uvicorn app.main:app --reload
```
✅ API: http://127.0.0.1:8000  
✅ Docs: http://127.0.0.1:8000/docs

### 3. Configurar Frontend
```bash
cd frontend

# Instalar dependências
npm install

# Configurar API
# Crie frontend/.env.local com:
# NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

# Iniciar desenvolvimento
npm run dev
```
✅ App: http://localhost:3000

---

## 🔐 Conformidade RGPD

O projeto inclui nativamente:
- ✅ Modal de consentimento antes de coleta de dados
- ✅ Logs de auditoria imutáveis (tabela `consent_logs`)
- ✅ Endpoint de exportação de dados (`GET /api/v1/consent/export/{user_id}`)
- ✅ Endpoint de eliminação de dados (`DELETE /api/v1/consent/erase/{user_id}`)
- ✅ Anonimização após 30 dias

---

## 📡 API Endpoints

### Busca Geolocalizada
```http
POST /api/v1/recherche/geo
Content-Type: application/json

{
  "lat": 44.933,
  "lng": 4.892,
  "rayon_m": 15000,
  "types_services": ["menage"]
}
```

### Registrar Consentimento
```http
POST /api/v1/consent
{
  "user_id": "uuid",
  "consent_type": "gps",
  "purpose": "local_search"
}
```

---

## 🌐 Deploy em Produçãoção

### Variáveis de Ambiente

**Backend (Render):**
```env
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require
```

**Frontend (Vercel):**
```env
NEXT_PUBLIC_API_URL=https://seu-backend.onrender.com
```

### Passos
1. Crie banco no [Neon](https://neon.tech) → copie `DATABASE_URL`
2. Deploy backend no [Render](https://render.com)
3. Deploy frontend no [Vercel](https://vercel.com)
4. Configure as variáveis de ambiente

---

## 📁 Estrutura do Projeto

```
valence-services/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── geo.py          # Busca geolocalizada
│   │   │   └── consent.py      # Logs RGPD
│   │   ├── models.py           # Modelos SQLAlchemy
│   │   ├── cache.py            # Cache simples
│   │   └── main.py             # App FastAPI
│   ├── requirements.txt
│   └── .env                    # ⚠️ NÃO COMMITAR
│
├── frontend/
│   ├── app/
│   │   └── page.tsx            # Página principal
│   ├── components/
│   │   └── ConsentModal.tsx    # Modal RGPD
│   ├── package.json
│   └── .env.local              # ⚠️ NÃO COMMITAR
│
├── .gitignore
└── README.md
```

---

## 🧪 Testes Rápidos

```bash
# Testar API
curl -X POST http://localhost:8000/api/v1/recherche/geo \
  -H "Content-Type: application/json" \
  -d '{"lat":44.933,"lng":4.892,"rayon_m":15000,"types_services":["menage"]}'
```

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Commit: `git commit -m 'feat: minha feature'`
4. Push: `git push origin feature/minha-feature`
5. Abra um Pull Request

---

## 📄 Licença

MIT © 2026 - Riko Borges

---

## 📞 Contato

**Riko Borges**  
📧 ricoborges@example.com  
🐙 [@Rikoborges](https://github.com/Rikoborges)

---

> ⚠️ **Aviso**: Este é um MVP. Não utilize em produção sem auditoria de segurança completa.

**Feito com ❤️ para Valence, França** 🇫🇷
```

---

## ✅ CHECKLIST ANTES DE SUBIR

Agora, antes de fazer o commit, execute:

```powershell
# 1. Verifique se .gitignore existe
Test-Path .gitignore

# 2. Veja o que será enviado
git status

# 3. Garanta que NÃO aparecem:
#    - backend/.env
#    - frontend/.env.local
#    - backend/venv/
#    - frontend/node_modules/
#    - frontend/.next/

# 4. Se estiver tudo limpo, faça o commit
git add .
git commit -m "feat: MVP completo - FastAPI + Next.js + PostgreSQL + RGPD"
git push -u origin main
```

**Está pronto!** 🚀 O README está profissional, limpo e sem informações sensíveis.
