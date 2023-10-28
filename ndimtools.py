from selenium.common import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import org


class Forum:
    def __init__(self, subdomain: str, time_setting: int = 1, posts_per_page: int = 15, users = None, bot = None):
        """
        Initializes a new instance of the MyClass class.

        Args:
            subdomain (str): The subdomain for the MyClass instance.
            time_setting (int, optional): The time setting for MyClass. Defaults to 1.
            posts_per_page (int, optional): The number of posts per page for MyClass. Defaults to 15.
            users (type, optional): A parameter description for users. Defaults to None.
            bot (type, optional): A parameter description for bot. Defaults to None.
        """
        self.subdomain = subdomain
        self.driver = start_driver()
        self.time_setting = time_setting  # see time_setting.txt for how to set this correctly
        self.url = "http://ndimforums.com/" + subdomain
        self.users = users
        self.bot = bot


class User:
    def __init__(self, subdomain: str, id: int = None, username: str = None, password: str = None, masks: list[str] = None, avatar: str = None, display_name: str = None, group: str = None):
        """
        Initializes a new instance of the class.

        Parameters:
            subdomain (str): The subdomain for the instance.
            id (int, optional): The ID for the instance. Defaults to None.
            username (str, optional): The username for the instance. Defaults to None.
            password (str, optional): The password for the instance. Defaults to None.
            masks (list[str], optional): The masks for the instance. Defaults to None.
            avatar (str, optional): The avatar for the instance. Defaults to None.
            display_name (str, optional): The display name for the instance. Defaults to None.
            group (str, optional): The group for the instance. Defaults to None.
        """
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
    """
    Starts the web driver and navigates to the Google homepage.

    Returns:
        driver (WebDriver): The initialized WebDriver object.
    """
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
    """
    Logs in to the forum using the provided credentials.

    Args:
        forum (Forum): The forum object representing the forum to log in to.
        user (User): The user object representing the user to log in as.
        admin (bool, optional): A flag indicating whether to log in to the Admin CP.
            Defaults to False.

    Returns:
        None
    """
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
    """
    Navigates to a specific forum in the provided Forum object.

    Args:
        forum (Forum): The Forum object containing the necessary driver and URL.
        forum_id (int): The ID of the forum to navigate to.

    Returns:
        None
    """
    driver = forum.driver
    url = forum.url + '/forum.asp?forumid=' + str(forum_id)
    driver.get(url)


def make_thread(forum: Forum, forum_id: int, thread_title: str, post_content: str, thread_description: str = "",
                locked: bool = False,
                pinned: bool = False,
                poll: bool = False, poll_question: str = "", poll_options: [str] = None, poll_num_of_options: int = 0,
                poll_num_of_votes: int = 0):
    """
    Creates a new thread in the specified forum with the given parameters.

    Args:
        forum (Forum): The forum object representing the forum where the thread will be created.
        forum_id (int): The ID of the forum where the thread will be created.
        thread_title (str): The title of the new thread.
        post_content (str): The content of the initial post in the thread.
        thread_description (str, optional): The description of the new thread (default: "").
        locked (bool, optional): Whether the new thread should be locked (default: False).
        pinned (bool, optional): Whether the new thread should be pinned (default: False).
        poll (bool, optional): Whether the new thread should have a poll (default: False).
        poll_question (str, optional): The question for the poll (default: "").
        poll_options (list[str], optional): The options for the poll (default: None).
        poll_num_of_options (int, optional): The number of options for the poll (default: 0).
        poll_num_of_votes (int, optional): The number of votes for the poll (default: 0).

    TODO: set up polls
    """
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
    """
    Make a post on a forum.

    Args:
        forum: The forum object.
        post_content: The content of the post.
        thread_id: (optional) The ID of the thread to post in. If left blank, it will attempt to
            post on the current page.

    Returns:
        None

    Note:
        The thread URL is constructed using the forum subdomain and the thread ID.
    """
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

def goto_admin_cp(forum):
    if '/Admin/admincp.asp' not in forum.driver.current_url:
        login(forum, forum.bot, admin=True)


def navigate_masks(forum: Forum):
    """
    Navigates to the mask page on the specified forum.

    Args:
        forum (Forum): The name of the forum to navigate to.

    Returns:
        None
    """
    goto_admin_cp(forum)
    driver = forum.driver
    mask_page = driver.find_element(By.LINK_TEXT, "Forum Masks")
    mask_page.send_keys(Keys.ENTER)
    iframe = driver.find_elements(By.TAG_NAME, 'iframe')[0]
    driver.switch_to.frame(iframe)


def create_mask(forum, mask_name, dictionary):
    """
    Create a mask in the forum.

    Args:
        forum (Forum): The forum object.
        mask_name (str): The name of the mask to be created.
        dictionary (dict): A dictionary containing the mask values.

    Returns:
        None
    """
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
    """
    Edits a mask on the forum.

    Parameters:
        forum (Forum): The forum object.
        mask_name (str): The name of the mask to edit.
        dictionary (dict): A dictionary containing the forum titles as keys and the desired permissions as values.
            Each value is a string containing the characters v, r, and/or c.
            V = View
            R = Reply
            C = Create Thread
            If a character appears in the string, that permission will be granted.
            e.g. "vr" will grant "View" and "Reply" permissions, but not "Create Thread."
            A blank string will grant no permissions.
        overwrite (bool, optional): Whether to overwrite and remove existing permissions not specified by the dictionary keys.
            If set to True, this is equivalent to setting all other permissions as blank/not allowed for any forum not specified in the dictionary.
            Defaults to False.
    """
    # from masks page, locate and click edit button
    driver = forum.driver
    # TODO: check if on mask page
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
    """
    Navigates to the "Word Filters" page in the Admin CP.

    Args:
        forum: The forum object.

    Returns:
        None
    """
    goto_admin_cp(forum)
    driver = forum.driver
    filter_page = driver.find_element(By.LINK_TEXT, "Word Filters")
    filter_page.send_keys(Keys.ENTER)
    iframe = driver.find_elements(By.TAG_NAME, 'iframe')[0]
    driver.switch_to.frame(iframe)


def add_filter(word_to_change, new_word, forum, mode=0):
    """
    Adds a filter to the forum's settings.

    Parameters:
        word_to_change (str): The word to be changed by the filter.
        new_word (str): The new word that will replace the old word in the filter.
        forum (Forum): The forum object representing the forum to add the filter to.
        mode (int, optional): The mode of the filter. 0 for Full Word Only, 1 for Containing Word.
            Defaults to 0.

    Returns:
        None
    """
    goto_admin_cp(forum)
    driver = forum.driver
    if "filters.asp" not in driver.current_url:
        navigate_edit_filters(forum)
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


def add_filters(filter_dictionary: dict, forum: Forum, mode: int=0):
    """
    Adds filters to a forum based on a filter dictionary.

    Args:
        filter_dictionary (dict): A dictionary containing filter keys (original word) and values (new word).
        forum (Forum): The forum object where the filters will be added.
        mode (int, optional): The mode of the filter. Defaults to 0.

    Returns:
        None
    """
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
