# FL2F Final Interview Task

All the source code is written in python and can be found at main.py file.

## To run this script on your machine:

1. Open the cmd

2. Clone the repository
   ```bash
   git clone https://github.com/Ba6ySHark/FL2F.git
   ```
   
3. Set up the virtual environment
   ```bash
   virtualenv myenv
   ```
   ```bash
   cd myenv/Scripts
   ```
   ```bash
   activate
   ```
   
4. Install the required pachages
   ```bash
   pip install -r requirements.txt
   ```

5. Run the main.py file
   ```bash
   python main.py
   ```
## Important notes:

1. I decided to choose Reddit API. The free version of this API only allows for 100 requests per minute. Therefore, I added a time.sleep(60) statement at the end of the main loop. Since I am parsing ~1500 posts, it takes around 15 minutes for the application to run.

2. In order to use the API, I had to register a new application at https://www.reddit.com/prefs/apps. When you register an application there, Reddit provides you with a CLIENT_ID and a SECRET_KEY. The application requires for CLIENT_ID, SECRET_KEY, REDDIT_USERNAME and REDDIT_PASSWORD to be saved in an .env file in the same directory as main.py.

REDDIT_USERNAME is your Reddit account username &
REDDIT_PASSWORD is the password associated with your Reddit account username

3. I am storing the results in .csv format, which does not carry any formatting information (since it is a plain-text file). Because of this the width of the columns has to be adjusted manually each time you open the file.
