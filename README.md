# Bussiness Manager

Personal project to put in practice all my backend knowledge by building a multicompany ERP system, with capabilities to track and register products, clients, sales, transfers and purchase orders.

For the framework i made use of FastApi.

The config is loaded in the config.py, with pydantic-settings, is importan to made use of recent pydantic version because im currently using settings_cached function instead of the classic lru_cache implementation.

ORM used is sqlalchemy with asyncpg for using postgres in async functions.

I implemented a file s3 bucket system, taking advantage of the supabase fre plan that comes with a s3 file storage, and we are connecting to it with boto3 like in aws.

Right now the emails get deliver by the layers service on endpoint calls directly, in the future i need to take a view to implement rabbitmq and celery to split message sending responsabilities, by the way i made use of the resend async sdk so sending the email are not blocking the loop.

Fastapi includes out of the box logs sending to systems with OpenTelemetry standard compability

## AI use

The only use of AI for this project is for making the initial idea and for some infraestructure questions, just by using it in the web client, all the code has been written by hand.
