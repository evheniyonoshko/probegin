* Backstory

Company decided to phase out old customer management system and introduce new python project
 which will take over control of DB and will allow extra information to be saved.

Old DB contains 2 tables:

--------
CUSTOMER
--------

lCustomer_id: int, primary key
cSearchName: textfield
cName: charfield 10
vEmailSender: charfield 255

-----------------
CUSTOMER_DISCOUNT
-----------------

intCustomerDiscountId: int, primary key
intCustomerId: int, reference to CUSTOMER
chvDescription: charfield 50
dtmInsertDate: datetime

Attached example DB.

Due to legacy software being heavily used we need to keep old database up to date, 
 however we're not allowed to change schema of old db.
Which means we need to create new DB and keep it in sync with old one.
 Luckily we can make new DB leading and do not have to bother about changes
 in old DB to be synchrozined to new db after initial sync.

* TODO:

 Create sample django application with will do following:

 - Define tables in new database,
 - Expose these tables via Admin interface, inlining Discounts for each customer
 - Will update old DB when data is added/updated to new DB
 - Management command to import all the data from old db into new one

Bonus point: tests.
