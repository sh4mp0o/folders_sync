import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from main import DirectorySyncApp
from sync import DirectorySynchronizer
from database import DatabaseLogger


class TestDirectorySyncApp(unittest.TestCase):

    def setUp(self):
        # Создаем тестовое приложение
        self.app = DirectorySyncApp()
        self.app.update()  # Обновляем интерфейс

    #Тестируют правильную работу методов выбора источника
    @patch("main.filedialog.askdirectory", return_value="/fake/source")
    def test_select_source(self, mock_askdirectory):
        self.app.select_source()
        self.assertEqual(self.app.source, "/fake/source")
        self.assertEqual(self.app.source_label.cget("text"), "Источник: /fake/source")

    #Тестируют правильную работу методов выбора приемника
    @patch("main.filedialog.askdirectory", return_value="/fake/target")
    def test_select_target(self, mock_askdirectory):
        self.app.select_target()
        self.assertEqual(self.app.target, "/fake/target")
        self.assertEqual(self.app.target_label.cget("text"), "Приемник: /fake/target")

    #Тестирует работу метода синхронизации, если не выбраны источники или приемники
    @patch("main.messagebox.showerror")
    @patch("main.messagebox.showinfo")
    def test_sync_directories_without_paths(self, mock_showinfo, mock_showerror):
        self.app.sync_directories()
        mock_showerror.assert_called_with("Ошибка", "Выберите оба каталога!")

    #Тестирует успешную синхронизацию, когда оба каталога выбраны
    @patch("main.messagebox.showinfo")
    @patch("sync.DirectorySynchronizer.synchronize")
    def test_sync_directories_with_paths(self, mock_synchronize, mock_showinfo):
        self.app.source = "/fake/source"
        self.app.target = "/fake/target"
        mock_synchronize.return_value = None 

        self.app.sync_directories()
        mock_showinfo.assert_called_with("Успех", "Синхронизация завершена!")

    #Тестирует обработку ошибки, когда метод синхронизации вызывает исключение
    @patch("sync.DirectorySynchronizer.synchronize")
    @patch("main.messagebox.showerror")
    def test_sync_directories_with_error(self, mock_showerror, mock_synchronize):
        self.app.source = "/fake/source"
        self.app.target = "/fake/target"
        mock_synchronize.side_effect = Exception("Произошла ошибка")

        self.app.sync_directories()
        mock_showerror.assert_called_with("Ошибка", "Произошла ошибка: Произошла ошибка")


if __name__ == "__main__":
    unittest.main()
