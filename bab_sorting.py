import sys
import csv
import pandas

LEADER_STRING_0 = "I go with the flow"
LEADER_STRING_1 = "I don't usually lead, but I'm comfortable speaking up and talking about my ideas"
LEADER_STRING_2 = "I usually take charge"


# CLASSES
######################################################
# A member in build-a-band
class bab_member:
    def __init__(self, name , instrument, genre, leader, availability, excelData):
        self.type = "member"
        self.name = name # string
        self.instrument = set(instrument.replace(' ', '').split(',')) # instrument
        
        # possible roles they can fill, based on instrument
        self.roles = set()
        if ('Drums' in self.instrument):
            self.roles.add("Drums")

        if ('Bass' in self.instrument):
            self.roles.add("Bass")

        if (('AcousticGuitar' in self.instrument) or \
            ('ElectricGuitar' in self.instrument) or \
            ('Piano' in self.instrument)):
            self.roles.add("Rhythm")

        if (('AcousticGuitar' in self.instrument) or \
            ('ElectricGuitar' in self.instrument) or \
            ('Piano' in self.instrument) or \
            ('ElectricGuitar' in self.instrument) or \
            ('Voice' in self.instrument)):
            self.roles.add("Melody")

        self.genre = set(genre.replace(' ', '').split(',')) # array

        if (leader == LEADER_STRING_0): self.leader = 0
        if (leader == LEADER_STRING_1): self.leader = 1
        if (leader == LEADER_STRING_2): self.leader = 2

        self.availability = availability
        self.placed = False # whether or not they have been placed for the given iteration
        self.compatibilityScore = -1 # Compatiblitiy score
        self.mostCompatible = 0 # Highest compatibility member OR group
        self.groups = []

        # EXCEL DATA
        self.excelData = []
        for line in excelData:
            self.excelData.append(line)

    def display(self):
        print("name: ", self.name, "\ninstrument: ", self.
              instrument, "\ngenre: ", self.genre, '\navailability: ', self.availability, '\n')
        
    def get_compatibility(self, member):
        crossover = list(self.genre & member.genre)
        print("Compatible genres: ", crossover, "\nCount: ", len(crossover), "\n")

        
    def display_compatiblity(self):
        print("Compatibility: ", self.compatiblity)
        
# A group / band formed by members
class bab_group:
    def __init__(self, name):
        self.type = "group"
        self.name = name
        self.drums = False #drums only
        self.bass = False #bass only
        self.rhythm = False # guitar, keyboard
        self.melody = False # guitar, keyboard, vocals
        self.etc = False # whatever else
        self.members = []
        self.full = False

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
        if len(self.members) == 4: self.full = True

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
        display_string = self.name + "\nDrums:  "
        if (self.drums): display_string += self.drums.name
        else: display_string += "Empty"
        display_string += "\nBass:   "

        if (self.bass): display_string += self.bass.name
        else: display_string += "Empty"
        display_string += "\nRhythm: "

        if (self.rhythm): display_string += self.rhythm.name
        else: display_string += "Empty"
        display_string += "\nMelody: "
        if (self.melody): display_string += self.melody.name
        else: display_string += "Empty"
        display_string += "\n"
        print(display_string)
        #print(self.name, "\nDrums: ", self.drums.name, "\nBass: ", self.bass.name, "\nRhythm: ", self.rhythm.name, "\nMelody: ", self.melody.name, "\n")

    def count(self):
        return len(self.members)
    
    # returns compatibility of this group with the current member
    # return < 0 for compatibiltiy score
    # return -1 for non-compatible ie. overlapping role etc
    def check_compatibility(self, member):
        # First check if this member has a role that we have not filled yet
        # If none of these roles are avialable, return -1 false
        if (self.full == True or member in self.members): return -1

        if not ((self.drums  == False) & ('Drums'  in member.roles) or \
                (self.bass   == False) & ('Bass'   in member.roles) or \
                (self.rhythm == False) & ('Rhythm' in member.roles) or \
                (self.melody == False) & ('Melody' in member.roles) ):
            return -1
        
        # otherwise compare compatibility
        compatiblity = 0
        for group_member in self.members:
            compatiblity += (len(list(member.genre & group_member.genre)))

        return compatiblity


    
