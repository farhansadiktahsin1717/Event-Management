# Generated manually to repair transition from auth.User to users.User.
from django.db import migrations


def sync_users_table(apps, schema_editor):
    connection = schema_editor.connection
    existing_tables = set(connection.introspection.table_names())

    if "users_user" not in existing_tables:
        schema_editor.execute(
            """
            CREATE TABLE users_user (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                password varchar(128) NOT NULL,
                last_login datetime NULL,
                is_superuser bool NOT NULL,
                username varchar(150) NOT NULL UNIQUE,
                first_name varchar(150) NOT NULL,
                last_name varchar(150) NOT NULL,
                email varchar(254) NOT NULL,
                is_staff bool NOT NULL,
                is_active bool NOT NULL,
                date_joined datetime NOT NULL,
                profile_picture varchar(100) NOT NULL DEFAULT 'profiles/default_profile.jpg',
                phone_number varchar(20) NOT NULL DEFAULT ''
            )
            """
        )

        if "auth_user" in existing_tables:
            schema_editor.execute(
                """
                INSERT INTO users_user (
                    id, password, last_login, is_superuser, username, first_name, last_name,
                    email, is_staff, is_active, date_joined, profile_picture, phone_number
                )
                SELECT
                    id, password, last_login, is_superuser, username, first_name, last_name,
                    email, is_staff, is_active, date_joined, 'profiles/default_profile.jpg', ''
                FROM auth_user
                """
            )

    if "users_user_groups" not in existing_tables:
        schema_editor.execute(
            """
            CREATE TABLE users_user_groups (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id bigint NOT NULL REFERENCES users_user (id) DEFERRABLE INITIALLY DEFERRED,
                group_id integer NOT NULL REFERENCES auth_group (id) DEFERRABLE INITIALLY DEFERRED
            )
            """
        )
        schema_editor.execute(
            "CREATE UNIQUE INDEX users_user_groups_user_id_group_id_uniq ON users_user_groups (user_id, group_id)"
        )
        schema_editor.execute(
            "CREATE INDEX users_user_groups_user_id_idx ON users_user_groups (user_id)"
        )
        schema_editor.execute(
            "CREATE INDEX users_user_groups_group_id_idx ON users_user_groups (group_id)"
        )
        if "auth_user_groups" in existing_tables:
            schema_editor.execute(
                """
                INSERT INTO users_user_groups (user_id, group_id)
                SELECT user_id, group_id FROM auth_user_groups
                """
            )

    if "users_user_user_permissions" not in existing_tables:
        schema_editor.execute(
            """
            CREATE TABLE users_user_user_permissions (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id bigint NOT NULL REFERENCES users_user (id) DEFERRABLE INITIALLY DEFERRED,
                permission_id integer NOT NULL REFERENCES auth_permission (id) DEFERRABLE INITIALLY DEFERRED
            )
            """
        )
        schema_editor.execute(
            "CREATE UNIQUE INDEX users_user_user_permissions_user_id_permission_id_uniq ON users_user_user_permissions (user_id, permission_id)"
        )
        schema_editor.execute(
            "CREATE INDEX users_user_user_permissions_user_id_idx ON users_user_user_permissions (user_id)"
        )
        schema_editor.execute(
            "CREATE INDEX users_user_user_permissions_permission_id_idx ON users_user_user_permissions (permission_id)"
        )
        if "auth_user_user_permissions" in existing_tables:
            schema_editor.execute(
                """
                INSERT INTO users_user_user_permissions (user_id, permission_id)
                SELECT user_id, permission_id FROM auth_user_user_permissions
                """
            )


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_delete_participant"),
    ]

    operations = [
        migrations.RunPython(sync_users_table, migrations.RunPython.noop),
    ]
