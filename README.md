# 🌊 Merry - One Piece Card Game Management 🏴‍☠️

Ahoy, nakama! 👋 Welcome to Merry, your friendly companion for navigating the vast seas of the One Piece Card Game!

## 🗺️ About

Merry is a Django-powered project designed to streamline and enhance your One Piece Card Game experience. It provides features like:

- **Card Database:** Explore a comprehensive database of One Piece cards, complete with details, images, and pricing information.
- **Card Recognition:** A strategy that combines Machine Learning with Google’s Gemini AI is used to identify cards from images.
- **Deck Building:** (Coming Soon! 🚧) Craft powerful decks and strategize your next conquest.
- **Price Tracking:** Stay updated on the latest card prices from various vendors.
- **Community Features:** (Coming Soon! 🚧) Connect with fellow One Piece enthusiasts, share decks, and discuss strategies.

## 🚀 Getting Started

Setting sail with Merry is easy peasy! 

1. **Clone the Repo:** 
   ```bash
   git clone https://github.com/your-username/merry.git
   ```

2. **Prepare the Environment:**
    - Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        ```
    - Open `.env` and set a strong, unique `DJANGO_SECRET_KEY`. You can use an online generator or Django's built-in command:
        ```bash
        python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
        ```

3. **Set Sail with Docker:**
   ```bash
   make up
   ```
   This will launch the application using Docker Compose.

4. **Access Merry:** Open your web browser and navigate to `http://localhost:8000` (or the port specified in your Docker Compose configuration).

## 🧰 Requirements

- Docker
- Docker Compose
- Make

## 🛠️ Makefiles - Double the Power!

Merry utilizes **two Makefiles** to make your life easier:

**1. Project Builder Makefile (`/Makefile`):**

   This Makefile, located in the project's root directory, handles the big picture tasks related to building and running your application within Docker:

   - `make up`: This is your primary command to start the application. It spins up all the necessary Docker containers (including the web server, database, Redis, Celery, and optionally Flower for monitoring Celery tasks) as defined in the `docker-compose.yml` file.

   - `make down`: Use this to gracefully shut down and remove the Docker containers when you're done with Merry.

   - `make restart`:  This command restarts all the running Docker containers. Useful for when you've made changes to your code or configuration and want to refresh the application.

   - `make build`: This specifically builds (or rebuilds) the Docker image for the core application, based on the instructions in the main `Dockerfile`.

   - `make docker-list-services`:  Lists out the names of all the services defined within your `docker-compose.yml` file. This can be helpful as a reference when you want to target specific containers with other commands.

   - `make docker-join c=<container_name>`: Allows you to get an interactive shell inside a running Docker container. Replace `<container_name>` with the actual name of the service from `docker-compose.yml` (e.g., `api`, `merry-postgres`). This is great for debugging or inspecting the state of your application.

**2. Container Makefile (`/src/Makefile`):**

   This Makefile lives inside the `src` directory and is specifically designed to be used **within the running Docker container**. It manages tasks related to your Django project itself:

   - `make resetdb`: This is a powerful (and potentially destructive!) command that completely wipes out the existing database and sets up a fresh one.  Use this only if you intentionally want to start from scratch with your database. It's often used during development, especially when you need to apply new migrations or clear out test data.

   - `make restore`:  Combines `make restore-db` and `make restore-media` to restore both your database and media files from backups. 

   - `make restore-db`: Restores the database from a backup located at the path specified by the `DB_DUMP_PATH` variable in your `.env` file. 

   - `make restore-media`:  Restores media files from a backup located at the path specified by the `MEDIA_BACKUP_PATH` variable in your `.env` file.

   - `make backup`:  Creates backups of your database and media files, saving them to the locations specified by `DB_DUMP_PATH` and `MEDIA_BACKUP_PATH` respectively in your `.env` file.

## 🤝 Contributing

Want to join the crew and make Merry even better?  We welcome contributions from fellow pirates! 

- **Report Bugs:** Create an issue on GitHub describing the problem you encountered. 
- **Suggest Features:** Open an issue on GitHub outlining the feature you'd like to see.
- **Submit Pull Requests:** Fork the repository, make your changes, and submit a pull request. 

## 🍻 Cheers!

May your pulls be lucky and your decks be unbeatable!  Let's set sail for grand adventures in the world of One Piece!
