import shutil
import os
import datetime


def create_archive():
    # Название архива: orders_service_v1.0_2023-10-05
    # (В реальности версию лучше брать из тега Git, но пока упростим)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    output_filename = f"microshop_release_{today}"

    # Папка, которую хотим архивировать
    source_dir = "orders_service"

    print(f"Начинаю упаковку сервиса {source_dir}...")

    # Создаем ZIP архив
    shutil.make_archive(output_filename, 'zip', source_dir)

    print(f"Архив создан: {output_filename}.zip")


if __name__ == "__main__":
    create_archive()
