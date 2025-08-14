# Story Generator

## Overview
Story Generator is a **full-stack web application** that lets users create and play interactive *"Choose Your Own Adventure"* stories powered by AI.  
Inspired by classic adventure books where readers make decisions to shape the narrative, this app uses **OpenAI's GPT models** to dynamically generate unique branching stories based on a user-provided theme (e.g., *pirates*, *space exploration*, *mystery*).

---

## Features
- **AI Story Generation** – Create unique stories by entering a theme or prompt.
- **Interactive Gameplay** – Progress through the story by making choices that lead to different paths and endings.
- **Shareable Links** – Share generated stories with friends via unique URLs.
- **Full-Stack Implementation** – Backend API design, database integration, AI model interactions, and a polished frontend built with React.

---

## How It Works
1. **Enter a Theme** – The user types a theme, such as “Haunted House” or “Lost in Space”.
2. **AI Generates Story** – The backend sends the theme to the AI model, which returns the first part of the story along with choices.
3. **Make Choices** – The user selects an option, and the AI generates the next part of the story accordingly.
4. **Repeat Until Ending** – The process continues until the story reaches a conclusion.
5. **Save & Share** – The final story can be saved and shared through a generated link.

---

## Tech Stack
- **Frontend**: React, HTML5, CSS3
- **Backend**: Node.js, Express
- **Database**: MongoDB (for storing stories and sessions)
- **AI Model**: OpenAI GPT API
- **Styling**: Tailwind CSS (or CSS modules depending on your setup)
- **Hosting**: (Add hosting service here if applicable, e.g., Vercel, Heroku, Render)

---

## Installation & Setup
To run this project locally:

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/Story_Generator.git
cd Story_Generator

# 2. Install dependencies
npm install
cd backend && npm install
cd ..

# 3. Create a .env file in the backend directory and add:
OPENAI_API_KEY=your_api_key_here
MONGODB_URI=your_mongo_db_uri_here

# 4. Run the development server
npm run dev


--------------
```


<img width="1919" height="441" alt="image" src="https://github.com/user-attachments/assets/14c8909b-6699-44e0-afbf-46385898e51f" />

<img width="1919" height="634" alt="image" src="https://github.com/user-attachments/assets/052dea24-6981-4b5c-912a-2d746ece51e5" />

<img width="1919" height="550" alt="image" src="https://github.com/user-attachments/assets/6146e563-15c5-4acd-8f27-d582af5e0fce" />

