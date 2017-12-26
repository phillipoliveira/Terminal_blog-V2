import uuid
import datetime
from database import Database
from models.post import Post

class Blog(object):
    def __init__(self, author, title, description, id=None):
        self.author = author
        self.title = title
        self.description = description
        self.id = uuid.uuid4().hex if id is None else id

    def new_post(self):
        title = input("Enter post title: ")
        content = input("Enter post content: ")
        date = input("Enter post date or leave blank for today (in format DDMMYYYY): ")
        try:
            date = datetime.datetime.strptime(date, "%d%m%Y")
        except ValueError:
            date = datetime.datetime.utcnow()
        post = Post(blog_id=self.id,
                    title=title,
                    content=content,
                    author=self.author,
                    date=date)
        post.save_to_mongo()
        # Author of the blog is the author of the posts,
        # id of the blog is automatically set as the post's
        # blog_id

    def get_posts(self):
         return Post.from_blog(self.id)

    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return {
            'author':self.author,
            'title':self.title,
            'description':self.description,
            'id':self.id
        }

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'id':id})
        return cls(author=blog_data['author'],
                    title=blog_data['title'],
                    description=blog_data['description'],
                    id=blog_data['id'])
    # We've written this this way, so that we can later run
    # methods on the blog object we've returned.
    # @classmethod allows us to use 'cls' to return the class
    # we're currently working with, in case the class name ever
    # changes.