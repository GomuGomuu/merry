from celery import shared_task


@shared_task
def exemplo_task():
    print("Tarefa executada com sucesso!")
