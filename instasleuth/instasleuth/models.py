from django.db import models

class UserPoints(models.Model):
	user_id = models.AutoField(primary_key=True)
	user_name = models.CharField(max_length=100)
	user_points = models.IntegerField(max_length=100)


class UserData(models.Model):
	user_id_fk = models.ForeignKey(UserPoints, db_column="user_id")
	user_name = models.CharField(max_length=100)
	user_pan = models.CharField(max_length=100)
	user_dob = models.CharField(max_length=100)
	user_image_url = models.CharField(max_length=1000, default='http://34.227.56.111/static/5.jpg')
	user_correction_timestamp = models.DateTimeField(auto_now_add=True, blank=True)


