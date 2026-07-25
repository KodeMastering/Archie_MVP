import os
import shutil


def execute():
    desktop_path = os.path.expanduser("~/Desktop")
    staging_dir = os.path.join(desktop_path, "Archie_Staging")
    os.makedirs(staging_dir, exist_ok=True)

    target_extensions = ('.txt', '.png', '.lnk')

    for item in os.listdir(desktop_path):
        item_path = os.path.join(desktop_path, item)
        if os.path.isfile(item_path) and item.lower().endswith(target_extensions):
            shutil.move(item_path, staging_dir)

    return "Рабочий стол очищен. Файлы перемещены в зону Staging."
