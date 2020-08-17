import constants as  c
import csv
import matplotlib.pyplot as plt

FOOD = c.FOOD
ONLINE_PURCHASES = c.ONLINE_PURCHASES
TAKE_CARE = c.TAKE_CARE
CONCERTS = c.CONCERTS
BANNED = c.BANNED
PURCHASE_TYPES = c.PURCHASE_TYPES
file_names = ['2020_CREDIT','2020_DEBIT','Discover_CREDIT','Amazon_CREDIT','Big_Venmo']

class Transaction():
    def __init__(self, card_type, date, title, location, amount,card_name):
        self.card_type = card_type
        self.amount = abs(amount)
        self.date = date
        self.title = title
        self.location = location
        self.purchase_type = self.type_purchase()
        self.card_name = card_name

    def __str__(self):
        return str(self.date) + ', ' + self.title + ', ' + self.purchase_type + ', ' + str(self.amount) +', ' + str(self.card_name)  
        
    def type_purchase(self):
        def helper(name):
            for key in PURCHASE_TYPES.keys():
                for thing in PURCHASE_TYPES[key]:
                    if thing in name:
                        return key 
            return 'Miscellaneous'

        if 'uber' in self.title.lower() or 'lyft' in self.title.lower():
            return 'Ride Share'

        else:
            return helper(self.title)
class Card():
    def __init__(self, file_name):
        self.name = file_name +'.csv'
        self.card_type = 'Credit' if 'CREDIT' in self.name else 'Debit'
        self.card_type = 'Venmo' if 'Venmo' in self.name else self.card_type
        self.types_set = {'Food','Transportation','Take Care','Online Purchase','Miscellaneous','Ride Share','Concerts'}
        self.types_dict = {'Concerts':[], 'Food': [], 'Miscellaneous':[], 'Online Purchase': [], 'Miscellaneous':[], 'Ride Share':[], 'Transportation': [], 'Take Care': []}
        #implement dates at the class level
        self.types_dict_dates = {month : [] for month in range(1,13)}
        self.types_amount = {category : 0 for category in self.types_set}

    def getTotal(self):
        '''Csv part'''
        TOTAL = 0
        list_transaction = []

        with open (self.name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            for row in csv_reader:
                if self.card_type == 'Debit':
                    if row[1] not in BANNED:
                        list_transaction.append(Transaction(self.card_type, row[0], row[1].lower(), self.card_type, float(row[2]), self.name))

                elif self.card_type  == 'Credit':
                    if 'Online payment' not in row[2] :
                        list_transaction.append(Transaction(self.card_type, row[0], row[2].lower(), row[3], float(row[4]), self.name))
                
                else:
                    if row[1] != 'Standard Transfer':
                        TOTAL+=float(row[5])
                    
        if self.card_type == 'Venmo':
            print(round(TOTAL,3))
            exit()

        for i in list_transaction:
            # a = i.date.split('/')[0]
            # types_dict_dates[a].append(i)
            self.types_dict[i.purchase_type].append(i)
            self.types_amount[i.purchase_type]+= i.amount
            TOTAL += i.amount

        percentages = { i : 0 if TOTAL == 0 else round(self.types_amount[i]/TOTAL,2) for i in self.types_amount }
        return TOTAL

    def plot(self, TOTAL):
        # Data to plot
        sizes, label = [], []
        for j in self.types_set:
            money_spent = self.types_amount[j]
            if abs(money_spent) != 0:
                sizes.append(round(abs(money_spent),3))
                label.append(j)

        #add more colrs for more categories
        colors = ['gold', 'brown', 'pink', 'lightskyblue','red','purple','blue']
        max = len(colors)

        if len(sizes) == max:
            explode = (0,) * max
        else:
            new_colors = []
            for j in range(len(sizes)):
                new_colors.append(colors[j])
                explode = (0,)*len(sizes) # explode 1st slice
            colors = new_colors
        # Plot
        plt.pie(sizes, explode=explode, labels=label, colors=colors,
        autopct='%1.1f%%', shadow=False, startangle=140)
        patches, texts = plt.pie(sizes, colors=colors, shadow=False, startangle=140)
        plt.legend(patches, sizes, loc = "upper left")
        plt.text(1, -.9, self.name)
        plt.text(1, -1, 'total for: ' + str(round(abs(TOTAL),3)))
        plt.axis('equal')
        plt.show()
class Total(Card):
    def __init__(self, list_total):
        self.list = [ Card(i) for i in list_total ]

    def plotall(self, together = True):
        all_cards = Card('ALLCards')       
        total = 0
        for card in self.list:
            t = card.getTotal()
            total += t
            if together:
                for key in card.types_amount.keys():
                    all_cards.types_amount[key] += card.types_amount[key]
            else:
                card.plot(t)
        if together:
            all_cards.plot(total)
        print(total)

a = Total(file_names[:4])
a.plotall(False)