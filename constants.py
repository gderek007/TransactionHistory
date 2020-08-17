#input stuff to their categories, 
# ideally this is automated but the bank descriptions arent the best, 
# might be an api somehwere out there to automate this
FOOD = set()
ONLINE_PURCHASES = set()
TAKE_CARE = set()
CONCERTS = set()
TRANSPORTATION = set()
#stuff to exclude incomes in csv 
# or other things that you dont want to include
BANNED = set()

a = [FOOD, ONLINE_PURCHASES, TAKE_CARE, TRANSPORTATION, CONCERTS]
PURCHASE_TYPES = {'Food':a[0],'Online Purchase':a[1],'Take Care':a[2], 'Transportation':a[3],'Concerts':a[4]}
