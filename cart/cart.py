
from django.conf import settings
from shop.models import Product, ProductSizes

flag = False

class Cart:
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
            
        self.cart = cart
        
    # add to cart
    def add(self,product,size_,quantity=1,override_quantity=False):
        size_id = str(size_.id)
        if size_id not in self.cart:
            if size_.price:
                self.cart[size_id] = {'quantity': 0, 'price': size_.price}
            elif size_.off_price:
                self.cart[size_id] = {'quantity': 0, 'price': size_.off_price}

        self.cart[size_id]['quantity'] += quantity
        self.save()
  

        self.save()
    
    def save(self):
        self.session.modified = True
    
    #remove from cart
    def remove(self,size_):
        product_id = str(size_.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        sizes_ids = self.cart.keys()
        products = ProductSizes.objects.filter(id__in=sizes_ids)
        
        cart = self.cart.copy()
        for size in products:
            cart[str(size.id)]['size'] = size
        
        for item in cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())
        
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
        

