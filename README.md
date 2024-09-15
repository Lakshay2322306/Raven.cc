# BITTU CHECKER Bot

## Description
A Telegram bot for various functionalities including BIN checking, scraping, and website analysis.

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/bittu-checker.git
    cd bittu-checker
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**
    - Create a `.env` file or configure environment variables in Render.
    - Add the following variable:
      ```
      BOT_TOKEN=your_telegram_bot_token
      ```

4. **Run the bot:**
    ```sh
    python main.py
    ```

## Deployment on Render

1. **Create a new web service:**
    - Go to the [Render dashboard](https://dashboard.render.com/).
    - Click "New" and select "Web Service".

2. **Connect your repository:**
    - Choose the repository containing your project.
    - Select the branch to deploy.

3. **Configure your service:**
    - For the "Build Command", enter: `pip install -r requirements.txt`
    - For the "Start Command", enter: `python main.py`

4. **Add environment variables:**
    - In the Render dashboard, go to your service settings.
    - Add a new environment variable:
      ```
      Key: BOT_TOKEN
      Value: your_telegram_bot_token
      ```

5. **Deploy the service:**
    - Click "Create Web Service" and Render will handle the rest.
