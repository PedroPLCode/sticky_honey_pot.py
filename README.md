# StickyHoneyPot - Multi-threaded Honeypot Server
A multi-threaded honeypot server that listens on specified ports, emulates various services, and logs suspicious activity.  
For each incoming connection, the honeypot sends a service-specific banner, receives data, and detects potential exploits.

## Features
- **Multi-threaded** – handles multiple connections concurrently.
- **Service emulation** – sends service-specific banners.
- **Threat detection** – identifies potential exploits.
- **GeoIP lookup** – logs the geographical origin of the connection.
- **Alerting** – sends alerts via Telegram.
- **Detailed logging** – timestamps, IP addresses, and attack details.

## Modules
- `socket` – network communication.
- `threading` – concurrent connection handling.
- `datetime` – event timestamping.
- `utils.exception_handler` – decorator for exception handling.
- `utils.alert_logs_utils` – log message creation.
- `utils.geoip` – GeoIP lookups.
- `utils.telegram_utils` – Telegram alert integration.
- `utils.exploit_detector` – exploit detection.
- `config` – service banners and port mappings.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/honeypot.git
cd honeypot
```
2. Set up a Python virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate or . venv/bin/activate
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Configure your environment variables by creating a .env file with your Binance API credentials, database URL, and email, telegram configuration.
```bash
TELEGRAM_BOT_TOKEN = 'your-telegram-bot-token'
TELEGRAM_CHAT_ID = 'your-telegram-chat-id'
```
5. Check and change config.py if needed.
6. Run tests:
```bash
python3 -m pytest
```
7. Run the app.
```bash
python3 -m app.honeypot
```
8. Tweak, pimp, improve and have fun.

## Testing
The project includes a test suite that can be executed using pytest. To run the tests, simply use pytest.


## Important! 
Familiarize yourself thoroughly with the source code. Understand its operation. Only then will you be able to customize and adjust scripts to your own needs, preferences, and requirements. Only then will you be able to use it correctly and avoid potential issues. Knowledge of the underlying code is essential for making informed decisions and ensuring the successful implementation of the app for your specific use case. Make sure to review all components and dependencies before running the scripts.

Code created by me, with no small contribution from Dr. Google and Mr. ChatGPT.
Any comments welcome.

StickyHoneyPot Project is under GNU General Public License Version 3, 29 June 2007