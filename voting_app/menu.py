class MenuItem:
    def __init__(self, name, title, url):
        self.name = name
        self.title = title
        self.url = url

        self.is_active = False
        self.is_dropdown = False
        self.is_right = True


class DropdownItem(MenuItem):
    def __init__(self, name, title, url):
        super().__init__(name, title, url)

        self.items = []
        self.is_dropdown = True


REGISTER_PAGE_NAME = "register"
LOGIN_PAGE_NAME = "login"
USER_PAGE_NAME = "user"
LOGOUT_PAGE_NAME = "logout"

HOME_PAGE_NAME = "index"

VOTES_PAGE_NAME = "votes"
VOTE_PAGE_NAME = "vote"
USER_VOTES_PAGE_NAME = "user_votes"
VOTES_EDITOR_PAGE_NAME = "votes_editor"

login_menu_item = MenuItem(LOGIN_PAGE_NAME, "Вход", "/login")
register_menu_item = MenuItem(REGISTER_PAGE_NAME, "Регистрация", "/register")

my_user_menu_item = MenuItem(LOGOUT_PAGE_NAME, "Профиль", "/user/")
logout_menu_item = MenuItem(LOGOUT_PAGE_NAME, "Выход", "/logout")

home_menu_item = MenuItem(HOME_PAGE_NAME, "Главная", "/")
votes_menu_item = MenuItem(VOTES_PAGE_NAME, "Список Голосований", "/votes")

user_votes_menu_item = MenuItem(USER_VOTES_PAGE_NAME, "История Голосований", "/votes/my")
votes_editor_menu_item = MenuItem(VOTES_EDITOR_PAGE_NAME, "Редактор Голосований", "/votes/editor")


def get_context_menu(request, current_name):
    return {"left": get_context_left_menu(request, current_name),
            "right": get_context_right_menu(request, current_name)}


def get_context_left_menu(request, current_name):
    menu = [home_menu_item]

    if request.user.is_authenticated:
        menu.append(votes_menu_item)
        menu.append(user_votes_menu_item)
        menu.append(votes_editor_menu_item)
    else:
        menu.append(login_menu_item)
        menu.append(register_menu_item)

    for item in menu:
        if item.name == current_name:
            item.is_active = True
        else:
            item.is_active = False

    return menu


def get_context_right_menu(request, current_name):
    menu = []

    if request.user.is_authenticated:
        my_user_menu_item.url = '/user/' + str(request.user.id)

        account_menu_item = DropdownItem("account", "Аккаунт", "")
        account_menu_item.items.append(my_user_menu_item)
        account_menu_item.items.append(logout_menu_item)

        account_menu_item.title = request.user.username
        menu.append(account_menu_item)

    for item in menu:
        if item.name == current_name:
            item.is_active = True
        else:
            item.is_active = False

    return menu
