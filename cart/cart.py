
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
            
        self.cart = cart
        
    # add to cart
    def add(self,product,size_,quantity=1,override_quantity=False):
        product_id = str(product.id)
        size_id = str(size_.id)
        print(product.size.name)
        if product_id not in self.cart  :
            if size_ != None:
                if  size_.off_price:
                    self.cart[product_id] = {'quantity':0,'price':size_.off_price}
                elif size_.price:
                    self.cart[product_id] = {'quantity':0,'price':size_.price}

            else:
                if product.off_price:
                    self.cart[product_id] = {'quantity':0,'price':product.off_price}
                else:
                    self.cart[product_id] = {'quantity':0,'price':product.price}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
   

        self.save()
    
    def save(self):
        self.session.modified = True
    
    #remove from cart
    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
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
        
