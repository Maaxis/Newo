from selenium.common import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import org


class Forum:
    def __init__(self, subdomain: str, time_setting: int = 1, posts_per_page: int = 15, users = None, bot = None):
        self.subdomain = subdomain
        self.driver = start_driver()
        self.time_setting = time_setting  # see time_setting.txt for how to set this correctly
        self.url = "http://ndimforums.com/" + subdomain
        self.users = users
        self.bot = bot


class User:
    def __init__(self, subdomain: str, id: int = None, username: str = None, password: str = None, masks: list[str] = None, avatar: str = None, display_name: str = None, group: str = None):
        self.subdomain = subdomain
        self.id = id  # id is not required since we can also premake the object for preregistering
        self.username = username
        self.password = password
        self.masks = masks
        self.avatar = avatar
        self.group = group
        self.display_name = display_name


class Mask:
    def __init__(self):
        pass


class Group:
    def __init__(self):
        pass


class Bot(User):
    def __init__(self, subdomain: str, username: str, posts_per_page: int = 15):
        super().__init__(subdomain = subdomain, username = username, password = self.return_password(subdomain))
        self.posts_per_page = posts_per_page

    def return_password(self, subdomain):
        from secret import passwords
        from base64 import b64decode
        pw = b64decode(passwords.get(subdomain))
        return pw.decode('utf-8')


def start_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--use-gl=desktop')
    chrome_options.add_argument('user-data-dir=/selenium/')
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.google.com')
    driver.implicitly_wait(1)
    return driver


def setup():  # use this for first-time logins
    start_driver()


def login(forum, user, admin=False):
    driver = forum.driver
    if admin:
        driver.get(forum.url + '/Admin/admincp.asp')
    else:
        driver.get(forum.url + '/login.asp')
    # username_box = driver.find_element(By.NAME, "username")
    pw_box = driver.find_element(By.NAME, "pwd")
    button = driver.find_element(By.XPATH, "/html/body/div/form[3]/table/tbody/tr[2]/td/table/tbody/tr[4]/td/input")
    # username_box.send_keys("Newo")
    pw = user.password
    pw_box.send_keys(pw)
    driver.execute_script("arguments[0].click();", button)


def navigate_forum(forum: Forum, forum_id):
    driver = forum.driver
    url = forum.url + '/forum.asp?forumid=' + str(forum_id)
    driver.get(url)


def make_thread(forum: Forum, forum_id: int, thread_title: str, post_content: str, thread_description: str = "",
                locked: bool = False,
                pinned: bool = False,
                poll: bool = False, poll_question: str = "", poll_options: [str] = None, poll_num_of_options: int = 0,
                poll_num_of_votes: int = 0):  # TODO: set up polls
    driver = forum.driver
    driver.get(forum.url + '/newthread.asp?forumid=' + str(forum_id))
    title_box = driver.find_element(By.XPATH,
                                    "//*[@id=\"sendform\"]/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/input")
    description_box = driver.find_element(By.XPATH,
                                          "//*[@id=\"sendform\"]/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input")
    post_box = driver.find_element(By.ID, "fullreply")
    title_box.send_keys(thread_title)
    description_box.send_keys(thread_description)
    post_box.send_keys(post_content)
    if locked:
        lock = driver.find_element(By.XPATH,
                                   "//*[@id=\"sendform\"]/div/table/tbody/tr[2]/td/table/tbody/tr[6]/td/table/tbody/tr/td[1]/input")
        lock.send_keys(Keys.ENTER)
        lock.click()
    if pinned:
        pin = driver.find_element(By.XPATH,
                                  "//*[@id=\"sendform\"]/div/table/tbody/tr[2]/td/table/tbody/tr[6]/td/table/tbody/tr/td[2]/input")
        pin.send_keys(Keys.ENTER)
        pin.click()
    create = driver.find_element(By.XPATH, "//*[@id=\"sendform\"]/div/table/tbody/tr[2]/td/table/tbody/tr[7]/td/input")
    create.click()


def read_thread(forum, thread_id):
    pass


def navigate_thread(forum, thread_id):
    driver = forum.driver
    url = forum.url + '/thread.asp?threadid=' + str(thread_id)
    print(url)
    driver.get(url)


def make_post(forum, post_content, thread_id = None):
    driver = forum.driver
    thread = f"ndimforums.com/{forum.subdomain}/thread.asp?threadid={thread_id}"
    if (thread_id) and (thread not in driver.current_url):
        navigate_thread(forum, thread_id)
    text_box = driver.find_element(By.ID, "fastreply")
    reply_button = driver.find_element(By.XPATH, "/html/body/div/div[6]/table[2]/tbody/tr[2]/td[2]/form/input[1]")
    text_box.send_keys(post_content)
    reply_button.send_keys(Keys.ENTER)


def read_post(forum, thread_id, post_num):
    pass


###---ADMIN CP---###


def navigate_masks(forum):
    login(forum, forum.bot, admin=True)
    driver = forum.driver
    mask_page = driver.find_element(By.LINK_TEXT, "Forum Masks")
    mask_page.send_keys(Keys.ENTER)
    iframe = driver.find_elements(By.TAG_NAME, 'iframe')[0]
    driver.switch_to.frame(iframe)


