import os
import shutil
import filecmp
from database import DatabaseLogger


class DirectorySynchronizer:
    def __init__(self, db_path="sync_log.db"):
        self.logger = DatabaseLogger(db_path)

    def synchronize(self, source, target):
        comparison = filecmp.dircmp(source, target)

        # Копируем новые файлы и папки из источника в приемник
        for file in comparison.left_only:
            source_path = os.path.join(source, file)
            target_path = os.path.join(target, file)
            if os.path.isdir(source_path):
                shutil.copytree(source_path, target_path)
                self.logger.log_action("Добавлена папка", target_path)
            else:
                shutil.copy2(source_path, target_path)
                self.logger.log_action("Добавлен файл", target_path)

        # Обновляем измененные файлы
        for file in comparison.diff_files:
            source_path = os.path.join(source, file)
            target_path = os.path.join(target, file)
            shutil.copy2(source_path, target_path)
            self.logger.log_action("Обновлен файл", target_path)

        # Удаляем лишние файлы и папки из приемника
        for file in comparison.right_only:
            target_path = os.path.join(target, file)
            if os.path.isdir(target_path):
                shutil.rmtree(target_path)
                self.logger.log_action("Удалена папка", target_path)
            else:
                os.remove(target_path)
                self.logger.log_action("Удален файл", target_path)

        # Рекурсивно синхронизируем подкаталоги
        for common_dir in comparison.common_dirs:
            self.synchronize(
                os.path.join(source, common_dir),
                os.path.join(target, common_dir)
            )
