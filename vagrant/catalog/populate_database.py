from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///itemcatalog.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
session = DBSession()

# Users
user1 = User(name="Priya Bala", email="priya.balakrishnan@gmail.com")
session.add(user1)
session.commit()

user2 = User(name="Pri B", email="pb@gmail.com")
session.add(user2)
session.commit()


# helper function to populate the database
# Items for TV Shows
category1 = Category(name="TV Shows")

session.add(category1)
session.commit()

Item1 = Item(title="Best Friends Whenever", description="Two teens who can ping pong \
             through the past, present and future are having the times of \
             their lives!",
             category=category1, user=user1)
session.add(Item1)
session.commit()

Item2 = Item(title="Bunk'd", description="The Ross siblings spend a summer \
             full of fun and adventure at Maine's Camp Kikiwaka, where \
             their parents first met.",
             category=category1, user=user1)
session.add(Item2)
session.commit()

Item3 = Item(title="We're Lalaloopsy", description="Laughter, creativity, caring and sharing: \
             these cuties are learning what friendship is all \
             about. They're Lalaloopsy!",
             category=category1, user=user2)
session.add(Item3)
session.commit()

category2 = Category(name="Action")

session.add(category2)
session.commit()

Item1 = Item(title="Ocean's Twelve", description="A jewel thief faces off against a \
             rival for the ultimate honor among thieves.",
             category=category2, user=user1)
session.add(Item1)
session.commit()

Item2 = Item(title="Marvel: Civi War", description="The greatest superhero team ever has been \
             split into two factions and their leaders aren't giving in. \
             This means war!", category=category2, user=user2)
session.add(Item2)
session.commit()

category3 = Category(name="Comedies")

session.add(category3)
session.commit()

Item1 = Item(title="Honey, I Shrunk the Kids", description="Four kids get an ant's-eye view \
             of the world, thanks to a wacky inventor's shrink ray.",
             category=category3, user=user2)
session.add(Item1)
session.commit()


category4 = Category(name="Children & Family")

session.add(category4)
session.commit()

Item1 = Item(title="Jungle Book", description="A bumbling bear and a shrewd panther make terrific \
             pals when you're a curious little boy in a dangerous jungle.",
             category=category4, user=user1)
session.add(Item1)
session.commit()

category5 = Category(name="Classics")

session.add(category5)
session.commit()

Item1 = Item(title="To Kill a Mockingbird", description="A valiant lawyer, a black man falsely accused. \
             Seen through the eyes of a feisty girl, innocence \
             and injustice collide.", category=category5, user=user1)
session.add(Item1)
session.commit()

category6 = Category(name="Documentaries")

session.add(category6)
session.commit()

Item1 = Item(title="The Eighties", description="The hair was big, the profits bigger \
             and MTV ruled the airwaves. This is one gnarly trip \
             down memory lane.", category=category6, user=user1)
session.add(Item1)
session.commit()

category7 = Category(name="Sci-Fi & Fantasy")

session.add(category7)
session.commit()
Item1 = Item(title="E.T.", description="He is not your typical alien invader. \
             In fact he couldn't be sweeter.",
             category=category7, user=user2)
session.add(Item1)
session.commit()
