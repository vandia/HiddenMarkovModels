from kanren import Relation, facts
from kanren import run, var

class StarWars():

    def __init__(self):
        parents={"Luke Skywalker":"Darth Vader", "Leia Organa":"Darth Vader", "Kylo Ren": ['Han Solo','Leia Organa']}
        sons={"Darth Vader":["Luke Skywalker","Leia Organa"], "Leia Organa":"Kylo Ren", "Han Solo":"Kylo Ren"}
        grandparents={"Kylo Ren":"Darth Vader"}
        grandsons={"Darth Vader":"Kylo Ren"}
        self.relations={"parents":parents,"sons":sons,"granparents":grandparents,"grandsons":grandsons}

    def run(self,relation,x):
        r=self.relations[relation]
        if r!= None:
            return r[x]


def star_wars_imperative():
    sw=StarWars()
    print(sw.run("parents","Luke Skywalker"))
    print(sw.run("sons", "Darth Vader"))
    print(sw.run("granparents","Kylo Ren"))

def star_wars_logic():

    x = var()

    parent = Relation()
    facts(parent, ("Darth Vader", "Luke Skywalker"),("Darth Vader", "Leia Organa"),("Han Solo",  "Kylo Ren"),
          ("Leia Organa",  "Kylo Ren"))
    print(run(0, x, parent(x, "Luke Skywalker")))
    print(run(0, x, parent("Darth Vader", x)))

    grandparent=Relation()
    facts(grandparent,("Darth Vader", "Kylo Ren"))
    print(run(1, x, grandparent(x, "Kylo Ren")))





if __name__ == '__main__':
    star_wars_logic()
    star_wars_imperative()