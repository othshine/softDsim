from pydantic import BaseSettings
from dotenv import load_dotenv


load_dotenv(".env")


class Configuration(BaseSettings):
    """Configuration Management class. This class reads the environment
    variables required for the database connection vom the environment. 

    Args:
        No arguments need to be passed to initialize an object of the 
        class since it reads the env vars automatically.
    """
    database_name: str
    database_host: str
    database_port: str
    database_user: str
    database_pass: str

    @property
    def mongo_client(self) -> str:
        """Created a string that can be used to connect to the mongodb.

        Returns:
            str: MongoDB client connection str 
                 (mongodb://user:pass@host:port/.....)
        """
        return f"mongodb://{self.database_user}:{self.database_pass}@{self.database_host}:{self.database_port}/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"


def get_config() -> Configuration:
    """This function should be used to create a Configuration object.
    A configuration object stores all the required variables to 
    connect to the mongoDB.

    Returns:
        Configuration: Instance of Configuration class
    """
    return Configuration()
