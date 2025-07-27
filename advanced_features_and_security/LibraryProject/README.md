# Django Permissions and Groups Setup

## Overview

This project demonstrates managing user permissions and groups in a Django application. 

## Permissions Created

- `can_view`: Permission to view model instances.
- `can_create`: Permission to create new model instances.
- `can_edit`: Permission to edit existing model instances.
- `can_delete`: Permission to delete model instances.

## User Groups

- **Viewers**: Can only view.
- **Editors**: Can view, create, and edit.
- **Admins**: Can view, create, edit, and delete.

## Usage

- Assign users to one or more groups to grant them permissions.
- Views are protected with Django's `@permission_required` decorator to enforce access control.
- Test the permissions by logging in as users with different group assignments.

## Notes

- The custom permissions are defined in the model's `Meta` class.
- Groups and permissions are managed through the Django admin interface.
