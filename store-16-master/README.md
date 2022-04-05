# Store 16

CMPT 470 Group 16 Project: E-Commerce Book Store

For TA to Note:
1: Pulling to Windows from git caused my computer to convert rc.local to a non unix encoded file. This caused me to get a
   file not found error because of improper line ends that tripped me up for almost 6 hours, since it worked on another 
   team members windows machine. If you get a file not found error at the 'startup' stage in the recipe after doing vargrant
   up please go to notepad++ and change the rc.local file to unix encoding. 

Description:
Our group created an e-commerce web app that can handle buying and selling books. It lists a number of features including login, wishlist, purchase history, shopping cart, reviews, and search options. Currently we do not actually make or validate purchases since all products do not exist. However, they do act in our system as if a purchase has been made.

Features:
Product List - Ability to view all products in a list on main page without login
Create Product - Ability to create a product with authorization for admin and sellers only.
Wishlist - Able to add and remove items from a wishlist unique to each person
Reviews - Able to set reviews for individual products that is displayed on the product page
Shopping Cart - Add items you wish to purchase to the shopping cart 
Purchase History - Able to review your previous purchases unqiue to your account
Seach - Able to search for products based on title or author
Login - Able to create an account and buy products through admin options can be promoted to seller to create products

How to Use:
Admin: go to /admin/ to get to the django Admin portal that also functions as our admin page. To create a seller add an existing user to the seller group, this will allow that user to create products. As an admin you have permission to use all functionality of the program. Due to limitations only admin can create a product that is available to sell on the available product table. 

Buyer:
-Guest: As a guest you can only view products to get any further than that you need to set up an account. To set up an account go to the register page and create a user.
-User: As a basic user you can now buy products, add to wishlist, leave reviews and use most of the functionality of our system. You cannot create products at this level of access.

-Seller: Once you are promoted to a seller by an admin you can create and list products on the site as well as use the basic user functions to buy products and add to wishlist, leave reviews, etc.

Technology Used:
Flickity is used for our carousel on the front page.
https://flickity.metafizzy.co/

Crispy forms is used for our forms
https://django-crispy-forms.readthedocs.io/en/latest/

Bootstrap is used for some of our buttons
https://getbootstrap.com/