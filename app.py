


from github import Github
from core import app
from config import Configuration

import os
port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
    #app.run(ssl_context='adhoc')