def create_mask(forum, mask_name, dictionary):
    navigate_masks(forum)
    driver = forum.driver
    # test_dict = {
    #	"my forum": "",
    #	"subforum": "",
    #	"another forum": "v",
    #	"unique name": "vrc"
    # }
    add_button = driver.find_element(By.XPATH, "//*[@id=\"admin0\"]/table/tbody/tr[2]/td/table/tbody/tr/td/input")
    add_button.click()
    textbox = driver.find_element(By.CLASS_NAME, "textboxstyle")
    textbox.send_keys(mask_name)
    save = driver.find_element(By.XPATH, "//*[@id=\"admin0\"]/table/tbody/tr[9]/td/table/tbody/tr/td/input[4]")
    save.click()
    edit_mask(forum, mask_name, dictionary)


def edit_mask(forum, mask_name, dictionary, overwrite=False):
    # from masks page, locate and click edit button
    driver = forum.driver
    n = 1
    while True:
        try:
            ele = driver.find_element(By.XPATH,
                                      f"//*[@id=\"admin0\"]/table/tbody/tr[4]/td/table/tbody/tr[{n}]/td[1]").text
            if ele == mask_name:
                break
        except NoSuchElementException:
            print("mask not found")
            break
        n = n + 1
    edit_button = driver.find_element(By.XPATH,
                                      f"//*[@id=\"admin0\"]/table/tbody/tr[4]/td/table/tbody/tr[{n}]/td[2]/input")
    edit_button.click()
    # test_dict = {
    #	"my forum": "",
    #	"subforum": "",
    #	"another forum": "v",
    #	"unique name": "vrc"
    # }
    # from edit mask page, locate elements
    n = 1
    j = 6
    headers = []
    driver.implicitly_wait(0.1)
    while True:
        try:
            ele = driver.find_element(By.XPATH,
                                      f"// *[ @ id = \"admin0\"] / table / tbody / tr[{j}] / td / table / tbody / tr[{n}] / td[1]").text
            headers.append(ele.lower())
            n = n + 1
        except NoSuchElementException:
            if n == 1:
                break
            else:
                n = 1
                j = j + 2
    driver.implicitly_wait(1)
    # select masks
    for forum_title in headers:
        for key, value in dictionary.items():
            if key in forum_title:  # this has a definition
                red_cell = "rgba(153, 51, 51, 1)"
                n = headers.index(forum_title) + 1
                row = str(n)
                view = driver.find_element(By.XPATH, f"// *[ @ id = \"readcell{row}\"]")
                reply = driver.find_element(By.XPATH, f"// *[ @ id = \"replycell{row}\"]")
                create = driver.find_element(By.XPATH, f"// *[ @ id = \"createcell{row}\"]")
                if "v" in value:  # view should be green
                    if view.value_of_css_property("background-color") == red_cell:  # but is red
                        view.click()  # so toggle
                else:  # view should be red
                    if view.value_of_css_property("background-color") != red_cell:  # but is green
                        view.click()  # so toggle
                if "r" in value:
                    if reply.value_of_css_property("background-color") == red_cell:
                        reply.click()
                else:
                    if reply.value_of_css_property("background-color") != red_cell:
                        reply.click()
                if "c" in value:
                    if create.value_of_css_property("background-color") == red_cell:
                        create.click()
                else:
                    if create.value_of_css_property("background-color") != red_cell:
                        create.click()
            elif overwrite and key not in forum_title:
                pass
    save = driver.find_element(By.CLASS_NAME, "buttonstyle")
    save.click()
    driver.get(forum.url)


def read_mask(forum, user):
    pass


def navigate_groups(forum):
    pass


def create_group(forum):
    pass


def edit_group(forum):
    pass


def read_group(forum):
    pass


def preregister_member(forum, user):
    pass
    #pre-make the User class


def navigate_edit_member(forum):
    pass


def edit_member_group(forum):
    pass


def edit_member_masks(forum):
    pass


def navigate_edit_filters(forum):
    driver = forum.driver
    login(forum, forum.bot, admin=True)
    filter_page = driver.find_element(By.LINK_TEXT, "Word Filters")
    filter_page.send_keys(Keys.ENTER)
    iframe = driver.find_elements(By.TAG_NAME, 'iframe')[0]
    driver.switch_to.frame(iframe)


def add_filter(word_to_change, new_word, forum, mode=0):
    # mode 0 is Full Word Only, mode 1 is Containing Word
    driver = forum.driver
    text_boxes = driver.find_elements(By.XPATH, "//input[@type='text']")
    word1 = text_boxes[0]
    word2 = text_boxes[1]
    word1.clear()
    word2.clear()
    word1.send_keys(word_to_change)
    word2.send_keys(new_word)
    print(word_to_change + " -> " + new_word)
    button = driver.find_elements(By.XPATH, "//input[@type='Submit']")[0]
    selector = Select(driver.find_elements(By.CLASS_NAME, "selectstyle")[0])
    selector.select_by_value(str(mode))
    button.send_keys(Keys.ENTER)


def remove_filters(forum):
    pass


def add_filters(filter_dictionary, forum, mode=0):
    # filters should be in key value pairs
    for item in filter_dictionary:
        add_filter(item, filter_dictionary[item], forum, mode)


def overwrite_filters():
    pass


def return_user_obj(id: int):
    pass


def edit_avatar(user: User):
    pass


def main():
    return Forum(subdomain="void")


if __name__ == "__main__":
    main()
