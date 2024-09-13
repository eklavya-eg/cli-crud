Hello,
This is simple cli app on POSTGRESQL hosted on neon db. password cannot be changed so db string has username mentioned password different.

connection string (.env also has) - DATABASE_URL="postgresql://users_owner:FXergW0iB1IA@ep-damp-smoke-a1ug0on3.ap-southeast-1.aws.neon.tech/sss_assignment_sep24?sslmode=require"

check db.py for tables and schemas

having feature                                                              COMMANDS
  - create users (password is hashed using sha256)       -   python main.py create -un <username> -ps <password>
  - search for cities                                    -   python main.py create -un <username> -ps <password> -ct <city name>
  - update password                                      -   python main.py create -un <username> -ps <password> -newun <new password>
  - delete particular histor using id                    -   python main.py create -un <username> -ps <password> -id <history id>
  - display all history for users having id for each id  -   python main.py create -un <username> -ps <password>
  - authentication

