import json, time, datetime
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core import serializers
from models import HousingPost
#************* View Handlers ****************

def home(request):
	return render(request, 'index.html')

def signup(request):
	return render(request, 'signup.html')

#************* Search Housing ****************
# /api/housing GET
def get_search_results(request):
	obj = request.GET
	print request.GET
	order_by = obj.get('order_by')
	min_price = obj.get('min_price')
	max_price = obj.get('max_price')
	num_bedrooms = obj.get('num_bedrooms')
	num_bathrooms = obj.get('num_bathrooms')
	# print 'starting'
	# print 'num_bedrooms: ' + str(request.GET.get['num_bedrooms'])
	# print ' num_bathroom: ' + num_bathrooms
	# print ' max_price: ' + max_price
	# print ' min_price ' + min_price 
	# print 'order_by' + order_by

	# address_line = obj.get('address_line')
	# need to be parsed later to do search in db (call google Maps API)
	# page_number = obj.get('page_number')
	# call address manager
	results = HousingPost.objects.filter(bedrooms = num_bedrooms).filter(bathrooms = num_bathrooms).filter(price__lt=max_price).filter(price__gt=min_price).order_by(order_by)	# TODO: check for empty fields
	housing_ids = []
	for result in results:
		housing_ids.append(result.id)
	return JsonResponse({"status": 1, "results": housing_ids})

# /api/housing POST
def make_housing_post(request):
	try:
		housing_json = json.loads(request.body)
		# TODO VIEW Error checking
		errors = check_errors_housing(housing_json)
		if len(errors) == 0:
			housing_post = HousingPost(price = housing_json['price'],
									bedrooms=housing_json['bedrooms'],
									bathrooms=housing_json['bathrooms'],
									# user=request.user, #TODO Figure out how to test with cookies
									longitude=housing_json['longitude'],
									latitude=housing_json['latitude'],
									line1=housing_json['line1'],
									line2=housing_json['line2'],
									city=housing_json['city'],
									zip_code=housing_json['zip_code'],
									property_name=housing_json['property_name'],
									title=housing_json['title'],
									last_updated=datetime.datetime.now(),
									state_date=housing_json['state_date'],
									end_date=housing_json['end_date'],
									description=housing_json['description'],
									num_people=housing_json['num_people'])
			housing_post.save()
			return success_response()
		else:
			return error_response(errors)
	except Exception, e:
		return error_response(e)


def check_errors_housing(housing_json):
	errors = []

	if housing_json['bedrooms'] <0:
		errors.append("Invalid Number of Bedrooms")
	if housing_json['bathrooms'] <0:
		errors.append("Invalid Number of Bathrooms")
	if housing_json['price'] < 0:
		errors.append("Invalid Price")
	if housing_json['rating'] < 0:
		errors.append("Invalid Rating")
	if housing_json['line1'] == '':
		errors.append("Line1 must be nonempty")
	if len(housing_json['line1']) > 95:
		errors.append("Line1 must be fewer than 95 characters")
	if housing_json['line2'] == '':
		errors.append("Line2 must be nonempty")
	if len(housing_json['line2']) > 95:
		errors.append("Line2 must be fewer than 95 characters")


	return errors
#************* Account Authentication ****************

# /api/account POST
def make_account(request):
	account_json = json.loads(request.body)
	if is_account(account_json):
		try:
			user = User.objects.get(email=account_json['email'])
			return error_response('Account with email: '
								  + account_json['email'] + ' already exists.')
		except User.DoesNotExist, e:
			errors = check_errors_account(account_json)
			if len(errors) == 0:
				user = create_user(account_json)
				user.save()
				logged_in_user = authenticate(username=account_json['email'],
											  password=account_json['password'])
				print logged_in_user
				login(request, logged_in_user)
				return success_response()
			else:
				return error_response(errors)
		except Exception, e:
			return error_response(e)
	else:
		return error_response('Ill Formed JSON: Missing one or more keys')

def create_user(account_json):
	user = User.objects.create_user( account_json['email'], account_json['email'],
									 account_json['password'])
	user.first_name = account_json['first_name']
	user.last_name = account_json['last_name']
	return user

def is_account(account_json):
	return ( ('email' in account_json) and ('password' in account_json)
			 and ('first_name' in account_json) and ('last_name' in account_json) )

def check_errors_account(account_json):
	errors = []
	if len(account_json['email']) > 256:
		errors.append("Email address must be 256 characters or less")
	if len(account_json['first_name']) > 32:
		errors.append("First Name must be 32 characters or less")
	if len(account_json['last_name']) > 32:
		errors.append("Last Name must be 32 characters or less")
	if len(account_json['password']) > 128:
		errors.append("Password must be 128 characters or less")
	if account_json['email'] == '':
		errors.append("Email address must be nonempty")
	if account_json['first_name'] == '':
		errors.append("First name must be nonempty")
	if account_json['last_name'] == '':
		errors.append("Last name must be nonempty")
	if account_json['password'] == '':
		errors.append("Password must be nonempty")
	if not is_email(account_json['email']):
		print account_json['email']
		errors.append("Malformed Email Address")
	return errors

def name_from_email(email):
	name = ""
	for char in email:
		if char == '@':
			return name
		else:
			name += char
	return None

def is_email(email):
	for char in email:
		if char == "@":
			return True
	return False

# /api/login POST
def login_account(request):
	account_json = json.loads(request.body)
	user = authenticate(username=account_json['email'], password=account_json['password'])
	if user is not None:
		if user.is_active:
			login(request, user)
			print user, "logged in."
			return success_response()
		else:
			return error_response("Your account has been disabled. Check your email for details")
	else:
		return error_response("Your account does not exist!")

# /api/account DELETE
def delete_testing_accounts(request):
	try:
		testing_users = User.objects.filter(email=TESTING_EMAIL)
		for u in testing_users:
			u.delete()
		return success_response()
	except Exception, e:
		return error_response(e)

#************* API Handlers ****************

def account(request):
	print "**********API**********", request.method
	if request.method == 'POST':
		return make_account(request)
	if request.method == 'DELETE':
		return delete_testing_accounts(request)

def login_api(request):
	print "**********API**********", request.method
	if request.method == 'POST':
		return login_account(request)

def handle_search(request):
	if request.method == 'GET':
		return get_search_results(request)
	elif request.method == 'POST':
		return make_housing_post(request)
	return

def handle_full_post(request, post_id):
	post = HousingPost.objects.filter(id = post_id)
	# TODO: logic to add review for posts / like a post
	return HttpResponse(serializers.serialize("json", post))

#************* Helper Functions ****************
def success_response():
	return JsonResponse({'status': 1})

def error_response(errors):
	if isinstance(errors, list):
		for e in errors:
			print "***********", e
		return JsonResponse({'status': -1,
							 'errors': errors,
							})
	else:
		print "***********", errors
		return JsonResponse({'status': -1,
							 'errors': [str(errors)],
							})

TESTING_EMAIL = 'testing@cs169.com'

# Use this line to see if a user is currently logged in
# request.user.is_authenticated()
