import csv
import heapq

FILE_NAME = "form_responses.csv"

class bab_member:
    def __init__(self, name , instrument, genre, availability):
        self.name = name # string
        self.instrument = set(instrument.replace(' ', '').split(',')) # instrument
        self.genre = set(genre.replace(' ', '').split(',')) # array
        self.availability = availability
        self.compatiblity = {}
        self.groups = []

    def display(self):
        print("name: ", self.name, "\ninstrument: ", self.
              instrument, "\ngenre: ", self.genre, '\navailability: ', self.availability, '\n')
        
    def get_compatibility(self, member):
        crossover = list(self.genre & member.genre)
        print("Compatible genres: ", crossover, "\nCount: ", len(crossover), "\n")

        
    def display_compatiblity(self):
        print("Compatibility: ", self.compatiblity)
        
class bab_group:
    def __init__(self, name):
        self.name = name
        self.drums = False #drums only
        self.bass = False #bass only
        self.rhythm = False # guitar, keyboard
        self.melody = False # guitar, keyboard, vocals
        self.etc = False # whatever else
        self.members = []

    # add a member to the group
    # returns true if member successfully added
    # returns false if role is not available
    def add_member(self, member):
        add_flag = False

        # check if member can be added preliminarily
        # member must: 
        # have availability
        # not already be a member of the band
        if (member.availability == 0) or \
            (member in self.members): return False

        if ((self.drums == False) & ('Drums' in member.instrument)):
            self.drums = member
            add_flag = True
        elif ((self.bass == False) & ('Bass' in member.instrument)):
            self.bass = member
            add_flag = True
        elif ((self.rhythm == False) & ( \
            ('AcousticGuitar' in member.instrument) or \
            ('ElectricGuitar' in member.instrument) or \
            ('Piano' in member.instrument))):
            self.rhythm = member
            add_flag = True
        elif ((self.melody == False) & ( \
            ('AcousticGuitar' in member.instrument) or \
            ('ElectricGuitar' in member.instrument) or \
            ('Piano' in member.instrument) or \
            ('ElectricGuitar' in member.instrument) or \
            ('Voice' in member.instrument))):
            self.melody = member
            add_flag = True

        if (add_flag):
            return True
        
        return False
    
    # register a member in the group
    def register(self, member): 
        self.members.append(member)
        member.availability = member.availability - 1
        member.groups.append(self)

    # get compatilbilty in the group based on similar genres
    def get_compatiblity(self):
        crossover = self.members[0].genre & self.members[1].genre
        for count, member in enumerate(self.members):
            crossover & member.genre
            
        #crossover = list(self.members[0].genre & self.members[1].genre & self.members[2].genre & self.members[3].genre)
        print("Compatible genres: ", crossover, "\nCount: ", len(crossover), "\n")

    def genre(self):
        crossover = self.members[0].genre & self.members[1].genre
        for count, member in enumerate(self.members):
            crossover & member.genre
        return crossover



    def display(self):
        display_string = self.name + "\nDrums: "
        if (self.drums): display_string += self.drums.name + "\nBass: "
        else: display_string += "Empty\n"
        if (self.bass): display_string += self.bass.name + "\nRhythm: "
        else: display_string += "Empty\n"
        if (self.rhythm): display_string += self.rhythm.name + "\nMelody: "
        else: display_string += "Empty\n"
        if (self.melody): display_string += self.melody.name + "\n"
        else: display_string += "Empty\n"
        print(display_string)
        #print(self.name, "\nDrums: ", self.drums.name, "\nBass: ", self.bass.name, "\nRhythm: ", self.rhythm.name, "\nMelody: ", self.melody.name, "\n")

    def count(self):
        return len(self.members)
    
def register_to_group(member, group):
    group.members.append(member)
    member.availability = member.availability - 1
    member.groups.append(group)

