from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
# Create your models here.
# class LocationManager(models.Manager):
# 	def create_location(self, longitude, latitude):
# 		longtitude = self.create(longitude = longitude)
# 		latitude = self.create(latitude = latitude)
# 		return [longtitude, latitude]
#
# class AddressManager(models.Manager):
# 	def create_address(self, line1, city, zip_code, line2 = None):
# 		line1 = self.create(line1 = line1)
# 		line2 =self.create(line2 = line2)
# 		city = self.create(city = city)
# 		zip_code = self.create(zip_code = zip_code)
# 		return [line1, line2, city, zip_code]

# class Building(models.Model):
# 	descr = " "
# 	rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(10.0)])
# 	location = LocationManager()
# 	address = AddressManager()
# 	property_name = models.CharField(max_length=64)

class HousingPost(models.Model):
	descr = " "
	price = models.PositiveIntegerField(validators=[MinValueValidator(0)])
	bedrooms = models.PositiveIntegerField(validators=[MinValueValidator(0)])
	bathrooms = models.PositiveIntegerField(validators=[MinValueValidator(0)])
	# user = models.ForeignKey(User, null=True)
	rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(10.0)], default = 0)
	# location = LocationManager()
	# address = AddressManager()
	longitude = models.FloatField(null = True)
	latitude = models.FloatField(null = True)
	line1 = models.CharField(max_length=95, null = True)
	line2 = models.CharField(max_length=95, null = True)
	city = models.CharField(max_length=35, null = True)
	zip_code = models.CharField(max_length = 16, null = True)
	property_name = models.CharField(max_length=64, null = True)
	title = models.CharField(max_length=64)
	last_updated = models.DateField()
	state_date = models.DateField()
	end_date = models.DateField()
	description = models.CharField(max_length= 2048, null=True)
	num_people = models.PositiveIntegerField(validators=[MinValueValidator(0)], null=True)
	# building = models.ForeignKey(Building)

class Review(models.Model):
	descr = " "
	housing_post= models.ForeignKey(HousingPost)
	user = models.ForeignKey(User)
	title = models.CharField(max_length=64)
	description = models.CharField(max_length= 2048)
	satisfaciton_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
	safety_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

class PostImage(models.Model):
	descr = " "
	housing_post = models.ForeignKey(HousingPost)
	image = models.ImageField()
