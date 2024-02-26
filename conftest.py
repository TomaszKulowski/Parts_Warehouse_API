from django.test.runner import DiscoverRunner


class DatabaseConnectionCleanupTestRunner(DiscoverRunner):
    def teardown_databases(self, old_config, **kwargs):
        """This method was override to address a MongoDB database error that occurred
        when the application interacts with MongoDB. It provides a workaround or fix
        to prevent the database error from being raised during the execution tests of the
        application.
        """