# EXTERNAL FUNCTIONS
######################################################
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

def calculate_compatibility(member_list, group_list):
    for member in member_list:
        member.compatibilityScore = -1
        # print(member.name)
        #member.display()

        # skip if availability is 0
        if (member.availability == 0 or member.placed == True):
            continue

        else: find_most_compatible(member, member_list, group_list)

        add_instrument_compatibility(member)
        #print("MOST COMPATIBLE MEMBER / GROUP: " + member.mostCompatible.name + " SCORE:" + str(member.compatibilityScore))

# Updates this member's compatiblity_list
def find_most_compatible(member, member_list, group_list):
    # find max compatiblity
    # do members list first
    # Member list ie. making new groups is only available as long as we are below the max number of possible grousp
    for compatible_member in member_list:
        if (compatible_member == member or compatible_member.availability == 0): continue

        compatiblity = (len(list(member.genre & compatible_member.genre)))
        
        # If this current compatible member has a higher compatiblity,
        # replace the mostCompatible member and update compatiblitiy score
        if (compatiblity > member.compatibilityScore):
            # check whether or not it is possible to form a group with this person
            # only cases would be if they only have one role and both fufill the same one
            if ((len(member.roles) == 1 and len(compatible_member.roles) == 1) & (list(member.roles)[0] == list(compatible_member.roles)[0])):
                #print("SAME ROLE!!!")
                continue

            member.mostCompatible = compatible_member
            member.compatibilityScore = compatiblity

        # equal compatiblity, tie breaker check here (instrument priority)
        # Tie breaker
        elif (compatiblity == member.compatibilityScore):
            # check if both players are leaders 
            # check if either player plays a drums / rhythm instrument
            # re-calculate compatiblity score based on this (gives higher priority as well)

            # higher priority instrument checking
            # put drums and bass together as higher priority
            if   ("Drums" in member.roles and "Bass" in compatible_member.roles) or \
                 ("Bass" in member.roles and "Drums" in compatible_member.roles): compatiblity += 2 
            
            # higher priority leadership checking
            if (member.leader == 2 and compatible_member.leader == 0) or \
               (compatible_member.leader == 2 and member.leader == 0): compatiblity += 1            

            if (compatiblity > member.compatibilityScore): 
                #rint("Tie breaker successful")
                member.mostCompatible = compatible_member
                member.compatibilityScore = compatiblity


    for compatible_group in group_list:
        #print("Checking member " + member.name + "Compatibility with  group" + compatible_group.name)
        compatiblity = compatible_group.check_compatibility(member)
        #print("Compatibility: " + str(compatiblity))
        if (compatiblity == -1): continue

        # If this current compatible member has a higher compatiblity,
        # replace the mostCompatible member and update compatiblitiy score
        if (compatiblity > member.compatibilityScore):
            # check whether or not it is possible to form a group with this person
            # only cases would be if they only have one role and both fufill the same one
            member.mostCompatible = compatible_group
            member.compatibilityScore = compatiblity

        # equal compatiblity, tie breaker check here (instrument priority)
        # Tie breaker
        elif (compatiblity == member.compatibilityScore):
            #print("SAME COMPATIBILTIY SCORE FOR GROUP: " + compatible_group.name)
            if (compatible_group.drums  == False) & ('Drums'  in member.roles): compatiblity += 2
            elif (compatible_group.bass  == False) & ('Bass'  in member.roles): compatiblity += 1
            
            if (compatiblity > member.compatibilityScore):
                #print("Tie breaker successful")
                # check whether or not it is possible to form a group with this person
                # only cases would be if they only have one role and both fufill the same one
                member.mostCompatible = compatible_group
                member.compatibilityScore = compatiblity


# sorts the member list based on highest compatibility score
def sort_memberlist_by_compatibility(member_list):
    member_list.sort(reverse = True, key=lambda x: x.compatibilityScore)

