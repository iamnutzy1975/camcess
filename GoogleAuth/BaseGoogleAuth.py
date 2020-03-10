class BaseGoogleAuth(object):
    """Represents base class for all the different ways Google authentication works"""

    def __init__(self, scope):
        assert isinstance(scope, list)

        self.scope = scope
        self.http = None

    def addScope(self, scope):
        """Adds scope or scopes to the scope list.
           Accept scope as string or multiple scopes in list
        """

        def addSingleScope(s):
            if not s in self.scope:
                self.scope.append(s)

        if isinstance(scope, str):
            addSingleScope(scope)

        elif isinstance(scope, list):
            for s in scope:
                addSingleScope(s)


    def authorize(self):
        raise NotImplementedError()

    def getHttpObject(self):
        if self.http is None:
            raise Exception("authorize was not called on Google auth object - http obect is None")

        return self.http
