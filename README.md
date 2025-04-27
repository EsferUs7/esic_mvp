Це README файл.

Тут ми описуємо основні поняття, визначення, функціонал та особливості нашого проєкту: ТГ-бот "ESIc".

Наша команда:
- Developer: Станіслав Бойко
- Project Manager: Ілля Віжуткін
- Product Manager and Tester: Есфер Усеінов


функціонал, призначення, особливості

Project Overview
This project is a Telegram bot called ESIc designed for entertainment and educational purposes.
The bot provides quizzes, random utilities, user ratings, and is configurable for different group chat activities.

Team
 - Developer: Stanislav Boiko
 - Project Manager: Illia Vizhutkin
 - Product Manager and Tester: Esfer Useinov

Key Features
Quiz System:
 - Scheduled quizzes posted automatically in chats.
 - Customizable quiz period and time settings with /set_period and /set_time.
 - Handling user answers and calculating correct responses.

User Ratings:
 - Command /my_rating shows the user's individual score.
 - Command /top displays a leaderboard of top participants in the chat.

Random Utilities:
 - Command /random_number returns a random number within specified bounds.
 - Command /random_member selects a random member from the group chat.

Database Integration:
Persistent storage of users, chats, quiz questions, answers, using a relational database.


Technologies Used
 - Python (Aiogram 3 for Telegram bot development)
 - PostgreSQL (Database)
 - Docker (Containerization for easier development and deployment)

Purpose
The ESIc bot is intended to make group chats more fun and interactive by combining knowledge testing, competitive elements, and random games.
It is highly configurable and aims to maintain an engaging environment for its users.