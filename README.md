# Home Accountant

A self-hosted web application created for managing bank accounts

# Requirements

In order to operate succesfully, this project require Python 3.7+ and a ready to user SQL database (PostgreSQL for now).

# Installation

1. Create a virtual environment with ```python -m venv venv```
2. Activate the virtual environment with ```source venv/bin/activate```
3. Install all the packages with ```pip install -r requirements.txt```
4. Run the software with ```python homeaccountant```

# Configuration

HomeAccountant can be configure with the help of a `config.yaml` file, located at `~/.config/homeaccountant/config.yaml`.

Here is an example :

    server:
        hostname: 127.0.0.1
        port: 8080
        login:
            auth_token_expire: 900
            refresh_token_expire: 7200
        logging:
            file: /path/to/log/file
            file_size: 4000000
            print: True
            verbosity: DEBUG
        registration:
            allow: True
            regex: .*@example.com$
            admin_confirmation: False
            email_confirmation: True
        sendmail:
            enabled: True
            use_ssl: True
            hostname: smtp.example.com
            port: 465
            username: user@example.com
            password: userpassword
    database:
        postgres:
            hostname: 127.0.0.1
            port: 5432
            username: postgres
            password: test
            database: homeaccountant