from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import server.models.commands.util
import server.models.fields
import server.models.module_version


# To generate this file:
# 1. AVOID django's squashmigrations. Its migration errors because each step
#    uses our app's models, which may be long-gone or whose fields may be gone
#    by the time the step is run.
# 2. python ./manage.py squashmigrations server NNNN -- just to generate the
#    `replaces` line, which is the only line that has any value
# 2. mkdir t && mv server/migrations/* t
# 3. bin/dev sql -c "DELETE FROM django_migrations WHERE app = 'server'"
# 4. bin/dev python ./manage.py makemigrations server
# 5. copy/paste the `sites` dependency and the `django_sites` RunSQL from
#    t/0001_squashed_... into the new migration
# 6. copy/paste the `replaces` line from t/0001_squashed_... into the new
#    migration
# 7. copy/paste this comment into the migration
# 8. Rename the new migration to 0001_squashed_... (same name as in the t/
#    directory
# 9. rm t/0001_squashed_*
# 10. mv t/* server/migrations/
# 11. (after everybody everywhere has applied the migration): remove the
#     `replaces` line and delete all the replaced migrations.
#
# And presto! A succinct migration. It works because our app allows all tables
# to start empty. (`./manage.py reload-*-modules` populates all the data we
# need.)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(sql=[
            """
            UPDATE django_site
            SET domain = 'app.workbenchdata.com', name = 'Workbench';
            """
        ]),
        migrations.CreateModel(
            name='AclEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=254, verbose_name='email')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('can_edit', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Delta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='datetime')),
            ],
            options={
                'base_manager_name': 'base_objects',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ModuleVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_name', models.CharField(max_length=200)),
                ('source_version_hash', models.CharField(default='1.0', max_length=200)),
                ('last_update_time', models.DateTimeField(auto_now=True)),
                ('spec', django.contrib.postgres.fields.jsonb.JSONField(validators=[server.models.module_version._django_validate_module_spec], verbose_name='spec')),
                ('js_module', models.TextField(default='', verbose_name='js_module')),
            ],
            options={
                'ordering': ['last_update_time'],
            },
        ),
        migrations.CreateModel(
            name='StoredObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bucket', models.CharField(blank=True, default='', max_length=255)),
                ('key', models.CharField(blank=True, default='', max_length=255)),
                ('stored_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('hash', models.CharField(max_length=32)),
                ('metadata', models.CharField(default=None, max_length=255, null=True)),
                ('size', models.IntegerField(default=0)),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(db_index=False, null=True)),
                ('name', models.TextField()),
                ('position', models.IntegerField()),
                ('selected_wf_module_position', models.IntegerField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('size', models.IntegerField(default=0)),
                ('uuid', models.CharField(max_length=255)),
                ('bucket', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WfModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_id_name', models.CharField(default='', max_length=200)),
                ('order', models.IntegerField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('stored_data_version', models.DateTimeField(blank=True, null=True)),
                ('is_collapsed', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('auto_update_data', models.BooleanField(default=False)),
                ('next_update', models.DateTimeField(blank=True, null=True)),
                ('update_interval', models.IntegerField(default=86400)),
                ('last_update_check', models.DateTimeField(blank=True, null=True)),
                ('notifications', models.BooleanField(default=False)),
                ('has_unseen_notification', models.BooleanField(default=False)),
                ('cached_render_result_delta_id', models.IntegerField(blank=True, null=True)),
                ('cached_render_result_status', models.CharField(blank=True, choices=[('ok', 'ok'), ('error', 'error'), ('unreachable', 'unreachable')], max_length=20, null=True)),
                ('cached_render_result_error', models.TextField(blank=True)),
                ('cached_render_result_json', models.BinaryField(blank=True)),
                ('cached_render_result_quick_fixes', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list)),
                ('cached_render_result_columns', server.models.fields.ColumnsField(blank=True, null=True)),
                ('cached_render_result_nrows', models.IntegerField(blank=True, null=True)),
                ('is_busy', models.BooleanField(default=False)),
                ('fetch_error', models.CharField(blank=True, max_length=2000, verbose_name='fetch_error')),
                ('last_relevant_delta_id', models.IntegerField(default=0)),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('secrets', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('tab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wf_modules', to='server.Tab')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('anonymous_owner_session_key', models.CharField(blank=True, max_length=40, null=True, verbose_name='anonymous_owner_session_key')),
                ('original_workflow_id', models.IntegerField(blank=True, null=True)),
                ('public', models.BooleanField(default=False)),
                ('example', models.BooleanField(default=False)),
                ('in_all_users_workflow_lists', models.BooleanField(default=False)),
                ('lesson_slug', models.CharField(blank=True, max_length=100, null=True, verbose_name='lesson_slug')),
                ('selected_tab_position', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='AddModuleCommand',
            fields=[
                ('delta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Delta')),
                ('wf_module_delta_ids', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2), size=None)),
                ('wf_module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='server.WfModule')),
            ],
            options={
                'abstract': False,
            },
            bases=('server.delta', server.models.commands.util.ChangesWfModuleOutputs),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='AddTabCommand',
            fields=[
                ('delta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Delta')),
                ('old_selected_tab_position', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('server.delta',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ChangeDataVersionCommand',
            fields=[
                ('delta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Delta')),
                ('wf_module_delta_ids', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2), size=None)),
                ('old_version', models.DateTimeField(null=True, verbose_name='old_version')),
                ('new_version', models.DateTimeField(verbose_name='new_version')),
                ('wf_module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='server.WfModule')),
            ],
            options={
                'abstract': False,
            },
            bases=('server.delta', server.models.commands.util.ChangesWfModuleOutputs),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ChangeParametersCommand',
            fields=[
                ('delta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Delta')),
                ('wf_module_delta_ids', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2), size=None)),
                ('old_values', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='old_values')),
                ('new_values', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='new_values')),
                ('wf_module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='server.WfModule')),
            ],
            options={
                'abstract': False,
            },
            bases=('server.delta', server.models.commands.util.ChangesWfModuleOutputs),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ChangeWfModuleNotesCommand',
            fields=[
                ('delta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Delta')),
                ('new_value', models.TextField(verbose_name='new_value')),
                ('old_value', models.TextField(verbose_name='old_value')),
                ('wf_module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='server.WfModule')),
            ],
            options={
                'abstract': False,
            },
            bases=('server.delta',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ChangeWorkflowTitleCommand',
            fields=[
                ('delta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Delta')),
                ('new_value', models.TextField(verbose_name='new_value')),
                ('old_value', models.TextField(verbose_name='old_value')),
            ],
            options={
                'abstract': False,
            },
            bases=('server.delta',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='DeleteModuleCommand',
            fields=[
                ('delta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Delta')),
                ('wf_module_delta_ids', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2), size=None)),
                ('wf_module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='server.WfModule')),
            ],
            options={
                'abstract': False,
            },
            bases=('server.delta', server.models.commands.util.ChangesWfModuleOutputs),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='DeleteTabCommand',
            fields=[
                ('delta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Delta')),
            ],
            options={
                'abstract': False,
            },
            bases=('server.delta',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='InitWorkflowCommand',
            fields=[
                ('delta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Delta')),
            ],
            options={
                'abstract': False,
            },
            bases=('server.delta',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ReorderModulesCommand',
            fields=[
                ('delta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Delta')),
                ('wf_module_delta_ids', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2), size=None)),
                ('old_order', models.TextField()),
                ('new_order', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('server.delta', server.models.commands.util.ChangesWfModuleOutputs),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ReorderTabsCommand',
            fields=[
                ('delta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Delta')),
                ('wf_module_delta_ids', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2), size=None)),
                ('old_order', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('new_order', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('server.delta', server.models.commands.util.ChangesWfModuleOutputs),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SetTabNameCommand',
            fields=[
                ('delta_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='server.Delta')),
                ('wf_module_delta_ids', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=2), size=None)),
                ('old_name', models.TextField()),
                ('new_name', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('server.delta', server.models.commands.util.ChangesWfModuleOutputs),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='workflow',
            name='last_delta',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='+', to='server.Delta'),
        ),
        migrations.AddField(
            model_name='workflow',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_workflows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='wf_module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_files', to='server.WfModule'),
        ),
        migrations.AddField(
            model_name='tab',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tabs', to='server.Workflow'),
        ),
        migrations.AddField(
            model_name='storedobject',
            name='wf_module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stored_objects', to='server.WfModule'),
        ),
        migrations.AlterUniqueTogether(
            name='moduleversion',
            unique_together=set([('id_name', 'last_update_time')]),
        ),
        migrations.AddField(
            model_name='delta',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_server.delta_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='delta',
            name='prev_delta',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_delta', to='server.Delta'),
        ),
        migrations.AddField(
            model_name='delta',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deltas', to='server.Workflow'),
        ),
        migrations.AddField(
            model_name='aclentry',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acl', to='server.Workflow'),
        ),
        migrations.AlterUniqueTogether(
            name='tab',
            unique_together=set([('workflow', 'slug')]),
        ),
        migrations.AddField(
            model_name='settabnamecommand',
            name='tab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='server.Tab'),
        ),
        migrations.AddField(
            model_name='reordermodulescommand',
            name='tab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='server.Tab'),
        ),
        migrations.AddField(
            model_name='deletetabcommand',
            name='tab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='server.Tab'),
        ),
        migrations.AddField(
            model_name='addtabcommand',
            name='tab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='server.Tab'),
        ),
        migrations.AlterUniqueTogether(
            name='aclentry',
            unique_together=set([('workflow', 'email')]),
        ),
    ]
