# IT Quiz Generator

## Description

**IT Quiz Generator** est une application web destinée aux étudiants en informatique.

L'application permet de générer automatiquement des quiz à partir d'un sujet informatique grâce à **Azure OpenAI** et au modèle **GPT-5 mini**.

L'utilisateur choisit :

- un sujet informatique ;
- le nombre de questions, de 1 à 10.

L'application génère ensuite les questions avec **4 propositions de réponse**.

L'étudiant doit d'abord sélectionner ses réponses. Après avoir terminé, il clique sur **Validate Quiz** pour obtenir son score, voir les réponses correctes et consulter les corrections et explications.

---

## Technologies utilisées

- **Python**
- **FastAPI**
- **HTML / CSS / JavaScript**
- **Azure OpenAI**
- **GPT-5 mini**
- **Docker**
- **Azure Container Registry**
- **Azure Container Apps**
- **Git / GitHub**
- **GitHub Actions**

---

## Architecture du projet

```text
it-quiz-generator/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── .dockerignore
├── .gitignore
├── Dockerfile
├── main.py
├── requirements.txt
└── README.md
## Démonstration vidéo

🎥 **Voir la démonstration vidéo :**

[▶️ Accéder à la vidéo de démonstration](https://drive.google.com/file/d/10NuhgF2QPnS_VfiDz0VJMaC2O3DBfVcN/view?usp=sharing)