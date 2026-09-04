from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies=[("leaves","0001_initial")]
    operations=[
        migrations.CreateModel(name="PublicHoliday",fields=[("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),("date",models.DateField(unique=True)),("name",models.CharField(max_length=200))],options={"ordering":["date"]}),
        migrations.AlterField(model_name="leavetype",name="annual_entitlement",field=models.DecimalField(decimal_places=2,default=21,max_digits=6)),
    ]
