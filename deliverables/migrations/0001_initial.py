# Generated by Django 3.1.4 on 2020-12-16 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConditionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Deliverable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=50)),
                ('format', models.CharField(choices=[('XLS', 'Excel tool'), ('PPT', 'PowerPoint deck'), ('PBI', 'Power BI dashboard'), ('TBL', 'Tableau dashboard')], max_length=50)),
                ('scope', models.CharField(blank=True, max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_the_reference_deliverable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DeliverableType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SpecificationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='deliverables.specificationtype')),
                ('deliverable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='deliverables.deliverable')),
            ],
        ),
        migrations.AddField(
            model_name='deliverable',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deliverables.deliverabletype'),
        ),
    ]
