# Автоматична документація

## Кроки для автоматичного генерування документації.

### Крок 1: Встановлення Sphinx.
```bash
pip install sphinx
```
### Крок 2: Ініціалізація Sphinx.
```bash
sphinx-quickstart
```
### Крок 3: Конфігурація файлу [конфігурації](Sphinx/source/conf.py):
Треба встановити такі extensions

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
]

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

sys.path.insert(0, os.path.abspath('../../../'))

### Крок 4: Додавання файлів .rst у [диркеторію](Sphinx/source/)
Для кожного файлу треба додати у [диркеторію](Sphinx/source/) файл .rst, наприклад для config.rst:
[приклад](Sphinx/source/config.rst)
### Крок 5: Додавання створених файлів в toctree:
У файлі [index.rst](Sphinx/source/index.rst) треба написати в toctree назви створених файлів.
### Крок 6: Білд
Після цього треба забілдити проєкт:
З директорії [TGChatBot/docs/Sphinx](./Sphinx)

Спочатку чистимо файли:
```bash
.\make.bat clean
```
Потім треба забілдити проєкт:
```bash
.\make.bat html
```

## Лінтери для документації
doc8 — перевіряє відповідність документації стилю reStructuredText.

### Встановлення
```bash
pip install doc8
```
### Використання:
```bash
doc8 docs/
```

rstcheck — валідує синтаксис .rst та перехресні посилання.

### Встановлення
```bash
pip install rstcheck
```
### Використання
```bash
rstcheck docs/
```