# Assigns member with highest compatibility group or person
# if member.mostCompatible is a person, form a new group
# if member.mostCompatible is a group, add them to it
def place_member(member, group_list):
    print("Member: " + member.name + " Member compatibility: " + member.mostCompatible.name + "\nType:" + member.mostCompatible.type + " Score: " + str(member.compatibilityScore) + " Availability: " + str(member.availability))
    # if the most compatible person is a member, form a new group
    if (member.mostCompatible.type == "member"):
        group_id = len(group_list)
        # try making new group with member
        new_group = bab_group("BAB" + str(group_id))
        print("CREATED NEW GROUP: " + new_group.name)

        new_group.add_member(member)
        new_group.add_member(member.mostCompatible)
        register_to_group(member, new_group)
        register_to_group(member.mostCompatible, new_group)
        group_list.append(new_group)
        member.mostCompatible.placed = True

    # if the most compatible person is a group, add this person to the group
    elif (member.mostCompatible.type == "group"):
        group = member.mostCompatible
        print("ADDED MEMBER TO GROUP: " + group.name)
        group.add_member(member)
        register_to_group(member, group)

    member.placed = True

# Tie breaker compatibility point calculation for people with the highest scores
# Additional points based on number of roles for higher priority assignment
# 1 role = +3, 2 roles = +2, 3 roles = +1, 4 roles = 0
def add_instrument_compatibility(member):
    if (len(member.roles) == 1): member.compatibilityScore += 3
    elif (len(member.roles) == 2): member.compatibilityScore += 2
    elif (len(member.roles) == 3): member.compatibilityScore += 1

# Algorithm / loop logic 
######################################################

# checks and returns if there are still members who have not been placed
# return True if all members are placed
# returns False if there are still members who need to be placed
def all_members_are_placed(member_list):
        for member in member_list:
            if member.placed == False: 
                return False

        return True

def members_have_availability(member_list):
        for member in member_list:
            if member.availability > 0: 
                return True

        return False

def refresh_placement(member_list):
    for member in member_list:
        # Reset placement only if member still has availability
        if (member.availability > 0): member.placed = False 

def main():

    
    member_list = []
    group_list = []

    # sorting alg
    # creating a number of groups based on avaliablity of drummers 
    # add bass based on highest genre overlap
    # add melody, prioritizing vocalists 
    # add rhythm, guitar / piano / whatever
    # also prioritize in terms of how many bands you're in


    # create our membber list
    
    print(len(sys.argv))
    if (len (sys.argv) != 2): 
        print("NO FORM RESPONSE ARGUMENT PROVIDED TO SCRIPT. Re-rerunscript using python3 bab_sorting.py form_responses.csv")
        return -1
    
    FILE_NAME = sys.argv[1]

    with open(FILE_NAME, mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            if (lines[0] == "Timestamp"): continue
            member_list.append(bab_member(lines[1], lines[2], lines[3], lines[4], int(lines[8]), lines))
            #print(lines) 
            #print("\n")


    # set the upper bound of members
    max_groups = 0
    for member in member_list:
        max_groups += member.availability

    max_groups /= 4
    # TODO: implement this limit

    # when making a new BAB group, we will check whether or not we have reached the upper bound of groups (Maybe)
    # ie. this will take place in the compatiblity function calculation, ie. members will no longer show up as possible new group forms if
    # the current size of groups is larger than our upper bound


    while (members_have_availability(member_list)):
        while (not all_members_are_placed(member_list)):
            calculate_compatibility(member_list, group_list)
            sort_memberlist_by_compatibility(member_list)
            place_member(member_list[0], group_list)
        refresh_placement(member_list)
        
    
    print("DONE!")

    for group in group_list:
        dataArray = []
        #dataArray = [[0]*len(group.members)]*len(member_list[0].excelData)
        group.display()
        for member in group.members:
            dataArray.append(member.excelData)

        df1 = pandas.DataFrame(data for data in dataArray)

        with pandas.ExcelWriter('BABgroups.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df1.to_excel(writer, sheet_name=group.name)


if __name__ == "__main__":
    main()
