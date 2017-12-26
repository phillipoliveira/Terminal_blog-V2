from models.post import Post
from models.blog import Blog
from menu import Menu
from database import Database

Database.initialize()

menu = Menu()

menu.run_menu()