from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
  user = models.OneToOneField(User, on_delete = models.CASCADE,  null  = True , blank = True)
  name = models.CharField(max_length = 200, null = True)
  email = models.CharField(max_length = 200, null = True)

  def __str__(self):
    return self.name

class Product(models.Model):
  name = models.CharField(max_length = 200, null = True)
  price = models.DecimalField(max_digits = 7, decimal_places = 2)
  digital = models.BooleanField(default = False, null = True, blank = False)
  image = models.ImageField(null = True, blank = True)

  def __str__(self):
    return self.name

  #incase the product does not have an image uploaded, render an empty string instead of not letting the store run
  @property
  def imageURL(self):
    try:
      url = self.image.url
    except :
      url  = ""
    return url 
  

class Order(models.Model):
  #By setting the customer to a foreign key, this enables the customer to continuosly add more product to the cart, creating a many to one relationship between the customer and the products. Also, if the customer decides to delete their account, nothing in the cart goes, hence why we assign the on_delete variable to models.SET_NULL
  customer = models.ForeignKey(Customer, on_delete = models.SET_NULL,  blank = True, null = True)
  date_ordered = models.DateTimeField(auto_now_add  =True)
  complete = models.BooleanField(default = False, null = True, blank = False)
  transaction_id = models.CharField(max_length = 200, null = True)

  def __str__(self):
    return str(self.id)

  @property
  def get_cart_total(self):
    orderitems = self.orderitem_set.all()
    total  =  sum([item.get_total for item in orderitems ])
    return total
  
  @property
  def get_cart_item(self):
    orderitems = self.orderitem_set.all()
    total  =  sum([item.quantity for item in orderitems ])
    return total

  @property
  def shipping(self):
    shipping = False
    orderitems = self.orderitem_set.all()
    for i in orderitems:
      if i.product.digital == False:
        shipping = True
    return shipping

class OrderItem(models.Model):
  #creating items that need to be added to our order with a many to one relationship
  #cart can have many products hence the many to one relationship
  product = models.ForeignKey(Product , on_delete = models.SET_NULL , null  = True)
  order = models.ForeignKey(Order, on_delete = models.SET_NULL , null = True)
  quantity = models.IntegerField(default = 0 , null = True , blank = True)
  date_added = models.DateTimeField(auto_now_add = True)

  @property
  def get_total(self):
    total = self.product.price * self.quantity
    return total



class ShippingAddress(models.Model):
  customer = models.ForeignKey(Customer, on_delete = models.SET_NULL,  blank = True, null = True)
  order = models.ForeignKey(Order, on_delete = models.SET_NULL,  blank = True, null = True)
  address = models.CharField(max_length = 200, null = True)
  city = models.CharField(max_length = 200, null = True)
  state = models.CharField(max_length = 200, null = True)
  postalcode = models.CharField(max_length = 200, null = True)
  country = models.CharField(max_length = 200, null = True)
  date_added = models.DateTimeField(auto_now_add = True)

  def __str__(self):
    return self.address
