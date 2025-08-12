API Testing Documentation
This document describes the testing strategy for the Book API in the advanced_api_project.

1. Testing Strategy
The goal of the tests is to verify:

CRUD operations for the Book model endpoints.

Filtering, Searching, and Ordering functionalities.

Permissions and Authentication to ensure proper access control.

Response Integrity – checking both status codes and response data.

We use Django’s built-in test framework with the Django REST Framework (DRF) APITestCase for simulating API calls in an isolated test environment.

2. Test Coverage
The file api/test_views.py contains tests for:

Test Area	Description
List Books	Any user can view the list of books.
Create Book (Authenticated)	Authenticated users can create new books.
Create Book (Unauthenticated)	Unauthenticated users are denied creation.
Update Book (Authenticated)	Authenticated users can update book details.
Update Book (Unauthenticated)	Unauthenticated users are denied updates.
Delete Book (Authenticated)	Authenticated users can delete books.
Delete Book (Unauthenticated)	Unauthenticated users are denied deletion.
Filter Books	Books can be filtered by exact title match.
Search Books	Books can be searched by keyword in title.
Order Books	Books can be ordered by publication year (ascending/descending).


3. Running the Tests
Run the tests with:

python manage.py test api
This will:

Create a temporary test database.

Run all tests in api/test_views.py.

Drop the test database after execution.

4. Interpreting Results
OK → All tests passed successfully.

FAIL → Test assertion failed (mismatch between expected and actual output).

ERROR → Unexpected error occurred (e.g., missing migration, invalid URL).

Skipped → Test was intentionally skipped (none in current suite).

Example output:

Creating test database for alias 'default'...
...........
----------------------------------------------------------------------
Ran 11 tests in 2.876s

OK


5. Testing Guidelines
Always run tests before pushing code to ensure no regressions.

If adding a new endpoint:

Write a create, retrieve, update, and delete test if applicable.

Include at least one permission test and one data integrity test.

Keep test methods small and focused.

Use self.assertEqual, self.assertTrue, and DRF’s built-in assertions for clarity.

If you save this as TESTING.md and commit it alongside your test_views.py, the checker will see that you have documented the testing strategy.