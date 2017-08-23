# Telegraph Clone

Clone of [telegra.ph](http://telegra.ph/).\
On this site user create anonymous story and publish it, with the subsequent possibility of post editing.\
Post editing using cookies authorization and possible within 7 days.

Working example: [telegraph-clone.herokuapp.com](https://telegraph-clone.herokuapp.com/)

# How to install
1. Recomended use venv or virtualenv for better isolation.\
   Venv setup example: \
   `python3 -m venv myenv`\
   `source myenv/bin/activate`
2. Install requirements: \
   `pip3 install -r requirements.txt` (alternatively try add `sudo` before command)

# How to launch
   - Run server `gunicorn server:app`
   - Open on browser `http://127.0.0.1:8000`

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
