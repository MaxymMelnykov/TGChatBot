��    	      d               �      �   E   �        Y        j  �   }  l     �   x  �  �     �  7   �  [  �  9   -  
   g  t   r  G   �  G   /	   callbacks.py Екземпляр TeleBot для взаємодії з Telegram API. Обробляє callback-запити: - Перехід по головному меню, допомога, контакти, FAQ. - Налаштування користувачів (замовник/ЖК). - Вибір типу та матеріалу контейнерів. - Опція датчиків наповнення для підземних контейнерів. - Підрахунок потрібних контейнерів для ЖК. - Запит номера телефону для замовника. Обробляє команду `/start` та виводить стартове меню. Параметри Працює в парі з іншими модулями проєкту: `config`, `handlers`, `Container`, `markups`, `user_data`, `utils`. Реєструє всі обробники команд і callback-запитів для Telegram-бота. Ця функція налаштовує основну логіку обробки взаємодії з користувачем: Project-Id-Version: PROJECT VERSION
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2025-04-16 17:11+0300
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: en
Language-Team: en <LL@li.org>
Plural-Forms: nplurals=2; plural=(n != 1);
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.17.0
 callbacks.py TeleBot instance for interacting with the Telegram API. Handles callback queries including:
- Navigation through the main menu, help, contacts, and FAQ.
- User role selection (customer/residential complex).
- Selection of container type and material.
- Sensor option for underground containers.
- Calculation of required containers for the residential complex.
- Request for the customer's phone number. Handles the `/start` command and displays the start menu. Parameters Works in conjunction with other project modules: `config`, `handlers`, `Container`, `markups`, `user_data`, `utils`. Registers all command and callback query handlers for the Telegram bot. This function configures the core logic for handling user interactions: 