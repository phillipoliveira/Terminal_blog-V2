from database import Database
from models.users import Users
from models.blog import Blog
import hashlib

class Menu(object):
    def __init__(self):
        # Ask user for author name
        # Check if they have an account
        # If not, prompt them to create one
        account_prompt = input("Do you have an account? (Y or N)")
        self.user = None
        if account_prompt.upper() == "Y":
            self.login()
        else:
            self.create_user()
        self.user_blog = None
        if self._user_has_blog():
            print("Welcome back {}".format(self.user))
        else:
            self._prompt_user_for_account()
        # An underscore before a method name denotes that
        # it's a private method. This means that only functions
        # in Menu class should be using this method. Python doesn't
        # enforce this, but it's bad practice.

    def login(self):
        count = 0
        while all([(count < 4),(self.user == None)]) :
            username = input("Enter your username: ")
            str_password = input("Enter your password: ")
            password_hash = hashlib.sha256(str_password.encode()).hexdigest()
            if Users.check_creditentials(username,password_hash) != None:
                print("Login successful! {}!".format(username))
                self.user = username
            else:
                print("Please try again!")
        else:
            if self.user == None:
                self.create_user()

    def create_user(self):
        username = input("Please enter a username: ")
        str_password = input("Enter your password: ")
        password_hash = hashlib.sha256(str_password.encode()).hexdigest()
        user = Users(username)
        user.save_user_to_mongo(password_hash)
        self.user = username

    def _user_has_blog(self):
        blog = Database.find_one(collection='blogs',query={'author':self.user})
        if blog is not None:
            self.user_blog = Blog.from_mongo(blog['id'])
            return True
        else:
            return False
        # This will return a true or false value, indicating whether or not the user has a blog

    def _prompt_user_for_account(self):
        title = input("Enter your blog title: ")
        description = input("Enter your blog description: ")
        blog = Blog(self.user,
                    title,
                    description)
        blog.save_to_mongo()
        self.user_blog = blog

    def run_menu(self):
        # User read or write blogs?
        read_or_write = input("Do you want to read (R) or write (W) blogs, or quit? (Q)? ")
        if read_or_write.upper() == "R":
            self._list_blogs()
            self._view_blogs()
            self.run_menu()
            pass
        elif read_or_write.upper() == "W":
            self.user_blog.new_post()
            self.run_menu()
            pass
        else:
            print("Thank you for blogging! ")
        pass

    def _list_blogs(self):
        blogs = Database.find(collection='blogs', query={})
        for blog in blogs:
            print("ID: {}, Title: {}, Author: {}".format(blog['id'],blog['title'],blog['author']))

    def _view_blogs(self):
        blog_to_see = input("Enter the ID of the blog you'd like to read: ")
        blog = Blog.from_mongo(blog_to_see)
        if blog == None:
            print("Please enter a valid blog ID!")
            _view_blogs()
        else:
            posts = blog.get_posts()
            for post in posts:
                print("Date: {}, Title: {}\n\n{}".format(post['created_date'], post['title'], post['content']))