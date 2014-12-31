#! /usr/bin/python
# vim: et sw=2 ts=2 sts=2
from advent import *
# for cloud9...
from advent import Game, World, Location, Connection, Thing, Animal, Robot, Pet, Hero
from advent import NORTH, SOUTH, EAST, WEST, UP, DOWN, RIGHT, LEFT, IN, OUT, FORWARD, BACK, NORTH_WEST, NORTH_EAST, SOUTH_WEST, SOUTH_EAST, NOT_DIRECTION

# setup the game you are going to build on...
my_game = Game()

# create your world, then we can stick stuff in it
my_world = World()

# create some interesting locations. Locations need a name, 
# and a description of any doorways or connections to the room, like this:
# variable_name = Location('The Name", "The description")
sidewalk = Location(
"Sidewalk", """
There is a large glass door to the east.
The sign says 'Come In!'
""" )

vestibule = Location(
"Vestibule", """
A small area at the bottom of a flight of stairs.
Up the stars you see the reception desk.
""" )

reception = Location( "Reception Desk",
"""Behind an opening in the wall you see an unlit room.
There is a locked sliding door to the south, and an intersection to the north.
""" )

intersection = Location( "Intersection",
"""A boring intersection. There is a passageway to the
north that leads to the shop. To the east is the elevator
landing, to the west is the guest lounge, and to the
south is the reception desk. There is nothing to do here.
""" )

elevator = Location( "Elevator",
"""The elevator is turned off, but the door is open.
The controls on the elevator do not seem to work.
To the west is an intersection.
""" )

secret_lab = Location("Secret Labratory", "This place is spooky. It's dark and \nthere are cobwebs everywhere. There must \nbe a lightswitch somewhere.")

# let's add the locations to your world
my_world.add_location(sidewalk)
my_world.add_location(vestibule)
my_world.add_location(reception)
my_world.add_location(intersection)
my_world.add_location(elevator)
my_world.add_location(secret_lab)


# create connections between the different places. each connection needs 
# a name, the two locations to connect, and the two directions you can go to get into and out of the space
# like this: variable = Connection("The Connection Name", location_a, location_b, direction_a, direction_b)
# you can have more than one way of using a connection by combining them in an array
# like this: new_connection = Connection("The Connection Name", location_a, location_b, [direction_a, other_direction_a], [direction_b, other_direction_b])
big_door = Connection("Big Door", sidewalk, vestibule, [IN, EAST], [WEST, OUT])
stairs = Connection("Stairs", vestibule, reception, UP, DOWN)
steps_to_reception = Connection("A Few Steps", reception, intersection, NORTH, SOUTH)
steps_to_elevator = Connection("A Few Steps", intersection, elevator, EAST, WEST)

# now add the connections to the world too
my_world.add_connection(big_door)
my_world.add_connection(stairs)
my_world.add_connection(steps_to_reception)
my_world.add_connection(steps_to_elevator)


# create some things to put in your world. You need a name and 
# a description for the thing you are making
# something = Thing("Think Name", "A description for the thing")
# if you add True as the last argument, then its an item that cant be taken
elev_key = Thing( "key", "small tarnished brass key" )

sidewalk.put( elev_key )

pebble = sidewalk.put( Thing( "pebble", "round pebble" ) )
sidewalk.put( Thing( "Gary the garden gnome",
                          "a small figure liberated from a nearby garden." ) )
                          


# you can make rooms require things, like keys, before a player can enter them
elevator.add_requirement(elev_key)
elevator.add_requirement(pebble)

# simple verb applicable at this location
sidewalk.add_verb( 'knock', my_game.say('The door makes a hollow sound.') )

# custom single location verb
def scream( location, words ):
  print "You scream your head off!"
  for w in words[1:]:
    print "You scream '%s'." % w
  return True

sidewalk.add_verb( 'scream', scream )

# Add an animal to roam around.  Animals act autonomously
cat = Animal(my_world, "cat")
cat.set_location(sidewalk)
cat.add_verb("pet", my_game.say("The cat purrs.") )
cat.add_verb("eat", my_game.say_on_noun("cat", "Don't do that, PETA will get you!"));
cat.add_verb("kill", my_game.say_on_noun("cat", "The cat escapes and bites you. Ouch!"));

# Add a robot.  Robots can take commands to perform actions.
robby = Robot( my_world, "Robby" )
robby.set_location( sidewalk )

# Add a Pet.  Pets are like Animals because they can act autonomously,
# but they also are like Robots in that they can take commands to
# perform actions.
fido = Pet ( my_world, "Fido")
fido.set_location( sidewalk )

# make the player
hero = Hero(my_world)

# add a hero verb
def throw( self, actor, words ):
  if len(words) > 1 and self.act('drop', words[1] ):
     print 'The %s bounces and falls to the floor' % words[1]
     return True
  else:
     print 'You hurt your arm.'
     return False

hero.add_verb( "throw", throw )

# create shared data
# NOTE: you must either set the server with share.set_host(...) or place the host information
# in a file 'share.info' in the local directory.  The host must be a webdis host using basic
# authentication.
share = Share()
share.set_game("bwx-adventure")
share.set_player("default")
share.start()

# custom verb to record things at locations
def scribble( self, actor, words ):
  if len(words) != 2:
    print "You can only scrible a single word."
    return False
  share.put_game_data('crumb.' + self.location.name, words[1].strip())
  return True

hero.add_verb( "scribble", scribble )

# custom verb to see things written
def peek( self, actor, words ):
  print 'Someone scribbled "%s" here.' % share.get_game_data('crumb.' + self.location.name)
  return True

hero.add_verb( "peek", peek )

# start on the sidewalk
hero.set_location( sidewalk )

# start playing
my_game.run(hero)