def create_compatibility_list(member_list):
    for member in member_list:
        #member.display()

        # Compare members based on compatibility
        # -----------------------------------------------------------
        for id, compatible_member in enumerate(member_list):
            # if this is the same member, skip
            if member.name != compatible_member.name:
                member.compatiblity[id] = (len(list(member.genre & compatible_member.genre)))

        # sort the compatiblity dictionary members based on highest compatibility
        member.compatibility = dict(sorted(member.compatiblity.items(), key=lambda item:item[1], reverse=True))

def main():

    
    member_list = []
    bab_groups = []
    group_id = 0

    # sorting alg
    # creating a number of groups based on avaliablity of drummers 
    # add bass based on highest genre overlap
    # add melody, prioritizing vocalists 
    # add rhythm, guitar / piano / whatever
    # also prioritize in terms of how many bands you're in


    # create our member list
    with open(FILE_NAME, mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            member_list.append(bab_member(lines[1], lines[2], lines[3], int(lines[5])))
            #print(lines) 
            #print("\n")

    # sort member list alphabetically
    #member_list.sort(key=lambda x: x.name)


    # first find genre compatiblity between people
    create_compatibility_list(member_list)
            

        #print("Member: ", member.name, "is most compatible with member: ", member_list[list(member.compatibility.keys())[0]].name)


    #sort the member list based on member compatibility
    #print(member_list[0].compatibility[list(member_list[0].compatibility)[0]])
    #if you're reading this, I'm so sorry
    member_list.sort(key=lambda x: x.compatibility[list(x.compatibility)[0]])
    # for member in member_list:
    #     print(member.name)
    # return


    for member in member_list:
        # Place members into groups based on compatibility
        # -----------------------------------------------------------
        print("CREATING FOR MEMBER: ", member.name, '\n')
        print(member.compatibility)
        for member_id in sorted(member.compatiblity.items(), key=lambda item:item[1], reverse=True):
            member_id = member_id[0]
            print("MEMBER ID: ", member_id)
            print("COMPAITBILITY TEST WITH: ", member_list[member_id].name, '\n')
            print("MEMBER GROUSP:", member.groups)
            if (member_list[member_id] == member): continue

            # if compatible member is already in a group, try to add current member to it
            if len(member_list[member_id].groups) != 0:
                for group in member_list[member_id].groups:
                    if group.add_member(member): 
                        register_to_group(member, group)
                        break

            # compatible member is not in any groups; create new one
            else:
                # try making new group with member
                new_group = bab_group("BAB" + str(group_id))
                
                # add this member to the group
                if new_group.add_member(member) == False: print("CRITICAL ERROR")

                # try adding member to the group
                if (new_group.add_member(member_list[member_id])): 
                    print ("New group sucessfully created.")
                    register_to_group(member, new_group)
                    register_to_group(member_list[member_id], new_group)
                    bab_groups.append(new_group)
                    group_id = group_id + 1


            # if we were not able to add the member to an existing group, 
            if (len(member.groups) != 0): 
                print("Added member to group")
                break

            # create new group
     

        #for key in member.compatibility:
            #print(member.compatibility[key])
        # list whoever is most compatibile 
        # then die
            
    
    # fill in remaining groups with missing members
    for group in bab_groups:
        # create new compatiblity list based on non-member members members who need a team
        group.display()
        group.get_compatiblity()
                
    
    #for member in member_list:
        #find most compatible members in member list

        
        #print("most compatibile member: ", member_list[find_max(member.compatiblity, 1)].name)

            
        #member.display_compatiblity()









    # create preliminary groups using drummers as base
    # initially start with trying to fill one person into each group
    # only fill solo drummers in for multiple (DRUMS ONLY)
            
    # for member in member_list:
    #     if len(member.instrument) == 1 and 'Drums' in member.instrument:
    #         for group in member.availability:
    #             bab_groups.append(bab_group(member))

    # for group in bab_groups:
    #     group.display()



#Display overlap between members in genre preferences
        



#group sorting algorithm
#form each group starting with a drummer
    
if __name__ == "__main__":
    main()
