# Drip Logs to Database

## Project Structure

```
├── LICENSE            <- Open-source license if one is chosen
├── README.md          <- The top-level README for developers using this project
├── data
│   └── database.db    <- Database file
│
├── database
    │
    ├── database.py    <- Database class to connect with SQLite
    └── models.py      <- Database models
│
├── requirements.txt   <- The requirements file for this project (generated with `pip freeze > requirements.txt`)
│
└── src                         <- Source code for this project
    │
    ├── __init__.py             <- Makes src a Python module
    ├── config.py               <- Store useful variables and configuration
    ├── database.py             <- Database class to connect with SQLite
    ├── logger.py               <- Logger class to log messages to the database
    └── services                <- Service classes to connect with external platforms, tools, or APIs
        └── drip_service.py     <- Service class to connect with Drip API
```
## Usage

```
cp .env.sample .env              # <--- Set your environment variables in .env
pip install -r requirements.txt  # <--- Install dependencies
python -m src.main   # <--- Run the script
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.